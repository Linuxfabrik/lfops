#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.


"""Unit tests for the uptimerobot_monitor_info module.

main() is driven through the shared ansible module harness. The HTTP layer
is replaced at its lowest level, `fetch_url()` in the uptimerobot
module_util, by a fake that serves canned UptimeRobot v2 `getMonitors`
responses and records every request, so no real API call is made. The
on-disk response cache is redirected into a per-test temporary directory.
Covered: the monitors come back with their enum fields translated to
labels (including the nested alert contacts), the request asks for the
optional detail fields, `search` is forwarded to the API while
`friendly_name` filters client-side, pages are fetched until the reported
total is reached, a rate-limited call is retried once, the module never
reports a change, API and HTTP errors end in fail_json, and the API key
never shows up in the result or the module log. The collection import is
wired up by tests/conftest.py.
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
    uptimerobot_monitor_info as mod,
)

# Not the plain 'linuxfabrik' placeholder: TestApiKeyNotLeaked searches the result for the key,
# and the canned API data uses 'linuxfabrik' as its own placeholder, e.g. in a webhook URL.
_API_KEY = 'linuxfabrik-ur-api-key'


def _monitor(monitor_id, friendly_name, **overrides):
    """One monitor as getMonitors returns it (enum fields as integers)."""
    monitor = {
        'id': monitor_id,
        'friendly_name': friendly_name,
        'url': 'https://www.example.com',
        'type': 1,
        'sub_type': '',
        'keyword_type': None,
        'keyword_case_type': None,
        'keyword_value': '',
        'http_username': '',
        'port': '',
        'interval': 300,
        'timeout': 30,
        'status': 2,
        'create_datetime': 1461508140,
        'alert_contacts': [],
        'mwindows': [],
    }
    monitor.update(overrides)
    return monitor


def _page(monitors, offset=0, total=None):
    """A getMonitors response page."""
    return {
        'stat': 'ok',
        'pagination': {
            'offset': offset,
            'limit': 50,
            'total': len(monitors) if total is None else total,
        },
        'monitors': monitors,
    }


def _account_page():
    return _page(
        [
            _monitor(
                777749809,
                '001 www.example.com',
                http_method=2,
                auth_type=1,
                alert_contacts=[
                    {
                        'id': '0993765',
                        'value': 'monitoring@example.com',
                        'type': 2,
                        'threshold': 0,
                        'recurrence': 0,
                    },
                ],
                mwindows=[{'id': 581}],
            ),
            _monitor(
                777712827,
                '001 shop.example.com',
                type=2,
                status=9,
                keyword_type=1,
                keyword_case_type=0,
                keyword_value='Welcome',
            ),
            _monitor(777810874, '002 db.example.com', type=4, status=0, port=5432),
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


class TestListMonitors(_ModuleTestCase):
    def test_returns_monitors_with_labels(self):
        self.fake.responses.append((200, _account_page()))
        result = self._run({'api_key': _API_KEY})
        self.assertFalse(result['changed'])
        self.assertEqual(result['debug'], {'operation': 'list', 'count': 3})
        web, shop, db = result['monitors']

        self.assertEqual(web['id'], 777749809)
        self.assertEqual(web['type'], 'http')
        self.assertEqual(web['status'], 'up')
        self.assertEqual(web['http_method'], 'get')
        self.assertEqual(web['http_auth_type'], 'basic')
        self.assertEqual(web['alert_contacts'][0]['type'], 'email')
        self.assertEqual(web['alert_contacts'][0]['id'], '0993765')
        self.assertEqual(web['mwindows'], [{'id': 581}])

        self.assertEqual(shop['type'], 'keyw')
        self.assertEqual(shop['status'], 'down')
        self.assertEqual(shop['keyword_type'], 'exist')
        self.assertEqual(shop['keyword_case_type'], 'cs')
        self.assertEqual(shop['keyword_value'], 'Welcome')

        self.assertEqual(db['type'], 'port')
        self.assertEqual(db['status'], 'paused')
        self.assertEqual(db['port'], 5432)

    def test_other_status_labels(self):
        page = _page(
            [
                _monitor(1, 'waiting', status=1, type=3),
                _monitor(2, 'flapping', status=8, type=5),
            ]
        )
        self.fake.responses.append((200, page))
        result = self._run({'api_key': _API_KEY})
        self.assertEqual(
            [(m['type'], m['status']) for m in result['monitors']],
            [('ping', 'wait'), ('beat', 'seems_down')],
        )

    def test_requests_detail_fields(self):
        self.fake.responses.append((200, _account_page()))
        self._run({'api_key': _API_KEY})
        self.assertEqual(len(self.fake.requests), 1)
        request = self.fake.requests[0]
        self.assertEqual(request['endpoint'], 'getMonitors')
        self.assertEqual(request['method'], 'POST')
        body = request['body']
        self.assertEqual(body['api_key'], _API_KEY)
        self.assertEqual(body['format'], 'json')
        self.assertEqual(body['alert_contacts'], '1')
        self.assertEqual(body['mwindows'], '1')
        # the API rejects `1` on this flag and expects the literal `True`
        self.assertEqual(body['http_request_details'], 'True')
        self.assertNotIn('search', body)

    def test_empty_account(self):
        self.fake.responses.append((200, _page([])))
        result = self._run({'api_key': _API_KEY})
        self.assertEqual(result['monitors'], [])
        self.assertEqual(result['debug']['count'], 0)

    def test_check_mode_still_reads(self):
        self.fake.responses.append((200, _account_page()))
        result = self._run({'api_key': _API_KEY, '_ansible_check_mode': True})
        self.assertFalse(result['changed'])
        self.assertEqual(len(result['monitors']), 3)


class TestFilters(_ModuleTestCase):
    def test_search_is_forwarded(self):
        self.fake.responses.append((200, _account_page()))
        self._run({'api_key': _API_KEY, 'search': '001 '})
        self.assertEqual(self.fake.requests[0]['body']['search'], '001 ')

    def test_empty_search_is_not_forwarded(self):
        self.fake.responses.append((200, _account_page()))
        self._run({'api_key': _API_KEY, 'search': ''})
        self.assertNotIn('search', self.fake.requests[0]['body'])

    def test_friendly_name_exact_match(self):
        self.fake.responses.append((200, _account_page()))
        result = self._run(
            {'api_key': _API_KEY, 'friendly_name': '001 shop.example.com'}
        )
        self.assertEqual(len(result['monitors']), 1)
        self.assertEqual(result['monitors'][0]['id'], 777712827)
        self.assertEqual(result['monitors'][0]['type'], 'keyw')
        self.assertEqual(result['debug']['count'], 1)
        self.assertNotIn('friendly_name', self.fake.requests[0]['body'])

    def test_friendly_name_no_match(self):
        for name in ('missing', '001 SHOP.example.com', '001'):
            with self.subTest(name=name):
                self.fake.responses.append((200, _account_page()))
                result = self._run({'api_key': _API_KEY, 'friendly_name': name})
                self.assertEqual(result['monitors'], [])
                self.assertEqual(result['debug']['count'], 0)
                # drop the cached response so every subtest hits the fake
                shutil.rmtree(self.cache_dir, ignore_errors=True)

    def test_search_and_friendly_name_combined(self):
        # the API narrows by substring, the module then picks the exact match
        page = _page(
            [
                _monitor(1, '001 www.example.com'),
                _monitor(2, '001 www.example.com/api'),
            ]
        )
        self.fake.responses.append((200, page))
        result = self._run(
            {
                'api_key': _API_KEY,
                'search': 'www.example.com',
                'friendly_name': '001 www.example.com',
            }
        )
        self.assertEqual(self.fake.requests[0]['body']['search'], 'www.example.com')
        self.assertEqual([m['id'] for m in result['monitors']], [1])


class TestPagination(_ModuleTestCase):
    def test_fetches_every_page(self):
        first = [_monitor(i, f'monitor {i:03d}') for i in range(50)]
        second = [_monitor(i, f'monitor {i:03d}') for i in range(50, 60)]
        self.fake.responses.append((200, _page(first, offset=0, total=60)))
        self.fake.responses.append((200, _page(second, offset=50, total=60)))
        result = self._run({'api_key': _API_KEY, 'search': 'monitor'})
        self.assertEqual([m['id'] for m in result['monitors']], list(range(60)))
        self.assertEqual(result['debug']['count'], 60)
        self.assertEqual([r['body']['offset'] for r in self.fake.requests], ['0', '50'])
        # every page carries the same filter and detail flags
        for request in self.fake.requests:
            self.assertEqual(request['body']['search'], 'monitor')
            self.assertEqual(request['body']['alert_contacts'], '1')

    def test_single_page_when_total_fits(self):
        monitors = [_monitor(i, f'monitor {i:03d}') for i in range(50)]
        self.fake.responses.append((200, _page(monitors, total=50)))
        result = self._run({'api_key': _API_KEY})
        self.assertEqual(len(self.fake.requests), 1)
        self.assertEqual(len(result['monitors']), 50)

    def test_error_on_later_page_fails_without_partial_result(self):
        first = [_monitor(i, f'monitor {i:03d}') for i in range(50)]
        self.fake.responses.append((200, _page(first, offset=0, total=60)))
        self.fake.responses.append((502, 'HTTP Error 502: Bad Gateway'))
        result = self._fail({'api_key': _API_KEY})
        self.assertIn('Could not list monitors', result['msg'])
        self.assertIn('HTTP 502', result['msg'])
        self.assertNotIn('monitors', result)


class TestRateLimit(_ModuleTestCase):
    def test_retries_once_after_429(self):
        self.fake.responses.append((429, 'HTTP Error 429: Too Many Requests'))
        self.fake.responses.append((200, _account_page()))
        with unittest.mock.patch.object(ur.time, 'sleep') as sleep:
            result = self._run({'api_key': _API_KEY})
        self.assertEqual(len(self.fake.requests), 2)
        self.assertEqual(sleep.call_count, 1)
        self.assertEqual(len(result['monitors']), 3)

    def test_second_429_fails(self):
        self.fake.responses.append((429, 'HTTP Error 429: Too Many Requests'))
        self.fake.responses.append((429, 'HTTP Error 429: Too Many Requests'))
        with unittest.mock.patch.object(ur.time, 'sleep'):
            result = self._fail({'api_key': _API_KEY})
        self.assertEqual(len(self.fake.requests), 2)
        self.assertIn('HTTP 429', result['msg'])


class TestErrors(_ModuleTestCase):
    def test_stat_fail_is_reported(self):
        self.fake.responses.append(
            (
                200,
                {
                    'stat': 'fail',
                    'error': {
                        'type': 'invalid_parameter',
                        'parameter_name': 'search',
                        'passed_value': '',
                        'message': 'search should be a string.',
                    },
                },
            )
        )
        result = self._fail({'api_key': _API_KEY})
        self.assertIn('Could not list monitors', result['msg'])
        self.assertIn('invalid_parameter', result['msg'])
        self.assertIn('search should be a string.', result['msg'])

    def test_http_error_is_reported(self):
        self.fake.responses.append((500, 'HTTP Error 500: Internal Server Error'))
        result = self._fail({'api_key': _API_KEY})
        self.assertIn('Could not list monitors', result['msg'])
        self.assertIn('HTTP 500', result['msg'])


class TestApiKeyNotLeaked(_ModuleTestCase):
    def test_not_in_result_or_log(self):
        self.fake.responses.append((200, _account_page()))
        result = self._run({'api_key': _API_KEY, 'search': '001'})
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
