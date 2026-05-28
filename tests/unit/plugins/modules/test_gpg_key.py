#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the gpg_key module's pure key-matching logic.

match_key decides whether an existing key satisfies the requested
attributes (used for idempotency); it takes plain dicts and needs no gpg
binary. The collection import is wired up by tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import copy
import unittest

from ansible_collections.linuxfabrik.lfops.plugins.modules import gpg_key


_KEY = {
    'algo': '1',          # 1 -> RSA
    'length': '2048',
    'uids': ['Test Name (a comment) <test@example.com>'],
}

_PARAMS = {
    'key_type': 'RSA',
    'key_length': 2048,
    'name_real': 'Test Name',
    'name_comment': 'a comment',
    'name_email': 'test@example.com',
    'subkey_type': None,
    'subkey_length': None,
}


class TestMatchKey(unittest.TestCase):

    def test_full_match(self):
        self.assertTrue(gpg_key.match_key(copy.deepcopy(_KEY), dict(_PARAMS)))

    def test_wrong_length(self):
        params = dict(_PARAMS, key_length=4096)
        self.assertFalse(gpg_key.match_key(copy.deepcopy(_KEY), params))

    def test_wrong_type(self):
        params = dict(_PARAMS, key_type='DSA')
        self.assertFalse(gpg_key.match_key(copy.deepcopy(_KEY), params))

    def test_wrong_email(self):
        params = dict(_PARAMS, name_email='other@example.com')
        self.assertFalse(gpg_key.match_key(copy.deepcopy(_KEY), params))

    def test_wrong_real_name(self):
        params = dict(_PARAMS, name_real='Someone Else')
        self.assertFalse(gpg_key.match_key(copy.deepcopy(_KEY), params))

    def test_subkey_match(self):
        key = copy.deepcopy(_KEY)
        key['subkey_info'] = {'sub1': {'algo': '1', 'length': '2048'}}
        params = dict(_PARAMS, subkey_type='RSA', subkey_length=2048)
        self.assertTrue(gpg_key.match_key(key, params))

    def test_subkey_no_match(self):
        key = copy.deepcopy(_KEY)
        key['subkey_info'] = {'sub1': {'algo': '1', 'length': '1024'}}
        params = dict(_PARAMS, subkey_type='RSA', subkey_length=2048)
        self.assertFalse(gpg_key.match_key(key, params))


if __name__ == '__main__':
    unittest.main()
