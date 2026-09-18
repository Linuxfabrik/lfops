#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the bitwarden module_util.

The util runs on the Ansible controller (it is imported by the
bitwarden_item lookup) and, via AnsiballZ, on the managed node for the
bitwarden_item module. All network access funnels through
ansible.module_utils.urls.open_url, which the tests mock; no real
Bitwarden server or cache file is touched.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import contextlib
import functools
import importlib.util
import io
import json
import multiprocessing
import os
import queue
import tempfile
import time
import unittest
import unittest.mock
from urllib.error import HTTPError

_MODULE_PATH = os.path.join(
    os.path.dirname(__file__),
    '..',
    '..',
    '..',
    '..',
    'plugins',
    'module_utils',
    'bitwarden.py',
)
_spec = importlib.util.spec_from_file_location('bitwarden', _MODULE_PATH)
bitwarden = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bitwarden)


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def read(self):
        return json.dumps(self._payload).encode('utf-8')


def _make_bitwarden(tmp_path='/nonexistent/lfops_bw_test_cache.json'):
    """Instantiate Bitwarden without touching a real cache file.

    Pointing CACHE_FILE at a missing path makes _load_cache start fresh,
    and the constructor performs no network I/O.
    """
    bitwarden.CACHE_FILE = tmp_path
    return bitwarden.Bitwarden()


class TestDisplayFallback(unittest.TestCase):
    """The module falls back to a no-op display where Ansible's cannot be loaded."""

    def _load_with_failing_display_import(self, exception):
        real_import = __import__

        def _import(name, *args, **kwargs):
            if name == 'ansible.utils.display':
                raise exception
            return real_import(name, *args, **kwargs)

        spec = importlib.util.spec_from_file_location(
            'bitwarden_fallback', _MODULE_PATH
        )
        module = importlib.util.module_from_spec(spec)
        with unittest.mock.patch('builtins.__import__', _import):
            spec.loader.exec_module(module)
        return module

    def test_import_error_falls_back(self):
        # AnsiballZ on a managed node without the controller's ansible package
        module = self._load_with_failing_display_import(ImportError('no display'))
        self.assertEqual(type(module.display).__name__, '_NoopDisplay')

    def test_other_error_falls_back(self):
        # Mitogen: the import is served, but ansible.constants cannot find base.yml
        module = self._load_with_failing_display_import(
            RuntimeError('Missing base YAML definition file (bad install?)')
        )
        self.assertEqual(type(module.display).__name__, '_NoopDisplay')


class TestGenerate(unittest.TestCase):
    def test_length_and_charset(self):
        bw = _make_bitwarden()
        result = bw.generate(password_length=32, password_choice='abc')
        self.assertEqual(len(result), 32)
        self.assertTrue(set(result).issubset(set('abc')))

    def test_rejects_non_positive_length(self):
        bw = _make_bitwarden()
        with self.assertRaises(ValueError):
            bw.generate(password_length=0)

    def test_hex_requires_even_length(self):
        bw = _make_bitwarden()
        with self.assertRaises(ValueError):
            bw.generate(password_length=3, password_choice='0123456789abcdef')
        # even length is fine
        self.assertEqual(
            len(bw.generate(password_length=4, password_choice='0123456789abcdef')), 4
        )


class TestGetPrettyName(unittest.TestCase):
    def test_explicit_name_wins(self):
        self.assertEqual(
            bitwarden.Bitwarden.get_pretty_name('myname', 'host', 'purpose'), 'myname'
        )

    def test_hostname_only(self):
        self.assertEqual(
            bitwarden.Bitwarden.get_pretty_name('', hostname='app4711'), 'app4711'
        )

    def test_hostname_and_purpose(self):
        self.assertEqual(
            bitwarden.Bitwarden.get_pretty_name(
                '', hostname='app4711', purpose='MariaDB'
            ),
            'app4711 - MariaDB',
        )


class TestApiCall(unittest.TestCase):
    def setUp(self):
        self.bw = _make_bitwarden()
        self._orig_open_url = bitwarden.open_url

    def tearDown(self):
        bitwarden.open_url = self._orig_open_url

    def test_success_returns_result(self):
        bitwarden.open_url = lambda *a, **k: _FakeResponse(
            {'success': True, 'data': {'x': 1}}
        )
        result = self.bw._api_call('status')
        self.assertEqual(result, {'success': True, 'data': {'x': 1}})

    def test_unsuccessful_payload_raises(self):
        bitwarden.open_url = lambda *a, **k: _FakeResponse(
            {'success': False, 'data': 'nope'}
        )
        with self.assertRaises(bitwarden.BitwardenException):
            self.bw._api_call('status')

    def test_http_error_raises_bitwarden_exception(self):
        def _raise(*a, **k):
            raise HTTPError(
                'http://127.0.0.1:8087/status', 500, 'err', {}, io.BytesIO(b'')
            )

        bitwarden.open_url = _raise
        with self.assertRaises(bitwarden.BitwardenException):
            self.bw._api_call('status')

    def test_invalid_json_raises_bitwarden_exception(self):
        class _BadResponse:
            def read(self):
                return b'not json'

        bitwarden.open_url = lambda *a, **k: _BadResponse()
        with self.assertRaises(bitwarden.BitwardenException):
            self.bw._api_call('status')


