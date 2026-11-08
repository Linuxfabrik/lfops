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

    # the values of a 2 GiB disk in a VG with 4 MiB extents, as LVM 2.03.36 reports them
    _PE_START = 1024**2
    _EXTENT_SIZE = 4 * 1024**2

    def __init__(self):
        self.pv_size = None  # None: the device is not a PV
        self.device_size = 2 * 1024**3
        self.in_vg = True
        self.commands = []

    def _pvs_resize_fields(self):
        """dev_size;pv_size;pe_start;vg_extent_size;pv_pe_count"""
        if not self.in_vg:
            return f'{self.device_size};{self.pv_size};{self._PE_START};0;0'
        pe_count = self.pv_size // self._EXTENT_SIZE
        return (
            f'{self.device_size};{pe_count * self._EXTENT_SIZE};{self._PE_START};'
            f'{self._EXTENT_SIZE};{pe_count}'
        )

    def run_command(self, module, args, check_rc=False, **kwargs):
        self.commands.append(list(args))
        if args[0] == 'pvs':
            if self.pv_size is None:
                return 5, '', f'Failed to find physical volume "{args[-1]}".'
            if '--separator' in args:
                return 0, f'  {self._pvs_resize_fields()}\n', ''
            if '--units' in args:
                return 0, f'  {self.pv_size}\n', ''
            return 0, f'  {args[-1]} lvm2 a-- 1.00g 1.00g\n', ''
        if args[0] == 'pvcreate':
            self.pv_size = self.device_size
        elif args[0] == 'pvresize':
            # pvresize sets the PV to the extents that fit behind pe_start
            self.pv_size = (
                self.device_size
                if not self.in_vg
                else (self.device_size - self._PE_START)
                // self._EXTENT_SIZE
                * self._EXTENT_SIZE
            )
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

    def test_unchanged_device_is_not_resized(self):
        # pvresize writes a file to /etc/lvm/archive even when the size stays the same, so it
        # must not run for a PV that already fills its device
        self.lvm.pv_size = self.lvm.device_size - self.lvm._PE_START
        result = self._run(resize=True)
        self.assertFalse(result['changed'])
        self.assertEqual(self.lvm.issued('pvresize'), [])

    def test_grown_orphan_pv_is_resized(self):
        self.lvm.in_vg = False
        self.lvm.pv_size = 512 * 1024**2
        result = self._run(resize=True)
        self.assertTrue(result['changed'])
        self.assertEqual(self.lvm.issued('pvresize'), [['pvresize', _DEVICE]])

    def test_unchanged_orphan_pv_is_not_resized(self):
        self.lvm.in_vg = False
        self.lvm.pv_size = self.lvm.device_size
        result = self._run(resize=True)
        self.assertFalse(result['changed'])
        self.assertEqual(self.lvm.issued('pvresize'), [])

    def test_check_mode_does_not_resize(self):
        self.lvm.pv_size = 512 * 1024**2
        result = self._run(resize=True, _ansible_check_mode=True)
        self.assertTrue(result['changed'])
        self.assertEqual(self.lvm.issued('pvresize'), [])

    def test_check_mode_reports_no_change_for_unchanged_device(self):
        self.lvm.pv_size = self.lvm.device_size - self.lvm._PE_START
        result = self._run(resize=True, _ansible_check_mode=True)
        self.assertFalse(result['changed'])

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

    def _rescan_path(self, device, partition, resolves_to=None):
        module = unittest.mock.Mock()
        opened = []
        handle = unittest.mock.mock_open()

        def _exists(path):
            if path.endswith('/partition'):
                return partition
            return True

        def _open(path, mode='r'):
            opened.append(path)
            return handle(path, mode)

        # no real /dev in a unit test: resolve only the symlink the test names
        realpath_patch = unittest.mock.patch.object(
            mod.os.path, 'realpath', lambda path: resolves_to or path
        )
        exists_patch = unittest.mock.patch.object(mod.os.path, 'exists', _exists)
        open_patch = unittest.mock.patch('builtins.open', _open)
        with realpath_patch, exists_patch, open_patch:
            self.assertTrue(mod.rescan_device(module, device))
        handle().write.assert_called_once_with('1')
        module.warn.assert_not_called()
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

    def test_symlink_is_resolved(self):
        self.assertEqual(
            self._rescan_path(
                '/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi0-part1',
                partition=True,
                resolves_to='/dev/sda1',
            ),
            '/sys/block/sda/device/rescan',
        )

    def test_virtio_blk_without_rescan_is_skipped_silently(self):
        # virtio_blk has no rescan attribute and picks up a new size on its own
        module = unittest.mock.Mock()

        def _exists(path):
            return path == '/sys/class/block/vdb1/partition'

        exists_patch = unittest.mock.patch.object(mod.os.path, 'exists', _exists)
        open_patch = unittest.mock.patch('builtins.open', unittest.mock.mock_open())
        with exists_patch, open_patch as opened:
            self.assertFalse(mod.rescan_device(module, '/dev/vdb1'))
        opened.assert_not_called()
        module.warn.assert_not_called()

    def test_failed_write_warns(self):
        module = unittest.mock.Mock()
        exists_patch = unittest.mock.patch.object(
            mod.os.path, 'exists', return_value=True
        )
        open_patch = unittest.mock.patch(
            'builtins.open', side_effect=OSError(13, 'Permission denied')
        )
        with exists_patch, open_patch:
            self.assertFalse(mod.rescan_device(module, '/dev/sda'))
        module.warn.assert_called_once()
        self.assertIn('Failed to rescan device /dev/sda', module.warn.call_args[0][0])


if __name__ == '__main__':
    unittest.main()
