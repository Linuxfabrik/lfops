#!/usr/bin/python
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: exoscale_security_group
short_description: Manage an Exoscale security group and its rules
version_added: '10.0.0'
description:
    - Creates or deletes an Exoscale security group, identified by I(name), and adds or removes the listed rules, using the Exoscale v2 API.
    - Rules that exist on the security group but are not listed in I(rules) are left alone. Remove a rule by listing it with C(state=absent).
    - Supports C(--check) and C(--diff).
author:
    - Linuxfabrik GmbH, Zurich, Switzerland (info (at) linuxfabrik (dot) ch)
options:
    api_key:
        description:
            - Exoscale API key.
        type: str
        required: true
    api_secret:
        description:
            - Exoscale API secret matching I(api_key).
        type: str
        required: true
    name:
        description:
            - Name of the security group. Must be unique in the organization.
        type: str
        required: true
    operation_timeout:
        description:
            - Seconds to wait for an asynchronous Exoscale operation to finish.
        type: int
        default: 600
    rules:
        description:
            - Rules to add to or remove from the security group.
            - A rule is identified by all of its subkeys except I(state).
        type: list
        elements: dict
        default: []
        suboptions:
            cidr:
                description:
                    - Network the rule applies to, in CIDR notation.
                type: str
                default: '0.0.0.0/0'
                aliases:
                    - network
            end_port:
                description:
                    - Last port of the range. Only for C(tcp) and C(udp).
                type: int
            icmp_code:
                description:
                    - ICMP code. Only for C(icmp) and C(icmpv6). C(-1) matches any code.
                type: int
                default: -1
            icmp_type:
                description:
                    - ICMP type. Only for C(icmp) and C(icmpv6). C(-1) matches any type.
                type: int
                default: -1
            protocol:
                description:
                    - Network protocol.
                type: str
                required: true
                choices:
                    - ah
                    - all
                    - esp
                    - gre
                    - icmp
                    - icmpv6
                    - ipip
                    - tcp
                    - udp
            start_port:
                description:
                    - First port of the range. Only for C(tcp) and C(udp).
                type: int
            state:
                description:
                    - Whether the rule should exist.
                type: str
                choices:
                    - absent
                    - present
                default: present
            type:
                description:
                    - Direction of the traffic.
                type: str
                choices:
                    - egress
                    - ingress
                default: ingress
                aliases:
                    - flow_direction
    state:
        description:
            - C(present) creates the security group if it is missing and applies I(rules).
            - C(absent) deletes the security group. Exoscale refuses this while an instance is still attached to it.
        type: str
        choices:
            - absent
            - present
        default: present
    zone:
        description:
            - Exoscale zone, for example C(ch-gva-2). Selects the API endpoint. Security groups themselves are global.
        type: str
        required: true
"""

EXAMPLES = r"""
- name: 'Allow SSH and ping to the instance'
  linuxfabrik.lfops.exoscale_security_group:
    api_key: '{{ exoscale_api_key }}'
    api_secret: '{{ exoscale_api_secret }}'
    zone: 'ch-gva-2'
    name: 'web01'
    rules:
      - protocol: 'tcp'
        start_port: 22
        end_port: 22
        cidr: '192.0.2.0/24'
      - protocol: 'icmp'
        icmp_type: 8
        icmp_code: 0
      - protocol: 'tcp'
        start_port: 23
        end_port: 23
        state: 'absent'
  delegate_to: 'localhost'
"""

RETURN = r"""
security_group:
    description: The security group as returned by the Exoscale API after all changes, including its C(rules). Empty when C(state=absent).
    returned: always
    type: dict
