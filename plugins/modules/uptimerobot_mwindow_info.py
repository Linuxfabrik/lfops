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
version_added: '6.0.2'
description:
    - Calls C(getMWindows) on the UptimeRobot v2 API and returns every maintenance window on the account.
    - Enum-coded fields are translated to human-readable labels - C(type) becomes C(once)/C(daily)/C(weekly)/C(monthly), C(status) becomes C(paused)/C(active), and for weekly windows C(value) is decoded from the dash-joined day-IDs (e.g. C(1-3-5)) back into labels (C(mon-wed-fri)). Monthly day-of-month numbers are passed through unchanged.
    - Read-only; the module always reports C(changed=false) and is safe to run in check mode.
author:
    - Linuxfabrik GmbH, Zurich, Switzerland (info (at) linuxfabrik (dot) ch)
options:
    api_key:
        description: UptimeRobot API key. See C(uptimerobot_monitor) for the resolution order.
        type: str
        no_log: true
    api_key_file:
        description: Path to a file whose first line is the UptimeRobot API key. Tilde-expanded.
        type: str
        default: '~/.uptimerobot'
    friendly_name:
        description:
            - Filter the returned list to the maintenance window whose C(friendly_name) is an exact match for this value. The result is still a list (length 0 or 1) for shape stability.
        type: str
'''


EXAMPLES = r'''
# 1) List every maintenance window on the account.
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
    description: List of maintenance window dicts. Empty list when nothing matched.
    type: list
    returned: always
    elements: dict
debug:
    description: Diagnostic information about the API call. Stable enough to assert against, not stable enough to be load-bearing.
    type: dict
    returned: always
    sample:
        operation: 'list'
        count: 4
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.linuxfabrik.lfops.plugins.module_utils import uptimerobot as ur


def main():
    argument_spec = dict(
        api_key=dict(type='str', no_log=True),
        api_key_file=dict(type='str', default='~/.uptimerobot'),
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
