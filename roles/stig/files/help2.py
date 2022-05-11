#! /usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

# https://git.linuxfabrik.ch/linuxfabrik-icinga-plugins/checks-linux/-/blob/master/CONTRIBUTING.md

"""Have a look at the check's README for further details.
"""

import os

import sys # pylint: disable=C0413

import lib.base3 # pylint: disable=C0413
import lib.db_sqlite3 # pylint: disable=C0413
from lib.globals3 import STATE_OK, STATE_UNKNOWN # pylint: disable=C0413


def main():
    success, conn = lib.db_sqlite3.connect(path='.', filename='stig.db')
    if not success:
        return False

    success, result = lib.db_sqlite3.select(
        conn,
        """SELECT control_name, control_id
        FROM profile
        WHERE
          profile_name = 'CIS CentOS Linux 8'
          and profile_version = 'v1.0.1'
        ORDER BY exec_order ASC""",
    )
    if not success:
        # error accessing or querying the cache
        lib.db_sqlite3.close(conn)
        return False

    if not result or result is None:
        # key not found
        lib.db_sqlite3.close(conn)
        return False

    # return the value
    lib.db_sqlite3.close(conn)

    for audit in result:
        in_filename = audit['control_name'].split(' ')[0].strip() + '.sh'
        if audit['control_id'] is not None:
            out_filename = audit['control_id'].strip() + '.sh'
            cmd = 'mv audits/{} audits/{}'.format(in_filename, out_filename)
            lib.base3.shell_exec(cmd)


if __name__ == '__main__':
    try:
        main()
    except Exception:   # pylint: disable=W0703
        lib.base3.cu()
