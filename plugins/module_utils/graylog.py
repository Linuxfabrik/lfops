#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Shared client and diff helpers for the linuxfabrik.lfops.graylog_* modules.

Wraps `ansible.module_utils.urls.fetch_url` with the headers and auth shape
Graylog expects (basic auth, `X-Requested-By`, JSON bodies). All HTTP errors
surface as `GraylogAPIError` so the modules can fail uniformly.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import base64
import json

from ansible.module_utils.urls import fetch_url


DEFAULT_HEADERS = {
    'Accept': 'application/json',
    'X-Requested-By': 'ansible-lfops',
}


class GraylogAPIError(Exception):
    """Raised on any non-2xx response from the Graylog API."""

    def __init__(self, status, url, body):
        self.status = status
        self.url = url
        self.body = body
        super().__init__(f'HTTP {status} from {url}: {body}')


class GraylogClient:
    """Thin REST client around `fetch_url`. One instance per module call."""

    def __init__(self, module, url, username, password, validate_certs=True, timeout=30):
        self._module = module
        self._base = url.rstrip('/')
        self._validate_certs = validate_certs
        self._timeout = timeout
        token = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('ascii')
        self._auth_header = f'Basic {token}'

    # --- low-level ------------------------------------------------------------

    def _request(self, method, path, body=None, expected_status=None):
        url = self._base + path
        headers = dict(DEFAULT_HEADERS)
        headers['Authorization'] = self._auth_header
        data = None
        if body is not None:
            headers['Content-Type'] = 'application/json'
            data = json.dumps(body).encode('utf-8')

        resp, info = fetch_url(
            self._module,
            url,
            data=data,
            headers=headers,
            method=method,
            timeout=self._timeout,
        )
        status = info.get('status', -1)

        if expected_status is not None:
            allowed = expected_status if isinstance(expected_status, (list, tuple, set)) else (expected_status,)
            if status not in allowed:
                raise GraylogAPIError(status, url, info.get('body') or info.get('msg') or '')
        elif status < 200 or status >= 300:
            raise GraylogAPIError(status, url, info.get('body') or info.get('msg') or '')

        if resp is None:
            return None
        raw = resp.read()
        if not raw:
            return None
        try:
            return json.loads(raw.decode('utf-8'))
        except (ValueError, AttributeError) as exc:
            raise GraylogAPIError(status, url, f'invalid JSON: {exc}')

    # --- verbs ----------------------------------------------------------------

    def get(self, path, expected_status=200):
        return self._request('GET', path, expected_status=expected_status)

    def post(self, path, body, expected_status=(200, 201)):
        return self._request('POST', path, body=body, expected_status=expected_status)

    def put(self, path, body=None, expected_status=(200, 201, 204)):
        return self._request('PUT', path, body=body, expected_status=expected_status)

    def delete(self, path, expected_status=(200, 204)):
        return self._request('DELETE', path, expected_status=expected_status)


# --- diff helpers ------------------------------------------------------------


def strip_keys(entry, keys):
    """Return a shallow copy of `entry` with the given role-only `keys` removed.

    Replaces the role's `dict2items | rejectattr | items2dict` chain.
    """
    if not entry:
        return {}
    return {k: v for k, v in entry.items() if k not in keys}


def _equal(a, b):
    """Recursive equality. Treats dicts and lists structurally; falls back to
    `==` for scalars. Used by `diff_changed_fields` so nested config dicts
    (e.g. Graylog input `configuration`, index-set `data_tiering`) compare
    correctly.
    """
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a.keys()) != set(b.keys()):
            return False
        return all(_equal(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False
        return all(_equal(x, y) for x, y in zip(a, b))
    return a == b


def diff_changed_fields(current, desired, ignore=None):
    """Return `(before, after)` containing only the keys whose values differ.

    Keys present in `desired` are checked against `current`; keys not in
    `desired` are not compared (we never want to "unset" a field the user
    did not mention). Keys listed in `ignore` are skipped entirely. Suitable
    for an Ansible `result["diff"]` payload that highlights just the user-
    visible delta on update.
    """
    if ignore is None:
        ignore = ()
    before = {}
    after = {}
    current = current or {}
    for key, desired_value in (desired or {}).items():
        if key in ignore:
            continue
        current_value = current.get(key)
        if not _equal(current_value, desired_value):
            before[key] = current_value
            after[key] = desired_value
    return before, after
