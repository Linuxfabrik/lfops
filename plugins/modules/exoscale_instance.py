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
module: exoscale_instance
short_description: Manage an Exoscale compute instance
version_added: '10.0.0'
description:
    - Creates, changes or deletes an Exoscale compute instance, identified by I(name), using the Exoscale v2 API.
    - On an existing instance, the module scales it to I(instance_type), grows its disk to I(disk_size), attaches the I(security_groups) and attaches, detaches or re-addresses the I(private_networks). Scaling and growing the disk need a stopped instance, see I(force).
    - I(template), I(ssh_keys) and I(public_ip_assignment) only take effect when the instance is created.
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
    disk_size:
        description:
            - Size of the root disk in GiB, between 10 and 51200. Required to create the instance.
            - On an existing instance, a larger value grows the disk. The disk cannot shrink, so a smaller value fails.
        type: int
        required: false
    force:
        description:
            - Allows the module to stop a running instance to scale it or to grow its disk, and to start it again afterwards.
            - Without it, the module fails instead of stopping the instance.
        type: bool
        default: false
    instance_type:
        description:
            - Instance type as C(<family>.<size>), for example C(standard.medium). Required to create the instance.
            - On an existing instance, a different type scales it. Exoscale only scales within the same family.
        type: str
        required: false
    name:
        description:
            - Name of the instance. Must be unique in the zone.
        type: str
        required: true
    operation_timeout:
        description:
            - Seconds to wait for an asynchronous Exoscale operation to finish.
        type: int
        default: 600
    private_networks:
        description:
            - Private networks to attach to or detach from the instance.
            - Attached networks that are not listed here are left alone.
        type: list
        elements: dict
        default: []
        suboptions:
            fixed_ip:
                description:
                    - IPv4 address the instance gets on a managed private network. If the instance currently has another one, it is changed.
                type: str
            name:
                description:
                    - Name of the private network. It has to exist, see M(linuxfabrik.lfops.exoscale_private_network).
                type: str
                required: true
            state:
                description:
                    - Whether the instance should be attached to the network.
                type: str
                choices:
                    - absent
                    - present
                default: present
    public_ip_assignment:
        description:
            - C(inet4) gives the instance a public IPv4 address, C(dual) a public IPv4 and IPv6 address, C(none) none at all.
            - Only used when the instance is created.
        type: str
        choices:
            - dual
            - inet4
            - none
        default: inet4
    security_groups:
        description:
            - Names of the security groups the instance is attached to. They have to exist.
            - Security groups attached to the instance that are not listed here are left alone.
        type: list
        elements: str
        default: []
    ssh_keys:
        description:
            - Names of the SSH keys registered at Exoscale to deploy to the instance. Only used when the instance is created.
        type: list
        elements: str
        default: []
        no_log: false
    state:
        description:
            - C(present) creates the instance if it is missing and leaves the power state of an existing instance alone.
            - C(started) and C(stopped) also start or stop the instance. An instance created with C(stopped) never boots.
            - C(restarted) reboots a running instance on every run and starts a stopped one.
            - C(absent) deletes the instance.
        type: str
        choices:
            - absent
            - present
            - restarted
            - started
            - stopped
        default: present
    template:
        description:
            - Name or ID of the template to create the instance from. Required to create the instance.
            - A name is looked up among the templates with I(template_visibility). Use the ID for a private template whose name is not unique.
        type: str
        required: false
    template_visibility:
        description:
            - Visibility of the templates that I(template) is looked up in. C(private) are the templates registered in the own organization.
        type: str
        choices:
            - private
            - public
        default: public
    zone:
        description:
            - Exoscale zone, for example C(ch-gva-2).
        type: str
        required: true
"""

EXAMPLES = r"""
- name: 'Create a private instance with a fixed address in a private network'
  linuxfabrik.lfops.exoscale_instance:
    api_key: '{{ exoscale_api_key }}'
    api_secret: '{{ exoscale_api_secret }}'
    zone: 'ch-gva-2'
    name: 'web01'
    instance_type: 'standard.small'
    template: 'Rocky Linux 9 (Blue Onyx) 64-bit'
    disk_size: 50
    ssh_keys:
      - 'linuxfabrik'
    public_ip_assignment: 'none'
    security_groups:
      - 'default'
      - 'web01'
    private_networks:
      - name: 'net-prod01'
        fixed_ip: '192.0.2.10'
    state: 'started'
  delegate_to: 'localhost'