"""

import ipaddress

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.linuxfabrik.lfops.plugins.module_utils.exoscale import (
    COMMON_ARGUMENT_SPEC,
    ExoscaleClient,
)

ICMP_PROTOCOLS = ('icmp', 'icmpv6')
PORT_PROTOCOLS = ('tcp', 'udp')


def normalize_network(network):
    # the API may print a network differently from the inventory, e.g. for
    # host bits set (`192.0.2.1/24`) or IPv6 zero compression
    return ipaddress.ip_network(network, strict=False).compressed


def rule_key(direction, protocol, network, start_port, end_port, icmp_type, icmp_code):
    """Reduce a rule to the tuple that identifies it.

    Ports only count for TCP and UDP and ICMP type and code only for ICMP, so
    a value the API ignores for a protocol cannot make two equal rules differ.
    """
    if protocol not in PORT_PROTOCOLS:
        start_port = end_port = None
    if protocol in ICMP_PROTOCOLS:
        icmp_type = -1 if icmp_type is None else icmp_type
        icmp_code = -1 if icmp_code is None else icmp_code
    else:
        icmp_type = icmp_code = None
    return (
        direction,
        protocol,
        normalize_network(network) if network else None,
        start_port,
        end_port,
        icmp_type,
        icmp_code,
    )


def key_from_api(rule):
    icmp = rule.get('icmp') or {}
    return rule_key(
        rule.get('flow-direction'),
        rule.get('protocol'),
        rule.get('network'),
        rule.get('start-port'),
        rule.get('end-port'),
        icmp.get('type'),
        icmp.get('code'),
    )


def key_from_param(rule):
    return rule_key(
        rule['type'],
        rule['protocol'],
        rule['cidr'],
        rule['start_port'],
        rule['end_port'],
        rule['icmp_type'],
        rule['icmp_code'],
    )


def body_from_key(key):
    direction, protocol, network, start_port, end_port, icmp_type, icmp_code = key
    body = {'flow-direction': direction, 'network': network, 'protocol': protocol}
    if protocol in PORT_PROTOCOLS:
        if start_port is not None:
            body['start-port'] = start_port
        if end_port is not None:
            body['end-port'] = end_port
    if protocol in ICMP_PROTOCOLS:
        body['icmp'] = {'code': icmp_code, 'type': icmp_type}
    return body


def format_key(key):
    """Render a rule key as one line for `--diff`."""
    direction, protocol, network, start_port, end_port, icmp_type, icmp_code = key
    line = f'{direction} {protocol} {network or "(security group source)"}'
    if start_port is not None or end_port is not None:
        line += f' port {start_port}-{end_port}'
    if icmp_type is not None:
        line += f' type {icmp_type} code {icmp_code}'
    return line


def render(name, keys):
    lines = [f'name: {name}', *sorted(f'rule: {format_key(key)}' for key in keys)]
    return '\n'.join(lines) + '\n'


def main():
    argument_spec = dict(
        COMMON_ARGUMENT_SPEC,
        name=dict(type='str', required=True),
        rules=dict(
            type='list',
            elements='dict',
            default=[],
            options=dict(
                cidr=dict(type='str', default='0.0.0.0/0', aliases=['network']),
                end_port=dict(type='int'),
                icmp_code=dict(type='int', default=-1),
                icmp_type=dict(type='int', default=-1),
                protocol=dict(
                    type='str',
                    required=True,
                    choices=[
                        'ah',
                        'all',
                        'esp',
                        'gre',
                        'icmp',
                        'icmpv6',
                        'ipip',
                        'tcp',
                        'udp',
                    ],
                ),
                start_port=dict(type='int'),
                state=dict(
                    type='str', choices=['absent', 'present'], default='present'
                ),
                type=dict(
                    type='str',
                    choices=['egress', 'ingress'],
                    default='ingress',
                    aliases=['flow_direction'],
                ),
            ),
        ),
        state=dict(type='str', choices=['absent', 'present'], default='present'),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    client = ExoscaleClient(module)
    name = module.params['name']

    try:
        wanted = [
            (key_from_param(rule), rule['state']) for rule in module.params['rules']
        ]
    except ValueError as e:
        module.fail_json(msg=f'invalid cidr in rules: {e}')

    summary = client.find('/security-group', 'security-groups', name, 'security group')
    group = client.get(f'/security-group/{summary["id"]}') if summary else None
    current = {
        key_from_api(rule): rule['id'] for rule in (group or {}).get('rules', [])
    }

    if module.params['state'] == 'absent':
        if group is None:
            module.exit_json(changed=False, security_group={})
        if not module.check_mode:
            client.mutate('DELETE', f'/security-group/{group["id"]}')
        module.exit_json(
            changed=True,
            diff={'before': render(name, current), 'after': ''},
            security_group={},
        )

    to_add = []
    to_delete = []
    for key, state in wanted:
        if state == 'present' and key not in current and key not in to_add:
            to_add.append(key)
        if state == 'absent' and key in current and key not in to_delete:
            to_delete.append(key)

    changed = group is None or bool(to_add) or bool(to_delete)
    after = (set(current) | set(to_add)) - set(to_delete)
    diff = {
        'before': render(name, current) if group is not None else '',
        'after': render(name, after),
    }
    if not changed or module.check_mode:
        module.exit_json(changed=changed, diff=diff, security_group=group or {})

    if group is None:
        body = {'name': name}
        operation = client.mutate('POST', '/security-group', body=body)
        group_id = operation['reference']['id']
    else:
        group_id = group['id']

    for key in to_delete:
        client.mutate('DELETE', f'/security-group/{group_id}/rules/{current[key]}')
    for key in to_add:
        client.mutate(
            'POST', f'/security-group/{group_id}/rules', body=body_from_key(key)
        )

    module.exit_json(
        changed=True,
        diff=diff,
        security_group=client.get(f'/security-group/{group_id}'),
    )


if __name__ == '__main__':
    main()
