#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: uptimerobot_psp
short_description: Create, update or delete an UptimeRobot Public Status Page
version_added: '6.0.2'
description:
    - Manages a single UptimeRobot Public Status Page (PSP) end-to-end (create, update, pause/resume, delete) against the v2 API.
    - Identification is by I(friendly_name); the value must be unique on the account. Re-running a task with the same I(friendly_name) updates the existing PSP in place and only reports C(changed=true) when one of the diffable fields actually differs.
    - I(monitors) is replaced on every run. The list is diffed by sorted monitor IDs, so re-ordering items in the inventory does not produce a spurious change. Omitting I(monitors) (or passing an empty list) leaves the C(monitors) field off the create / edit payload, in which case UptimeRobot applies its own default behaviour for that page.
    - I(password) cannot be diffed because UptimeRobot never returns it. When supplied, the module always sends it on edit and reports C(changed=true). To keep an existing password as is, simply omit I(password) from the task.
    - I(status) is only honoured on edit; UptimeRobot rejects this field on create.
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
        description: Display name of the status page. Used as the idempotency key, so it must be unique on the account.
        type: str
        required: true
    state:
        description: C(present) creates the PSP when missing, or updates it in place when present. C(absent) deletes it; when the PSP does not exist, the module exits with C(changed=false).
        type: str
        choices: ['absent', 'present']
        default: 'present'
    monitors:
        description:
            - Monitors to display on the status page. Each item references an existing monitor.
            - When an item has I(id), it is used directly. Otherwise I(friendly_name) is resolved against C(getMonitors); an unknown name fails the play.
        type: list
        elements: dict
        suboptions:
            friendly_name:
                description: Friendly name of an existing monitor. Required if I(id) is not given.
                type: str
            id:
                description: Numeric monitor ID. Takes precedence over I(friendly_name) when both are set.
                type: int
    custom_domain:
        description: Custom domain to host the status page under (e.g. C(status.example.com)). Mutually exclusive with I(custom_url).
        type: str
    custom_url:
        description:
            - Backward-compatible alias for I(custom_domain) - this is also the field name UptimeRobot uses on the read side. Mutually exclusive with I(custom_domain).
        type: str
    password:
        description: Password to protect the status page. UptimeRobot never returns the stored value, so re-running the task with I(password) set always reports C(changed=true). Omit to keep the previous password.
        type: str
        no_log: true
    sort:
        description: Sort order of the monitors on the page.
        type: str
        choices: ['a-z', 'down-up-paused', 'up-down-paused', 'z-a']
    hide_url_links:
        description: When C(true), the rendered page does not show the underlying monitor URLs.
        type: bool
    status:
        description: C(active) un-pauses the page, C(paused) pauses it. Only honoured on edit; UptimeRobot rejects this field on create.
        type: str
        choices: ['active', 'paused']
'''


EXAMPLES = r'''
# 1) Create-or-update a public status page. Monitors are referenced by their
#    friendly_name; the module resolves them to numeric IDs at runtime.
- name: 'Public status page for example.com'
  linuxfabrik.lfops.uptimerobot_psp:
    friendly_name: 'Status - example.com'
    custom_url: 'status.example.com'
    monitors:
      - friendly_name: '001 www.example.com/index.php/login'
      - friendly_name: '001 office.example.com/hosting/discovery'
    sort: 'a-z'
    status: 'active'
    state: 'present'

# 2) Password-protected page (no `monitors` => the API publishes ALL monitors
#    of the account).
- linuxfabrik.lfops.uptimerobot_psp:
    friendly_name: 'Internal status'
    password: '{{ vault_psp_password }}'
    sort: 'down-up-paused'
    status: 'active'
    state: 'present'

# 3) Pause a status page without changing its content.
- linuxfabrik.lfops.uptimerobot_psp:
    friendly_name: 'Status - example.com'
    status: 'paused'
    state: 'present'

# 4) Delete a stale status page.
- linuxfabrik.lfops.uptimerobot_psp:
    friendly_name: 'old-status-page'
    state: 'absent'
