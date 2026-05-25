#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the bitwarden_item lookup plugin.

The lookup runs on the controller. All Bitwarden I/O goes through the
Bitwarden client, which is replaced with a fake here, so no server or
cache is touched. The collection import is wired up by tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

from ansible.errors import AnsibleError
from ansible_collections.linuxfabrik.lfops.plugins.lookup import bitwarden_item as lookup_mod


class _FakeBitwarden:
    """Minimal stand-in for the Bitwarden client used by the lookup."""

    items_by_search = []
    item_by_id = None

    def __init__(self, *args, **kwargs):
        pass

    @property
    def is_unlocked(self):
        return True

    def sync(self, *args, **kwargs):
        pass

    def get_items(self, name, username=None, folder_id=None, collection_id=None, organization_id=None):
        return list(type(self).items_by_search)

    def get_item_by_id(self, item_id):
        return type(self).item_by_id

    @staticmethod
    def get_pretty_name(name, hostname=None, purpose=None):
        return name or hostname


class _BitwardenLookupTestCase(unittest.TestCase):

    def setUp(self):
        self._orig = lookup_mod.Bitwarden
        lookup_mod.Bitwarden = _FakeBitwarden
        _FakeBitwarden.items_by_search = []
        _FakeBitwarden.item_by_id = None
        self.lookup = lookup_mod.LookupModule(loader=None, templar=None)

    def tearDown(self):
        lookup_mod.Bitwarden = self._orig


class TestRun(_BitwardenLookupTestCase):

    def test_existing_single_item_lifts_credentials(self):
        _FakeBitwarden.items_by_search = [
            {'name': 'host - db', 'login': {'username': 'dba', 'password': 'linuxfabrik'}},
        ]
        result = self.lookup.run([{'name': 'host - db', 'username': 'dba'}])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['username'], 'dba')
        self.assertEqual(result[0]['password'], 'linuxfabrik')

    def test_multiple_matches_raise(self):
        _FakeBitwarden.items_by_search = [
            {'name': 'host - db', 'login': {'username': 'dba', 'password': 'linuxfabrik'}},
            {'name': 'host - db', 'login': {'username': 'dba', 'password': 'linuxfabrik'}},
        ]
        with self.assertRaises(AnsibleError):
            self.lookup.run([{'name': 'host - db', 'username': 'dba'}])

    def test_lookup_by_id_lifts_credentials(self):
        _FakeBitwarden.item_by_id = {
            'id': 'abc', 'login': {'username': 'dba', 'password': 'linuxfabrik'},
        }
        result = self.lookup.run([{'id': 'abc'}])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['username'], 'dba')
        self.assertEqual(result[0]['password'], 'linuxfabrik')


if __name__ == '__main__':
    unittest.main()
