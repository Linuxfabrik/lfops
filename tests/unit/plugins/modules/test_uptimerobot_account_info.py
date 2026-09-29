#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the uptimerobot_account_info module.

main() is driven through the shared ansible module harness. The HTTP layer
is replaced at its lowest level, `fetch_url()` in the uptimerobot
module_util, by a fake that serves canned UptimeRobot v2 responses and
records every request, so no real API call is made. The on-disk response
cache is redirected into a per-test temporary directory. Covered: the
account record is returned as the API sent it, the module never reports a
change, the API key resolution order, API and HTTP errors end in fail_json,
and the API key never shows up in the result or the module log. The
collection import is wired up by tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import io
import json
import os
import shutil
import tempfile
import unittest
import unittest.mock
import urllib.parse

import ansible_harness
from ansible.module_utils import basic
from ansible_collections.linuxfabrik.lfops.plugins.module_utils import uptimerobot as ur
from ansible_collections.linuxfabrik.lfops.plugins.modules import (
    uptimerobot_account_info as mod,
)

# Not the plain 'linuxfabrik' placeholder: TestApiKeyNotLeaked searches the result for the key,
# and the canned API data uses 'linuxfabrik' as its own placeholder, e.g. in a webhook URL.
_API_KEY = 'linuxfabrik-ur-api-key'

_ACCOUNT = {
    'email': 'user@example.com',
    'monitor_limit': 50,
    'monitor_interval': 1,
    'up_monitors': 10,
    'down_monitors': 1,
    'paused_monitors': 2,
}


class _FakeFetchUrl:
    """Stand-in for fetch_url() in the uptimerobot module_util.

    Serves the queued (HTTP status, payload) tuples in order and records
    every request (endpoint, method and decoded form body). A 2xx payload
    that is not a string is JSON-encoded; for any other status the payload
    is the error message fetch_url() would put into `info['msg']`.
    """

    def __init__(self):
        self.responses = []
        self.requests = []

    def __call__(self, module, url, data=None, headers=None, method=None, timeout=None):
        self.requests.append(
            {
                'endpoint': url.rsplit('/', 1)[-1],
                'method': method,
                'body': dict(urllib.parse.parse_qsl(data.decode('utf-8'))),
            }
        )
        if not self.responses:
            raise AssertionError(f'unexpected API call to {url}')
        status, payload = self.responses.pop(0)
        info = {'status': status, 'url': url}
        if status < 200 or status >= 300:
            info['msg'] = payload
            return None, info
        if not isinstance(payload, str):
            payload = json.dumps(payload)
        return io.BytesIO(payload.encode('utf-8')), info


class _ModuleTestCase(unittest.TestCase):
    def setUp(self):
        self.cache_dir = tempfile.mkdtemp(prefix='lfops_uptimerobot_cache_')
        self.fake = _FakeFetchUrl()
        self.log_lines = []
        log_lines = self.log_lines

        def _log(module, msg, log_args=None):
            log_lines.append(msg)

        self._patchers = [
            unittest.mock.patch.object(ur, 'fetch_url', self.fake),
            unittest.mock.patch.object(ur, 'CACHE_DIR', self.cache_dir),
            unittest.mock.patch.object(basic.AnsibleModule, 'log', _log),
            ansible_harness.patch_module(),
        ]
        for p in self._patchers:
            p.start()

    def tearDown(self):
        for p in reversed(self._patchers):
            p.stop()
        shutil.rmtree(self.cache_dir, ignore_errors=True)

    def _run(self, args):
        ansible_harness.set_module_args(args)
        try:
            mod.main()
        except ansible_harness.AnsibleExitJson as exc:
            return exc.args[0]
        raise AssertionError('module did not call exit_json')

    def _fail(self, args):
        ansible_harness.set_module_args(args)
        with self.assertRaises(ansible_harness.AnsibleFailJson) as ctx:
            mod.main()
        return ctx.exception.args[0]


class TestAccountDetails(_ModuleTestCase):
    def test_returns_account_unchanged(self):
        self.fake.responses.append((200, {'stat': 'ok', 'account': _ACCOUNT}))
        result = self._run({'api_key': _API_KEY})
        self.assertFalse(result['changed'])
        self.assertEqual(result['account'], _ACCOUNT)
        self.assertEqual(result['debug']['operation'], 'read')
        self.assertEqual(result['debug']['fields'], sorted(_ACCOUNT))

    def test_calls_get_account_details_once(self):
        self.fake.responses.append((200, {'stat': 'ok', 'account': _ACCOUNT}))
        self._run({'api_key': _API_KEY})
        self.assertEqual(len(self.fake.requests), 1)
        request = self.fake.requests[0]
        self.assertEqual(request['endpoint'], 'getAccountDetails')
        self.assertEqual(request['method'], 'POST')
        self.assertEqual(request['body']['api_key'], _API_KEY)
        self.assertEqual(request['body']['format'], 'json')

    def test_check_mode_still_reads(self):
        self.fake.responses.append((200, {'stat': 'ok', 'account': _ACCOUNT}))
        result = self._run({'api_key': _API_KEY, '_ansible_check_mode': True})
        self.assertFalse(result['changed'])
        self.assertEqual(result['account'], _ACCOUNT)


