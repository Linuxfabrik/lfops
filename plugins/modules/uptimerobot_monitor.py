#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Linuxfabrik, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r'''
---
module: uptimerobot_monitor
short_description: Manage UptimeRobot monitors
version_added: '6.1.0'
description:
    - Create, update or delete a monitor on UptimeRobot.
    - Targets the UptimeRobot API v2 (POST + form-urlencoded). Migration to v3
      is local to C(plugins/module_utils/uptimerobot.py); module-level options
      do not need to change.
    - Identification is by C(friendly_name). Re-running a task with the same
      C(friendly_name) updates the existing monitor in-place and only reports
      C(changed=true) when something actually differs.
author:
    - Linuxfabrik GmbH, Zurich, Switzerland (info (at) linuxfabrik (dot) ch)
requirements:
    - python >= 3.9
options:
    api_key:
        description:
            - UptimeRobot API key. If not given, the module reads
              C(api_key_file) (default C(~/.uptimerobot)) and finally
              C(UPTIMEROBOT_API_KEY) from the environment.
        type: str
        required: false
        no_log: true
    api_key_file:
        description:
            - Path to a file containing the UptimeRobot API key. Default
              C(~/.uptimerobot) (compatible with the C(utr) CLI).
        type: str
        required: false
    friendly_name:
        description:
            - Display name of the monitor. Used as the idempotency key.
        type: str
        required: true
    state:
        description:
            - C(present) creates the monitor if missing or updates it in-place
              if present.
            - C(absent) deletes the monitor identified by C(friendly_name)
              if it exists.
        type: str
        choices: ['absent', 'present']
        default: 'present'
    url:
        description:
            - URL / host / IP / heartbeat-token to monitor. Required for
              C(state=present) when the monitor does not yet exist.
        type: str
        required: false
    type:
        description:
            - Monitor type. C(http) for HTTP(S) checks, C(keyw) for keyword
              checks, C(ping) for ICMP, C(port) for TCP-port checks, C(beat)
              for heartbeat. Only honoured on create; UptimeRobot does not
              allow changing the type after the fact.
        type: str
        choices: ['beat', 'http', 'keyw', 'ping', 'port']
        required: false
    sub_type:
        description:
            - For C(type=port): which protocol/port preset to use. C(custom)
              means "use the explicit C(port) value".
        type: str
        choices: ['custom', 'ftp', 'http', 'https', 'imap', 'pop3', 'smtp']
        required: false
    port:
        description:
            - Custom port for C(type=port) + C(sub_type=custom).
        type: int
        required: false
    keyword_type:
        description:
            - For C(type=keyw): C(exist) alerts when the keyword is found,
              C(notex) alerts when it is missing.
        type: str
        choices: ['exist', 'notex']
        required: false
    keyword_case_type:
        description:
            - C(cs) case-sensitive, C(ci) case-insensitive.
        type: str
        choices: ['ci', 'cs']
        required: false
    keyword_value:
        description:
            - Keyword to look for in the response body.
        type: str
        required: false
    interval:
        description:
            - Check interval in seconds (UptimeRobot enforces a per-plan
              minimum, e.g. 30s on the Pro plan).
        type: int
        required: false
    timeout:
        description:
            - Per-check timeout in seconds.
        type: int
        required: false
    status:
        description:
            - C(up) un-pauses the monitor, C(paused) pauses it. Only honoured
              on edit (UptimeRobot rejects this on create).
        type: str
        choices: ['paused', 'up']
        required: false
    http_username:
        description:
            - Basic-auth / digest-auth username for HTTP(S) monitors.
        type: str
        required: false
    http_password:
        description:
            - Basic-auth / digest-auth password.
        type: str
        required: false
        no_log: true
    http_auth_type:
        description:
            - Auth scheme used together with C(http_username) /
              C(http_password).
        type: str
        choices: ['basic', 'digest']
        required: false
    http_method:
        description:
            - HTTP method for HTTP(S) monitors.
        type: str
        choices: ['delete', 'get', 'head', 'options', 'patch', 'post', 'put']
        required: false
    post_type:
        description:
            - Format of the C(post_value) payload.
        type: str
        choices: ['key-value', 'raw data']
        required: false
    post_value:
        description:
            - Payload sent with C(POST) / C(PUT) / C(PATCH) requests.
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
            - Extra HTTP headers to send. Pass either a JSON string or a dict;
              both are accepted.
        type: raw
        required: false
    custom_http_statuses:
        description:
            - Per-status-code override. UptimeRobot wire format applies.
        type: str
        required: false
    ignore_ssl_errors:
        description:
            - If C(true), accept invalid / self-signed TLS certificates.
        type: bool
        required: false
    disable_domain_expire_notifications:
        description:
            - C(disable) silences UptimeRobot's domain-expiry warnings,
              C(enable) keeps them on.
        type: str
        choices: ['disable', 'enable']
        required: false
    alert_contacts:
        description:
            - List of alert contacts to attach. Each item must reference an
              existing alert contact via its C(friendly_name) (preferred) or
              C(id), plus the per-monitor C(threshold) (alert delay in
              seconds, 0 = immediately) and C(recurrence) (re-alert interval
              in minutes, 0 = no recurrence).
        type: list
        elements: dict
        required: false
        suboptions:
            friendly_name:
                description: Friendly name of an existing alert contact.
                type: str
            id:
                description: ID of an existing alert contact (alternative to C(friendly_name)).
                type: int
            threshold:
                description: Alert delay in seconds.
                type: int
                default: 0
            recurrence:
                description: Re-alert interval in minutes.
                type: int
                default: 0
    mwindows:
        description:
            - List of maintenance windows to attach to the monitor. Each item
              references an existing maintenance window via its
              C(friendly_name) (preferred) or C(id).
        type: list
        elements: dict
        required: false
        suboptions:
            friendly_name:
                description: Friendly name of an existing maintenance window.
                type: str
            id:
                description: ID of an existing maintenance window.
                type: int
