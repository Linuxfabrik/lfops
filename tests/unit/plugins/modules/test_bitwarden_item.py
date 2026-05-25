#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the bitwarden_item module's pure diff helper.

The module itself runs via AnsiballZ, but `diff_and_update` is a plain
function and is tested in isolation. The collection import is wired up by
tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

from ansible_collections.linuxfabrik.lfops.plugins.modules.bitwarden_item import diff_and_update


class TestDiffAndUpdate(unittest.TestCase):

    def test_takes_over_id(self):
        current = {'id': 'abc', 'name': 'x'}
        target = {'name': 'x'}
        changed, updated = diff_and_update(current, target)
        self.assertEqual(updated['id'], 'abc')

    def test_no_change_when_equal(self):
        current = {'id': 'abc', 'name': 'x', 'notes': 'n'}
        target = {'name': 'x', 'notes': 'n'}
        changed, _ = diff_and_update(current, target)
        self.assertFalse(changed)

    def test_change_detected_on_differing_value(self):
        current = {'id': 'abc', 'name': 'x', 'notes': 'old'}
        target = {'name': 'x', 'notes': 'new'}
        changed, _ = diff_and_update(current, target)
        self.assertTrue(changed)

    def test_falsy_vs_falsy_is_not_a_change(self):
        # None vs empty list / empty string must not count as a change
        current = {'id': 'abc', 'collectionIds': None, 'notes': ''}
        target = {'collectionIds': [], 'notes': None}
        changed, _ = diff_and_update(current, target)
        self.assertFalse(changed)

    def test_nested_dict_change_detected(self):
        current = {'id': 'abc', 'login': {'username': 'old', 'totp': ''}}
        target = {'login': {'username': 'new', 'totp': ''}}
        changed, _ = diff_and_update(current, target)
        self.assertTrue(changed)

    def test_nested_dict_no_change(self):
        current = {'id': 'abc', 'login': {'username': 'same', 'totp': ''}}
        target = {'login': {'username': 'same', 'totp': ''}}
        changed, _ = diff_and_update(current, target)
        self.assertFalse(changed)


if __name__ == '__main__':
    unittest.main()
