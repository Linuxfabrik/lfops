#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the nextcloud_occ_app module.

main() is driven through ansible_harness. `occ` is replaced by a fake
AnsibleModule.run_command that keeps the app states in memory and records
every command, so the tests assert which occ commands the module issues (and
which it must not issue, e.g. when idempotent or in check mode) without a
Nextcloud installation. The collection import is wired up by tests/conftest.py.

The fake `occ app:list --output=json` output follows ListApps.php of the
Nextcloud server (verified against the nextcloud-server tree at
v34.0.0beta5): `{"enabled": {"<app>": "<version>"}, "disabled": {...}}`,
where an empty section is JSON-encoded as `[]` instead of `{}`.

The module runs on the managed node, so this file also runs in the Python 3.6
(RHEL 8) tier, see tox.ini.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import unittest
import unittest.mock

import ansible_harness
from ansible.module_utils import basic
from ansible_collections.linuxfabrik.lfops.plugins.modules import (
    nextcloud_occ_app as mod,
)

_APP = 'notify_push'
_OCC = '/var/www/html/nextcloud/occ'
_PREFIX = ['php', _OCC, '--no-interaction']


class _FakeOcc:
    """In-memory stand-in for `occ app:*`."""

    def __init__(self):
        self.apps = {}  # app name -> 'enabled' / 'disabled'
        self.commands = []
        self.fail_subcommand = None  # e.g. 'app:install' -> that call fails
        self.list_rc = 0
        self.list_stdout = None  # override the app:list output

    def app_list_json(self):
        enabled = {a: '1.0.0' for a, s in self.apps.items() if s == 'enabled'}
        disabled = {a: '1.0.0' for a, s in self.apps.items() if s == 'disabled'}
        # PHP's json_encode() turns an empty array into a list
        return json.dumps(
            {'enabled': enabled or [], 'disabled': disabled or []},
        )

    def run_command(self, module, args, check_rc=False, **kwargs):
        self.commands.append(list(args))
        subcommand = next(a for a in args if a.startswith('app:'))
        if subcommand == 'app:list':
            if self.list_stdout is not None:
                return self.list_rc, self.list_stdout, ''
            return self.list_rc, self.app_list_json(), ''
        name = args[-1]
        if subcommand == self.fail_subcommand:
            rc, stderr = 1, f'Could not {subcommand} {name}'
            if check_rc:
                # what the real run_command does on a non-zero exit code
                module.fail_json(cmd=args, rc=rc, stdout='', stderr=stderr, msg=stderr)
            return rc, '', stderr
        if subcommand == 'app:install':
            self.apps[name] = 'disabled'
            return 0, f'{name} 1.0.0 installed\n', ''
        if subcommand == 'app:enable':
            self.apps[name] = 'enabled'
            return 0, f'{name} 1.0.0 enabled\n', ''
        if subcommand == 'app:disable':
            self.apps[name] = 'disabled'
            return 0, f'{name} 1.0.0 disabled\n', ''
        if subcommand == 'app:remove':
            del self.apps[name]
            return 0, f'{name} removed\n', ''
        raise AssertionError(f'unexpected occ call: {args}')

    def writes(self):
        """Return every recorded command except the read-only app:list."""
        return [c for c in self.commands if 'app:list' not in c]


class OccAppTestCase(unittest.TestCase):
    def setUp(self):
        self.occ = _FakeOcc()
        occ = self.occ

        def _run_command(module, args, check_rc=False, **kwargs):
            return occ.run_command(module, args, check_rc=check_rc, **kwargs)

        self._patchers = [
            ansible_harness.patch_module(),
            unittest.mock.patch.object(
                basic.AnsibleModule, 'run_command', _run_command
            ),
        ]
        for p in self._patchers:
            p.start()

    def tearDown(self):
        for p in reversed(self._patchers):
            p.stop()

    def _run(self, **args):
        args.setdefault('name', _APP)
        ansible_harness.set_module_args(args)
        try:
            mod.main()
        except ansible_harness.AnsibleExitJson as exc:
            return exc.args[0]
        raise AssertionError('module did not call exit_json')

    def _fail(self, **args):
        args.setdefault('name', _APP)
        ansible_harness.set_module_args(args)
        with self.assertRaises(ansible_harness.AnsibleFailJson) as ctx:
            mod.main()
        return ctx.exception.args[0]


