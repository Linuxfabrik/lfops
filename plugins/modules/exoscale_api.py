#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: exoscale_api
short_description: Send one signed request to the Exoscale v2 API
version_added: "3.0.0"
description:
    - Sends a single HTTP request to the Exoscale v2 API (C(https://api-{zone}.exoscale.com/v2)) with the required C(EXO2-HMAC-SHA256) Authorization header computed on the fly from the supplied API key / secret.
    - On a mutating request (C(POST), C(PUT), C(DELETE)) the response is normally an C(operation) object describing an asynchronous job. When I(wait) is C(true) (the default), the module then polls C(/operation/{id}) until C(state) leaves C(pending), so the caller can rely on the resource actually existing (or being gone) when the task returns.
    - Idempotency is the caller's job. This is a thin transport wrapper, not a per-resource module. Use the role / playbook around it to GET the list first and skip the mutating call when the resource is already in the desired shape.
author:
    - Linuxfabrik GmbH, Zurich, Switzerland
options:
    api_key:
        description:
            - Exoscale API key (the C(EXO...) string). API keys can be managed at U(https://portal.exoscale.com/iam/api-keys).
        type: str
        required: true
    api_secret:
        description:
            - Exoscale API secret matching I(api_key).
        type: str
        required: true
    body:
        description:
            - Request body as a dictionary. The module serialises it with C(json.dumps(..., sort_keys=True, separators=(',', ':'))) and sends the resulting bytes both to the server and to the signature, so the on-wire and signed payloads match exactly.
            - Omit for C(GET) and for mutating requests that have no body.
        type: dict
        required: false
    method:
        description:
            - HTTP method to send.
        type: str
        choices: ['DELETE', 'GET', 'POST', 'PUT']
        required: true
    operation_interval:
        description:
            - Seconds to wait between two operation polls when I(wait=true).
        type: int
        required: false
        default: 2
    operation_timeout:
        description:
            - Maximum seconds to wait for an operation to finish when I(wait=true). The module fails if the operation is still C(pending) after this many seconds.
        type: int
        required: false
        default: 300
    path:
        description:
            - API path without the C(/v2) prefix (the module adds it). Examples C(/security-group), C(/instance/{id}), C(/private-network/{id}:attach).
        type: str
        required: true
    query_params:
        description:
            - Dictionary of query-string parameters. These are both appended to the URL and folded into the signature (alphabetically by name, values concatenated, names listed in C(signed-query-args=)) as the Exoscale signing scheme requires.
        type: dict
        required: false
    wait:
        description:
            - Only meaningful for mutating requests. When C(true) (the default), if the response looks like an C(operation) object the module polls C(/operation/{id}) until C(state) is no longer C(pending), then returns the final operation payload alongside the original response. Set to C(false) to return immediately with the C(pending) operation.
        type: bool
        required: false
        default: true
    zone:
        description:
            - Exoscale zone. Determines the API endpoint host (C(https://api-{zone}.exoscale.com/v2)). Examples C(ch-dk-2), C(ch-gva-2), C(de-fra-1).
        type: str
        required: true
'''

EXAMPLES = r'''
- name: 'GET /v2/security-group'
  linuxfabrik.lfops.exoscale_api:
    api_key: '{{ exoscale_vm__api_key }}'
    api_secret: '{{ exoscale_vm__api_secret }}'
    zone: 'ch-dk-2'
    method: 'GET'
    path: '/security-group'
  register: 'sg_list'
  delegate_to: 'localhost'
  become: false

- name: 'POST /v2/security-group'
  linuxfabrik.lfops.exoscale_api:
    api_key: '{{ exoscale_vm__api_key }}'
    api_secret: '{{ exoscale_vm__api_secret }}'
    zone: 'ch-dk-2'
    method: 'POST'
    path: '/security-group'
    body:
      name: 'my-vm'
  delegate_to: 'localhost'
  become: false

- name: 'GET /v2/template?visibility=public'
  linuxfabrik.lfops.exoscale_api:
    api_key: '{{ exoscale_vm__api_key }}'
    api_secret: '{{ exoscale_vm__api_secret }}'
    zone: 'ch-dk-2'
    method: 'GET'
    path: '/template'
    query_params:
      visibility: 'public'
  register: 'tpl_list'
  delegate_to: 'localhost'
  become: false
'''

RETURN = r'''
changed:
    description: C(true) for any mutating request (C(POST), C(PUT), C(DELETE)) that the server accepted; C(false) for C(GET).
    returned: always
    type: bool
check_mode_skipped:
    description: C(true) when the request was a mutation and the play was run with C(--check), so the module returned without contacting the API.
    returned: when running under C(--check) on a mutating request
    type: bool
diff:
    description:
        - For mutating requests, a unified-diff payload describing the request that would be (or was) sent. The C(before) / C(after) text contains the method, path and JSON body. Rendered by Ansible when C(--diff) is set.
        - Not emitted for C(GET).
    returned: for mutating requests
    type: dict
json:
    description: Decoded JSON body returned by the initial API call (for mutating endpoints this is the C(operation) object as first returned by Exoscale, before any polling).
    returned: success
    type: dict
operation:
    description: Final operation payload, only present for mutating requests when I(wait=true) and the initial response looked like an operation. C(operation.state) is C(success) at this point; C(operation.reference.id) typically holds the ID of the resource that was created / updated / deleted.
    returned: when the initial response was an operation and I(wait=true)
    type: dict
status:
    description: HTTP status code returned by the initial API call.
    returned: success
    type: int
'''


import json
from urllib.parse import urlencode

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.linuxfabrik.lfops.plugins.module_utils.exoscale import (
    is_operation,
    request,
    wait_for_operation,
)


def _build_diff(method, path, body, query_params):
    """Render the would-be-sent request as a diff payload.

    POST / PUT show as additions (`before` empty, `after` populated);
    DELETE shows as a removal (`before` populated, `after` empty).
    """
    summary = '{method} /v2{path}'.format(method=method, path=path)
    if query_params:
        summary += '?' + urlencode(query_params)
    if body:
        summary += '\n' + json.dumps(body, indent=2, sort_keys=True)
    summary += '\n'

    if method == 'DELETE':
        return {'before': summary, 'after': ''}
    return {'before': '', 'after': summary}


def main():
    module = AnsibleModule(
        argument_spec=dict(
            api_key=dict(type='str', required=True, no_log=True),
            api_secret=dict(type='str', required=True, no_log=True),
            body=dict(type='dict', required=False, default=None),
            method=dict(type='str', required=True, choices=['DELETE', 'GET', 'POST', 'PUT']),
            operation_interval=dict(type='int', required=False, default=2),
            operation_timeout=dict(type='int', required=False, default=300),
            path=dict(type='str', required=True),
            query_params=dict(type='dict', required=False, default=None),
            wait=dict(type='bool', required=False, default=True),
            zone=dict(type='str', required=True),
        ),
        supports_check_mode=True,
    )

    api_key = module.params['api_key']
    api_secret = module.params['api_secret']
    zone = module.params['zone']
    method = module.params['method'].upper()
    path = module.params['path']
    body = module.params['body']
    query_params = module.params['query_params']
    wait = module.params['wait']
    operation_timeout = module.params['operation_timeout']
    operation_interval = module.params['operation_interval']

    is_mutation = method != 'GET'
    diff = _build_diff(method, path, body, query_params) if is_mutation else None

    if is_mutation and module.check_mode:
        kwargs = dict(
            changed=True,
            json={},
            status=0,
            check_mode_skipped=True,
        )
        if diff is not None:
            kwargs['diff'] = diff
        module.exit_json(**kwargs)

    success, status, payload = request(
        module, api_key, api_secret, zone, method, path,
        body=body, query_params=query_params,
    )
    if not success:
        module.fail_json(msg=payload, status=status)

    result = {
        'changed': is_mutation,
        'status': status,
        'json': payload,
    }
    if diff is not None:
        result['diff'] = diff

    if is_mutation and wait and is_operation(payload):
        op_success, op_payload = wait_for_operation(
            module, api_key, api_secret, zone, payload['id'],
            timeout=operation_timeout, interval=operation_interval,
        )
        if not op_success:
            module.fail_json(msg=op_payload, status=status, json=payload)
        result['operation'] = op_payload

    module.exit_json(**result)


if __name__ == '__main__':
    main()
