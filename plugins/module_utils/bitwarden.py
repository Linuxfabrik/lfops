#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import contextlib
import copy
import email.encoders
import email.mime.application
import email.mime.multipart
import email.mime.nonmultipart
import email.parser
import email.policy
import fcntl
import json
import mimetypes
import os
import secrets
import tempfile
import time
from urllib.error import HTTPError, URLError

from ansible.module_utils.common.collections import Mapping
from ansible.module_utils.common.text.converters import to_bytes, to_native, to_text
from ansible.module_utils.six import string_types
from ansible.module_utils.urls import ConnectionError, SSLValidationError, open_url

try:
    from ansible.utils.display import Display

    display = Display()
except Exception:
    # When used from a module (not a lookup plugin), this code runs inside an AnsiballZ
    # process on the remote host where ansible.utils.display is not available, so the
    # import raises ImportError. Under Mitogen the import itself succeeds, because
    # Mitogen serves it from the controller, but loading ansible.constants then raises
    # AnsibleError ("Missing base YAML definition file"), since the data files are not
    # served along. Verified with Mitogen 0.3.53 and ansible-core 2.16 on Rocky Linux 9.
    class _NoopDisplay:
        def vvv(self, msg, **kwargs):
            pass

    display = _NoopDisplay()


def prepare_multipart_no_base64(fields):
    """Taken from ansible.module_utils.urls, but adjusted to not encode the payload, as the
    Bitwarden API does not work with that (even though it should according to the RFC,
    Content-Transfer-Encoding is deprecated but not removed).
    See https://github.com/ansible/ansible/issues/73621

    Takes a mapping, and prepares a multipart/form-data body

    :arg fields: Mapping
    :returns: tuple of (content_type, body) where ``content_type`` is
        the ``multipart/form-data`` ``Content-Type`` header including
        ``boundary`` and ``body`` is the prepared bytestring body

    Payload content from a file will be base64 encoded and will include
    the appropriate ``Content-Transfer-Encoding`` and ``Content-Type``
    headers.

    Example:
        {
            "file1": {
                "filename": "/bin/true",
                "mime_type": "application/octet-stream"
            },
            "file2": {
                "content": "text based file content",
                "filename": "fake.txt",
                "mime_type": "text/plain",
            },
            "text_form_field": "value"
        }
    """

    if not isinstance(fields, Mapping):
        raise TypeError(
            f'Mapping is required, cannot be type {fields.__class__.__name__}'
        )

    m = email.mime.multipart.MIMEMultipart('form-data')
    for field, value in sorted(fields.items()):
        if isinstance(value, string_types):
            main_type = 'text'
            sub_type = 'plain'
            content = value
            filename = None
        elif isinstance(value, Mapping):
            filename = value.get('filename')
            content = value.get('content')
            if not any((filename, content)):
                raise ValueError('at least one of filename or content must be provided')

            mime = value.get('mime_type')
            if not mime:
                try:
                    mime = (
                        mimetypes.guess_type(filename or '', strict=False)[0]
                        or 'application/octet-stream'
                    )
                except Exception:
                    mime = 'application/octet-stream'
            main_type, _sep, sub_type = mime.partition('/')
        else:
            raise TypeError(
                f'value must be a string, or mapping, cannot be type {value.__class__.__name__}'
            )

        if not content and filename:
            with open(to_bytes(filename, errors='surrogate_or_strict'), 'rb') as f:
                part = email.mime.application.MIMEApplication(
                    f.read(), _encoder=email.encoders.encode_noop
                )
                del part['Content-Type']
                part.add_header('Content-Type', f'{main_type}/{sub_type}')
        else:
            part = email.mime.nonmultipart.MIMENonMultipart(main_type, sub_type)
            part.set_payload(to_bytes(content))

        part.add_header('Content-Disposition', 'form-data')
        del part['MIME-Version']
        part.set_param('name', field, header='Content-Disposition')
        if filename:
            part.set_param(
                'filename',
                to_native(os.path.basename(filename)),
                header='Content-Disposition',
            )

        m.attach(part)

    # Ensure headers are not split over multiple lines
    # The HTTP policy also uses CRLF by default
    b_data = m.as_bytes(policy=email.policy.HTTP)
    del m

    headers, _sep, b_content = b_data.partition(b'\r\n\r\n')
    del b_data

    parser = email.parser.BytesHeaderParser().parsebytes

    return (
        parser(headers)['content-type'],  # Message converts to native strings
        b_content,
    )


