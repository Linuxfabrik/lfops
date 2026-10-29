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
module: exoscale_private_network
short_description: Manage an Exoscale private network
version_added: '10.0.0'
description:
    - Creates or deletes an Exoscale private network in a zone, identified by I(name), using the Exoscale v2 API.
    - With I(cidr), the network is a managed one, where Exoscale hands out addresses by DHCP. The range runs from the second address of the network to the third last, which leaves room for a gateway and the broadcast address.
    - An existing network is never changed, since other instances may depend on its addressing.
    - Attaching instances is done by M(linuxfabrik.lfops.exoscale_instance).
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
    cidr:
        description:
            - IPv4 network in CIDR notation, for example C(192.0.2.0/24). Only used when the network is created.
            - Without it, the network is unmanaged, and the instances have to configure their addresses themselves.
        type: str
        required: false
    name:
        description:
            - Name of the private network. Must be unique in the zone.
        type: str
        required: true
    operation_timeout:
        description:
            - Seconds to wait for an asynchronous Exoscale operation to finish.
        type: int
        default: 600
    state:
        description:
            - C(present) creates the network if it is missing.
            - C(absent) deletes the network. Exoscale refuses this while an instance is still attached to it.
        type: str
        choices:
            - absent
            - present
        default: present
    zone:
        description:
            - Exoscale zone, for example C(ch-gva-2).
        type: str
        required: true
"""

EXAMPLES = r"""
- name: 'Create a managed private network'
  linuxfabrik.lfops.exoscale_private_network:
    api_key: '{{ exoscale_api_key }}'
    api_secret: '{{ exoscale_api_secret }}'
    zone: 'ch-gva-2'
    name: 'net-prod01'
    cidr: '192.0.2.0/24'
  delegate_to: 'localhost'
"""

RETURN = r"""
private_network:
    description: The private network as returned by the Exoscale API. Empty when C(state=absent), or when it would be created in check mode.
    returned: always
    type: dict
"""

import ipaddress

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.linuxfabrik.lfops.plugins.module_utils.exoscale import (
    COMMON_ARGUMENT_SPEC,
    ExoscaleClient,
)


def addressing(cidr):
    """Return the `start-ip`, `end-ip` and `netmask` of a managed network."""
    network = ipaddress.IPv4Network(cidr, strict=False)
    if network.num_addresses < 8:
        raise ValueError(f'{cidr} is too small for a managed private network')
    return {
        'end-ip': str(network[-3]),
        'netmask': str(network.netmask),
        'start-ip': str(network[2]),
    }


def render(network):
    lines = [f'name: {network["name"]}']
    for field in ('start-ip', 'end-ip', 'netmask'):
        if network.get(field):
            lines.append(f'{field}: {network[field]}')
    return '\n'.join(lines) + '\n'


def main():
    argument_spec = dict(
        COMMON_ARGUMENT_SPEC,
        cidr=dict(type='str'),
        name=dict(type='str', required=True),
        state=dict(type='str', choices=['absent', 'present'], default='present'),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    client = ExoscaleClient(module)
    name = module.params['name']

    network = client.find(
        '/private-network', 'private-networks', name, 'private network'
    )

    if module.params['state'] == 'absent':
        if network is None:
            module.exit_json(changed=False, private_network={})
        if not module.check_mode:
            client.mutate('DELETE', f'/private-network/{network["id"]}')
        module.exit_json(
            changed=True,
            diff={'before': render(network), 'after': ''},
            private_network={},
        )

    if network is not None:
        module.exit_json(changed=False, private_network=network)

    body = {'name': name}
    if module.params['cidr']:
        try:
            body.update(addressing(module.params['cidr']))
        except ValueError as e:
            module.fail_json(msg=f'invalid cidr: {e}')
    diff = {'before': '', 'after': render(body)}
    if module.check_mode:
        module.exit_json(changed=True, diff=diff, private_network={})

    operation = client.mutate('POST', '/private-network', body=body)
    module.exit_json(
        changed=True,
        diff=diff,
        private_network=client.get(f'/private-network/{operation["reference"]["id"]}'),
    )


if __name__ == '__main__':
    main()
