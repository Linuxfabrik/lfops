#!/usr/bin/python

# Copyright (c) 2025, Klention Mali <klention@gmail.com>
# Based on lvol module by Jeroen Hoekx <jeroen.hoekx@dsquare.be>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Local patch: upstream uses `from __future__ import annotations`, which Python 3.6 (the
# platform-python on RHEL 8) rejects with a SyntaxError before the module even runs.
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: lvm_pv
short_description: Manage LVM Physical Volumes
version_added: "6.0.0"
description:
  - Creates, resizes or removes LVM Physical Volumes.
author:
  - Klention Mali (@klention)
options:
  device:
    description:
      - Path to the block device to manage.
    type: path
    required: true
  state:
    description:
      - Control if the physical volume exists.
    type: str
    choices: [present, absent]
    default: present
  force:
    description:
      - Force the operation.
      - When O(state=present) (creating a PV), this uses C(pvcreate -f) to force creation.
      - When O(state=absent) (removing a PV), this uses C(pvremove -ff) to force removal even if part of a volume group.
    type: bool
    default: false
  resize:
    description:
      - Resize PV to device size when O(state=present).
      - Before resizing, a rescan of the underlying disk is triggered for SCSI devices and NVMe controllers so that the
        kernel picks up a changed disk size. Other block devices, such as virtio-blk disks, are not rescanned since
        the kernel detects size changes for them automatically.
    type: bool
    default: false
notes:
  - Requires LVM2 utilities installed on the target system.
  - Device path must exist when creating a PV.
"""

EXAMPLES = r"""
- name: Creating physical volume on /dev/sdb
  linuxfabrik.lfops.lvm_pv:
    device: /dev/sdb

- name: Creating and resizing (if needed) physical volume
  linuxfabrik.lfops.lvm_pv:
    device: /dev/sdb
    resize: true

- name: Removing physical volume that is not part of any volume group
  linuxfabrik.lfops.lvm_pv:
    device: /dev/sdb
    state: absent

- name: Force removing physical volume that is already part of a volume group
  linuxfabrik.lfops.lvm_pv:
    device: /dev/sdb
    force: true
    state: absent
"""

RETURN = r"""
"""


import os

from ansible.module_utils.basic import AnsibleModule


def get_pv_status(module, device):
    """Check if the device is already a PV."""
    cmd = ['pvs', '--noheadings', '--readonly', device]
    return module.run_command(cmd)[0] == 0


def get_pv_size(module, device):
    """Get current PV size in bytes."""
    cmd = ['pvs', '--noheadings', '--nosuffix', '--units', 'b', '-o', 'pv_size', device]
    _rc, out, _err = module.run_command(cmd, check_rc=True)
    return int(out.strip())


def pv_needs_resize(module, device):
    """Tell whether pvresize would change the size of the PV.

    Local patch: upstream runs pvresize on every call. pvresize commits the VG metadata even
    when the size stays the same, which writes a file to /etc/lvm/archive on every run
    (pv_resize_single() in lib/metadata/pv_manip.c, verified with LVM 2.03.36 on Rocky 10).

    A PV in a VG reports pe_count * extent size as pv_size, and pvresize sets pe_count to
    (device size - pe_start) / extent size. A second metadata area at the end of the device
    makes this an overestimate, so pvresize runs as before. An orphan PV has neither extents
    nor an extent size, and reports the device size it was last resized to.
    """
    cmd = [
        'pvs',
        '--noheadings',
        '--nosuffix',
        '--units',
        'b',
        '--separator',
        ';',
        '-o',
        'dev_size,pv_size,pe_start,vg_extent_size,pv_pe_count',
        device,
    ]
    _rc, out, _err = module.run_command(cmd, check_rc=True)
    dev_size, pv_size, pe_start, extent_size, pe_count = (
        int(value) for value in out.strip().split(';')
    )
    if extent_size == 0:
        return dev_size != pv_size
    return (dev_size - pe_start) // extent_size != pe_count


_SYSFS = '/sys'


def rescan_device(module: AnsibleModule, device: str) -> bool:
    """Ask the kernel to re-read the size of the disk backing the device.

    Returns True if a rescan was triggered, False otherwise. Only SCSI devices (``rescan``)
    and NVMe controllers (``rescan_controller``) offer a rescan attribute. Other block devices
    (virtio-blk, Xen, loop, device-mapper, MD, ...) pick up size changes on their own or do
    not support a rescan, so they are silently skipped.

    Taken from upstream commit 6f22759f (community.general#13218), which fixes
    community.general#13212. Drop it with the rest of this file.
    """
    # Resolve symlinks such as /dev/disk/by-id/... or /dev/mapper/... to the kernel device name
    name = os.path.basename(os.path.realpath(device))
    sys_block = os.path.join(_SYSFS, 'class', 'block', name)
    if not os.path.exists(sys_block):
        return False

    # For a partition, the parent disk is the parent directory of its sysfs entry
    # (for example .../block/sda/sda1 or .../block/nvme0n1/nvme0n1p1)
    if os.path.exists(os.path.join(sys_block, 'partition')):
        name = os.path.basename(os.path.dirname(os.path.realpath(sys_block)))

    for attr in ('rescan', 'rescan_controller'):
        rescan_path = os.path.join(_SYSFS, 'block', name, 'device', attr)
        if os.path.exists(rescan_path):
            try:
                with open(rescan_path, 'w') as f:
                    f.write('1')
                return True
            except OSError as e:
                module.warn(f'Failed to rescan device {device}: {e!s}')
                return False
    return False


def main():
    module = AnsibleModule(
        argument_spec=dict(
            device=dict(type='path', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            force=dict(type='bool', default=False),
            resize=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )

    device = module.params['device']
    state = module.params['state']
    force = module.params['force']
    resize = module.params['resize']
    changed = False
    actions = []

    # Validate device existence for present state
    if state == 'present' and not os.path.exists(device):
        module.fail_json(msg=f'Device {device} not found')

    is_pv = get_pv_status(module, device)

    if state == 'present':
        # Create PV if needed
        if not is_pv:
            if module.check_mode:
                changed = True
                actions.append('would be created')
            else:
                cmd = ['pvcreate']
                if force:
                    cmd.append('-f')
                cmd.append(device)
                _rc, _out, _err = module.run_command(cmd, check_rc=True)
                changed = True
                actions.append('created')
            is_pv = True

        # Handle resizing
        elif resize and is_pv:
            if module.check_mode:
                if pv_needs_resize(module, device):
                    changed = True
                    actions.append('would be resized')
            else:
                # Perform device rescan if each time
                if rescan_device(module, device):
                    actions.append('rescanned')
                if pv_needs_resize(module, device):
                    original_size = get_pv_size(module, device)
                    _rc, _out, _err = module.run_command(
                        ['pvresize', device], check_rc=True
                    )
                    new_size = get_pv_size(module, device)
                    if new_size != original_size:
                        changed = True
                        actions.append('resized')

    elif state == 'absent':
        if is_pv:
            if module.check_mode:
                changed = True
                actions.append('would be removed')
            else:
                cmd = ['pvremove', '-y']
                if force:
                    cmd.append('-ff')
                changed = True
                cmd.append(device)
                _rc, _out, _err = module.run_command(cmd, check_rc=True)
                actions.append('removed')

    # Generate final message
    if actions:
        msg = f'PV {device}: {", ".join(actions)}'
    else:
        msg = f'No changes needed for PV {device}'
    module.exit_json(changed=changed, msg=msg)


if __name__ == '__main__':
    main()
