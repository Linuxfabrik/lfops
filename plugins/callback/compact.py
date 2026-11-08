#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import multiprocessing
import os
import re
import sys

from ansible import constants as C
from ansible.playbook.task_include import TaskInclude
from ansible.plugins.callback.default import CallbackModule as Default
from ansible.utils.color import ANSIBLE_COLOR, stringc

DOCUMENTATION = r"""
  name: compact
  type: stdout
  version_added: "10.0.0"
  short_description: Compact output, one block per task, ok and skipped hosts summarized
  description:
    - Prints one block per task, with the role and the task name on lines of their own.
    - While the task runs, every host result appends an asterisk in the color of its status (ok, changed, skipped, failed, unreachable), so the asterisks add up to a progress bar.
    - After the task, unchanged ok and skipped hosts are listed in one C(ok) and one C(skipped) line. Host names that share the part up to the last dash and the delegation target are merged in bash brace expansion syntax, for example C(web-{01,02} > localhost).
    - While a task runs, only the progress bar and failures are printed. At its end, the changed hosts follow, grouped by identical output (the diff, or without a diff the C(msg), C(results), C(stdout) and C(stderr) of the result, where modules report what they changed), then the ok and skipped hosts, then the warnings.
    - Failed and unreachable results are printed as usual, with C(msg), C(stdout), C(stderr), C(module_stdout) and C(module_stderr) as plain text below the JSON, so tracebacks stay readable.
    - Warnings are grouped by text and list the hosts they occurred on. A host name within a warning of Ansible itself (for example from a lookup) is replaced by C(<host>) for the grouping.
    - Failures that a task accepts with C(ignore_errors) are shown in one C(ignored) line per message with the hosts, not as a full result (C(--verbose) shows the full result).
    - At the end of the run, a report in Markdown lists each distinct message once with the hosts it occurred on, in sections by severity (FATAL, UNREACHABLE, WARNING, IGNORED, CHANGED), within a section one list per role (or playbook) with the task names in task order.
  author:
    - Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
  notes:
    - Under ansible-navigator, set the environment variable C(ANSIBLE_STDOUT_CALLBACK). ansible-runner replaces the stdout callback with its own wrapper, which only builds on this variable and ignores C(stdout_callback) in C(ansible.cfg). The terminal needs at least 65 columns there, since ansible-runner writes 64 characters wide invisible event markers, which wrap and become visible on a narrower terminal, with any stdout callback.
    - Made for the linear strategies (C(linear), C(mitogen_linear)), which run one task on all hosts before the next. With C(free) or C(host_pinned), the progress bar and the host lists of concurrent tasks mix.
  extends_documentation_fragment:
    - ansible.builtin.default_callback
    - ansible.builtin.result_format_callback
  requirements:
    - set as stdout callback in the configuration
"""

EXAMPLES = r"""
# ansible.cfg
[defaults]
stdout_callback = linuxfabrik.lfops.compact

# ansible-navigator.yml
ansible-navigator:
  execution-environment:
    environment-variables:
      set:
        ANSIBLE_STDOUT_CALLBACK: 'linuxfabrik.lfops.compact'
"""


def _task(result):
    # ansible-core 2.19 added `task`, `host` and `result` and deprecated the
    # underscore names for removal in 2.23.
    return result.task if hasattr(result, 'task') else result._task


def _host(result):
    return result.host if hasattr(result, 'host') else result._host


def _res(result):
    return result.result if hasattr(result, 'result') else result._result


def compact_hosts(hosts):
    """Join sorted host labels, merging hosts that share the part up to the last "-"
    and the delegation target, in bash brace expansion syntax:
    "web-01, web-02" -> "web-{01,02}",
    "web-01 -> localhost, web-02 -> localhost" -> "web-{01,02} > localhost".
    """
    # (prefix, delegate) -> suffixes, in order of first appearance. A host without
    # "-" gets a group of its own, keyed by its full name.
    groups = {}
    for label in sorted(set(hosts)):
        # host_label() renders delegated results as "host -> delegate"
        host, _, delegate = label.partition(' -> ')
        prefix, sep, suffix = host.rpartition('-')
        key = (prefix + sep, delegate) if sep else (host, delegate, None)
        groups.setdefault(key, []).append(suffix if sep else '')
    parts = []
    for (prefix, delegate, *_), suffixes in groups.items():
        if len(suffixes) > 1:
            part = f'{prefix}{{{",".join(suffixes)}}}'
        else:
            part = f'{prefix}{suffixes[0]}'
        parts.append(f'{part} > {delegate}' if delegate else part)
    return ', '.join(parts)


