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
module: uptimerobot_monitor
short_description: Create, update or delete an UptimeRobot monitor
version_added: '6.0.2'
description:
    - Manages a single UptimeRobot monitor end-to-end (create, update, pause/resume, delete) against the v2 API.
    - Identification is by I(friendly_name); the value must be unique on the account. Re-running a task with the same I(friendly_name) updates the existing monitor in place and only reports C(changed=true) when one of the diffable fields actually differs.
    - Enum-coded fields (C(type), C(sub_type), C(keyword_type), C(keyword_case_type), C(http_auth_type), C(http_method), C(post_type), C(post_content_type), C(disable_domain_expire_notifications), C(status)) are accepted in their human-readable form; the module translates to the API's integer codes on write and back on read, so the diff happens on labels.
    - I(http_password) and I(http_auth_type) are not visible in the C(getMonitors) response; when set, they are forwarded on every edit but never count as a change. I(type) is only honoured on create - UptimeRobot does not allow changing the monitor type after the fact. I(status) is only honoured on edit, since UptimeRobot rejects it on create.
author:
    - Linuxfabrik GmbH, Zurich, Switzerland (info (at) linuxfabrik (dot) ch)
requirements:
    - python >= 3.9
options:
    api_key:
        description:
            - UptimeRobot API key. When unset, the module reads I(api_key_file) (default C(~/.uptimerobot)) and finally falls back to the C(UPTIMEROBOT_API_KEY) environment variable.
        type: str
        required: false
        no_log: true
    api_key_file:
        description:
            - Path to a file whose first line is the UptimeRobot API key. Tilde-expanded.
        type: str
        required: false
        default: '~/.uptimerobot'
    friendly_name:
        description:
            - Display name of the monitor. Used as the idempotency key, so it must be unique on the account.
        type: str
        required: true
    state:
        description:
            - C(present) creates the monitor when missing, or updates it in place when present.
            - C(absent) deletes the monitor identified by I(friendly_name). When the monitor does not exist, the module exits with C(changed=false).
        type: str
        choices: ['absent', 'present']
        default: 'present'
    url:
        description:
            - URL, host, IP or heartbeat token to monitor. Required when creating a new monitor; ignored on update if unchanged.
        type: str
        required: false
    type:
        description:
            - Monitor type. C(http) for HTTP(S) checks, C(keyw) for keyword checks, C(ping) for ICMP, C(port) for TCP-port checks, C(beat) for heartbeat.
            - Required when creating a new monitor. Only honoured on create; UptimeRobot rejects type changes on existing monitors.
        type: str
        choices: ['beat', 'http', 'keyw', 'ping', 'port']
        required: false
    sub_type:
        description:
            - For I(type=C(port)), which protocol/port preset to use. C(custom) means "use the explicit I(port) value".
        type: str
        choices: ['custom', 'ftp', 'http', 'https', 'imap', 'pop3', 'smtp']
        required: false
    port:
        description:
            - Custom port number. Only consulted by UptimeRobot when I(type=C(port)) and I(sub_type=C(custom)).
        type: int
        required: false
    keyword_type:
        description:
            - For I(type=C(keyw)), C(exist) alerts when the keyword is found in the response body, C(notex) alerts when it is missing.
        type: str
        choices: ['exist', 'notex']
        required: false
    keyword_case_type:
        description:
            - For I(type=C(keyw)), C(cs) makes the search case-sensitive, C(ci) case-insensitive.
        type: str
        choices: ['ci', 'cs']
        required: false
    keyword_value:
        description:
            - Keyword to look for in the response body. Required for I(type=C(keyw)).
        type: str
        required: false
    interval:
        description:
            - Check interval in seconds. UptimeRobot enforces a per-plan minimum (e.g. 30s on the Pro plan, 300s on the free plan).
        type: int
        required: false
    timeout:
        description:
            - Per-check timeout in seconds.
        type: int
        required: false
    status:
        description:
            - C(up) un-pauses the monitor, C(paused) pauses it. Only honoured on edit; UptimeRobot rejects this field on create. To create a monitor in a paused state, create it first and then re-run the task with I(status=C(paused)).
        type: str
        choices: ['paused', 'up']
        required: false
    http_username:
        description:
            - Username for HTTP basic / digest authentication. Only meaningful for I(type=C(http)) and I(type=C(keyw)).
        type: str
        required: false
    http_password:
        description:
            - Password for HTTP basic / digest authentication. UptimeRobot does not return this field in C(getMonitors), so the module always forwards the value on edit but never counts it as a change.
        type: str
        required: false
        no_log: true
    http_auth_type:
        description:
            - Authentication scheme used together with I(http_username) and I(http_password). Like I(http_password), this is forwarded on every edit but never counted as a change because the API does not return it.
        type: str
        choices: ['basic', 'digest']
        required: false
    http_method:
        description:
            - HTTP method to use for I(type=C(http)) and I(type=C(keyw)) monitors.
        type: str
        choices: ['delete', 'get', 'head', 'options', 'patch', 'post', 'put']
        required: false
    post_type:
        description:
            - Format of the I(post_value) payload.
        type: str
        choices: ['key-value', 'raw data']
        required: false
    post_value:
        description:
            - Payload to send with C(POST) / C(PUT) / C(PATCH) requests.
        type: str
        required: false
    post_content_type:
        description:
            - C(Content-Type) header for the request body.
        type: str
        choices: ['content/json', 'text/html']
        required: false
    custom_http_headers:
        description:
            - Extra HTTP headers to send with each check. Accepts either a JSON-encoded string or a plain dict; the module forwards either form to UptimeRobot unchanged.
        type: raw
        required: false
    custom_http_statuses:
        description:
            - Override of which HTTP status codes count as up/down, in UptimeRobot's wire format (e.g. C(200:0_201:0_500:1)). Only forwarded as-is.
        type: str
        required: false
    ignore_ssl_errors:
        description:
            - When C(true), accept invalid or self-signed TLS certificates and only fail on connection-level errors.
        type: bool
        required: false
    disable_domain_expire_notifications:
        description:
            - C(disable) silences UptimeRobot's domain-expiry warnings for this monitor, C(enable) keeps them on.
        type: str
        choices: ['disable', 'enable']
        required: false
    alert_contacts:
        description:
            - Alert contacts to attach to the monitor. Each item references an existing alert contact, plus the per-monitor I(threshold) and I(recurrence). The list is replaced on every run; pass an empty list to clear all attached contacts.
            - When an item has I(id), it is used directly. Otherwise I(friendly_name) is resolved against C(getAlertContacts); an unknown name fails the play.
        type: list
        elements: dict
        required: false
        suboptions:
            friendly_name:
                description: Friendly name of an existing alert contact. Required if I(id) is not given.
                type: str
            id:
                description: Numeric ID of an existing alert contact. Takes precedence over I(friendly_name) when both are set.
                type: int
            threshold:
                description: Alert delay in seconds. C(0) means alert immediately.
                type: int
                default: 0
            recurrence:
                description: Re-alert interval in minutes. C(0) disables re-alerting.
                type: int
                default: 0
    mwindows:
        description:
            - Maintenance windows to attach to the monitor. Each item references an existing maintenance window. The list is replaced on every run; pass an empty list to detach all windows.
            - When an item has I(id), it is used directly. Otherwise I(friendly_name) is resolved against C(getMWindows); an unknown name fails the play.
        type: list
        elements: dict
        required: false
        suboptions:
            friendly_name:
                description: Friendly name of an existing maintenance window. Required if I(id) is not given.
                type: str
            id:
                description: Numeric ID of an existing maintenance window. Takes precedence over I(friendly_name) when both are set.
                type: int
