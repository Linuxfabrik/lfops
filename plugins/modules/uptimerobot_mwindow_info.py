#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: uptimerobot_mwindow_info
short_description: List UptimeRobot maintenance windows
version_added: '6.1.0'
description:
    - Returns the full list of maintenance windows on the UptimeRobot account,
      with enum-style fields translated to human-readable labels (C(type),
      C(value), C(status)).
    - Equivalent of C(utr get mwindows).
    - Read-only. Reports C(changed=false).
author:
    - Linuxfabrik GmbH, Zurich, Switzerland (info (at) linuxfabrik (dot) ch)
options:
    api_key:
        description: UptimeRobot API key. See C(uptimerobot_monitor) for the resolution order.
        type: str
        no_log: true
    api_key_file:
        description: Path to a file containing the API key. Default C(~/.uptimerobot).
        type: str
    friendly_name:
        description:
            - If set, only the maintenance window with this exact friendly
              name is returned (or none, if no match).
        type: str
'''


EXAMPLES = r'''
# 1) Equivalent to `utr get mwindows`.
- name: 'Capture all maintenance windows'
  linuxfabrik.lfops.uptimerobot_mwindow_info:
  register: 'ur_mwindows'

- ansible.builtin.debug:
    msg: '{{ ur_mwindows.mwindows | length }} maintenance windows defined'

# 2) Look up a single window by its friendly_name (auto-synthesised
#    `<type> [<value>] <start_time>-<end_time>` form is fine).
- linuxfabrik.lfops.uptimerobot_mwindow_info:
    friendly_name: 'weekly mon 03:30-05:30'
  register: 'ur_window'

- ansible.builtin.debug:
    msg: 'Window status: {{ ur_window.mwindows[0].status }}'

# 3) Inventory check: list all PAUSED windows (e.g. before kicking off a
#    deployment that needs them re-activated).
- linuxfabrik.lfops.uptimerobot_mwindow_info:
  register: 'ur_all'

- ansible.builtin.debug:
    msg: >-
      Paused windows: {{
        ur_all.mwindows
        | selectattr("status", "equalto", "paused")
        | map(attribute="friendly_name")
        | list
      }}
'''


RETURN = r'''
mwindows:
    description: List of maintenance window dicts (empty list if none matched).
    type: list
    returned: always
    elements: dict
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.linuxfabrik.lfops.plugins.module_utils import uptimerobot as ur


def main():
    argument_spec = dict(
        api_key=dict(type='str', no_log=True),
        api_key_file=dict(type='str'),
        friendly_name=dict(type='str'),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    api_key = ur.resolve_api_key(module, module.params.get('api_key'), module.params.get('api_key_file'))
    friendly_name = module.params.get('friendly_name')

    module.log('uptimerobot_mwindow_info: fetching maintenance windows')
    success, mwindows = ur.get_mwindows(module, api_key)
    if not success:
        module.fail_json(msg='Could not list maintenance windows: {0}'.format(mwindows))

    if friendly_name:
        match = ur.find_by_friendly_name(mwindows, friendly_name)
        mwindows = [match] if match else []

    module.exit_json(changed=False, mwindows=mwindows, debug={
        'operation': 'list',
        'count': len(mwindows),
    })


if __name__ == '__main__':
    main()
