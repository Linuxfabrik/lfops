#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: sqlite
short_description: Run SQLite queries
description:
   - Runs arbitrary SQLite queries.
options:
  as_dict:
    description:
    - Return a key-value dictionary (default), or a list of values.
    type: bool
    default: true
  db:
    description:
    - Filename of the SQLite db file to connect to and run queries against.
    type: str
    required: true
  fetch_one:
    description:
    - Just return the first item found.
    type: bool
    default: false
  named_args:
    description:
    - Dictionary of key-value arguments to pass to the query.
    type: dict
  path:
    description:
    - Path to the SQLite db file.
    type: str
    required: true
  query:
    description:
    - SQL query to run.
    type: str
    required: true
  query_type:
    description:
    - SQL query type to run. Currently only 'select', but might be more in future versions.
    type: str
    choices: select
    default: select
author:
- Linuxfabrik GmbH, Zurich, Switzerland
'''

EXAMPLES = r'''
- name: Simple select query
  sqlite_query:
    db: acme.db
    path: "{{ role_path }}/library"
    query: SELECT sqlite_version();

- name: Extended select query
  sqlite_query:
    db: stig.db
    path: "{{ role_path }}/library"
    query_type: select
    query: SELECT control_id FROM profile WHERE profile_name = :profile_name and enabled = :enabled
    named_args:
      profile_name: CIS CentOS 7
      enabled: 1
  delegate_to: localhost
'''


from ansible.module_utils.basic import AnsibleModule


# all sqlite functions taken from
# https://git.linuxfabrik.ch/linuxfabrik/lib/-/blob/master/db_mysql3.py
import os
import sqlite3
import re


def close(conn):
    """This closes the database connection. Note that this does not
    automatically call commit(). If you just close your database connection
    without calling commit() first, your changes will be lost.
    """
    try:
        conn.close()
    except:
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
        return(False, 'Connecting to DB {} failed, Error: {}, CWD: {}'.format(db, e, os.getcwd()))
    return (True, conn)


def select(conn, sql, data={}, fetchone=False, as_dict=True):
    """The SELECT statement is used to query the database. The result of a
    SELECT is zero or more rows of data where each row has a fixed number
    of columns. A SELECT statement does not make any changes to the
    database.
    """
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
        return(False, 'Query failed: {}, Error: {}, Data: {}'.format(sql, e, data))


def regexp(expr, item):
    """The SQLite engine does not support a REGEXP implementation by default. This has to be
    done by the client.
    For Python, you have to implement REGEXP using a Python function at runtime.
    https://stackoverflow.com/questions/5365451/problem-with-regexp-python-and-sqlite/5365533#5365533
    """
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
        module.fail_json(msg='Unable to connect to database: {}'.format(conn))

    query_result = []
    if query_type == 'select':
        success, query_result = select(conn, query, named_args, fetchone=fetch_one, as_dict=as_dict)
        changed = False
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
