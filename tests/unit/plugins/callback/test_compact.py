#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the `compact` stdout callback plugin.

A callback runs on the Ansible controller only, so this test belongs to the
controller matrix. Besides the host list compaction, it runs a real
`ansible-playbook` against local fake hosts with the callback enabled, since the
callback builds on internals of the default callback that differ between the
ansible-core releases in the tox matrix.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import fcntl
import importlib.util
import os
import pty
import shutil
import struct
import subprocess  # nosec B404
import sys
import tempfile
import termios
import textwrap
import unittest

_PLUGIN_PATH = os.path.join(
    os.path.dirname(__file__),
    '..',
    '..',
    '..',
    '..',
    'plugins',
    'callback',
    'compact.py',
)
_spec = importlib.util.spec_from_file_location('compact', _PLUGIN_PATH)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
compact_hosts = _module.compact_hosts

# next to the interpreter in a tox env or venv, else from PATH
_ANSIBLE_PLAYBOOK = shutil.which(
    'ansible-playbook', path=os.path.dirname(sys.executable)
) or shutil.which('ansible-playbook')


class TestCompactHosts(unittest.TestCase):
    def test_merges_hosts_with_a_common_prefix(self):
        self.assertEqual(
            compact_hosts(['web-31', 'web-01', 'db-p-01', 'proxy01']),
            'db-p-01, proxy01, web-{01,31}',
        )

    def test_single_host_stays_unbraced(self):
        self.assertEqual(compact_hosts(['web-01']), 'web-01')

    def test_host_without_dash(self):
        self.assertEqual(compact_hosts(['localhost', 'h01']), 'h01, localhost')

    def test_duplicates_are_listed_once(self):
        self.assertEqual(compact_hosts(['a-1', 'a-1', 'a-2']), 'a-{1,2}')

    def test_delegated_hosts_are_grouped_by_target(self):
        self.assertEqual(
            compact_hosts(
                [
                    'web-a01 -> localhost',
                    'web-a02',
                    'web-a03 -> localhost',
                    'web-b01 -> other',
                ]
            ),
            'web-{a01,a03} > localhost, web-a02, web-b01 > other',
        )


_INVENTORY = """
all:
  hosts:
    t-h01:
    t-h02:
    t-h03:
    t-h04:
  vars:
    ansible_connection: 'local'
    ansible_python_interpreter: '{python}'
"""

_ROLE_TASKS = """
- name: 'Role task'
  ansible.builtin.command: 'true'
  changed_when: inventory_hostname == 't-h04'

- name: 'Second role task'
  ansible.builtin.command: 'true'
  changed_when: false
"""

_PLAYBOOK = """
- name: 'Playbook linuxfabrik.lfops.test'
  hosts: 'all'
  gather_facts: false
  roles:
    - 'demo'
  tasks:
    - name: 'All ok'
      ansible.builtin.command: 'true'
      changed_when: false

    - name: 'Changed without diff'
      ansible.builtin.command: 'echo linuxfabrik-changed'
      changed_when: inventory_hostname == 't-h02'

    - name: 'Changed with diff'
      ansible.builtin.copy:
        content: "linuxfabrik\\n"
        dest: '{tmp}/{{{{ inventory_hostname }}}}.txt'
        mode: '0644'
      when: inventory_hostname == 't-h01'

    - name: 'Failing task'
      ansible.builtin.fail:
        msg: 'linuxfabrik-boom'
      when: inventory_hostname == 't-h03'
      ignore_errors: true

    - name: 'Delegated task'
      ansible.builtin.command: 'true'
      changed_when: false
      delegate_to: 'localhost'

    - name: 'Include per item'
      ansible.builtin.include_tasks: 'roles/demo/tasks/included.yml'
      loop:
        - name: 'alpha'
          packages: ['linuxfabrik-a', 'linuxfabrik-b']

    - name: 'Grouped changes'
      ansible.builtin.shell: >-
        {{{{ 'echo a; echo b' if inventory_hostname == 't-h01' else 'echo b; echo a' }}}}
      changed_when: inventory_hostname in ['t-h01', 't-h02']

    - name: 'Warning task'
      warn_module:
      when: inventory_hostname in ['t-h02', 't-h03']

    - name: 'Final failure'
      ansible.builtin.fail:
        msg: 'linuxfabrik-final'
      when: inventory_hostname == 't-h04'
"""