'''


RETURN = r'''
psp:
    description:
        - On create or update, the PSP as returned by UptimeRobot's C(newPSP) / C(editPSP). On delete, the last known state of the PSP.
        - Empty dict when there was nothing to delete.
        - In check mode, a synthetic preview reflecting what the run would have written.
    type: dict
    returned: always
debug:
    description: Diagnostic information about the operation (one of C(create), C(update), C(delete), C(noop), each optionally suffixed with C( (check_mode))). Stable enough to assert against, not stable enough to be load-bearing.
    type: dict
    returned: always
    sample:
        operation: 'update'
        friendly_name: 'Status - example.com'
        psp_id: 4321
        diff_fields: ['monitors']
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.linuxfabrik.lfops.plugins.module_utils import uptimerobot as ur


def _resolve_monitor_ids(module, api_key, items):
    if not items:
        return None
    needs_resolution = [i.get('friendly_name') for i in items if not i.get('id')]
    by_name = {}
    if needs_resolution:
        success, monitors = ur.get_monitors(module, api_key)
        if not success:
            module.fail_json(msg='Could not list monitors: {0}'.format(monitors))
        by_name = {m.get('friendly_name'): m for m in monitors}
    ids = []
    for item in items:
        mid = item.get('id')
        if mid is None:
            name = item['friendly_name']
            if name not in by_name:
                module.fail_json(msg='Monitor {0!r} not found on UptimeRobot'.format(name))
            mid = int(by_name[name]['id'])
        ids.append(int(mid))
    return ur.monitors_wire(ids)


