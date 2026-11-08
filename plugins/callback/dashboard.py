#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import atexit
import json
import os
import re
import subprocess  # nosec B404
import sys
import time
from collections import Counter

from ansible import constants as C
from ansible.playbook.task_include import TaskInclude
from ansible.release import __version__ as ANSIBLE_CORE_VERSION
from ansible.utils.color import ANSIBLE_COLOR, stringc
from ansible_collections.linuxfabrik.lfops.plugins.callback.compact import (
    CallbackModule as Compact,
)
from ansible_collections.linuxfabrik.lfops.plugins.callback.compact import (
    _host,
    _res,
    _task,
)

try:
    import termios
except ImportError:  # not on a POSIX system
    termios = None

DOCUMENTATION = r"""
  name: dashboard
  type: stdout
  version_added: "10.0.0"
  short_description: Fixed full-screen view of a run, details at the end
  description:
    - Shows the run on one fixed screen that is updated in place instead of scrolling. At the top the playbook, the number of hosts and the elapsed time, the current role and task, then counters of the results of the current task and of the whole run.
    - Below the title, where LFOps comes from - its version, or for a git checkout the branch, the commit and the number of uncommitted files, and the source path when the checkout is mounted into an execution environment - and the ansible-core version. An C(LFOPS_EE_VERSION) environment variable is shown as the EE version.
    - Below, the hosts are listed, sorted by their most severe result (fatal, warning, changed, ignored, ok), then by name, with their counters and their last notable result, or the last ok result for a host without one. Hosts with only skipped results are counted, not listed.
    - At the end of the run, the screen is left and the details follow in the format of C(linuxfabrik.lfops.compact), but only for the tasks with changes, warnings or failures. Then the recap and the report of the distinct messages by severity.
    - Without a terminal (log file, pipe, CI) or with C(--verbose), the plugin behaves exactly like C(linuxfabrik.lfops.compact).
  author:
    - Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
  notes:
    - Under ansible-navigator, set the environment variable C(ANSIBLE_STDOUT_CALLBACK). ansible-runner replaces the stdout callback with its own wrapper, which only builds on this variable and ignores C(stdout_callback) in C(ansible.cfg).
    - The terminal needs at least 65 columns and 12 lines, else the plugin behaves like C(linuxfabrik.lfops.compact). ansible-runner writes 64 characters wide invisible event markers, which the screen keeps on its last line.
    - Keyboard input is not echoed while the screen is shown, so that a pressed key does not move it. Prompts (C(vars_prompt), C(pause)) are not supported on the screen.
    - Made for the linear strategies (C(linear), C(mitogen_linear)).
  extends_documentation_fragment:
    - ansible.builtin.default_callback
    - ansible.builtin.result_format_callback
  requirements:
    - set as stdout callback in the configuration
"""

EXAMPLES = r"""
# ansible.cfg
[defaults]
stdout_callback = linuxfabrik.lfops.dashboard

# ansible-navigator.yml
ansible-navigator:
  execution-environment:
    environment-variables:
      set:
        ANSIBLE_STDOUT_CALLBACK: 'linuxfabrik.lfops.dashboard'
"""

# Alternate screen buffer on/off, cursor hidden/shown
_SCREEN_ON = '\033[?1049h\033[?25l\033[2J'
_SCREEN_OFF = '\033[?25h\033[?1049l'

_MIN_COLUMNS = 65
_MIN_LINES = 12