'''


EXAMPLES = r'''
# 1) Create-or-update a simple HTTPS monitor. Idempotent: re-running with the
#    same values reports `changed=false`.
- name: 'Manage a simple HTTPS monitor'
  linuxfabrik.lfops.uptimerobot_monitor:
    api_key: '{{ uptimerobot__api_key }}'
    friendly_name: '001 www.example.com/index.php/login'
    url: 'https://www.example.com/index.php/login'
    type: 'http'
    interval: 120
    http_method: 'get'
    alert_contacts:
      - friendly_name: 'monitoring@example.com'
        threshold: 1
        recurrence: 0
    mwindows:
      - friendly_name: 'weekly mon 03:30-05:30'
    state: 'present'

# 2) Keyword monitor: alert if the page does NOT contain "OK" (case-insensitive).
- name: 'Keyword-monitor a healthcheck endpoint'
  linuxfabrik.lfops.uptimerobot_monitor:
    friendly_name: '001 healthcheck.example.com'
    url: 'https://healthcheck.example.com/status'
    type: 'keyw'
    keyword_type: 'notex'
    keyword_case_type: 'ci'
    keyword_value: 'OK'
    interval: 60
    alert_contacts:
      - friendly_name: 'monitoring@example.com'
        threshold: 1
        recurrence: 0
    state: 'present'