class TestGetCurrentState(OccAppTestCase):
    """The current state comes from app:list, or from installed_apps_json."""

    def test_reads_state_from_occ_app_list(self):
        self.occ.apps = {_APP: 'disabled'}
        result = self._run(state='disabled')
        self.assertEqual(result['current_state'], 'disabled')
        self.assertEqual(self.occ.commands, [[*_PREFIX, '--output=json', 'app:list']])

    def test_empty_sections_as_json_lists(self):
        # a fresh instance with no disabled apps returns "disabled": []
        result = self._run(state='absent')
        self.assertEqual(result['current_state'], 'absent')
        self.assertFalse(result['changed'])

    def test_cached_json_string_skips_app_list(self):
        cache = json.dumps({'enabled': {_APP: '1.0.0'}, 'disabled': []})
        result = self._run(state='enabled', installed_apps_json=cache)
        self.assertEqual(result['current_state'], 'enabled')
        self.assertEqual(self.occ.commands, [])

    def test_cached_dict_skips_app_list(self):
        cache = {'enabled': {}, 'disabled': {_APP: '1.0.0'}}
        result = self._run(state='disabled', installed_apps_json=cache)
        self.assertEqual(result['current_state'], 'disabled')
        self.assertEqual(self.occ.commands, [])

    def test_uses_custom_php_and_occ_path(self):
        self._run(state='absent', php_path='/usr/bin/php82', occ_path='/srv/nc/occ')
        self.assertEqual(self.occ.commands[0][:2], ['/usr/bin/php82', '/srv/nc/occ'])


class TestEnabled(OccAppTestCase):
    def test_absent_app_is_installed_then_enabled(self):
        result = self._run(state='enabled')
        self.assertTrue(result['changed'])
        self.assertEqual(result['current_state'], 'absent')
        self.assertEqual(
            self.occ.writes(),
            [
                [*_PREFIX, 'app:install', '--keep-disabled', _APP],
                [*_PREFIX, 'app:enable', _APP],
            ],
        )
        self.assertEqual(self.occ.apps[_APP], 'enabled')
        # the result of the last command is returned
        self.assertEqual(result['rc'], 0)
        self.assertIn('enabled', result['stdout'])

    def test_force_is_passed_to_install_and_enable(self):
        self._run(state='enabled', force=True)
        self.assertEqual(
            self.occ.writes(),
            [
                [*_PREFIX, 'app:install', '--keep-disabled', '--force', _APP],
                [*_PREFIX, 'app:enable', '--force', _APP],
            ],
        )

    def test_disabled_app_is_enabled_only(self):
        self.occ.apps = {_APP: 'disabled'}
        result = self._run(state='enabled')
        self.assertTrue(result['changed'])
        self.assertEqual(self.occ.writes(), [[*_PREFIX, 'app:enable', _APP]])

    def test_enabled_app_is_left_alone(self):
        self.occ.apps = {_APP: 'enabled'}
        result = self._run(state='enabled')
        self.assertFalse(result['changed'])
        self.assertEqual(self.occ.writes(), [])

    def test_state_defaults_to_enabled(self):
        self._run()
        self.assertEqual(self.occ.apps[_APP], 'enabled')


class TestDisabled(OccAppTestCase):
    def test_enabled_app_is_disabled(self):
        self.occ.apps = {_APP: 'enabled'}
        result = self._run(state='disabled')
        self.assertTrue(result['changed'])
        self.assertEqual(self.occ.writes(), [[*_PREFIX, 'app:disable', _APP]])

    def test_disabled_app_is_left_alone(self):
        self.occ.apps = {_APP: 'disabled'}
        result = self._run(state='disabled')
        self.assertFalse(result['changed'])
        self.assertEqual(self.occ.writes(), [])

    def test_absent_app_is_not_installed(self):
        result = self._run(state='disabled')
        self.assertFalse(result['changed'])
        self.assertEqual(self.occ.writes(), [])


class TestPresent(OccAppTestCase):
    def test_absent_app_is_installed_disabled(self):
        result = self._run(state='present')
        self.assertTrue(result['changed'])
        self.assertEqual(
            self.occ.writes(), [[*_PREFIX, 'app:install', '--keep-disabled', _APP]]
        )
        self.assertEqual(self.occ.apps[_APP], 'disabled')

    def test_force_is_passed_to_install(self):
        self._run(state='present', force=True)
        self.assertEqual(
            self.occ.writes(),
            [[*_PREFIX, 'app:install', '--keep-disabled', '--force', _APP]],
        )

    def test_enabled_app_is_left_alone(self):
        self.occ.apps = {_APP: 'enabled'}
        result = self._run(state='present')
        self.assertFalse(result['changed'])
        self.assertEqual(self.occ.writes(), [])

    def test_disabled_app_is_left_alone(self):
        self.occ.apps = {_APP: 'disabled'}
        result = self._run(state='present')
        self.assertFalse(result['changed'])
        self.assertEqual(self.occ.writes(), [])