class TestStatus(unittest.TestCase):
    def setUp(self):
        self.bw = _make_bitwarden()
        self._orig_open_url = bitwarden.open_url

    def tearDown(self):
        bitwarden.open_url = self._orig_open_url

    def _serve_status(self, status):
        bitwarden.open_url = lambda *a, **k: _FakeResponse(
            {
                'success': True,
                'data': {'object': 'template', 'template': {'status': status}},
            }
        )

    def test_status_is_passed_through(self):
        # the complete set of values bw reports, see the status property
        for status in ('unauthenticated', 'locked', 'unlocked'):
            with self.subTest(status=status):
                self._serve_status(status)
                self.assertEqual(self.bw.status, status)

    def test_not_unlocked_message_names_endpoint_and_status(self):
        message = self.bw.get_not_unlocked_message('locked')
        self.assertIn('http://127.0.0.1:8087', message)
        self.assertIn('"locked"', message)
        self.assertIn('bw serve', message)

    def test_not_unlocked_message_has_no_trailing_period(self):
        # AnsibleError appends ". <original message>" when it wraps an exception,
        # so a trailing period would show up doubled in the playbook output
        self.assertFalse(self.bw.get_not_unlocked_message('locked').endswith('.'))


class TestGetItems(unittest.TestCase):
    def setUp(self):
        self.bw = _make_bitwarden()
        # seed the in-memory cache directly; get_items only reads it
        self.bw._cache = {
            'items': [
                {
                    'type': 1,
                    'name': 'host - db',
                    'login': {'username': 'dba'},
                    'folderId': None,
                    'collectionIds': [],
                    'organizationId': None,
                },
                {
                    'type': 2,
                    'name': 'host - db',
                    'login': {'username': 'dba'},
                },  # non-login, skipped
                {
                    'type': 1,
                    'name': 'other',
                    'login': {'username': 'dba'},
                    'folderId': None,
                    'collectionIds': [],
                    'organizationId': None,
                },
            ],
        }

    def test_matches_login_item_by_name_and_username(self):
        matches = self.bw.get_items('host - db', username='dba')
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['name'], 'host - db')

    def test_skips_non_login_items(self):
        # the type=2 entry shares name+username but must not match
        matches = self.bw.get_items('host - db', username='dba')
        self.assertTrue(all(item.get('type') == 1 for item in matches))

    def test_no_match_returns_empty(self):
        self.assertEqual(self.bw.get_items('does-not-exist', username='dba'), [])


_LOGIN_ITEM = {
    'id': 'abc',
    'type': 1,
    'name': 'host - db',
    'login': {'username': 'dba', 'password': 'linuxfabrik'},
    'folderId': None,
    'collectionIds': [],
    'organizationId': None,
}


def _serve_in_order(*payloads):
    """Fake open_url that answers each call with the next payload.

    A payload that is an exception instance is raised instead.
    """
    remaining = list(payloads)
    calls = []

    def _open_url(url, *args, **kwargs):
        calls.append(url)
        payload = remaining.pop(0)
        if isinstance(payload, Exception):
            raise payload
        return _FakeResponse(payload)

    return _open_url, calls


def _items(*items):
    return {'success': True, 'data': {'object': 'list', 'data': list(items)}}


_SYNCED = {'success': True, 'data': {'object': 'message', 'title': 'Syncing complete.'}}