def main():
    argument_spec = dict(
        api_key=dict(type='str', no_log=True),
        api_key_file=dict(type='str', default='~/.uptimerobot'),
        friendly_name=dict(type='str', required=True),
        state=dict(type='str', choices=['absent', 'present'], default='present'),
        monitors=dict(type='list', elements='dict'),
        custom_domain=dict(type='str'),
        custom_url=dict(type='str'),
        password=dict(type='str', no_log=True),
        sort=dict(type='str', choices=['a-z', 'down-up-paused', 'up-down-paused', 'z-a']),
        hide_url_links=dict(type='bool'),
        status=dict(type='str', choices=['active', 'paused']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=[['custom_domain', 'custom_url']],
    )

    api_key = ur.resolve_api_key(module, module.params.get('api_key'), module.params.get('api_key_file'))
    friendly_name = module.params['friendly_name']
    state = module.params['state']

    module.log('uptimerobot_psp: looking up friendly_name={0!r}'.format(friendly_name))
    success, psps = ur.get_psps(module, api_key)
    if not success:
        module.fail_json(msg='Could not list PSPs: {0}'.format(psps))
    current = ur.find_by_friendly_name(psps, friendly_name)
    module.log('uptimerobot_psp: existing={0} (out of {1} PSPs on the account)'.format(
        bool(current), len(psps),
    ))

    if state == 'absent':
        if current is None:
            module.exit_json(changed=False, psp={}, debug={
                'operation': 'noop',
                'reason': 'PSP not present',
                'friendly_name': friendly_name,
            })
        delete_before = {
            'friendly_name': current.get('friendly_name'),
            'id': current.get('id'),
            'custom_domain': current.get('custom_domain'),
        }
        if module.check_mode:
            module.exit_json(changed=True, psp=current,
                diff={'before': delete_before, 'after': {}},
                debug={
                    'operation': 'delete (check_mode)',
                    'friendly_name': friendly_name,
                    'psp_id': current['id'],
                })
        module.log('uptimerobot_psp: deleting id={0}'.format(current['id']))
        success, result = ur.delete_psp(module, api_key, current['id'])
        if not success:
            module.fail_json(msg='Could not delete PSP {0!r}: {1}'.format(friendly_name, result))
        module.exit_json(changed=True, psp=current,
            diff={'before': delete_before, 'after': {}},
            debug={
                'operation': 'delete',
                'friendly_name': friendly_name,
                'psp_id': current['id'],
            })

    # Desired payload.
    custom_domain = module.params.get('custom_domain') or module.params.get('custom_url')
    monitors_wire = _resolve_monitor_ids(module, api_key, module.params.get('monitors'))

    desired = {
        'monitors': monitors_wire,
        'custom_domain': custom_domain,
        'password': module.params.get('password'),
        'sort': module.params.get('sort'),
        'hide_url_links': module.params.get('hide_url_links'),
        'status': module.params.get('status'),
    }
    desired = {k: v for k, v in desired.items() if v is not None and v != ''}

    if current is None:
        body = dict(desired)
        body['friendly_name'] = friendly_name
        body.pop('status', None)  # not allowed on create
        create_diff = {'before': {}, 'after': dict(body)}
        if module.check_mode:
            module.exit_json(changed=True, psp=body,
                diff=create_diff,
                debug={
                    'operation': 'create (check_mode)',
                    'friendly_name': friendly_name,
                    'sent_keys': sorted(body.keys()),
                })
        module.log('uptimerobot_psp: creating friendly_name={0!r} sent_keys={1}'.format(
            friendly_name, sorted(body.keys()),
        ))
        success, result = ur.new_psp(module, api_key, body)
        if not success:
            module.fail_json(msg='Could not create PSP {0!r}: {1}'.format(friendly_name, result))
        module.exit_json(changed=True, psp=result,
            diff=create_diff,
            debug={
                'operation': 'create',
                'friendly_name': friendly_name,
                'sent_keys': sorted(body.keys()),
            })

    # Update. `get_psps` already translated sort/status to labels. The API
    # returns monitors as a list of IDs and password is never returned, so
    # those need their own normalisation.
    current_compare = {
        'monitors': ur.monitors_wire(sorted(int(m) for m in (current.get('monitors') or []))),
        'custom_domain': current.get('custom_domain'),
        'sort': current.get('sort'),
        'hide_url_links': current.get('hide_url_links'),
        'status': current.get('status'),
    }
    desired_compare = dict(desired)
    if 'monitors' in desired_compare:
        ids = sorted(int(x) for x in desired_compare['monitors'].split(',') if x)
        desired_compare['monitors'] = ur.monitors_wire(ids)

    diff_fields = ['monitors', 'custom_domain', 'sort', 'hide_url_links', 'status']
    field_diff = ur.diff_for_update(current_compare, desired_compare, diff_fields)
    if not field_diff and 'password' not in desired:
        module.log('uptimerobot_psp: id={0} no diff -> changed=false'.format(current['id']))
        module.exit_json(changed=False, psp=current, debug={
            'operation': 'noop',
            'reason': 'no diff',
            'friendly_name': friendly_name,
            'psp_id': current['id'],
        })

    module.log('uptimerobot_psp: id={0} diff_fields={1}{2}'.format(
        current['id'], sorted(field_diff.keys()),
        ' (+password)' if 'password' in desired else '',
    ))

    update_diff = {
        'before': {k: current_compare.get(k) for k in field_diff},
        'after': dict(field_diff),
    }
    if 'password' in desired:
        # Bandit B105 triggers on any string assigned to a `password` key;
        # this is just the diff display token, never used as an auth secret.
        update_diff['after']['password'] = '<masked>'  # nosec B105

    if module.check_mode:
        preview = dict(current)
        preview.update(field_diff)
        module.exit_json(changed=True, psp=preview,
            diff=update_diff,
            debug={
                'operation': 'update (check_mode)',
                'friendly_name': friendly_name,
                'psp_id': current['id'],
                'diff_fields': sorted(field_diff.keys()),
            })

    body = dict(desired)
    body['id'] = current['id']
    success, result = ur.edit_psp(module, api_key, body)
    if not success:
        module.fail_json(msg='Could not edit PSP {0!r}: {1}'.format(friendly_name, result))
    module.exit_json(changed=True, psp=result,
        diff=update_diff,
        debug={
            'operation': 'update',
            'friendly_name': friendly_name,
            'psp_id': current['id'],
            'diff_fields': sorted(field_diff.keys()),
        })


if __name__ == '__main__':
    main()
