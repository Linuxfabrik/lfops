#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

"""Shared client for the Exoscale v2 API used by the linuxfabrik.lfops.exoscale_*
modules.

The Exoscale v2 API requires every request to carry an `Authorization` header
of the form

    EXO2-HMAC-SHA256 credential=<key>[,signed-query-args=<p1;p2>],expires=<ts>,signature=<sig>

where `<sig>` is the base64-encoded HMAC-SHA256 of a multi-line message
composed of method+path, body, sorted query-string values, signed headers
(none today), and the expiration timestamp. Mutating endpoints
(POST/PUT/DELETE) return an `operation` object that has to be polled on
`/operation/{id}` until `state` flips from `pending` to `success` or
`failure`. Both pieces of behaviour live here so individual modules only deal
with the resource shape, not transport.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import base64
import hashlib
import hmac
import json
import time
from urllib.parse import urlencode

from ansible.module_utils.urls import fetch_url


API_BASE_TEMPLATE = 'https://api-{zone}.exoscale.com/v2'

DEFAULT_REQUEST_TIMEOUT = 60
DEFAULT_SIGNATURE_LIFETIME = 600
DEFAULT_OPERATION_TIMEOUT = 300
DEFAULT_OPERATION_INTERVAL = 2


def build_auth_header(api_key, api_secret, method, sign_path, body=b'',
                      query_params=None, expires_in=DEFAULT_SIGNATURE_LIFETIME):
    """Return the EXO2-HMAC-SHA256 Authorization header for one request.

    `sign_path` is the URL path including the `/v2` prefix (e.g.
    `/v2/security-group`); `body` is the exact request body bytes that will be
    sent on the wire (so the signature stays aligned with what the server
    receives); `query_params` is the dict of query-string parameters that will
    be appended to the URL.
    """
    expires_ts = int(time.time() + expires_in)

    if body is None:
        body_bytes = b''
    elif isinstance(body, (bytes, bytearray)):
        body_bytes = bytes(body)
    else:
        body_bytes = body.encode('utf-8')

    msg_parts = [
        '{method} {path}'.format(method=method.upper(), path=sign_path).encode('utf-8'),
        body_bytes,
        b'',
        b'',
        str(expires_ts).encode('utf-8'),
    ]

    signed_names = []
    if query_params:
        signed_names = sorted(query_params)
        msg_parts[2] = ''.join(
            str(query_params[name]) for name in signed_names
        ).encode('utf-8')

    msg = b'\n'.join(msg_parts)
    signature = base64.standard_b64encode(
        hmac.new(api_secret.encode('utf-8'), msg=msg, digestmod=hashlib.sha256).digest(),
    ).decode('utf-8')

    header = 'EXO2-HMAC-SHA256 credential={key}'.format(key=api_key)
    if signed_names:
        header += ',signed-query-args=' + ';'.join(signed_names)
    header += ',expires={ts},signature={sig}'.format(ts=expires_ts, sig=signature)
    return header


def request(module, api_key, api_secret, zone, method, path,
            body=None, query_params=None, timeout=DEFAULT_REQUEST_TIMEOUT):
    """Send one signed request to the Exoscale v2 API.

    Returns a tuple `(success, status, payload)`. On success `payload` is the
    decoded JSON response; on failure `payload` is a human-readable error
    string and `status` carries the HTTP status (or -1 if the request did not
    reach the server).
    """
    method = method.upper()
    base_url = API_BASE_TEMPLATE.format(zone=zone)
    sign_path = '/v2' + path

    if body is None:
        body_bytes = None
        signed_body = b''
    else:
        body_bytes = json.dumps(body, separators=(',', ':'), sort_keys=True).encode('utf-8')
        signed_body = body_bytes

    url = base_url + path
    if query_params:
        url += '?' + urlencode(query_params)

    headers = {
        'Accept': 'application/json',
        'Authorization': build_auth_header(
            api_key, api_secret, method, sign_path, signed_body, query_params,
        ),
    }
    if body_bytes is not None:
        headers['Content-Type'] = 'application/json'

    resp, info = fetch_url(
        module,
        url,
        data=body_bytes,
        headers=headers,
        method=method,
        timeout=timeout,
    )
    status = info.get('status', -1)

    if status < 200 or status >= 300:
        api_msg = info.get('msg') or ''
        body_payload = info.get('body')
        if body_payload:
            try:
                err = json.loads(body_payload)
                api_msg = err.get('message') or err.get('error') or api_msg or body_payload
            except (TypeError, ValueError):
                api_msg = api_msg or body_payload
        return False, status, 'HTTP {status} from {method} {url}: {msg}'.format(
            status=status, method=method, url=url, msg=api_msg,
        )

    try:
        raw = resp.read() if resp is not None else b''
        payload = json.loads(raw.decode('utf-8')) if raw else {}
    except (AttributeError, UnicodeDecodeError, ValueError) as exc:
        return False, status, 'cannot decode JSON response from {url}: {exc}'.format(
            url=url, exc=exc,
        )

    return True, status, payload


def is_operation(payload):
    """Heuristic: does this payload look like an Exoscale `operation` object?"""
    return (
        isinstance(payload, dict)
        and 'id' in payload
        and 'state' in payload
        and payload.get('state') in ('pending', 'success', 'failure')
    )


def wait_for_operation(module, api_key, api_secret, zone, operation_id,
                       timeout=DEFAULT_OPERATION_TIMEOUT,
                       interval=DEFAULT_OPERATION_INTERVAL):
    """Poll `/operation/{id}` until `state` is no longer `pending`.

    Returns `(success, payload_or_error)`. `success=True` means the operation
    finished with `state=success`; otherwise `payload_or_error` is a string
    describing why (timeout, API error, or `state=failure`).
    """
    deadline = time.time() + timeout
    while True:
        success, _status, payload = request(
            module, api_key, api_secret, zone, 'GET',
            '/operation/' + operation_id,
        )
        if not success:
            return False, payload

        state = payload.get('state')
        if state == 'success':
            return True, payload
        if state == 'failure':
            return False, 'operation {oid} failed: reason={reason} message={message}'.format(
                oid=operation_id,
                reason=payload.get('reason'),
                message=payload.get('message'),
            )
        if time.time() >= deadline:
            return False, (
                'operation {oid} did not finish within {timeout}s '
                '(last state={state})'
            ).format(oid=operation_id, timeout=timeout, state=state)
        time.sleep(interval)
