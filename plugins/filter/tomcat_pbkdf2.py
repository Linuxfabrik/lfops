#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import hashlib

from ansible.errors import AnsibleFilterError

DOCUMENTATION = r"""
  name: tomcat_pbkdf2
  version_added: "10.0.0"
  short_description: Hash a password for Tomcat's SecretKeyCredentialHandler
  description:
    - Returns the stored form that Apache Tomcat's C(org.apache.catalina.realm.SecretKeyCredentialHandler) expects in C(tomcat-users.xml), which is C(<hex salt>$<iterations>$<hex key>).
    - The key is derived with PBKDF2-HMAC-SHA512 from the UTF-8 encoded password. The handler therefore has to be configured with C(algorithm="PBKDF2WithHmacSHA512").
    - Tomcat reads the salt, the iteration count and the key length from the stored value, so the corresponding handler attributes only matter for hashes that Tomcat creates itself.
    - The salt is taken as given, so the result is deterministic and the template that uses it stays idempotent. Pass a salt that differs per host and user.
  positional: _input, salt
  options:
    _input:
      description: The password in clear text.
      type: str
      required: true
    salt:
      description: The salt as a hexadecimal string, for example 32 hex digits for 16 bytes.
      type: str
      required: true
    iterations:
      description: The number of PBKDF2 iterations.
      type: int
      default: 210000
    key_length:
      description: The length of the derived key in bits. Must be a multiple of 8.
      type: int
      default: 512
"""

EXAMPLES = r"""
- name: 'Hash the password of a Tomcat user'
  ansible.builtin.debug:
    # a salt of 16 bytes (32 hex digits) that is stable per host and user, so re-runs render the same file
    msg: '{{ "linuxfabrik" | linuxfabrik.lfops.tomcat_pbkdf2(salt=((inventory_hostname ~ ":tomcat-admin") | hash("sha256"))[:32]) }}'
"""

RETURN = r"""
  _value:
    description: The stored credential, C(<hex salt>$<iterations>$<hex key>).
    type: str
"""


def tomcat_pbkdf2(password, salt, iterations=210000, key_length=512):
    """Return `<hex salt>$<iterations>$<hex key>` as Tomcat's SecretKeyCredentialHandler stores it.

    Tomcat derives the key with `PBEKeySpec(password.toCharArray(), ...)`, and the JDK's
    PBKDF2 implementation encodes those characters as UTF-8. Verified against
    `org.apache.catalina.realm.RealmBase` of tomcat-9.0.120 (OpenJDK 8, Rocky 8) and
    tomcat-10.1.49 (OpenJDK 21, Rocky 10), including a non-ASCII password.
    """
    if not isinstance(password, str):
        raise AnsibleFilterError(
            f'tomcat_pbkdf2: the password must be a string, got {type(password).__name__}'
        )
    try:
        salt_bytes = bytes.fromhex(salt)
    except (TypeError, ValueError) as e:
        raise AnsibleFilterError(
            f'tomcat_pbkdf2: the salt must be a hexadecimal string, got {salt!r}'
        ) from e
    if not salt_bytes:
        raise AnsibleFilterError('tomcat_pbkdf2: the salt must not be empty')
    if (
        isinstance(iterations, bool)
        or not isinstance(iterations, int)
        or iterations < 1
    ):
        raise AnsibleFilterError(
            f'tomcat_pbkdf2: iterations must be a positive integer, got {iterations!r}'
        )
    if (
        isinstance(key_length, bool)
        or not isinstance(key_length, int)
        or key_length < 8
        or key_length % 8
    ):
        raise AnsibleFilterError(
            f'tomcat_pbkdf2: key_length must be a positive multiple of 8, got {key_length!r}'
        )

    key = hashlib.pbkdf2_hmac(
        'sha512',
        password.encode('utf-8'),
        salt_bytes,
        iterations,
        dklen=key_length // 8,
    )
    # Tomcat's HexUtils.toHexString() writes lowercase digits; the comparison ignores case
    # anyway, but keeping the salt as given would make the output depend on its spelling.
    return f'{salt_bytes.hex()}${iterations}${key.hex()}'


class FilterModule:
    """Register custom filter plugins in Ansible"""

    def filters(self):
        return {
            'tomcat_pbkdf2': tomcat_pbkdf2,
        }