'''


EXAMPLES = r'''
- name: 'Manage a simple HTTPS monitor'
  linuxfabrik.lfops.uptimerobot_monitor:
    api_key: '{{ uptimerobot__api_key }}'
    friendly_name: '001 cloud.linuxfabrik.io/index.php/login'
    url: 'https://cloud.linuxfabrik.io/index.php/login'
    type: 'http'
    interval: 120
    http_method: 'get'
    alert_contacts:
      - friendly_name: 'root@linuxfabrik.ch'
        threshold: 1
        recurrence: 0
    mwindows:
      - friendly_name: 'weekly mon 03:30-05:30'
    state: 'present'

- name: 'Pause a monitor'
  linuxfabrik.lfops.uptimerobot_monitor:
    friendly_name: '001 cloud.linuxfabrik.io/index.php/login'
    status: 'paused'
    state: 'present'
  environment:
    UPTIMEROBOT_API_KEY: '{{ uptimerobot__api_key }}'

- name: 'Delete a monitor'
  linuxfabrik.lfops.uptimerobot_monitor:
    friendly_name: 'old-monitor'
    state: 'absent'
'''


RETURN = r'''
monitor:
    description: The monitor object as returned by UptimeRobot. Empty dict if the monitor was just deleted.
    type: dict
    returned: always
    sample:
        id: 794294
        friendly_name: '001 cloud.linuxfabrik.io/index.php/login'
        url: 'https://cloud.linuxfabrik.io/index.php/login'
        type: 1
        interval: 120
        status: 2
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
            module.fail_json(msg='Could not list alert contacts: {0}'.format(contacts))
        by_name = {c.get('friendly_name'): c for c in contacts}

    resolved = []
    for item in items:
        contact_id = item.get('id')
        if contact_id is None:
            name = item['friendly_name']
            if name not in by_name:
                module.fail_json(msg='Alert contact {0!r} not found on UptimeRobot'.format(name))
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
            module.fail_json(msg='Could not list maintenance windows: {0}'.format(mwindows))
        by_name = {m.get('friendly_name'): m for m in mwindows}

    ids = []
    for item in items:
        wid = item.get('id')
        if wid is None:
            name = item['friendly_name']
            if name not in by_name:
                module.fail_json(msg='Maintenance window {0!r} not found on UptimeRobot'.format(name))
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
        api_key_file=dict(type='str', required=False),
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

    module.log('uptimerobot_monitor: looking up friendly_name={0!r}'.format(friendly_name))

    # Step 1: locate the monitor by friendly_name. We can't trust `search` to
    # be exact-match, so list all and filter ourselves.
    success, monitors = ur.get_monitors(module, api_key)
    if not success:
        module.fail_json(msg='Could not list monitors: {0}'.format(monitors))
    current = ur.find_by_friendly_name(monitors, friendly_name)
    module.log('uptimerobot_monitor: existing={0} (out of {1} monitors on the account)'.format(
        bool(current), len(monitors),
    ))

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
        if module.check_mode:
            module.exit_json(changed=True, monitor=current, debug={
                'operation': 'delete (check_mode)',
                'friendly_name': friendly_name,
                'monitor_id': current['id'],
            })
        module.log('uptimerobot_monitor: deleting id={0} friendly_name={1!r}'.format(
            current['id'], friendly_name,
        ))
        success, result = ur.delete_monitor(module, api_key, current['id'])
        if not success:
            module.fail_json(msg='Could not delete monitor {0!r}: {1}'.format(friendly_name, result))
        module.exit_json(changed=True, monitor=current, debug={
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
        if module.check_mode:
            module.exit_json(changed=True, monitor=body, debug={
                'operation': 'create (check_mode)',
                'friendly_name': friendly_name,
                'sent_keys': sorted(body.keys()),
            })
        module.log('uptimerobot_monitor: creating friendly_name={0!r} sent_keys={1}'.format(
            friendly_name, sorted(body.keys()),
        ))
        success, result = ur.new_monitor(module, api_key, body)
        if not success:
            module.fail_json(msg='Could not create monitor {0!r}: {1}'.format(friendly_name, result))
        module.exit_json(changed=True, monitor=result, debug={
            'operation': 'create',
            'friendly_name': friendly_name,
            'sent_keys': sorted(body.keys()),
        })

    # --- present, update ----------------------------------------------------
    # Build the comparable representation of the current state.
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
        'status': ur.MONITOR_STATUS_READ.get(current.get('status'), current.get('status')),
        'alert_contacts': _normalize_current_alert_contacts(current.get('alert_contacts')),
        'mwindows': _normalize_current_mwindows(current.get('mwindows')),
    }

    desired_compare = dict(desired)
    if 'alert_contacts' in desired_compare:
        desired_compare['alert_contacts'] = _normalize_desired_alert_contacts(desired_compare['alert_contacts'])
    if 'mwindows' in desired_compare:
        desired_compare['mwindows'] = _normalize_desired_mwindows(desired_compare['mwindows'])

    # http_password can't be diffed (API hides it). If the user provided one,
    # always send it through to the edit, but don't let it count as a change.
    diff_fields = [f for f in _MONITOR_DIFFABLE_FIELDS if f != 'http_password']
    diff = ur.diff_for_update(current_compare, desired_compare, diff_fields)

    if not diff:
        module.log('uptimerobot_monitor: id={0} no diff -> changed=false'.format(current['id']))
        module.exit_json(changed=False, monitor=current, debug={
            'operation': 'noop',
            'reason': 'no diff',
            'friendly_name': friendly_name,
            'monitor_id': current['id'],
        })

    module.log('uptimerobot_monitor: id={0} diff_fields={1}'.format(
        current['id'], sorted(diff.keys()),
    ))

    if module.check_mode:
        preview = dict(current)
        preview.update(diff)
        module.exit_json(changed=True, monitor=preview, debug={
            'operation': 'update (check_mode)',
            'friendly_name': friendly_name,
            'monitor_id': current['id'],
            'diff_fields': sorted(diff.keys()),
        })

    body = dict(desired)
    body['id'] = current['id']
    success, result = ur.edit_monitor(module, api_key, body)
    if not success:
        module.fail_json(msg='Could not edit monitor {0!r}: {1}'.format(friendly_name, result))
    module.exit_json(changed=True, monitor=result, debug={
        'operation': 'update',
        'friendly_name': friendly_name,
        'monitor_id': current['id'],
        'diff_fields': sorted(diff.keys()),
    })


if __name__ == '__main__':
    main()
