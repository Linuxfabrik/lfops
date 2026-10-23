#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the exoscale_private_network module.

main() runs against the in-memory Exoscale fake from tests/exoscale_fake.py.
The collection import is wired up by tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

import exoscale_fake
from ansible_collections.linuxfabrik.lfops.plugins.modules import (
    exoscale_private_network as mod,
)


def run(fake, check_mode=False, **args):
    args.setdefault('name', 'net-prod01')
    return exoscale_fake.run_module(mod, fake, args, check_mode=check_mode)


class TestAddressing(unittest.TestCase):
    def test_slash_24(self):
        # same range as the former ansible.utils.ipaddr("2") / ipaddr("-3")
        self.assertEqual(
            mod.addressing('192.0.2.0/24'),
            {
                'end-ip': '192.0.2.253',
                'netmask': '255.255.255.0',
                'start-ip': '192.0.2.2',
            },
        )

    def test_host_bits_are_ignored(self):
        self.assertEqual(mod.addressing('192.0.2.7/24'), mod.addressing('192.0.2.0/24'))

    def test_too_small(self):
        with self.assertRaises(ValueError):
            mod.addressing('192.0.2.0/30')


class TestMain(unittest.TestCase):
    def test_create_managed(self):
        fake = exoscale_fake.FakeExoscale()
        result = run(fake, cidr='192.0.2.0/24')
        self.assertTrue(result['changed'])
        network = fake.networks[fake.find('networks', 'net-prod01')]
        self.assertEqual(network['start-ip'], '192.0.2.2')
        self.assertEqual(result['private_network']['id'], network['id'])

    def test_create_unmanaged(self):
        fake = exoscale_fake.FakeExoscale()
        run(fake)
        network = fake.networks[fake.find('networks', 'net-prod01')]
        self.assertNotIn('start-ip', network)

    def test_existing_is_never_changed(self):
        fake = exoscale_fake.FakeExoscale()
        fake.add_network('net-prod01', **{'start-ip': '198.51.100.2'})
        result = run(fake, cidr='192.0.2.0/24')
        self.assertFalse(result['changed'])
        self.assertEqual(fake.writes(), [])

    def test_check_mode_writes_nothing(self):
        fake = exoscale_fake.FakeExoscale()
        result = run(fake, check_mode=True, cidr='192.0.2.0/24')
        self.assertTrue(result['changed'])
        self.assertEqual(fake.writes(), [])
        self.assertIn('start-ip: 192.0.2.2', result['diff']['after'])

    def test_invalid_cidr_fails(self):
        fake = exoscale_fake.FakeExoscale()
        result = run(fake, cidr='192.0.2.0/33')
        self.assertTrue(result['failed'])

    def test_delete(self):
        fake = exoscale_fake.FakeExoscale()
        fake.add_network('net-prod01')
        result = run(fake, state='absent')
        self.assertTrue(result['changed'])
        self.assertEqual(fake.networks, {})


if __name__ == '__main__':
    unittest.main()