# a module that only emits a warning, found in library/ next to the playbook
_WARN_MODULE = """
from ansible.module_utils.basic import AnsibleModule
module = AnsibleModule(argument_spec={})
module.warn('linuxfabrik-warning')
module.exit_json(changed=False)
"""


class TestCompactOutput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # fail instead of skip, so a broken test env does not pass unnoticed
        assert _ANSIBLE_PLAYBOOK, 'ansible-playbook not found'  # nosec B101
        cls.tmp = tempfile.mkdtemp(prefix='lfops_compact_')
        tmp = cls.tmp
        os.makedirs(os.path.join(tmp, 'library'))
        os.makedirs(os.path.join(tmp, 'roles', 'demo', 'tasks'))
        files = {
            'inventory.yml': _INVENTORY.format(python=sys.executable),
            'playbook.yml': _PLAYBOOK.format(tmp=tmp),
            'library/warn_module.py': _WARN_MODULE,
            'roles/demo/tasks/main.yml': _ROLE_TASKS,
            'roles/demo/tasks/included.yml': (
                "- name: 'Included task'\n  ansible.builtin.debug:\n    msg: 'x'\n"
            ),
            # an empty config, so no ansible.cfg of the developer interferes
            'ansible.cfg': '[defaults]\n',
        }
        for name, content in files.items():
            with open(os.path.join(tmp, name), 'w') as f:
                f.write(textwrap.dedent(content))
        env = dict(os.environ)
        env.update(
            {
                'ANSIBLE_CONFIG': os.path.join(tmp, 'ansible.cfg'),
                'ANSIBLE_HOME': os.path.join(tmp, '.ansible'),
                'ANSIBLE_LOCAL_TEMP': os.path.join(tmp, '.ansible', 'tmp'),
                'ANSIBLE_NOCOLOR': '1',
                'ANSIBLE_STDOUT_CALLBACK': 'linuxfabrik.lfops.compact',
            }
        )
        proc = subprocess.run(  # nosec B603
            [
                _ANSIBLE_PLAYBOOK,
                '--inventory',
                os.path.join(tmp, 'inventory.yml'),
                '--diff',
                os.path.join(tmp, 'playbook.yml'),
            ],
            capture_output=True,
            check=False,
            cwd=tmp,
            env=env,
            text=True,
        )
        cls.output = proc.stdout
        cls.lines = proc.stdout.splitlines()
        cls.returncode = proc.returncode
        cls.stderr = proc.stderr

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _block(self, task_name):
        """Return the non-empty output lines of one task block, without its banner.
        The block ends at the next banner (diffs contain empty lines).
        """
        start = self.lines.index(f'Task: {task_name}') + 1
        end = start
        while end < len(self.lines) and not self.lines[end].startswith(
            ('PLAY RECAP', 'Role: ', 'Task: ')
        ):
            end += 1
        return [line for line in self.lines[start:end] if line]

    def test_run_fails_for_the_failing_host_only(self):
        # 2 is the exit code of ansible-playbook for failed hosts
        self.assertEqual(self.returncode, 2, self.output + self.stderr)

    def test_include_names_hosts_compact_and_the_item_by_name(self):
        self.assertIn(
            'included: demo/tasks/included.yml for t-{h01,h02,h03,h04} (item=alpha)',
            self.lines,
        )

    def test_changes_with_the_same_lines_are_one_group(self):
        # same lines in another order, like restorecon -v
        block = self._block('Grouped changes')
        self.assertEqual(block[1:3], ['changed: t-{h01,h02}', '  stdout:'])
        # shown in the order of the host that finished first
        self.assertEqual(sorted(block[3:5]), ['    a', '    b'])
        self.assertEqual(block[5:], ['ok: t-{h03,h04}'])

    def test_identical_warnings_are_grouped_with_their_hosts(self):
        self.assertEqual(self.stderr.count('[WARNING]: linuxfabrik-warning'), 1)
        self.assertIn('[WARNING]: linuxfabrik-warning\n  on t-{h02,h03}\n', self.stderr)

    def test_report_per_message_by_severity(self):
        # the report follows the recap
        i = self.lines.index('# FATAL')
        play = 'linuxfabrik.lfops.test'
        self.assertEqual(
            self.lines[i:],
            [
                '# FATAL',
                '',
                f'* {play} - Final failure: linuxfabrik-final',
                '  t-h04',
                '',
                '# WARNING',
                '',
                f'* {play} - Warning task: linuxfabrik-warning',
                '  t-{h02,h03}',
                '',
                '# IGNORED',
                '',
                f'* {play} - Failing task: linuxfabrik-boom',
                '  t-h03',
                '',
                '# CHANGED',
                '',
                # role tasks name the role instead of the playbook
                '* demo - Role task',
                '  t-h04',
                f'* {play} - Changed without diff',
                '  t-h02',
                f'* {play} - Changed with diff',
                '  t-h01',
                f'* {play} - Grouped changes',
                '  t-{h01,h02}',
                '',
            ],
        )

    def test_play_line(self):
        self.assertIn('Playbook: linuxfabrik.lfops.test', self.lines)

    def test_role_and_task_on_lines_of_their_own(self):
        i = self.lines.index('Task: Role task')
        self.assertEqual(self.lines[i - 1], 'Role: demo')

    def test_section_header_only_when_the_section_changes(self):
        self.assertEqual(self.lines.count('Role: demo'), 1)
        # back to the tasks of the playbook after the role
        i = self.lines.index('Task: All ok')
        self.assertEqual(self.lines[i - 1], 'Playbook: linuxfabrik.lfops.test')
        self.assertEqual(self.lines.count('Playbook: linuxfabrik.lfops.test'), 2)

    def test_ok_hosts_as_bar_and_one_line(self):
        self.assertEqual(self._block('All ok'), ['****', 'ok: all 4 hosts'])

    def test_changed_without_diff_shows_the_result(self):
        block = self._block('Changed without diff')
        i = block.index('changed: t-h02')
        self.assertEqual(block[i + 1 : i + 3], ['  stdout:', '    linuxfabrik-changed'])
        self.assertEqual(block[-1], 'ok: t-{h01,h03,h04}')

    def test_changed_with_diff_has_the_host_above_the_diff(self):
        block = self._block('Changed with diff')
        i = block.index('changed: t-h01')
        self.assertTrue(block[i + 1].startswith('--- before'), block)
        self.assertNotIn('changed: [t-h01]', self.output)
        self.assertEqual(block[-1], 'skipped: t-{h02,h03,h04}')

    def test_failed_shows_the_message_as_plain_text(self):
        self.assertIn('fatal: [t-h04]: FAILED!', self.output)
        self.assertIn('MSG:\n\nlinuxfabrik-final', self.output)

    def test_ignored_failure_is_compact(self):
        self.assertEqual(
            self._block('Failing task')[1:],
            ['ignored: t-h03', '  linuxfabrik-boom', 'skipped: t-{h01,h02,h04}'],
        )
        self.assertNotIn('fatal: [t-h03]', self.output)

    def test_delegated_hosts_are_merged(self):
        self.assertEqual(
            self._block('Delegated task')[-1], 'ok: all 4 hosts > localhost'
        )


