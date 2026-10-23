#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""In-memory fake of the Exoscale v2 API for the exoscale_* module tests.

It replaces `fetch_url` in the exoscale module_util, which is the only place
that talks HTTP, so request signing, error handling and operation polling run
for real. The response shapes follow the OpenAPI spec bundled with
python-exoscale 0.16.4. Every mutating call answers with a `pending`
operation, which turns `success` on the first poll, and is recorded in
`calls`, so tests can assert which writes were issued.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import io
import json
import re
import unittest.mock
from urllib.parse import urlparse

import ansible_harness
from ansible_collections.linuxfabrik.lfops.plugins.module_utils import exoscale

API_KEY = 'EXOlinuxfabrik'
API_SECRET = 'linuxfabrik'
ZONE = 'ch-gva-2'

COMMON_ARGS = {'api_key': API_KEY, 'api_secret': API_SECRET, 'zone': ZONE}

TYPES = {
    'type-standard-small': ('standard', 'small'),
    'type-standard-tiny': ('standard', 'tiny'),
    'type-memory-large': ('memory', 'large'),
}
TEMPLATE_ID = '11111111-2222-3333-4444-555555555555'
TEMPLATE_NAME = 'Rocky Linux 9 (Blue Onyx) 64-bit'


class FakeExoscale:
    def __init__(self):
        self.instances = {}
        self.networks = {}
        self.security_groups = {}
        self.operations = {}
        self.calls = []
        # (method, path) -> (status, message)
        self.failures = {}
        self._next_id = 0
        self.add_security_group('default')

    def new_id(self, prefix):
        self._next_id += 1
        return f'{prefix}-{self._next_id}'

    # fixtures

    def add_security_group(self, name, rules=None):
        sg_id = self.new_id('sg')
        self.security_groups[sg_id] = {
            'id': sg_id,
            'name': name,
            'rules': [dict(rule, id=self.new_id('rule')) for rule in rules or []],
        }
        return sg_id

    def add_network(self, name, **fields):
        network_id = self.new_id('net')
        self.networks[network_id] = dict(fields, id=network_id, name=name, leases=[])
        return network_id

    def add_instance(
        self, name, state='running', type_id='type-standard-tiny', **fields
    ):
        instance_id = self.new_id('instance')
        self.instances[instance_id] = dict(
            {
                'disk-size': 10,
                'public-ip-assignment': 'none',
                'security-groups': [{'id': self.find('security_groups', 'default')}],
            },
            **fields,
            id=instance_id,
            name=name,
            state=state,
        )
        self.instances[instance_id]['instance-type'] = {'id': type_id}
        return instance_id

    def attach(self, network_id, instance_id, ip=None):
        self.networks[network_id]['leases'].append(
            {'instance-id': instance_id, 'ip': ip}
        )

    def find(self, collection, name):
        for item_id, item in getattr(self, collection).items():
            if item['name'] == name:
                return item_id
        return None

    def writes(self):
        return [(method, path) for method, path, _body in self.calls if method != 'GET']

    # transport

    def fetch_url(self, module, url, data=None, headers=None, method=None, **_kwargs):
        assert headers['Authorization'].startswith(
            f'EXO2-HMAC-SHA256 credential={API_KEY},'
        )
        parsed = urlparse(url)
        assert parsed.netloc == f'api-{ZONE}.exoscale.com'
        path = parsed.path[len('/v2') :]
        body = json.loads(data.decode('utf-8')) if data else None
        self.calls.append((method, path, body))

        if (method, path) in self.failures:
            status, message = self.failures[(method, path)]
            return None, {
                'status': status,
                'msg': f'HTTP Error {status}',
                'body': json.dumps({'message': message}),
            }
        payload = self.dispatch(method, path, body)
        if payload is None:
            return None, {'status': 404, 'msg': 'Not Found', 'body': ''}
        return io.BytesIO(json.dumps(payload).encode('utf-8')), {'status': 200}

    def operation(self, reference_id):
        op_id = self.new_id('op')
        self.operations[op_id] = {
            'id': op_id,
            'reference': {'id': reference_id},
            'state': 'success',
        }
        return {'id': op_id, 'reference': {'id': reference_id}, 'state': 'pending'}

    def dispatch(self, method, path, body):
        match = re.match(
            r'^/([a-z-]+)(?:/([^/:]+))?(?::([a-z-]+))?(?:/rules(?:/(.+))?)?$', path
        )
        if not match:
            return None
        kind, item_id, action, rule_id = match.groups()
        is_rules = '/rules' in path

        if kind == 'operation':
            return self.operations.get(item_id)
        if kind == 'instance-type':
            return {
                'instance-types': [
                    {'family': family, 'id': type_id, 'size': size}
                    for type_id, (family, size) in TYPES.items()
                ]
            }
        if kind == 'template':
            return {'templates': [{'id': TEMPLATE_ID, 'name': TEMPLATE_NAME}]}

        if kind == 'security-group':
            if method == 'GET' and item_id is None:
                return {'security-groups': list(self.security_groups.values())}
            if method == 'POST' and item_id is None:
                return self.operation(self.add_security_group(body['name']))
            group = self.security_groups.get(item_id)
            if group is None:
                return None
            if method == 'GET':
                return group
            if method == 'DELETE' and not is_rules:
                del self.security_groups[item_id]
                return self.operation(item_id)
            if method == 'POST' and is_rules:
                group['rules'].append(dict(body, id=self.new_id('rule')))
                return self.operation(item_id)
            if method == 'DELETE' and is_rules:
                group['rules'] = [
                    rule for rule in group['rules'] if rule['id'] != rule_id
                ]
                return self.operation(item_id)
            if action == 'attach':
                instance = self.instances[body['instance']['id']]
                instance['security-groups'].append({'id': item_id})
                return self.operation(item_id)

        if kind == 'private-network':
            if method == 'GET' and item_id is None:
                return {'private-networks': list(self.networks.values())}
            if method == 'POST' and item_id is None:
                fields = {k: v for k, v in body.items() if k != 'name'}
                return self.operation(self.add_network(body['name'], **fields))
            network = self.networks.get(item_id)
            if network is None:
                return None
            if method == 'GET':
                return network
            if method == 'DELETE':
                del self.networks[item_id]
                return self.operation(item_id)
            instance_id = body['instance']['id']
            network['leases'] = [
                lease
                for lease in network['leases']
                if lease['instance-id'] != instance_id
            ]
            if action in ('attach', 'update-ip'):
                network['leases'].append(
                    {'instance-id': instance_id, 'ip': body.get('ip')}
                )
            return self.operation(item_id)

        if kind == 'instance':
            if method == 'GET' and item_id is None:
                return {
                    'instances': [
                        {'id': i['id'], 'name': i['name'], 'state': i['state']}
                        for i in self.instances.values()
                    ]
                }
            if method == 'POST' and item_id is None:
                instance_id = self.add_instance(
                    body['name'],
                    state='running' if body.get('auto-start', True) else 'stopped',
                    type_id=body['instance-type']['id'],
                    **{
                        'disk-size': body['disk-size'],
                        'public-ip-assignment': body.get('public-ip-assignment'),
                    },
                )
                self.instances[instance_id]['security-groups'] = body.get(
                    'security-groups', []
                )
                return self.operation(instance_id)
            instance = self.instances.get(item_id)
            if instance is None:
                return None
            if method == 'GET':
                result = dict(instance)
                result['private-networks'] = [
                    {'id': network['id']}
                    for network in self.networks.values()
                    if any(
                        lease['instance-id'] == item_id for lease in network['leases']
                    )
                ]
                return result
            if method == 'DELETE':
                del self.instances[item_id]
                return self.operation(item_id)
            if action in ('scale', 'resize-disk') and instance['state'] != 'stopped':
                return None
            if action == 'start':
                instance['state'] = 'running'
            elif action == 'stop':
                instance['state'] = 'stopped'
            elif action == 'scale':
                instance['instance-type'] = {'id': body['instance-type']['id']}
            elif action == 'resize-disk':
                instance['disk-size'] = body['disk-size']
            return self.operation(item_id)
        return None


def run_module(module, fake, args, check_mode=False):
    """Run `module.main()` against `fake` and return the result dict.

    A failed run returns the `fail_json()` arguments, with `failed` set.
    """
    args = dict(COMMON_ARGS, **args)
    if check_mode:
        args['_ansible_check_mode'] = True
    ansible_harness.set_module_args(args)
    with ansible_harness.patch_module(), unittest.mock.patch.object(
        exoscale, 'fetch_url', fake.fetch_url
    ), unittest.mock.patch.object(exoscale.time, 'sleep'):
        try:
            module.main()
        except ansible_harness.AnsibleExitJson as e:
            return e.args[0]
        except ansible_harness.AnsibleFailJson as e:
            return e.args[0]
    raise AssertionError('the module neither exited nor failed')
