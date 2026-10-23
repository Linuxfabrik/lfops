#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Shared client for the Exoscale v2 API used by the linuxfabrik.lfops.exoscale_*
modules.

Every request carries an `EXO2-HMAC-SHA256` Authorization header. The signing
follows `ExoscaleV2Auth` from requests-exoscale-auth 1.1.2 (the library behind
Exoscale's own python-exoscale SDK). Mutating endpoints return an `operation`
object that is polled on `/operation/{id}` until it leaves `pending`.

Request and response shapes were taken from the OpenAPI spec bundled with
python-exoscale 0.16.4 (API version 2.0.0).
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import base64
import hashlib
import hmac
import json
import re
import time
from urllib.parse import urlencode

from ansible.module_utils.urls import fetch_url

API_URL = 'https://api-{zone}.exoscale.com/v2'

OPERATION_INTERVAL = 3
REQUEST_TIMEOUT = 60
SIGNATURE_LIFETIME = 600

UUID_RE = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    re.IGNORECASE,
)

COMMON_ARGUMENT_SPEC = dict(
    api_key=dict(type='str', required=True, no_log=True),
    api_secret=dict(type='str', required=True, no_log=True),
    operation_timeout=dict(type='int', default=600),
    zone=dict(type='str', required=True),
)


def build_auth_header(api_key, api_secret, method, path, body, query, expires):
    """Return the `EXO2-HMAC-SHA256` Authorization header for one request.

    `path` is the URL path including the `/v2` prefix, `body` the exact bytes
    sent on the wire, `query` the dict of query-string parameters.
    """
    signed_names = sorted(query) if query else []
    msg = b'\n'.join(
        [
            f'{method} {path}'.encode(),
            body or b'',
            ''.join(str(query[name]) for name in signed_names).encode('utf-8'),
            b'',  # signed headers, none at the moment
            str(expires).encode('utf-8'),
        ]
    )
    signature = base64.standard_b64encode(
        hmac.new(api_secret.encode('utf-8'), msg=msg, digestmod=hashlib.sha256).digest()
    ).decode('utf-8')

    header = f'EXO2-HMAC-SHA256 credential={api_key}'
    if signed_names:
        header += ',signed-query-args=' + ';'.join(signed_names)
    return header + f',expires={expires},signature={signature}'


def find_by_name(items, name, kind):
    """Return the single item called `name`, or `None`.

    Exoscale does not enforce unique names, so more than one hit is an error:
    acting on an arbitrary one of them would be a guess.
    """
    matches = [item for item in items if item.get('name') == name]
    if len(matches) > 1:
        raise ValueError(
            f'{len(matches)} {kind}s are called "{name}", '
            'rename them so the name is unique'
        )
    return matches[0] if matches else None


class ExoscaleClient:
    def __init__(self, module):
        self.module = module
        self.api_key = module.params['api_key']
        self.api_secret = module.params['api_secret']
        self.operation_timeout = module.params['operation_timeout']
        self.base_url = API_URL.format(zone=module.params['zone'])

    def request(self, method, path, body=None, query=None, allow_404=False):
        """Send one signed request and return the decoded JSON response.

        Fails the module on any HTTP error, except a 404 with `allow_404`,
        which returns `None`.
        """
        data = None
        if body is not None:
            data = json.dumps(body, separators=(',', ':'), sort_keys=True).encode(
                'utf-8'
            )
        url = self.base_url + path
        if query:
            url += '?' + urlencode(query)

        headers = {
            'Accept': 'application/json',
            'Authorization': build_auth_header(
                self.api_key,
                self.api_secret,
                method,
                '/v2' + path,
                data,
                query,
                int(time.time() + SIGNATURE_LIFETIME),
            ),
        }
        if data is not None:
            headers['Content-Type'] = 'application/json'

        resp, info = fetch_url(
            self.module,
            url,
            data=data,
            headers=headers,
            method=method,
            timeout=REQUEST_TIMEOUT,
        )
        status = info.get('status', -1)
        if status == 404 and allow_404:
            return None
        if not 200 <= status < 300:
            message = info.get('msg', '')
            try:
                error = json.loads(info.get('body') or '')
                message = error.get('message') or error.get('error') or message
            except (AttributeError, TypeError, ValueError):
                pass
            self.module.fail_json(
                msg=f'{method} {url} failed with HTTP {status}: {message}'
            )

        raw = resp.read() if resp is not None else b''
        try:
            return json.loads(raw.decode('utf-8')) if raw else {}
        except ValueError as e:
            self.module.fail_json(msg=f'{method} {url} returned no valid JSON: {e}')

    def get(self, path, query=None, allow_404=False):
        return self.request('GET', path, query=query, allow_404=allow_404)

    def mutate(self, method, path, body=None):
        """Send a mutating request and wait for the resulting operation."""
        operation = self.request(method, path, body=body)
        return self.wait(operation)

    def wait(self, operation):
        deadline = time.time() + self.operation_timeout
        while operation.get('state') == 'pending':
            if time.time() >= deadline:
                self.module.fail_json(
                    msg=f'operation {operation["id"]} did not finish within '
                    f'{self.operation_timeout}s'
                )
            time.sleep(OPERATION_INTERVAL)
            operation = self.get(f'/operation/{operation["id"]}')
        if operation.get('state') != 'success':
            # `failure` or `timeout`
            self.module.fail_json(
                msg=f'operation {operation.get("id")} ended with state '
                f'{operation.get("state")}: reason={operation.get("reason")}, '
                f'message={operation.get("message")}',
                operation=operation,
            )
        return operation

    def find(self, path, list_key, name, kind):
        """List a resource collection and return the item called `name`."""
        items = self.get(path).get(list_key, [])
        try:
            return find_by_name(items, name, kind)
        except ValueError as e:
            self.module.fail_json(msg=str(e))
