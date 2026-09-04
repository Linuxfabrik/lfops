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

The lookup is instantiated through the plugin loader rather than by
calling `LookupModule()` directly, because `self.set_options()` only
resolves the documented options (and therefore the environment variable
behind `create`) for a plugin the loader has registered.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import unittest
from typing import ClassVar

from ansible.errors import AnsibleError
from ansible.plugins.loader import lookup_loader
from ansible_collections.linuxfabrik.lfops.plugins.lookup import (
    bitwarden_item as lookup_mod,
)

CREATE_ENV_VAR = 'LFOPS_BITWARDEN_LOOKUP_ITEM_CREATE'


def _load_lookup():
    """Return a loader-registered instance of the lookup plugin."""
    return lookup_loader.get('linuxfabrik.lfops.bitwarden_item')


class _FakeBitwarden:
    """Minimal stand-in for the Bitwarden client used by the lookup."""

    items_by_search: ClassVar[list] = []
    item_by_id = None
    created_items: ClassVar[list] = []
    vault_status = 'unlocked'

    def __init__(self, *args, **kwargs):
        pass

    @property
    def status(self):
        return type(self).vault_status

    def get_not_unlocked_message(self, status):
        return f'vault reports status "{status}"'

    def sync(self, *args, **kwargs):
        pass

    def get_items(
        self,
        name,
        username=None,
        folder_id=None,
        collection_id=None,
        organization_id=None,
    ):
        return list(type(self).items_by_search)

    def get_item_by_id(self, item_id):
        return type(self).item_by_id

    def generate(self, password_length=60, password_choice=''):
        return 'linuxfabrik'

    def get_template_item_login_uri(self, uris):
        return list(uris)

    def get_template_item_login(self, username, password, login_uris):
        return {'password': password, 'uris': login_uris, 'username': username}

    def get_template_item(
        self, name, login, notes, organization_id, collection_id, folder_id
    ):
        return {'login': login, 'name': name, 'notes': notes}

    def create_item(self, item):
        type(self).created_items.append(item)
        return item

    @staticmethod
    def get_pretty_name(name, hostname=None, purpose=None):
        return name or hostname


class _BitwardenLookupTestCase(unittest.TestCase):
    def setUp(self):
        self._orig = lookup_mod.Bitwarden
        lookup_mod.Bitwarden = _FakeBitwarden
        _FakeBitwarden.items_by_search = []
        _FakeBitwarden.item_by_id = None
        _FakeBitwarden.created_items = []
        _FakeBitwarden.vault_status = 'unlocked'
        # a value leaking in from the caller's environment would flip the
        # default of the `create` option under the tests' feet
        self._orig_create_env = os.environ.pop(CREATE_ENV_VAR, None)
        self.lookup = _load_lookup()

    def tearDown(self):
        lookup_mod.Bitwarden = self._orig
        os.environ.pop(CREATE_ENV_VAR, None)
        if self._orig_create_env is not None:
            os.environ[CREATE_ENV_VAR] = self._orig_create_env


class TestRun(_BitwardenLookupTestCase):
    def test_existing_single_item_lifts_credentials(self):
        _FakeBitwarden.items_by_search = [
            {
                'name': 'host - db',
                'login': {'username': 'dba', 'password': 'linuxfabrik'},
            },
        ]
        result = self.lookup.run([{'name': 'host - db', 'username': 'dba'}])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['username'], 'dba')
        self.assertEqual(result[0]['password'], 'linuxfabrik')

    def test_vault_not_unlocked_aborts(self):
        for status in ('unauthenticated', 'locked'):
            with self.subTest(status=status):
                _FakeBitwarden.vault_status = status
                with self.assertRaises(AnsibleError) as ctx:
                    self.lookup.run([{'name': 'host - db', 'username': 'dba'}])
                self.assertIn(status, str(ctx.exception))
                self.assertEqual(_FakeBitwarden.created_items, [])

    def test_multiple_matches_raise(self):
        _FakeBitwarden.items_by_search = [
            {
                'name': 'host - db',
                'login': {'username': 'dba', 'password': 'linuxfabrik'},
            },
            {
                'name': 'host - db',
                'login': {'username': 'dba', 'password': 'linuxfabrik'},
            },
        ]
        with self.assertRaises(AnsibleError):
            self.lookup.run([{'name': 'host - db', 'username': 'dba'}])

    def test_missing_item_is_created_by_default(self):
        result = self.lookup.run([{'name': 'host - db', 'username': 'dba'}])
        self.assertEqual(len(_FakeBitwarden.created_items), 1)
        self.assertEqual(_FakeBitwarden.created_items[0]['name'], 'host - db')
        self.assertEqual(result[0]['username'], 'dba')
        self.assertEqual(result[0]['password'], 'linuxfabrik')

    def test_missing_item_raises_when_creation_disabled(self):
        os.environ[CREATE_ENV_VAR] = 'false'
        lookup = _load_lookup()
        with self.assertRaises(AnsibleError) as ctx:
            lookup.run([{'name': 'host - db', 'username': 'dba'}])
        self.assertIn('item creation is disabled', str(ctx.exception))
        self.assertEqual(_FakeBitwarden.created_items, [])

    def test_existing_item_is_returned_when_creation_disabled(self):
        os.environ[CREATE_ENV_VAR] = 'false'
        _FakeBitwarden.items_by_search = [
            {
                'name': 'host - db',
                'login': {'username': 'dba', 'password': 'linuxfabrik'},
            },
        ]
        lookup = _load_lookup()
        result = lookup.run([{'name': 'host - db', 'username': 'dba'}])
        self.assertEqual(result[0]['password'], 'linuxfabrik')

    def test_lookup_by_id_lifts_credentials(self):
        _FakeBitwarden.item_by_id = {
            'id': 'abc',
            'login': {'username': 'dba', 'password': 'linuxfabrik'},
        }
        result = self.lookup.run([{'id': 'abc'}])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['username'], 'dba')
        self.assertEqual(result[0]['password'], 'linuxfabrik')


if __name__ == '__main__':
    unittest.main()
