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
import os
import pty
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


def _run(columns=None):
    """Run the playbook, on a pseudo-terminal with `columns` if given. Return the
    exit code and the output.
    """
    assert _ANSIBLE_PLAYBOOK, 'ansible-playbook not found'  # nosec B101
    tmp = tempfile.mkdtemp(prefix='lfops_dashboard_')
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
            'playbook.yml': _PLAYBOOK,
        }
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
        self.assertIn('pending', screen)
        self.assertIn('ansible-core ', screen)
        self.assertIn('LFOps ', screen)
        self.assertIn('t-h01', screen)
        self.assertIn('F   W   C  LAST', screen)
        # the last notable result with the letter of its kind, the playbook
        # "linuxfabrik.lfops.test" shortened to "test"
        self.assertIn('C test - Some changes', screen)
        # ok hosts are counted, not listed
        self.assertNotIn('t-h03', screen)

    def test_details_only_for_tasks_with_changes(self):
        after = self.raw[self.raw.rindex(_SCREEN_OFF) :].replace('\r\n', '\n')
        self.assertNotIn('Task: All ok', after)
        self.assertIn('Task: Some changes', after)
        self.assertIn('changed: t-{h01,h02}', after)
        self.assertIn('PLAY RECAP', after)
        self.assertIn('# CHANGED', after)
        self.assertIn('linuxfabrik.lfops.test:\n\n* Some changes  \n', after)


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
