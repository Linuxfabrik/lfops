#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the uptimerobot module_util pure helpers.

These cover the wire-format builders, the secret-redaction helper, the
cache-key hashing, the friendly-name resolution and the read-direction
response translators (which encode the idempotency-critical mapping
between UptimeRobot integer IDs and the human-readable labels). All are
pure functions; no HTTP and no filesystem is touched. The collection
import is wired up by tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

from ansible_collections.linuxfabrik.lfops.plugins.module_utils import uptimerobot as ur


class TestWireBuilders(unittest.TestCase):

    def test_alert_contacts_wire_with_defaults(self):
        wire = ur.alert_contacts_wire([{'id': 1, 'threshold': 5, 'recurrence': 0}, {'id': 2}])
        self.assertEqual(wire, '1_5_0-2_0_0')

    def test_mwindows_wire(self):
        self.assertEqual(ur.mwindows_wire([3, 4, 5]), '3-4-5')

    def test_monitors_wire(self):
        self.assertEqual(ur.monitors_wire([7, 8]), '7,8')


class TestTranslateHelpers(unittest.TestCase):

    def test_translate_known_and_unknown(self):
        self.assertEqual(ur._translate('http', ur.MONITOR_TYPE), 1)
        self.assertEqual(ur._translate('nope', ur.MONITOR_TYPE), 'nope')
        # non-string passes through untouched
        self.assertEqual(ur._translate(5, ur.MONITOR_TYPE), 5)

    def test_filter_keys_drops_unknown_and_empty(self):
        out = ur._filter_keys({'a': 1, 'b': None, 'c': '', 'd': 'x'}, {'a', 'b', 'c'})
        self.assertEqual(out, {'a': 1})

    def test_translate_keys_only_strings(self):
        params = {'type': 'http', 'interval': 300}
        ur._translate_keys(params, {'type': ur.MONITOR_TYPE})
        self.assertEqual(params['type'], 1)
        self.assertEqual(params['interval'], 300)


class TestSafeKeysAndCache(unittest.TestCase):

    def test_safe_keys_redacts_secrets(self):
        self.assertEqual(
            ur._safe_keys({'api_key': 'x', 'password': 'y', 'friendly_name': 'n'}),
            ['api_key=<redacted>', 'friendly_name', 'password=<redacted>'],
        )

    def test_cache_key_stable_and_param_sensitive(self):
        a = ur._cache_key('getMonitors', 'k', {'x': 1})
        b = ur._cache_key('getMonitors', 'k', {'x': 1})
        c = ur._cache_key('getMonitors', 'k', {'x': 2})
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)


class TestFriendlyNames(unittest.TestCase):

    def test_find_by_friendly_name(self):
        items = [{'friendly_name': 'a'}, {'friendly_name': 'b'}]
        self.assertEqual(ur.find_by_friendly_name(items, 'b'), {'friendly_name': 'b'})
        self.assertIsNone(ur.find_by_friendly_name(items, 'missing'))

    def test_resolve_friendly_names_ok(self):
        items = [{'friendly_name': 'a', 'id': 1}, {'friendly_name': 'b', 'id': 2}]
        self.assertEqual(ur.resolve_friendly_names(items, ['b', 'a'], 'monitor'), [2, 1])

    def test_resolve_friendly_names_unknown_raises(self):
        with self.assertRaises(ValueError):
            ur.resolve_friendly_names([{'friendly_name': 'a', 'id': 1}], ['zzz'], 'monitor')


class TestDiffForUpdate(unittest.TestCase):

    def test_diff_compares_stringified(self):
        # int 1 vs string '1' must be considered equal (no spurious change)
        out = ur.diff_for_update({'x': 1, 'y': 2}, {'x': '1', 'y': '3'}, ['x', 'y'])
        self.assertEqual(out, {'y': '3'})

    def test_diff_skips_fields_not_in_desired(self):
        out = ur.diff_for_update({'x': 1}, {}, ['x'])
        self.assertEqual(out, {})


class TestResponseTranslators(unittest.TestCase):

    def test_monitor_response_maps_ids_to_labels(self):
        item = {'type': 1, 'status': 2, 'http_method': 2, 'auth_type': 1}
        ur._translate_monitor_response(item)
        self.assertEqual(item['type'], 'http')
        self.assertEqual(item['status'], 'up')
        self.assertEqual(item['http_method'], 'get')
        # auth_type is mirrored to http_auth_type (write-side name)
        self.assertEqual(item['http_auth_type'], 'basic')

    def test_mwindow_response_translates_weekly_days(self):
        item = {'type': 3, 'status': 1, 'value': '1-3-5'}
        ur._translate_mwindow_response(item)
        self.assertEqual(item['type'], 'weekly')
        self.assertEqual(item['status'], 'active')
        self.assertEqual(item['value'], 'mon-wed-fri')

    def test_psp_response_mirrors_custom_url(self):
        item = {'sort': 1, 'status': 1, 'custom_url': 'status.example.com'}
        ur._translate_psp_response(item)
        self.assertEqual(item['sort'], 'a-z')
        self.assertEqual(item['status'], 'active')
        self.assertEqual(item['custom_domain'], 'status.example.com')

    def test_alert_contact_response_maps_ids(self):
        item = {'status': 2, 'type': 2}
        ur._translate_alert_contact_response(item)
        self.assertEqual(item['status'], 'active')
        self.assertEqual(item['type'], 'email')


if __name__ == '__main__':
    unittest.main()
