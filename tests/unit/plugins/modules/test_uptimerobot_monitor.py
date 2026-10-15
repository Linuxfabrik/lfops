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

from ansible_collections.linuxfabrik.lfops.plugins.modules import (
    uptimerobot_monitor as mod,
)


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
        self.assertEqual(
            mod._normalize_desired_alert_contacts('2_5_0-1_0_0'), '1_0_0-2_5_0'
        )

    def test_current_and_desired_match_when_equivalent(self):
        current = [
            {'id': 1, 'threshold': 0, 'recurrence': 0},
            {'id': 2, 'threshold': 5, 'recurrence': 0},
        ]
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


class TestApplySubTypePort(unittest.TestCase):
    # UptimeRobot ignores sub_type on edit and reports 1 for it on every port
    # monitor, so a preset has to travel, and compare, as its port.

    def test_preset_adds_its_port(self):
        self.assertEqual(
            mod._apply_sub_type_port({'sub_type': 'https'}),
            {'sub_type': 'https', 'port': 443},
        )

    def test_explicit_port_wins(self):
        self.assertEqual(
            mod._apply_sub_type_port({'sub_type': 'https', 'port': 8443}),
            {'sub_type': 'https', 'port': 8443},
        )

    def test_custom_and_missing_sub_type_add_nothing(self):
        self.assertEqual(
            mod._apply_sub_type_port({'sub_type': 'custom', 'port': 2222}),
            {'sub_type': 'custom', 'port': 2222},
        )
        self.assertEqual(mod._apply_sub_type_port({'url': 'x'}), {'url': 'x'})

    def test_preset_matches_the_port_the_api_reports(self):
        # getMonitors returns sub_type 1 and port 443 for an https preset, which
        # must not count as a change.
        current = {'sub_type': 1, 'port': 443}
        desired = mod._apply_sub_type_port({'sub_type': 'https'})
        self.assertEqual(
            mod.ur.diff_for_update(current, desired, ['port']),
            {},
        )


if __name__ == '__main__':
    unittest.main()