CACHE_DIR = os.environ.get('XDG_RUNTIME_DIR', '/tmp')  # nosec B108 - cache files are created with mkstemp (mode 0600) and atomically replaced
CACHE_FILE = os.path.join(CACHE_DIR, 'lfops_bitwarden_cache.json')
CACHE_VERSION = 2026032701

# how long a process waits for another one to finish its sync, search and create
MUTEX_TIMEOUT = 300

# `bw serve` briefly reports an empty vault right after a sync, see
# https://github.com/bitwarden/clients/issues/23283
# Verified against bw 2026.8.0 and 2026.9.0 on Rocky Linux 9: the list recovers
# within a few seconds, so ask again a few times before giving up.
EMPTY_LIST_RETRIES = 5
EMPTY_LIST_RETRY_DELAY = 2


class BitwardenException(Exception):
    pass


class Bitwarden:
    # https://bitwarden.com/help/vault-management-api

    def __init__(self, hostname='127.0.0.1', port=8087):
        self._base_url = f'http://{hostname}:{port}'
        self._cache = None
        self._mutex_fd = None
        self._load_cache()

    def _acquire_mutex(self, timeout=MUTEX_TIMEOUT):
        """Take the mutex, waiting at most `timeout` seconds. Use mutex() instead."""
        if self._mutex_fd is not None:
            return
        mutex_file = f'{CACHE_FILE}.mutex'
        try:
            fd = os.open(mutex_file, os.O_RDWR | os.O_CREAT, 0o600)
        except OSError as e:
            raise BitwardenException(
                f'Unable to open the mutex file {mutex_file}: {to_native(e)}'
            ) from e
        deadline = time.time() + timeout
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.time() >= deadline:
                    os.close(fd)
                    raise BitwardenException(
                        f'Another process has held {mutex_file} for more than {timeout}s. '
                        'Check for a hanging Ansible run using the Bitwarden lookup or module'
                    ) from None
                time.sleep(0.2)
        self._mutex_fd = fd
        display.vvv(f'lfbw - acquired mutex {mutex_file}')
        self._load_cache()

    def _release_mutex(self):
        if self._mutex_fd is None:
            return
        fcntl.flock(self._mutex_fd, fcntl.LOCK_UN)
        os.close(self._mutex_fd)
        self._mutex_fd = None
        display.vvv('lfbw - released mutex')

    @contextlib.contextmanager
    def mutex(self, timeout=MUTEX_TIMEOUT):
        """Let only one process at a time sync, search and create.

        Ansible evaluates a lookup in one worker process per host. Without the mutex,
        workers that all miss an item create it once each, and each one overwrites the
        cache file with its own view of the vault. The cache is re-read once the mutex
        is held, so a process sees what the previous holder synced or created.

        Hold it only for the duration of one lookup or module run. flock() belongs to
        the open file, not to the process, so a second Bitwarden() in the same process,
        for example the next evaluation of the same lookup, would otherwise wait for
        the first one. This is also why the release must not be left to the end of the
        process: Mitogen can run modules in an interpreter that stays alive.
        """
        self._acquire_mutex(timeout)
        try:
            yield self
        finally:
            self._release_mutex()

    def _api_call(self, url_path, method='GET', body=None, body_format='json'):
        url = f'{self._base_url}/{url_path}'

        headers = {}
        if body:
            if body_format == 'json':
                body = json.dumps(body)
                headers['Content-Type'] = 'application/json'
            elif body_format == 'form-multipart':
                try:
                    content_type, body = prepare_multipart_no_base64(body)
                except (TypeError, ValueError) as e:
                    raise BitwardenException(
                        f'failed to parse body as form-multipart: {to_native(e)}'
                    ) from e
                headers['Content-Type'] = content_type

        # mostly taken from ansible.builtin.url lookup plugin
        try:
            # increased the timeout since listing all items via `list/object/items` takes forever (13s for ~2500 items)
            response = open_url(
                url, method=method, data=body, headers=headers, timeout=60
            )
        except HTTPError as e:
            raise BitwardenException(
                f'Received HTTP error for {url} : {to_native(e)}'
            ) from e
        except URLError as e:
            raise BitwardenException(
                f'Failed lookup url for {url} : {to_native(e)}'
            ) from e
        except SSLValidationError as e:
            raise BitwardenException(
                f"Error validating the server's certificate for {url}: {to_native(e)}"
            ) from e
        except ConnectionError as e:
            raise BitwardenException(
                f'Error connecting to {url}: {to_native(e)}'
            ) from e

        try:
            result = json.loads(to_text(response.read()))
        except json.decoder.JSONDecodeError as e:
            raise BitwardenException(f'Unable to load JSON: {to_native(e)}') from e

        if not result.get('success'):
            raise BitwardenException(f'API call failed: {result.get("data")}')

        return result

    def _load_cache(self):
        """Load the cache from disk. If missing, unreadable, or invalid, start with an empty cache.
        Freshness is handled by sync().
        """
        try:
            with open(CACHE_FILE, 'r') as f:
                data = json.load(f)
            if data.get('version') == CACHE_VERSION:
                self._cache = data
                item_count = (
                    len(self._cache['items']) if self._cache['items'] is not None else 0
                )
                display.vvv(
                    f'lfbw - cache loaded from {CACHE_FILE} ({item_count} items)'
                )
                return
        except (OSError, ValueError, json.decoder.JSONDecodeError):
            pass
        self._cache = {
            'version': CACHE_VERSION,
            'sync_timestamp': 0,
            'items': None,
            'templates': {},
        }
        display.vvv('lfbw - no valid cache found, starting fresh')

    def _save_cache(self):
        """Write the cache to disk atomically."""
        try:
            fd, tmp_path = tempfile.mkstemp(
                dir=os.path.dirname(CACHE_FILE),
                prefix='.lfops_bw_cache_',
            )
            try:
                with os.fdopen(fd, 'w') as f:
                    json.dump(self._cache, f)
                os.replace(tmp_path, CACHE_FILE)
                display.vvv(f'lfbw - cache saved to {CACHE_FILE}')
            except Exception:
                os.unlink(tmp_path)
                raise
        except OSError:
            display.vvv(f'lfbw - failed to save cache to {CACHE_FILE}')

    def _get_template(self, template_name):
        """Return a template from cache, fetching from API on first use.
        Templates are static API schema definitions that never change.
        """
        if template_name not in self._cache['templates']:
            display.vvv(f'lfbw - fetching template "{template_name}" from API')
            result = self._api_call(f'object/template/{template_name}')
            self._cache['templates'][template_name] = result['data']['template']
            self._save_cache()
        else:
            display.vvv(f'lfbw - using cached template "{template_name}"')
        return copy.deepcopy(self._cache['templates'][template_name])

    @property
    def status(self):
        """Vault status as reported by the `bw serve` API.

        Exactly one of 'unauthenticated' (not logged in), 'locked' (logged in, vault
        locked) or 'unlocked'. Verified against the StatusCommand of bw 2026.8.0, which
        declares these three and no others.
        """
        result = self._api_call('status')
        return result['data']['template']['status']

    def get_not_unlocked_message(self, status):
        """Error message for a `bw serve` whose vault cannot be read.

        Shared by the lookup plugin and the module so both give the same advice.
        """
        return (
            f'The Bitwarden vault behind `bw serve` at {self._base_url} reports '
            f'status "{status}", expected "unlocked". `bw serve` keeps its own session, '
            'taken from the environment it was started in, so `bw status` in your '
            'shell can report "unlocked" while this API does not. Run `bw login` if '
            'needed, then `export BW_SESSION="$(bw unlock --raw)"` and restart '
            '`bw serve`'
        )

    def sync(self, force=False, interval=60):
        """Pull the latest vault data from server and repopulate the items cache.
        Syncs only if the last sync was more than `interval` seconds ago, unless `force` is True.
        """
        if not force and time.time() - self._cache.get('sync_timestamp', 0) < interval:
            display.vvv('lfbw - sync skipped, last sync was recent enough')
            return
        display.vvv(f'lfbw - syncing vault (force={force})')
        self._api_call('sync', method='POST')
        self._cache['items'] = self._list_items()
        self._cache['sync_timestamp'] = time.time()
        display.vvv(f'lfbw - sync complete, cached {len(self._cache["items"])} items')
        self._save_cache()

    def _list_items(self, retries=EMPTY_LIST_RETRIES, delay=EMPTY_LIST_RETRY_DELAY):
        """Return all items of the vault. An empty list is not trusted.

        Right after a sync, `bw serve` answers `list/object/items` with `success: true`
        and no items for a few seconds. Taken at face value, every item would look
        missing and be created again, so ask again, and give up rather than accept an
        empty vault.
        """
        for attempt in range(retries + 1):
            items = self._api_call('list/object/items')['data']['data']
            if items:
                return items
            if attempt < retries:
                display.vvv(
                    f'lfbw - bw serve returned an empty item list, retrying in {delay}s'
                )
                time.sleep(delay)
        raise BitwardenException(
            f'`bw serve` reported an empty vault {retries + 1} times in a row. It does '
            'that for a few seconds after a sync '
            '(https://github.com/bitwarden/clients/issues/23283), so the list is not '
            'trusted, since every item would look missing and be created again. If the '
            'vault really is empty, create any item in it first'
        )

    def get_items(
        self,
        name,
        username=None,
        folder_id=None,
        collection_id=None,
        organization_id=None,
    ):
        """Search for items in Bitwarden. Returns a list of the items that *exactly* matches all the parameters.

        A complete object:
        {
          "object": "item",
          "id": "60020baa-e876-4fd4-b5bc-259b5e6389a8",
          "organizationId": "44906ecb-b307-47a5-92b4-a097745592ed",
          "folderId": null,
          "type": 1,
          "reprompt": 0,
          "name": "myhost - purpose",
          "notes": "Generated by Ansible.",
          "favorite": false,
          "login": {
            "uris": [
              {
                "match": null,
                "uri": "https://www.example.com"
              }
            ],
            "username": "username",
            "password": "password",
            "totp": null,
            "passwordRevisionDate": null
          },
          "collectionIds": [
            "153e991a-a56f-4e5d-9dea-c13b9e693fc4"
          ],
          "revisionDate": "2022-06-26T06:00:00.000Z"
        }
        """

        # convert empty string to None
        # else the matching later on fails
        if isinstance(username, str) and len(username.strip()) == 0:
            username = None
        if isinstance(folder_id, str) and len(folder_id.strip()) == 0:
            folder_id = None
        if isinstance(collection_id, str) and len(collection_id.strip()) == 0:
            collection_id = None
        if isinstance(organization_id, str) and len(organization_id.strip()) == 0:
            organization_id = None

        display.vvv(f'lfbw - searching cache for name="{name}", username="{username}"')
        matching_items = []
        for item in self._cache['items']:
            if item.get('type') != 1:
                continue  # skip non-login items (cards, secure notes, identities)
            if (
                item['name'] == name
                and (item['login']['username'] == username)
                and (item.get('folderId') == folder_id)
                and (
                    # cover case if collectionIds is an empty list
                    (collection_id is None and not item.get('collectionIds'))
                    or (collection_id in item.get('collectionIds', []))
                )
                and (item.get('organizationId') == organization_id)
            ):
                matching_items.append(item)

        display.vvv(f'lfbw - found {len(matching_items)} matching item(s)')
        return matching_items

    def get_item_by_id(
        self, item_id, retries=EMPTY_LIST_RETRIES, delay=EMPTY_LIST_RETRY_DELAY
    ):
        """Get an item by ID from Bitwarden. Looks in the cache first, then falls back to the
        API (the item may have been created externally). Returns the item; raises
        BitwardenException if the API does not know the ID.
        """
        display.vvv(f'lfbw - looking up item by id={item_id}')
        for item in self._cache['items']:
            if item.get('id') == item_id:
                display.vvv('lfbw - found item in cache')
                return item
        # fallback to API if not found in cache (item could have been created externally)
        display.vvv('lfbw - item not in cache, falling back to API')
        # in the same window after a sync in which `list/object/items` comes back empty,
        # `bw serve` answers 400 for an existing item, see _list_items()
        for attempt in range(retries + 1):
            try:
                return self._api_call(f'object/item/{item_id}')['data']
            except BitwardenException:
                if attempt == retries:
                    raise
                display.vvv(f'lfbw - item lookup failed, retrying in {delay}s')
                time.sleep(delay)

    def generate(
        self,
        password_length=60,
        password_choice='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
    ):  # nosec B107 - this is the character set to draw from, not a password
        """Generates a random password of a given length. If you want to generate a hex-based
        password, ensure that password_length is positive and even (as hex characters typically
        come in pairs representing bytes), and that password_choice is set to '0123456789abcdef'.

        We do not use Bitwarden's "generate?mypass" API function, as it can't create more than 128
        chars, doesn't let you handle the characters in detail, and can't create passwords using hex
        characters (0-9 and a-f).
        """
        if password_length <= 0:
            raise ValueError('Password length must be a positive integer')
        if password_choice.lower() == '0123456789abcdef' and password_length % 2 != 0:
            raise ValueError(
                'Password length must be an even number to represent full hex bytes'
            )
        return ''.join(secrets.choice(password_choice) for _ in range(password_length))

    def get_template_item_login_uri(self, uris):
        """Get an item.login.uri object from the vault.

        A complete object:

        {
          "match": null,
          "uri": "https://google.com"
        }
        """
        login_uris = []
        if uris:
            template = self._get_template('item.login.uri')
            for uri in uris:
                login_uri = (
                    template.copy()
                )  # make sure we are not editing the same object repeatedly
                login_uri['uri'] = uri
                login_uris.append(login_uri)

        return login_uris

    def get_template_item_login(self, username=None, password=None, login_uris=None):
        """Get an item.login object from the vault.

        A complete object:

        {
          "uris": [],
          "username": "jdoe",
          "password": "myp@ssword123",
          "totp": "JBSWY3DPEHPK3PXP"
        }
        """
        login = self._get_template('item.login')
        login['password'] = password
        login['totp'] = ''
        login['uris'] = login_uris or []
        login['username'] = username

        return login

    def get_template_item(
        self,
        name,
        login=None,
        notes=None,
        organization_id=None,
        collection_ids=None,
        folder_id=None,
    ):
        """Get an item.login object from the vault.

        A complete item object:

        {
          "organizationId": null,
          "collectionIds": null,
          "folderId": null,
          "type": 1,
          "name": "Item name",
          "notes": "Some notes about this item.",
          "favorite": false,
          "fields": [],
          "login": null,
          "secureNote": null,
          "card": null,
          "identity": null,
          "reprompt": 0
        }
        """
        item = self._get_template('item')
        item['collectionIds'] = collection_ids
        item['folderId'] = folder_id
        item['login'] = login
        item['name'] = name
        item['notes'] = notes
        item['organizationId'] = organization_id

        return item

    def create_item(self, item):
        """Creates an item object in Bitwarden."""
        display.vvv(f'lfbw - creating item "{item.get("name", "")}"')
        result = self._api_call('object/item', method='POST', body=item)
        self._cache['items'].append(result['data'])
        self._save_cache()
        time.sleep(1)
        return result['data']

    def edit_item(self, item, item_id):
        """Edits an item object in Bitwarden."""
        display.vvv(f'lfbw - editing item {item_id}')
        result = self._api_call(f'object/item/{item_id}', method='PUT', body=item)
        for i, cached_item in enumerate(self._cache['items']):
            if cached_item.get('id') == item_id:
                self._cache['items'][i] = result['data']
                break
        self._save_cache()
        time.sleep(1)
        return result['data']

    def add_attachment(self, item_id, attachment_path):
        """Adds the file at `attachment_path` to the item specified by `item_id`"""
        display.vvv(f'lfbw - adding attachment "{attachment_path}" to item {item_id}')

        body = {
            'file': {
                'filename': attachment_path,
            },
        }
        result = self._api_call(
            f'attachment?itemId={item_id}',
            method='POST',
            body=body,
            body_format='form-multipart',
        )
        for i, cached_item in enumerate(self._cache['items']):
            if cached_item.get('id') == item_id:
                self._cache['items'][i] = result['data']
                break
        self._save_cache()
        time.sleep(1)
        return result

    @staticmethod
    def get_pretty_name(name, hostname=None, purpose=None):
        """create a nice name for the item if none is given
        schemes:
        * hostname - purpose (for example "app4711 - MariaDB")
        * hostname (for example "app4711")
        """
        if not name:
            name = hostname
            if purpose:
                name += f' - {purpose}'

        return name
