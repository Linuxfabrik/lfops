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

import importlib.util
import os
import shutil
import subprocess  # nosec B404
import sys
import tempfile
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
"""


class TestCompactOutput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # fail instead of skip, so a broken test env does not pass unnoticed
        assert _ANSIBLE_PLAYBOOK, 'ansible-playbook not found'  # nosec B101
        cls.tmp = tempfile.mkdtemp(prefix='lfops_compact_')
        tmp = cls.tmp
        os.makedirs(os.path.join(tmp, 'roles', 'demo', 'tasks'))
        files = {
            'inventory.yml': _INVENTORY.format(python=sys.executable),
            'playbook.yml': _PLAYBOOK.format(tmp=tmp),
            'roles/demo/tasks/main.yml': _ROLE_TASKS,
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

    def test_run_succeeds(self):
        self.assertEqual(self.returncode, 0, self.output + self.stderr)

    def test_play_line(self):
        self.assertIn('Playbook: linuxfabrik.lfops.test', self.lines)

    def test_role_and_task_on_lines_of_their_own(self):
        i = self.lines.index('Task: Role task')
        self.assertEqual(self.lines[i - 1], 'Role: demo')

    def test_ok_hosts_as_bar_and_one_line(self):
        self.assertEqual(self._block('All ok'), ['****', 'ok: t-{h01,h02,h03,h04}'])

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
        self.assertIn('fatal: [t-h03]: FAILED!', self.output)
        self.assertIn('MSG:\n\nlinuxfabrik-boom', self.output)
        self.assertIn('...ignoring', self.output)

    def test_delegated_hosts_are_merged(self):
        self.assertEqual(
            self._block('Delegated task')[-1], 'ok: t-{h01,h02,h03,h04} > localhost'
        )


if __name__ == '__main__':
    unittest.main()
