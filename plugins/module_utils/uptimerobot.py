#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Linuxfabrik, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

"""Shared client for the UptimeRobot API used by the linuxfabrik.lfops.uptimerobot_*
modules.

Currently targets UptimeRobot API v2 (POST + form-urlencoded, API key in body),
because v2 is fully specified, all five resources are covered by
linuxfabrik-lib's `lib.uptimerobot`, and there's no public, machine-readable
spec for v3 that we can rely on. Migration to v3 is local to this file: change
the endpoint URLs / request shape in `_request()` and the per-resource
methods, modules don't have to change.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import os
import time
from urllib.parse import urlencode

from ansible.module_utils.urls import fetch_url


API_BASE = 'https://api.uptimerobot.com/v2/'
ENV_API_KEY = 'UPTIMEROBOT_API_KEY'
DEFAULT_API_KEY_FILE = '~/.uptimerobot'

# How many items v2 returns per page. We page until pagination['total'] is reached.
PAGE_SIZE = 50

# When the API returns 429 (rate limit), wait this many seconds and retry once.
DEFAULT_RATE_LIMIT_RETRY_SECONDS = 10

# --- Human-readable -> UptimeRobot wire values -------------------------------
# These come 1:1 from linuxfabrik-lib's lib/uptimerobot.py replace_maps.
# Keep them in sync if upstream changes.

MONITOR_TYPE = {'http': 1, 'keyw': 2, 'ping': 3, 'port': 4, 'beat': 5}
MONITOR_STATUS_READ = {0: 'paused', 1: 'wait', 2: 'up', 8: 'seems_down', 9: 'down'}
MONITOR_STATUS_WRITE = {'paused': 0, 'up': 1}  # write side only allows pause/un-pause
MONITOR_SUB_TYPE = {
    'http': 1, 'https': 443, 'ftp': 21, 'smtp': 25,
    'pop3': 110, 'imap': 143, 'custom': 99,
}
KEYWORD_TYPE = {'exist': 1, 'notex': 2}
KEYWORD_CASE_TYPE = {'cs': 0, 'ci': 1}
HTTP_AUTH_TYPE = {'basic': 1, 'digest': 2}
HTTP_METHOD = {
    'head': 1, 'get': 2, 'post': 3, 'put': 4,
    'patch': 5, 'delete': 6, 'options': 7,
}
POST_TYPE = {'key-value': 1, 'raw data': 2}
POST_CONTENT_TYPE = {'text/html': 0, 'content/json': 1}
DISABLE_DOMAIN_EXPIRE = {'enable': 0, 'disable': 1}

MWINDOW_TYPE = {'once': 1, 'daily': 2, 'weekly': 3, 'monthly': 4}
MWINDOW_DAY = {
    'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4,
    'fri': 5, 'sat': 6, 'sun': 7,
}
MWINDOW_STATUS = {'paused': 0, 'active': 1}

PSP_SORT = {'a-z': 1, 'z-a': 2, 'up-down-paused': 3, 'down-up-paused': 4}
PSP_STATUS = {'paused': 0, 'active': 1}

ALERT_CONTACT_TYPE_READ = {
    1: 'sms', 2: 'email', 3: 'twitter_dm', 5: 'web-hook', 6: 'pushbullet',
    7: 'zapier', 8: 'pushover', 9: 'hipchat', 10: 'slack', 11: 'voice-call',
    12: 'splunk', 13: 'pagerduty', 14: 'opsgenie', 15: 'ms_teams',
    16: 'google_chat', 17: 'discord', 18: 'mattermost',
}


def _translate(value, mapping):
    """Translate a single value via mapping; return original if unknown."""
    if isinstance(value, str) and value in mapping:
        return mapping[value]
    return value


# --- Auth --------------------------------------------------------------------


def resolve_api_key(module, api_key, api_key_file):
    """Resolve API key in this order:
    1. `api_key` module argument (if non-empty),
    2. `api_key_file` (if set and readable; also tries DEFAULT_API_KEY_FILE),
    3. ENV_API_KEY environment variable.

    Calls `module.fail_json` if nothing yielded a key.
    """
    if api_key:
        module.log('uptimerobot: api_key resolved from module argument')
        return api_key

    candidates = []
    if api_key_file:
        candidates.append(os.path.expanduser(api_key_file))
    else:
        candidates.append(os.path.expanduser(DEFAULT_API_KEY_FILE))

    for path in candidates:
        try:
            with open(path) as fh:
                value = fh.read().strip()
                if value:
                    module.log('uptimerobot: api_key resolved from file {0}'.format(path))
                    return value
        except OSError:
            pass

    env = os.environ.get(ENV_API_KEY, '').strip()
    if env:
        module.log('uptimerobot: api_key resolved from env {0}'.format(ENV_API_KEY))
        return env

    module.fail_json(msg=(
        'No UptimeRobot API key found. Provide one via the `api_key` parameter, '
        'an `api_key_file` (default: {default}), or the {env} environment '
        'variable.'
    ).format(default=DEFAULT_API_KEY_FILE, env=ENV_API_KEY))


# --- Wire format helpers -----------------------------------------------------


def alert_contacts_wire(items):
    """Build the v2 wire string for alert_contacts.

    Input: list of dicts with keys `id`, `threshold` (int seconds, 0 = immediately),
    `recurrence` (int minutes, 0 = no recurrence).
    Wire format: 'id_threshold_recurrence-id_threshold_recurrence-...'.
    """
    parts = []
    for item in items:
        parts.append('{id}_{t}_{r}'.format(
            id=item['id'],
            t=item.get('threshold', 0),
            r=item.get('recurrence', 0),
        ))
    return '-'.join(parts)


def mwindows_wire(ids):
    """Build the v2 wire string for mwindows.

    Input: list of integer mwindow IDs.
    Wire format: 'id-id-id' (dash-separated).
    """
    return '-'.join(str(i) for i in ids)


def monitors_wire(ids):
    """Build the v2 wire string for the PSP `monitors` field (comma-separated)."""
    return ','.join(str(i) for i in ids)


# --- Core HTTP ---------------------------------------------------------------


# Keys we never want to leak into module.log() output.
_SENSITIVE_KEYS = frozenset(('api_key', 'http_password', 'password'))


def _safe_keys(params):
    """Return a sorted list of params keys with sensitive values masked.

    Used for module.log() so we can see which fields a call is sending
    without leaking secrets to syslog.
    """
    return sorted(
        '{0}=<redacted>'.format(k) if k in _SENSITIVE_KEYS else k
        for k in params
    )


def _request(module, api_key, endpoint, params, result_key):
    """POST against the v2 API and return (success, result).

    On success, `result` is a list of items (or a scalar dict for single-resource
    endpoints, e.g. account). On failure, `result` is an error message string.

    Handles offset-pagination automatically. Retries once on HTTP 429.
    """
    url = API_BASE + endpoint
    body = dict(params)
    body['api_key'] = api_key
    body['format'] = 'json'

    module.log('uptimerobot: POST {endpoint} keys={keys}'.format(
        endpoint=endpoint, keys=_safe_keys(params),
    ))

    aggregated = []
    offset = 0
    is_paginated_field = None
    pages = 0

    while True:
        body['offset'] = offset
        encoded = urlencode(body, doseq=True).encode('utf-8')
        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        resp, info = fetch_url(
            module,
            url,
            data=encoded,
            headers=headers,
            method='POST',
            timeout=20,
        )
        status = info.get('status', -1)
        pages += 1

        if status == 429:
            retry_after = int(info.get('retry-after') or DEFAULT_RATE_LIMIT_RETRY_SECONDS)
            sleep_for = min(retry_after, 60)
            module.warn(
                'uptimerobot: rate limited on {endpoint} (HTTP 429); sleeping {sec}s and retrying once'.format(
                    endpoint=endpoint, sec=sleep_for,
                ),
            )
            time.sleep(sleep_for)
            resp, info = fetch_url(
                module,
                url,
                data=encoded,
                headers=headers,
                method='POST',
                timeout=20,
            )
            status = info.get('status', -1)

        if status < 200 or status >= 300:
            module.log('uptimerobot: POST {endpoint} -> HTTP {status}'.format(
                endpoint=endpoint, status=status,
            ))
            return False, 'HTTP {status} from {url}: {msg}'.format(
                status=status,
                url=url,
                msg=info.get('msg') or info.get('body') or '',
            )

        try:
            payload = json.loads(resp.read().decode('utf-8'))
        except (ValueError, AttributeError) as exc:
            return False, 'Could not parse JSON from {url}: {exc}'.format(url=url, exc=exc)

        if payload.get('stat') != 'ok':
            err = payload.get('error') or {}
            module.log('uptimerobot: POST {endpoint} stat=fail type={type}'.format(
                endpoint=endpoint, type=err.get('type', 'unknown'),
            ))
            return False, '{type}: {message}'.format(
                type=err.get('type', 'unknown'),
                message=err.get('message', payload),
            )

        if payload.get(result_key) is None:
            # Some endpoints return only `stat: 'ok'` (e.g. delete, edit when no
            # detail is included). Fall back to the message field if present.
            module.log('uptimerobot: POST {endpoint} stat=ok (no {key} in payload)'.format(
                endpoint=endpoint, key=result_key,
            ))
            return True, payload.get('message', payload)

        item = payload[result_key]
        if isinstance(item, list):
            aggregated += item
            is_paginated_field = True
        else:
            module.log('uptimerobot: POST {endpoint} stat=ok pages={pages}'.format(
                endpoint=endpoint, pages=pages,
            ))
            return True, item

        pagination = payload.get('pagination') or {}
        if not pagination:
            break
        total = pagination.get('total', len(aggregated))
        if offset + PAGE_SIZE >= total:
            break
        offset += PAGE_SIZE

    module.log('uptimerobot: POST {endpoint} stat=ok pages={pages} items={n}'.format(
        endpoint=endpoint, pages=pages, n=len(aggregated),
    ))
    return True, aggregated if is_paginated_field else aggregated


def _filter_keys(params, allowed):
    """Drop keys not in `allowed` and drop None / empty-string values."""
    out = {}
    for key, value in params.items():
        if key not in allowed:
            continue
        if value is None or value == '':
            continue
        out[key] = value
    return out


def _translate_keys(params, mapping_per_key):
    """For each key in `mapping_per_key`, translate the value via the mapping
    (e.g. 'http' -> 1) when the value is a string and present in the map.
    """
    for key, mapping in mapping_per_key.items():
        if key in params and isinstance(params[key], str):
            params[key] = _translate(params[key], mapping)
    return params


# --- Per-resource API: monitors ---------------------------------------------


# Common to new + edit. `id` and `status` are edit-only; `type` is create-only.
_MONITOR_COMMON_KEYS = {
    'friendly_name', 'url', 'sub_type', 'port',
    'keyword_type', 'keyword_case_type', 'keyword_value',
    'interval', 'timeout',
    'http_username', 'http_password', 'http_auth_type',
    'post_type', 'post_value', 'http_method', 'post_content_type',
    'alert_contacts', 'mwindows',
    'custom_http_headers', 'custom_http_statuses',
    'ignore_ssl_errors', 'disable_domain_expire_notifications',
}

_MONITOR_TRANSLATIONS = {
    'sub_type': MONITOR_SUB_TYPE,
    'keyword_type': KEYWORD_TYPE,
    'keyword_case_type': KEYWORD_CASE_TYPE,
    'http_auth_type': HTTP_AUTH_TYPE,
    'http_method': HTTP_METHOD,
    'post_type': POST_TYPE,
    'post_content_type': POST_CONTENT_TYPE,
    'disable_domain_expire_notifications': DISABLE_DOMAIN_EXPIRE,
}


def get_monitors(module, api_key, search=None):
    """Return the full list of monitors. Optional case-insensitive substring
    `search` against the friendly name (handled by the API).
    """
    params = {}
    if search:
        params['search'] = search
    # Ask the API to include alert_contacts and mwindows so we can diff.
    params['alert_contacts'] = 1
    params['mwindows'] = 1
    return _request(module, api_key, 'getMonitors', params, 'monitors')


def new_monitor(module, api_key, params):
    allowed = _MONITOR_COMMON_KEYS | {'type'}
    body = _filter_keys(params, allowed)
    body = _translate_keys(body, dict(_MONITOR_TRANSLATIONS, type=MONITOR_TYPE))
    return _request(module, api_key, 'newMonitor', body, 'monitor')


def edit_monitor(module, api_key, params):
    allowed = _MONITOR_COMMON_KEYS | {'id', 'status'}
    body = _filter_keys(params, allowed)
    body = _translate_keys(body, dict(_MONITOR_TRANSLATIONS, status=MONITOR_STATUS_WRITE))
    return _request(module, api_key, 'editMonitor', body, 'monitor')


def delete_monitor(module, api_key, monitor_id):
    return _request(module, api_key, 'deleteMonitor', {'id': monitor_id}, 'monitor')


# --- Per-resource API: maintenance windows ----------------------------------


_MWINDOW_TRANSLATIONS = {
    'type': MWINDOW_TYPE,
    'value': MWINDOW_DAY,
    'status': MWINDOW_STATUS,
}


def get_mwindows(module, api_key):
    return _request(module, api_key, 'getMWindows', {}, 'mwindows')


def new_mwindow(module, api_key, params):
    allowed = {'friendly_name', 'type', 'value', 'start_time', 'duration'}
    body = _filter_keys(params, allowed)
    body = _translate_keys(body, _MWINDOW_TRANSLATIONS)
    return _request(module, api_key, 'newMWindow', body, 'mwindow')


def edit_mwindow(module, api_key, params):
    allowed = {'id', 'friendly_name', 'type', 'value', 'start_time', 'duration', 'status'}
    body = _filter_keys(params, allowed)
    body = _translate_keys(body, _MWINDOW_TRANSLATIONS)
    return _request(module, api_key, 'editMWindow', body, 'mwindow')


def delete_mwindow(module, api_key, mwindow_id):
    return _request(module, api_key, 'deleteMWindow', {'id': mwindow_id}, 'mwindow')


# --- Per-resource API: public status pages (PSPs) ---------------------------


_PSP_TRANSLATIONS = {
    'sort': PSP_SORT,
    'status': PSP_STATUS,
}


def get_psps(module, api_key):
    return _request(module, api_key, 'getPSPs', {}, 'psps')


def new_psp(module, api_key, params):
    # `status` is not allowed on create per upstream; only edit_psp accepts it.
    allowed = {
        'friendly_name', 'monitors', 'custom_domain',
        'password', 'sort', 'hide_url_links',
    }
    body = _filter_keys(params, allowed)
    body = _translate_keys(body, _PSP_TRANSLATIONS)
    return _request(module, api_key, 'newPSP', body, 'psp')


def edit_psp(module, api_key, params):
    allowed = {
        'id', 'friendly_name', 'monitors', 'custom_domain',
        'password', 'sort', 'hide_url_links', 'status',
    }
    body = _filter_keys(params, allowed)
    body = _translate_keys(body, _PSP_TRANSLATIONS)
    return _request(module, api_key, 'editPSP', body, 'psp')


def delete_psp(module, api_key, psp_id):
    return _request(module, api_key, 'deletePSP', {'id': psp_id}, 'psp')


# --- Per-resource API: alert contacts ---------------------------------------


def get_alert_contacts(module, api_key):
    return _request(module, api_key, 'getAlertContacts', {}, 'alert_contacts')


def delete_alert_contact(module, api_key, contact_id):
    return _request(module, api_key, 'deleteAlertContact', {'id': contact_id}, 'alert_contact')


# --- Per-resource API: account ----------------------------------------------


def get_account_details(module, api_key):
    return _request(module, api_key, 'getAccountDetails', {}, 'account')


# --- Idempotency helpers ----------------------------------------------------


def find_by_friendly_name(items, friendly_name):
    """Return the first item whose `friendly_name` exactly equals the argument,
    or None.
    """
    for item in items:
        if item.get('friendly_name') == friendly_name:
            return item
    return None


def resolve_friendly_names(items, names, kind):
    """Resolve a list of friendly_names to a list of integer IDs.

    `items` is the full list returned by e.g. get_alert_contacts. `names` is
    the list of friendly_names supplied by the user. `kind` is a label
    (e.g. 'alert_contact') used in the error message.

    Returns a list of IDs (ints) in the order of `names`. Raises ValueError
    on the first unresolved name.
    """
    by_name = {item.get('friendly_name'): item for item in items}
    out = []
    for name in names:
        if name not in by_name:
            raise ValueError(
                '{kind} with friendly_name {name!r} not found on UptimeRobot'.format(
                    kind=kind, name=name,
                ),
            )
        out.append(int(by_name[name]['id']))
    return out


def diff_for_update(current, desired, fields):
    """Return the subset of `desired` that differs from `current` for the given
    `fields`. Used to decide whether an edit call is needed and what to send.

    Compares stringified values to side-step type mismatches (e.g. API returns
    an int, user passes a string).
    """
    out = {}
    for field in fields:
        if field not in desired:
            continue
        cur = current.get(field)
        des = desired.get(field)
        if str(cur) != str(des):
            out[field] = des
    return out
