#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the exoscale_instance module.

main() runs against the in-memory Exoscale fake from tests/exoscale_fake.py,
which refuses to scale or resize a running instance, as Exoscale does. The
collection import is wired up by tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest
import unittest.mock

import exoscale_fake
from ansible.module_utils import basic
from ansible_collections.linuxfabrik.lfops.plugins.modules import (
    exoscale_instance as mod,
)

CREATE = {
    'disk_size': 10,
    'instance_type': 'standard.tiny',
    'public_ip_assignment': 'none',
    'ssh_keys': ['linuxfabrik'],
    'template': exoscale_fake.TEMPLATE_NAME,
}


def run(fake, check_mode=False, **args):
    args.setdefault('name', 'web01')
    return exoscale_fake.run_module(mod, fake, args, check_mode=check_mode)


def actions(fake):
    """Return the mutating calls as `METHOD /kind:action` without IDs."""
    return [
        f'{method} {path.split("/")[1]}'
        + (f':{path.split(":")[1]}' if ':' in path else '')
        for method, path in fake.writes()
    ]


class TestCreate(unittest.TestCase):
    def test_create(self):
        fake = exoscale_fake.FakeExoscale()
        sg_id = fake.add_security_group('web01')
        net_id = fake.add_network('net-prod01')
        result = run(
            fake,
            state='started',
            security_groups=['default', 'web01'],
            private_networks=[{'name': 'net-prod01', 'fixed_ip': '192.0.2.10'}],
            **CREATE,
        )
        self.assertTrue(result['changed'])
        instance = fake.instances[fake.find('instances', 'web01')]
        self.assertEqual(instance['state'], 'running')
        self.assertEqual(instance['instance-type']['id'], 'type-standard-tiny')
        self.assertIn({'id': sg_id}, instance['security-groups'])
        self.assertEqual(
            fake.networks[net_id]['leases'],
            [{'instance-id': instance['id'], 'ip': '192.0.2.10'}],
        )
        _method, _path, body = next(
            c for c in fake.calls if c[:2] == ('POST', '/instance')
        )
        self.assertEqual(body['template']['id'], exoscale_fake.TEMPLATE_ID)
        self.assertEqual(body['ssh-keys'], [{'name': 'linuxfabrik'}])
        self.assertTrue(body['auto-start'])

    def test_create_stopped_does_not_boot(self):
        fake = exoscale_fake.FakeExoscale()
        run(fake, state='stopped', **CREATE)
        instance = fake.instances[fake.find('instances', 'web01')]
        self.assertEqual(instance['state'], 'stopped')

    def test_create_needs_type(self):
        fake = exoscale_fake.FakeExoscale()
        result = run(fake, template=exoscale_fake.TEMPLATE_NAME, disk_size=10)
        self.assertTrue(result['failed'])
        self.assertIn('instance_type is required', result['msg'])

    def test_unknown_type_fails(self):
        fake = exoscale_fake.FakeExoscale()
        result = run(fake, **dict(CREATE, instance_type='standard.huge'))
        self.assertTrue(result['failed'])
        self.assertIn('unknown instance type', result['msg'])

    def test_missing_security_group_fails(self):
        fake = exoscale_fake.FakeExoscale()
        result = run(fake, security_groups=['web01'], **CREATE)
        self.assertTrue(result['failed'])
        self.assertIn('security group "web01" does not exist', result['msg'])

    def test_check_mode_with_missing_dependencies(self):
        # in check mode, the security group and network tasks before did not
        # create anything either
        fake = exoscale_fake.FakeExoscale()
        result = run(
            fake,
            check_mode=True,
            security_groups=['default', 'web01'],
            private_networks=[{'name': 'net-prod01'}],
            **CREATE,
        )
        self.assertTrue(result['changed'])
        self.assertEqual(fake.writes(), [])
        self.assertIn('security-group: web01', result['diff']['after'])
        self.assertEqual(result['diff']['before'], '')


