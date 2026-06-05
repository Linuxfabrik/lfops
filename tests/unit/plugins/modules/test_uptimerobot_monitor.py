#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the uptimerobot_monitor pure normalizers.

These reduce the API form and the user/wire form of alert_contacts and
mwindows to the same canonical, order-independent string, which is what
keeps the module idempotent. The collection import is wired up by
tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

from ansible_collections.linuxfabrik.lfops.plugins.modules import uptimerobot_monitor as mod


class TestNormalizeAlertContacts(unittest.TestCase):

    def test_current_is_sorted_by_id(self):
        current = [
            {'id': 2, 'threshold': 5, 'recurrence': 0, 'friendly_name': 'b'},
            {'id': 1, 'threshold': 0, 'recurrence': 0, 'friendly_name': 'a'},
        ]
        self.assertEqual(mod._normalize_current_alert_contacts(current), '1_0_0-2_5_0')

    def test_empty_current(self):
        self.assertEqual(mod._normalize_current_alert_contacts([]), '')

    def test_desired_wire_is_sorted(self):
        self.assertEqual(mod._normalize_desired_alert_contacts('2_5_0-1_0_0'), '1_0_0-2_5_0')

    def test_current_and_desired_match_when_equivalent(self):
        current = [{'id': 1, 'threshold': 0, 'recurrence': 0},
                   {'id': 2, 'threshold': 5, 'recurrence': 0}]
        self.assertEqual(
            mod._normalize_current_alert_contacts(current),
            mod._normalize_desired_alert_contacts('2_5_0-1_0_0'),
        )


class TestNormalizeMwindows(unittest.TestCase):

    def test_current_sorted(self):
        self.assertEqual(mod._normalize_current_mwindows([{'id': 3}, {'id': 1}]), '1-3')

    def test_desired_sorted(self):
        self.assertEqual(mod._normalize_desired_mwindows('3-1-2'), '1-2-3')

    def test_empty(self):
        self.assertEqual(mod._normalize_current_mwindows([]), '')
        self.assertEqual(mod._normalize_desired_mwindows(''), '')


if __name__ == '__main__':
    unittest.main()
