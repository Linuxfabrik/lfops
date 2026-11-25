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
import hashlib
import json
import os
import re
import stat
import subprocess  # nosec B404
import sys
import tempfile
import threading
import time
from collections import Counter

from ansible import constants as C
from ansible.playbook.block import Block
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
    - Shows the run on one fixed screen that is updated in place instead of scrolling, at least once a second. At the top the playbook, the number of hosts and the elapsed time, the current role and task, a progress bar of the play with the estimated remaining time, then counters of the results of the current task and of the whole run. The ok counter of the task is followed by the number of hosts still at work on the task and the number of hosts, for example C(ok 13/22/35).
    - Below the title, where LFOps comes from - its version, or for a git checkout the branch, the commit and the number of uncommitted files, and the source path, shortened to the initials of its parent directories, when the checkout is mounted into an execution environment - and the ansible-core version. An C(LFOPS_EE_VERSION) environment variable is shown as the EE version.
    - The progress bar counts the tasks of the play that are known when it starts, after C(--tags) and C(--skip-tags) are applied. A task included with C(include_tasks) or C(include_role) is one step, the bar stands still while the tasks it includes run. Tasks in C(rescue) sections and handlers are not counted. The bar counts tasks, not time, and starts over with every batch of C(serial).
    - The estimated remaining time (ETA) adds up how long each step left took the last time it ran, an include with all its tasks, until the slowest host was done. The durations are kept in O(eta_cache_dir) for the next runs, one file per step, so that runs in parallel, like several ansible-navigator sessions, do not wait for each other. A step that never ran before is assumed to take as long as the steps of this play so far did on average.
    - Below, the hosts are listed, sorted by their most severe result (fatal, warning, changed, ignored, ok), then by name, with their counts of fatal (F), warning (W), changed (C) and ok (O) results and their last notable result (LAST WORST), or the last ok result for a host without one. Hosts with only skipped results are counted, not listed.
    - At the end of the run, the screen is left and the details follow in the format of C(linuxfabrik.lfops.compact), but only for the tasks with changes, warnings or failures. Then the recap and the report of the distinct messages by severity.
    - Without a terminal (log file, pipe, CI) or with C(--verbose), the plugin behaves exactly like C(linuxfabrik.lfops.compact).
  author:
    - Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
  notes:
    - Under ansible-navigator, set the environment variable C(ANSIBLE_STDOUT_CALLBACK). ansible-runner replaces the stdout callback with its own wrapper, which only builds on this variable and ignores C(stdout_callback) in C(ansible.cfg).
    - The terminal needs at least 65 columns and 12 lines, else the plugin behaves like C(linuxfabrik.lfops.compact). ansible-runner writes 64 characters wide invisible event markers, which the screen keeps on its last line.
    - Keyboard input is not echoed while the screen is shown, so that a pressed key does not move it. Prompts (C(vars_prompt), C(pause)) are not supported on the screen.
    - Made for the linear strategies (C(linear), C(mitogen_linear)).
  options:
    display_debug_output:
      description:
        - Show the output of C(ansible.builtin.debug) tasks, although their hosts are ok, grouped by identical output like the changes, with the other details at the end of the run.
        - If disabled, the hosts of a C(ansible.builtin.debug) task are listed in the C(ok) line like those of any other task.
      type: bool
      default: true
      env:
        - name: ANSIBLE_CALLBACK_COMPACT_DISPLAY_DEBUG_OUTPUT
      ini:
        - section: callback_compact
          key: display_debug_output
    eta_cache_dir:
      description:
        - The directory where the durations of the steps are kept for the ETA of later runs, below C(/var/tmp/lfops), which the README asks ansible-navigator users to mount into the execution environment.
        - The directory and its parent are created with mode C(0700) and must belong to the user running Ansible, else the ETA is estimated from the current play only. An empty value does the same.
      type: path
      default: /var/tmp/lfops/dashboard
      env:
        - name: ANSIBLE_CALLBACK_DASHBOARD_ETA_CACHE_DIR
      ini:
        - section: callback_dashboard
          key: eta_cache_dir
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

# collection root: plugins/callback/dashboard.py -> ../../..
_COLLECTION_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