# 3) Pause / resume a monitor. The API key is taken from the environment.
- name: 'Pause a monitor before a deployment'
  linuxfabrik.lfops.uptimerobot_monitor:
    friendly_name: '001 www.example.com/index.php/login'
    status: 'paused'
    state: 'present'
  environment:
    UPTIMEROBOT_API_KEY: '{{ uptimerobot__api_key }}'

- name: 'Resume the monitor after the deployment'
  linuxfabrik.lfops.uptimerobot_monitor:
    friendly_name: '001 www.example.com/index.php/login'
    status: 'up'
    state: 'present'

# 4) Bulk-pause every monitor of a given prefix (e.g. before a deployment
#    that would otherwise trigger spurious down-alerts):
- name: 'Inventory monitors to pause'
  linuxfabrik.lfops.uptimerobot_monitor_info:
    search: '001 '
  register: 'ur_to_pause'

- name: 'Pause them all'
  linuxfabrik.lfops.uptimerobot_monitor:
    friendly_name: '{{ item.friendly_name }}'
    status: 'paused'
    state: 'present'
  loop: '{{ ur_to_pause.monitors }}'
  loop_control:
    label: '{{ item.friendly_name }}'

# 5) Delete a stale monitor.
- name: 'Delete a monitor'
  linuxfabrik.lfops.uptimerobot_monitor:
    friendly_name: 'old-monitor'
    state: 'absent'

# Debugging hints:
#   * Tail per-call syslog: `journalctl --identifier ansible-uptimerobot_monitor --follow`
#   * Inspect the structured operation summary: `register: r` + `debug var=r.debug`.
#   * Use `--check --diff` to preview create/update/delete without API writes.
'''


RETURN = r'''
monitor:
    description:
        - On create or update, the monitor object as returned by UptimeRobot's C(newMonitor) / C(editMonitor). On delete, the last known state of the monitor as returned by C(getMonitors).
        - Empty dict when there was nothing to delete (state=absent and monitor not present).
        - In check mode, a synthetic preview reflecting what the run would have written.
    type: dict
    returned: always
    sample:
        id: 794294
        friendly_name: '001 www.example.com/index.php/login'
        url: 'https://www.example.com/index.php/login'
        type: 'http'
        interval: 120
        status: 'up'
debug:
    description: Diagnostic information about the operation (one of C(create), C(update), C(delete), C(noop), each optionally suffixed with C( (check_mode))). Stable enough to assert against, not stable enough to be load-bearing.
    type: dict
    returned: always
    sample:
        operation: 'update'
        friendly_name: '001 www.example.com/index.php/login'
        monitor_id: 794294
        diff_fields: ['interval']
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.linuxfabrik.lfops.plugins.module_utils import uptimerobot as ur


# Fields we ship to new_monitor / edit_monitor and that we also diff against
# the API's current state to decide whether an edit call is needed.
_MONITOR_DIFFABLE_FIELDS = [
    'url',
    'sub_type', 'port',
    'keyword_type', 'keyword_case_type', 'keyword_value',
    'interval', 'timeout',
    'http_username', 'http_password', 'http_auth_type',
    'post_type', 'post_value', 'http_method', 'post_content_type',
    'custom_http_headers', 'custom_http_statuses',
    'ignore_ssl_errors', 'disable_domain_expire_notifications',
    'status',
    'alert_contacts', 'mwindows',
]


