#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the graylog_index_set pure helpers.

The collection import is wired up by tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

from ansible_collections.linuxfabrik.lfops.plugins.modules import graylog_index_set as mod


class TestFindByPrefix(unittest.TestCase):

    def test_match(self):
        sets = [{'index_prefix': 'audit'}, {'index_prefix': 'access'}]
        self.assertEqual(mod.find_by_prefix(sets, 'access'), {'index_prefix': 'access'})

    def test_no_match_returns_none(self):
        self.assertIsNone(mod.find_by_prefix([{'index_prefix': 'audit'}], 'access'))

    def test_empty_list(self):
        self.assertIsNone(mod.find_by_prefix([], 'access'))
        self.assertIsNone(mod.find_by_prefix(None, 'access'))


class TestNormalizeCurrent(unittest.TestCase):

    def test_keeps_only_diff_fields(self):
        current = {
            'id': 'srv-managed',
            'creation_date': '2026-01-01T00:00:00Z',
            'can_be_default': True,
            'title': 'Audit',
            'index_prefix': 'audit',
            'shards': 1,
            'replicas': 0,
            'writable': True,
            'data_tiering': {'type': 'hot_only',
                             'index_lifetime_min': 'P360D',
                             'index_lifetime_max': 'P365D'},
            'use_legacy_rotation': False,
            'description': 'Audit logs',
            'index_analyzer': 'standard',
            'index_optimization_disabled': False,
            'index_optimization_max_num_segments': 1,
            'field_type_refresh_interval': 5000,
        }
        normalized = mod.normalize_current(current)
        self.assertNotIn('id', normalized)
        self.assertNotIn('creation_date', normalized)
        self.assertNotIn('can_be_default', normalized)
        self.assertEqual(normalized['title'], 'Audit')
        self.assertEqual(normalized['data_tiering']['index_lifetime_max'], 'P365D')


class TestBuildDesired(unittest.TestCase):

    def test_drops_none(self):
        params = {
            'index_prefix': 'audit',
            'title': 'Audit',
            'description': None,
            'use_legacy_rotation': False,
            'data_tiering': {'type': 'hot_only'},
            'shards': 1,
            'replicas': 0,
            'writable': True,
            'index_analyzer': 'standard',
            'index_optimization_disabled': False,
            'index_optimization_max_num_segments': 1,
            'field_type_refresh_interval': 5000,
        }
        desired = mod.build_desired(params)
        self.assertNotIn('description', desired)
        self.assertEqual(desired['index_prefix'], 'audit')
        self.assertEqual(desired['data_tiering'], {'type': 'hot_only'})

    def test_ignores_role_only_and_connection_keys(self):
        params = {
            'index_prefix': 'audit',
            'url': 'http://x',
            'username': 'admin',
            'state': 'present',
            'default': True,
        }
        desired = mod.build_desired(params)
        # default + state + connection keys are role-only / module-only and
        # must never be POSTed/PUT'd to Graylog.
        self.assertEqual(set(desired.keys()), {'index_prefix'})


if __name__ == '__main__':
    unittest.main()
