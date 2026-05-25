#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the uptimerobot_mwindow pure time helpers.

The collection import is wired up by tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

from ansible_collections.linuxfabrik.lfops.plugins.modules import uptimerobot_mwindow as mod


class TestHhmmToMinutes(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(mod._hhmm_to_minutes('00:00'), 0)
        self.assertEqual(mod._hhmm_to_minutes('01:30'), 90)
        self.assertEqual(mod._hhmm_to_minutes('23:59'), 1439)


class TestComputeDuration(unittest.TestCase):

    def test_same_day(self):
        self.assertEqual(mod._compute_duration('09:00', '17:00'), 480)

    def test_wraps_over_midnight(self):
        self.assertEqual(mod._compute_duration('22:00', '02:00'), 240)

    def test_equal_start_end_is_full_day(self):
        # duration <= 0 wraps to a full 24h window
        self.assertEqual(mod._compute_duration('03:00', '03:00'), 1440)


class TestSynthesiseName(unittest.TestCase):

    def test_with_value(self):
        params = {'type': 'weekly', 'value': 'mon-wed', 'start_time': '03:30', 'end_time': '05:30'}
        self.assertEqual(mod._synthesise_name(params), 'weekly mon-wed 03:30-05:30')

    def test_without_value(self):
        params = {'type': 'daily', 'start_time': '01:00', 'end_time': '02:00'}
        self.assertEqual(mod._synthesise_name(params), 'daily 01:00-02:00')


if __name__ == '__main__':
    unittest.main()