class TestAbsent(OccAppTestCase):
    def test_enabled_app_is_removed(self):
        self.occ.apps = {_APP: 'enabled'}
        result = self._run(state='absent')
        self.assertTrue(result['changed'])
        self.assertEqual(self.occ.writes(), [[*_PREFIX, 'app:remove', _APP]])
        self.assertNotIn(_APP, self.occ.apps)

    def test_disabled_app_is_removed(self):
        self.occ.apps = {_APP: 'disabled'}
        result = self._run(state='absent')
        self.assertTrue(result['changed'])
        self.assertEqual(self.occ.writes(), [[*_PREFIX, 'app:remove', _APP]])

    def test_absent_app_is_left_alone(self):
        result = self._run(state='absent')
        self.assertFalse(result['changed'])
        self.assertEqual(self.occ.writes(), [])


class TestCheckMode(OccAppTestCase):
    def test_install_is_reported_but_not_run(self):
        result = self._run(state='enabled', _ansible_check_mode=True)
        self.assertTrue(result['changed'])
        self.assertEqual(self.occ.writes(), [])
        self.assertNotIn('rc', result)

    def test_remove_is_reported_but_not_run(self):
        self.occ.apps = {_APP: 'enabled'}
        result = self._run(state='absent', _ansible_check_mode=True)
        self.assertTrue(result['changed'])
        self.assertEqual(self.occ.writes(), [])
        self.assertIn(_APP, self.occ.apps)


class TestDiff(OccAppTestCase):
    def test_diff_shows_state_transition(self):
        self.occ.apps = {_APP: 'disabled'}
        result = self._run(state='enabled', _ansible_diff=True)
        self.assertEqual(
            result['diff'],
            {'before': f'{_APP}: disabled\n', 'after': f'{_APP}: enabled\n'},
        )

    def test_diff_after_is_empty_on_removal(self):
        self.occ.apps = {_APP: 'enabled'}
        result = self._run(state='absent', _ansible_diff=True)
        self.assertEqual(result['diff']['after'], '')

    def test_no_diff_without_diff_mode(self):
        result = self._run(state='enabled')
        self.assertNotIn('diff', result)


class TestErrors(OccAppTestCase):
    def test_failing_app_list_fails(self):
        self.occ.list_rc = 1
        self.occ.list_stdout = ''
        result = self._fail(state='enabled')
        self.assertIn('Failed to list apps (rc=1)', result['msg'])
        self.assertEqual(self.occ.writes(), [])

    def test_unparsable_app_list_fails(self):
        self.occ.list_stdout = 'An unhandled exception has been thrown'
        result = self._fail(state='enabled')
        self.assertIn('Failed to parse JSON', result['msg'])
        self.assertEqual(self.occ.writes(), [])

    def test_app_list_that_is_not_an_object_fails(self):
        self.occ.list_stdout = '[]'
        result = self._fail(state='enabled')
        self.assertIn('Unexpected app list', result['msg'])
        self.assertEqual(self.occ.writes(), [])

    def test_cached_json_that_is_not_an_object_fails(self):
        result = self._fail(state='enabled', installed_apps_json='["files"]')
        self.assertIn('Unexpected app list', result['msg'])
        self.assertEqual(self.occ.commands, [])

    def test_unparsable_cached_json_fails(self):
        result = self._fail(state='enabled', installed_apps_json='{not json')
        self.assertIn('Failed to parse installed_apps_json', result['msg'])
        self.assertEqual(self.occ.commands, [])

    def test_failing_install_aborts_before_enable(self):
        self.occ.fail_subcommand = 'app:install'
        # the harness' fail_json raises an Exception subclass, which the module's
        # `except Exception` wraps into a second fail_json; the stderr survives
        result = self._fail(state='enabled')
        self.assertIn(f'Could not app:install {_APP}', result['msg'])
        self.assertEqual(
            self.occ.writes(), [[*_PREFIX, 'app:install', '--keep-disabled', _APP]]
        )

    def test_exception_from_run_command_fails(self):
        with unittest.mock.patch.object(
            basic.AnsibleModule,
            'run_command',
            side_effect=OSError('No such file or directory: php'),
        ):
            result = self._fail(state='enabled')
        self.assertIn('No such file or directory', result['msg'])


if __name__ == '__main__':
    unittest.main()
