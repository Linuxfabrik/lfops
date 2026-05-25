#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sqlite_query
short_description: Run a read-only SQLite query
version_added: "2.0.0"
description:
    - Connects to a SQLite database file and runs a single C(SELECT) query against it.
    - The query is parameterized via I(named_args) using SQLite's named placeholders (e.g. C(:my_arg)), so user-provided values do not have to be string-concatenated into the SQL.
    - The connection is opened with a 1-second busy timeout, returns rows as dictionaries by default, and registers a Python-backed C(REGEXP) function so that C(WHERE col REGEXP '...') works (SQLite has no built-in regex implementation).
    - The module is read-only by design - C(query_type) currently only accepts C(select), no transaction is committed, and the connection is closed (without commit) at the end. As a result, the module always reports C(changed=false).
author:
    - Linuxfabrik GmbH, Zurich, Switzerland
options:
    as_dict:
        description:
            - When C(true) (the default), each result row is returned as a dictionary keyed by column name. When C(false), rows are returned as positional tuples.
        type: bool
        default: true
    db:
        description:
            - Filename of the SQLite database file. Combined with I(path) using C(os.path.join) to form the full path.
        type: str
        required: true
    fetch_one:
        description:
            - When C(true), return only the first row of the result set instead of all rows. If there are no rows, an empty list is returned.
        type: bool
        default: false
    named_args:
        description:
            - Dictionary of values bound to SQLite named placeholders (C(:name)) inside I(query). Use this instead of formatting values into the SQL string to avoid injection.
        type: dict
    path:
        description:
            - Directory the database file lives in. Combined with I(db) to form the full path.
        type: str
        required: true
    query:
        description:
            - The SQL C(SELECT) statement to run. Use named placeholders (C(:name)) for any user-provided values and pass them through I(named_args).
        type: str
        required: true
    query_type:
        description:
            - Type of SQL query to run. Currently only C(select) is implemented; the option exists to leave room for future write-capable variants.
        type: str
        choices: ['select']
        default: 'select'
'''

EXAMPLES = r'''
- name: 'Simple select query'
  linuxfabrik.lfops.sqlite_query:
    db: 'acme.db'
    path: '{{ role_path }}/library'
    query: 'SELECT sqlite_version();'

- name: 'Parameterized select query'
  linuxfabrik.lfops.sqlite_query:
    db: 'stig.db'
    path: '{{ role_path }}/library'
    query: 'SELECT control_id FROM profile WHERE profile_name = :profile_name AND enabled = :enabled'
    named_args:
      profile_name: 'CIS CentOS 7'
      enabled: 1
  delegate_to: 'localhost'
'''

RETURN = r'''
changed:
    description: Always C(false). The module never modifies the database.
    returned: always
    type: bool
    sample: false
query:
    description: The SQL query that was executed, echoed back unchanged.
    returned: always
    type: str
    sample: 'SELECT control_id FROM profile WHERE enabled = :enabled'
query_type:
    description: The query type that was executed.
    returned: always
    type: str
    sample: 'select'
query_result:
    description:
        - Rows returned by the query.
        - With I(as_dict=true) (default), a list of dicts keyed by column name; with I(as_dict=false), a list of positional tuples.
        - With I(fetch_one=true), only the first row is returned (as a single dict / tuple), or an empty list if the query produced no rows.
    returned: always
    type: list
rowcount:
    description: Number of rows in I(query_result). With I(fetch_one=true) this is C(0) when no rows were returned and C(1) (or the field count of the row) otherwise, since C(len()) is taken over the returned object.
    returned: always
    type: int
    sample: 42
'''


import os
import re
import sqlite3

from ansible.module_utils.basic import AnsibleModule

# the close / connect / select / regexp helpers below are taken from
# https://git.linuxfabrik.ch/linuxfabrik/lib/-/blob/master/db_mysql3.py


def close(conn):
    """This closes the database connection. Note that this does not
    automatically call commit(). If you just close your database connection
    without calling commit() first, your changes will be lost.
    """
    try:
        conn.close()
    except Exception:
        pass
    return True


def connect(path='', filename=''):
    """Connect to a SQLite database file. If path is ommitted, the
    temporary directory is used. If filename is ommitted,
    `linuxfabrik-plugins.db` is used.
    """
    db = os.path.join(path, filename)
    try:
        conn = sqlite3.connect(db, timeout=1)
        # https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
        conn.row_factory = sqlite3.Row
        # https://stackoverflow.com/questions/3425320/sqlite3-programmingerror-you-must-not-use-8-bit-bytestrings-unless-you-use-a-te
        conn.text_factory = str
        conn.create_function("REGEXP", 2, regexp)
    except Exception as e:
        return (False, f'Connecting to DB {db} failed, Error: {e}, CWD: {os.getcwd()}')
    return (True, conn)


def select(conn, sql, data=None, fetchone=False, as_dict=True):
    """The SELECT statement is used to query the database. The result of a
    SELECT is zero or more rows of data where each row has a fixed number
    of columns. A SELECT statement does not make any changes to the
    database.
    """
    if data is None:
        data = {}
    c = conn.cursor()
    try:
        if data:
            c.execute(sql, data)
        else:
            c.execute(sql)
        # https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
        if as_dict:
            if fetchone:
                try:
                    return (True, [dict(row) for row in c.fetchall()][0])
                except IndexError:
                    return (True, [])
            return (True, [dict(row) for row in c.fetchall()])
        if fetchone:
            return (True,  c.fetchone())
        return (True, c.fetchall())
    except Exception as e:
        return (False, f'Query failed: {sql}, Error: {e}, Data: {data}')


def regexp(expr, item):
    """The SQLite engine does not support a REGEXP implementation by default. This has to be
    done by the client.
    For Python, you have to implement REGEXP using a Python function at runtime.
    https://stackoverflow.com/questions/5365451/problem-with-regexp-python-and-sqlite/5365533#5365533
    """
    if item is None:
        # a NULL column value cannot match a regex (and re.search(None) raises)
        return False
    reg = re.compile(expr)
    return reg.search(item) is not None


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        as_dict=dict(type='bool', default=True),
        db=dict(type='str', required=True),
        fetch_one=dict(type='bool', default=False),
        named_args=dict(type='dict', default={}),
        path=dict(type='str', required=True),
        query=dict(type='str', required=True),
        query_type=dict(default='select', choices=['select']),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    as_dict = module.params['as_dict']
    db = module.params['db']
    fetch_one = module.params['fetch_one']
    named_args = module.params['named_args']
    path = module.params['path']
    query = module.params['query']
    query_type = module.params['query_type']

    success, conn = connect(path=path, filename=db)
    if not success:
        module.fail_json(msg=f'Unable to connect to database: {conn}')

    query_result = []
    if query_type == 'select':
        success, query_result = select(conn, query, named_args, fetchone=fetch_one, as_dict=as_dict)
        changed = False
        if not success:
            close(conn)
            # query_result holds the error message when the query failed
            module.fail_json(msg=query_result)
    close(conn)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    kw = dict(
        changed=changed,
        query=query,
        query_type=query_type,
        query_result=query_result,
        rowcount=len(query_result),
    )
    module.exit_json(**kw)


if __name__ == '__main__':
    main()
