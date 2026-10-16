#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the uptimerobot_alert_contact module.

The module is delete-only, so the tests cover lookup by friendly name
and by ID, the idempotent no-op when the contact is already gone, check
mode, the rejected state=present and the error paths. main() is driven
through the shared ansible module harness against an in-memory fake of
the UptimeRobot v2 API. The fake replaces `fetch_url` in the uptimerobot
module_util, which is the only place that talks HTTP, so request
encoding, error handling and response translation run for real. It keeps
the alert contacts, answers with v2-shaped JSON (string IDs, integer
`type` / `status`, `offset` / `limit` / `total` on the top level) and
records every call. The on-disk read cache is pointed at a fresh
temporary directory per test. The collection import is wired up by
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
from urllib.parse import parse_qs

import ansible_harness
from ansible_collections.linuxfabrik.lfops.plugins.module_utils import uptimerobot as ur
from ansible_collections.linuxfabrik.lfops.plugins.modules import (
    uptimerobot_alert_contact as mod,
)

API_KEY = 'linuxfabrik'


class _FakeUptimeRobot:
    """In-memory UptimeRobot v2 API, plugged in as `fetch_url`."""

    def __init__(self):
        self.alert_contacts = []
        self.calls = []
        # endpoint -> ('http', status) or ('stat', error type, error message)
        self.failures = {}
        self._handlers = {
            'deleteAlertContact': self._delete_alert_contact,
            'getAlertContacts': self._get_alert_contacts,
        }

    def fetch_url(
        self, module, url, data=None, headers=None, method=None, timeout=None
    ):
        endpoint = url.rsplit('/', 1)[-1]
        params = {k: v[0] for k, v in parse_qs(data.decode('utf-8')).items()}
        self.calls.append((endpoint, params))
        info = {'status': 200, 'msg': 'OK', 'url': url}
        failure = self.failures.get(endpoint)
        if failure and failure[0] == 'http':
            info.update(status=failure[1], msg=f'HTTP Error {failure[1]}')
            return None, info
        if failure and failure[0] == 'stat':
            payload = {
                'stat': 'fail',
                'error': {'type': failure[1], 'message': failure[2]},
            }
        else:
            payload = self._handlers[endpoint](params)
        return io.BytesIO(json.dumps(payload).encode('utf-8')), info

    def writes(self):
        return [c for c in self.calls if c[0] == 'deleteAlertContact']

    def _get_alert_contacts(self, params):
        return {
            'stat': 'ok',
            'offset': 0,
            'limit': 50,
            'total': len(self.alert_contacts),
            'alert_contacts': copy.deepcopy(self.alert_contacts),
        }

    def _delete_alert_contact(self, params):
        for contact in self.alert_contacts:
            if int(contact['id']) == int(params['id']):
                self.alert_contacts.remove(contact)
                return {'stat': 'ok', 'alert_contact': {'id': contact['id']}}
        return {
            'stat': 'fail',
            'error': {'type': 'not_found', 'message': 'alert contact not found'},
        }


_CONTACTS = [
    {
        'id': '7068316',
        'friendly_name': 'old-pager@example.com',
        'type': 2,  # email
        'status': 0,  # not activated
        'value': 'old-pager@example.com',
    },
    {
        'id': '7068317',
        'friendly_name': 'ops@example.com',
        'type': 2,
        'status': 2,  # active
        'value': 'ops@example.com',
    },
]


