#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the graylog module_util (pure diff helpers).

The collection import is wired up by tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

from ansible_collections.linuxfabrik.lfops.plugins.module_utils import graylog


class TestStripKeys(unittest.TestCase):

    def test_drops_listed_keys(self):
        self.assertEqual(
            graylog.strip_keys({'a': 1, 'state': 'present', 'b': 2}, ('state',)),
            {'a': 1, 'b': 2},
        )

    def test_handles_empty(self):
        self.assertEqual(graylog.strip_keys({}, ('state',)), {})
        self.assertEqual(graylog.strip_keys(None, ('state',)), {})

    def test_no_op_when_keys_missing(self):
        self.assertEqual(
            graylog.strip_keys({'a': 1}, ('state', 'default')),
            {'a': 1},
        )


class TestEqual(unittest.TestCase):

    def test_scalar(self):
        self.assertTrue(graylog._equal(1, 1))
        self.assertFalse(graylog._equal(1, 2))
        self.assertTrue(graylog._equal('a', 'a'))

    def test_nested_dict(self):
        a = {'x': {'y': [1, 2]}}
        b = {'x': {'y': [1, 2]}}
        self.assertTrue(graylog._equal(a, b))

    def test_nested_dict_diff(self):
        a = {'x': {'y': [1, 2]}}
        b = {'x': {'y': [1, 3]}}
        self.assertFalse(graylog._equal(a, b))

    def test_list_order_sensitive(self):
        # diff_changed_fields treats lists positionally to avoid masking order
        # changes in things like rotation/retention configuration.
        self.assertFalse(graylog._equal([1, 2], [2, 1]))


class TestDiffChangedFields(unittest.TestCase):

    def test_no_change(self):
        before, after = graylog.diff_changed_fields(
            {'a': 1, 'b': 2}, {'a': 1, 'b': 2},
        )
        self.assertEqual((before, after), ({}, {}))

    def test_scalar_change(self):
        before, after = graylog.diff_changed_fields(
            {'a': 1, 'b': 2}, {'a': 1, 'b': 9},
        )
        self.assertEqual(before, {'b': 2})
        self.assertEqual(after, {'b': 9})

    def test_nested_change(self):
        before, after = graylog.diff_changed_fields(
            {'configuration': {'port': 5044}},
            {'configuration': {'port': 5045}},
        )
        self.assertEqual(before, {'configuration': {'port': 5044}})
        self.assertEqual(after, {'configuration': {'port': 5045}})

    def test_ignore_skips_field(self):
        before, after = graylog.diff_changed_fields(
            {'id': 'abc', 'title': 'old'},
            {'id': 'abc', 'title': 'new'},
            ignore=('id',),
        )
        self.assertEqual(before, {'title': 'old'})
        self.assertEqual(after, {'title': 'new'})

    def test_desired_only_keys(self):
        # Keys present in current but absent from desired are never reported;
        # the module never wants to "unset" something the inventory did not
        # mention.
        before, after = graylog.diff_changed_fields(
            {'a': 1, 'extra': 'server_managed'},
            {'a': 1},
        )
        self.assertEqual((before, after), ({}, {}))

    def test_field_added_in_desired(self):
        before, after = graylog.diff_changed_fields(
            {'a': 1},
            {'a': 1, 'b': 2},
        )
        self.assertEqual(before, {'b': None})
        self.assertEqual(after, {'b': 2})

    def test_both_empty(self):
        self.assertEqual(graylog.diff_changed_fields({}, {}), ({}, {}))
        self.assertEqual(graylog.diff_changed_fields(None, None), ({}, {}))


class TestGraylogAPIError(unittest.TestCase):

    def test_carries_fields(self):
        err = graylog.GraylogAPIError(400, 'http://x/y', 'bad request')
        self.assertEqual(err.status, 400)
        self.assertEqual(err.url, 'http://x/y')
        self.assertEqual(err.body, 'bad request')
        self.assertIn('HTTP 400', str(err))


if __name__ == '__main__':
    unittest.main()
