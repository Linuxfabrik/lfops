#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the `platform_select` filter plugin.

`platform_select` is a filter plugin and therefore runs on the Ansible
controller only. The controller requires Python >= 3.10 (ansible-core
2.16/2.17) or >= 3.11 (2.18), so this test runs on the controller
matrix, not on the Python 3.6 (RHEL 8) managed-node tier. See
`tests/README.md`.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import importlib.util
import os
import unittest

from ansible.errors import AnsibleFilterError

# The plugin lives outside any importable package, so load it by path
# (repo_root/plugins/filter/platform_select.py) relative to this test file.
_PLUGIN_PATH = os.path.join(
    os.path.dirname(__file__),
    '..', '..', '..', '..',
    'plugins', 'filter', 'platform_select.py',
)
_spec = importlib.util.spec_from_file_location('platform_select', _PLUGIN_PATH)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
platform_select = _module.platform_select


# realistic fact sets
_FACTS_ROCKY8 = {
    'os_family': 'RedHat',
    'distribution': 'Rocky',
    'distribution_major_version': '8',
    'distribution_version': '8.10',
}
_FACTS_DEBIAN12 = {
    'os_family': 'Debian',
    'distribution': 'Debian',
    'distribution_major_version': '12',
    'distribution_version': '12.5',
}
_FACTS_SUSE = {
    'os_family': 'Suse',
    'distribution': 'openSUSE Leap',
    'distribution_major_version': '15',
    'distribution_version': '15.6',
}


class Test(unittest.TestCase):

    # --- basic matching --------------------------------------------------

    def test_os_family_only(self):
        """The os_family key alone is enough when nothing more specific is present."""
        values = {'RedHat': 'redhat-pkg', 'Debian': 'debian-pkg'}
        self.assertEqual(platform_select(values, _FACTS_ROCKY8), 'redhat-pkg')
        self.assertEqual(platform_select(values, _FACTS_DEBIAN12), 'debian-pkg')

    def test_returned_value_can_be_any_type(self):
        """The filter returns the matched value verbatim, including lists/dicts."""
        values = {
            'RedHat': [{'name': 'python3-PyMySQL'}],
            'Debian': [{'name': 'python3-pymysql'}],
        }
        self.assertEqual(
            platform_select(values, _FACTS_ROCKY8),
            [{'name': 'python3-PyMySQL'}],
        )

    # --- precedence ------------------------------------------------------

    def test_distribution_beats_os_family(self):
        """A `distribution` key wins over a generic `os_family` key."""
        values = {'RedHat': 'family', 'Rocky': 'distro'}
        self.assertEqual(platform_select(values, _FACTS_ROCKY8), 'distro')

    def test_distribution_major_beats_distribution(self):
        """`distribution + major_version` wins over plain `distribution`."""
        values = {'Rocky': 'distro', 'Rocky8': 'major'}
        self.assertEqual(platform_select(values, _FACTS_ROCKY8), 'major')

    def test_distribution_version_beats_distribution_major(self):
        """`distribution + version` wins over `distribution + major_version`."""
        values = {'Rocky8': 'major', 'Rocky8.10': 'version'}
        self.assertEqual(platform_select(values, _FACTS_ROCKY8), 'version')

    def test_os_family_major_beats_os_family(self):
        """`os_family + major_version` wins over plain `os_family`."""
        values = {'RedHat': 'family', 'RedHat8': 'family-major'}
        self.assertEqual(platform_select(values, _FACTS_ROCKY8), 'family-major')

    def test_distribution_beats_os_family_version(self):
        """Documented quirk of platform-variables.yml: plain `distribution` is more
        specific than `os_family + distribution_version`. Mirror it here.
        """
        values = {'RedHat8.10': 'family-version', 'Rocky': 'distro'}
        self.assertEqual(platform_select(values, _FACTS_ROCKY8), 'distro')

    def test_full_precedence_chain(self):
        """All six precedence levels present at once: the most specific (distribution
        + distribution_version) wins."""
        values = {
            'RedHat': 'a',
            'RedHat8': 'b',
            'RedHat8.10': 'c',
            'Rocky': 'd',
            'Rocky8': 'e',
            'Rocky8.10': 'f',
        }
        self.assertEqual(platform_select(values, _FACTS_ROCKY8), 'f')

    # --- defaulting and unmatched ---------------------------------------

    def test_no_match_raises_without_default(self):
        values = {'RedHat': 'x', 'Debian': 'y'}
        with self.assertRaises(AnsibleFilterError):
            platform_select(values, _FACTS_SUSE)

    def test_no_match_returns_default(self):
        values = {'RedHat': 'x', 'Debian': 'y'}
        self.assertEqual(platform_select(values, _FACTS_SUSE, default=[]), [])

    def test_default_none_is_distinct_from_no_default(self):
        """Passing `default=None` returns None; omitting `default` raises."""
        values = {'RedHat': 'x'}
        self.assertIsNone(platform_select(values, _FACTS_SUSE, default=None))
        with self.assertRaises(AnsibleFilterError):
            platform_select(values, _FACTS_SUSE)

    def test_empty_input_dict_with_default(self):
        self.assertEqual(platform_select({}, _FACTS_ROCKY8, default='fallback'), 'fallback')

    def test_empty_input_dict_without_default_raises(self):
        with self.assertRaises(AnsibleFilterError):
            platform_select({}, _FACTS_ROCKY8)

    # --- partial / odd facts --------------------------------------------

    def test_partial_facts_only_os_family(self):
        """Missing distribution/version fact entries skip those precedence steps but
        os_family matching still works."""
        facts = {'os_family': 'RedHat'}
        values = {'RedHat': 'x', 'Rocky8.10': 'y'}
        self.assertEqual(platform_select(values, facts), 'x')

    def test_empty_facts_with_default(self):
        self.assertEqual(platform_select({'RedHat': 'x'}, {}, default='none'), 'none')

    def test_empty_facts_without_default_raises(self):
        with self.assertRaises(AnsibleFilterError):
            platform_select({'RedHat': 'x'}, {})

    # --- input validation -----------------------------------------------

    def test_non_dict_input_raises(self):
        with self.assertRaises(AnsibleFilterError):
            platform_select(['not', 'a', 'dict'], _FACTS_ROCKY8)

    def test_non_dict_ansible_facts_raises(self):
        with self.assertRaises(AnsibleFilterError):
            platform_select({'RedHat': 'x'}, 'not a dict')


if __name__ == '__main__':
    unittest.main()
