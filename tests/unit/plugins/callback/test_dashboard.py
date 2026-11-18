#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the `dashboard` stdout callback plugin.

Runs a real `ansible-playbook` with the callback against local fake hosts, on a
pseudo-terminal (full-screen view) and without a terminal (behaves like `compact`).
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import fcntl
import importlib.util
import json
import os
import pty
import re
import shutil
import struct
import subprocess  # nosec B404
import sys
import tempfile
import termios
import unittest

# next to the interpreter in a tox env or venv, else from PATH
_ANSIBLE_PLAYBOOK = shutil.which(
    'ansible-playbook', path=os.path.dirname(sys.executable)
) or shutil.which('ansible-playbook')

# the plugin is loaded by path for lfops_origin(), its imports resolve via the
# collection tree that tests/conftest.py provides
_PLUGIN_PATH = os.path.join(
    os.path.dirname(__file__),
    '..',
    '..',
    '..',
    '..',
    'plugins',
    'callback',
    'dashboard.py',
)
_spec = importlib.util.spec_from_file_location('dashboard', _PLUGIN_PATH)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
lfops_origin = _module.lfops_origin
progress_bar = _module.progress_bar
shorten_path = _module.shorten_path

_SCREEN_ON = '\x1b[?1049h'
_SCREEN_OFF = '\x1b[?1049l'

_PLAYBOOK = """
- name: 'Playbook linuxfabrik.lfops.test'
  hosts: 'all'
  gather_facts: false
  tasks:
    - name: 'All ok'
      ansible.builtin.command: 'true'
      changed_when: false

    - name: 'Some changes'
      ansible.builtin.command: 'echo linuxfabrik-changed'
      changed_when: inventory_hostname in ['t-h01', 't-h02']
"""


def _run(columns=None, playbook=_PLAYBOOK, files=None, workdir=None):
    """Run the playbook, on a pseudo-terminal with `columns` if given, with the
    additional `files` (name -> content) next to it. Everything, including the
    durations for the ETA, goes to `workdir`, by default a directory of its own
    that is removed afterwards. Return the exit code and the output.
    """
    assert _ANSIBLE_PLAYBOOK, 'ansible-playbook not found'  # nosec B101
    tmp = workdir or tempfile.mkdtemp(prefix='lfops_dashboard_')
    try:
        hosts = ''.join(f'    t-h{i:02d}:\n' for i in range(1, 5))
        files = {
            'ansible.cfg': '[defaults]\n',
            'inventory.yml': (
                'all:\n  hosts:\n'
                + hosts
                + "  vars:\n    ansible_connection: 'local'\n"
                + f"    ansible_python_interpreter: '{sys.executable}'\n"
            ),
            'playbook.yml': playbook,
            **(files or {}),
        }
        for name, content in files.items():
            with open(os.path.join(tmp, name), 'w') as f:
                f.write(content)
        env = dict(os.environ)
        env.update(
            {
                'ANSIBLE_CALLBACK_DASHBOARD_ETA_CACHE_DIR': os.path.join(tmp, 'eta'),
                'ANSIBLE_CONFIG': os.path.join(tmp, 'ansible.cfg'),
                'ANSIBLE_HOME': os.path.join(tmp, '.ansible'),
                'ANSIBLE_LOCAL_TEMP': os.path.join(tmp, '.ansible', 'tmp'),
                'ANSIBLE_NOCOLOR': '1',
                'ANSIBLE_STDOUT_CALLBACK': 'linuxfabrik.lfops.dashboard',
            }
        )
        cmd = [
            _ANSIBLE_PLAYBOOK,
            '--inventory',
            os.path.join(tmp, 'inventory.yml'),
            os.path.join(tmp, 'playbook.yml'),
        ]
        if columns is None:
            proc = subprocess.run(  # nosec B603
                cmd, capture_output=True, check=False, cwd=tmp, env=env, text=True
            )
            return proc.returncode, proc.stdout
        master, slave = pty.openpty()
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack('HHHH', 30, columns, 0, 0))
        proc = subprocess.Popen(  # nosec B603
            cmd, cwd=tmp, env=env, stdin=slave, stdout=slave, stderr=slave
        )
        os.close(slave)
        chunks = []
        while True:
            try:
                data = os.read(master, 65536)
            except OSError:  # EIO once the child closed the terminal
                break
            if not data:
                break
            chunks.append(data)
        os.close(master)
        return proc.wait(), b''.join(chunks).decode('utf-8', 'replace')
    finally:
        if not workdir:
            shutil.rmtree(tmp, ignore_errors=True)


