#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the systemd_credential module.

Covers the name validation, the systemd version parsing, the file handling and
the whole state logic in apply(): idempotence, check mode, migration between
the stores, symlinks and wrong owners. systemd-creds is replaced by a fake that
"encrypts" by prefixing `ENC:`, and both stores are redirected into a temporary
directory owned by the user running the tests. The collection import is wired
up by tests/conftest.py.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import shutil
import stat
import tempfile
import unittest

from ansible_collections.linuxfabrik.lfops.plugins.modules import systemd_credential


class FakeModule:
    """Stands in for AnsibleModule. run_command() emulates `systemd-creds encrypt - -` and
    `systemd-creds decrypt <path> -`, and records every call.
    """

    def __init__(self, fail_encrypt=False):
        self.calls = []
        self.fail_encrypt = fail_encrypt

    def run_command(self, args, data=None, **kwargs):
        self.calls.append((args, data, kwargs))
        if args[1] == 'encrypt':
            if self.fail_encrypt:
                return 1, b'', b'boom'
            return 0, b'ENC:' + data, b''
        if args[1] == 'decrypt':
            with open(args[3], 'rb') as f:
                content = f.read()
            if content.startswith(b'ENC:'):
                return 0, content[4:], b''
            return 1, b'', b'Decryption failed'
        raise AssertionError(f'unexpected command {args}')

    def fail_json(self, **kwargs):
        raise AssertionError(kwargs['msg'])


def mode(path):
    return stat.S_IMODE(os.lstat(path).st_mode)


