#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the bitwarden module_util.

The util runs on the Ansible controller (it is imported by the
bitwarden_item lookup) and, via AnsiballZ, on the managed node for the
bitwarden_item module. All network access funnels through
ansible.module_utils.urls.open_url, which the tests mock; no real
Bitwarden server or cache file is touched.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import importlib.util
import io
import json
import os
import unittest
from urllib.error import HTTPError

_MODULE_PATH = os.path.join(
    os.path.dirname(__file__),
    '..', '..', '..', '..',
    'plugins', 'module_utils', 'bitwarden.py',
)
_spec = importlib.util.spec_from_file_location('bitwarden', _MODULE_PATH)
bitwarden = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bitwarden)


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def read(self):
        return json.dumps(self._payload).encode('utf-8')


def _make_bitwarden(tmp_path='/nonexistent/lfops_bw_test_cache.json'):
    """Instantiate Bitwarden without touching a real cache file.

    Pointing CACHE_FILE at a missing path makes _load_cache start fresh,
    and the constructor performs no network I/O.
    """
    bitwarden.CACHE_FILE = tmp_path
    return bitwarden.Bitwarden()


class TestGenerate(unittest.TestCase):

    def test_length_and_charset(self):
        bw = _make_bitwarden()
        result = bw.generate(password_length=32, password_choice='abc')
        self.assertEqual(len(result), 32)
        self.assertTrue(set(result).issubset(set('abc')))

    def test_rejects_non_positive_length(self):
        bw = _make_bitwarden()
        with self.assertRaises(ValueError):
            bw.generate(password_length=0)

    def test_hex_requires_even_length(self):
        bw = _make_bitwarden()
        with self.assertRaises(ValueError):
            bw.generate(password_length=3, password_choice='0123456789abcdef')
        # even length is fine
        self.assertEqual(len(bw.generate(password_length=4, password_choice='0123456789abcdef')), 4)


class TestGetPrettyName(unittest.TestCase):

    def test_explicit_name_wins(self):
        self.assertEqual(bitwarden.Bitwarden.get_pretty_name('myname', 'host', 'purpose'), 'myname')

    def test_hostname_only(self):
        self.assertEqual(bitwarden.Bitwarden.get_pretty_name('', hostname='app4711'), 'app4711')

    def test_hostname_and_purpose(self):
        self.assertEqual(
            bitwarden.Bitwarden.get_pretty_name('', hostname='app4711', purpose='MariaDB'),
            'app4711 - MariaDB',
        )


class TestApiCall(unittest.TestCase):

    def setUp(self):
        self.bw = _make_bitwarden()
        self._orig_open_url = bitwarden.open_url

    def tearDown(self):
        bitwarden.open_url = self._orig_open_url

    def test_success_returns_result(self):
        bitwarden.open_url = lambda *a, **k: _FakeResponse({'success': True, 'data': {'x': 1}})
        result = self.bw._api_call('status')
        self.assertEqual(result, {'success': True, 'data': {'x': 1}})

    def test_unsuccessful_payload_raises(self):
        bitwarden.open_url = lambda *a, **k: _FakeResponse({'success': False, 'data': 'nope'})
        with self.assertRaises(bitwarden.BitwardenException):
            self.bw._api_call('status')

    def test_http_error_raises_bitwarden_exception(self):
        def _raise(*a, **k):
            raise HTTPError('http://127.0.0.1:8087/status', 500, 'err', {}, io.BytesIO(b''))
        bitwarden.open_url = _raise
        with self.assertRaises(bitwarden.BitwardenException):
            self.bw._api_call('status')

    def test_invalid_json_raises_bitwarden_exception(self):
        class _BadResponse:
            def read(self):
                return b'not json'
        bitwarden.open_url = lambda *a, **k: _BadResponse()
        with self.assertRaises(bitwarden.BitwardenException):
            self.bw._api_call('status')


class TestGetItems(unittest.TestCase):

    def setUp(self):
        self.bw = _make_bitwarden()
        # seed the in-memory cache directly; get_items only reads it
        self.bw._cache = {
            'items': [
                {'type': 1, 'name': 'host - db', 'login': {'username': 'dba'},
                 'folderId': None, 'collectionIds': [], 'organizationId': None},
                {'type': 2, 'name': 'host - db', 'login': {'username': 'dba'}},  # non-login, skipped
                {'type': 1, 'name': 'other', 'login': {'username': 'dba'},
                 'folderId': None, 'collectionIds': [], 'organizationId': None},
            ],
        }

    def test_matches_login_item_by_name_and_username(self):
        matches = self.bw.get_items('host - db', username='dba')
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['name'], 'host - db')

    def test_skips_non_login_items(self):
        # the type=2 entry shares name+username but must not match
        matches = self.bw.get_items('host - db', username='dba')
        self.assertTrue(all(item.get('type') == 1 for item in matches))

    def test_no_match_returns_empty(self):
        self.assertEqual(self.bw.get_items('does-not-exist', username='dba'), [])


if __name__ == '__main__':
    unittest.main()
