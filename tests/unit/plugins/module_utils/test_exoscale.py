#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the exoscale module_util.

The signatures below were computed with `ExoscaleV2Auth._sign_request()` of
requests-exoscale-auth 1.1.2, the signing library of Exoscale's own Python
SDK, for the same requests and expiry. The collection import is wired up by
tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

from ansible_collections.linuxfabrik.lfops.plugins.module_utils import exoscale

EXPIRES = 1767225600


class TestBuildAuthHeader(unittest.TestCase):
    def test_get_with_query(self):
        self.assertEqual(
            exoscale.build_auth_header(
                'EXOlinuxfabrik',
                'linuxfabrik',
                'GET',
                '/v2/template',
                None,
                {'visibility': 'public'},
                EXPIRES,
            ),
            'EXO2-HMAC-SHA256 credential=EXOlinuxfabrik,'
            'signed-query-args=visibility,expires=1767225600,'
            'signature=LjdEOUokeh7VVJdZEKHs58MBfDZG4IzhlB+tyBZOKAU=',
        )

    def test_post_with_body(self):
        self.assertEqual(
            exoscale.build_auth_header(
                'EXOlinuxfabrik',
                'linuxfabrik',
                'POST',
                '/v2/security-group',
                b'{"name":"web01"}',
                None,
                EXPIRES,
            ),
            'EXO2-HMAC-SHA256 credential=EXOlinuxfabrik,expires=1767225600,'
            'signature=Q3gDOutsoSklqHkeQtWxzxeJn1dQGfujU8g2f5wIQ9E=',
        )

    def test_get_without_query(self):
        self.assertEqual(
            exoscale.build_auth_header(
                'EXOlinuxfabrik',
                'linuxfabrik',
                'GET',
                '/v2/instance',
                None,
                {},
                EXPIRES,
            ),
            'EXO2-HMAC-SHA256 credential=EXOlinuxfabrik,expires=1767225600,'
            'signature=SFIoMHnrpre8oG0/zZuDUmMe/BNFM1yvkSIQfV6c3eo=',
        )


class TestFindByName(unittest.TestCase):
    def test_found(self):
        items = [{'id': 1, 'name': 'a'}, {'id': 2, 'name': 'b'}]
        self.assertEqual(exoscale.find_by_name(items, 'b', 'instance'), items[1])

    def test_missing(self):
        self.assertIsNone(
            exoscale.find_by_name([{'id': 1, 'name': 'a'}], 'b', 'instance')
        )

    def test_duplicate_is_an_error(self):
        items = [{'id': 1, 'name': 'a'}, {'id': 2, 'name': 'a'}]
        with self.assertRaises(ValueError):
            exoscale.find_by_name(items, 'a', 'instance')


class TestUuid(unittest.TestCase):
    def test_uuid(self):
        self.assertTrue(exoscale.UUID_RE.match('11111111-2222-3333-4444-555555555555'))

    def test_name(self):
        self.assertFalse(exoscale.UUID_RE.match('Rocky Linux 9 (Blue Onyx) 64-bit'))


if __name__ == '__main__':
    unittest.main()
