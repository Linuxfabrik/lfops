#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: uptimerobot_monitor_info
short_description: List UptimeRobot monitors
version_added: '6.0.2'
description:
    - Calls C(getMonitors) on the UptimeRobot v2 API and returns every monitor on the account, paginated transparently.
    - Enum-coded fields are translated to human-readable labels - C(type) becomes C(http)/C(keyw)/C(ping)/C(port)/C(beat), C(status) becomes C(paused)/C(wait)/C(up)/C(seems_down)/C(down), C(http_method)/C(keyword_type)/C(keyword_case_type)/C(http_auth_type) are unmangled, and the C(type) of each entry in nested C(alert_contacts[]) is mapped to its label (C(sms), C(email), C(slack), ...).
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
            - Filter the returned list to the monitor whose C(friendly_name) is an exact match for this value. The result is still a list (length 0 or 1) for shape stability. Applied client-side after I(search) has narrowed the API response.
        type: str
    search:
        description:
            - Server-side, case-insensitive substring filter forwarded to UptimeRobot's C(search) parameter. Useful to keep the response small when the account has thousands of monitors. Combine with I(friendly_name) to narrow further.
        type: str
'''


EXAMPLES = r'''
# 1) Quick ad-hoc list of every monitor on the account. The API key is read
#    from ~/.uptimerobot when not passed.
- name: 'Capture all monitors'
  linuxfabrik.lfops.uptimerobot_monitor_info:
  register: 'ur_monitors'

- ansible.builtin.debug:
    msg: '{{ ur_monitors.monitors | length }} monitors total'

# 2) Filter by friendly_name (exact match). Returns at most one entry.
- name: 'Capture one monitor by friendly_name'
  linuxfabrik.lfops.uptimerobot_monitor_info:
    friendly_name: '001 www.example.com'
  register: 'ur_monitor'

- ansible.builtin.debug:
    msg: 'Status: {{ ur_monitor.monitors[0].status }} ({{ ur_monitor.monitors[0].interval }}s interval)'

# 3) Server-side substring filter — useful for prefixed inventories.
- linuxfabrik.lfops.uptimerobot_monitor_info:
    search: '001 '
  register: 'ur_001'

- ansible.builtin.debug:
    msg: '{{ ur_001.monitors | map(attribute="friendly_name") | list }}'

# 4) Drive a maintenance task: pause every monitor matching a prefix while a
#    deployment is in progress (see uptimerobot_monitor for the pause action).
- linuxfabrik.lfops.uptimerobot_monitor_info:
    search: '001 '
  register: 'ur_to_pause'

- linuxfabrik.lfops.uptimerobot_monitor:
    friendly_name: '{{ item.friendly_name }}'
    status: 'paused'
    state: 'present'
  loop: '{{ ur_to_pause.monitors }}'
  loop_control:
    label: '{{ item.friendly_name }}'

# 5) Reporting — list monitors that are currently down or seem down.
- linuxfabrik.lfops.uptimerobot_monitor_info:
  register: 'ur_all'

- ansible.builtin.debug:
    msg: >-
      Down: {{
        ur_all.monitors
        | selectattr("status", "in", ["down", "seems_down"])
        | map(attribute="friendly_name")
        | list
      }}
'''


RETURN = r'''
monitors:
    description: List of monitor dicts. Empty list when nothing matched.
    type: list
    returned: always
    elements: dict
debug:
    description: Diagnostic information about the API call. Stable enough to assert against, not stable enough to be load-bearing.
    type: dict
    returned: always
    sample:
        operation: 'list'
        count: 17
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.linuxfabrik.lfops.plugins.module_utils import uptimerobot as ur


def main():
    argument_spec = dict(
        api_key=dict(type='str', no_log=True),
        api_key_file=dict(type='str', default='~/.uptimerobot'),
        friendly_name=dict(type='str'),
        search=dict(type='str'),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    api_key = ur.resolve_api_key(module, module.params.get('api_key'), module.params.get('api_key_file'))
    search = module.params.get('search') or None
    friendly_name = module.params.get('friendly_name')

    module.log('uptimerobot_monitor_info: fetching monitors search={0!r}'.format(search))
    success, monitors = ur.get_monitors(module, api_key, search=search)
    if not success:
        module.fail_json(msg='Could not list monitors: {0}'.format(monitors))

    if friendly_name:
        match = ur.find_by_friendly_name(monitors, friendly_name)
        monitors = [match] if match else []

    module.exit_json(changed=False, monitors=monitors, debug={
        'operation': 'list',
        'count': len(monitors),
    })


if __name__ == '__main__':
    main()
