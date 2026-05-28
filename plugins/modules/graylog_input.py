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
module: graylog_input
short_description: Create, update or delete a Graylog system input
version_added: 'in the next LFOps release.'
description:
    - Manages a single Graylog system input end-to-end (create, update, delete) against the Graylog REST API.
    - Identification is by I(title); the value must be unique within the Graylog instance. Re-running the task with the same I(title) updates the existing input in place and reports C(changed=true) only when one of the diffable fields actually differs.
    - The C(port) inside I(configuration) cannot be changed once an input exists; changing it in inventory would update the existing entry in place via PUT, which the Graylog API rejects. Renaming I(title) is treated as "delete the old entry and create a new one"; the module does not detect renames.
    - Supports check mode (C(--check)) and diff mode (C(--diff)).
author:
    - Linuxfabrik GmbH, Zurich, Switzerland (info (at) linuxfabrik (dot) ch)
requirements:
    - python >= 3.6
options:
    url:
        description:
            - Base URL of the Graylog HTTP interface, e.g. C(http://127.0.0.1:9000). The C(/api) prefix is appended automatically.
        type: str
        required: true
    username:
        description:
            - Username for HTTP basic authentication against the Graylog API. Typically the Graylog root user.
        type: str
        required: true
    password:
        description:
            - Password for HTTP basic authentication.
        type: str
        required: true
        no_log: true
    validate_certs:
        description:
            - Whether to verify the TLS certificate of the Graylog endpoint. Only relevant for C(https://) URLs.
        type: bool
        required: false
        default: true
    title:
        description:
            - Human-readable name of the input. Used as the idempotency key, so it must be unique on the Graylog instance.
        type: str
        required: true
    type:
        description:
            - Fully qualified Graylog input class, e.g. C(org.graylog2.inputs.gelf.udp.GELFUDPInput). Required when creating a new input.
        type: str
        required: false
    configuration:
        description:
            - Input-specific configuration, e.g. C(bind_address), C(port), C(number_worker_threads). See the Graylog API browser (C(/api-browser#?route=get-/system/inputs/types/all)) for the per-type fields. The C(port) cannot change after creation.
        type: dict
        required: false
    global:
        description:
            - Whether the input runs on every node (C(true)) or only on the node named in I(node) (C(false)).
            - Required when creating a new input.
        type: bool
        required: false
    node:
        description:
            - Node ID to bind the input to when I(global=false). Ignored when I(global=true).
        type: str
        required: false
    state:
        description:
            - C(present) creates the input when missing, updates it in place when present (modulo the immutable I(configuration.port)).
            - C(absent) deletes the input identified by I(title). When the input does not exist, the module exits with C(changed=false).
        type: str
        choices: ['absent', 'present']
        default: 'present'
'''

EXAMPLES = r'''
- name: 'Create a GELF UDP input on every node'
  linuxfabrik.lfops.graylog_input:
    url: 'http://127.0.0.1:9000'
    username: 'admin'
    password: '{{ graylog_admin_password }}'
    title: 'Gelf (12201/UDP - managed by Ansible - do not edit)'
    type: 'org.graylog2.inputs.gelf.udp.GELFUDPInput'
    configuration:
      bind_address: '0.0.0.0'
      port: 12201
      decompress_size_limit: 8388608
      number_worker_threads: 4
      override_source: ''
      recv_buffer_size: 1048576
    global: true
    state: 'present'

- name: 'Retire the legacy Syslog input'
  linuxfabrik.lfops.graylog_input:
    url: 'http://127.0.0.1:9000'
    username: 'admin'
    password: '{{ graylog_admin_password }}'
    title: 'Syslog (1514/UDP - managed by Ansible - do not edit)'
    state: 'absent'

# Preview a change without writing:
#   ansible-playbook ... --check --diff --tags graylog_server:configure_system_inputs
'''

RETURN = r'''
input:
    description:
        - On create or update, the input object as returned by Graylog. On delete, the last known state of the input. Empty dict when there was nothing to delete.
        - In check mode, a synthetic preview reflecting what the run would have written.
    type: dict
    returned: always
diff:
    description: Standard Ansible diff structure. C(before) / C(after) contain only the fields whose values actually change.
    type: dict
    returned: when changed
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.linuxfabrik.lfops.plugins.module_utils.graylog import (
    GraylogAPIError,
    GraylogClient,
    diff_changed_fields,
)


# Fields the user can set in the inventory. These are the ones we compare and
# the ones we send on POST/PUT.
_DIFF_FIELDS = ('title', 'type', 'global', 'node', 'configuration')

# Server-managed fields that come back in GET responses but are not user input.
_IGNORE_ON_DIFF = ('id', 'created_at', 'creator_user_id', 'static_fields')


def find_by_title(inputs, title):
    """Return the first input dict whose `title` matches, or None."""
    for item in inputs or []:
        if item.get('title') == title:
            return item
    return None


def _unwrap_secret(value):
    """Graylog stores secret-bearing fields like `tls_key_password` as
    `{"encrypted_value": "...", "salt": "..."}` on read, while POST/PUT bodies
    accept a plain string. When the secret is empty, unwrap the dict to `''`
    so the diff does not fire on every run.

    A non-empty `encrypted_value` is left as-is because the plain user-supplied
    value cannot be compared to the encrypted form; the module treats such
    secrets as write-once (a subsequent run will diff and re-send, which
    Graylog stores idempotently).
    """
    if (
        isinstance(value, dict)
        and set(value.keys()) == {'encrypted_value', 'salt'}
        and value.get('encrypted_value') == ''
    ):
        return ''
    return value


def normalize_current(item):
    """Reduce a GET-side input dict to the fields we diff against.

    The Graylog GET response uses `attributes` for the per-input configuration
    block, while POST/PUT bodies use `configuration`. Mirror so both sides
    compare under the same key, and unwrap Graylog's empty-secret dicts back
    to plain strings.
    """
    if not item:
        return {}
    configuration = item.get('attributes', item.get('configuration')) or {}
    configuration = {k: _unwrap_secret(v) for k, v in configuration.items()}
    return {
        'title': item.get('title'),
        'type': item.get('type'),
        'global': item.get('global'),
        'node': item.get('node'),
        'configuration': configuration,
    }


def build_desired(params):
    """Return the dict we POST/PUT, with `None`/omitted params left out."""
    desired = {}
    for field in _DIFF_FIELDS:
        value = params.get(field)
        if value is None:
            continue
        desired[field] = value
    return desired


def main():
    # `global` is a Python keyword, so we build argument_spec via a dict literal.
    argument_spec = {
        'url': {'type': 'str', 'required': True},
        'username': {'type': 'str', 'required': True},
        'password': {'type': 'str', 'required': True, 'no_log': True},
        'validate_certs': {'type': 'bool', 'default': True},
        'title': {'type': 'str', 'required': True},
        'type': {'type': 'str'},
        'configuration': {'type': 'dict'},
        'global': {'type': 'bool'},
        'node': {'type': 'str'},
        'state': {'type': 'str', 'choices': ['absent', 'present'], 'default': 'present'},
    }
    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=[
            ('state', 'present', ['type', 'configuration', 'global'], False),
        ],
        supports_check_mode=True,
    )

    client = GraylogClient(
        module,
        url=module.params['url'],
        username=module.params['username'],
        password=module.params['password'],
        validate_certs=module.params['validate_certs'],
    )
    title = module.params['title']
    state = module.params['state']

    try:
        listing = client.get('/api/system/inputs')
    except GraylogAPIError as exc:
        module.fail_json(msg=f'Could not list inputs: {exc}')

    current = find_by_title((listing or {}).get('inputs') or [], title)
    current_compare = normalize_current(current)
    desired = build_desired(module.params)

    # --- absent --------------------------------------------------------------
    if state == 'absent':
        if current is None:
            module.exit_json(changed=False, input={}, diff={'before': {}, 'after': {}})
        diff = {'before': current_compare, 'after': {}}
        if module.check_mode:
            module.exit_json(changed=True, input=current, diff=diff)
        try:
            client.delete(f"/api/system/inputs/{current['id']}", expected_status=204)
        except GraylogAPIError as exc:
            module.fail_json(msg=f'Could not delete input {title!r}: {exc}')
        module.exit_json(changed=True, input=current, diff=diff)

    # --- present, create -----------------------------------------------------
    if current is None:
        diff = {'before': {}, 'after': dict(desired)}
        if module.check_mode:
            module.exit_json(changed=True, input=desired, diff=diff)
        try:
            created = client.post('/api/system/inputs', body=desired, expected_status=201)
        except GraylogAPIError as exc:
            module.fail_json(msg=f'Could not create input {title!r}: {exc}')
        module.exit_json(changed=True, input=created or desired, diff=diff)

    # --- present, update -----------------------------------------------------
    before, after = diff_changed_fields(current_compare, desired, ignore=_IGNORE_ON_DIFF)
    if not before and not after:
        module.exit_json(changed=False, input=current, diff={'before': {}, 'after': {}})

    diff = {'before': before, 'after': after}
    if module.check_mode:
        module.exit_json(changed=True, input=current, diff=diff)

    # Graylog's InputCreateRequest builder rejects `id` in the PUT body
    # ("Unable to map property id"); the id only goes in the URL path. Index
    # sets behave the opposite way - see graylog_index_set.
    try:
        client.put(f"/api/system/inputs/{current['id']}", body=desired, expected_status=201)
    except GraylogAPIError as exc:
        module.fail_json(msg=f'Could not update input {title!r}: {exc}')

    module.exit_json(changed=True, input=current, diff=diff)


if __name__ == '__main__':
    main()
