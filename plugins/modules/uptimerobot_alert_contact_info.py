#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: uptimerobot_alert_contact_info
short_description: List UptimeRobot alert contacts
version_added: '6.0.2'
description:
    - Calls C(getAlertContacts) on the UptimeRobot v2 API and returns every alert contact on the account.
    - Enum-coded fields are translated to human-readable labels - C(status) becomes C(not activated)/C(paused)/C(active), C(type) becomes C(sms)/C(email)/C(slack)/etc.
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
            - Filter the returned list to the contact whose C(friendly_name) is an exact match for this value. The result is still a list (length 0 or 1) for shape stability.
        type: str
'''


EXAMPLES = r'''
# 1) List every alert contact on the account.
- name: 'Capture all alert contacts'
  linuxfabrik.lfops.uptimerobot_alert_contact_info:
  register: 'ur_alert_contacts'

- ansible.builtin.debug:
    msg: '{{ ur_alert_contacts.alert_contacts | length }} alert contacts on the account'

# 2) Look up a single contact by friendly_name.
- linuxfabrik.lfops.uptimerobot_alert_contact_info:
    friendly_name: 'monitoring@example.com'
  register: 'ur_contact'

- ansible.builtin.debug:
    msg: 'Contact id={{ ur_contact.alert_contacts[0].id }} status={{ ur_contact.alert_contacts[0].status }}'

# 3) Audit: list all contacts that never accepted the opt-in invitation
#    (`status == "not activated"`) — typically safe to delete.
- linuxfabrik.lfops.uptimerobot_alert_contact_info:
  register: 'ur_all'

- ansible.builtin.debug:
    msg: >-
      Stale contacts: {{
        ur_all.alert_contacts
        | selectattr("status", "equalto", "not activated")
        | map(attribute="friendly_name")
        | list
      }}
'''


RETURN = r'''
alert_contacts:
    description: List of alert contact dicts. Empty list when nothing matched.
    type: list
    returned: always
    elements: dict
debug:
    description: Diagnostic information about the API call. Stable enough to assert against, not stable enough to be load-bearing.
    type: dict
    returned: always
    sample:
        operation: 'list'
        count: 3
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

    module.log('uptimerobot_alert_contact_info: fetching alert contacts')
    success, contacts = ur.get_alert_contacts(module, api_key)
    if not success:
        module.fail_json(msg=f'Could not list alert contacts: {contacts}')

    if friendly_name:
        match = ur.find_by_friendly_name(contacts, friendly_name)
        contacts = [match] if match else []

    module.exit_json(changed=False, alert_contacts=contacts, debug={
        'operation': 'list',
        'count': len(contacts),
    })


if __name__ == '__main__':
    main()
