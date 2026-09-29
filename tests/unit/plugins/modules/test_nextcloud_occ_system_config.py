#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the nextcloud_occ_system_config module.

main() is driven through ansible_harness. `occ` is replaced by a fake
AnsibleModule.run_command that keeps the system config in memory and records
every command, so the tests assert which occ commands the module issues (and
which it must not issue, e.g. when idempotent or in check mode) without a
Nextcloud installation. The collection import is wired up by tests/conftest.py.

The fake `occ config:system:get` follows GetConfig.php and Base.php of the
Nextcloud server (verified against the nextcloud-server tree at
v34.0.0beta5): a missing key exits with rc 1 and no output, a scalar is
printed on its own line, booleans as `true` / `false`. The cached path reads
the `system` section of `occ config:list --output=json --private`, where
arrays such as `trusted_domains` are JSON lists.

The module runs on the managed node, so this file also runs in the Python 3.6
(RHEL 8) tier, see tox.ini.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import unittest
import unittest.mock
from typing import ClassVar

import ansible_harness
from ansible.module_utils import basic
from ansible_collections.linuxfabrik.lfops.plugins.modules import (
    nextcloud_occ_system_config as mod,
)

_OCC = '/var/www/html/nextcloud/occ'
_PREFIX = ['php', _OCC, '--no-interaction']


def _to_occ_string(value):
    """Render a stored value the way `occ config:system:get` prints it."""
    if isinstance(value, bool):
        return 'true' if value else 'false'
    return str(value)


def _cast(value, value_type):
    """Mirror what CastHelper stores for `config:system:set --type`."""
    if value_type == 'boolean':
        return value == 'true'
    if value_type == 'integer':
        return int(value)
    if value_type == 'double':
        return float(value)
    return value


class _FakeOcc:
    """In-memory stand-in for `occ config:system:{get,set,delete}`."""

    def __init__(self):
        self.config = {}
        self.commands = []
        self.fail_set = False

    def _lookup(self, parts):
        node = self.config
        for part in parts:
            if isinstance(node, list):
                index = int(part)
                if index >= len(node):
                    return False, None
                node = node[index]
            elif isinstance(node, dict) and part in node:
                node = node[part]
            else:
                return False, None
        return True, node

    def run_command(self, module, args, check_rc=False, **kwargs):
        self.commands.append(list(args))
        subcommand = args[3]
        if subcommand == 'config:system:get':
            found, value = self._lookup(args[4:])
            if not found:
                return 1, '', ''
            return 0, _to_occ_string(value) + '\n', ''
        if subcommand == 'config:system:set':
            if self.fail_set:
                stderr = 'Cannot set value'
                if check_rc:
                    # what the real run_command does on a non-zero exit code
                    module.fail_json(
                        cmd=args, rc=1, stdout='', stderr=stderr, msg=stderr
                    )
                return 1, '', stderr
            value = args[4][len('--value=') :]
            value_type = args[5][len('--type=') :]
            parts = args[6:]
            node = self.config
            for part in parts[:-1]:
                node = node.setdefault(part, {})
            if isinstance(node, list):
                # PHP arrays: setting the next index appends
                index = int(parts[-1])
                if index == len(node):
                    node.append(None)
                node[index] = _cast(value, value_type)
            else:
                node[parts[-1]] = _cast(value, value_type)
            return 0, f'System config value {" => ".join(parts)} set to {value}\n', ''
        if subcommand == 'config:system:delete':
            parts = args[4:]
            node = self.config
            for part in parts[:-1]:
                node = node[part]
            del node[parts[-1]]
            return 0, f'System config value {" => ".join(parts)} deleted\n', ''
        raise AssertionError(f'unexpected occ call: {args}')

    def writes(self):
        """Return every recorded command except the read-only config:system:get."""
        return [c for c in self.commands if c[3] != 'config:system:get']


class OccSystemConfigTestCase(unittest.TestCase):
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
        ansible_harness.set_module_args(args)
        try:
            mod.main()
        except ansible_harness.AnsibleExitJson as exc:
            return exc.args[0]
        raise AssertionError('module did not call exit_json')

    def _fail(self, **args):
        ansible_harness.set_module_args(args)
        with self.assertRaises(ansible_harness.AnsibleFailJson) as ctx:
            mod.main()
        return ctx.exception.args[0]