class TestDashboardOnTerminal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.returncode, cls.raw = _run(columns=100)

    def test_run_succeeds(self):
        self.assertEqual(self.returncode, 0, self.raw)

    def test_uses_and_leaves_the_alternate_screen(self):
        self.assertIn(_SCREEN_ON, self.raw)
        self.assertIn(_SCREEN_OFF, self.raw)

    def test_screen_shows_counters_and_the_hosts_needing_attention(self):
        screen = self.raw[self.raw.index(_SCREEN_ON) : self.raw.rindex(_SCREEN_OFF)]
        self.assertIn('HOST', screen)
        self.assertIn('Task   ok', screen)
        self.assertIn('Run    ok', screen)
        # the ok results of the task, the hosts still at work on it, all hosts
        self.assertRegex(screen, r'Task   ok \d/\d/4 +changed ')
        self.assertIn('Task   ok 0/4/4 ', screen)
        self.assertIn('ansible-core ', screen)
        self.assertIn('LFOps ', screen)
        self.assertIn('t-h01', screen)
        self.assertIn('F   W   C    O  LAST WORST', screen)
        # the last notable result with the letter of its kind, the playbook
        # "linuxfabrik.lfops.test" shortened to "test"
        self.assertIn('C test - Some changes', screen)
        # hosts with only ok results are listed with their last ok result
        self.assertIn('O test - Some changes', screen)
        # F, W, C and O counts: one changed and one ok, or two ok results
        self.assertRegex(screen, r't-h01\s+0\s+0\s+1\s+1  C test - Some changes')
        self.assertRegex(screen, r't-h03\s+0\s+0\s+0\s+2  O test - Some changes')

    def test_hosts_sorted_by_severity_then_name(self):
        # the last drawn host list, rows start with the host name
        screen = self.raw[self.raw.rindex('LAST WORST') : self.raw.rindex(_SCREEN_OFF)]
        order = sorted(
            ('t-h01', 't-h02', 't-h03', 't-h04'), key=lambda host: screen.index(host)
        )
        # changed before ok, by name within
        self.assertEqual(order, ['t-h01', 't-h02', 't-h03', 't-h04'])

    def test_details_only_for_tasks_with_changes(self):
        after = self.raw[self.raw.rindex(_SCREEN_OFF) :].replace('\r\n', '\n')
        self.assertNotIn('Task: All ok', after)
        self.assertIn('Task: Some changes', after)
        self.assertIn('changed: t-{h01,h02}', after)
        self.assertIn('PLAY RECAP', after)
        self.assertIn('# CHANGED', after)
        self.assertIn('linuxfabrik.lfops.test:\n\n* Some changes  \n', after)


class TestSerial(unittest.TestCase):
    def test_header_counts_all_hosts_of_the_play(self):
        # with "serial", the play starts once per batch of one host
        playbook = _PLAYBOOK.replace(
            "  hosts: 'all'\n", "  hosts: 'all'\n  serial: 1\n"
        )
        returncode, raw = _run(columns=100, playbook=playbook)
        self.assertEqual(returncode, 0, raw)
        self.assertIn('4 hosts', raw)
        self.assertNotIn('1 host ', raw)