class StoreTestCase(unittest.TestCase):
    """Redirects both stores and the owner into a temporary directory."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.old_umask = os.umask(0o022)
        self.saved = (
            systemd_credential.ENCRYPTED_DIR,
            systemd_credential.PLAIN_DIR,
            systemd_credential.OWNER_UID,
            systemd_credential.OWNER_GID,
        )
        systemd_credential.ENCRYPTED_DIR = os.path.join(self.tmp, 'credstore.encrypted')
        systemd_credential.PLAIN_DIR = os.path.join(self.tmp, 'credstore')
        systemd_credential.OWNER_UID = os.getuid()
        systemd_credential.OWNER_GID = os.getgid()
        self.enc_path = os.path.join(systemd_credential.ENCRYPTED_DIR, 'cred')
        self.plain_path = os.path.join(systemd_credential.PLAIN_DIR, 'cred')

    def tearDown(self):
        (
            systemd_credential.ENCRYPTED_DIR,
            systemd_credential.PLAIN_DIR,
            systemd_credential.OWNER_UID,
            systemd_credential.OWNER_GID,
        ) = self.saved
        os.umask(self.old_umask)
        shutil.rmtree(self.tmp)

    def apply(
        self,
        data=b'secret',
        state='present',
        encrypted=True,
        check_mode=False,
        module=None,
    ):
        return systemd_credential.apply(
            module or FakeModule(),
            'cred',
            data,
            state,
            encrypted,
            'systemd-creds',
            check_mode,
        )

    def read(self, path):
        with open(path, 'rb') as f:
            return f.read()


class TestIsValidName(unittest.TestCase):
    def test_valid(self):
        for name in ('mariadb-dump-login.cnf', 'a', 'A_b-1.2', '_x'):
            self.assertTrue(systemd_credential.is_valid_name(name), name)

    def test_invalid(self):
        for name in (
            '',
            '.',
            '..',
            '../x',
            'a/b',
            '/etc/passwd',
            '.hidden',
            'a b',
            'ä',
            'foo\n',
        ):
            self.assertFalse(systemd_credential.is_valid_name(name), repr(name))

    def test_too_long(self):
        self.assertFalse(systemd_credential.is_valid_name('a' * 256))


class TestParseSystemdVersion(unittest.TestCase):
    def test_show_property(self):
        self.assertEqual(systemd_credential.parse_systemd_version('252-51.el9\n'), 252)
        self.assertEqual(
            systemd_credential.parse_systemd_version('257.13-1~deb13u1\n'), 257
        )

    def test_version_output(self):
        output = 'systemd 252 (252-51.el9)\n+PAM +AUDIT +SELINUX\n'
        self.assertEqual(systemd_credential.parse_systemd_version(output), 252)

    def test_garbage(self):
        self.assertIsNone(systemd_credential.parse_systemd_version('not systemd'))
        self.assertIsNone(systemd_credential.parse_systemd_version(''))


class TestEncrypted(StoreTestCase):
    def test_create_and_idempotence(self):
        changed, path = self.apply()
        self.assertTrue(changed)
        self.assertEqual(path, self.enc_path)
        self.assertEqual(self.read(self.enc_path), b'ENC:secret')
        self.assertEqual(mode(self.enc_path), 0o600)
        self.assertEqual(mode(systemd_credential.ENCRYPTED_DIR), 0o700)
        self.assertEqual(self.apply(), (False, self.enc_path))

    def test_secret_never_in_argv(self):
        module = FakeModule()
        self.apply(module=module)
        self.apply(module=module)
        for args, _data, kwargs in module.calls:
            self.assertFalse(any('secret' in a for a in args), args)
            self.assertTrue(kwargs['binary_data'])
            self.assertIsNone(kwargs['encoding'])
        encrypt_calls = [c for c in module.calls if c[0][1] == 'encrypt']
        self.assertEqual(
            encrypt_calls[0][0], ['systemd-creds', 'encrypt', '--name=cred', '-', '-']
        )
        self.assertEqual(encrypt_calls[0][1], b'secret')

    def test_content_change(self):
        self.apply()
        self.assertEqual(self.apply(data=b'other'), (True, self.enc_path))
        self.assertEqual(self.read(self.enc_path), b'ENC:other')

    def test_trailing_newline_counts(self):
        self.apply()
        self.assertTrue(self.apply(data=b'secret\n')[0])

    def test_undecryptable_is_replaced(self):
        # e.g. lost host key
        self.apply()
        with open(self.enc_path, 'wb') as f:
            f.write(b'garbage')
        self.assertTrue(self.apply()[0])
        self.assertEqual(self.read(self.enc_path), b'ENC:secret')

    def test_check_mode_writes_nothing(self):
        changed, _ = self.apply(check_mode=True)
        self.assertTrue(changed)
        self.assertFalse(os.path.lexists(systemd_credential.ENCRYPTED_DIR))
        self.apply()
        module = FakeModule()
        self.assertTrue(self.apply(data=b'other', check_mode=True, module=module)[0])
        self.assertEqual(self.read(self.enc_path), b'ENC:secret')
        self.assertEqual([c for c in module.calls if c[0][1] == 'encrypt'], [])

    def test_wrong_mode_is_fixed(self):
        self.apply()
        os.chmod(self.enc_path, 0o644)
        self.assertTrue(self.apply()[0])
        self.assertEqual(mode(self.enc_path), 0o600)
        os.chmod(systemd_credential.ENCRYPTED_DIR, 0o755)
        self.assertTrue(self.apply()[0])
        self.assertEqual(mode(systemd_credential.ENCRYPTED_DIR), 0o700)

    def test_migration_removes_plain_copy(self):
        self.apply(encrypted=False)
        self.assertTrue(os.path.exists(self.plain_path))
        self.assertTrue(self.apply()[0])
        self.assertFalse(os.path.lexists(self.plain_path))
        self.assertEqual(self.read(self.enc_path), b'ENC:secret')

    def test_encrypt_failure_keeps_old_credential(self):
        self.apply()
        with self.assertRaises(AssertionError) as ctx:
            self.apply(data=b'other', module=FakeModule(fail_encrypt=True))
        self.assertIn('boom', str(ctx.exception))
        self.assertNotIn('other', str(ctx.exception))
        self.assertEqual(self.read(self.enc_path), b'ENC:secret')
        self.assertEqual(os.listdir(systemd_credential.ENCRYPTED_DIR), ['cred'])


class TestPlain(StoreTestCase):
    def test_create_and_idempotence(self):
        changed, path = self.apply(encrypted=False)
        self.assertTrue(changed)
        self.assertEqual(path, self.plain_path)
        self.assertEqual(self.read(self.plain_path), b'secret')
        self.assertEqual(mode(self.plain_path), 0o600)
        self.assertEqual(mode(systemd_credential.PLAIN_DIR), 0o700)
        self.assertEqual(os.listdir(systemd_credential.PLAIN_DIR), ['cred'])
        self.assertEqual(self.apply(encrypted=False), (False, self.plain_path))

    def test_check_mode_writes_nothing(self):
        self.assertTrue(self.apply(encrypted=False, check_mode=True)[0])
        self.assertFalse(os.path.lexists(systemd_credential.PLAIN_DIR))

    def test_stale_encrypted_copy_is_removed(self):
        self.apply()
        self.assertTrue(self.apply(encrypted=False)[0])
        self.assertFalse(os.path.lexists(self.enc_path))

    def test_symlinked_credential_is_replaced_not_followed(self):
        os.makedirs(systemd_credential.PLAIN_DIR, 0o700)
        target = os.path.join(self.tmp, 'unrelated')
        with open(target, 'wb') as f:
            f.write(b'secret')
        os.chmod(target, 0o644)
        os.symlink(target, self.plain_path)
        self.assertTrue(self.apply(encrypted=False)[0])
        self.assertFalse(os.path.islink(self.plain_path))
        self.assertEqual(self.read(self.plain_path), b'secret')
        # the target is neither read as the credential nor changed
        self.assertEqual(mode(target), 0o644)

    def test_fifo_is_replaced_without_blocking(self):
        os.makedirs(systemd_credential.PLAIN_DIR, 0o700)
        os.mkfifo(self.plain_path)
        self.assertTrue(self.apply(encrypted=False)[0])
        self.assertTrue(stat.S_ISREG(os.lstat(self.plain_path).st_mode))

    def test_symlinked_store_dir_fails(self):
        elsewhere = os.path.join(self.tmp, 'elsewhere')
        os.mkdir(elsewhere, 0o777)
        os.symlink(elsewhere, systemd_credential.PLAIN_DIR)
        with self.assertRaises(systemd_credential.StoreError):
            self.apply(encrypted=False)
        self.assertEqual(os.listdir(elsewhere), [])

    def test_store_dir_is_a_file_fails(self):
        with open(systemd_credential.PLAIN_DIR, 'w') as f:
            f.write('x')
        with self.assertRaises(systemd_credential.StoreError):
            self.apply(encrypted=False)


class TestAbsent(StoreTestCase):
    def test_removes_both(self):
        self.apply()
        os.makedirs(systemd_credential.PLAIN_DIR, 0o700)
        with open(self.plain_path, 'wb') as f:
            f.write(b'secret')
        self.assertEqual(self.apply(state='absent'), (True, ''))
        self.assertFalse(os.path.lexists(self.enc_path))
        self.assertFalse(os.path.lexists(self.plain_path))
        self.assertEqual(self.apply(state='absent'), (False, ''))

    def test_check_mode(self):
        self.apply()
        self.assertTrue(self.apply(state='absent', check_mode=True)[0])
        self.assertTrue(os.path.exists(self.enc_path))


class TestWriteAtomic(StoreTestCase):
    def test_new_file_is_not_world_readable(self):
        # AnsibleModule.atomic_move() would give a new file 0666 minus the umask
        os.mkdir(systemd_credential.PLAIN_DIR, 0o700)
        systemd_credential.write_atomic(self.plain_path, b'secret')
        self.assertEqual(mode(self.plain_path), 0o600)
        self.assertEqual(os.listdir(systemd_credential.PLAIN_DIR), ['cred'])


if __name__ == '__main__':
    unittest.main()
