#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: uptimerobot_account_info
short_description: Read UptimeRobot account details
version_added: '6.1.0'
description:
    - Returns account-level facts (email, monitor limit, monitor counters, ...) from UptimeRobot.
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
'''


EXAMPLES = r'''
# 1) Read account quota and current usage. The API key comes from
#    ~/.uptimerobot when no parameter is given.
- name: 'Capture UptimeRobot account info'
  linuxfabrik.lfops.uptimerobot_account_info:
  register: 'ur_account'

- ansible.builtin.debug:
    msg: >-
      {{ ur_account.account.up_monitors }}/{{ ur_account.account.monitor_limit }}
      monitors used; subscription expires
      {{ ur_account.account.subscription_expiry_date }}

# 2) Same call but with an explicit key file (any reachable path is fine).
- linuxfabrik.lfops.uptimerobot_account_info:
    api_key_file: '/etc/ansible/secrets/uptimerobot.key'
  register: 'ur_account'

# 3) Fail the play early if the account is over 90% of its monitor quota.
- linuxfabrik.lfops.uptimerobot_account_info:
  register: 'ur_account'

- ansible.builtin.assert:
    that: 'ur_account.account.up_monitors / ur_account.account.monitor_limit < 0.9'
    fail_msg: 'UptimeRobot quota is nearly exhausted; bump the plan or delete stale monitors.'
'''


RETURN = r'''
account:
    description: Account details as returned by UptimeRobot.
    type: dict
    returned: always
    sample:
        email: 'user@example.com'
        monitor_limit: 50
        monitor_interval: 60
        up_monitors: 10
        down_monitors: 0
        paused_monitors: 0
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.linuxfabrik.lfops.plugins.module_utils import uptimerobot as ur


def main():
    argument_spec = dict(
        api_key=dict(type='str', no_log=True),
        api_key_file=dict(type='str'),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    api_key = ur.resolve_api_key(module, module.params.get('api_key'), module.params.get('api_key_file'))
    module.log('uptimerobot_account_info: fetching account details')
    success, account = ur.get_account_details(module, api_key)
    if not success:
        module.fail_json(msg='Could not fetch UptimeRobot account details: {0}'.format(account))
    module.log('uptimerobot_account_info: monitor_limit={0} up={1} down={2} paused={3}'.format(
        account.get('monitor_limit'), account.get('up_monitors'),
        account.get('down_monitors'), account.get('paused_monitors'),
    ))
    module.exit_json(changed=False, account=account, debug={
        'operation': 'read',
        'fields': sorted(account.keys()) if isinstance(account, dict) else None,
    })


if __name__ == '__main__':
    main()