_DURATION_SUFFIX = '.json'


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


def shorten_path(path):
    """Reduce every component of a path except the last one to its first character,
    like the zsh prompt does: "/home/user/git/lfops" -> "/h/u/g/lfops". The same as
    shorten_path() in disk.py of the Linuxfabrik lib, which the plugin cannot import.
    """
    if not path or '/' not in path:
        return path
    head, _, tail = path.rpartition('/')
    return '/'.join(part[:1] for part in head.split('/')) + f'/{tail}'


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


def step_key(task, root=_COLLECTION_ROOT):
    """What identifies a task across runs and playbooks: its file and line,
    relative to the collection root when it is part of LFOps, so that a checkout, a
    worktree and an execution environment share it, followed by the chain of roles
    that lead to it. A task of a role imported by many roles, like
    shared/tasks/platform-variables.yml, gets a key per importing role. A task
    without a file of its own, like the implicit fact gathering or the validation
    of the role arguments, has the file and line of its play.
    """
    path = task.get_path()
    if path.startswith(root.rstrip('/') + '/'):
        path = path[len(root.rstrip('/')) + 1 :]
    key = path or f'{task.action} {task.get_name()}'
    roles = [role.get_name() for role in task.get_dep_chain() or []]
    if roles:
        key += f' [{" > ".join(roles)}]'
    return key


def play_steps(play, root=_COLLECTION_ROOT):
    """Number the tasks of a play that ansible-core will start, the way its
    PlayIterator sees them: play.compile() with --tags and --skip-tags applied.
    Return a dict of task UUID -> step, starting at 1, and the list of the keys of
    the steps, see step_key(). A role that runs twice in a play with other
    parameters has the same key twice, the second occurrence gets a "#2".

    Left out are the meta tasks, which never fire v2_playbook_on_task_start, and the
    rescue sections, which only run on a failure. Included tasks are only known at
    run time; the include itself is one step. A role listed twice with the same
    parameters runs once, its tasks keep the step of their first occurrence.
    Verified against ansible-core 2.16, 2.18 and 2.22 (executor/play_iterator.py,
    plugins/strategy/linear.py).
    """
    all_vars = play.get_variable_manager().get_vars(play=play)
    steps = {}
    keys = []
    seen = Counter()

    def walk(tasks):
        for task in tasks or []:
            if isinstance(task, Block):
                walk(task.block)
                walk(task.always)
            elif task.action not in C._ACTION_META and task._uuid not in steps:
                steps[task._uuid] = len(steps) + 1
                key = step_key(task, root)
                seen[key] += 1
                keys.append(key if seen[key] == 1 else f'{key}#{seen[key]}')

    for block in play.compile():
        walk([block.filter_tagged_tasks(all_vars)])
    return steps, keys


def hms(seconds):
    """Seconds as "hh:mm:ss"."""
    seconds = int(seconds)
    return f'{seconds // 3600:02d}:{seconds % 3600 // 60:02d}:{seconds % 60:02d}'


def eta(step, durations, play_start, step_start, now):
    """The remaining time of a play: the sum of the `durations` (seconds, one per
    step, None if unknown) of the steps after the running one, plus what is left of
    the duration of that step. A step that runs longer than its duration does not
    eat into the estimate for the steps after it. An unknown duration is the
    average of the finished steps of this play; None if there is none yet.
    """
    if step < 1:
        return None
    done = step - 1
    average = (step_start - play_start) / done if done else None
    remaining = 0.0
    for index in range(step - 1, len(durations)):
        duration = durations[index] if durations[index] is not None else average
        if duration is None:
            return None
        if index == step - 1:
            duration = max(duration - (now - step_start), 0)
        remaining += duration
    return remaining


def _private_dir(directory):
    """Create `directory` and its parent with mode 0700, return whether both are
    real directories of the effective user. Below the world-writable /var/tmp,
    another user could create them first and swap the file for a symlink.
    """
    directory = directory.rstrip('/')
    parent = os.path.dirname(directory)
    try:
        # the mode of makedirs() only applies to the last directory
        os.makedirs(parent, mode=0o700, exist_ok=True)
        os.makedirs(directory, mode=0o700, exist_ok=True)
        for path in (parent, directory):
            st = os.lstat(path)
            if not stat.S_ISDIR(st.st_mode) or st.st_uid != os.geteuid():
                return False
    except OSError:
        return False
    return True


