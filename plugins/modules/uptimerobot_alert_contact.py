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
module: uptimerobot_alert_contact
short_description: Delete an UptimeRobot alert contact
version_added: '6.0.2'
description:
    - Deletes a single alert contact on UptimeRobot. Creation and editing are deliberately not implemented because UptimeRobot's API v2 does not expose them - new contacts have to be added through the web UI (which sends an opt-in mail), and existing ones have to be edited there too. Calling this module with I(state=present) is rejected up front with an explanatory error.
    - Identification is by either I(friendly_name) or I(id); exactly one must be given. When I(id) is set, the lookup goes straight to the numeric ID. When only I(friendly_name) is given, the module lists all alert contacts and matches the C(friendly_name) exactly.
    - When the contact does not exist (no match by either ID or friendly name, or the listing call failed), the module exits with C(changed=false) instead of failing - so a sweep over a static list of contacts to remove stays idempotent.
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
        description: Friendly name of the alert contact to delete. Exact match. Required if I(id) is not given.
        type: str
    id:
        description: Numeric ID of the alert contact. Required if I(friendly_name) is not given. Takes precedence when both are set.
        type: int
    state:
        description:
            - Only C(absent) is supported. C(present) is rejected because UptimeRobot's v2 API does not expose contact creation or editing.
        type: str
        choices: ['absent', 'present']
        default: 'absent'
'''


EXAMPLES = r'''
# UptimeRobot's v2 API does not allow CREATING or EDITING alert contacts via
# the API — they must be added in the web UI (which sends an opt-in mail).
# This module is therefore delete-only, useful for sweeping contacts that no
# longer correspond to an active recipient.

# 1) Delete by friendly_name (recommended — survives ID re-numbering).
- name: 'Sweep a stale alert contact by friendly_name'
  linuxfabrik.lfops.uptimerobot_alert_contact:
    friendly_name: 'old-pager@example.com'
    state: 'absent'

# 2) Delete by ID (when you already have it from uptimerobot_alert_contact_info).
- linuxfabrik.lfops.uptimerobot_alert_contact:
    id: 7068316
    state: 'absent'

# 3) Drive a sweep from inventory: list everything via the info module, filter
#    for the ones you want gone, then delete them.
- linuxfabrik.lfops.uptimerobot_alert_contact_info:
  register: 'ur_contacts'

- linuxfabrik.lfops.uptimerobot_alert_contact:
    friendly_name: '{{ item.friendly_name }}'
    state: 'absent'
  loop: '{{ ur_contacts.alert_contacts | selectattr("status", "equalto", "not activated") | list }}'
  loop_control:
    label: '{{ item.friendly_name }}'
'''


RETURN = r'''
alert_contact:
    description: The alert contact that was deleted (or that would have been deleted, in check mode), as returned by C(getAlertContacts). Empty dict when there was nothing to delete.
    type: dict
    returned: always
debug:
    description: Diagnostic information about the operation (one of C(delete), C(delete (check_mode)) or C(noop)). Stable enough to assert against, not stable enough to be load-bearing.
    type: dict
    returned: always
    sample:
        operation: 'delete'
        contact_id: 7068316
        friendly_name: 'monitoring@example.com'
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.linuxfabrik.lfops.plugins.module_utils import uptimerobot as ur


def main():
    argument_spec = dict(
        api_key=dict(type='str', no_log=True),
        api_key_file=dict(type='str', default='~/.uptimerobot'),
        friendly_name=dict(type='str'),
        id=dict(type='int'),
        state=dict(type='str', choices=['absent', 'present'], default='absent'),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[['friendly_name', 'id']],
    )

    if module.params['state'] == 'present':
        module.fail_json(msg=(
            "uptimerobot_alert_contact only supports state='absent'. "
            "UptimeRobot API v2 does not expose creating or editing alert "
            "contacts; use the web UI for that."
        ))

    api_key = ur.resolve_api_key(module, module.params.get('api_key'), module.params.get('api_key_file'))
    contact_id = module.params.get('id')
    friendly_name = module.params.get('friendly_name')

    module.log(f'uptimerobot_alert_contact: looking up id={contact_id} friendly_name={friendly_name!r}')

    target = None
    if contact_id is None:
        success, contacts = ur.get_alert_contacts(module, api_key)
        if not success:
            module.fail_json(msg=f'Could not list alert contacts: {contacts}')
        target = ur.find_by_friendly_name(contacts, friendly_name)
        if target is None:
            module.exit_json(changed=False, alert_contact={}, debug={
                'operation': 'noop',
                'reason': 'alert contact not present',
                'friendly_name': friendly_name,
            })
        contact_id = int(target['id'])
    else:
        # We can still try to look up the friendly_name for the report, but it
        # is not strictly required.
        success, contacts = ur.get_alert_contacts(module, api_key)
        if success:
            for c in contacts:
                if int(c.get('id', -1)) == contact_id:
                    target = c
                    break
        if target is None:
            # Either the listing failed or the contact does not exist; treat
            # both as "nothing to do".
            module.exit_json(changed=False, alert_contact={}, debug={
                'operation': 'noop',
                'reason': 'alert contact not present (or could not list)',
                'contact_id': contact_id,
            })

    if module.check_mode:
        module.exit_json(changed=True, alert_contact=target, debug={
            'operation': 'delete (check_mode)',
            'contact_id': contact_id,
            'friendly_name': target.get('friendly_name'),
        })

    module.log(
        f"uptimerobot_alert_contact: deleting id={contact_id} "
        f"friendly_name={target.get('friendly_name')!r}"
    )
    success, result = ur.delete_alert_contact(module, api_key, contact_id)
    if not success:
        module.fail_json(msg=f'Could not delete alert contact {target!r}: {result}')
    module.exit_json(changed=True, alert_contact=target, debug={
        'operation': 'delete',
        'contact_id': contact_id,
        'friendly_name': target.get('friendly_name'),
    })


if __name__ == '__main__':
    main()