class TestUpdate(unittest.TestCase):
    def test_unchanged(self):
        fake = exoscale_fake.FakeExoscale()
        instance_id = fake.add_instance('web01')
        net_id = fake.add_network('net-prod01')
        fake.attach(net_id, instance_id, '192.0.2.10')
        result = run(
            fake,
            state='started',
            security_groups=['default'],
            private_networks=[{'name': 'net-prod01', 'fixed_ip': '192.0.2.10'}],
            **CREATE,
        )
        self.assertFalse(result['changed'])
        self.assertEqual(fake.writes(), [])
        self.assertEqual(result['diff']['before'], result['diff']['after'])

    def test_template_change_is_ignored(self):
        fake = exoscale_fake.FakeExoscale()
        fake.add_instance('web01')
        result = run(fake, **dict(CREATE, template='Some Other Template'))
        self.assertFalse(result['changed'])

    def test_scale_running_needs_force(self):
        fake = exoscale_fake.FakeExoscale()
        fake.add_instance('web01')
        result = run(
            fake, state='started', **dict(CREATE, instance_type='standard.small')
        )
        self.assertTrue(result['failed'])
        self.assertIn('scale it from standard.tiny to standard.small', result['msg'])
        self.assertEqual(fake.writes(), [])

    def test_refusal_changes_nothing_else(self):
        fake = exoscale_fake.FakeExoscale()
        fake.add_instance('web01')
        fake.add_security_group('web01')
        result = run(
            fake,
            security_groups=['default', 'web01'],
            **dict(CREATE, disk_size=20),
        )
        self.assertTrue(result['failed'])
        self.assertEqual(fake.writes(), [])

    def test_scale_running_with_force(self):
        fake = exoscale_fake.FakeExoscale()
        instance_id = fake.add_instance('web01')
        result = run(
            fake,
            state='started',
            force=True,
            **dict(CREATE, instance_type='standard.small'),
        )
        self.assertTrue(result['changed'])
        self.assertEqual(
            actions(fake),
            ['PUT instance:stop', 'PUT instance:scale', 'PUT instance:start'],
        )
        instance = fake.instances[instance_id]
        self.assertEqual(instance['instance-type']['id'], 'type-standard-small')
        self.assertEqual(instance['state'], 'running')

    def test_present_restarts_what_it_stopped(self):
        fake = exoscale_fake.FakeExoscale()
        instance_id = fake.add_instance('web01')
        run(fake, state='present', force=True, **dict(CREATE, disk_size=20))
        self.assertEqual(fake.instances[instance_id]['state'], 'running')
        self.assertEqual(fake.instances[instance_id]['disk-size'], 20)

    def test_grow_disk_of_stopped_instance(self):
        fake = exoscale_fake.FakeExoscale()
        instance_id = fake.add_instance('web01', state='stopped')
        result = run(fake, state='stopped', **dict(CREATE, disk_size=20))
        self.assertTrue(result['changed'])
        self.assertEqual(actions(fake), ['PUT instance:resize-disk'])
        self.assertEqual(fake.instances[instance_id]['state'], 'stopped')

    def test_stopped_needs_no_force(self):
        fake = exoscale_fake.FakeExoscale()
        instance_id = fake.add_instance('web01')
        run(fake, state='stopped', **dict(CREATE, disk_size=20))
        self.assertEqual(
            actions(fake), ['PUT instance:stop', 'PUT instance:resize-disk']
        )
        self.assertEqual(fake.instances[instance_id]['state'], 'stopped')

    def test_shrink_disk_fails(self):
        fake = exoscale_fake.FakeExoscale()
        fake.add_instance('web01', **{'disk-size': 50})
        result = run(fake, **CREATE)
        self.assertTrue(result['failed'])
        self.assertIn('cannot shrink from 50 GiB to 10 GiB', result['msg'])

    def test_start(self):
        fake = exoscale_fake.FakeExoscale()
        instance_id = fake.add_instance('web01', state='stopped')
        result = run(fake, state='started')
        self.assertTrue(result['changed'])
        self.assertEqual(fake.instances[instance_id]['state'], 'running')
        self.assertIn('state: stopped', result['diff']['before'])
        self.assertIn('state: running', result['diff']['after'])

    def test_present_keeps_power_state(self):
        fake = exoscale_fake.FakeExoscale()
        fake.add_instance('web01', state='stopped')
        result = run(fake, state='present')
        self.assertFalse(result['changed'])

    def test_restarted(self):
        fake = exoscale_fake.FakeExoscale()
        fake.add_instance('web01')
        result = run(fake, state='restarted')
        self.assertTrue(result['changed'])
        self.assertEqual(actions(fake), ['PUT instance:reboot'])

    def test_attach_security_group(self):
        fake = exoscale_fake.FakeExoscale()
        instance_id = fake.add_instance('web01')
        sg_id = fake.add_security_group('web01')
        result = run(fake, security_groups=['default', 'web01'])
        self.assertTrue(result['changed'])
        self.assertIn({'id': sg_id}, fake.instances[instance_id]['security-groups'])

    def test_unlisted_security_group_is_kept(self):
        fake = exoscale_fake.FakeExoscale()
        fake.add_instance('web01')
        result = run(fake, security_groups=[])
        self.assertFalse(result['changed'])

    def test_update_ip(self):
        fake = exoscale_fake.FakeExoscale()
        instance_id = fake.add_instance('web01')
        net_id = fake.add_network('net-prod01')
        fake.attach(net_id, instance_id, '192.0.2.10')
        result = run(
            fake, private_networks=[{'name': 'net-prod01', 'fixed_ip': '192.0.2.11'}]
        )
        self.assertTrue(result['changed'])
        self.assertEqual(actions(fake), ['PUT private-network:update-ip'])
        self.assertEqual(fake.networks[net_id]['leases'][0]['ip'], '192.0.2.11')

    def test_detach(self):
        fake = exoscale_fake.FakeExoscale()
        instance_id = fake.add_instance('web01')
        net_id = fake.add_network('net-prod01')
        fake.attach(net_id, instance_id)
        result = run(fake, private_networks=[{'name': 'net-prod01', 'state': 'absent'}])
        self.assertTrue(result['changed'])
        self.assertEqual(fake.networks[net_id]['leases'], [])

    def test_unlisted_network_is_kept(self):
        fake = exoscale_fake.FakeExoscale()
        instance_id = fake.add_instance('web01')
        net_id = fake.add_network('net-prod01')
        fake.attach(net_id, instance_id)
        result = run(fake, private_networks=[])
        self.assertFalse(result['changed'])

    def test_public_ip_assignment_warns(self):
        fake = exoscale_fake.FakeExoscale()
        fake.add_instance('web01')
        with unittest.mock.patch.object(basic.AnsibleModule, 'warn') as warn:
            result = run(fake, public_ip_assignment='inet4')
        self.assertFalse(result['changed'])
        self.assertIn('public_ip_assignment', warn.call_args[0][0])


class TestDelete(unittest.TestCase):
    def test_delete(self):
        fake = exoscale_fake.FakeExoscale()
        fake.add_instance('web01')
        result = run(fake, state='absent')
        self.assertTrue(result['changed'])
        self.assertEqual(fake.instances, {})
        self.assertIn('name: web01', result['diff']['before'])

    def test_delete_check_mode(self):
        fake = exoscale_fake.FakeExoscale()
        fake.add_instance('web01')
        result = run(fake, check_mode=True, state='absent')
        self.assertTrue(result['changed'])
        self.assertEqual(fake.writes(), [])

    def test_delete_missing(self):
        fake = exoscale_fake.FakeExoscale()
        result = run(fake, state='absent')
        self.assertFalse(result['changed'])


if __name__ == '__main__':
    unittest.main()
