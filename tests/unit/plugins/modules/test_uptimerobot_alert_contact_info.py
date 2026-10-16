#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.


"""Unit tests for the uptimerobot_alert_contact_info module.

main() is driven through the shared ansible module harness. The HTTP layer
is replaced at its lowest level, `fetch_url()` in the uptimerobot
module_util, by a fake that serves canned UptimeRobot v2 `getAlertContacts`
responses and records every request, so no real API call is made. The
on-disk response cache is redirected into a per-test temporary directory.
Covered: the contacts come back with their status and type labels, the
exact-match friendly_name filter, the module never reports a change, API
and HTTP errors end in fail_json, and the API key never shows up in the
result or the module log. The collection import is wired up by
tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import copy
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
    uptimerobot_alert_contact_info as mod,
)

# Not the plain 'linuxfabrik' placeholder: TestApiKeyNotLeaked searches the result for the key,
# and the canned API data uses 'linuxfabrik' as its own placeholder, e.g. in a webhook URL.
_API_KEY = 'linuxfabrik-ur-api-key'

# getAlertContacts reports offset/limit/total at the top level
_CONTACTS_PAYLOAD = {
    'stat': 'ok',
    'offset': 0,
    'limit': 50,
    'total': 3,
    'alert_contacts': [
        {
            'id': '0993765',
            'friendly_name': 'monitoring@example.com',
            'type': 2,
            'status': 2,
            'value': 'monitoring@example.com',
        },
        {
            'id': '2978365',
            'friendly_name': 'Slack #ops',
            'type': 10,
            'status': 1,
            'value': 'https://hooks.slack.com/services/linuxfabrik',
        },
        {
            'id': '3978366',
            'friendly_name': 'On-call phone',
            'type': 1,
            'status': 0,
            'value': '+41000000000',
        },
    ],
}


def _payload():
    return copy.deepcopy(_CONTACTS_PAYLOAD)


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


class TestListAlertContacts(_ModuleTestCase):
    def test_returns_contacts_with_labels(self):
        self.fake.responses.append((200, _payload()))
        result = self._run({'api_key': _API_KEY})
        self.assertFalse(result['changed'])
        self.assertEqual(
            [
                (c['id'], c['friendly_name'], c['type'], c['status'])
                for c in result['alert_contacts']
            ],
            [
                ('0993765', 'monitoring@example.com', 'email', 'active'),
                ('2978365', 'Slack #ops', 'slack', 'paused'),
                ('3978366', 'On-call phone', 'sms', 'not activated'),
            ],
        )
        self.assertEqual(result['alert_contacts'][0]['value'], 'monitoring@example.com')
        self.assertEqual(result['debug'], {'operation': 'list', 'count': 3})

    def test_calls_get_alert_contacts_once(self):
        self.fake.responses.append((200, _payload()))
        self._run({'api_key': _API_KEY})
        self.assertEqual(len(self.fake.requests), 1)
        request = self.fake.requests[0]
        self.assertEqual(request['endpoint'], 'getAlertContacts')
        self.assertEqual(request['method'], 'POST')
        self.assertEqual(request['body']['api_key'], _API_KEY)
        self.assertEqual(request['body']['format'], 'json')

    def test_empty_account(self):
        payload = _payload()
        payload['total'] = 0
        payload['alert_contacts'] = []
        self.fake.responses.append((200, payload))
        result = self._run({'api_key': _API_KEY})
        self.assertFalse(result['changed'])
        self.assertEqual(result['alert_contacts'], [])
        self.assertEqual(result['debug']['count'], 0)

    def test_check_mode_still_reads(self):
        self.fake.responses.append((200, _payload()))
        result = self._run({'api_key': _API_KEY, '_ansible_check_mode': True})
        self.assertFalse(result['changed'])
        self.assertEqual(len(result['alert_contacts']), 3)


class TestFriendlyNameFilter(_ModuleTestCase):
    def test_exact_match_returns_one_element_list(self):
        self.fake.responses.append((200, _payload()))
        result = self._run({'api_key': _API_KEY, 'friendly_name': 'Slack #ops'})
        self.assertFalse(result['changed'])
        self.assertEqual(len(result['alert_contacts']), 1)
        self.assertEqual(result['alert_contacts'][0]['id'], '2978365')
        self.assertEqual(result['alert_contacts'][0]['type'], 'slack')
        self.assertEqual(result['debug']['count'], 1)

    def test_no_match_returns_empty_list(self):
        for name in ('missing', 'slack #ops', 'Slack'):
            with self.subTest(name=name):
                self.fake.responses.append((200, _payload()))
                result = self._run({'api_key': _API_KEY, 'friendly_name': name})
                self.assertEqual(result['alert_contacts'], [])
                self.assertEqual(result['debug']['count'], 0)
                # drop the cached response so every subtest hits the fake
                shutil.rmtree(self.cache_dir, ignore_errors=True)

    def test_filter_is_not_sent_to_the_api(self):
        self.fake.responses.append((200, _payload()))
        self._run({'api_key': _API_KEY, 'friendly_name': 'Slack #ops'})
        self.assertNotIn('friendly_name', self.fake.requests[0]['body'])


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
        self.assertIn('Could not list alert contacts', result['msg'])
        self.assertIn('internal', result['msg'])
        self.assertIn('An internal error occurred.', result['msg'])

    def test_http_error_is_reported(self):
        self.fake.responses.append((503, 'HTTP Error 503: Service Unavailable'))
        result = self._fail({'api_key': _API_KEY})
        self.assertIn('Could not list alert contacts', result['msg'])
        self.assertIn('HTTP 503', result['msg'])


class TestApiKeyNotLeaked(_ModuleTestCase):
    def test_not_in_result_or_log(self):
        self.fake.responses.append((200, _payload()))
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