class TestProgress(unittest.TestCase):
    def test_includes_are_one_step_rescue_not_counted(self):
        playbook = _PLAYBOOK.replace(
            "    - name: 'Some changes'\n",
            "    - name: 'Include'\n"
            "      ansible.builtin.include_tasks: 'included.yml'\n"
            '\n'
            '    - block:\n'
            "        - name: 'In a block'\n"
            "          ansible.builtin.command: 'true'\n"
            '          changed_when: false\n'
            '      rescue:\n'
            "        - name: 'Rescue'\n"
            "          ansible.builtin.command: 'true'\n"
            '\n'
            "    - name: 'Some changes'\n",
        )
        included = (
            "- name: 'Included 1'\n"
            "  ansible.builtin.command: 'true'\n"
            '  changed_when: false\n'
            "- name: 'Included 2'\n"
            "  ansible.builtin.command: 'true'\n"
            '  changed_when: false\n'
        )
        returncode, raw = _run(
            columns=100, playbook=playbook, files={'included.yml': included}
        )
        self.assertEqual(returncode, 0, raw)
        screen = raw[raw.index(_SCREEN_ON) : raw.rindex(_SCREEN_OFF)]
        steps = list(dict.fromkeys(re.findall(r'step (\d+)/(\d+)', screen)))
        # All ok, Include (with its two tasks), In a block, Some changes
        self.assertEqual(
            steps, [('0', '4'), ('1', '4'), ('2', '4'), ('3', '4'), ('4', '4')]
        )
        self.assertIn(' step 4/4 (100%) ', screen)

    def test_bar_without_color(self):
        bar = progress_bar(7, 21, 80, color=False)
        self.assertEqual(bar, ' step 7/21 (33%) ' + '#' * 9 + ' ' * 54)

    def test_bar_with_color_reverses_the_done_part(self):
        bar = progress_bar(7, 21, 40, color=True)
        self.assertTrue(bar.startswith('\033[7m'))
        self.assertEqual(
            bar.replace('\033[7m', '').replace('\033[0m', ''),
            ' step 7/21 (33%) '.ljust(40),
        )

    def test_bar_with_remaining_time(self):
        bar = progress_bar(7, 21, 60, color=False, remaining=3725)
        self.assertTrue(bar.startswith(' step 7/21 (33%)   ETA 01:02:05 '))

    def test_bar_cut_to_width(self):
        self.assertEqual(len(progress_bar(1, 3, 10, color=False)), 10)

    def test_eta_from_the_finished_steps(self):
        unknown = [None] * 21
        # 6 steps done in 60 s, 15 left at 10 s each, 4 s into step 7
        self.assertEqual(_module.eta(7, unknown, 100, 160, 164), 146)
        # no step done yet
        self.assertIsNone(_module.eta(1, unknown, 100, 100, 130))
        # a step that takes longer than the average, like a large include, keeps
        # the estimate for the 14 steps after it
        self.assertEqual(_module.eta(7, unknown, 100, 160, 460), 140)
        # and the last step does not go below zero
        self.assertEqual(_module.eta(21, unknown, 0, 200, 900), 0)
        # before the first step
        self.assertIsNone(_module.eta(0, [5.0] * 21, 100, 100, 100))

    def test_eta_from_the_durations_of_earlier_runs(self):
        # all known: available from the first step on, 2 s into step 1 of 3
        self.assertEqual(_module.eta(1, [10.0, 20.0, 300.0], 100, 100, 102), 328)
        # a known slow step after average ones: 2 steps done in 20 s, the unknown
        # step 3 at 10 s, the include of step 4 took 300 s last time
        durations = [None, None, None, 300.0]
        self.assertEqual(_module.eta(3, durations, 100, 120, 124), 306)
        # a known step running longer than last time does not go below zero
        self.assertEqual(_module.eta(4, durations, 100, 130, 500), 0)


