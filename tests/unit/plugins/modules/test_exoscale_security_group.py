#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the exoscale_security_group module.

main() runs against the in-memory Exoscale fake from tests/exoscale_fake.py.
The collection import is wired up by tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

import exoscale_fake
from ansible_collections.linuxfabrik.lfops.plugins.modules import (
    exoscale_security_group as mod,
)

SSH = {'protocol': 'tcp', 'start_port': 22, 'end_port': 22}
SSH_API = {
    'end-port': 22,
    'flow-direction': 'ingress',
    'network': '0.0.0.0/0',
    'protocol': 'tcp',
    'start-port': 22,
}


def run(fake, check_mode=False, **args):
    args.setdefault('name', 'web01')
    return exoscale_fake.run_module(mod, fake, args, check_mode=check_mode)


class TestRuleKey(unittest.TestCase):
    def test_param_and_api_match(self):
        param = {
            'cidr': '0.0.0.0/0',
            'end_port': 22,
            'icmp_code': -1,
            'icmp_type': -1,
            'protocol': 'tcp',
            'start_port': 22,
            'type': 'ingress',
        }
        self.assertEqual(mod.key_from_param(param), mod.key_from_api(SSH_API))

    def test_network_is_normalized(self):
        self.assertEqual(
            mod.rule_key('ingress', 'tcp', '192.0.2.7/24', 22, 22, None, None),
            mod.rule_key('ingress', 'tcp', '192.0.2.0/24', 22, 22, None, None),
        )

    def test_icmp_defaults_to_any(self):
        api = {'flow-direction': 'ingress', 'network': '0.0.0.0/0', 'protocol': 'icmp'}
        self.assertEqual(
            mod.key_from_api(api),
            mod.rule_key('ingress', 'icmp', '0.0.0.0/0', None, None, -1, -1),
        )

    def test_ports_ignored_for_icmp(self):
        self.assertEqual(
            mod.rule_key('ingress', 'icmp', '0.0.0.0/0', 22, 22, 8, 0),
            mod.rule_key('ingress', 'icmp', '0.0.0.0/0', None, None, 8, 0),
        )

    def test_body(self):
        key = mod.rule_key('ingress', 'icmp', '0.0.0.0/0', None, None, 8, 0)
        self.assertEqual(
            mod.body_from_key(key),
            {
                'flow-direction': 'ingress',
                'icmp': {'code': 0, 'type': 8},
                'network': '0.0.0.0/0',
                'protocol': 'icmp',
            },
        )


class TestMain(unittest.TestCase):
    def test_create_with_rules(self):
        fake = exoscale_fake.FakeExoscale()
        result = run(fake, rules=[SSH])
        self.assertTrue(result['changed'])
        sg_id = fake.find('security_groups', 'web01')
        rules = fake.security_groups[sg_id]['rules']
        self.assertEqual(len(rules), 1)
        self.assertEqual({k: v for k, v in rules[0].items() if k != 'id'}, SSH_API)
        self.assertEqual(result['security_group']['id'], sg_id)

    def test_existing_rule_is_idempotent(self):
        fake = exoscale_fake.FakeExoscale()
        fake.add_security_group('web01', rules=[SSH_API])
        result = run(fake, rules=[dict(SSH, type='ingress', cidr='0.0.0.0/0')])
        self.assertFalse(result['changed'])
        self.assertEqual(fake.writes(), [])

    def test_unlisted_rule_is_kept(self):
        fake = exoscale_fake.FakeExoscale()
        sg_id = fake.add_security_group('web01', rules=[SSH_API])
        result = run(fake, rules=[{'protocol': 'icmp'}])
        self.assertTrue(result['changed'])
        self.assertEqual(len(fake.security_groups[sg_id]['rules']), 2)

    def test_absent_rule_is_deleted(self):
        fake = exoscale_fake.FakeExoscale()
        sg_id = fake.add_security_group('web01', rules=[SSH_API])
        result = run(fake, rules=[dict(SSH, state='absent')])
        self.assertTrue(result['changed'])
        self.assertEqual(fake.security_groups[sg_id]['rules'], [])

    def test_check_mode_writes_nothing(self):
        fake = exoscale_fake.FakeExoscale()
        result = run(fake, check_mode=True, rules=[SSH])
        self.assertTrue(result['changed'])
        self.assertEqual(fake.writes(), [])
        self.assertIn('rule: ingress tcp 0.0.0.0/0 port 22-22', result['diff']['after'])

    def test_delete(self):
        fake = exoscale_fake.FakeExoscale()
        fake.add_security_group('web01')
        result = run(fake, state='absent')
        self.assertTrue(result['changed'])
        self.assertIsNone(fake.find('security_groups', 'web01'))

    def test_delete_missing(self):
        fake = exoscale_fake.FakeExoscale()
        result = run(fake, state='absent')
        self.assertFalse(result['changed'])

    def test_duplicate_name_fails(self):
        fake = exoscale_fake.FakeExoscale()
        fake.add_security_group('web01')
        fake.add_security_group('web01')
        result = run(fake, rules=[SSH])
        self.assertTrue(result['failed'])
        self.assertIn('2 security groups are called "web01"', result['msg'])

    def test_api_error_fails(self):
        fake = exoscale_fake.FakeExoscale()
        fake.failures[('GET', '/security-group')] = (403, 'forbidden')
        result = run(fake, rules=[SSH])
        self.assertTrue(result['failed'])
        self.assertIn('HTTP 403: forbidden', result['msg'])


if __name__ == '__main__':
    unittest.main()
