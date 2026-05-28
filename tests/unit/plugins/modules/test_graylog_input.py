#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the graylog_input pure helpers.

The collection import is wired up by tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

from ansible_collections.linuxfabrik.lfops.plugins.modules import graylog_input as mod


class TestFindByTitle(unittest.TestCase):

    def test_match(self):
        inputs = [{'title': 'a'}, {'title': 'b'}]
        self.assertEqual(mod.find_by_title(inputs, 'b'), {'title': 'b'})

    def test_no_match_returns_none(self):
        self.assertIsNone(mod.find_by_title([{'title': 'a'}], 'b'))

    def test_empty_list(self):
        self.assertIsNone(mod.find_by_title([], 'b'))
        self.assertIsNone(mod.find_by_title(None, 'b'))


class TestNormalizeCurrent(unittest.TestCase):

    def test_attributes_remapped_to_configuration(self):
        # Graylog GET responses use `attributes` for what POST/PUT bodies call
        # `configuration`; the normalizer mirrors the field so the diff
        # compares like with like.
        current = {
            'id': 'abc',
            'title': 'Gelf UDP',
            'type': 'org.graylog2.inputs.gelf.udp.GELFUDPInput',
            'global': True,
            'node': None,
            'attributes': {'port': 12201, 'bind_address': '0.0.0.0'},
        }
        normalized = mod.normalize_current(current)
        self.assertEqual(normalized['configuration'], {'port': 12201, 'bind_address': '0.0.0.0'})
        self.assertEqual(normalized['title'], 'Gelf UDP')
        self.assertEqual(normalized['type'], 'org.graylog2.inputs.gelf.udp.GELFUDPInput')
        self.assertTrue(normalized['global'])

    def test_empty(self):
        self.assertEqual(mod.normalize_current({}), {})
        self.assertEqual(mod.normalize_current(None), {})

    def test_empty_secret_dict_unwrapped(self):
        # Graylog stores secret-bearing fields like `tls_key_password` as
        # {"encrypted_value": "", "salt": ""} on read but accepts a plain
        # string on write. Without unwrapping, the diff fires every run.
        current = {
            'title': 't',
            'attributes': {
                'port': 5044,
                'tls_key_password': {'encrypted_value': '', 'salt': ''},
            },
        }
        normalized = mod.normalize_current(current)
        self.assertEqual(normalized['configuration']['tls_key_password'], '')

    def test_non_empty_secret_dict_left_as_is(self):
        # A non-empty encrypted_value cannot be compared to the user's plain
        # value; preserve the dict so the diff continues to fire (write-once
        # semantics) rather than silently masking a real secret change.
        current = {
            'title': 't',
            'attributes': {
                'tls_key_password': {'encrypted_value': 'abc', 'salt': 'xyz'},
            },
        }
        normalized = mod.normalize_current(current)
        self.assertEqual(
            normalized['configuration']['tls_key_password'],
            {'encrypted_value': 'abc', 'salt': 'xyz'},
        )


class TestBuildDesired(unittest.TestCase):

    def test_drops_none_values(self):
        params = {
            'title': 'a',
            'type': 'foo',
            'configuration': {'port': 1},
            'global': True,
            'node': None,
        }
        desired = mod.build_desired(params)
        self.assertNotIn('node', desired)
        self.assertEqual(desired['title'], 'a')
        self.assertEqual(desired['configuration'], {'port': 1})

    def test_ignores_unknown_keys(self):
        # build_desired only picks up _DIFF_FIELDS; ancillary AnsibleModule
        # params like `url`/`username`/`state` must not leak into the body.
        params = {
            'title': 'a',
            'url': 'http://x',
            'username': 'admin',
            'state': 'present',
        }
        desired = mod.build_desired(params)
        self.assertEqual(set(desired.keys()), {'title'})


if __name__ == '__main__':
    unittest.main()