- name: 'Grow the disk, stopping the instance for it'
  linuxfabrik.lfops.exoscale_instance:
    api_key: '{{ exoscale_api_key }}'
    api_secret: '{{ exoscale_api_secret }}'
    zone: 'ch-gva-2'
    name: 'web01'
    disk_size: 100
    force: true
    state: 'started'
  delegate_to: 'localhost'
"""

RETURN = r"""
instance:
    description: The instance as returned by the Exoscale API after all changes. Empty when C(state=absent), or when it would be created in check mode.
    returned: always
    type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.linuxfabrik.lfops.plugins.module_utils.exoscale import (
    COMMON_ARGUMENT_SPEC,
    UUID_RE,
    ExoscaleClient,
    find_by_name,
)


def render(view):
    """Render the managed attributes of an instance as text for `--diff`."""
    if not view:
        return ''
    lines = []
    for field in (
        'name',
        'state',
        'instance-type',
        'disk-size',
        'public-ip-assignment',
    ):
        if view.get(field) is not None:
            lines.append(f'{field}: {view[field]}')
    lines += sorted(f'security-group: {name}' for name in view['security-groups'])
    lines += sorted(
        f'private-network: {name}' + (f' ({ip})' if ip else '')
        for name, ip in view['private-networks'].items()
    )
    return '\n'.join(lines) + '\n'