def _duration_file(directory, key):
    """The file of a step: the key hashed, since it contains slashes and spaces."""
    name = hashlib.sha256(key.encode('utf-8')).hexdigest()
    return os.path.join(directory, name + _DURATION_SUFFIX)


def _read_duration(path, key):
    """The seconds in the file of the step `key`, None if unusable."""
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or data.get('key') != key:
        return None
    seconds = data.get('seconds')
    return seconds if isinstance(seconds, (int, float)) else None


def load_durations(directory, keys):
    """The durations of the steps `keys` from earlier runs, key -> seconds, for
    those that are known.
    """
    if not directory or not keys or not _private_dir(directory):
        return {}
    durations = {}
    for key in keys:
        seconds = _read_duration(_duration_file(directory, key), key)
        if seconds is not None:
            durations[key] = seconds
    return durations


def save_durations(directory, measured):
    """Write the `measured` durations (key -> seconds), one file per step, so
    that runs in parallel, e.g. several ansible-navigator sessions, need no lock:
    each file is replaced as a whole, the last run wins.
    """
    if not directory or not measured or not _private_dir(directory):
        return
    for key, seconds in measured.items():
        # a new file moved into place, so that a run that aborts while writing
        # leaves the old one, and another run never reads half a file
        try:
            fd, tmp = tempfile.mkstemp(dir=directory, prefix='.tmp.')
        except OSError:
            return
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump({'key': key, 'seconds': round(seconds, 1)}, f)
            os.replace(tmp, _duration_file(directory, key))
        except OSError:
            try:
                os.unlink(tmp)
            except OSError:
                pass


def progress_bar(step, total, width, color=True, remaining=None):
    """A bar of `width` characters starting with "step 7/21 (33%)" and the
    remaining time, if known. With color, the done part is shown in reverse video,
    else filled with "#".
    """
    label = f' step {step}/{total} ({step * 100 // total}%)'
    if remaining is not None:
        label += f'   ETA {hms(remaining)}'
    label += ' '
    done = width * step // total
    if not color:
        bar = '#' * done + ' ' * (width - done)
        return (label + bar[len(label) :])[:width]
    line = label.ljust(width)[:width]
    return f'\033[7m{line[:done]}\033[0m{line[done:]}'