def _build_alert_contacts(module, api_key, items):
    """Resolve the user-supplied list of {friendly_name|id, threshold, recurrence}
    into the v2 wire string id_threshold_recurrence-...
    """
    if not items:
        return None
    needs_resolution = [i.get('friendly_name') for i in items if not i.get('id')]
    by_name = {}
    if needs_resolution:
        success, contacts = ur.get_alert_contacts(module, api_key)
        if not success:
            module.fail_json(msg=f'Could not list alert contacts: {contacts}')
        by_name = {c.get('friendly_name'): c for c in contacts}

    resolved = []
    for item in items:
        contact_id = item.get('id')
        if contact_id is None:
            name = item['friendly_name']
            if name not in by_name:
                module.fail_json(msg=f'Alert contact {name!r} not found on UptimeRobot')
            contact_id = int(by_name[name]['id'])
        resolved.append({
            'id': contact_id,
            'threshold': int(item.get('threshold', 0)),
            'recurrence': int(item.get('recurrence', 0)),
        })
    return ur.alert_contacts_wire(resolved)


def _build_mwindows(module, api_key, items):
    if not items:
        return None
    needs_resolution = [i.get('friendly_name') for i in items if not i.get('id')]
    by_name = {}
    if needs_resolution:
        success, mwindows = ur.get_mwindows(module, api_key)
        if not success:
            module.fail_json(msg=f'Could not list maintenance windows: {mwindows}')
        by_name = {m.get('friendly_name'): m for m in mwindows}

    ids = []
    for item in items:
        wid = item.get('id')
        if wid is None:
            name = item['friendly_name']
            if name not in by_name:
                module.fail_json(msg=f'Maintenance window {name!r} not found on UptimeRobot')
            wid = int(by_name[name]['id'])
        ids.append(int(wid))
    return ur.mwindows_wire(ids)


def _normalize_current_alert_contacts(current_field):
    """The API returns alert_contacts as a list of dicts with keys id, threshold,
    recurrence (and type, friendly_name, ...). Reduce to the wire representation
    so we can str-compare against the desired wire string.
    """
    if not current_field:
        return ''
    items = []
    for ac in current_field:
        items.append({
            'id': int(ac['id']),
            'threshold': int(ac.get('threshold', 0)),
            'recurrence': int(ac.get('recurrence', 0)),
        })
    items.sort(key=lambda x: x['id'])
    return ur.alert_contacts_wire(items)


def _normalize_current_mwindows(current_field):
    if not current_field:
        return ''
    ids = sorted(int(m['id']) for m in current_field)
    return ur.mwindows_wire(ids)


def _normalize_desired_alert_contacts(wire):
    """Sort the wire string by id so it compares stably to the API form."""
    if not wire:
        return ''
    parts = []
    for token in wire.split('-'):
        bits = token.split('_')
        parts.append({'id': int(bits[0]), 'threshold': int(bits[1]), 'recurrence': int(bits[2])})
    parts.sort(key=lambda x: x['id'])
    return ur.alert_contacts_wire(parts)


def _normalize_desired_mwindows(wire):
    if not wire:
        return ''
    ids = sorted(int(x) for x in wire.split('-') if x)
    return ur.mwindows_wire(ids)