class TestPresent(OccSystemConfigTestCase):
    def test_missing_key_is_set(self):
        result = self._run(name='maintenance_window_start', value='1', type='integer')
        self.assertTrue(result['changed'])
        self.assertEqual(result['current_value'], '')
        self.assertEqual(
            self.occ.writes(),
            [
                [
                    *_PREFIX,
                    'config:system:set',
                    '--value=1',
                    '--type=integer',
                    'maintenance_window_start',
                ]
            ],
        )
        self.assertEqual(self.occ.config['maintenance_window_start'], 1)
        self.assertEqual(result['rc'], 0)
        self.assertIn('set to 1', result['stdout'])

    def test_differing_value_is_updated(self):
        self.occ.config = {'default_language': 'en'}
        result = self._run(name='default_language', value='de')
        self.assertTrue(result['changed'])
        self.assertEqual(result['current_value'], 'en')
        self.assertEqual(
            self.occ.writes(),
            [
                [
                    *_PREFIX,
                    'config:system:set',
                    '--value=de',
                    '--type=string',
                    'default_language',
                ]
            ],
        )

    def test_matching_value_is_left_alone(self):
        self.occ.config = {'default_language': 'de'}
        result = self._run(name='default_language', value='de')
        self.assertFalse(result['changed'])
        self.assertEqual(result['current_value'], 'de')
        self.assertEqual(self.occ.writes(), [])

    def test_nested_key_is_split_into_arguments(self):
        self.occ.config = {'trusted_domains': ['localhost']}
        result = self._run(name='trusted_domains 1', value='cloud.example.com')
        self.assertTrue(result['changed'])
        self.assertEqual(
            self.occ.commands[0],
            [*_PREFIX, 'config:system:get', 'trusted_domains', '1'],
        )
        self.assertEqual(
            self.occ.writes()[0][-2:],
            ['trusted_domains', '1'],
        )

    def test_nested_key_matching_is_left_alone(self):
        self.occ.config = {'trusted_domains': ['localhost', 'cloud.example.com']}
        result = self._run(name='trusted_domains 1', value='cloud.example.com')
        self.assertFalse(result['changed'])
        self.assertEqual(self.occ.writes(), [])

    def test_value_is_required(self):
        result = self._fail(name='default_language')
        self.assertIn('value', result['msg'])
        self.assertEqual(self.occ.commands, [])


class TestBoolean(OccSystemConfigTestCase):
    """Truthy spellings become 'true', everything else 'false'."""

    def test_truthy_spellings_become_true(self):
        for spelling in ('true', 'True', '1', 'on', 'YES'):
            with self.subTest(spelling=spelling):
                self.occ.commands = []
                self.occ.config = {}
                self._run(name='debug', value=spelling, type='boolean')
                self.assertIn('--value=true', self.occ.writes()[0])
                self.assertIs(self.occ.config['debug'], True)

    def test_other_spellings_become_false(self):
        for spelling in ('false', '0', 'off', 'no', 'anything'):
            with self.subTest(spelling=spelling):
                self.occ.commands = []
                self.occ.config = {}
                self._run(name='debug', value=spelling, type='boolean')
                self.assertIn('--value=false', self.occ.writes()[0])
                self.assertIs(self.occ.config['debug'], False)

    def test_stored_boolean_matches_yes(self):
        self.occ.config = {'check_for_working_wellknown_setup': True}
        result = self._run(
            name='check_for_working_wellknown_setup', value='yes', type='boolean'
        )
        self.assertFalse(result['changed'])
        self.assertEqual(result['current_value'], 'true')
        self.assertEqual(self.occ.writes(), [])


class TestAbsent(OccSystemConfigTestCase):
    def test_existing_key_is_deleted(self):
        self.occ.config = {'debug': True}
        result = self._run(name='debug', state='absent')
        self.assertTrue(result['changed'])
        self.assertEqual(result['current_value'], 'true')
        self.assertEqual(
            self.occ.writes(), [[*_PREFIX, 'config:system:delete', 'debug']]
        )
        self.assertNotIn('debug', self.occ.config)

    def test_nested_key_is_deleted(self):
        self.occ.config = {'trusted_domains': {'0': 'localhost', '1': 'a.example.com'}}
        self._run(name='trusted_domains 1', state='absent')
        self.assertEqual(
            self.occ.writes(),
            [[*_PREFIX, 'config:system:delete', 'trusted_domains', '1']],
        )

    def test_missing_key_is_left_alone(self):
        result = self._run(name='debug', state='absent')
        self.assertFalse(result['changed'])
        self.assertEqual(result['current_value'], '')
        self.assertEqual(self.occ.writes(), [])


