#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: uptimerobot_mwindow
short_description: Manage UptimeRobot maintenance windows
version_added: '6.1.0'
description:
    - Create, update or delete a maintenance window on UptimeRobot.
    - Identification is by C(friendly_name). The window is auto-named
      C("<type> [<value>] <start_time>-<end_time>") when no C(friendly_name)
      is given (e.g. C("weekly mon 03:30-05:30")).
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
            - Display name of the window. If omitted, it is synthesised from
              C(type), C(value), C(start_time) and C(end_time).
        type: str
    state:
        description: C(present) creates or updates, C(absent) deletes.
        type: str
        choices: ['absent', 'present']
        default: 'present'
    type:
        description: Recurrence type.
        type: str
        choices: ['daily', 'monthly', 'once', 'weekly']
    value:
        description:
            - For C(weekly): day of week (C(mon)..C(sun)).
            - For C(monthly): day of the month (C(1)..C(31)).
            - For C(once): unused.
        type: str
    start_time:
        description:
            - For C(once): RFC3339 timestamp.
            - For C(daily) / C(weekly) / C(monthly): C(HH:MM).
        type: str
    end_time:
        description:
            - C(HH:MM). Used together with C(start_time) to compute C(duration).
              You can give either C(end_time) or C(duration), not both.
        type: str
    duration:
        description: Duration of the window in minutes.
        type: int
    status:
        description: C(active) or C(paused). Only honoured on edit.
        type: str
        choices: ['active', 'paused']
'''


EXAMPLES = r'''
# 1) Create-or-update a weekly window. friendly_name is auto-synthesised as
#    "weekly mon 03:30-05:30" so re-runs are idempotent without naming it.
- name: 'Weekly Monday-night maintenance window'
  linuxfabrik.lfops.uptimerobot_mwindow:
    type: 'weekly'
    value: 'mon'
    start_time: '03:30'
    end_time: '05:30'
    state: 'present'

# 2) Daily window (no `value` for type=daily).
- linuxfabrik.lfops.uptimerobot_mwindow:
    type: 'daily'
    start_time: '02:00'
    end_time: '02:30'
    state: 'present'

# 3) Override the auto-name and pass a literal duration in minutes.
- linuxfabrik.lfops.uptimerobot_mwindow:
    friendly_name: 'cert-renewal'
    type: 'weekly'
    value: 'sun'
    start_time: '04:00'
    duration: 120
    state: 'present'

# 4) Pause an existing window without changing schedule.
- linuxfabrik.lfops.uptimerobot_mwindow:
    friendly_name: 'weekly mon 03:30-05:30'
    status: 'paused'
    state: 'present'

# 5) Delete a stale window by friendly_name.
- linuxfabrik.lfops.uptimerobot_mwindow:
    friendly_name: 'old-window'
    state: 'absent'
'''


RETURN = r'''
mwindow:
    description: The maintenance window object as returned by UptimeRobot. Empty dict if just deleted.
    type: dict
    returned: always
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.linuxfabrik.lfops.plugins.module_utils import uptimerobot as ur


def _hhmm_to_minutes(hhmm):
    h, m = hhmm.split(':')
    return int(h) * 60 + int(m)


def _compute_duration(start_time, end_time):
    """For daily/weekly/monthly windows: derive duration in minutes from
    start_time / end_time (both 'HH:MM'). Wraps over midnight if end < start.
    """
    start = _hhmm_to_minutes(start_time)
    end = _hhmm_to_minutes(end_time)
    duration = end - start
    if duration <= 0:
        duration += 24 * 60
    return duration


def _synthesise_name(params):
    parts = [params['type']]
    if params.get('value'):
        parts.append(str(params['value']))
    parts.append('{0}-{1}'.format(params['start_time'], params['end_time']))
    return ' '.join(parts)


