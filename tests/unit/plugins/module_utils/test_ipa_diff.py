#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the ipa_diff module_util (pure --diff helpers).

The collection import is wired up by tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

from ansible_collections.linuxfabrik.lfops.plugins.module_utils import ipa_diff


class TestCompareKey(unittest.TestCase):

    def test_scalar_equal(self):
        self.assertTrue(ipa_diff._compare_key('a', 'a'))
        self.assertFalse(ipa_diff._compare_key('a', 'b'))

    def test_list_order_insensitive(self):
        self.assertTrue(ipa_diff._compare_key(['a', 'b'], ['b', 'a']))

    def test_list_length_mismatch(self):
        self.assertFalse(ipa_diff._compare_key(['a'], ['a', 'b']))

    def test_scalar_promoted_to_list(self):
        # ipa side is a one-element list, arg is the bare scalar
        self.assertTrue(ipa_diff._compare_key('a', ['a']))


class TestGenArgsDiff(unittest.TestCase):

    def test_only_changed_keys(self):
        before, after = ipa_diff.gen_args_diff({'a': 'x', 'b': 'y'}, {'a': ['x'], 'b': ['z']})
        self.assertEqual(before, {'b': 'z'})
        self.assertEqual(after, {'b': 'y'})

    def test_ignore_list(self):
        before, after = ipa_diff.gen_args_diff({'a': 'x'}, {'a': ['z']}, ignore=['a'])
        self.assertEqual((before, after), ({}, {}))

    def test_empty_args(self):
        self.assertEqual(ipa_diff.gen_args_diff({}, {'a': ['x']}), ({}, {}))


class TestGenMemberDiff(unittest.TestCase):

    def test_no_change(self):
        self.assertEqual(ipa_diff.gen_member_diff('member_user', [], [], ['a']), ({}, {}))

    def test_add_and_delete(self):
        before, after = ipa_diff.gen_member_diff('member_user', ['c'], ['a'], ['a', 'b'])
        self.assertEqual(before, {'member_user': ['a', 'b']})
        self.assertEqual(after, {'member_user': ['b', 'c']})


class TestMergeDiffs(unittest.TestCase):

    def test_merge(self):
        before, after = ipa_diff.merge_diffs(({'a': 1}, {'a': 2}), ({'b': 3}, {'b': 4}))
        self.assertEqual(before, {'a': 1, 'b': 3})
        self.assertEqual(after, {'a': 2, 'b': 4})


class TestIPADiffTracker(unittest.TestCase):

    def test_empty_build(self):
        self.assertEqual(ipa_diff.IPADiffTracker().build_diff(), {})

    def test_skips_equal_entries(self):
        t = ipa_diff.IPADiffTracker()
        t.add_entry_diff('host1', {'x': 1}, {'x': 1})
        self.assertEqual(t.build_diff(), {})

    def test_records_changed_entry(self):
        t = ipa_diff.IPADiffTracker()
        t.add_entry_diff('host1', {'x': 1}, {'x': 2})
        diff = t.build_diff()
        self.assertEqual(len(diff['diff']), 1)
        self.assertEqual(diff['diff'][0]['before_header'], 'host1')


if __name__ == '__main__':
    unittest.main()