class TestCachedConfig(OccSystemConfigTestCase):
    """installed_config_json replaces config:system:get."""

    _CACHE: ClassVar[dict] = {
        'system': {
            'debug': False,
            'default_language': 'de',
            'maintenance_window_start': 1,
            'trusted_domains': ['localhost', 'cloud.example.com'],
        },
        'apps': {},
    }

    def test_matching_string_from_dict(self):
        result = self._run(
            name='default_language', value='de', installed_config_json=self._CACHE
        )
        self.assertFalse(result['changed'])
        self.assertEqual(self.occ.commands, [])

    def test_matching_value_from_json_string(self):
        result = self._run(
            name='maintenance_window_start',
            value='1',
            type='integer',
            installed_config_json=json.dumps(self._CACHE),
        )
        self.assertFalse(result['changed'])
        self.assertEqual(self.occ.commands, [])

    def test_boolean_is_compared_lowercase(self):
        result = self._run(
            name='debug',
            value='false',
            type='boolean',
            installed_config_json=self._CACHE,
        )
        self.assertFalse(result['changed'])
        self.assertEqual(result['current_value'], 'false')

    def test_list_element_by_index(self):
        result = self._run(
            name='trusted_domains 1',
            value='cloud.example.com',
            installed_config_json=self._CACHE,
        )
        self.assertFalse(result['changed'])
        self.assertEqual(self.occ.commands, [])

    def test_list_index_out_of_range_is_missing(self):
        result = self._run(
            name='trusted_domains 5',
            value='new.example.com',
            installed_config_json=self._CACHE,
        )
        self.assertTrue(result['changed'])
        self.assertEqual(result['current_value'], '')
        self.assertEqual(self.occ.writes()[0][-2:], ['trusted_domains', '5'])

    def test_non_numeric_list_index_is_missing(self):
        result = self._run(
            name='trusted_domains foo',
            state='absent',
            installed_config_json=self._CACHE,
        )
        self.assertFalse(result['changed'])
        self.assertEqual(self.occ.commands, [])

    def test_descending_into_a_scalar_is_missing(self):
        result = self._run(
            name='default_language sub',
            state='absent',
            installed_config_json=self._CACHE,
        )
        self.assertFalse(result['changed'])

    def test_missing_key_is_left_alone_on_absent(self):
        result = self._run(
            name='redis', state='absent', installed_config_json=self._CACHE
        )
        self.assertFalse(result['changed'])
        self.assertEqual(self.occ.commands, [])

    def test_existing_key_is_deleted_on_absent(self):
        self.occ.config = {'debug': False}
        result = self._run(
            name='debug', state='absent', installed_config_json=self._CACHE
        )
        self.assertTrue(result['changed'])
        self.assertEqual(result['current_value'], 'false')
        self.assertEqual(
            self.occ.writes(), [[*_PREFIX, 'config:system:delete', 'debug']]
        )

    def test_unparsable_json_fails(self):
        result = self._fail(
            name='debug', value='true', installed_config_json='{not json'
        )
        self.assertIn('Failed to parse installed_config_json', result['msg'])
        self.assertEqual(self.occ.commands, [])


class TestCheckMode(OccSystemConfigTestCase):
    def test_set_is_reported_but_not_run(self):
        result = self._run(
            name='default_language', value='de', _ansible_check_mode=True
        )
        self.assertTrue(result['changed'])
        self.assertEqual(self.occ.writes(), [])
        self.assertNotIn('rc', result)

    def test_delete_is_reported_but_not_run(self):
        self.occ.config = {'debug': True}
        result = self._run(name='debug', state='absent', _ansible_check_mode=True)
        self.assertTrue(result['changed'])
        self.assertEqual(self.occ.writes(), [])
        self.assertIn('debug', self.occ.config)


class TestDiff(OccSystemConfigTestCase):
    def test_diff_on_set(self):
        self.occ.config = {'default_language': 'en'}
        result = self._run(name='default_language', value='de', _ansible_diff=True)
        self.assertEqual(
            result['diff'],
            {'before': 'default_language: en\n', 'after': 'default_language: de\n'},
        )

    def test_diff_on_delete(self):
        self.occ.config = {'default_language': 'en'}
        result = self._run(name='default_language', state='absent', _ansible_diff=True)
        self.assertEqual(
            result['diff'], {'before': 'default_language: en\n', 'after': ''}
        )


class TestErrors(OccSystemConfigTestCase):
    def test_failing_set_fails(self):
        self.occ.fail_set = True
        # the harness' fail_json raises an Exception subclass, which the module's
        # `except Exception` wraps into a second fail_json; the stderr survives
        result = self._fail(name='default_language', value='de')
        self.assertIn('Cannot set value', result['msg'])

    def test_exception_from_run_command_fails(self):
        with unittest.mock.patch.object(
            basic.AnsibleModule,
            'run_command',
            side_effect=OSError('No such file or directory: php'),
        ):
            result = self._fail(name='default_language', value='de')
        self.assertIn('No such file or directory', result['msg'])


if __name__ == '__main__':
    unittest.main()