def main():
    argument_spec = dict(
        api_key=dict(type='str', no_log=True),
        api_key_file=dict(type='str'),
        friendly_name=dict(type='str'),
        state=dict(type='str', choices=['absent', 'present'], default='present'),
        type=dict(type='str', choices=['daily', 'monthly', 'once', 'weekly']),
        value=dict(type='str'),
        start_time=dict(type='str'),
        end_time=dict(type='str'),
        duration=dict(type='int'),
        status=dict(type='str', choices=['active', 'paused']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=[['end_time', 'duration']],
    )

    api_key = ur.resolve_api_key(module, module.params.get('api_key'), module.params.get('api_key_file'))
    state = module.params['state']

    # Synthesise friendly_name on create when the user didn't pass one.
    friendly_name = module.params.get('friendly_name')
    if not friendly_name and state == 'present':
        if not (module.params.get('type') and module.params.get('start_time') and module.params.get('end_time')):
            module.fail_json(msg='Either pass `friendly_name` or pass `type`, `start_time`, `end_time` so it can be synthesised.')
        friendly_name = _synthesise_name(module.params)

    module.log('uptimerobot_mwindow: looking up friendly_name={0!r}'.format(friendly_name))
    success, mwindows = ur.get_mwindows(module, api_key)
    if not success:
        module.fail_json(msg='Could not list maintenance windows: {0}'.format(mwindows))
    current = ur.find_by_friendly_name(mwindows, friendly_name) if friendly_name else None
    module.log('uptimerobot_mwindow: existing={0} (out of {1} mwindows on the account)'.format(
        bool(current), len(mwindows),
    ))

    if state == 'absent':
        if current is None:
            module.exit_json(changed=False, mwindow={}, debug={
                'operation': 'noop',
                'reason': 'mwindow not present',
                'friendly_name': friendly_name,
            })
        delete_before = {
            'friendly_name': current.get('friendly_name'),
            'id': current.get('id'),
            'type': current.get('type'),
        }
        if module.check_mode:
            module.exit_json(changed=True, mwindow=current,
                diff={'before': delete_before, 'after': {}},
                debug={
                    'operation': 'delete (check_mode)',
                    'friendly_name': friendly_name,
                    'mwindow_id': current['id'],
                })
        module.log('uptimerobot_mwindow: deleting id={0}'.format(current['id']))
        success, result = ur.delete_mwindow(module, api_key, current['id'])
        if not success:
            module.fail_json(msg='Could not delete maintenance window {0!r}: {1}'.format(friendly_name, result))
        module.exit_json(changed=True, mwindow=current,
            diff={'before': delete_before, 'after': {}},
            debug={
                'operation': 'delete',
                'friendly_name': friendly_name,
                'mwindow_id': current['id'],
            })

    # Build desired payload.
    duration = module.params.get('duration')
    if duration is None and module.params.get('end_time'):
        if not module.params.get('start_time'):
            module.fail_json(msg='`start_time` is required when `end_time` is given (so duration can be computed).')
        duration = _compute_duration(module.params['start_time'], module.params['end_time'])

    desired = {
        'friendly_name': friendly_name,
        'type': module.params.get('type'),
        'value': module.params.get('value'),
        'start_time': module.params.get('start_time'),
        'duration': duration,
        'status': module.params.get('status'),
    }
    desired = {k: v for k, v in desired.items() if v is not None and v != ''}

    if current is None:
        # Create. type/start_time/duration are required for new mwindows.
        for required in ('type', 'start_time'):
            if not desired.get(required):
                module.fail_json(msg='`{0}` is required when creating a new maintenance window.'.format(required))
        if not desired.get('duration'):
            module.fail_json(msg='Either `end_time` or `duration` is required when creating a new maintenance window.')
        # `status` not honoured on create.
        body = dict(desired)
        body.pop('status', None)
        create_diff = {'before': {}, 'after': dict(body)}
        if module.check_mode:
            module.exit_json(changed=True, mwindow=body,
                diff=create_diff,
                debug={
                    'operation': 'create (check_mode)',
                    'friendly_name': friendly_name,
                    'sent_keys': sorted(body.keys()),
                })
        module.log('uptimerobot_mwindow: creating friendly_name={0!r} sent_keys={1}'.format(
            friendly_name, sorted(body.keys()),
        ))
        success, result = ur.new_mwindow(module, api_key, body)
        if not success:
            module.fail_json(msg='Could not create maintenance window {0!r}: {1}'.format(friendly_name, result))
        module.exit_json(changed=True, mwindow=result,
            diff=create_diff,
            debug={
                'operation': 'create',
                'friendly_name': friendly_name,
                'sent_keys': sorted(body.keys()),
            })

    # Update. `get_mwindows` already translated type/value/status to labels.
    # `friendly_name` already encodes type/value/start_time/end_time (it is
    # auto-synthesised from those four), so changing any of them produces a
    # *new* mwindow rather than an edit. The only fields realistically
    # editable in-place are `duration` and `status`. Limiting the diff to
    # those two also dodges the API's inconsistent `start_time` storage
    # (older windows are saved as local `HH:MM`, newer ones as UTC `HH:MM:SS`).
    diff_fields = ['duration', 'status']
    current_compare = {field: current.get(field) for field in diff_fields}
    field_diff = ur.diff_for_update(current_compare, desired, diff_fields)
    if not field_diff:
        module.log('uptimerobot_mwindow: id={0} no diff -> changed=false'.format(current['id']))
        module.exit_json(changed=False, mwindow=current, debug={
            'operation': 'noop',
            'reason': 'no diff',
            'friendly_name': friendly_name,
            'mwindow_id': current['id'],
        })

    module.log('uptimerobot_mwindow: id={0} diff_fields={1}'.format(
        current['id'], sorted(field_diff.keys()),
    ))

    update_diff = {
        'before': {k: current_compare.get(k) for k in field_diff},
        'after': dict(field_diff),
    }

    if module.check_mode:
        preview = dict(current)
        preview.update(field_diff)
        module.exit_json(changed=True, mwindow=preview,
            diff=update_diff,
            debug={
                'operation': 'update (check_mode)',
                'friendly_name': friendly_name,
                'mwindow_id': current['id'],
                'diff_fields': sorted(field_diff.keys()),
            })

    body = dict(desired)
    body['id'] = current['id']
    success, result = ur.edit_mwindow(module, api_key, body)
    if not success:
        module.fail_json(msg='Could not edit maintenance window {0!r}: {1}'.format(friendly_name, result))
    module.exit_json(changed=True, mwindow=result,
        diff=update_diff,
        debug={
            'operation': 'update',
            'friendly_name': friendly_name,
            'mwindow_id': current['id'],
            'diff_fields': sorted(field_diff.keys()),
        })


if __name__ == '__main__':
    main()
