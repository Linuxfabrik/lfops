#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Guard the play-level conventions of the playbooks.

Every play sets `force_handlers: true`. Without it, a failing task drops the
handlers notified so far, and since every later run reports the deployed file
unchanged, the running service never picks up the new config (see
"Playbooks" in CONTRIBUTING.md).

Files that only import other playbooks contain no play and are skipped.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import glob
import os
import unittest

import yaml

_REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


def _plays():
    """Yield (relative path, play) for every play in playbooks/*.yml."""
    for path in sorted(glob.glob(os.path.join(_REPO_ROOT, 'playbooks', '*.yml'))):
        with open(path, 'r') as f:
            entries = yaml.safe_load(f) or []
        for entry in entries:
            if 'hosts' in entry:
                yield os.path.relpath(path, _REPO_ROOT), entry


class TestPlaybooks(unittest.TestCase):
    def test_every_play_forces_handlers(self):
        plays = list(_plays())
        self.assertTrue(plays, 'no plays found')
        missing = [
            f'{path}: {play.get("name", "<unnamed>")}'
            for path, play in plays
            if play.get('force_handlers') is not True
        ]
        self.assertEqual(
            missing,
            [],
            'set `force_handlers: true` on these plays:\n  ' + '\n  '.join(missing),
        )

    def test_roles_internal_var_lists_the_roles_of_the_play(self):
        # A play that validates the variables of its roles in pre_tasks lists them in
        # `<playbook>__roles__internal_var`. A role missing from that list would be
        # validated only when the play reaches it, so the list has to follow the play.
        checked = 0
        for path, play in _plays():
            for key, value in (play.get('vars') or {}).items():
                if not key.endswith('__roles__internal_var'):
                    continue
                checked += 1
                listed = [item['name'] for item in value]
                in_play = [
                    entry['role'].split('.')[-1]
                    for entry in play.get('roles', [])
                    if isinstance(entry, dict) and 'role' in entry
                ]
                with self.subTest(playbook=path):
                    self.assertEqual(listed, in_play)
        self.assertTrue(checked, 'no play with a __roles__internal_var found')


if __name__ == '__main__':
    unittest.main()