class TestDurations(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='lfops_dashboard_')
        self.directory = os.path.join(self.tmp, 'lfops', 'dashboard')

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_saved_and_loaded(self):
        _module.save_durations(self.directory, {'roles/a/tasks/main.yml:3': 12.34})
        self.assertEqual(
            _module.load_durations(self.directory),
            {'roles/a/tasks/main.yml:3': 12.3},
        )
        # directory and parent private
        for path in (self.directory, os.path.dirname(self.directory)):
            self.assertEqual(os.stat(path).st_mode & 0o777, 0o700)

    def test_last_duration_wins_and_others_are_kept(self):
        _module.save_durations(self.directory, {'a:1': 50.0, 'b:1': 5.0})
        _module.save_durations(self.directory, {'a:1': 10.0})
        self.assertEqual(
            _module.load_durations(self.directory), {'a:1': 10.0, 'b:1': 5.0}
        )

    def test_old_entries_are_dropped(self):
        now = 1_800_000_000
        _module.save_durations(self.directory, {'old:1': 5.0}, now=now)
        _module.save_durations(
            self.directory, {'new:1': 7.0}, now=now + _module._DURATIONS_MAX_AGE + 1
        )
        self.assertEqual(_module.load_durations(self.directory), {'new:1': 7.0})

    def test_broken_file_is_ignored_and_replaced(self):
        os.makedirs(self.directory)
        with open(os.path.join(self.directory, 'durations.json'), 'w') as f:
            f.write('{"a:1": {"seconds": 1')
        self.assertEqual(_module.load_durations(self.directory), {})
        _module.save_durations(self.directory, {'b:1': 2.0})
        self.assertEqual(_module.load_durations(self.directory), {'b:1': 2.0})

    def test_symlinked_directory_is_not_used(self):
        target = os.path.join(self.tmp, 'elsewhere')
        os.makedirs(target)
        os.makedirs(os.path.dirname(self.directory))
        os.symlink(target, self.directory)
        _module.save_durations(self.directory, {'a:1': 1.0})
        self.assertEqual(os.listdir(target), [])
        self.assertEqual(_module.load_durations(self.directory), {})

    def test_disabled_with_an_empty_value(self):
        _module.save_durations('', {'a:1': 1.0})
        self.assertEqual(_module.load_durations(''), {})

    def test_task_key_relative_to_the_collection(self):
        class Role:
            def __init__(self, name):
                self.name = name

            def get_name(self):
                return self.name

        class Task:
            action = 'ansible.builtin.gather_facts'

            def __init__(self, path, roles=()):
                self.path = path
                self.roles = [Role(name) for name in roles]

            def get_dep_chain(self):
                return self.roles or None

            def get_path(self):
                return self.path

            def get_name(self):
                return 'Gathering Facts'

        self.assertEqual(
            _module.step_key(Task('/x/lfops/roles/a/tasks/main.yml:3'), '/x/lfops'),
            'roles/a/tasks/main.yml:3',
        )
        self.assertEqual(
            _module.step_key(Task('/x/lfops2/roles/a/tasks/main.yml:3'), '/x/lfops'),
            '/x/lfops2/roles/a/tasks/main.yml:3',
        )
        self.assertEqual(
            _module.step_key(Task(''), '/x/lfops'),
            'ansible.builtin.gather_facts Gathering Facts',
        )
        # a role imported by another one, by the chain of roles
        self.assertEqual(
            _module.step_key(
                Task(
                    '/x/lfops/roles/shared/tasks/x.yml:11', ['l.l.aide', 'l.l.shared']
                ),
                '/x/lfops',
            ),
            'roles/shared/tasks/x.yml:11 [l.l.aide > l.l.shared]',
        )