class CallbackModule(Compact):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'linuxfabrik.lfops.dashboard'

    # kind -> letter and color in the LAST WORST column of the host list
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

    # a mid gray of the 256 color palette, readable on dark and light backgrounds
    _GRAY = 'gray12'

    # at most this many redraws per second, the last state is always drawn at the
    # end of a task
    _REDRAW_INTERVAL = 0.1
    # without events, the screen is redrawn after this many seconds, so the elapsed
    # time and the ETA keep moving during a long task
    _TICK_INTERVAL = 1.0

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
        # all hosts of the play, and those of the running batch with "serial"
        self._play_hosts = set()
        self._batch_hosts = set()
        self._dead_hosts = set()
        # task UUID -> step of the running play and the keys of the steps, see
        # play_steps(), the step of the running task, and when the play and that
        # step started, for the ETA
        self._steps = {}
        self._step_keys = []
        self._step = 0
        self._play_start = time.monotonic()
        self._step_start = self._play_start
        # key -> seconds: the durations of the steps of the running play from
        # earlier runs, and those measured in this run, see _learn()
        self._durations = {}
        self._measured = {}
        # where the plugin, and with it LFOps, comes from, see lfops_origin()
        self._origin = None
        # output of the running task and the details for the end of the run
        self._capture = []
        self._details = []
        self._details_section = None
        # the screen is drawn by the main thread on events and by a ticker thread
        # in between, see _tick()
        self._screen_lock = threading.RLock()
        self._ticker_stop = threading.Event()

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
        threading.Thread(
            target=self._tick, name='lfops-dashboard-ticker', daemon=True
        ).start()

    def _tick(self):
        """Redraw the screen when no event did so for _TICK_INTERVAL seconds."""
        # checked four times as often, so a redraw is at most a quarter late
        while not self._ticker_stop.wait(self._TICK_INTERVAL / 4):
            if time.monotonic() - self._last_draw < self._TICK_INTERVAL:
                continue
            try:
                self._draw(force=True)
            except Exception:  # the main thread changed the state, next tick
                pass

    def _end_tui(self):
        self._ticker_stop.set()
        # wait for a draw of the ticker thread in progress
        with self._screen_lock:
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
        save_durations(self._eta_cache_dir(), self._measured)

    def _eta_cache_dir(self):
        try:
            return self.get_option('eta_cache_dir')
        except KeyError:  # options not set, e.g. in a unit test
            return None

    def _learn(self, now):
        """Keep how long the running step took, until the next one starts or the
        play ends, i.e. until its slowest host was done, with all tasks of an
        include and the handlers notified meanwhile.
        """
        if 1 <= self._step <= len(self._step_keys):
            self._measured[self._step_keys[self._step - 1]] = now - self._step_start

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

    @staticmethod
    def _counter_rows(rows):
        """Lay out rows of counters like "Task   ok 3/32 changed 0 ...". A row is a
        label and a list of (kind, value) cells, a value a list of (text, color,
        bold) segments. The values of a column are padded to the widest of them
        plus one space, so the columns line up, also with numbers of any length.
        """
        widths = {}
        for _, cells in rows:
            for column, (_, value) in enumerate(cells):
                length = sum(len(text) for text, _, _ in value)
                widths[column] = max(widths.get(column, 4), length)
        lines = []
        for label, cells in rows:
            segments = [(f'{label:<7}', None, True)]
            for column, (kind, value) in enumerate(cells):
                length = sum(len(text) for text, _, _ in value)
                segments.append((f'{kind} ', None, False))
                segments.extend(value)
                segments.append((' ' * (widths[column] - length + 1), None, False))
            lines.append(segments)
        return lines

    @staticmethod
    def _counter_cells(counts, kinds):
        """(kind, value) cells for _counter_rows(), a count in the color of its
        kind and in bold, a zero plain.
        """
        return [
            (
                kind,
                [
                    (
                        str(counts.get(kind, 0)),
                        color if counts.get(kind) else None,
                        bool(counts.get(kind)),
                    )
                ],
            )
            for kind, color in kinds
        ]

    def _draw(self, force=False):
        with self._screen_lock:
            if self._tui:
                self._render(force)

    def _render(self, force):
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

        elapsed = hms(now - self._start)
        count = len(self._play_hosts)
        right = f'{count} host{"" if count == 1 else "s"}   {elapsed}'
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
            lfops, source = lfops_origin(_COLLECTION_ROOT)
            # the most important first, the path is cut on a narrow terminal
            self._origin = f'{lfops}   ansible-core {ANSIBLE_CORE_VERSION}'
            ee = os.environ.get('LFOPS_EE_VERSION')
            if ee:
                self._origin += f'   EE {ee}'
            if source:
                self._origin += f'   mounted from {shorten_path(source)}'
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
        if self._steps:
            screen.append(
                progress_bar(
                    self._step,
                    len(self._steps),
                    width,
                    ANSIBLE_COLOR,
                    eta(
                        self._step,
                        [
                            self._measured.get(key, (self._durations or {}).get(key))
                            for key in self._step_keys
                        ],
                        self._play_start,
                        self._step_start,
                        now,
                    ),
                )
            )
        else:
            screen.append('')
        screen.append('─' * width)

        task_cells = self._counter_cells(
            self._task_counts,
            (
                ('ok', C.COLOR_OK),
                ('changed', C.COLOR_CHANGED),
                ('skipped', C.COLOR_SKIP),
                ('fatal', C.COLOR_ERROR),
                ('unreachable', C.COLOR_UNREACHABLE),
                ('ignored', C.COLOR_WARN),
            ),
        )
        if self._batch_hosts:
            # "ok 13/22/35": the ok results, the hosts still at work on the task,
            # and the hosts of the play or of the batch with "serial"
            alive = len(self._batch_hosts - self._dead_hosts)
            pending = max(alive - len(self._task_hosts), 0)
            task_cells[0][1].extend(
                [
                    (f'/{pending}', self._GRAY, False),
                    (f'/{len(self._batch_hosts)}', self._GRAY, True),
                ]
            )
        run_cells = self._counter_cells(
            self._run_counts,
            (
                ('ok', C.COLOR_OK),
                ('changed', C.COLOR_CHANGED),
                ('warning', C.COLOR_WARN),
                ('fatal', C.COLOR_ERROR),
                ('unreachable', C.COLOR_UNREACHABLE),
            ),
        )
        for segments in self._counter_rows([('Task', task_cells), ('Run', run_cells)]):
            screen.append(self._fit(segments, width))
        screen.append('─' * width)

        hosts = sorted(self._host_counts, key=lambda h: (self._host_severity(h), h))
        name_width = min(max([len(h) for h in hosts] + [4]), 30)
        screen.append(
            self._fit(
                [
                    (
                        f'{"HOST":<{name_width}}  {"F":>3} {"W":>3} {"C":>3}'
                        f' {"O":>4}  LAST WORST',
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
            # the ok count shows that a host is still at work while LAST WORST
            # stays the same
            for value, value_color, value_width in (
                (fatal, C.COLOR_ERROR, 3),
                (counts['warning'], C.COLOR_WARN, 3),
                (counts['changed'], C.COLOR_CHANGED, 3),
                (counts['ok'], C.COLOR_OK, 4),
            ):
                segments.append(
                    (
                        f' {value:>{value_width}}',
                        value_color if value else None,
                        False,
                    )
                )
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
        # Straight to the file descriptor, past the buffer of sys.stdout: Ansible
        # forks its workers while the ticker thread may be drawing, and a fork
        # while that thread holds the lock of the buffer leaves the worker hanging
        # on it when it flushes its streams at exit. Verified against the CPython
        # source: Modules/_io/bufferedio.c does not reset that lock after a fork,
        # and multiprocessing/process.py calls _flush_std_streams() at the end of
        # a worker.
        if threading.current_thread() is threading.main_thread():
            sys.stdout.flush()
        data = ''.join(out).encode('utf-8', 'replace')
        while data:
            data = data[os.write(sys.stdout.fileno(), data) :]

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
        # a task of an include_tasks or include_role is found through its parents,
        # which lead to the include; handlers are not found and keep the step
        node = task
        while node is not None:
            step = self._steps.get(node._uuid)
            if step:
                # only forward, e.g. when a failure skips to an "always" section
                if step > self._step:
                    now = time.monotonic()
                    self._learn(now)
                    self._step = step
                    self._step_start = now
                break
            node = getattr(node, '_parent', None)
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
        """The LAST WORST column of the host list: "<role> - <task>: <message>"."""
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
            # With "serial", the play starts once per batch, and the inventory is
            # restricted to the hosts of the batch; --limit still applies.
            self._play_hosts = {
                h.name
                for h in inventory.get_hosts(play.hosts, ignore_restrictions=True)
            }
            self._batch_hosts = {h.name for h in inventory.get_hosts(play.hosts)}
        except Exception:  # only for the host counters
            self._play_hosts = set()
            self._batch_hosts = set()
        self._dead_hosts = set()
        self._start_tui()
        # the last step of the previous play, or batch with "serial", is done
        self._learn(time.monotonic())
        self._steps = {}
        self._step_keys = []
        self._step = 0
        self._play_start = time.monotonic()
        self._step_start = self._play_start
        if self._tui:
            try:
                self._steps, self._step_keys = play_steps(play)
            except Exception:  # only for the progress bar, which is then left out
                pass
            # per play, to see what runs in parallel learned meanwhile
            self._durations = load_durations(self._eta_cache_dir(), self._step_keys)
        # the play line is part of the screen header, not of the details, and was
        # printed above the screen already
        self._capture = []
        self._details_section = self._play_line
        self._header = (self._play_line, None, None)
        self._draw(force=True)

    def v2_playbook_on_stats(self, stats):
        if self._tui:
            self._flush_hosts()
            # a run that is aborted never gets here and keeps its running step out
            # of the cache
            self._learn(time.monotonic())
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