class Instance:
    def __init__(self, module):
        self.module = module
        self.client = ExoscaleClient(module)
        self.params = module.params
        self.changed = False
        self._networks = None
        self._security_groups = None
        self._types = None

    def fail(self, msg):
        self.module.fail_json(msg=f'instance "{self.params["name"]}": {msg}')

    # lookups

    def instance_types(self):
        """Map each instance type ID to its `<family>.<size>` name."""
        if self._types is None:
            self._types = {
                item['id']: f'{item["family"]}.{item["size"]}'
                for item in self.client.get('/instance-type').get('instance-types', [])
            }
        return self._types

    def instance_type_id(self, name):
        wanted = name if '.' in name else f'standard.{name}'
        for type_id, type_name in self.instance_types().items():
            if type_name == wanted.lower():
                return type_id
        return self.fail(f'unknown instance type "{name}"')

    def template_id(self, name):
        if UUID_RE.match(name):
            return name
        visibility = self.params['template_visibility']
        templates = self.client.get('/template', query={'visibility': visibility})
        try:
            template = find_by_name(templates.get('templates', []), name, 'template')
        except ValueError as e:
            return self.fail(f'{e}, or use the template ID instead')
        if template is None:
            return self.fail(f'no {visibility} template is called "{name}"')
        return template['id']

    def security_groups(self):
        if self._security_groups is None:
            self._security_groups = self.client.get('/security-group').get(
                'security-groups', []
            )
        return self._security_groups

    def networks(self):
        if self._networks is None:
            self._networks = self.client.get('/private-network').get(
                'private-networks', []
            )
        return self._networks

    def resolve(self, items, name, kind):
        """Return the ID of the named item.

        In check mode, a missing item is no error, since the task that would
        create it was not run for real either. `None` stands in for its ID.
        """
        try:
            item = find_by_name(items, name, kind)
        except ValueError as e:
            return self.fail(str(e))
        if item is None and not self.module.check_mode:
            return self.fail(f'{kind} "{name}" does not exist')
        return item['id'] if item else None

    # state

    def view(self, instance):
        """Reduce an instance to the attributes this module manages."""
        sg_names = {item['id']: item['name'] for item in self.security_groups()}
        networks = {}
        for ref in instance.get('private-networks') or []:
            network = self.client.get(f'/private-network/{ref["id"]}')
            ip = next(
                (
                    lease['ip']
                    for lease in network.get('leases') or []
                    if lease.get('instance-id') == instance['id']
                ),
                None,
            )
            networks[network['name']] = ip
        instance_type = instance.get('instance-type') or {}
        return {
            'disk-size': instance.get('disk-size'),
            'instance-type': self.instance_types().get(instance_type.get('id')),
            'name': instance['name'],
            'private-networks': networks,
            'public-ip-assignment': instance.get('public-ip-assignment'),
            'security-groups': sorted(
                sg_names.get(ref['id'], ref['id'])
                for ref in instance.get('security-groups') or []
            ),
            'state': instance.get('state'),
        }

    def mutate(self, method, path, body=None):
        self.changed = True
        if self.module.check_mode:
            return None
        return self.client.mutate(method, path, body=body)

    # actions

    def create(self):
        for param in ('disk_size', 'instance_type', 'template'):
            if self.params[param] is None:
                self.fail(f'{param} is required to create the instance')
        state = self.params['state']
        body = {
            'auto-start': state != 'stopped',
            'disk-size': self.params['disk_size'],
            'instance-type': {
                'id': self.instance_type_id(self.params['instance_type'])
            },
            'name': self.params['name'],
            'public-ip-assignment': self.params['public_ip_assignment'],
            'template': {'id': self.template_id(self.params['template'])},
        }
        if self.params['ssh_keys']:
            body['ssh-keys'] = [{'name': name} for name in self.params['ssh_keys']]
        sg_ids = [
            self.resolve(self.security_groups(), name, 'security group')
            for name in self.params['security_groups']
        ]
        if sg_ids:
            body['security-groups'] = [{'id': sg_id} for sg_id in sg_ids]

        after = {
            'disk-size': self.params['disk_size'],
            'instance-type': self.params['instance_type'],
            'name': self.params['name'],
            'private-networks': {},
            'public-ip-assignment': self.params['public_ip_assignment'],
            'security-groups': sorted(self.params['security_groups']),
            'state': 'stopped' if state == 'stopped' else 'running',
        }
        operation = self.mutate('POST', '/instance', body=body)
        instance_id = operation['reference']['id'] if operation else None
        self.reconcile_networks(instance_id, {}, after)
        return after, instance_id

    def update(self, instance):
        before = self.view(instance)
        after = dict(before, **{'private-networks': dict(before['private-networks'])})
        instance_id = instance['id']

        needs_stop = []
        type_id = None
        if self.params['instance_type'] is not None:
            type_id = self.instance_type_id(self.params['instance_type'])
            if type_id != (instance.get('instance-type') or {}).get('id'):
                needs_stop.append(
                    f'scale it from {before["instance-type"]} to '
                    f'{self.params["instance_type"]}'
                )
                after['instance-type'] = self.params['instance_type']
            else:
                type_id = None
        grow_disk = False
        if self.params['disk_size'] is not None:
            current = instance.get('disk-size') or 0
            if self.params['disk_size'] < current:
                self.fail(
                    f'the disk cannot shrink from {current} GiB to '
                    f'{self.params["disk_size"]} GiB'
                )
            if self.params['disk_size'] > current:
                grow_disk = True
                needs_stop.append(
                    f'grow its disk from {current} GiB to {self.params["disk_size"]} GiB'
                )
                after['disk-size'] = self.params['disk_size']

        # refuse before changing anything else
        state = self.params['state']
        running = instance.get('state') == 'running'
        # stopping is no surprise when the instance should end up stopped
        if needs_stop and running and not self.params['force'] and state != 'stopped':
            self.fail(
                f'the instance has to be stopped to {" and ".join(needs_stop)}. '
                'Stop it, or allow stopping it with force'
            )

        # `PUT /instance/{id}` accepts `public-ip-assignment`, but the operation
        # succeeds without changing it (verified against ch-gva-2 on 2026-10-23,
        # stopped instance, inet4 -> none)
        if self.params['public_ip_assignment'] != before['public-ip-assignment']:
            self.module.warn(
                f'instance "{self.params["name"]}" has public_ip_assignment '
                f'{before["public-ip-assignment"]}, which can only be set on creation'
            )

        for name in self.params['security_groups']:
            if name in before['security-groups']:
                continue
            sg_id = self.resolve(self.security_groups(), name, 'security group')
            self.mutate(
                'PUT',
                f'/security-group/{sg_id}:attach',
                body={'instance': {'id': instance_id}},
            )
            after['security-groups'] = sorted(after['security-groups'] + [name])

        self.reconcile_networks(instance_id, before['private-networks'], after)

        stopped_here = False
        if needs_stop and running:
            self.mutate('PUT', f'/instance/{instance_id}:stop')
            running = False
            stopped_here = True
        if type_id is not None:
            self.mutate(
                'PUT',
                f'/instance/{instance_id}:scale',
                body={'instance-type': {'id': type_id}},
            )
        if grow_disk:
            self.mutate(
                'PUT',
                f'/instance/{instance_id}:resize-disk',
                body={'disk-size': self.params['disk_size']},
            )

        if state == 'stopped' and running:
            self.mutate('PUT', f'/instance/{instance_id}:stop')
            running = False
        elif state == 'restarted' and running:
            self.mutate('PUT', f'/instance/{instance_id}:reboot')
        elif not running and (
            state in ('restarted', 'started') or (state == 'present' and stopped_here)
        ):
            self.mutate('PUT', f'/instance/{instance_id}:start', body={})
            running = True
        if before['state'] in ('running', 'stopped'):
            after['state'] = 'running' if running else 'stopped'
        return before, after

    def reconcile_networks(self, instance_id, attached, after):
        """Attach, detach and re-address the private networks.

        `attached` maps the names of the attached networks to the address of
        the instance in each of them. `after` is updated to the outcome.
        """
        for item in self.params['private_networks']:
            name = item['name']
            if item['state'] == 'absent':
                if name in attached:
                    network_id = self.resolve(self.networks(), name, 'private network')
                    self.mutate(
                        'PUT',
                        f'/private-network/{network_id}:detach',
                        body={'instance': {'id': instance_id}},
                    )
                    after['private-networks'].pop(name, None)
                continue

            fixed_ip = item['fixed_ip']
            if name in attached and (not fixed_ip or attached[name] == fixed_ip):
                continue
            network_id = self.resolve(self.networks(), name, 'private network')
            body = {'instance': {'id': instance_id}}
            if fixed_ip:
                body['ip'] = fixed_ip
            action = 'update-ip' if name in attached else 'attach'
            self.mutate('PUT', f'/private-network/{network_id}:{action}', body=body)
            after['private-networks'][name] = fixed_ip or attached.get(name)

    def delete(self, instance):
        self.mutate('DELETE', f'/instance/{instance["id"]}')


