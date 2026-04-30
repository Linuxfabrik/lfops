#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: uptimerobot_mwindow
short_description: Create, update or delete an UptimeRobot maintenance window
version_added: '6.0.2'
description:
    - Manages a single UptimeRobot maintenance window (create, update of the editable parts, pause/resume, delete) against the v2 API.
    - Identification is by I(friendly_name). When omitted on I(state=present), the module synthesises one as C("<type> [<value>] <start_time>-<end_time>") (e.g. C(weekly mon 03:30-05:30), C(daily 02:00-02:30)) so re-runs stay idempotent without having to invent a name.
    - Update is intentionally narrow - only I(duration) and I(status) are diffed against the existing window. Changing the schedule itself (I(type), I(value), I(start_time), I(end_time)) means changing I(friendly_name) too (or the synthesised one), which results in a *new* window being created next to the old one rather than an in-place edit. This also avoids UptimeRobot's inconsistent C(start_time) storage (older windows are kept as local C(HH:MM), newer ones as UTC C(HH:MM:SS)) confusing the diff.
    - Provide either I(end_time) or I(duration), not both. When I(end_time) is given, the duration in minutes is computed automatically (wrapping over midnight when C(end_time < start_time)).
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
            - Display name of the window. When omitted on I(state=present), the module synthesises one from I(type), I(value), I(start_time) and I(end_time); in that case all four must be given. Required on I(state=absent).
        type: str
    state:
        description: C(present) creates or updates, C(absent) deletes. When the window does not exist on I(state=absent), the module exits with C(changed=false).
        type: str
        choices: ['absent', 'present']
        default: 'present'
    type:
        description: Recurrence type. Required when creating a new window.
        type: str
        choices: ['daily', 'monthly', 'once', 'weekly']
    value:
        description:
            - For I(type=C(weekly)), the weekday as a label (C(mon), C(tue), ..., C(sun)). Multiple weekdays can be passed as a dash-joined list (e.g. C(mon-wed-fri)).
            - For I(type=C(monthly)), the day of the month as a number C(1)..C(31) (passed through unchanged).
            - For I(type=C(once)) and I(type=C(daily)), unused.
        type: str
    start_time:
        description:
            - For I(type=C(once)), an RFC3339 timestamp.
            - For I(type=C(daily))/C(weekly)/C(monthly), an C(HH:MM) wall-clock time.
        type: str
    end_time:
        description:
            - C(HH:MM) wall-clock time. Combined with I(start_time) to compute I(duration) automatically; wraps over midnight when end < start. Mutually exclusive with I(duration).
        type: str
    duration:
        description: Duration of the window in minutes. Mutually exclusive with I(end_time).
        type: int
    status:
        description: C(active) un-pauses the window, C(paused) pauses it. Only honoured on edit; UptimeRobot rejects this field on create.
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
    description:
        - On create or update, the maintenance window as returned by UptimeRobot's C(newMWindow) / C(editMWindow). On delete, the last known state of the window.
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
        friendly_name: 'weekly mon 03:30-05:30'
        mwindow_id: 12345
        diff_fields: ['duration']
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
        api_key_file=dict(type='str', default='~/.uptimerobot'),
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
