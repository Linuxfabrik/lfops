#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: uptimerobot_alert_contact_info
short_description: List UptimeRobot alert contacts
version_added: '6.0.2'
description:
    - Returns the full list of alert contacts on the UptimeRobot account,
      with enum-style fields translated to human-readable labels (C(status),
      C(type)).
    - Read-only. Reports C(changed=false).
author:
    - Linuxfabrik GmbH, Zurich, Switzerland (info (at) linuxfabrik (dot) ch)
options:
    api_key:
        description: UptimeRobot API key. See C(uptimerobot_monitor) for the resolution order.
        type: str
        no_log: true
    api_key_file:
        description: Path to a file containing the API key.
        type: str
        default: '~/.uptimerobot'
    friendly_name:
        description:
            - If set, only the alert contact with this exact friendly name is
              returned (or none, if no match).
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
    description: List of alert contact dicts (empty list if none matched).
    type: list
    returned: always
    elements: dict
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
        module.fail_json(msg='Could not list alert contacts: {0}'.format(contacts))

    if friendly_name:
        match = ur.find_by_friendly_name(contacts, friendly_name)
        contacts = [match] if match else []

    module.exit_json(changed=False, alert_contacts=contacts, debug={
        'operation': 'list',
        'count': len(contacts),
    })


if __name__ == '__main__':
    main()