def _git(root, *args):
    """Run git in `root`, return its output or None. safe.directory: in an EE, the
    mounted checkout belongs to another user than the one running Ansible.
    """
    # Without the GIT_* variables of the environment: set by git itself while it runs
    # a hook, they would point git at another repository than `root`.
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    try:
        proc = subprocess.run(  # nosec B603 B607
            ['git', '-C', str(root), '-c', 'safe.directory=*', *args],
            capture_output=True,
            check=False,
            env=env,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return proc.stdout.strip() if proc.returncode == 0 else None


def lfops_origin(root, mountinfo='/proc/self/mountinfo'):
    """Describe the LFOps collection at `root`: its version, for a git checkout the
    branch, commit and number of changed files, e.g. "LFOps main@3e8a7b75, 2
    uncommitted". Return it with the source path of a bind mount (an EE with the
    checkout mounted), or None. The path is relative to the file system it lives
    on, so a separate /tmp or /home shows without that prefix.
    """
    root = os.path.realpath(root)
    version = None
    try:
        with open(os.path.join(root, 'MANIFEST.json'), encoding='utf-8') as f:
            version = json.load(f)['collection_info']['version']
    except (OSError, ValueError, KeyError):
        try:
            with open(os.path.join(root, 'galaxy.yml'), encoding='utf-8') as f:
                m = re.search(r'^version:\s*[\'"]?([^\'"\s]+)', f.read(), re.M)
            version = m.group(1) if m else None
        except OSError:
            pass
    parts = [f'LFOps {version or "unknown"}']
    if os.path.exists(os.path.join(root, '.git')):
        branch = _git(root, 'rev-parse', '--abbrev-ref', 'HEAD')
        commit = _git(root, 'rev-parse', '--short=8', 'HEAD')
        if branch and commit:
            parts[0] = f'LFOps {branch}@{commit}'
            changed = _git(root, 'status', '--porcelain', '--untracked-files=no')
            if changed:
                parts.append(f'{len(changed.splitlines())} uncommitted')
    # a bind mount: the 4th field is the source path, the 5th the mount point
    source = None
    try:
        with open(mountinfo, encoding='utf-8') as f:
            for line in f:
                fields = line.split()
                if len(fields) > 4 and fields[4] == root and fields[3] != '/':
                    source = fields[3]
                    break
    except OSError:
        pass
    return ', '.join(parts), source


class CallbackModule(Compact):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'linuxfabrik.lfops.dashboard'

    # kind -> letter and color in the LAST column of the host list
    _KIND_LETTERS = {  # noqa: RUF012
        'changed': ('C', C.COLOR_CHANGED),
        'failed': ('F', C.COLOR_ERROR),
        'ignored': ('I', C.COLOR_SKIP),
        'ok': ('O', C.COLOR_OK),
        'unreachable': ('U', C.COLOR_UNREACHABLE),
        'warning': ('W', C.COLOR_WARN),
    }

    # the host list is sorted by the most severe result of a host, then by name;
    # the name is shown in the color of that result
    _HOST_SEVERITY = (
        ('fatal', C.COLOR_ERROR),
        ('warning', C.COLOR_WARN),
        ('changed', C.COLOR_CHANGED),
        ('ignored', C.COLOR_SKIP),
        ('ok', C.COLOR_OK),
    )

    # at most this many redraws per second, the last state is always drawn at the
    # end of a task
    _REDRAW_INTERVAL = 0.1

    def __init__(self):
        super().__init__()
        # whether the screen is shown right now
        self._tui = False
        self._tui_done = False
        self._start = time.monotonic()
        self._last_draw = 0.0
        self._size = None
        self._termios_saved = None
        # header: (section, prefix, task line) of the running task
        self._header = (None, None, None)
        self._task_counts = Counter()
        self._run_counts = Counter()
        # host name -> Counter of changed/failed/ignored/ok/unreachable/warning,
        # its last notable result, and its last ok result for hosts without one
        self._host_counts = {}
        self._host_last = {}
        self._host_last_ok = {}
        self._play_hosts = set()
        self._dead_hosts = set()
        # where the plugin, and with it LFOps, comes from, see lfops_origin()
        self._origin = None
        # output of the running task and the details for the end of the run
        self._capture = []
        self._details = []
        self._details_section = None

    # -- screen ------------------------------------------------------------------

    def _terminal_size(self):
        try:
            size = os.get_terminal_size(sys.stdout.fileno())
        except (OSError, ValueError):
            return None
        return size.columns, size.lines

    def _start_tui(self):
        if self._tui or self._tui_done:
            return
        size = self._terminal_size()
        if (
            not sys.stdout.isatty()
            or self._display.verbosity > 0
            or size is None
            or size[0] < _MIN_COLUMNS
            or size[1] < _MIN_LINES
        ):
            self._tui_done = True
            return
        if termios is not None and sys.stdin.isatty():
            try:
                self._termios_saved = termios.tcgetattr(sys.stdin.fileno())
                attrs = termios.tcgetattr(sys.stdin.fileno())
                attrs[3] &= ~termios.ECHO
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, attrs)
            except termios.error:
                self._termios_saved = None
        sys.stdout.write(_SCREEN_ON)
        sys.stdout.flush()
        self._tui = True
        # leave the screen and print the details also on Ctrl+C or a crash
        atexit.register(self._end_tui)

    def _end_tui(self):
        if not self._tui:
            return
        self._tui = False
        self._tui_done = True
        sys.stdout.write(_SCREEN_OFF)
        sys.stdout.flush()
        if self._termios_saved is not None:
            try:
                termios.tcsetattr(
                    sys.stdin.fileno(), termios.TCSADRAIN, self._termios_saved
                )
            except termios.error:
                pass
        if self._capture:
            self._keep_capture()
        self._replay_details()

    @staticmethod
    def _fit(segments, width):
        """Join (text, color, bold) segments, cut to `width` visible characters."""
        out, used = [], 0
        for text, color, bold in segments:
            if used >= width:
                break
            text = text[: width - used]
            used += len(text)
            if color and ANSIBLE_COLOR:
                text = stringc(text, color)
            if bold and ANSIBLE_COLOR:
                text = f'\033[1m{text}\033[0m'
            out.append(text)
        return ''.join(out)

    def _counter_segments(self, label, counts, kinds):
        segments = [(f'{label:<7}', None, True)]
        for kind, color in kinds:
            value = counts.get(kind, 0)
            segments.append((f'{kind} ', None, False))
            segments.append((f'{value:<5}', color if value else None, bool(value)))
        return segments

    def _draw(self, force=False):
        if not self._tui:
            return
        now = time.monotonic()
        if not force and now - self._last_draw < self._REDRAW_INTERVAL:
            return
        self._last_draw = now
        size = self._terminal_size()
        if size is None:
            return
        columns, lines = size
        width = columns - 1
        screen = []

        elapsed = int(now - self._start)
        elapsed = f'{elapsed // 3600:02d}:{elapsed % 3600 // 60:02d}:{elapsed % 60:02d}'
        right = f'{len(self._play_hosts)} hosts   {elapsed}'
        title = self._play_line.split(': ', 1)[-1]
        screen.append(
            self._fit(
                [
                    (title, None, True),
                    (' ' * max(width - len(title) - len(right), 1), None, False),
                    (right, None, False),
                ],
                width,
            )
        )
        if self._origin is None:
            # collection root: plugins/callback/dashboard.py -> ../../..
            root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            lfops, source = lfops_origin(root)
            # the most important first, the path is cut on a narrow terminal
            self._origin = f'{lfops}   ansible-core {ANSIBLE_CORE_VERSION}'
            ee = os.environ.get('LFOPS_EE_VERSION')
            if ee:
                self._origin += f'   EE {ee}'
            if source:
                self._origin += f'   mounted from {source}'
        screen.append(self._fit([(self._origin, None, False)], width))
        section, prefix, task_line = self._header
        if section and section.startswith('Role: '):
            screen.append(
                self._fit(
                    [
                        ('Role: ', 'blue', False),
                        (section[len('Role: ') :], None, False),
                    ],
                    width,
                )
            )
        else:
            screen.append(self._fit([(section or '', None, False)], width))
        if prefix:
            screen.append(
                self._fit(
                    [(f'{prefix}: ', 'green', False), (task_line, None, False)], width
                )
            )
        else:
            screen.append('')
        screen.append('─' * width)

        task_counts = Counter(self._task_counts)
        if self._play_hosts:
            alive = len(self._play_hosts - self._dead_hosts)
            # hosts that are still at work on the task
            task_counts['pending'] = max(alive - len(self._task_hosts), 0)
        screen.append(
            self._fit(
                self._counter_segments(
                    'Task',
                    task_counts,
                    (
                        ('ok', C.COLOR_OK),
                        ('changed', C.COLOR_CHANGED),
                        ('skipped', C.COLOR_SKIP),
                        ('fatal', C.COLOR_ERROR),
                        ('unreachable', C.COLOR_UNREACHABLE),
                        ('ignored', C.COLOR_WARN),
                        ('pending', None),
                    ),
                ),
                width,
            )
        )
        screen.append(
            self._fit(
                self._counter_segments(
                    'Run',
                    self._run_counts,
                    (
                        ('ok', C.COLOR_OK),
                        ('changed', C.COLOR_CHANGED),
                        ('warning', C.COLOR_WARN),
                        ('fatal', C.COLOR_ERROR),
                        ('unreachable', C.COLOR_UNREACHABLE),
                    ),
                ),
                width,
            )
        )
        screen.append('─' * width)

        hosts = sorted(self._host_counts, key=lambda h: (self._host_severity(h), h))
        name_width = min(max([len(h) for h in hosts] + [4]), 30)
        screen.append(
            self._fit(
                [
                    (
                        f'{"HOST":<{name_width}}  {"F":>3} {"W":>3} {"C":>3}  LAST',
                        None,
                        True,
                    )
                ],
                width,
            )
        )
        # the last line stays empty, the cursor and the markers of ansible-runner
        # sit there
        room = lines - len(screen) - 1
        shown = hosts if len(hosts) <= room else hosts[: max(room - 1, 0)]
        for host in shown:
            counts = self._host_counts[host]
            fatal = counts['failed'] + counts['unreachable']
            color = self._HOST_SEVERITY[self._host_severity(host)][1]
            # every count in the color of its own kind, zeros plain
            segments = [(f'{host[:name_width]:<{name_width}} ', color, bool(fatal))]
            for value, value_color in (
                (fatal, C.COLOR_ERROR),
                (counts['warning'], C.COLOR_WARN),
                (counts['changed'], C.COLOR_CHANGED),
            ):
                segments.append((f' {value:>3}', value_color if value else None, False))
            segments.append(('  ', None, False))
            kind, text = self._host_last.get(host) or self._host_last_ok.get(
                host, (None, '')
            )
            if kind:
                letter, letter_color = self._KIND_LETTERS[kind]
                segments.append((f'{letter} ', letter_color, True))
            segments.append((text, None, False))
            screen.append(self._fit(segments, width))
        if len(shown) < len(hosts):
            screen.append(f'+ {len(hosts) - len(shown)} more hosts')

        out = []
        if size != self._size:
            # resized: start from a blank screen
            self._size = size
            out.append('\033[2J')
        for row, line in enumerate(screen[: lines - 1], start=1):
            out.append(f'\033[{row};1H{line}\033[K')
        for row in range(len(screen) + 1, lines + 1):
            out.append(f'\033[{row};1H\033[K')
        out.append(f'\033[{lines};1H')
        sys.stdout.write(''.join(out))
        sys.stdout.flush()

    # -- output of the run -------------------------------------------------------

    def _display_wrapper(self, msg, *args, **kwargs):
        if not self._tui:
            return super()._display_wrapper(msg, *args, **kwargs)
        if isinstance(msg, str) and msg.startswith(self._WARNING_MARK):
            # a warning of a worker process, see compact
            return super()._display_wrapper(msg, *args, **kwargs)
        if kwargs.get('log_only'):
            return self._display_orig(msg, *args, **kwargs)
        # Nothing may print over the screen: keep it for the end of the run, but
        # log it right away.
        if not args and not kwargs.get('screen_only'):
            self._display_orig(msg, **{**kwargs, 'log_only': True})
        self._capture.append((msg, args, {**kwargs, 'screen_only': True}))
        return None

    def _keep_capture(self):
        """Keep the output of the finished task for the end of the run, under its
        section and task line.
        """
        section, prefix, task_line = self._header
        if section != self._details_section:
            self._details_section = section
            self._details.append(('', (), {}))
            bold = f'\033[1m{section}\033[0m' if ANSIBLE_COLOR else section
            self._details.append((bold, (), {'screen_only': True}))
        # output outside of a task, like "no hosts matched", has no task line
        if task_line is not None:
            self._details.append(('', (), {}))
            styled = f'{stringc(f"{prefix}:", "green")} {task_line}'
            self._details.append((styled, (), {'screen_only': True}))
        self._details.extend(self._capture)
        self._capture = []

    def _replay_details(self):
        for msg, args, kwargs in self._details:
            self._display_orig(msg, *args, **kwargs)
        self._details = []

    def _bar(self, color):
        if not self._tui:
            super()._bar(color)

    def _print_ok_skipped(self):
        if not self._tui:
            super()._print_ok_skipped()

    def v2_playbook_on_include(self, included_file):
        if not self._tui:
            super().v2_playbook_on_include(included_file)

    def _print_task_banner(self, task):
        if not self._tui:
            super()._print_task_banner(task)
            return
        self._header = self._banner_parts(task)
        self._last_task_banner = task._uuid
        self._draw(force=True)

    def _flush_hosts(self):
        super()._flush_hosts()
        if self._tui:
            if self._capture:
                self._keep_capture()
            self._task_counts = Counter()
            self._draw(force=True)

    def _host_severity(self, host):
        """The index in _HOST_SEVERITY of the most severe result of a host."""
        counts = self._host_counts[host]
        present = {
            'fatal': counts['failed'] + counts['unreachable'],
            'warning': counts['warning'],
            'changed': counts['changed'],
            'ignored': counts['ignored'],
        }
        for index, (kind, _) in enumerate(self._HOST_SEVERITY):
            if present.get(kind):
                return index
        return len(self._HOST_SEVERITY) - 1

    def _last_text(self, task, message=None):
        """The LAST column of the host list: "<role> - <task>: <message>"."""
        source, name = self._source_and_name(task)
        # "namespace.collection.role" -> "role", the screen is narrow and the report
        # at the end names it in full
        if source.count('.') == 2:
            source = source.rsplit('.', 1)[1]
        last = f'{source} - {name}'
        if message:
            last += ': ' + ' '.join(str(message).split())
        return last

    def _record_entry(self, host, kind, task, messages):
        super()._record_entry(host, kind, task, messages)
        if not messages:
            return
        # ignored failures are counted, but not shown in the F, W and C columns
        counts = self._host_counts.setdefault(host, Counter())
        counts[kind] += len(messages)
        self._host_last[host] = (kind, self._last_text(task, messages[-1]))
        if kind == 'warning':
            self._run_counts['warning'] += len(messages)

    def _count(self, kind):
        self._task_counts[kind] += 1
        self._run_counts[kind] += 1
        self._draw()

    # -- events ------------------------------------------------------------------

    def v2_playbook_on_play_start(self, play):
        super().v2_playbook_on_play_start(play)
        try:
            inventory = play.get_variable_manager()._inventory
            self._play_hosts = {h.name for h in inventory.get_hosts(play.hosts)}
        except Exception:  # only for the host counter
            self._play_hosts = set()
        self._dead_hosts = set()
        self._start_tui()
        # the play line is part of the screen header, not of the details, and was
        # printed above the screen already
        self._capture = []
        self._details_section = self._play_line
        self._header = (self._play_line, None, None)
        self._draw(force=True)

    def v2_playbook_on_stats(self, stats):
        if self._tui:
            self._flush_hosts()
            self._end_tui()
        super().v2_playbook_on_stats(stats)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        super().v2_runner_on_failed(result, ignore_errors)
        if ignore_errors:
            self._count('ignored')
        else:
            self._dead_hosts.add(_host(result).get_name())
            self._count('fatal')

    def v2_runner_on_ok(self, result):
        super().v2_runner_on_ok(result)
        task = _task(result)
        if isinstance(task, TaskInclude):
            return
        if not _res(result).get('changed'):
            # listed as well, so the list of a run without issues is not empty
            host = _host(result).get_name()
            self._host_counts.setdefault(host, Counter())['ok'] += 1
            self._host_last_ok[host] = ('ok', self._last_text(task))
        self._count('changed' if _res(result).get('changed') else 'ok')

    def v2_runner_on_skipped(self, result):
        super().v2_runner_on_skipped(result)
        self._count('skipped')

    def v2_runner_on_unreachable(self, result):
        super().v2_runner_on_unreachable(result)
        self._dead_hosts.add(_host(result).get_name())
        self._count('unreachable')
