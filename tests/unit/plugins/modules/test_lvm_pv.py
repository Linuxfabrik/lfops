#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the vendored lvm_pv module.

main() is driven through ansible_harness. The LVM tools are replaced by a
fake AnsibleModule.run_command that keeps the PV state in memory and records
every command, so the tests assert which commands the module issues (and
which it must not issue, e.g. in check mode) without touching a block device.
The collection import is wired up by tests/conftest.py.

The module runs on the managed node, so this file also runs in the Python 3.6
(RHEL 8) tier, see tox.ini. Importing the module there is what catches syntax
that platform-python does not understand.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest
import unittest.mock

import ansible_harness
from ansible.module_utils import basic
from ansible_collections.linuxfabrik.lfops.plugins.modules import lvm_pv as mod

_DEVICE = '/dev/vdb1'


class _FakeLvm:
    """In-memory stand-in for pvs, pvcreate, pvresize and pvremove."""

    def __init__(self):
        self.pv_size = None  # None: the device is not a PV
        self.device_size = 2 * 1024**3
        self.commands = []

    def run_command(self, module, args, check_rc=False, **kwargs):
        self.commands.append(list(args))
        if args[0] == 'pvs':
            if self.pv_size is None:
                return 5, '', f'Failed to find physical volume "{args[-1]}".'
            if '--units' in args:
                return 0, f'  {self.pv_size}\n', ''
            return 0, f'  {args[-1]} lvm2 a-- 1.00g 1.00g\n', ''
        if args[0] in ('pvcreate', 'pvresize'):
            self.pv_size = self.device_size
        elif args[0] == 'pvremove':
            self.pv_size = None
        return 0, '', ''

    def issued(self, command):
        """Return the recorded invocations of `command` (e.g. 'pvcreate')."""
        return [c for c in self.commands if c[0] == command]


class LvmPvTestCase(unittest.TestCase):
    def setUp(self):
        self.lvm = _FakeLvm()
        lvm = self.lvm

        def _run_command(module, args, check_rc=False, **kwargs):
            return lvm.run_command(module, args, check_rc=check_rc, **kwargs)

        self._patchers = [
            ansible_harness.patch_module(),
            unittest.mock.patch.object(
                basic.AnsibleModule, 'run_command', _run_command
            ),
            # the device always exists, so the module never fails on that check
            unittest.mock.patch.object(mod.os.path, 'exists', return_value=True),
            # no sysfs in a unit test, rescan_device is tested separately
            unittest.mock.patch.object(mod, 'rescan_device', return_value=False),
        ]
        for p in self._patchers:
            p.start()

    def tearDown(self):
        for p in reversed(self._patchers):
            p.stop()

    def _run(self, **args):
        args.setdefault('device', _DEVICE)
        ansible_harness.set_module_args(args)
        try:
            mod.main()
        except ansible_harness.AnsibleExitJson as exc:
            return exc.args[0]
        raise AssertionError('module did not call exit_json')


class TestPresent(LvmPvTestCase):
    def test_creates_pv(self):
        result = self._run()
        self.assertTrue(result['changed'])
        self.assertEqual(self.lvm.issued('pvcreate'), [['pvcreate', _DEVICE]])

    def test_force_creates_pv_with_f(self):
        self._run(force=True)
        self.assertEqual(self.lvm.issued('pvcreate'), [['pvcreate', '-f', _DEVICE]])

    def test_existing_pv_is_left_alone(self):
        self.lvm.pv_size = self.lvm.device_size
        result = self._run()
        self.assertFalse(result['changed'])
        self.assertEqual(self.lvm.issued('pvcreate'), [])
        self.assertEqual(self.lvm.issued('pvresize'), [])

    def test_check_mode_does_not_create(self):
        result = self._run(_ansible_check_mode=True)
        self.assertTrue(result['changed'])
        self.assertEqual(self.lvm.issued('pvcreate'), [])

    def test_missing_device_fails(self):
        with unittest.mock.patch.object(mod.os.path, 'exists', return_value=False):
            ansible_harness.set_module_args({'device': _DEVICE})
            with self.assertRaises(ansible_harness.AnsibleFailJson) as ctx:
                mod.main()
        self.assertIn('not found', ctx.exception.args[0]['msg'])
        self.assertEqual(self.lvm.commands, [])