class TestLearnedEta(unittest.TestCase):
    def test_durations_learned_and_used_by_the_next_run(self):
        # the include sleeps in its second task, so the step only knows it from
        # an earlier run
        playbook = _PLAYBOOK.replace(
            "    - name: 'Some changes'\n",
            "    - name: 'Include'\n"
            "      ansible.builtin.include_tasks: 'included.yml'\n"
            '\n'
            "    - name: 'Some changes'\n",
        )
        included = (
            "- name: 'Included 1'\n"
            "  ansible.builtin.command: 'true'\n"
            '  changed_when: false\n'
            "- name: 'Sleep on one host'\n"
            "  ansible.builtin.command: 'sleep 3'\n"
            '  changed_when: false\n'
            "  when: inventory_hostname == 't-h04'\n"
        )
        tmp = tempfile.mkdtemp(prefix='lfops_dashboard_eta_')
        try:
            for _ in range(2):
                returncode, raw = _run(
                    columns=100,
                    playbook=playbook,
                    files={'included.yml': included},
                    workdir=tmp,
                )
                self.assertEqual(returncode, 0, raw)
            with open(os.path.join(tmp, 'eta', 'durations.json')) as f:
                durations = json.load(f)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        # the three steps by file and line of the playbook, outside the collection
        self.assertEqual(len(durations), 3, durations)
        self.assertTrue(all('playbook.yml:' in key for key in durations), durations)
        # the include with its tasks, until the slowest host was done
        slowest = max(durations.values(), key=lambda value: value['seconds'])
        self.assertGreaterEqual(slowest['seconds'], 3, durations)
        # in the second run, the ETA is known from the first step on and counts
        # the sleep of the include
        screen = raw[raw.index(_SCREEN_ON) : raw.rindex(_SCREEN_OFF)]
        first = re.search(r'step 1/3 \(33%\)   ETA 00:00:(\d\d)', screen)
        self.assertIsNotNone(first, screen)
        self.assertGreaterEqual(int(first.group(1)), 3)


class TestTicker(unittest.TestCase):
    def test_screen_redrawn_during_a_long_task(self):
        # no event for 3 seconds, the elapsed time still moves on
        playbook = _PLAYBOOK.replace(
            "    - name: 'Some changes'\n",
            "    - name: 'Sleep'\n"
            "      ansible.builtin.command: 'sleep 3'\n"
            '      changed_when: false\n'
            '\n'
            "    - name: 'Some changes'\n",
        )
        returncode, raw = _run(columns=100, playbook=playbook)
        self.assertEqual(returncode, 0, raw)
        screen = raw[raw.index(_SCREEN_ON) : raw.rindex(_SCREEN_OFF)]
        # every frame starts in the top left corner
        frames = [f for f in screen.split('\x1b[1;1H') if 'Task: Sleep' in f]
        elapsed = {re.search(r'hosts   (\d\d:\d\d:\d\d)', f).group(1) for f in frames}
        # drawn at the start of the task, and at least twice while it sleeps
        self.assertGreaterEqual(len(elapsed), 3, elapsed)
        # no warning about forking a multi-threaded process (Python 3.12+)
        self.assertNotIn('multi-threaded', raw)


class TestCounterRows(unittest.TestCase):
    def test_columns_aligned_and_apart_for_long_numbers(self):
        rows = _module.CallbackModule._counter_rows(
            [
                (
                    'Task',
                    [
                        (
                            'ok',
                            [
                                ('3', None, True),
                                ('/2', None, False),
                                ('/32', None, True),
                            ],
                        )
                    ],
                ),
                (
                    'Run',
                    [('ok', [('11044', None, True)]), ('changed', [('5', None, True)])],
                ),
            ]
        )
        task, run = (''.join(text for text, _, _ in row) for row in rows)
        self.assertEqual(run, 'Run    ok 11044  changed 5    ')
        self.assertEqual(task, 'Task   ok 3/2/32 ')


class TestShortenPath(unittest.TestCase):
    def test_parents_reduced_to_their_initial(self):
        self.assertEqual(
            shorten_path('/home/user/git/linuxfabrik/github/lfops'), '/h/u/g/l/g/lfops'
        )

    def test_without_a_slash_unchanged(self):
        self.assertEqual(shorten_path('lfops'), 'lfops')
        self.assertEqual(shorten_path(''), '')


