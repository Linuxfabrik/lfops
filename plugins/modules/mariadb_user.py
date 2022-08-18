#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

try:
    # https://pymysql.readthedocs.io/en/latest/
    import pymysql as mysql_driver
    _mysql_cursor_param = 'cursor'
except ImportError:
    try:
        import MySQLdb as mysql_driver
        import MySQLdb.cursors
        _mysql_cursor_param = 'cursorclass'
    except ImportError:
        mysql_driver = None


DOCUMENTATION = r'''
---
module: mariadb_user
short_description: Adds or removes a user from a MariaDB database
description:
   - Adds or removes a user from a MariaDB database.
options:
  name:
    description:
      - Name of the user (role) to add or remove.
    type: str
    required: true
  password:
    description:
      - Set the user's password..
    type: str
  host:
    description:
      - The 'host' part of the MariaDB username.
    type: str
    default: localhost
  host_all:
    description:
      - Override the host option, making ansible apply changes to all hostnames for a given user.
      - This option is ignored when creating users.
    type: bool
    default: no
  priv:
    description:
      - "MariaDB privileges string in the format: C(db.table:priv1,priv2)."
      - The format is based on MariaDB C(GRANT) statement.
      - Database and table names can be quoted, MariaDB-style.
      - Has to be passed as a dictionary (see the examples).
    type: raw
  state:
    description:
      - Whether the user should exist.
      - When C(absent), removes the user.
    type: str
    choices: [ absent, present ]
    default: present

seealso:
- module: community.mysql.mysql_user

author:
- Linuxfabrik GmbH, Zurich, Switzerland

'''

EXAMPLES = r'''
- name: Removes anonymous user account for localhost
  mariadb_user:
    name: ''
    host: localhost
    state: absent

- name: Removes all anonymous user accounts
  mariadb_user:
    name: ''
    host_all: yes
    state: absent

- name: Create database user with name 'bob' and password '12345' with all database privileges
  mariadb_user:
    name: bob
    password: 12345
    priv:
      '*.*:ALL'
    state: present

- name: Create database user with password and all database privileges and 'WITH GRANT OPTION'
  mariadb_user:
    name: bob
    password: 12345
    priv:
      '*.*:ALL,GRANT'
    state: present

- name: Create user with password, all database privileges and 'WITH GRANT OPTION' in db1 and db2
  mariadb_user:
    state: present
    name: bob
    password: 12345dd
    priv:
      'db1.*': 'ALL,GRANT'
      'db2.*': 'ALL,GRANT'

- name: Ensure no user named 'sally'@'localhost' exists, also passing in the auth credentials.
  mariadb_user:
    login_user: root
    login_password: 123456
    name: sally
    state: absent

- name: Ensure no user named 'sally' exists at all
  mariadb_user:
    name: sally
    host_all: yes
    state: absent

- name: Specify grants composed of more than one word
  mariadb_user:
    name: replication
    password: 12345
    priv:
      "*.*:REPLICATION CLIENT"
    state: present

- name: Revoke all privileges for user 'bob' and password '12345'
  mariadb_user:
    name: bob
    password: 12345
    priv:
      "*.*:USAGE"
    state: present
'''


# Full version on:
# https://github.com/ansible-collections/community.mysql/blob/main/plugins/module_utils/mysql.py
def mysql_connect(module, login_host='localhost', login_port=3306, login_user='root', login_password=None,
                  cursor_class=None, connect_timeout=5,
                  autocommit=False):

    config = {}
    config['connect_timeout'] = connect_timeout
    config['host'] = login_host
    config['passwd'] = login_password
    config['port'] = int(login_port)
    config['user'] = login_user

    if _mysql_cursor_param == 'cursor':
        # In case of PyMySQL driver:
        db_connection = mysql_driver.connect(autocommit=autocommit, **config)
    else:
        # In case of MySQLdb driver
        db_connection = mysql_driver.connect(**config)
        if autocommit:
            db_connection.autocommit(True)

    # Monkey patch the Connection class to close the connection when garbage collected
    def _conn_patch(conn_self):
        conn_self.close()
    db_connection.__class__.__del__ = _conn_patch
    # Patched

    if cursor_class == 'DictCursor':
        return db_connection.cursor(**{_mysql_cursor_param: mysql_driver.cursors.DictCursor}), db_connection
    else:
        return db_connection.cursor(), db_connection


def user_get_hostnames(cursor, user):
    cursor.execute("SELECT Host FROM mysql.user WHERE user = '{user}'".format(user=user))
    hostnames_raw = cursor.fetchall()

    return [hostname_raw[0] for hostname_raw in hostnames_raw]


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        login_host=dict(type='str', required=False, default='localhost'),
        login_user=dict(type='str', required=True),
        login_password=dict(type='str', required=False, default=None, no_log=True),
        host=dict(type='str', required=False, default='localhost'),
        host_all=dict(type='bool', default=False),
        user=dict(type='str', required=True),
        password=dict(type='str', required=False, default=None, no_log=True),
        priv=dict(type='raw'),
        state=dict(type='str', default='present', choices=['absent', 'present']),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        user='',
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    if mysql_driver is None:
        module.fail_json(msg='The PyMySQL (Python 2.7 and Python 3.X) or MySQL-python (Python 2.X) module is required.')

    login_host = module.params['login_host']
    login_user = module.params['login_user']
    login_password = module.params['login_password']

    try:
        cursor, _ = mysql_connect(
            module,
            login_host=login_host,
            login_user=login_user,
            login_password=login_password
        )
    except Exception as e:
        module.fail_json(msg='Unable to connect to database, check login_user credentials.', exception=e)

    user = module.params['user']
    host = module.params['host']
    if not host:
        host = 'localhost'
    host_all = bool(module.params['host_all'])
    password = module.params['password']
    state = module.params['state']


    # https://mariadb.com/kb/en/drop-user/
    if host_all and state == 'absent':
        hostnames = user_get_hostnames(cursor, user)
        for hostname in hostnames:
            sql = "DROP USER IF EXISTS '{user}'@'{host}';".format(
                user=user,
                host=hostname,
            )
            cursor.execute(sql)
    else:
        sql = "DROP USER IF EXISTS '{user}'@'{host}';".format(
            user=user,
            host=host,
        )
        cursor.execute(sql)


    if state == 'present':

        # https://mariadb.com/kb/en/create-user/
        sql = "CREATE USER '{user}'@'{host}' IDENTIFIED BY '{password}';".format(
            user=user,
            host=host,
            password=password,
        )
        cursor.execute(sql)

        # https://mariadb.com/kb/en/grant
        for priv in module.params['priv']:
            db_table, p = priv.split(':')
            sql = "GRANT {p} ON {db_table} TO '{user}'@'{host}';".format(
                user=user,
                host=host,
                db_table=db_table,
                p=p,
            )
            cursor.execute(sql)

    result['changed'] = True
    result['user'] = user

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

if __name__ == '__main__':
    main()