class TestApiKeyResolution(_ModuleTestCase):
    def setUp(self):
        super().setUp()
        self.tmp_dir = tempfile.mkdtemp(prefix='lfops_uptimerobot_key_')
        env_patcher = unittest.mock.patch.dict(os.environ)
        env_patcher.start()
        self._patchers.append(env_patcher)
        os.environ.pop(ur.ENV_API_KEY, None)

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_key_from_file(self):
        key_file = os.path.join(self.tmp_dir, 'uptimerobot')
        with open(key_file, 'w') as fh:
            fh.write('linuxfabrik-from-file\n')
        self.fake.responses.append((200, {'stat': 'ok', 'account': _ACCOUNT}))
        self._run({'api_key_file': key_file})
        self.assertEqual(
            self.fake.requests[0]['body']['api_key'], 'linuxfabrik-from-file'
        )

    def test_argument_wins_over_file(self):
        key_file = os.path.join(self.tmp_dir, 'uptimerobot')
        with open(key_file, 'w') as fh:
            fh.write('linuxfabrik-from-file\n')
        self.fake.responses.append((200, {'stat': 'ok', 'account': _ACCOUNT}))
        self._run({'api_key': _API_KEY, 'api_key_file': key_file})
        self.assertEqual(self.fake.requests[0]['body']['api_key'], _API_KEY)

    def test_key_from_environment(self):
        os.environ[ur.ENV_API_KEY] = 'linuxfabrik-from-env'
        self.fake.responses.append((200, {'stat': 'ok', 'account': _ACCOUNT}))
        self._run({'api_key_file': os.path.join(self.tmp_dir, 'missing')})
        self.assertEqual(
            self.fake.requests[0]['body']['api_key'], 'linuxfabrik-from-env'
        )

    def test_no_key_fails_without_calling_the_api(self):
        result = self._fail({'api_key_file': os.path.join(self.tmp_dir, 'missing')})
        self.assertIn('No UptimeRobot API key found', result['msg'])
        self.assertEqual(self.fake.requests, [])


class TestErrors(_ModuleTestCase):
    def test_stat_fail_is_reported(self):
        self.fake.responses.append(
            (
                200,
                {
                    'stat': 'fail',
                    'error': {
                        'type': 'invalid_parameter',
                        'parameter_name': 'api_key',
                        'passed_value': _API_KEY,
                        'message': 'api_key is invalid.',
                    },
                },
            )
        )
        result = self._fail({'api_key': _API_KEY})
        self.assertIn('Could not fetch UptimeRobot account details', result['msg'])
        self.assertIn('invalid_parameter', result['msg'])
        self.assertIn('api_key is invalid.', result['msg'])

    def test_http_error_is_reported(self):
        self.fake.responses.append((500, 'HTTP Error 500: Internal Server Error'))
        result = self._fail({'api_key': _API_KEY})
        self.assertIn('HTTP 500', result['msg'])
        self.assertIn('Internal Server Error', result['msg'])

    def test_connection_error_is_reported(self):
        # fetch_url() reports connection-level failures with status -1
        self.fake.responses.append((-1, 'Request failed: <urlopen error timed out>'))
        result = self._fail({'api_key': _API_KEY})
        self.assertIn('timed out', result['msg'])

    def test_non_json_body_is_reported(self):
        self.fake.responses.append((200, '<html>Bad Gateway</html>'))
        result = self._fail({'api_key': _API_KEY})
        self.assertIn('Could not parse JSON', result['msg'])


class TestApiKeyNotLeaked(_ModuleTestCase):
    def test_not_in_result_or_log(self):
        self.fake.responses.append((200, {'stat': 'ok', 'account': _ACCOUNT}))
        result = self._run({'api_key': _API_KEY})
        self.assertNotIn(_API_KEY, json.dumps(result))
        for line in self.log_lines:
            self.assertNotIn(_API_KEY, line)

    def test_not_in_failure_message(self):
        # the API echoes the rejected key in `passed_value`
        self.fake.responses.append(
            (
                200,
                {
                    'stat': 'fail',
                    'error': {
                        'type': 'invalid_parameter',
                        'parameter_name': 'api_key',
                        'passed_value': _API_KEY,
                        'message': 'api_key is invalid.',
                    },
                },
            )
        )
        result = self._fail({'api_key': _API_KEY})
        self.assertNotIn(_API_KEY, json.dumps(result))
        for line in self.log_lines:
            self.assertNotIn(_API_KEY, line)


if __name__ == '__main__':
    unittest.main()