class TestHostSeverity(unittest.TestCase):
    def test_order_fatal_warning_changed_ignored_ok(self):
        callback = _module.CallbackModule()
        for host, kind in (
            ('a-ok', 'ok'),
            ('b-ignored', 'ignored'),
            ('c-changed', 'changed'),
            ('d-warning', 'warning'),
            ('e-unreachable', 'unreachable'),
            ('f-failed', 'failed'),
            ('g-changed', 'changed'),
        ):
            callback._host_counts[host] = _module.Counter({kind: 1})
        hosts = sorted(
            callback._host_counts, key=lambda h: (callback._host_severity(h), h)
        )
        self.assertEqual(
            hosts,
            [
                'e-unreachable',
                'f-failed',
                'd-warning',
                'c-changed',
                'g-changed',
                'b-ignored',
                'a-ok',
            ],
        )


class TestDashboardFallback(unittest.TestCase):
    def test_without_a_terminal_like_compact(self):
        returncode, output = _run()
        self.assertEqual(returncode, 0, output)
        self.assertNotIn(_SCREEN_ON, output)
        self.assertIn('Task: All ok', output)
        self.assertIn('ok: all 4 hosts', output)

    def test_on_a_narrow_terminal_like_compact(self):
        returncode, output = _run(columns=50)
        self.assertEqual(returncode, 0, output)
        self.assertNotIn(_SCREEN_ON, output)
        self.assertIn('Task: All ok', output)


class TestLfopsOrigin(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='lfops_origin_')
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def _write(self, name, content):
        with open(os.path.join(self.tmp, name), 'w') as f:
            f.write(content)

    def test_installed_collection(self):
        self._write('MANIFEST.json', '{"collection_info": {"version": "9.0.0"}}')
        self.assertEqual(
            lfops_origin(self.tmp, mountinfo='/nonexistent'), ('LFOps 9.0.0', None)
        )

    @unittest.skipUnless(shutil.which('git'), 'git not found')
    def test_mounted_checkout_with_changes(self):
        self._write('galaxy.yml', "version: 'main'\n")
        # Without the GIT_* variables of the environment: during a commit, git sets
        # GIT_DIR and GIT_INDEX_FILE for its hooks (pre-commit runs this test), which
        # would point these git calls at the repository being committed to.
        env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        env.update(
            GIT_AUTHOR_NAME='linuxfabrik',
            GIT_AUTHOR_EMAIL='linuxfabrik@example.com',
            GIT_COMMITTER_NAME='linuxfabrik',
            GIT_COMMITTER_EMAIL='linuxfabrik@example.com',
        )
        for args in (
            ['init', '--quiet', '--initial-branch=feature'],
            ['add', 'galaxy.yml'],
            ['commit', '--quiet', '--message=init'],
        ):
            subprocess.run(['git', '-C', self.tmp, *args], check=True, env=env)  # nosec B603 B607
        self._write('galaxy.yml', "version: 'main'\n# changed\n")
        commit = subprocess.run(  # nosec B603 B607
            ['git', '-C', self.tmp, 'rev-parse', '--short=8', 'HEAD'],
            capture_output=True,
            check=True,
            env=env,
            text=True,
        ).stdout.strip()
        root = os.path.realpath(self.tmp)
        mountinfo = os.path.join(self.tmp, 'mountinfo')
        self._write(
            'mountinfo',
            f'4031 4033 0:36 /home/user/lfops {root} rw,relatime - btrfs /dev/x rw\n',
        )
        self.assertEqual(
            lfops_origin(self.tmp, mountinfo=mountinfo),
            (f'LFOps feature@{commit}, 1 uncommitted', '/home/user/lfops'),
        )


if __name__ == '__main__':
    unittest.main()
