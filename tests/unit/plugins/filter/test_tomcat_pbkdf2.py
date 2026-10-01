#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the `tomcat_pbkdf2` filter plugin.

`tomcat_pbkdf2` is a filter plugin and therefore runs on the Ansible
controller only, so this test runs on the controller matrix, not on the
Python 3.6 (RHEL 8) managed-node tier. See `tests/README.md`.

The reference values were produced by Tomcat itself, with
`java org.apache.catalina.realm.RealmBase -a PBKDF2WithHmacSHA512 -s 16 -k 512
-h org.apache.catalina.realm.SecretKeyCredentialHandler`, which picks a random
salt. Re-deriving them from the salt Tomcat chose proves that the filter writes
what Tomcat's SecretKeyCredentialHandler accepts.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import importlib.util
import os
import unittest

from ansible.errors import AnsibleFilterError

# The plugin lives outside any importable package, so load it by path
# (repo_root/plugins/filter/tomcat_pbkdf2.py) relative to this test file.
_PLUGIN_PATH = os.path.join(
    os.path.dirname(__file__),
    '..',
    '..',
    '..',
    '..',
    'plugins',
    'filter',
    'tomcat_pbkdf2.py',
)
_spec = importlib.util.spec_from_file_location('tomcat_pbkdf2', _PLUGIN_PATH)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
tomcat_pbkdf2 = _module.tomcat_pbkdf2


# (password, stored credential) as printed by Tomcat's RealmBase
_TOMCAT_9_0_120_OPENJDK_8 = (
    'linuxfabrik',
    '91a29b13eebb2e721ac618f314466bc1$210000$'
    '4dd258ca5de563cc37b0b7ee7b9b5cdab4e32336300620acfaa9fff40169dda2'
    '8875bc67dab322e8f464f1f5b77366d5bd36143966e12a0f906a31a05395e5d0',
)
_TOMCAT_10_1_49_OPENJDK_21 = (
    'linuxfabrik',
    'd699c9ff2fdc079466cb8062af0701e7$210000$'
    '5acb4430e7a6d1a2a8f2923c039f36a5a5fabc13d481d6c2a96713a0c41b6ea0'
    'e01316683f745f0cbe579e7d2b9bbd9f84792798ad7fa33e06d7507e8883a815',
)
_TOMCAT_10_1_49_OPENJDK_21_NON_ASCII = (
    'pässwörd€',
    'dd350e7f0f91016c58d06038db0c2199$1000$'
    '056d98cd730009129773ad1a5341a0ef2c77c1ae02551a2935421ea34105cbe4'
    '94f45a50e35bb04c21fb6199b3fde620f7f1b0faf04407ec4669e3b9ce46bedc',
)


def _rederive(vector):
    password, stored = vector
    salt, iterations, key = stored.split('$')
    return tomcat_pbkdf2(
        password, salt, iterations=int(iterations), key_length=len(key) * 4
    )


class TestTomcatCompatibility(unittest.TestCase):
    def test_tomcat_9_0(self):
        self.assertEqual(
            _rederive(_TOMCAT_9_0_120_OPENJDK_8), _TOMCAT_9_0_120_OPENJDK_8[1]
        )

    def test_tomcat_10_1(self):
        self.assertEqual(
            _rederive(_TOMCAT_10_1_49_OPENJDK_21), _TOMCAT_10_1_49_OPENJDK_21[1]
        )

    def test_non_ascii_password_is_utf8_encoded(self):
        self.assertEqual(
            _rederive(_TOMCAT_10_1_49_OPENJDK_21_NON_ASCII),
            _TOMCAT_10_1_49_OPENJDK_21_NON_ASCII[1],
        )


class TestOutput(unittest.TestCase):
    _SALT = '00112233445566778899aabbccddeeff'

    def test_format_and_defaults(self):
        salt, iterations, key = tomcat_pbkdf2('linuxfabrik', self._SALT).split('$')
        self.assertEqual(salt, self._SALT)
        self.assertEqual(iterations, '210000')
        self.assertEqual(len(key), 128)  # 512 bits

    def test_deterministic(self):
        self.assertEqual(
            tomcat_pbkdf2('linuxfabrik', self._SALT, iterations=10),
            tomcat_pbkdf2('linuxfabrik', self._SALT, iterations=10),
        )

    def test_salt_changes_result(self):
        self.assertNotEqual(
            tomcat_pbkdf2('linuxfabrik', self._SALT, iterations=10).split('$')[2],
            tomcat_pbkdf2('linuxfabrik', 'ff' * 16, iterations=10).split('$')[2],
        )

    def test_uppercase_salt_is_normalized(self):
        self.assertEqual(
            tomcat_pbkdf2('linuxfabrik', self._SALT.upper(), iterations=10),
            tomcat_pbkdf2('linuxfabrik', self._SALT, iterations=10),
        )

    def test_key_length(self):
        key = tomcat_pbkdf2('linuxfabrik', self._SALT, iterations=10, key_length=160)
        self.assertEqual(len(key.split('$')[2]), 40)


class TestInvalidInput(unittest.TestCase):
    _SALT = '00112233445566778899aabbccddeeff'

    def test_password_not_a_string(self):
        with self.assertRaises(AnsibleFilterError):
            tomcat_pbkdf2(None, self._SALT)

    def test_salt_not_hex(self):
        with self.assertRaises(AnsibleFilterError):
            tomcat_pbkdf2('linuxfabrik', 'not-hex')

    def test_salt_odd_length(self):
        with self.assertRaises(AnsibleFilterError):
            tomcat_pbkdf2('linuxfabrik', 'abc')

    def test_salt_empty(self):
        with self.assertRaises(AnsibleFilterError):
            tomcat_pbkdf2('linuxfabrik', '')

    def test_salt_not_a_string(self):
        with self.assertRaises(AnsibleFilterError):
            tomcat_pbkdf2('linuxfabrik', None)

    def test_iterations_zero(self):
        with self.assertRaises(AnsibleFilterError):
            tomcat_pbkdf2('linuxfabrik', self._SALT, iterations=0)

    def test_iterations_bool(self):
        with self.assertRaises(AnsibleFilterError):
            tomcat_pbkdf2('linuxfabrik', self._SALT, iterations=True)

    def test_key_length_not_multiple_of_8(self):
        with self.assertRaises(AnsibleFilterError):
            tomcat_pbkdf2('linuxfabrik', self._SALT, key_length=100)


if __name__ == '__main__':
    unittest.main()
