#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the uptimerobot_psp module.

main() is driven through the shared ansible module harness against an
in-memory fake of the UptimeRobot v2 API. The fake replaces `fetch_url`
in the uptimerobot module_util, which is the only place that talks HTTP,
so the whole stack below main() (request encoding, pagination, error
handling, response translation, the read cache) runs for real. The fake
keeps the PSPs and monitors, answers with v2-shaped JSON (integer
`sort` / `status`, `custom_url` on the read side, monitors as a list of
IDs) and records every call, so the tests can assert that no write call
is issued when nothing differs or in check mode. The on-disk read cache
is pointed at a fresh temporary directory per test. The collection
import is wired up by tests/conftest.py.
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
from ansible_collections.linuxfabrik.lfops.plugins.modules import uptimerobot_psp as mod

API_KEY = 'linuxfabrik'
PASSWORD = 'linuxfabrik'
PSP_NAME = 'Status - example.com'

_WRITE_ENDPOINTS = ('deletePSP', 'editPSP', 'newPSP')


class _FakeUptimeRobot:
    """In-memory UptimeRobot v2 API, plugged in as `fetch_url`."""

    def __init__(self):
        self.psps = []
        self.monitors = []
        self.calls = []
        # endpoint -> ('http', status) or ('stat', error type, error message)
        self.failures = {}
        self._next_id = 9000
        self._handlers = {
            'deletePSP': self._delete_psp,
            'editPSP': self._edit_psp,
            'getMonitors': self._get_monitors,
            'getPSPs': self._get_psps,
            'newPSP': self._new_psp,
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
        return [c for c in self.calls if c[0] in _WRITE_ENDPOINTS]

    def endpoints(self):
        return [c[0] for c in self.calls]

    def _find(self, psp_id):
        for psp in self.psps:
            if psp['id'] == int(psp_id):
                return psp
        return None

    @staticmethod
    def _page(key, items):
        return {
            'stat': 'ok',
            'pagination': {'offset': 0, 'limit': 50, 'total': len(items)},
            key: copy.deepcopy(items),
        }

    def _get_psps(self, params):
        return self._page('psps', self.psps)

    def _get_monitors(self, params):
        return self._page('monitors', self.monitors)

    @staticmethod
    def _apply(psp, params):
        if 'monitors' in params:
            psp['monitors'] = [int(i) for i in params['monitors'].split(',')]
        if 'custom_domain' in params:
            psp['custom_url'] = params['custom_domain']
        for key in ('sort', 'status'):
            if key in params:
                psp[key] = int(params[key])

    def _new_psp(self, params):
        self._next_id += 1
        psp = {
            'id': self._next_id,
            'friendly_name': params['friendly_name'],
            'sort': 1,
            'status': 1,
            'custom_url': '',
            'monitors': [],
        }
        self._apply(psp, params)
        self.psps.append(psp)
        return {'stat': 'ok', 'psp': {'id': psp['id']}}

    def _edit_psp(self, params):
        psp = self._find(params['id'])
        self._apply(psp, params)
        return {'stat': 'ok', 'psp': {'id': psp['id']}}

    def _delete_psp(self, params):
        psp = self._find(params['id'])
        self.psps.remove(psp)
        return {'stat': 'ok', 'psp': {'id': psp['id']}}


def _existing_psp(**overrides):
    psp = {
        'id': 500,
        'friendly_name': PSP_NAME,
        'sort': 1,  # a-z
        'status': 1,  # active
        'standard_url': 'https://stats.uptimerobot.com/abc',
        'custom_url': 'status.example.com',
        'monitors': [12, 11],
    }
    psp.update(overrides)
    return psp


_MONITORS = [
    {'id': 11, 'friendly_name': 'www.example.com', 'type': 1},
    {'id': 12, 'friendly_name': 'office.example.com', 'type': 1},
    {'id': 13, 'friendly_name': 'mail.example.com', 'type': 1},
]


class _FakeApiTestCase(unittest.TestCase):
    def setUp(self):
        self.api = _FakeUptimeRobot()
        self.api.monitors = copy.deepcopy(_MONITORS)
        self.cache_dir = tempfile.mkdtemp(prefix='lfops_uptimerobot_psp_')
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


class TestMain(_FakeApiTestCase):
    def _args(self, **kwargs):
        args = {'api_key': API_KEY, 'friendly_name': PSP_NAME}
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

    # --- create ------------------------------------------------------------

    def test_create_when_absent(self):
        result = self._run(
            custom_url='status.example.com',
            monitors=[{'friendly_name': 'www.example.com'}, {'id': 12}],
            sort='z-a',
            hide_url_links=True,
        )
        self.assertTrue(result['changed'])
        self.assertEqual(result['debug']['operation'], 'create')
        writes = self.api.writes()
        self.assertEqual(len(writes), 1)
        endpoint, params = writes[0]
        self.assertEqual(endpoint, 'newPSP')
        self.assertEqual(params['friendly_name'], PSP_NAME)
        # monitor names are resolved to IDs, the wire format is comma-separated
        self.assertEqual(params['monitors'], '11,12')
        # custom_url is an alias, the write side is called custom_domain
        self.assertEqual(params['custom_domain'], 'status.example.com')
        # labels are translated to the API integers
        self.assertEqual(params['sort'], '2')
        self.assertEqual(params['hide_url_links'], 'True')
        self.assertEqual(result['psp'], {'id': self.api.psps[0]['id']})
        self.assertEqual(result['diff']['before'], {})
        self.assertEqual(result['diff']['after']['monitors'], '11,12')

    def test_create_drops_status(self):
        # UptimeRobot rejects `status` on newPSP
        result = self._run(status='paused')
        self.assertTrue(result['changed'])
        endpoint, params = self.api.writes()[0]
        self.assertEqual(endpoint, 'newPSP')
        self.assertNotIn('status', params)
        self.assertNotIn('status', result['diff']['after'])

    def test_create_without_monitors_omits_the_field(self):
        self._run(sort='a-z', monitors=[])
        _endpoint, params = self.api.writes()[0]
        self.assertNotIn('monitors', params)
        # nothing had to be resolved by name
        self.assertNotIn('getMonitors', self.api.endpoints())

    def test_create_check_mode_does_not_write(self):
        result = self._run(sort='a-z', status='active', _ansible_check_mode=True)
        self.assertTrue(result['changed'])
        self.assertEqual(result['debug']['operation'], 'create (check_mode)')
        self.assertEqual(self.api.writes(), [])
        self.assertEqual(self.api.psps, [])
        self.assertEqual(result['psp'], {'friendly_name': PSP_NAME, 'sort': 'a-z'})

    # --- idempotency -------------------------------------------------------

    def test_no_change_when_matching(self):
        self.api.psps = [_existing_psp()]
        result = self._run(
            custom_domain='status.example.com',
            # different order than the API returns them
            monitors=[{'id': 11}, {'id': 12}],
            sort='a-z',
            status='active',
        )
        self.assertFalse(result['changed'])
        self.assertEqual(result['debug']['operation'], 'noop')
        self.assertEqual(self.api.writes(), [])

    def test_no_change_when_matching_by_monitor_name(self):
        self.api.psps = [_existing_psp()]
        result = self._run(
            custom_url='status.example.com',
            monitors=[
                {'friendly_name': 'office.example.com'},
                {'friendly_name': 'www.example.com'},
            ],
        )
        self.assertFalse(result['changed'])
        self.assertEqual(self.api.writes(), [])

    def test_no_change_when_only_friendly_name_given(self):
        self.api.psps = [_existing_psp()]
        result = self._run()
        self.assertFalse(result['changed'])
        self.assertEqual(self.api.writes(), [])

    def test_second_run_after_create_is_idempotent(self):
        args = {
            'custom_domain': 'status.example.com',
            'monitors': [{'id': 13}, {'friendly_name': 'www.example.com'}],
            'sort': 'down-up-paused',
        }
        self.assertTrue(self._run(**args)['changed'])
        result = self._run(**args)
        self.assertFalse(result['changed'])
        self.assertEqual(len(self.api.writes()), 1)

    # --- update ------------------------------------------------------------

    def test_update_reports_only_the_differing_field(self):
        self.api.psps = [_existing_psp()]
        result = self._run(
            custom_domain='status.example.com',
            monitors=[{'id': 11}, {'id': 12}],
            sort='z-a',
            status='active',
        )
        self.assertTrue(result['changed'])
        self.assertEqual(result['debug']['operation'], 'update')
        self.assertEqual(result['debug']['diff_fields'], ['sort'])
        self.assertEqual(
            result['diff'], {'before': {'sort': 'a-z'}, 'after': {'sort': 'z-a'}}
        )
        writes = self.api.writes()
        self.assertEqual(len(writes), 1)
        endpoint, params = writes[0]
        self.assertEqual(endpoint, 'editPSP')
        self.assertEqual(params['id'], '500')
        self.assertEqual(params['sort'], '2')
        self.assertEqual(self.api.psps[0]['sort'], 2)
        self.assertEqual(result['psp'], {'id': 500})

    def test_update_monitors(self):
        self.api.psps = [_existing_psp()]
        result = self._run(monitors=[{'id': 13}, {'id': 11}])
        self.assertTrue(result['changed'])
        self.assertEqual(
            result['diff'],
            {'before': {'monitors': '11,12'}, 'after': {'monitors': '11,13'}},
        )
        _endpoint, params = self.api.writes()[0]
        self.assertEqual(sorted(params['monitors'].split(',')), ['11', '13'])
        self.assertEqual(sorted(self.api.psps[0]['monitors']), [11, 13])

    def test_pause(self):
        self.api.psps = [_existing_psp()]
        result = self._run(status='paused')
        self.assertTrue(result['changed'])
        self.assertEqual(result['debug']['diff_fields'], ['status'])
        _endpoint, params = self.api.writes()[0]
        self.assertEqual(params['status'], '0')
        self.assertEqual(self.api.psps[0]['status'], 0)

    def test_custom_domain_change(self):
        self.api.psps = [_existing_psp()]
        result = self._run(custom_url='status.example.org')
        self.assertTrue(result['changed'])
        self.assertEqual(
            result['diff'],
            {
                'before': {'custom_domain': 'status.example.com'},
                'after': {'custom_domain': 'status.example.org'},
            },
        )
        _endpoint, params = self.api.writes()[0]
        self.assertEqual(params['custom_domain'], 'status.example.org')

    def test_password_always_updates_and_is_masked(self):
        self.api.psps = [_existing_psp()]
        result = self._run(password=PASSWORD, sort='a-z')
        # UptimeRobot never returns the password, so it cannot be diffed
        self.assertTrue(result['changed'])
        self.assertEqual(result['debug']['diff_fields'], [])
        self.assertEqual(result['diff']['after'], {'password': '<masked>'})
        _endpoint, params = self.api.writes()[0]
        self.assertEqual(params['password'], PASSWORD)
        self.assertNotIn(PASSWORD, json.dumps(result))

    def test_update_check_mode_does_not_write(self):
        self.api.psps = [_existing_psp()]
        result = self._run(sort='z-a', _ansible_check_mode=True)
        self.assertTrue(result['changed'])
        self.assertEqual(result['debug']['operation'], 'update (check_mode)')
        self.assertEqual(self.api.writes(), [])
        self.assertEqual(self.api.psps[0]['sort'], 1)
        # the preview reflects what the run would have written
        self.assertEqual(result['psp']['sort'], 'z-a')
        self.assertEqual(result['psp']['id'], 500)

    # --- delete ------------------------------------------------------------

    def test_delete(self):
        self.api.psps = [_existing_psp()]
        result = self._run(state='absent')
        self.assertTrue(result['changed'])
        self.assertEqual(result['debug']['operation'], 'delete')
        self.assertEqual(self.api.writes(), [('deletePSP', unittest.mock.ANY)])
        self.assertEqual(self.api.writes()[0][1]['id'], '500')
        self.assertEqual(self.api.psps, [])
        self.assertEqual(result['psp']['id'], 500)
        self.assertEqual(
            result['diff'],
            {
                'before': {
                    'friendly_name': PSP_NAME,
                    'id': 500,
                    'custom_domain': 'status.example.com',
                },
                'after': {},
            },
        )

    def test_delete_when_absent_is_noop(self):
        self.api.psps = [_existing_psp(friendly_name='another page')]
        result = self._run(state='absent')
        self.assertFalse(result['changed'])
        self.assertEqual(result['psp'], {})
        self.assertEqual(result['debug']['operation'], 'noop')
        self.assertEqual(self.api.writes(), [])

    def test_delete_check_mode_does_not_write(self):
        self.api.psps = [_existing_psp()]
        result = self._run(state='absent', _ansible_check_mode=True)
        self.assertTrue(result['changed'])
        self.assertEqual(result['debug']['operation'], 'delete (check_mode)')
        self.assertEqual(result['diff']['after'], {})
        self.assertEqual(self.api.writes(), [])
        self.assertEqual(len(self.api.psps), 1)

    # --- errors ------------------------------------------------------------

    def test_list_psps_api_error_fails(self):
        self.api.failures['getPSPs'] = ('stat', 'invalid_parameter', 'bad key')
        result = self._fail(sort='a-z')
        self.assertIn('Could not list PSPs', result['msg'])
        self.assertIn('invalid_parameter: bad key', result['msg'])
        self.assertEqual(self.api.writes(), [])

    def test_list_psps_http_error_fails(self):
        self.api.failures['getPSPs'] = ('http', 503)
        result = self._fail(sort='a-z')
        self.assertIn('Could not list PSPs', result['msg'])
        self.assertIn('HTTP 503', result['msg'])

    def test_create_api_error_fails(self):
        self.api.failures['newPSP'] = ('stat', 'invalid_parameter', 'sort is bad')
        result = self._fail(sort='a-z')
        self.assertIn(f'Could not create PSP {PSP_NAME!r}', result['msg'])
        self.assertIn('sort is bad', result['msg'])

    def test_edit_http_error_fails(self):
        self.api.psps = [_existing_psp()]
        self.api.failures['editPSP'] = ('http', 500)
        result = self._fail(sort='z-a')
        self.assertIn(f'Could not edit PSP {PSP_NAME!r}', result['msg'])
        self.assertIn('HTTP 500', result['msg'])

    def test_delete_api_error_fails(self):
        self.api.psps = [_existing_psp()]
        self.api.failures['deletePSP'] = ('stat', 'not_found', 'psp not found')
        result = self._fail(state='absent')
        self.assertIn(f'Could not delete PSP {PSP_NAME!r}', result['msg'])
        self.assertIn('psp not found', result['msg'])

    def test_unknown_monitor_name_fails_without_writing(self):
        result = self._fail(monitors=[{'friendly_name': 'nope.example.com'}])
        self.assertIn("Monitor 'nope.example.com' not found", result['msg'])
        self.assertEqual(self.api.writes(), [])

    def test_list_monitors_error_fails(self):
        self.api.failures['getMonitors'] = ('http', 502)
        result = self._fail(monitors=[{'friendly_name': 'www.example.com'}])
        self.assertIn('Could not list monitors', result['msg'])
        self.assertEqual(self.api.writes(), [])

    def test_custom_domain_and_custom_url_are_mutually_exclusive(self):
        result = self._fail(
            custom_domain='status.example.com', custom_url='status.example.com'
        )
        self.assertIn('mutually exclusive', result['msg'])
        self.assertEqual(self.api.calls, [])

    # --- secrets -----------------------------------------------------------

    def test_api_key_is_sent_but_not_returned(self):
        result = self._run(sort='a-z')
        self.assertTrue(
            all(params['api_key'] == API_KEY for _e, params in self.api.calls)
        )
        self.assertNotIn(API_KEY, json.dumps(result))

    def test_api_key_not_in_error_message(self):
        self.api.failures['getPSPs'] = ('http', 401)
        result = self._fail()
        self.assertNotIn(API_KEY, json.dumps(result))


class TestResolveMonitorIds(_FakeApiTestCase):
    def setUp(self):
        super().setUp()
        self.module = unittest.mock.MagicMock()
        self.module.fail_json.side_effect = ansible_harness.AnsibleFailJson

    def test_empty_returns_none(self):
        self.assertIsNone(mod._resolve_monitor_ids(self.module, API_KEY, None))
        self.assertIsNone(mod._resolve_monitor_ids(self.module, API_KEY, []))
        self.assertEqual(self.api.calls, [])

    def test_ids_only_need_no_lookup(self):
        wire = mod._resolve_monitor_ids(self.module, API_KEY, [{'id': 5}, {'id': 3}])
        self.assertEqual(wire, '5,3')
        self.assertEqual(self.api.calls, [])

    def test_id_takes_precedence_over_name(self):
        items = [
            {'id': 99, 'friendly_name': 'www.example.com'},
            {'friendly_name': 'mail.example.com'},
        ]
        wire = mod._resolve_monitor_ids(self.module, API_KEY, items)
        self.assertEqual(wire, '99,13')

    def test_unknown_name_fails(self):
        with self.assertRaises(ansible_harness.AnsibleFailJson):
            mod._resolve_monitor_ids(
                self.module, API_KEY, [{'friendly_name': 'nope.example.com'}]
            )


if __name__ == '__main__':
    unittest.main()