class TestMain(unittest.TestCase):
    def setUp(self):
        self.api = _FakeUptimeRobot()
        self.api.alert_contacts = copy.deepcopy(_CONTACTS)
        self.cache_dir = tempfile.mkdtemp(prefix='lfops_uptimerobot_contact_')
        self._patchers = [
            unittest.mock.patch.object(ur, 'fetch_url', self.api.fetch_url),
            unittest.mock.patch.object(ur, 'CACHE_DIR', self.cache_dir),
            ansible_harness.patch_module(),
        ]
        for p in self._patchers:
            p.start()

    def tearDown(self):
        for p in reversed(self._patchers):
            p.stop()
        shutil.rmtree(self.cache_dir, ignore_errors=True)

    def _args(self, **kwargs):
        args = {'api_key': API_KEY}
        args.update(kwargs)
        return args

    def _run(self, **kwargs):
        ansible_harness.set_module_args(self._args(**kwargs))
        try:
            mod.main()
        except ansible_harness.AnsibleExitJson as exc:
            return exc.args[0]
        raise AssertionError('module did not call exit_json')

    def _fail(self, **kwargs):
        ansible_harness.set_module_args(self._args(**kwargs))
        with self.assertRaises(ansible_harness.AnsibleFailJson) as ctx:
            mod.main()
        return ctx.exception.args[0]

    def _remaining_names(self):
        return [c['friendly_name'] for c in self.api.alert_contacts]

    # --- delete ------------------------------------------------------------

    def test_delete_by_friendly_name(self):
        result = self._run(friendly_name='old-pager@example.com')
        self.assertTrue(result['changed'])
        self.assertEqual(result['debug']['operation'], 'delete')
        self.assertEqual(result['debug']['contact_id'], 7068316)
        writes = self.api.writes()
        self.assertEqual(len(writes), 1)
        self.assertEqual(writes[0][1]['id'], '7068316')
        self.assertEqual(self._remaining_names(), ['ops@example.com'])
        # the returned contact carries the translated labels
        self.assertEqual(
            result['alert_contact']['friendly_name'], 'old-pager@example.com'
        )
        self.assertEqual(result['alert_contact']['type'], 'email')
        self.assertEqual(result['alert_contact']['status'], 'not activated')

    def test_delete_by_id(self):
        result = self._run(id=7068317)
        self.assertTrue(result['changed'])
        self.assertEqual(result['debug']['friendly_name'], 'ops@example.com')
        self.assertEqual(self.api.writes()[0][1]['id'], '7068317')
        self.assertEqual(self._remaining_names(), ['old-pager@example.com'])

    def test_id_takes_precedence_over_friendly_name(self):
        result = self._run(id=7068317, friendly_name='old-pager@example.com')
        self.assertTrue(result['changed'])
        self.assertEqual(self.api.writes()[0][1]['id'], '7068317')
        self.assertEqual(self._remaining_names(), ['old-pager@example.com'])

    def test_state_absent_is_the_default(self):
        result = self._run(friendly_name='ops@example.com', state='absent')
        self.assertTrue(result['changed'])
        self.assertEqual(len(self.api.writes()), 1)

    # --- idempotency -------------------------------------------------------

    def test_absent_by_friendly_name_is_noop(self):
        result = self._run(friendly_name='gone@example.com')
        self.assertFalse(result['changed'])
        self.assertEqual(result['alert_contact'], {})
        self.assertEqual(result['debug']['operation'], 'noop')
        self.assertEqual(self.api.writes(), [])

    def test_absent_by_id_is_noop(self):
        result = self._run(id=1)
        self.assertFalse(result['changed'])
        self.assertEqual(result['alert_contact'], {})
        self.assertEqual(result['debug']['operation'], 'noop')
        self.assertEqual(self.api.writes(), [])

    def test_friendly_name_match_is_exact(self):
        result = self._run(friendly_name='OPS@example.com')
        self.assertFalse(result['changed'])
        self.assertEqual(self.api.writes(), [])

    def test_second_run_is_noop(self):
        self.assertTrue(self._run(friendly_name='ops@example.com')['changed'])
        self.assertFalse(self._run(friendly_name='ops@example.com')['changed'])
        self.assertEqual(len(self.api.writes()), 1)

    def test_listing_failure_with_id_is_noop(self):
        # documented: when the listing call fails, an ID lookup exits unchanged
        self.api.failures['getAlertContacts'] = ('http', 500)
        result = self._run(id=7068316)
        self.assertFalse(result['changed'])
        self.assertEqual(self.api.writes(), [])

    # --- check mode --------------------------------------------------------

    def test_check_mode_does_not_write(self):
        result = self._run(
            friendly_name='old-pager@example.com', _ansible_check_mode=True
        )
        self.assertTrue(result['changed'])
        self.assertEqual(result['debug']['operation'], 'delete (check_mode)')
        self.assertEqual(result['alert_contact']['id'], '7068316')
        self.assertEqual(self.api.writes(), [])
        self.assertEqual(len(self.api.alert_contacts), 2)

    def test_check_mode_absent_is_noop(self):
        result = self._run(id=1, _ansible_check_mode=True)
        self.assertFalse(result['changed'])
        self.assertEqual(self.api.writes(), [])

    # --- rejected input ----------------------------------------------------

    def test_state_present_is_rejected_without_api_calls(self):
        result = self._fail(friendly_name='ops@example.com', state='present')
        self.assertIn("only supports state='absent'", result['msg'])
        self.assertEqual(self.api.calls, [])

    def test_friendly_name_or_id_is_required(self):
        result = self._fail()
        self.assertIn('friendly_name', result['msg'])
        self.assertIn('id', result['msg'])
        self.assertEqual(self.api.calls, [])

    # --- errors ------------------------------------------------------------

    def test_listing_api_error_with_friendly_name_fails(self):
        self.api.failures['getAlertContacts'] = (
            'stat',
            'invalid_parameter',
            'api_key is invalid',
        )
        result = self._fail(friendly_name='ops@example.com')
        self.assertIn('Could not list alert contacts', result['msg'])
        self.assertIn('invalid_parameter: api_key is invalid', result['msg'])
        self.assertEqual(self.api.writes(), [])

    def test_listing_http_error_with_friendly_name_fails(self):
        self.api.failures['getAlertContacts'] = ('http', 503)
        result = self._fail(friendly_name='ops@example.com')
        self.assertIn('Could not list alert contacts', result['msg'])
        self.assertIn('HTTP 503', result['msg'])

    def test_delete_api_error_fails(self):
        self.api.failures['deleteAlertContact'] = (
            'stat',
            'not_authorized',
            'contact is in use',
        )
        result = self._fail(friendly_name='ops@example.com')
        self.assertIn('Could not delete alert contact', result['msg'])
        self.assertIn('not_authorized: contact is in use', result['msg'])

    def test_delete_http_error_fails(self):
        self.api.failures['deleteAlertContact'] = ('http', 500)
        result = self._fail(id=7068316)
        self.assertIn('Could not delete alert contact', result['msg'])
        self.assertIn('HTTP 500', result['msg'])

    # --- secrets -----------------------------------------------------------

    def test_api_key_is_sent_but_not_returned(self):
        result = self._run(friendly_name='ops@example.com')
        self.assertTrue(
            all(params['api_key'] == API_KEY for _e, params in self.api.calls)
        )
        self.assertNotIn(API_KEY, json.dumps(result))

    def test_api_key_not_in_error_message(self):
        self.api.failures['deleteAlertContact'] = ('http', 401)
        result = self._fail(friendly_name='ops@example.com')
        self.assertNotIn(API_KEY, json.dumps(result))


if __name__ == '__main__':
    unittest.main()
