#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the sqlite_query module helpers.

These exercise connect / select / regexp / close against a real
temporary SQLite database (sqlite3 is in the standard library, so no
mocking is needed). The collection import is wired up by
tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import tempfile
import unittest

from ansible_collections.linuxfabrik.lfops.plugins.modules import sqlite_query as mod


class SqliteHelpersTestCase(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix='lfops_sqlite_test_')
        ok, self.conn = mod.connect(path=self.tmpdir, filename='test.db')
        self.assertTrue(ok)
        cur = self.conn.cursor()
        cur.execute('CREATE TABLE t (id INTEGER, name TEXT)')
        cur.execute("INSERT INTO t VALUES (1, 'alpha'), (2, 'beta'), (3, NULL)")
        self.conn.commit()

    def tearDown(self):
        mod.close(self.conn)


class TestSelect(SqliteHelpersTestCase):

    def test_as_dict(self):
        ok, rows = mod.select(self.conn, 'SELECT id, name FROM t WHERE id = 1')
        self.assertTrue(ok)
        self.assertEqual(rows, [{'id': 1, 'name': 'alpha'}])

    def test_as_tuple(self):
        ok, rows = mod.select(self.conn, 'SELECT id, name FROM t WHERE id = 1', as_dict=False)
        self.assertTrue(ok)
        self.assertEqual(tuple(rows[0]), (1, 'alpha'))

    def test_fetch_one(self):
        ok, row = mod.select(self.conn, 'SELECT id FROM t ORDER BY id', fetchone=True)
        self.assertTrue(ok)
        self.assertEqual(row, {'id': 1})

    def test_fetch_one_empty(self):
        ok, row = mod.select(self.conn, 'SELECT id FROM t WHERE id = 999', fetchone=True)
        self.assertTrue(ok)
        self.assertEqual(row, [])

    def test_named_args(self):
        ok, rows = mod.select(
            self.conn, 'SELECT name FROM t WHERE id = :wanted', data={'wanted': 2},
        )
        self.assertTrue(ok)
        self.assertEqual(rows, [{'name': 'beta'}])

    def test_bad_query_reports_failure(self):
        ok, msg = mod.select(self.conn, 'SELECT * FROM does_not_exist')
        self.assertFalse(ok)
        self.assertIn('Query failed', msg)


class TestRegexp(SqliteHelpersTestCase):

    def test_regexp_in_where(self):
        ok, rows = mod.select(self.conn, "SELECT name FROM t WHERE name REGEXP '^al'")
        self.assertTrue(ok)
        self.assertEqual(rows, [{'name': 'alpha'}])


class TestConnectFailure(unittest.TestCase):

    def test_connect_to_unwritable_path(self):
        ok, result = mod.connect(path='/nonexistent/dir/that/should/not/exist', filename='x.db')
        self.assertFalse(ok)
        self.assertIn('failed', result.lower())


if __name__ == '__main__':
    unittest.main()
