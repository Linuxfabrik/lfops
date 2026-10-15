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

import contextlib
import multiprocessing
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
    # what a forced sync brings into the cache, None for no change
    items_after_forced_sync = None
    item_by_id = None
    created_items: ClassVar[list] = []
    sync_calls: ClassVar[list] = []
    # what sync() reports, True for a sync that actually ran
    sync_result = False
    vault_status = 'unlocked'

    mutex_held = False

    def __init__(self, *args, **kwargs):
        pass

    @contextlib.contextmanager
    def mutex(self, *args, **kwargs):
        type(self).mutex_held = True
        try:
            yield self
        finally:
            type(self).mutex_held = False

    @property
    def status(self):
        return type(self).vault_status

    def get_not_unlocked_message(self, status):
        return f'vault reports status "{status}"'

    def sync(self, force=False, run_id=None, **kwargs):
        type(self).sync_calls.append({'force': force, 'run_id': run_id})
        if force and type(self).items_after_forced_sync is not None:
            type(self).items_by_search = type(self).items_after_forced_sync
        return force or type(self).sync_result

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
        type(self).created_items.append(
            {**item, 'created_under_mutex': self.mutex_held}
        )
        return item

    @staticmethod
    def get_pretty_name(name, hostname=None, purpose=None):
        return name or hostname


class _BitwardenLookupTestCase(unittest.TestCase):
    def setUp(self):
        self._orig = lookup_mod.Bitwarden
        lookup_mod.Bitwarden = _FakeBitwarden
        _FakeBitwarden.items_by_search = []
        _FakeBitwarden.items_after_forced_sync = None
        _FakeBitwarden.item_by_id = None
        _FakeBitwarden.created_items = []
        _FakeBitwarden.sync_calls = []
        _FakeBitwarden.sync_result = False
        _FakeBitwarden.mutex_held = False
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

    def test_item_is_created_under_the_mutex_and_mutex_is_released(self):
        self.lookup.run([{'name': 'host - db', 'username': 'dba'}])
        self.assertTrue(_FakeBitwarden.created_items[0]['created_under_mutex'])
        self.assertFalse(_FakeBitwarden.mutex_held)

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

    def test_missing_item_is_searched_again_after_a_sync_before_it_is_created(self):
        # the cache predates an item created elsewhere during this run
        _FakeBitwarden.items_after_forced_sync = [
            {
                'name': 'host - db',
                'login': {'username': 'dba', 'password': 'linuxfabrik'},
            },
        ]
        result = self.lookup.run([{'name': 'host - db', 'username': 'dba'}])
        self.assertEqual(_FakeBitwarden.created_items, [])
        self.assertEqual(result[0]['password'], 'linuxfabrik')
        self.assertEqual([c['force'] for c in _FakeBitwarden.sync_calls], [False, True])

    def test_no_second_sync_if_the_lookup_has_just_synced(self):
        _FakeBitwarden.sync_result = True
        self.lookup.run([{'name': 'host - db', 'username': 'dba'}])
        self.assertEqual(len(_FakeBitwarden.created_items), 1)
        self.assertEqual(len(_FakeBitwarden.sync_calls), 1)

    def test_sync_gets_the_run_id(self):
        self.lookup.run([{'name': 'host - db', 'username': 'dba'}])
        self.assertEqual(
            _FakeBitwarden.sync_calls[0]['run_id'], lookup_mod.get_run_id()
        )


def _put_run_id(queue):
    queue.put(lookup_mod.get_run_id())


class TestGetRunId(unittest.TestCase):
    def test_forked_worker_gets_the_run_id_of_its_parent(self):
        # Ansible forks its workers without exec, like multiprocessing's fork context
        run_id = lookup_mod.get_run_id()
        self.assertIsNotNone(run_id)
        ctx = multiprocessing.get_context('fork')
        queue = ctx.Queue()
        worker = ctx.Process(target=_put_run_id, args=(queue,))
        worker.start()
        worker.join()
        self.assertEqual(queue.get(timeout=5), run_id)

    def test_no_proc_gives_no_run_id(self):
        def _missing(pid, name):
            raise FileNotFoundError(name)

        orig = lookup_mod._read_proc
        lookup_mod._read_proc = _missing
        try:
            self.assertIsNone(lookup_mod.get_run_id())
        finally:
            lookup_mod._read_proc = orig


if __name__ == '__main__':
    unittest.main()
