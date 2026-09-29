#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.


"""Unit tests for the uptimerobot_mwindow_info module.

main() is driven through the shared ansible module harness. The HTTP layer
is replaced at its lowest level, `fetch_url()` in the uptimerobot
module_util, by a fake that serves canned UptimeRobot v2 `getMWindows`
responses and records every request, so no real API call is made. The
on-disk response cache is redirected into a per-test temporary directory.
Covered: the windows come back with type, status and weekday labels while
monthly day numbers are passed through, the exact-match friendly_name
filter, pages are fetched until the reported total is reached, the module
never reports a change, API and HTTP errors end in fail_json, and the API
key never shows up in the result or the module log. The collection import
is wired up by tests/conftest.py.
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
    uptimerobot_mwindow_info as mod,
)

# Not the plain 'linuxfabrik' placeholder: TestApiKeyNotLeaked searches the result for the key,
# and the canned API data uses 'linuxfabrik' as its own placeholder, e.g. in a webhook URL.
_API_KEY = 'linuxfabrik-ur-api-key'


def _mwindow(mwindow_id, friendly_name, mwindow_type, value, status=1):
    """One maintenance window as getMWindows returns it."""
    return {
        'id': mwindow_id,
        'user': 1,
        'type': mwindow_type,
        'friendly_name': friendly_name,
        'start_time': '03:30',
        'duration': 120,
        'value': value,
        'status': status,
    }


def _page(mwindows, offset=0, total=None):
    """A getMWindows response page."""
    return {
        'stat': 'ok',
        'pagination': {
            'offset': offset,
            'limit': 50,
            'total': len(mwindows) if total is None else total,
        },
        'mwindows': mwindows,
    }


def _account_page():
    return _page(
        [
            _mwindow(581, 'once 03:30-05:30', 1, '', status=0),
            _mwindow(582, 'daily 03:30-05:30', 2, ''),
            _mwindow(583, 'weekly mon-wed-fri 03:30-05:30', 3, '1-3-5'),
            _mwindow(584, 'weekly sun 03:30-05:30', 3, '7'),
            _mwindow(585, 'monthly 15-28 03:30-05:30', 4, '15-28'),
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


class TestListMwindows(_ModuleTestCase):
    def test_returns_windows_with_labels(self):
        self.fake.responses.append((200, _account_page()))
        result = self._run({'api_key': _API_KEY})
        self.assertFalse(result['changed'])
        self.assertEqual(result['debug'], {'operation': 'list', 'count': 5})
        self.assertEqual(
            [(w['id'], w['type'], w['value'], w['status']) for w in result['mwindows']],
            [
                (581, 'once', '', 'paused'),
                (582, 'daily', '', 'active'),
                (583, 'weekly', 'mon-wed-fri', 'active'),
                (584, 'weekly', 'sun', 'active'),
                # day-of-month numbers are not weekday IDs
                (585, 'monthly', '15-28', 'active'),
            ],
        )
        self.assertEqual(result['mwindows'][2]['start_time'], '03:30')
        self.assertEqual(result['mwindows'][2]['duration'], 120)

    def test_calls_get_mwindows_once(self):
        self.fake.responses.append((200, _account_page()))
        self._run({'api_key': _API_KEY})
        self.assertEqual(len(self.fake.requests), 1)
        request = self.fake.requests[0]
        self.assertEqual(request['endpoint'], 'getMWindows')
        self.assertEqual(request['method'], 'POST')
        self.assertEqual(request['body']['api_key'], _API_KEY)
        self.assertEqual(request['body']['format'], 'json')

    def test_empty_account(self):
        self.fake.responses.append((200, _page([])))
        result = self._run({'api_key': _API_KEY})
        self.assertEqual(result['mwindows'], [])
        self.assertEqual(result['debug']['count'], 0)

    def test_check_mode_still_reads(self):
        self.fake.responses.append((200, _account_page()))
        result = self._run({'api_key': _API_KEY, '_ansible_check_mode': True})
        self.assertFalse(result['changed'])
        self.assertEqual(len(result['mwindows']), 5)


class TestFriendlyNameFilter(_ModuleTestCase):
    def test_exact_match_returns_one_element_list(self):
        self.fake.responses.append((200, _account_page()))
        result = self._run(
            {'api_key': _API_KEY, 'friendly_name': 'weekly mon-wed-fri 03:30-05:30'}
        )
        self.assertEqual(len(result['mwindows']), 1)
        self.assertEqual(result['mwindows'][0]['id'], 583)
        self.assertEqual(result['mwindows'][0]['value'], 'mon-wed-fri')
        self.assertEqual(result['debug']['count'], 1)
        self.assertNotIn('friendly_name', self.fake.requests[0]['body'])

    def test_no_match_returns_empty_list(self):
        for name in ('missing', 'weekly', 'DAILY 03:30-05:30'):
            with self.subTest(name=name):
                self.fake.responses.append((200, _account_page()))
                result = self._run({'api_key': _API_KEY, 'friendly_name': name})
                self.assertEqual(result['mwindows'], [])
                self.assertEqual(result['debug']['count'], 0)
                # drop the cached response so every subtest hits the fake
                shutil.rmtree(self.cache_dir, ignore_errors=True)


class TestPagination(_ModuleTestCase):
    def test_fetches_every_page(self):
        first = [_mwindow(i, f'daily {i:03d}', 2, '') for i in range(50)]
        second = [_mwindow(i, f'daily {i:03d}', 2, '') for i in range(50, 55)]
        self.fake.responses.append((200, _page(first, offset=0, total=55)))
        self.fake.responses.append((200, _page(second, offset=50, total=55)))
        result = self._run({'api_key': _API_KEY})
        self.assertEqual([w['id'] for w in result['mwindows']], list(range(55)))
        self.assertEqual([r['body']['offset'] for r in self.fake.requests], ['0', '50'])


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
        self.assertIn('Could not list maintenance windows', result['msg'])
        self.assertIn('An internal error occurred.', result['msg'])

    def test_http_error_is_reported(self):
        self.fake.responses.append((500, 'HTTP Error 500: Internal Server Error'))
        result = self._fail({'api_key': _API_KEY})
        self.assertIn('Could not list maintenance windows', result['msg'])
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