def main():
    argument_spec = dict(
        api_key=dict(type='str', required=False, no_log=True),
        api_key_file=dict(type='str', required=False, default='~/.uptimerobot'),
        friendly_name=dict(type='str', required=True),
        state=dict(type='str', choices=['absent', 'present'], default='present'),

        url=dict(type='str'),
        type=dict(type='str', choices=['beat', 'http', 'keyw', 'ping', 'port']),
        sub_type=dict(type='str', choices=['custom', 'ftp', 'http', 'https', 'imap', 'pop3', 'smtp']),
        port=dict(type='int'),
        keyword_type=dict(type='str', choices=['exist', 'notex']),
        keyword_case_type=dict(type='str', choices=['ci', 'cs']),
        keyword_value=dict(type='str'),
        interval=dict(type='int'),
        timeout=dict(type='int'),
        status=dict(type='str', choices=['paused', 'up']),
        http_username=dict(type='str'),
        http_password=dict(type='str', no_log=True),
        http_auth_type=dict(type='str', choices=['basic', 'digest']),
        http_method=dict(type='str', choices=['delete', 'get', 'head', 'options', 'patch', 'post', 'put']),
        post_type=dict(type='str', choices=['key-value', 'raw data']),
        post_value=dict(type='str'),
        post_content_type=dict(type='str', choices=['content/json', 'text/html']),
        custom_http_headers=dict(type='raw'),
        custom_http_statuses=dict(type='str'),
        ignore_ssl_errors=dict(type='bool'),
        disable_domain_expire_notifications=dict(type='str', choices=['disable', 'enable']),
        alert_contacts=dict(type='list', elements='dict'),
        mwindows=dict(type='list', elements='dict'),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    api_key = ur.resolve_api_key(module, module.params.get('api_key'), module.params.get('api_key_file'))
    friendly_name = module.params['friendly_name']
    state = module.params['state']

    module.log(f'uptimerobot_monitor: looking up friendly_name={friendly_name!r}')

    # Step 1: locate the monitor by friendly_name. We can't trust `search` to
    # be exact-match, so list all and filter ourselves.
    success, monitors = ur.get_monitors(module, api_key)
    if not success:
        module.fail_json(msg=f'Could not list monitors: {monitors}')
    current = ur.find_by_friendly_name(monitors, friendly_name)
    module.log(f'uptimerobot_monitor: existing={bool(current)} (out of {len(monitors)} monitors on the account)')

    # Step 2: build the desired payload (only fields the user actually set).
    desired = {}
    for field in [
        'url', 'sub_type', 'port',
        'keyword_type', 'keyword_case_type', 'keyword_value',
        'interval', 'timeout',
        'http_username', 'http_password', 'http_auth_type',
        'post_type', 'post_value', 'http_method', 'post_content_type',
        'custom_http_headers', 'custom_http_statuses',
        'ignore_ssl_errors', 'disable_domain_expire_notifications',
        'status',
    ]:
        value = module.params.get(field)
        if value is not None and value != '':
            desired[field] = value
    if module.params.get('alert_contacts'):
        desired['alert_contacts'] = _build_alert_contacts(module, api_key, module.params['alert_contacts'])
    if module.params.get('mwindows'):
        desired['mwindows'] = _build_mwindows(module, api_key, module.params['mwindows'])

    # --- absent -------------------------------------------------------------
    if state == 'absent':
        if current is None:
            module.exit_json(changed=False, monitor={}, debug={
                'operation': 'noop',
                'reason': 'monitor not present',
                'friendly_name': friendly_name,
            })
        delete_before = {
            'friendly_name': current.get('friendly_name'),
            'id': current.get('id'),
            'url': current.get('url'),
        }
        if module.check_mode:
            module.exit_json(changed=True, monitor=current,
                diff={'before': delete_before, 'after': {}},
                debug={
                    'operation': 'delete (check_mode)',
                    'friendly_name': friendly_name,
                    'monitor_id': current['id'],
                })
        module.log(f"uptimerobot_monitor: deleting id={current['id']} friendly_name={friendly_name!r}")
        success, result = ur.delete_monitor(module, api_key, current['id'])
        if not success:
            module.fail_json(msg=f'Could not delete monitor {friendly_name!r}: {result}')
        module.exit_json(changed=True, monitor=current,
            diff={'before': delete_before, 'after': {}},
            debug={
                'operation': 'delete',
                'friendly_name': friendly_name,
                'monitor_id': current['id'],
            })

    # --- present, create ----------------------------------------------------
    if current is None:
        if not module.params.get('url'):
            module.fail_json(msg='`url` is required when creating a new monitor.')
        if not module.params.get('type'):
            module.fail_json(msg='`type` is required when creating a new monitor.')
        body = dict(desired)
        body['friendly_name'] = friendly_name
        body['url'] = module.params['url']
        body['type'] = module.params['type']
        # `status` is not allowed on create.
        body.pop('status', None)
        create_diff = {'before': {}, 'after': dict(body)}
        if module.check_mode:
            module.exit_json(changed=True, monitor=body,
                diff=create_diff,
                debug={
                    'operation': 'create (check_mode)',
                    'friendly_name': friendly_name,
                    'sent_keys': sorted(body.keys()),
                })
        module.log(f'uptimerobot_monitor: creating friendly_name={friendly_name!r} sent_keys={sorted(body.keys())}')
        success, result = ur.new_monitor(module, api_key, body)
        if not success:
            module.fail_json(msg=f'Could not create monitor {friendly_name!r}: {result}')
        module.exit_json(changed=True, monitor=result,
            diff=create_diff,
            debug={
                'operation': 'create',
                'friendly_name': friendly_name,
                'sent_keys': sorted(body.keys()),
            })

    # --- present, update ----------------------------------------------------
    # Build the comparable representation of the current state. `get_monitors`
    # already translated enum-coded fields back to user-facing labels, so we
    # can compare current/desired field-by-field without further conversion.
    current_compare = {
        'url': current.get('url'),
        'sub_type': current.get('sub_type'),
        'port': current.get('port'),
        'keyword_type': current.get('keyword_type'),
        'keyword_case_type': current.get('keyword_case_type'),
        'keyword_value': current.get('keyword_value'),
        'interval': current.get('interval'),
        'timeout': current.get('timeout'),
        'http_username': current.get('http_username'),
        # http_password is not returned by the API, so don't try to diff it.
        'http_auth_type': current.get('http_auth_type'),
        'post_type': current.get('post_type'),
        'post_value': current.get('post_value'),
        'http_method': current.get('http_method'),
        'post_content_type': current.get('post_content_type'),
        'custom_http_headers': current.get('custom_http_headers'),
        'custom_http_statuses': current.get('custom_http_statuses'),
        'ignore_ssl_errors': current.get('ignore_ssl_errors'),
        'disable_domain_expire_notifications': current.get('disable_domain_expire_notifications'),
        'status': current.get('status'),
        'alert_contacts': _normalize_current_alert_contacts(current.get('alert_contacts')),
        'mwindows': _normalize_current_mwindows(current.get('mwindows')),
    }

    desired_compare = dict(desired)
    if 'alert_contacts' in desired_compare:
        desired_compare['alert_contacts'] = _normalize_desired_alert_contacts(desired_compare['alert_contacts'])
    if 'mwindows' in desired_compare:
        desired_compare['mwindows'] = _normalize_desired_mwindows(desired_compare['mwindows'])

    # `http_password` and `http_auth_type` can't be diffed reliably because
    # the API hides them in `getMonitors` responses (the `auth_type` field
    # comes back as null even when credentials are set). Always send them
    # through on edit when the user supplied them, but don't let them count
    # as a change.
    write_only = {'http_password', 'http_auth_type'}
    diff_fields = [f for f in _MONITOR_DIFFABLE_FIELDS if f not in write_only]
    field_diff = ur.diff_for_update(current_compare, desired_compare, diff_fields)

    if not field_diff:
        module.log(f"uptimerobot_monitor: id={current['id']} no diff -> changed=false")
        module.exit_json(changed=False, monitor=current, debug={
            'operation': 'noop',
            'reason': 'no diff',
            'friendly_name': friendly_name,
            'monitor_id': current['id'],
        })

    module.log(f"uptimerobot_monitor: id={current['id']} diff_fields={sorted(field_diff.keys())}")

    update_diff = {
        'before': {k: current_compare.get(k) for k in field_diff},
        'after': dict(field_diff),
    }

    if module.check_mode:
        preview = dict(current)
        preview.update(field_diff)
        module.exit_json(changed=True, monitor=preview,
            diff=update_diff,
            debug={
                'operation': 'update (check_mode)',
                'friendly_name': friendly_name,
                'monitor_id': current['id'],
                'diff_fields': sorted(field_diff.keys()),
            })

    body = dict(desired)
    body['id'] = current['id']
    success, result = ur.edit_monitor(module, api_key, body)
    if not success:
        module.fail_json(msg=f'Could not edit monitor {friendly_name!r}: {result}')
    module.exit_json(changed=True, monitor=result,
        diff=update_diff,
        debug={
            'operation': 'update',
            'friendly_name': friendly_name,
            'monitor_id': current['id'],
            'diff_fields': sorted(field_diff.keys()),
        })


if __name__ == '__main__':
    main()