_TERMINAL_HOSTS = 50
_TERMINAL_COLUMNS = 40


class TestCompactOutputOnTerminal(unittest.TestCase):
    """On a terminal, the callback ends every bar line and redraws it from the line
    below (cursor up), so that the event markers of ansible-runner never sit behind
    the bar. Run on a pseudo-terminal that is narrower than the number of hosts and
    replay the redraws.
    """

    @classmethod
    def setUpClass(cls):
        assert _ANSIBLE_PLAYBOOK, 'ansible-playbook not found'  # nosec B101
        cls.tmp = tempfile.mkdtemp(prefix='lfops_compact_tty_')
        tmp = cls.tmp
        hosts = ''.join(f'    t-h{i:02d}:\n' for i in range(_TERMINAL_HOSTS))
        files = {
            'inventory.yml': (
                'all:\n  hosts:\n'
                + hosts
                + "  vars:\n    ansible_connection: 'local'\n"
                + f"    ansible_python_interpreter: '{sys.executable}'\n"
            ),
            'playbook.yml': (
                "- hosts: 'all'\n  gather_facts: false\n  tasks:\n"
                "    - name: 'All ok'\n      ansible.builtin.debug:\n"
                "        msg: 'linuxfabrik'\n"
                "    - name: 'Warning'\n      warn_module:\n"
                "      when: inventory_hostname == 't-h07'\n"
                # the fileglob lookup warns about the missing directory of each
                # host, before `when` is evaluated
                "    - name: 'Lookup warning'\n      ansible.builtin.debug:\n"
                "        msg: '{{ item }}'\n"
                '      with_fileglob:\n'
                "        - '/nonexistent-linuxfabrik/{{ inventory_hostname }}/*'\n"
                '      when: false\n'
            ),
            # a module that only emits a warning, found in library/ next to the
            # playbook
            'library/warn_module.py': (
                'from ansible.module_utils.basic import AnsibleModule\n'
                'module = AnsibleModule(argument_spec={})\n'
                "module.warn('linuxfabrik-warning')\n"
                'module.exit_json(changed=False)\n'
            ),
            'ansible.cfg': '[defaults]\n',
        }
        os.makedirs(os.path.join(tmp, 'library'))
        for name, content in files.items():
            with open(os.path.join(tmp, name), 'w') as f:
                f.write(content)
        env = dict(os.environ)
        env.update(
            {
                'ANSIBLE_CONFIG': os.path.join(tmp, 'ansible.cfg'),
                'ANSIBLE_HOME': os.path.join(tmp, '.ansible'),
                'ANSIBLE_LOCAL_TEMP': os.path.join(tmp, '.ansible', 'tmp'),
                'ANSIBLE_NOCOLOR': '1',
                'ANSIBLE_STDOUT_CALLBACK': 'linuxfabrik.lfops.compact',
            }
        )
        master, slave = pty.openpty()
        # Display takes the terminal width from stdin
        fcntl.ioctl(
            slave, termios.TIOCSWINSZ, struct.pack('HHHH', 24, _TERMINAL_COLUMNS, 0, 0)
        )
        proc = subprocess.Popen(  # nosec B603
            [
                _ANSIBLE_PLAYBOOK,
                '--inventory',
                os.path.join(tmp, 'inventory.yml'),
                os.path.join(tmp, 'playbook.yml'),
            ],
            cwd=tmp,
            env=env,
            stdin=slave,
            stdout=slave,
            stderr=slave,
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
        cls.returncode = proc.wait()
        cls.raw = b''.join(chunks).decode('utf-8', 'replace')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _screen_lines(self):
        """Replay the output like a terminal: a line that starts with "cursor up,
        carriage return" replaces the line above it.
        """
        lines = []
        for line in self.raw.replace('\r\n', '\n').split('\n'):
            if line.startswith('\x1b[A\r'):
                lines[-1] = line[len('\x1b[A\r') :]
            else:
                lines.append(line)
        return lines

    def test_run_succeeds(self):
        self.assertEqual(self.returncode, 0, self.raw)

    def test_bar_uses_the_full_width(self):
        self.assertIn('\x1b[A\r', self.raw)
        lines = self._screen_lines()
        start = lines.index('Task: All ok') + 1
        bar = []
        for line in lines[start:]:
            if not line.startswith('*'):
                break
            bar.append(line)
        # one column less than the terminal, so a full line never wraps
        self.assertEqual(
            [len(line) for line in bar],
            [_TERMINAL_COLUMNS - 1, _TERMINAL_HOSTS - (_TERMINAL_COLUMNS - 1)],
        )

    def _task_lines(self, task_name):
        lines = self._screen_lines()
        start = lines.index(f'Task: {task_name}') + 1
        end = start
        while end < len(lines) and lines[end]:
            end += 1
        return lines[start:end]

    def test_warning_follows_the_task_with_its_host(self):
        block = self._task_lines('Warning')
        self.assertTrue(block[0].startswith('*'), block)
        self.assertEqual(block[-2:], ['[WARNING]: linuxfabrik-warning', '  on t-h07'])

    def test_lookup_warnings_of_all_hosts_are_one_group(self):
        block = self._task_lines('Lookup warning')
        # the bar stays in one piece (39 columns, 50 hosts)
        self.assertEqual([len(line) for line in block[:2]], [39, 11])
        warnings = [line for line in block if line.startswith('[WARNING]')]
        self.assertEqual(len(warnings), 1, block)
        self.assertIn("'/nonexistent-linuxfabrik/<host>", warnings[0])
        self.assertEqual(
            block[block.index(warnings[0]) + 1], f'  on all {_TERMINAL_HOSTS} hosts'
        )


if __name__ == '__main__':
    unittest.main()
