#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Linuxfabrik, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

from __future__ import absolute_import, division, print_function

import email.encoders
import email.mime.application
import email.mime.multipart
import email.mime.nonmultipart
import email.parser
import email.utils
import json
import mimetypes
import os
import secrets
import urllib.parse
from urllib.error import HTTPError, URLError

from ansible.module_utils.common.collections import Mapping
from ansible.module_utils.six import PY2, PY3, string_types
from ansible.module_utils.six.moves import cStringIO

try:
    import email.policy
except ImportError:
    # Py2
    import email.generator

from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible.module_utils.urls import (ConnectionError, SSLValidationError,
                                       open_url)


def prepare_multipart_no_base64(fields):
    """Taken from ansible.module_utils.urls, but adjusted to not no encoding as the bitwarden API does not work with that
    (even though it should according to the RFC, Content-Transfer-Encoding is deprecated but not removed).
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
            'Mapping is required, cannot be type %s' % fields.__class__.__name__
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
                    mime = mimetypes.guess_type(filename or '', strict=False)[0] or 'application/octet-stream'
                except Exception:
                    mime = 'application/octet-stream'
            main_type, sep, sub_type = mime.partition('/')
        else:
            raise TypeError(
                'value must be a string, or mapping, cannot be type %s' % value.__class__.__name__
            )

        if not content and filename:
            with open(to_bytes(filename, errors='surrogate_or_strict'), 'rb') as f:
                part = email.mime.application.MIMEApplication(f.read(), _encoder=email.encoders.encode_noop)
                del part['Content-Type']
                part.add_header('Content-Type', '%s/%s' % (main_type, sub_type))
        else:
            part = email.mime.nonmultipart.MIMENonMultipart(main_type, sub_type)
            part.set_payload(to_bytes(content))

        part.add_header('Content-Disposition', 'form-data')
        del part['MIME-Version']
        part.set_param(
            'name',
            field,
            header='Content-Disposition'
        )
        if filename:
            part.set_param(
                'filename',
                to_native(os.path.basename(filename)),
                header='Content-Disposition'
            )

        m.attach(part)

    if PY3:
        # Ensure headers are not split over multiple lines
        # The HTTP policy also uses CRLF by default
        b_data = m.as_bytes(policy=email.policy.HTTP)
    else:
        # Py2
        # We cannot just call ``as_string`` since it provides no way
        # to specify ``maxheaderlen``
        fp = cStringIO()  # cStringIO seems to be required here
        # Ensure headers are not split over multiple lines
        g = email.generator.Generator(fp, maxheaderlen=0)
        g.flatten(m)
        # ``fix_eols`` switches from ``\n`` to ``\r\n``
        b_data = email.utils.fix_eols(fp.getvalue())
    del m

    headers, sep, b_content = b_data.partition(b'\r\n\r\n')
    del b_data

    if PY3:
        parser = email.parser.BytesHeaderParser().parsebytes
    else:
        # Py2
        parser = email.parser.HeaderParser().parsestr

    return (
        parser(headers)['content-type'],  # Message converts to native strings
        b_content
    )


class BitwardenException(Exception):
    pass


class Bitwarden(object):
    # https://bitwarden.com/help/vault-management-api

    def __init__(self, hostname='127.0.0.1', port=8087):
        self._base_url = 'http://%s:%s' % (hostname, port)

    def _api_call(self, url_path, method='GET', body=None, body_format='json'):
        url = '%s/%s' % (self._base_url, url_path)

        headers = {}
        if body:
            if body_format == 'json':
                body = json.dumps(body)
                headers['Content-Type'] = 'application/json'
            elif body_format == 'form-multipart':
                try:
                    content_type, body = prepare_multipart_no_base64(body)
                except (TypeError, ValueError) as e:
                    BitwardenException('failed to parse body as form-multipart: %s' % to_native(e))
                headers['Content-Type'] = content_type

        # mostly taken from ansible.builtin.url lookup plugin
        try:
            response = open_url(url, method=method, data=body, headers=headers)
        except HTTPError as e:
            raise BitwardenException("Received HTTP error for %s : %s" % (url, to_native(e)))
        except URLError as e:
            raise BitwardenException("Failed lookup url for %s : %s" % (url, to_native(e)))
        except SSLValidationError as e:
            raise BitwardenException("Error validating the server's certificate for %s: %s" % (url, to_native(e)))
        except ConnectionError as e:
            raise BitwardenException("Error connecting to %s: %s" % (url, to_native(e)))

        try:
            result = json.loads(to_text(response.read()))
        except json.decoder.JSONDecodeError as e:
            raise BitwardenException('Unable to load JSON: %s' % (to_native(e)))

        if not result.get('success'):
            raise BitwardenException('API call failed: %s' % (result.get('data')))

        return result


    def is_unlocked(self):
        """Check if the Bitwarden vault is unlocked.
        """
        result = self._api_call('status')
        return result['data']['template']['status'] == 'unlocked'


    def sync(self):
        """Pull the latest vault data from server.
        """
        return self._api_call('sync', method='POST')


    def get_items(self, name, username=None, folder_id=None, collection_id=None, organization_id=None):
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

        params = urllib.parse.urlencode(
            {
                'search': name,
            },
            quote_via=urllib.parse.quote,
        )
        result = self._api_call('list/object/items?%s' % (params))

        # make sure that all the given parameters exactly match the requested one, as `bw` is not that precise (only performs a search)
        # we are not using the filter parameters of the `bw` utility, as they perform an OR operation, but we want AND
        matching_items = []
        for item in result['data']['data']:
            if item['name'] == name \
            and (item['login']['username'] == username) \
            and (item.get('folderId') == folder_id) \
            and (
                # cover case if collectionIds is an empty list
                (collection_id is None and not item.get('collectionIds')) \
                or \
                (collection_id in item.get('collectionIds', [])) \
            ) \
            and (item.get('organizationId') == organization_id):
                matching_items.append(item)

        return matching_items


    def get_item_by_id(self, item_id):
        """Get an item by ID from Bitwarden. Returns the item or None. Throws an exception if the id leads to unambiguous results.
        """

        result = self._api_call('object/item/%s' % (item_id))
        return result['data']


    def generate(self, password_length=60, password_choice='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        """Generates a random password of a given length. If you want to generate a hex-based
        password, ensure that password_length is positive and even (as hex characters typically
        come in pairs representing bytes), and that password_choice is set to '0123456789abcdef'.

        We do not use Bitwarden's "generate?mypass" API function, as it can't create more than 128
        chars, doesn't let you handle the characters in detail, and can't create passwords using hex
        characters (0-9 and a-f).
        """
        if password_length <= 0:
            raise ValueError('Password length must be a positive integer.')
        if password_choice.lower() == '0123456789abcdef' and password_length % 2 != 0:
            raise ValueError('Password length must be an even number to represent full hex bytes.')
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
            # To create uris, fetch the JSON structure for that.
            result = self._api_call('object/template/item.login.uri')
            template = result['data']['template']
            for uri in uris:
                login_uri = template.copy() # make sure we are not editing the same object repeatedly
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
        # To create a login item, fetch the JSON structure for that.
        result = self._api_call('object/template/item.login')
        login = result['data']['template']
        login['password'] = password
        login['totp'] = ''
        login['uris'] = login_uris or []
        login['username'] = username

        return login


    def get_template_item(self, name, login=None, notes=None, organization_id=None, collection_ids=None, folder_id=None):
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
        # To create an item later on, fetch the item JSON structure, and fill in the appropriate
        # values.
        result = self._api_call('object/template/item')
        item = result['data']['template']
        item['collectionIds'] = collection_ids
        item['folderId'] = folder_id
        item['login'] = login
        item['name'] = name
        item['notes'] = notes
        item['organizationId'] = organization_id

        return item


    def create_item(self, item):
        """Creates an item object in Bitwarden.
        """
        result = self._api_call('object/item', method='POST', body=item)
        return result['data']


    def edit_item(self, item, item_id):
        """Edits an item object in Bitwarden.
        """
        result = self._api_call('object/item/%s' % (item_id), method='PUT', body=item)
        return result['data']


    def add_attachment(self, item_id, attachment_path):
        """Adds the file at `attachment_path` to the item specified by `item_id`
        """

        body = {
            'file': {
                'filename': attachment_path,
            },
        }
        result = self._api_call('attachment?itemId=%s' % (item_id), method='POST', body=body, body_format='form-multipart')
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
                name += ' - {}'.format(purpose)

        return name