def main():
    argument_spec = dict(
        COMMON_ARGUMENT_SPEC,
        disk_size=dict(type='int'),
        force=dict(type='bool', default=False),
        instance_type=dict(type='str'),
        name=dict(type='str', required=True),
        private_networks=dict(
            type='list',
            elements='dict',
            default=[],
            options=dict(
                fixed_ip=dict(type='str'),
                name=dict(type='str', required=True),
                state=dict(
                    type='str', choices=['absent', 'present'], default='present'
                ),
            ),
        ),
        public_ip_assignment=dict(
            type='str', choices=['dual', 'inet4', 'none'], default='inet4'
        ),
        security_groups=dict(type='list', elements='str', default=[]),
        ssh_keys=dict(type='list', elements='str', default=[], no_log=False),
        state=dict(
            type='str',
            choices=['absent', 'present', 'restarted', 'started', 'stopped'],
            default='present',
        ),
        template=dict(type='str'),
        template_visibility=dict(
            type='str', choices=['private', 'public'], default='public'
        ),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    manager = Instance(module)
    client = manager.client

    summary = client.find('/instance', 'instances', module.params['name'], 'instance')
    instance = client.get(f'/instance/{summary["id"]}') if summary else None

    if module.params['state'] == 'absent':
        if instance is None:
            module.exit_json(changed=False, instance={})
        before = manager.view(instance)
        manager.delete(instance)
        module.exit_json(
            changed=True, diff={'before': render(before), 'after': ''}, instance={}
        )

    if instance is None:
        before = None
        after, instance_id = manager.create()
    else:
        before, after = manager.update(instance)
        instance_id = instance['id']

    result = {}
    if instance_id and not module.check_mode:
        result = client.get(f'/instance/{instance_id}')
    elif instance is not None:
        result = instance
    module.exit_json(
        changed=manager.changed,
        diff={'before': render(before), 'after': render(after)},
        instance=result,
    )


if __name__ == '__main__':
    main()
