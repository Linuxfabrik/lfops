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
    - Changed results print the host as a header above their diff. Without a diff, the C(msg), C(results), C(stdout) and C(stderr) of the result are shown below the host, since that is where modules report what they changed.
    - Failed and unreachable results are printed as usual, with C(msg), C(stdout), C(stderr), C(module_stdout) and C(module_stderr) as plain text below the JSON, so tracebacks stay readable.
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
        self._ok_hosts = []
        self._skipped_hosts = []
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

    def _display_wrapper(self, msg, *args, **kwargs):
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

    def _warnings(self, result):
        if hasattr(self, '_handle_warnings_and_exception'):
            # ansible-core 2.19+
            self._handle_warnings_and_exception(result)
        else:
            self._handle_warnings(_res(result))

    def _flush_hosts(self):
        self._close_line()
        for label, hosts, color in (
            ('ok', self._ok_hosts, C.COLOR_OK),
            ('skipped', self._skipped_hosts, C.COLOR_SKIP),
        ):
            if hosts:
                self._display.display(f'{label}: {compact_hosts(hosts)}', color=color)
                hosts.clear()

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

    def _print_task_banner(self, task):
        # "Role: x" / "Task: y" instead of "TASK [x : y] ****". Mirrors the default
        # callback, minus the check mode marker (the run starts with a DRY RUN banner
        # anyway).
        args = ''
        if not task.no_log and C.DISPLAY_ARGS_TO_STDOUT:
            args = ' ' + ', '.join(f'{k}={v}' for k, v in task.args.items())
        prefix = self._BANNER_PREFIX.get(
            self._task_type_cache.get(task._uuid, 'TASK'), 'Task'
        )
        name = self._last_task_name
        if name is None:
            name = task.get_name().strip()
        self._display.display('')
        if task._role:
            # Task.get_name() renders role tasks as "<role> : <name>"
            role = task._role.get_name()
            name = name.removeprefix(f'{role} : ')
            self._display_styled(f'{stringc("Role:", "blue")} {role}', f'Role: {role}')
        line = f'{name}{args}'
        self._display_styled(
            f'{stringc(f"{prefix}:", "green")} {line}', f'{prefix}: {line}'
        )
        if self._display.verbosity >= 2:
            self._print_task_path(task)
        self._last_task_banner = task._uuid

    def _task_start(self, task, prefix=None):
        self._flush_hosts()
        super()._task_start(task, prefix)
        # The default callback defers the banner when ok/skipped results are hidden.
        # Print it right away instead, unless it was already printed.
        # _last_task_name is None for the free/host_pinned strategies, where the
        # default callback also never prints the banner on task start.
        if self._last_task_name is not None and self._last_task_banner != task._uuid:
            self._print_task_banner(task)

    def _print_changed(self, result, item=False):
        """Print "changed: host", unless v2_on_file_diff already did."""
        task = _task(result)
        res = _res(result)
        key = (_host(result).get_name(), task._uuid)
        if self._diff_printed.get(key):
            self._diff_printed[key] -= 1
            return
        if self._last_task_banner != task._uuid:
            self._print_task_banner(task)
        self._bar(C.COLOR_CHANGED)
        msg = f'changed: {self.host_label(result)}'
        if item:
            msg += f' (item={self._get_item_label(res)})'
        self._clean_results(res, task.action)
        if self._run_is_verbose(result):
            self._display.display(
                f'{msg} => {self._dump_results(res)}', color=C.COLOR_CHANGED
            )
            return
        self._display.display(msg, color=C.COLOR_CHANGED)
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
            self._display.display(f'  {field}:')
            for line in value.rstrip('\n').splitlines():
                self._display.display(f'    {line}')

    def v2_on_file_diff(self, result):
        # Ansible sends v2_on_file_diff right before v2_runner_(item_)on_ok for the
        # same result (executor/task_executor.py, plugins/strategy/__init__.py,
        # verified against ansible-core 2.16). Print the host as header above its
        # diff and skip the "changed" line that would follow below it.
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
        self._display.display(
            f'changed: {self.host_label(result)}', color=C.COLOR_CHANGED
        )
        self._display.display(diff)
        key = (_host(result).get_name(), task._uuid)
        self._diff_printed[key] = self._diff_printed.get(key, 0) + 1

    def v2_playbook_on_include(self, included_file):
        # Shorten ".../roles/network/tasks/set_facts.yml" to the part from the role
        # name on.
        path = included_file._filename
        if '/roles/' in path:
            path = path.rsplit('/roles/', 1)[1]
        hosts = ', '.join(sorted(h.name for h in included_file._hosts))
        msg = f'included: {path} for {hosts}'
        label = self._get_item_label(included_file._vars)
        if label:
            msg += f' (item={label})'
        self._display.display(msg, color=C.COLOR_SKIP)

    def v2_playbook_on_no_hosts_remaining(self):
        self._flush_hosts()
        super().v2_playbook_on_no_hosts_remaining()

    def v2_playbook_on_play_start(self, play):
        self._flush_hosts()
        self._play = play
        name = play.get_name().strip()
        # LFOps names its plays "Playbook linuxfabrik.lfops.<name>".
        if name.startswith('Playbook '):
            line = f'Playbook: {name[len("Playbook ") :]}'
        else:
            line = f'Play: {name}' if name else 'Play'
        # Ansible's color names have no bold, so use the plain SGR code
        self._display_styled(f'\033[1m{line}\033[0m' if ANSIBLE_COLOR else line, line)

    def v2_playbook_on_stats(self, stats):
        self._flush_hosts()
        super().v2_playbook_on_stats(stats)

    def v2_runner_item_on_ok(self, result):
        # Unchanged items are covered by the host's asterisk and the "ok" line.
        if isinstance(_task(result), TaskInclude) or not _res(result).get('changed'):
            return
        self._print_changed(result, item=True)

    def v2_runner_item_on_skipped(self, result):
        pass

    def v2_runner_on_failed(self, result, ignore_errors=False):
        task = _task(result)
        if self._last_task_banner != task._uuid:
            self._print_task_banner(task)
        self._bar(C.COLOR_ERROR)
        super().v2_runner_on_failed(result, ignore_errors)

    def v2_runner_on_ok(self, result):
        task = _task(result)
        res = _res(result)
        if isinstance(task, TaskInclude):
            super().v2_runner_on_ok(result)
            return
        self._warnings(result)
        if not res.get('changed'):
            # The banner is still missing with the free strategies, see notes.
            if self._last_task_banner != task._uuid:
                self._print_task_banner(task)
            self._ok_hosts.append(self.host_label(result))
            self._bar(C.COLOR_OK)
        elif not (task.loop and 'results' in res):
            # Loop results were already printed per item.
            self._print_changed(result)

    def v2_runner_on_skipped(self, result):
        task = _task(result)
        if self._last_task_banner != task._uuid:
            self._print_task_banner(task)
        self._skipped_hosts.append(self.host_label(result))
        self._bar(C.COLOR_SKIP)

    def v2_runner_on_unreachable(self, result):
        task = _task(result)
        if self._last_task_banner != task._uuid:
            self._print_task_banner(task)
        self._bar(C.COLOR_UNREACHABLE)
        super().v2_runner_on_unreachable(result)