class CallbackModule(Default):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'linuxfabrik.lfops.compact'

    # Prefixes the default callback caches per task, see _task_start()
    _BANNER_PREFIX = {  # noqa: RUF012
        'CLEANUP TASK': 'Cleanup',
        'RUNNING HANDLER': 'Handler',
        'TASK': 'Task',
    }

    # Result fields shown below "changed: host" when there is no diff. In display
    # order, not sorted: the message first, then the output in the order a shell
    # shows it.
    _CHANGE_DETAIL_FIELDS = ('msg', 'results', 'stdout', 'stderr')

    # Result fields that _dump_results() prints as plain text below the JSON, in
    # display order like above
    _PLAIN_TEXT_FIELDS = ('msg', 'stdout', 'stderr', 'module_stdout', 'module_stderr')

    _BAR_CHAR = '*'

    # Cursor up one line, see _bar()
    _CURSOR_UP = '\033[A'

    def __init__(self):
        super().__init__()
        # (host, task uuid) -> number of diffs already printed with a header
        self._diff_printed = {}
        # (kind, role or playbook, task name, message) -> host names, in order of
        # first appearance, for the report at the end
        self._report = {}
        # (host, task uuid, message) of the warnings in the report
        self._reported_warnings = set()
        # ignored failures of the running task: message -> host labels
        self._ignored = {}
        self._ok_hosts = []
        self._skipped_hosts = []
        # Output collected while a task runs, printed grouped at its end:
        # grouping key -> [header suffix, body lines, host labels]
        self._changes = {}
        # (host label or None, text)
        self._task_warnings = []
        # host names with a result so far, to find them in the text of warnings
        self._seen_hosts = set()
        # host names with a result in the running task
        self._task_hosts = set()
        # the running task, None between tasks
        self._task = None
        # header line of the play, and of the current section (role or play)
        self._play_line = 'Play'
        self._section = None
        # warnings printed outside of a task, Ansible shows each text only once
        self._warned = set()
        # State of the progress bar: whether it is open (more results may follow)
        # and the (char, color) pairs of its current line
        self._line_open = False
        self._line_chars = []
        # ansible-runner (ansible-navigator) writes an invisible event marker per
        # callback event at the cursor: base64 data (64 characters for the begin
        # marker), then "ESC[<n>D" and "ESC[K" to move back and erase it
        # (ansible_runner/display_callback/callback/awx_display.py). Behind a bar
        # that reaches the right terminal edge, such a marker wraps and stays
        # visible. On a terminal, the bar is therefore terminated after every
        # asterisk, so the cursor and the markers sit on the empty line below it,
        # and the next asterisk redraws the bar line from there. Without a terminal
        # (log, pipe, CI), the asterisks are simply appended.
        self._redraw = sys.stdout.isatty()
        # Terminate an open bar line before anything else is printed, including
        # warnings from Ansible itself. Display is a singleton, so this patch also
        # covers output that does not come from this callback.
        self._display_orig = self._display.display
        self._display.display = self._display_wrapper
        # Catch the warnings of Ansible itself (lookups, templating) before Display
        # wraps them, to group them at the end of the task. ansible-core 2.19+ hands
        # them to the main process as a WarningSummary via Display._warning, before
        # that Display.warning formats them in the worker process.
        if hasattr(type(self._display), '_warning'):
            self._warning_orig = self._display._warning
            self._display._warning = self._warning_summary_hook
        else:
            self._warning_orig = self._display.warning
            self._display.warning = self._warning_hook

    # Prefix of a warning text that a worker process sends to the main process
    _WARNING_MARK = '\x00linuxfabrik.lfops.compact warning\x00'

    def _warning_hook(self, msg, *args, **kwargs):
        # ansible-core before 2.19. Takes the `formatted` argument of Display.warning()
        # and ignores it, the text is never wrapped here.
        if multiprocessing.parent_process() is not None:
            # A worker process: send the unwrapped text through the proxied
            # display() to the main process, see _display_wrapper().
            self._display.display(self._WARNING_MARK + msg, stderr=True)
            return
        self._foreign_warning(msg)

    def _warning_summary_hook(self, warning):
        # ansible-core 2.19+
        if multiprocessing.parent_process() is not None:
            # a worker process, the original proxies it to the main process
            self._warning_orig(warning)
            return
        self._foreign_warning(warning.event.msg)

    def _foreign_warning(self, text):
        if self._task is not None:
            self._task_warnings.append((None, text))
            return
        if text not in self._warned:
            self._warned.add(text)
            self._close_line()
            self._display_orig(f'[WARNING]: {text}', color=C.COLOR_WARN, stderr=True)

    def _display_wrapper(self, msg, *args, **kwargs):
        # in a worker process, the proxied display() carries it to the main process
        if (
            isinstance(msg, str)
            and msg.startswith(self._WARNING_MARK)
            and multiprocessing.parent_process() is None
        ):
            self._foreign_warning(msg[len(self._WARNING_MARK) :])
            return None
        # Forked workers proxy their output to the main process and only carry a
        # stale copy of the line state.
        if (
            self._line_open
            and not kwargs.get('log_only')
            and multiprocessing.parent_process() is None
        ):
            self._close_line()
        return self._display_orig(msg, *args, **kwargs)

    def _display_styled(self, styled, plain):
        """Show styled text on screen, but keep escape codes out of the log."""
        self._display.display(styled, screen_only=True)
        self._display_orig(plain, log_only=True)

    def _close_line(self):
        if self._line_open:
            self._line_open = False
            self._line_chars = []
            if not self._redraw:
                self._display_orig('', screen_only=True)

    def _bar(self, color):
        # One column less than the terminal, so a full line never triggers the
        # terminal's own wrap. Not Display.columns, which is at least 79 even on a
        # narrower terminal. Asked on every call to follow a resized terminal.
        try:
            width = os.get_terminal_size(sys.stdout.fileno()).columns - 1
        except (OSError, ValueError):
            width = self._display.columns or 79
        width = max(width, 1)
        if self._line_open and len(self._line_chars) >= width:
            # the line is full, continue on the next one
            if not self._redraw:
                self._display_orig('', screen_only=True)
            self._line_chars = []
        # screen_only: the progress bar does not belong in the log file
        if self._redraw:
            redraw_line = self._line_open and bool(self._line_chars)
            self._line_chars.append((self._BAR_CHAR, color))
            line = ''.join(stringc(char, col) for char, col in self._line_chars)
            if redraw_line:
                line = self._CURSOR_UP + '\r' + line
            self._display_orig(line, screen_only=True)
        else:
            self._line_chars.append((self._BAR_CHAR, color))
            self._display_orig(
                self._BAR_CHAR, color=color, newline=False, screen_only=True
            )
        sys.stdout.flush()
        self._line_open = True

    @staticmethod
    def _warning_texts(result):
        res = _res(result)
        if not res.get('warnings') or not getattr(C, 'ACTION_WARNINGS', True):
            return []
        # ansible-core 2.19+ keeps the warnings as WarningSummary objects on the
        # task result, before that they are strings in the result dict.
        summaries = getattr(result, 'warnings', None)
        if summaries:
            return [summary.event.msg for summary in summaries]
        return [str(warning) for warning in res['warnings']]

    def _record(self, result, kind, messages):
        """Remember a result for the summary at the end of the run. `messages` is a
        list; one entry is recorded per message, `[None]` records one without.
        """
        host, task = _host(result).get_name(), _task(result)
        if kind == 'warning':
            # Before ansible-core 2.19, a loop repeats the warnings of its items
            # with its final result, under the task name with the loop variable
            # not rendered. Record each warning once per host and task.
            keys = [(host, task._uuid, message) for message in messages]
            messages = [
                message
                for key, message in zip(keys, messages)
                if key not in self._reported_warnings
            ]
            self._reported_warnings.update(keys)
        self._record_entry(host, kind, task, messages)

    def _source_and_name(self, task):
        """The role of a task (or the playbook, for its own tasks) and its name."""
        name = task.get_name().strip()
        if '<< error ' in name:
            # ansible-core 2.19+ renders a name with a variable it cannot resolve,
            # like the loop variable, as "<< error 1 - 'item' is undefined >>",
            # take the name as it is written in the playbook instead
            raw = (task.get_ds() or {}).get('name')
            if isinstance(raw, str):
                name = raw.strip()
        if task._role:
            # Task.get_name() renders role tasks as "<role> : <name>"
            source = task._role.get_name()
            return source, name.removeprefix(f'{source} : ')
        return self._play.get_name().strip().removeprefix('Playbook '), name

    def _record_entry(self, host, kind, task, messages):
        if not messages:
            return
        source, name = self._source_and_name(task)
        for message in messages:
            hosts = self._report.setdefault((kind, source, name, message), [])
            if host not in hosts:
                hosts.append(host)

    def _warnings(self, result):
        """Collect the warnings of a result for the end of the task and record them
        for the summary. Ansible itself would print a warning text only once per run
        and without the host, so it does not get them.
        """
        texts = self._warning_texts(result)
        label = self.host_label(result)
        self._task_warnings.extend((label, text) for text in texts)
        self._record(result, 'warning', texts)
        _res(result).pop('warnings', None)
        # deprecations and exceptions stay with Ansible
        if hasattr(self, '_handle_warnings_and_exception'):
            # ansible-core 2.19+
            self._handle_warnings_and_exception(result)
        else:
            self._handle_warnings(_res(result))

    def _flush_hosts(self):
        """Print what was collected during the task: the changes, grouped by
        identical output, the ok and skipped hosts, and the warnings.
        """
        self._close_line()
        for suffix, body, hosts in self._changes.values():
            self._display.display(
                f'changed: {self._host_list(hosts)}{suffix}', color=C.COLOR_CHANGED
            )
            for line in body:
                self._display.display(line)
        self._changes.clear()
        for message, hosts in self._ignored.items():
            self._display.display(
                f'ignored: {self._host_list(hosts)}', color=C.COLOR_SKIP
            )
            self._display.display(f'  {message}')
        self._ignored.clear()
        self._print_ok_skipped()
        self._ok_hosts.clear()
        self._skipped_hosts.clear()
        self._flush_warnings()
        self._task = None
        self._task_hosts.clear()

    def _print_ok_skipped(self):
        for label, hosts, color in (
            ('ok', self._ok_hosts, C.COLOR_OK),
            ('skipped', self._skipped_hosts, C.COLOR_SKIP),
        ):
            if hosts:
                self._display.display(f'{label}: {self._host_list(hosts)}', color=color)

    def _saw(self, result):
        name = _host(result).get_name()
        self._seen_hosts.add(name)
        self._task_hosts.add(name)

    def _host_list(self, labels):
        """compact_hosts(), or "all <n> hosts" if `labels` covers every host with a
        result in this task, which spares the same long list on task after task.
        """
        names = {label.partition(' -> ')[0] for label in labels}
        delegates = {label.partition(' -> ')[2] for label in labels}
        if len(names) > 1 and names == self._task_hosts and len(delegates) == 1:
            delegate = delegates.pop()
            text = f'all {len(names)} hosts'
            return f'{text} > {delegate}' if delegate else text
        return compact_hosts(labels)

    def _find_host(self, text):
        """Return the first known host name in `text` and the text with all of
        its occurrences replaced by "<host>", or (None, text).
        """
        # longest first, so "web-1" does not match within "web-10"
        for host in sorted(self._seen_hosts, key=len, reverse=True):
            pattern = rf'(?<![\w-]){re.escape(host)}(?![\w-])'
            if re.search(pattern, text):
                return host, re.sub(pattern, '<host>', text)
        return None, text

    def _flush_warnings(self):
        # text -> host labels, in order of first appearance
        groups = {}
        for host, text in self._task_warnings:
            if host is None:
                host, text = self._find_host(text)
                if host is not None and self._task is not None:
                    self._record_entry(host, 'warning', self._task, [text])
            hosts = groups.setdefault(text, [])
            if host is not None:
                hosts.append(host)
        self._task_warnings.clear()
        for text, hosts in groups.items():
            self._display.display(f'[WARNING]: {text}', color=C.COLOR_WARN, stderr=True)
            if hosts:
                self._display.display(
                    f'  on {self._host_list(hosts)}', color=C.COLOR_WARN, stderr=True
                )

    def _dump_results(self, result, *args, **kwargs):
        # Print multi-line text fields (tracebacks, command output) as plain text
        # below the JSON instead of as escaped one-line JSON strings.
        saved = {
            key: result.pop(key) for key in self._PLAIN_TEXT_FIELDS if key in result
        }
        try:
            output = super()._dump_results(result, *args, **kwargs)
        finally:
            result.update(saved)
        for key in self._PLAIN_TEXT_FIELDS:
            if saved.get(key):
                output += f'\n\n{key.upper()}:\n\n{saved[key]}\n'
        return output

    def _banner_parts(self, task):
        """Return the section header (role or playbook), the prefix ("Task",
        "Handler", ...) and the rest of the banner line of a task.
        """
        args = ''
        if not task.no_log and C.DISPLAY_ARGS_TO_STDOUT:
            args = ' ' + ', '.join(f'{k}={v}' for k, v in task.args.items())
        prefix = self._BANNER_PREFIX.get(
            self._task_type_cache.get(task._uuid, 'TASK'), 'Task'
        )
        name = self._last_task_name
        if name is None:
            name = task.get_name().strip()
        if task._role:
            # Task.get_name() renders role tasks as "<role> : <name>"
            role = task._role.get_name()
            name = name.removeprefix(f'{role} : ')
            section = f'Role: {role}'
        else:
            section = self._play_line
        return section, prefix, f'{name}{args}'

    def _print_task_banner(self, task):
        # "Role: x" / "Task: y" instead of "TASK [x : y] ****". Mirrors the default
        # callback, minus the check mode marker (the run starts with a DRY RUN banner
        # anyway).
        section, prefix, line = self._banner_parts(task)
        self._display.display('')
        # The tasks are grouped in sections, one per role and one for the tasks of
        # the playbook itself, with a bold header line whenever the section changes.
        if section != self._section:
            self._section = section
            self._bold(section)
        self._display_styled(
            f'{stringc(f"{prefix}:", "green")} {line}', f'{prefix}: {line}'
        )
        if self._display.verbosity >= 2:
            self._print_task_path(task)
        self._last_task_banner = task._uuid

    def _task_start(self, task, prefix=None):
        self._flush_hosts()
        self._task = task
        super()._task_start(task, prefix)
        # The default callback defers the banner when ok/skipped results are hidden.
        # Print it right away instead, unless it was already printed.
        # _last_task_name is None for the free/host_pinned strategies, where the
        # default callback also never prints the banner on task start.
        if self._last_task_name is not None and self._last_task_banner != task._uuid:
            self._print_task_banner(task)

    def _add_change(self, result, body, item=False):
        """Collect a changed host for the end of the task, grouped with the hosts
        whose output has the same lines (in any order, e.g. restorecon -v).
        """
        label = self._short_label(self._get_item_label(_res(result)))
        suffix = f' (item={label})' if item else ''
        key = (suffix, tuple(sorted(body)))
        self._changes.setdefault(key, [suffix, body, []])[2].append(
            self.host_label(result)
        )
        self._saw(result)

    def _print_changed(self, result, item=False):
        """Collect a changed host, unless v2_on_file_diff already did."""
        task = _task(result)
        res = _res(result)
        key = (_host(result).get_name(), task._uuid)
        if self._diff_printed.get(key):
            self._diff_printed[key] -= 1
            return
        if self._last_task_banner != task._uuid:
            self._print_task_banner(task)
        self._bar(C.COLOR_CHANGED)
        self._record(result, 'changed', [None])
        self._clean_results(res, task.action)
        if self._run_is_verbose(result):
            self._add_change(result, [f'=> {self._dump_results(res)}'], item)
            return
        body = []
        # Without a diff, these fields are where modules report what they changed
        # (e.g. the network_connections module of fedora.linux_system_roles logs to
        # stderr, dnf lists "Installed: x" in results). Loop results are dicts and
        # are printed per item instead.
        for field in self._CHANGE_DETAIL_FIELDS:
            value = res.get(field)
            if isinstance(value, list):
                if not all(isinstance(v, str) for v in value):
                    continue
                value = '\n'.join(value)
            if not isinstance(value, str) or not value.strip():
                continue
            body.append(f'  {field}:')
            body.extend(f'    {line}' for line in value.rstrip('\n').splitlines())
        self._add_change(result, body, item)

    def v2_on_file_diff(self, result):
        # Ansible sends v2_on_file_diff right before v2_runner_(item_)on_ok for the
        # same result (executor/task_executor.py, plugins/strategy/__init__.py,
        # verified against ansible-core 2.16). Collect the host with its diff and
        # skip the "changed" that follows for the same result.
        task = _task(result)
        res = _res(result)
        if (task.loop and 'results' in res) or not res.get('changed'):
            super().v2_on_file_diff(result)
            return
        diff = self._get_diff(res['diff']) if res.get('diff') else ''
        if not diff:
            return
        if self._last_task_banner != task._uuid:
            self._print_task_banner(task)
        self._bar(C.COLOR_CHANGED)
        self._record(result, 'changed', [None])
        # the empty line keeps the next "changed" apart from the diff
        self._add_change(result, [*diff.rstrip('\n').splitlines(), ''], task.loop)
        key = (_host(result).get_name(), task._uuid)
        self._diff_printed[key] = self._diff_printed.get(key, 0) + 1

    def v2_playbook_on_include(self, included_file):
        # Shorten ".../roles/network/tasks/set_facts.yml" to the part from the role
        # name on.
        path = included_file._filename
        if '/roles/' in path:
            path = path.rsplit('/roles/', 1)[1]
        hosts = compact_hosts(h.name for h in included_file._hosts)
        msg = f'included: {path} for {hosts}'
        label = self._get_item_label(included_file._vars)
        if label:
            msg += f' (item={self._short_label(label)})'
        self._display.display(msg, color=C.COLOR_SKIP)

    _LABEL_MAX = 60

    def _short_label(self, label):
        """The name of a dict item, else the item cut to _LABEL_MAX characters."""
        if isinstance(label, dict) and isinstance(label.get('name'), str):
            return label['name']
        label = str(label)
        if len(label) > self._LABEL_MAX:
            return label[: self._LABEL_MAX - 3] + '...'
        return label

    def v2_playbook_on_no_hosts_remaining(self):
        self._flush_hosts()
        super().v2_playbook_on_no_hosts_remaining()

    def v2_playbook_on_play_start(self, play):
        self._flush_hosts()
        self._play = play
        name = play.get_name().strip()
        # LFOps names its plays "Playbook linuxfabrik.lfops.<name>".
        if name.startswith('Playbook '):
            self._play_line = f'Playbook: {name[len("Playbook ") :]}'
        else:
            self._play_line = f'Play: {name}' if name else 'Play'
        self._section = self._play_line
        self._bold(self._play_line)

    def _bold(self, line):
        # Ansible's color names have no bold, so use the plain SGR code
        self._display_styled(f'\033[1m{line}\033[0m' if ANSIBLE_COLOR else line, line)

    def v2_playbook_on_stats(self, stats):
        self._flush_hosts()
        super().v2_playbook_on_stats(stats)
        self._print_issues()

    # Sections of the report at the end of the run, most severe first
    _REPORT_SECTIONS = (
        ('failed', 'FATAL', 'COLOR_ERROR'),
        ('unreachable', 'UNREACHABLE', 'COLOR_UNREACHABLE'),
        ('warning', 'WARNING', 'COLOR_WARN'),
        ('ignored', 'IGNORED', 'COLOR_SKIP'),
        ('changed', 'CHANGED', 'COLOR_CHANGED'),
    )

    def _print_issues(self):
        """The report at the end of the run, in Markdown: one section per kind,
        most severe first, the heading in the color of the kind. Within a section,
        one list per role or playbook, and in it each distinct message in task
        order, "* <task>: <message>", with the hosts on the next line, after a hard
        line break.
        """
        for kind, title, color in self._REPORT_SECTIONS:
            # role or playbook -> [(task, message, hosts)], in order of first
            # appearance
            sources = {}
            for (k, source, name, message), hosts in self._report.items():
                if k == kind:
                    sources.setdefault(source, []).append((name, message, hosts))
            if not sources:
                continue
            self._display.display('')
            heading = f'# {title}'
            color = getattr(C, color)
            if ANSIBLE_COLOR:
                self._display_styled(
                    f'\033[1m{stringc(heading, color)}\033[0m', heading
                )
            else:
                self._display.display(heading)
            for source, entries in sources.items():
                self._display.display('')
                self._display.display(f'{source}:')
                self._display.display('')
                for name, message, hosts in entries:
                    line = f'* {name}'
                    if message:
                        # one line per entry, multi-line messages are joined
                        line += ': ' + ' '.join(str(message).split())
                    # two trailing spaces are a hard line break in Markdown
                    self._display.display(f'{line}  ')
                    # always the hosts themselves, so the report names every one
                    self._display.display(f'  {compact_hosts(hosts)}')
        if self._report:
            self._display.display('')

    def v2_runner_item_on_ok(self, result):
        if isinstance(_task(result), TaskInclude):
            return
        res = _res(result)
        if res.get('changed'):
            self._print_changed(result, item=True)
        # unchanged items are covered by the host's asterisk and the "ok" line
        self._warnings(result)

    def v2_runner_item_on_skipped(self, result):
        pass

    def v2_runner_on_failed(self, result, ignore_errors=False):
        task = _task(result)
        if self._last_task_banner != task._uuid:
            self._print_task_banner(task)
        self._bar(C.COLOR_ERROR)
        self._saw(result)
        if ignore_errors and not self._run_is_verbose(result):
            # A failure the role accepts on purpose: collect it for the end of the
            # task instead of the full result. --verbose shows it as usual.
            messages = self._failure_messages(result)
            self._record(result, 'ignored', messages)
            for message in messages:
                self._ignored.setdefault(message, []).append(self.host_label(result))
            # ansible-core 2.19+ would print the exception of the failure as an
            # error, which the message above already covers
            _res(result).pop('exception', None)
            self._warnings(result)
            return
        if ignore_errors:
            self._record(result, 'ignored', self._failure_messages(result))
        else:
            self._record(result, 'failed', self._failure_messages(result))
        self._record(result, 'warning', self._warning_texts(result))
        super().v2_runner_on_failed(result, ignore_errors)

    def _failure_messages(self, result):
        """The first line of the message of a failed result, per failed item for a
        loop. The details are printed above with the result.
        """
        res = _res(result)
        if _task(result).loop and isinstance(res.get('results'), list):
            messages = [
                f'(item={self._get_item_label(item)}) '
                + (str(item.get('msg') or 'failed').strip().splitlines() or [''])[0]
                for item in res['results']
                if isinstance(item, dict) and item.get('failed')
            ]
            if messages:
                return messages
        return [(str(res.get('msg') or 'failed').strip().splitlines() or [''])[0]]

    def v2_runner_on_ok(self, result):
        task = _task(result)
        res = _res(result)
        if isinstance(task, TaskInclude):
            super().v2_runner_on_ok(result)
            return
        if not res.get('changed'):
            # The banner is still missing with the free strategies, see notes.
            if self._last_task_banner != task._uuid:
                self._print_task_banner(task)
            self._ok_hosts.append(self.host_label(result))
            self._saw(result)
            self._bar(C.COLOR_OK)
        elif not (task.loop and 'results' in res):
            # Loop results were already collected per item.
            self._print_changed(result)
        self._warnings(result)

    def v2_runner_on_skipped(self, result):
        task = _task(result)
        if self._last_task_banner != task._uuid:
            self._print_task_banner(task)
        self._skipped_hosts.append(self.host_label(result))
        self._saw(result)
        self._bar(C.COLOR_SKIP)

    def v2_runner_on_unreachable(self, result):
        task = _task(result)
        if self._last_task_banner != task._uuid:
            self._print_task_banner(task)
        self._bar(C.COLOR_UNREACHABLE)
        self._saw(result)
        self._record(result, 'unreachable', [_res(result).get('msg') or 'unreachable'])
        super().v2_runner_on_unreachable(result)