class TestEmptyListIsNotTrusted(unittest.TestCase):
    """bw serve briefly reports an empty vault right after a sync (#23283)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.bw = _make_bitwarden(os.path.join(self._tmp.name, 'cache.json'))
        self._orig_open_url = bitwarden.open_url

    def tearDown(self):
        bitwarden.open_url = self._orig_open_url
        self._tmp.cleanup()

    def test_empty_list_is_asked_again(self):
        bitwarden.open_url, calls = _serve_in_order(
            _items(), _items(), _items(_LOGIN_ITEM)
        )
        self.assertEqual(self.bw._list_items(delay=0), [_LOGIN_ITEM])
        self.assertEqual(len(calls), 3)

    def test_non_empty_list_is_not_asked_again(self):
        bitwarden.open_url, calls = _serve_in_order(_items(_LOGIN_ITEM))
        self.assertEqual(self.bw._list_items(delay=0), [_LOGIN_ITEM])
        self.assertEqual(len(calls), 1)

    def test_persistently_empty_list_raises(self):
        bitwarden.open_url, calls = _serve_in_order(*[_items()] * 3)
        with self.assertRaises(bitwarden.BitwardenException) as ctx:
            self.bw._list_items(retries=2, delay=0)
        self.assertEqual(len(calls), 3)
        self.assertIn('23283', str(ctx.exception))
        # AnsibleError appends ". <original message>", see TestStatus
        self.assertFalse(str(ctx.exception).endswith('.'))

    def test_sync_does_not_cache_an_empty_list(self):
        bitwarden.open_url, _calls = _serve_in_order(
            _SYNCED, _items(), _items(_LOGIN_ITEM)
        )
        # no real delay between the attempts
        self.bw._list_items = functools.partial(
            bitwarden.Bitwarden._list_items, self.bw, delay=0
        )
        self.bw.sync(force=True)
        self.assertEqual(self.bw.get_items('host - db', username='dba'), [_LOGIN_ITEM])

    def test_item_by_id_is_asked_again(self):
        self.bw._cache['items'] = []
        bitwarden.open_url, calls = _serve_in_order(
            HTTPError('http://127.0.0.1:8087/object/item/abc', 400, 'Bad', {}, None),
            {'success': True, 'data': _LOGIN_ITEM},
        )
        self.assertEqual(self.bw.get_item_by_id('abc', delay=0), _LOGIN_ITEM)
        self.assertEqual(len(calls), 2)

    def test_unknown_item_by_id_still_raises(self):
        self.bw._cache['items'] = []
        bitwarden.open_url, calls = _serve_in_order(
            *[{'success': False, 'data': 'Not found.'}] * 3
        )
        with self.assertRaises(bitwarden.BitwardenException):
            self.bw.get_item_by_id('abc', retries=2, delay=0)
        self.assertEqual(len(calls), 3)


def _create_if_missing(cache_file, created):
    """Worker for TestMutex: the lookup's search-then-create, run in its own process."""
    bitwarden.CACHE_FILE = cache_file
    bw = bitwarden.Bitwarden()
    with bw.mutex():
        if bw._cache['items'] is None:
            bw._cache['items'] = []
        if not bw.get_items('host - db', username='dba'):
            time.sleep(0.2)  # the time a create takes, the window of the race
            bw._cache['items'].append(_LOGIN_ITEM)
            bw._save_cache()
            created.put(os.getpid())


class TestMutex(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.cache_file = os.path.join(self._tmp.name, 'cache.json')

    def tearDown(self):
        self._tmp.cleanup()

    def test_parallel_processes_create_a_missing_item_once(self):
        # fork, so the children inherit the module loaded by file path above
        ctx = multiprocessing.get_context('fork')
        created = ctx.Queue()
        workers = [
            ctx.Process(target=_create_if_missing, args=(self.cache_file, created))
            for _ in range(8)
        ]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join(timeout=60)
            self.assertEqual(worker.exitcode, 0)
        creators = []
        with contextlib.suppress(queue.Empty):
            while True:
                creators.append(created.get(timeout=1))
        self.assertEqual(len(creators), 1)

    def test_mutex_times_out_while_another_holder_has_it(self):
        holder = _make_bitwarden(self.cache_file)
        waiter = bitwarden.Bitwarden()

        def _wait_for_the_mutex():
            with waiter.mutex(timeout=0.5):
                pass

        with holder.mutex():
            self.assertRaises(bitwarden.BitwardenException, _wait_for_the_mutex)
        # released, so the next one gets it
        _wait_for_the_mutex()

    def test_mutex_is_released_when_the_body_raises(self):
        # fail_json() in the module leaves the with block through SystemExit
        first = _make_bitwarden(self.cache_file)
        second = bitwarden.Bitwarden()
        with self.assertRaises(SystemExit), first.mutex():
            raise SystemExit(1)
        with second.mutex(timeout=0.5):
            pass

    def test_mutex_reloads_the_cache(self):
        first = _make_bitwarden(self.cache_file)
        second = bitwarden.Bitwarden()
        with first.mutex():
            first._cache['items'] = [_LOGIN_ITEM]
            first._save_cache()
        # `second` loaded the cache before `first` wrote it
        self.assertIsNone(second._cache['items'])
        with second.mutex():
            self.assertEqual(second._cache['items'], [_LOGIN_ITEM])


if __name__ == '__main__':
    unittest.main()
