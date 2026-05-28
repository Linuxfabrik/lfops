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
module: graylog_index_set
short_description: Create, update or delete a Graylog index set
version_added: 'in the next LFOps release.'
description:
    - Manages a single Graylog index set end-to-end (create, update, delete, set-as-default) against the Graylog REST API.
    - Identification is by I(index_prefix); the value must be unique within the Graylog instance. Re-running the task with the same I(index_prefix) updates the existing index set in place and reports C(changed=true) only when one of the diffable fields actually differs.
    - I(index_prefix) is immutable after creation; changing it in inventory produces a new index set rather than renaming the existing one.
    - When I(default=true), the module additionally calls C(PUT /api/system/indices/index_sets/{id}/default) after a successful create/update. The default flag itself does not need to be sent to the create/update endpoint and is only used by this module to drive the extra call.
    - Supports check mode (C(--check)) and diff mode (C(--diff)).
author:
    - Linuxfabrik GmbH, Zurich, Switzerland (info (at) linuxfabrik (dot) ch)
requirements:
    - python >= 3.6
options:
    url:
        description: Base URL of the Graylog HTTP interface, e.g. C(http://127.0.0.1:9000). The C(/api) prefix is appended automatically.
        type: str
        required: true
    username:
        description: Username for HTTP basic authentication against the Graylog API.
        type: str
        required: true
    password:
        description: Password for HTTP basic authentication.
        type: str
        required: true
        no_log: true
    validate_certs:
        description: Whether to verify the TLS certificate of the Graylog endpoint.
        type: bool
        required: false
        default: true
    index_prefix:
        description: Unique prefix used in indices belonging to this index set. Identity key for create/update/delete.
        type: str
        required: true
    title:
        description: Human-readable name of the index set. Required on create.
        type: str
        required: false
    description:
        description: Free-text description.
        type: str
        required: false
    shards:
        description: Number of shards per index. Required on create.
        type: int
        required: false
    replicas:
        description: Number of replicas per index. Required on create.
        type: int
        required: false
    writable:
        description: Whether this index set is writable.
        type: bool
        required: false
    index_analyzer:
        description: Elasticsearch / OpenSearch analyzer. Required on create.
        type: str
        required: false
    index_optimization_disabled:
        description: Whether to skip force-merge after rotation.
        type: bool
        required: false
    index_optimization_max_num_segments:
        description: Maximum number of segments per index after optimization.
        type: int
        required: false
    field_type_refresh_interval:
        description: Field-type refresh interval in milliseconds.
        type: int
        required: false
    use_legacy_rotation:
        description: C(false) (recommended) uses the I(data_tiering) field. C(true) falls back to the legacy I(rotation_strategy) / I(retention_strategy) configuration, which Graylog has announced will be deprecated.
        type: bool
        required: false
        default: false
    data_tiering:
        description: Data-tiering configuration. Mandatory when I(use_legacy_rotation=false).
        type: dict
        required: false
    rotation_strategy:
        description: Legacy rotation strategy configuration. Mandatory when I(use_legacy_rotation=true).
        type: dict
        required: false
    rotation_strategy_class:
        description: Legacy rotation strategy class. Mandatory when I(use_legacy_rotation=true).
        type: str
        required: false
    retention_strategy:
        description: Legacy retention strategy configuration. Mandatory when I(use_legacy_rotation=true).
        type: dict
        required: false
    retention_strategy_class:
        description: Legacy retention strategy class. Mandatory when I(use_legacy_rotation=true).
        type: str
        required: false
    default:
        description: When C(true), also set this index set as the Graylog default after create/update. Exactly one index set should be marked as default across the inventory.
        type: bool
        required: false
        default: false
    state:
        description:
            - C(present) creates the index set when missing, updates it in place when present.
            - C(absent) deletes the index set identified by I(index_prefix). When the index set does not exist, the module exits with C(changed=false).
        type: str
        choices: ['absent', 'present']
        default: 'present'
'''

EXAMPLES = r'''
- name: 'Create the default catch-all index set'
  linuxfabrik.lfops.graylog_index_set:
    url: 'http://127.0.0.1:9000'
    username: 'admin'
    password: '{{ graylog_admin_password }}'
    title: 'Default'
    description: 'Default catch-all index set; 25-30 days - managed by Ansible - do not edit'
    index_prefix: 'default'
    shards: 1
    replicas: 0
    writable: true
    index_analyzer: 'standard'
    index_optimization_disabled: false
    index_optimization_max_num_segments: 1
    field_type_refresh_interval: 5000
    use_legacy_rotation: false
    data_tiering:
      type: 'hot_only'
      index_lifetime_min: 'P25D'
      index_lifetime_max: 'P30D'
    default: true
    state: 'present'

- name: 'Drop the access index set'
  linuxfabrik.lfops.graylog_index_set:
    url: 'http://127.0.0.1:9000'
    username: 'admin'
    password: '{{ graylog_admin_password }}'
    index_prefix: 'access'
    state: 'absent'

# Preview a change without writing:
#   ansible-playbook ... --check --diff --tags graylog_server:configure_system_index_sets
'''

RETURN = r'''
index_set:
    description:
        - On create or update, the index-set object as returned by Graylog. On delete, the last known state of the index set. Empty dict when there was nothing to delete.
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


# Fields the user can set in the inventory.
_DIFF_FIELDS = (
    'title',
    'description',
    'index_prefix',
    'shards',
    'replicas',
    'writable',
    'index_analyzer',
    'index_optimization_disabled',
    'index_optimization_max_num_segments',
    'field_type_refresh_interval',
    'use_legacy_rotation',
    'data_tiering',
    'rotation_strategy',
    'rotation_strategy_class',
    'retention_strategy',
    'retention_strategy_class',
)

# Server-managed / read-only fields that come back in GET responses but are
# not user input.
_IGNORE_ON_DIFF = (
    'id',
    'creation_date',
    'can_be_default',
    'index_template_type',
    'field_restrictions',
    'field_type_profile',
    'default',
)


def find_by_prefix(index_sets, prefix):
    """Return the first index-set dict whose `index_prefix` matches, or None."""
    for item in index_sets or []:
        if item.get('index_prefix') == prefix:
            return item
    return None


def normalize_current(item):
    """Reduce a GET-side index-set dict to the fields we diff against."""
    if not item:
        return {}
    return {field: item.get(field) for field in _DIFF_FIELDS}


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
    argument_spec = {
        'url': {'type': 'str', 'required': True},
        'username': {'type': 'str', 'required': True},
        'password': {'type': 'str', 'required': True, 'no_log': True},
        'validate_certs': {'type': 'bool', 'default': True},
        'index_prefix': {'type': 'str', 'required': True},
        'title': {'type': 'str'},
        'description': {'type': 'str'},
        'shards': {'type': 'int'},
        'replicas': {'type': 'int'},
        'writable': {'type': 'bool'},
        'index_analyzer': {'type': 'str'},
        'index_optimization_disabled': {'type': 'bool'},
        'index_optimization_max_num_segments': {'type': 'int'},
        'field_type_refresh_interval': {'type': 'int'},
        'use_legacy_rotation': {'type': 'bool', 'default': False},
        'data_tiering': {'type': 'dict'},
        'rotation_strategy': {'type': 'dict'},
        'rotation_strategy_class': {'type': 'str'},
        'retention_strategy': {'type': 'dict'},
        'retention_strategy_class': {'type': 'str'},
        'default': {'type': 'bool', 'default': False},
        'state': {'type': 'str', 'choices': ['absent', 'present'], 'default': 'present'},
    }
    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=[
            (
                'state', 'present',
                ['title', 'description', 'shards', 'replicas', 'writable',
                 'index_analyzer', 'index_optimization_disabled',
                 'index_optimization_max_num_segments',
                 'field_type_refresh_interval'],
                False,
            ),
        ],
        supports_check_mode=True,
    )

    state = module.params['state']
    if state == 'present':
        if module.params['use_legacy_rotation']:
            missing = [
                k for k in ('rotation_strategy', 'rotation_strategy_class',
                            'retention_strategy', 'retention_strategy_class')
                if module.params.get(k) is None
            ]
            if missing:
                module.fail_json(
                    msg=f'use_legacy_rotation=true requires: {", ".join(missing)}',
                )
        else:
            if module.params.get('data_tiering') is None:
                module.fail_json(
                    msg='use_legacy_rotation=false (the default) requires `data_tiering`.',
                )

    client = GraylogClient(
        module,
        url=module.params['url'],
        username=module.params['username'],
        password=module.params['password'],
        validate_certs=module.params['validate_certs'],
    )
    prefix = module.params['index_prefix']
    set_default = module.params['default']

    try:
        listing = client.get('/api/system/indices/index_sets')
    except GraylogAPIError as exc:
        module.fail_json(msg=f'Could not list index sets: {exc}')

    current = find_by_prefix((listing or {}).get('index_sets') or [], prefix)
    current_compare = normalize_current(current)
    desired = build_desired(module.params)

    # --- absent --------------------------------------------------------------
    if state == 'absent':
        if current is None:
            module.exit_json(changed=False, index_set={}, diff={'before': {}, 'after': {}})
        diff = {'before': current_compare, 'after': {}}
        if module.check_mode:
            module.exit_json(changed=True, index_set=current, diff=diff)
        try:
            client.delete(f"/api/system/indices/index_sets/{current['id']}", expected_status=204)
        except GraylogAPIError as exc:
            module.fail_json(msg=f'Could not delete index set {prefix!r}: {exc}')
        module.exit_json(changed=True, index_set=current, diff=diff)

    # --- present, create -----------------------------------------------------
    if current is None:
        diff = {'before': {}, 'after': dict(desired)}
        if set_default:
            diff['after']['default'] = True
        if module.check_mode:
            module.exit_json(changed=True, index_set=desired, diff=diff)
        try:
            created = client.post('/api/system/indices/index_sets', body=desired, expected_status=200)
        except GraylogAPIError as exc:
            module.fail_json(msg=f'Could not create index set {prefix!r}: {exc}')
        if set_default and created and created.get('id'):
            try:
                client.put(f"/api/system/indices/index_sets/{created['id']}/default", expected_status=200)
            except GraylogAPIError as exc:
                module.fail_json(msg=f'Created {prefix!r} but failed to set it as default: {exc}')
        module.exit_json(changed=True, index_set=created or desired, diff=diff)

    # --- present, update -----------------------------------------------------
    before, after = diff_changed_fields(current_compare, desired, ignore=_IGNORE_ON_DIFF)
    # Track default-flip separately: GET returns `default: true|false`, the
    # write endpoint does not accept it, so compare here and drive an extra
    # PUT below if needed.
    default_now = bool(current.get('default'))
    default_change = set_default != default_now if set_default else False
    if default_change:
        before['default'] = default_now
        after['default'] = True

    if not before and not after:
        module.exit_json(changed=False, index_set=current, diff={'before': {}, 'after': {}})

    diff = {'before': before, 'after': after}
    if module.check_mode:
        module.exit_json(changed=True, index_set=current, diff=diff)

    # Only PUT if non-default fields actually changed (i.e. anything other
    # than the `default` flip, which is its own endpoint).
    field_changes = {k: v for k, v in after.items() if k != 'default'}
    if field_changes:
        body = dict(desired)
        body['id'] = current['id']
        try:
            client.put(f"/api/system/indices/index_sets/{current['id']}", body=body, expected_status=200)
        except GraylogAPIError as exc:
            module.fail_json(msg=f'Updating index set {prefix!r} failed: {exc}')

    if default_change:
        try:
            client.put(f"/api/system/indices/index_sets/{current['id']}/default", expected_status=200)
        except GraylogAPIError as exc:
            module.fail_json(msg=f'Could not set index set {prefix!r} as default: {exc}')

    module.exit_json(changed=True, index_set=current, diff=diff)


if __name__ == '__main__':
    main()