class TestResize(LvmPvTestCase):
    def test_grown_device_resizes_pv(self):
        self.lvm.pv_size = 512 * 1024**2
        result = self._run(resize=True)
        self.assertTrue(result['changed'])
        self.assertEqual(self.lvm.issued('pvresize'), [['pvresize', _DEVICE]])

    def test_unchanged_device_reports_no_change(self):
        # pvresize runs every time, only a different size afterwards is a change
        self.lvm.pv_size = self.lvm.device_size
        result = self._run(resize=True)
        self.assertFalse(result['changed'])
        self.assertEqual(self.lvm.issued('pvresize'), [['pvresize', _DEVICE]])

    def test_check_mode_does_not_resize(self):
        self.lvm.pv_size = 512 * 1024**2
        result = self._run(resize=True, _ansible_check_mode=True)
        self.assertTrue(result['changed'])
        self.assertEqual(self.lvm.issued('pvresize'), [])

    def test_new_pv_is_not_resized(self):
        # pvcreate already uses the whole device
        self._run(resize=True)
        self.assertEqual(self.lvm.issued('pvresize'), [])


class TestAbsent(LvmPvTestCase):
    def test_removes_pv(self):
        self.lvm.pv_size = self.lvm.device_size
        result = self._run(state='absent')
        self.assertTrue(result['changed'])
        self.assertEqual(self.lvm.issued('pvremove'), [['pvremove', '-y', _DEVICE]])

    def test_force_removes_pv_with_ff(self):
        self.lvm.pv_size = self.lvm.device_size
        self._run(state='absent', force=True)
        self.assertEqual(
            self.lvm.issued('pvremove'), [['pvremove', '-y', '-ff', _DEVICE]]
        )

    def test_absent_pv_is_left_alone(self):
        result = self._run(state='absent')
        self.assertFalse(result['changed'])
        self.assertEqual(self.lvm.issued('pvremove'), [])

    def test_check_mode_does_not_remove(self):
        self.lvm.pv_size = self.lvm.device_size
        result = self._run(state='absent', _ansible_check_mode=True)
        self.assertTrue(result['changed'])
        self.assertEqual(self.lvm.issued('pvremove'), [])


class TestRescanDevice(unittest.TestCase):
    """rescan_device derives the sysfs rescan file of the parent disk."""

    def _rescan_path(self, device, partition):
        module = unittest.mock.Mock()
        opened = []

        def _exists(path):
            if path.endswith('/partition'):
                return partition
            return True

        def _open(path, mode='r'):
            opened.append(path)
            return unittest.mock.mock_open()()

        exists_patch = unittest.mock.patch.object(mod.os.path, 'exists', _exists)
        open_patch = unittest.mock.patch('builtins.open', _open)
        with exists_patch, open_patch:
            self.assertTrue(mod.rescan_device(module, device))
        return opened[0]

    def test_scsi_partition(self):
        self.assertEqual(
            self._rescan_path('/dev/sda3', partition=True),
            '/sys/block/sda/device/rescan',
        )

    def test_scsi_whole_disk(self):
        self.assertEqual(
            self._rescan_path('/dev/sdb', partition=False),
            '/sys/block/sdb/device/rescan',
        )

    def test_nvme_partition(self):
        self.assertEqual(
            self._rescan_path('/dev/nvme0n1p2', partition=True),
            '/sys/block/nvme0n1/device/rescan_controller',
        )

    def test_missing_rescan_path_warns(self):
        module = unittest.mock.Mock()
        with unittest.mock.patch.object(mod.os.path, 'exists', return_value=False):
            self.assertFalse(mod.rescan_device(module, '/dev/vdb1'))
        module.warn.assert_called_once()


if __name__ == '__main__':
    unittest.main()
