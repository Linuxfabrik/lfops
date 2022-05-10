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

# considering a virtual environment
ACTIVATE_THIS = False
venv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'linuxfabrik-venv3')
if os.path.exists(venv_path):
    ACTIVATE_THIS = os.path.join(venv_path, 'bin/activate_this.py')

if os.getenv('LINUXFABRIK_VENV3'):
    ACTIVATE_THIS = os.path.join(os.getenv('LINUXFABRIK_VENV3') + 'bin/activate_this.py')

if ACTIVATE_THIS and os.path.isfile(ACTIVATE_THIS):
    exec(open(ACTIVATE_THIS).read(), {'__file__': ACTIVATE_THIS}) # pylint: disable=W0122


import argparse # pylint: disable=C0413
import sys # pylint: disable=C0413
from termcolor import colored

import lib.base3 # pylint: disable=C0413
import lib.db_sqlite3 # pylint: disable=C0413
from lib.globals3 import STATE_OK, STATE_UNKNOWN # pylint: disable=C0413


__author__ = 'Linuxfabrik GmbH, Zurich/Switzerland'
__version__ = '2021121601'

DESCRIPTION = """A working Linuxfabrik monitoring plugin, written in Python 3, as a basis for
                further development, and much more text to help admins get this check up and
                running."""

DEFAULT_HOSTNAME = 'localhost'
DEFAULT_LENGTHY = False
DEFAULT_PATH = '../library'
DEFAULT_USERNAME = 'root'

STIG_PROFILES = [
    'CIS Apache HTTP Server 2.4',
    'CIS CentOS Linux 7',
    'CIS CentOS Linux 8',
]

# list of result codes
PASS = 0
FAIL = 1
SKIP = 2   # not applicable
TODO = 4   # needs to be implemented
REV = 8    # review manually


