#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for nextcloud_occ_app_config array idempotency.

Nextcloud stores an C(array) value and returns it as a parsed JSON array
via C(config:list) (verified against Nextcloud 33: the value comes back
as C(["alpha", "beta"])). Comparing that as a Python repr string against
the user's array literal never matched, so the module reported a change
on every run. values_match() now compares array values as parsed JSON.
The collection import is wired up by tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

import ansible_harness

from ansible_collections.linuxfabrik.lfops.plugins.modules import nextcloud_occ_app_config as mod


class TestValuesMatch(unittest.TestCase):

    def test_array_equal_ignoring_whitespace(self):
        # occ returns '["alpha","beta"]'; user passes a spaced literal
        self.assertTrue(mod.values_match('["alpha","beta"]', '["alpha", "beta"]', 'array'))

    def test_array_canonical_vs_user(self):
        # cached path stores json.dumps(list) -> '["alpha", "beta"]'
        self.assertTrue(mod.values_match('["alpha", "beta"]', '["alpha","beta"]', 'array'))

    def test_array_different(self):
        self.assertFalse(mod.values_match('["alpha", "beta"]', '["alpha","gamma"]', 'array'))

    def test_array_invalid_json_is_not_a_match(self):
        self.assertFalse(mod.values_match("['alpha', 'beta']", '["alpha","beta"]', 'array'))

    def test_non_array_string_compare(self):
        self.assertTrue(mod.values_match('90', '90', 'integer'))
        self.assertFalse(mod.values_match('90', '91', 'integer'))


class TestMainCachedArray(unittest.TestCase):
    """Exercise main() via the installed_config_json (cache) path, no occ needed."""

    def setUp(self):
        self._patch = ansible_harness.patch_module()
        self._patch.start()

    def tearDown(self):
        self._patch.stop()

    def _run(self, args):
        ansible_harness.set_module_args(args)
        try:
            mod.main()
        except ansible_harness.AnsibleExitJson as exc:
            return exc.args[0]
        raise AssertionError('module did not call exit_json')

    def test_array_already_set_is_idempotent(self):
        result = self._run({
            'app': 'core',
            'name': 'test_array',
            'value': '["alpha","beta"]',
            'type': 'array',
            'installed_config_json': {'apps': {'core': {'test_array': ['alpha', 'beta']}}},
        })
        self.assertFalse(result['changed'])

    def test_array_differs_reports_change(self):
        result = self._run({
            'app': 'core',
            'name': 'test_array',
            'value': '["alpha","beta"]',
            'type': 'array',
            'installed_config_json': {'apps': {'core': {'test_array': ['alpha', 'gamma']}}},
            '_ansible_check_mode': True,  # avoid the real occ config:app:set call
        })
        self.assertTrue(result['changed'])


if __name__ == '__main__':
    unittest.main()
