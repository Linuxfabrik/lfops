#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.


"""Unit tests for the uptimerobot_psp_info module.

main() is driven through the shared ansible module harness. The HTTP layer
is replaced at its lowest level, `fetch_url()` in the uptimerobot
module_util, by a fake that serves canned UptimeRobot v2 `getPSPs`
responses and records every request, so no real API call is made. The
on-disk response cache is redirected into a per-test temporary directory.
Covered: the status pages come back with sort and status labels and the
custom domain under its write-side name, the exact-match friendly_name
filter, the module never reports a change, API and HTTP errors end in
fail_json, and the API key never shows up in the result or the module log.
The collection import is wired up by tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import io
import json
import shutil
import tempfile
import unittest
import unittest.mock
import urllib.parse

import ansible_harness
from ansible.module_utils import basic
from ansible_collections.linuxfabrik.lfops.plugins.module_utils import uptimerobot as ur
from ansible_collections.linuxfabrik.lfops.plugins.modules import (
    uptimerobot_psp_info as mod,
)

# Not the plain 'linuxfabrik' placeholder: TestApiKeyNotLeaked searches the result for the key,
# and the canned API data uses 'linuxfabrik' as its own placeholder, e.g. in a webhook URL.
_API_KEY = 'linuxfabrik-ur-api-key'


def _psp(psp_id, friendly_name, sort=1, status=1, custom_url=''):
    """One public status page as getPSPs returns it."""
    return {
        'id': psp_id,
        'friendly_name': friendly_name,
        'monitors': 0,
        'sort': sort,
        'status': status,
        'standard_url': f'https://stats.uptimerobot.com/{psp_id}',
        'custom_url': custom_url,
    }


def _page(psps, offset=0, total=None):
    """A getPSPs response page."""
    return {
        'stat': 'ok',
        'pagination': {
            'offset': offset,
            'limit': 50,
            'total': len(psps) if total is None else total,
        },
        'psps': psps,
    }


def _account_page():
    return _page(
        [
            _psp(2345678, 'Status - example.com', custom_url='status.example.com'),
            _psp(2345679, 'Internal', sort=2, status=0),
            _psp(2345680, 'Ops board', sort=3),
            _psp(2345681, 'Incidents first', sort=4),
        ]
    )


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


class TestListPsps(_ModuleTestCase):
    def test_returns_psps_with_labels(self):
        self.fake.responses.append((200, _account_page()))
        result = self._run({'api_key': _API_KEY})
        self.assertFalse(result['changed'])
        self.assertEqual(result['debug'], {'operation': 'list', 'count': 4})
        self.assertEqual(
            [(p['id'], p['sort'], p['status']) for p in result['psps']],
            [
                (2345678, 'a-z', 'active'),
                (2345679, 'z-a', 'paused'),
                (2345680, 'up-down-paused', 'active'),
                (2345681, 'down-up-paused', 'active'),
            ],
        )
        first = result['psps'][0]
        self.assertEqual(first['standard_url'], 'https://stats.uptimerobot.com/2345678')

    def test_custom_url_is_exposed_as_custom_domain(self):
        self.fake.responses.append((200, _account_page()))
        result = self._run({'api_key': _API_KEY})
        first, second = result['psps'][:2]
        self.assertEqual(first['custom_domain'], 'status.example.com')
        self.assertEqual(first['custom_url'], 'status.example.com')
        self.assertEqual(second['custom_domain'], '')

    def test_calls_get_psps_once(self):
        self.fake.responses.append((200, _account_page()))
        self._run({'api_key': _API_KEY})
        self.assertEqual(len(self.fake.requests), 1)
        request = self.fake.requests[0]
        self.assertEqual(request['endpoint'], 'getPSPs')
        self.assertEqual(request['method'], 'POST')
        self.assertEqual(request['body']['api_key'], _API_KEY)
        self.assertEqual(request['body']['format'], 'json')

    def test_empty_account(self):
        self.fake.responses.append((200, _page([])))
        result = self._run({'api_key': _API_KEY})
        self.assertEqual(result['psps'], [])
        self.assertEqual(result['debug']['count'], 0)

    def test_check_mode_still_reads(self):
        self.fake.responses.append((200, _account_page()))
        result = self._run({'api_key': _API_KEY, '_ansible_check_mode': True})
        self.assertFalse(result['changed'])
        self.assertEqual(len(result['psps']), 4)


class TestFriendlyNameFilter(_ModuleTestCase):
    def test_exact_match_returns_one_element_list(self):
        self.fake.responses.append((200, _account_page()))
        result = self._run({'api_key': _API_KEY, 'friendly_name': 'Internal'})
        self.assertEqual(len(result['psps']), 1)
        self.assertEqual(result['psps'][0]['id'], 2345679)
        self.assertEqual(result['psps'][0]['status'], 'paused')
        self.assertEqual(result['debug']['count'], 1)
        self.assertNotIn('friendly_name', self.fake.requests[0]['body'])

    def test_no_match_returns_empty_list(self):
        for name in ('missing', 'internal', 'Status'):
            with self.subTest(name=name):
                self.fake.responses.append((200, _account_page()))
                result = self._run({'api_key': _API_KEY, 'friendly_name': name})
                self.assertEqual(result['psps'], [])
                self.assertEqual(result['debug']['count'], 0)
                # drop the cached response so every subtest hits the fake
                shutil.rmtree(self.cache_dir, ignore_errors=True)


class TestErrors(_ModuleTestCase):
    def test_stat_fail_is_reported(self):
        self.fake.responses.append(
            (
                200,
                {
                    'stat': 'fail',
                    'error': {
                        'type': 'internal',
                        'message': 'An internal error occurred.',
                    },
                },
            )
        )
        result = self._fail({'api_key': _API_KEY})
        self.assertIn('Could not list PSPs', result['msg'])
        self.assertIn('An internal error occurred.', result['msg'])

    def test_http_error_is_reported(self):
        self.fake.responses.append((500, 'HTTP Error 500: Internal Server Error'))
        result = self._fail({'api_key': _API_KEY})
        self.assertIn('Could not list PSPs', result['msg'])
        self.assertIn('HTTP 500', result['msg'])


class TestApiKeyNotLeaked(_ModuleTestCase):
    def test_not_in_result_or_log(self):
        self.fake.responses.append((200, _account_page()))
        result = self._run({'api_key': _API_KEY})
        self.assertNotIn(_API_KEY, json.dumps(result))
        for line in self.log_lines:
            self.assertNotIn(_API_KEY, line)

    def test_not_in_failure_message(self):
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


if __name__ == '__main__':
    unittest.main()