def parse_args():
    """Parse command line arguments using argparse.
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument(
        '-V', '--version',
        action='version',
        version='%(prog)s: v{} by {}'.format(__version__, __author__)
    )

    parser.add_argument(
        '--control-name-exclude',
        help='STIG control names to exclude, using a regular expression. Example: "^1\\.1\\.2|^1\\.1\\.4". Default: %(default)s',
        dest='CONTROL_NAME_EXCLUDE',
        default=None,
    )

    parser.add_argument(
        '--control-name-include',
        help='STIG control names to use, using a regular expression. Include comes before exclude. Example: "^1\\.1|^3". Default: %(default)s',
        dest='CONTROL_NAME_INCLUDE',
        default=None,
    )

    parser.add_argument(
        '-H', '--hostname',
        help='Host to be audited, can be IP address or hostname. Default: %(default)s',
        dest='HOSTNAME',
        default=DEFAULT_HOSTNAME,
    )

    parser.add_argument(
        '--lengthy',
        help='Extended reporting.',
        dest='LENGTHY',
        action='store_true',
        default=DEFAULT_LENGTHY,
    )

    parser.add_argument(
        '--path',
        help='Local path to stig.db. Default: %(default)s',
        dest='PATH',
        default=DEFAULT_PATH,
    )

    parser.add_argument(
        '--profile-name',
        help='STIG profile to audit.',
        dest='PROFILE_NAME',
        choices=STIG_PROFILES,
        required=True,
    )

    parser.add_argument(
        '--profile-version',
        help='STIG profile version. To be specific, use something like "v3.1.2". Default: %(default)s',
        dest='PROFILE_VERSION',
        default='latest',
    )

    parser.add_argument(
        '--username',
        help='Remote SSH Username. Default: %(default)s',
        dest='USERNAME',
        default=DEFAULT_USERNAME,
    )

    return parser.parse_args()


def get_latest(args):
    """Get latest audit from local STIG database (SQLite).
    """
    success, conn = lib.db_sqlite3.connect(path=args.PATH, filename='stig.db')
    if not success:
        return False

    # Get a list of matching profile remediations from the STIG database
    if args.PROFILE_VERSION == 'latest':
        success, result = lib.db_sqlite3.select(
            conn,
            """SELECT profile_version
            FROM profile
            WHERE
              profile_name = :profile_name
            ORDER BY profile_version DESC
            LIMIT 1""",
            data={
                'profile_name': args.PROFILE_NAME,
            },
        )
        lib.db_sqlite3.close(conn)
        return result[0]['profile_version']

    lib.db_sqlite3.close(conn)
    return args.PROFILE_VERSION


def get_audits(args):
    """Get audits from local STIG database (SQLite).
    """
    success, conn = lib.db_sqlite3.connect(path=args.PATH, filename='stig.db')
    if not success:
        return False

    data = {}
    sql = """SELECT *
        FROM profile as p
        LEFT JOIN control as c ON p.control_id = c.id
        WHERE
          profile_name = :profile_name
          and profile_version = :profile_version
        """
    if args.CONTROL_NAME_INCLUDE:
        sql += 'and control_name REGEXP :control_name_include\n'
        data['control_name_include'] = args.CONTROL_NAME_INCLUDE
    if args.CONTROL_NAME_EXCLUDE:
        sql += 'and control_name NOT REGEXP :control_name_exclude\n'
        data['control_name_exclude'] = args.CONTROL_NAME_EXCLUDE
    sql += 'ORDER BY exec_order ASC'
    data['profile_name'] = args.PROFILE_NAME
    data['profile_version'] = get_latest(args)
    success, result = lib.db_sqlite3.select(conn, sql, data)
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
    return result


def retc2str(retc):
    if retc == PASS:
        return colored('Passed', 'green')
    if retc == FAIL:
        return colored('Failed', 'red')
    if retc == SKIP:
        return colored('Skipped', 'yellow')
    if retc == TODO:
        return colored('TODO', 'magenta')
    if retc == REV:
        return colored('Review', 'blue')


def get_grade(percentage):
    if percentage >= 97:
        return colored('A+', 'green', attrs=['bold'])
    if percentage >= 93:
        return colored('A', 'green', attrs=['bold'])
    if percentage >= 90:
        return colored('A-', 'green', attrs=['bold'])
    if percentage >= 87:
        return colored('B+', 'yellow', attrs=['bold'])
    if percentage >= 83:
        return colored('B', 'yellow', attrs=['bold'])
    if percentage >= 80:
        return colored('B-', 'yellow', attrs=['bold'])
    if percentage >= 77:
        return colored('C+', 'yellow', attrs=['bold'])
    if percentage >= 73:
        return colored('C', 'yellow', attrs=['bold'])
    if percentage >= 70:
        return colored('C-', 'yellow', attrs=['bold'])
    if percentage >= 67:
        return colored('D+', 'red', attrs=['bold'])
    if percentage >= 63:
        return colored('D', 'red', attrs=['bold'])
    if percentage >= 60:
        return colored('D-', 'red', attrs=['bold'])
    return colored('F', 'red', attrs=['bold'])


def main():
    """The main function. Hier spielt die Musik.
    """

    # parse the command line, exit with UNKNOWN if it fails
    try:
        args = parse_args()
    except SystemExit:
        sys.exit(STATE_UNKNOWN)

    # get all audits that has to be done
    audits = get_audits(args)
    if not audits:
        lib.base3.oao('No audit tasks found.')

    # init some vars
    total_score = 0
    host_score = 0
    percentage = 0
    prolog = ''

    msg = 'Audit Result\n============\n\n'

    # prepare the host, copy shell libraries
    cmd = 'scp audits/lib.sh {}@{}:/tmp/'.format(
        args.USERNAME,
        args.HOSTNAME,
    )
    stdout, stderr, retc = lib.base3.coe(lib.base3.shell_exec(cmd))
    cmd = 'scp audits/lib-apache-httpd.sh {}@{}:/tmp/'.format(
        args.USERNAME,
        args.HOSTNAME,
    )
    stdout, stderr, retc = lib.base3.coe(lib.base3.shell_exec(cmd))
    # The scp utility exits 0 on success, and >0 if an error occurs.
    if retc != 0:
        print(f'The command "{cmd}" failed with:\n{stderr}')
        sys.exit(STATE_UNKNOWN)

    # progress bar
    count = len(audits)
    if count == 0:
        increase = 100
    else:
        increase = 100 / count
    progress = 0

    # run the audit on the specified host via ssh
    # this code section is ok for the moment, but could be improved in the future
    table_values = []
    for audit in audits:
        # print the progress bar
        print('{}% ({}){}'.format(round(progress), audit['control_name'], ' '*40) , end='\r')
        progress += increase

        if audit['audit_name'] and os.path.isfile('audits/' + audit['audit_name']) and audit['control_id']:
            cmd = 'ssh {}@{} "sudo bash -s --" < audits/{}'.format(
                    args.USERNAME,
                    args.HOSTNAME,
                    audit['audit_name'],
            )
            stdout, stderr, retc = lib.base3.coe(lib.base3.shell_exec(cmd, shell=True))
            # ssh exits with the exit status of the remote command or with 255 if an error occurred.
            if retc == 255:
                print(f'The command "{cmd}" failed with:\n{stderr}')
                sys.exit(STATE_UNKNOWN)

            # todo do error handling
            if stdout:
                prolog += stdout.strip() + '\n\n\n'
        else:
            # there is no script for auditing provided, seems to be not implemented
            retc = TODO
        table_values.append({
            'control_name': audit['control_name'],
            'scored': 'Scored' if audit['automated'] == 1 else 'Not Scored',
            'level': audit['server_level'],
            'result': retc2str(retc),
            'audit_name': audit['audit_name'],
        })
        # calculate the score based on the plugin return code (but only if this is a scored test)
        if audit['automated'] == 1:
            if retc == PASS:
                total_score += audit['server_level']
                host_score += audit['server_level']
            if retc == FAIL:
                total_score += audit['server_level']
    print(' '*85, end='\r')     # clear the progress bar

    if total_score:
        percentage = round(host_score / total_score * 100, 1)

    # build the message
    if prolog:
        msg += '{}\n\n\n'.format(prolog.strip())
    msg += 'Summary Table\n-------------\n\n'
    if args.LENGTHY:
        msg += lib.base3.get_table(
            table_values,
            ['control_name', 'audit_name', 'scored', 'level', 'result'],
            header=['Control', 'Script', 'Scoring', 'Lvl', 'Result'],
        )
    else:
        msg += lib.base3.get_table(
            table_values,
            ['control_name', 'result'],
            header=['Control', 'Result'],
        )
    msg += '\n\n'

    msg += 'Profile\n-------\n\n'
    msg += '* Benchmark: {} ({})\n* Host:      ``{}``\n* Datetime:  {}\n'.format(
        args.PROFILE_NAME,
        get_latest(args),
        args.HOSTNAME,
        lib.base3.now(as_type='iso'),
    )

    if total_score:
        msg += '* Score:     {}/{} {} ({}%)\n* Grade:     {}'.format(
            host_score,
            total_score,
            lib.base3.pluralize('point', total_score),
            percentage,
            get_grade(percentage),
        )

    # over and out
    lib.base3.oao(msg)


if __name__ == '__main__':
    try:
        main()
    except Exception:   # pylint: disable=W0703
        lib.base3.cu()
