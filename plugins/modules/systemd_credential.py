#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: systemd_credential

short_description: Manage a systemd credential in the system credential store

description:
    - Stores a secret as a systemd credential, so that a service can load it with C(LoadCredentialEncrypted=) or C(LoadCredential=) and read it from C($CREDENTIALS_DIRECTORY/<name>).
    - With systemd 251 or newer, the secret is encrypted with C(systemd-creds encrypt) and stored in C(/etc/credstore.encrypted/<name>), where C(LoadCredentialEncrypted=<name>) finds it without a path.
    - With an older systemd (for example RHEL 8 or Ubuntu 22.04), the secret is stored in plain text in C(/etc/credstore/<name>), readable by root only. A consumer that reads C(${CREDENTIALS_DIRECTORY:-/etc/credstore}/<name>) works with both.
    - "Idempotent: an encrypted credential is decrypted on the host and compared with I(content). It is only encrypted again if the content differs or the file cannot be decrypted, for example after the host key was lost. C(systemd-creds encrypt) produces a different file on every call, so comparing files would always report a change."
    - The secret is passed to C(systemd-creds) on stdin, never on the command line, and the module never returns it.
    - Switching between the two stores, for example after an upgrade from RHEL 8 to RHEL 9, removes the credential from the store that is no longer used.
    - The store directory is kept at mode C(0700) and the credential at C(0600), both owned by root. A symlink in place of the store directory makes the module fail, a symlink or other non-regular file in place of the credential is replaced. Files are written to a temporary file in the store, synced and renamed, so a service never loads a half-written credential.

notes:
    - A service reads its credentials only when it starts. Restart it when the module reports a change.
    - The encrypted credential is bound to the host key C(/var/lib/systemd/credential.secret) and, if the host has one, to its TPM2 chip. On a host without a TPM2 chip, a full copy of the disk is enough to decrypt it.
    - With a TPM2 chip, C(systemd-creds) also binds the credential to the Secure Boot state (PCR 7). After a firmware, shim or Secure Boot update, the service cannot decrypt it and fails to start until the module runs again and re-encrypts it.
    - Check mode is supported. Diff mode is not, since a diff would reveal the secret.
    - Has to run as root.
    - The version of the running service manager decides between the two stores, since it is the one that loads the credential.

requirements:
    - systemd. C(systemd-creds) for the encrypted store.

author:
    - Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch

version_added: "10.0.0"

options:
    content:
        description: The secret. Stored byte for byte as given, without adding a trailing newline. Required and must not be empty with I(state=present).
        required: False
        type: str
    name:
        description: Name of the credential, also used as the file name in the credential store and embedded in the encrypted file. Letters, digits, C(_), C(-) and C(.) only.
        required: True
        type: str
    state:
        description: Whether the credential should exist. C(absent) removes it from both stores.
        required: False
        type: str
        default: 'present'
        choices:
            - 'absent'
            - 'present'
"""

EXAMPLES = r"""
- name: 'Store the dump login as a systemd credential'
  linuxfabrik.lfops.systemd_credential:
    name: 'mariadb-dump-login.cnf'
    content: |
      [client]
      user = "mariadb-dump"
      password = "linuxfabrik"
  register: 'dump_login_credential_result'

# The unit loads the credential from the store the module chose. The template contains:
# {% if dump_login_credential_result['encrypted'] %}
# LoadCredentialEncrypted=mariadb-dump-login.cnf
# {% endif %}
# and the script reads ${CREDENTIALS_DIRECTORY:-/etc/credstore}/mariadb-dump-login.cnf
- name: 'Deploy /etc/systemd/system/mariadb-dump.service'
  ansible.builtin.template:
    src: 'etc/systemd/system/mariadb-dump.service.j2'
    dest: '/etc/systemd/system/mariadb-dump.service'
    owner: 'root'
    group: 'root'
    mode: 0o644

- name: 'Remove the credential'
  linuxfabrik.lfops.systemd_credential:
    name: 'mariadb-dump-login.cnf'
    state: 'absent'
"""

RETURN = r"""
encrypted:
    description: Whether the credential is stored encrypted (systemd 251 or newer). Use it to decide between C(LoadCredentialEncrypted=) and the plain fallback.
    returned: always
    type: bool
    sample: true
path:
    description: Path of the credential in the credential store. Empty with I(state=absent).
    returned: always
    type: str
    sample: '/etc/credstore.encrypted/mariadb-dump-login.cnf'
systemd_version:
    description: Major version of the running systemd service manager.
    returned: always
    type: int
    sample: 252
"""

import os
import re
import stat
import tempfile

from ansible.module_utils.basic import AnsibleModule

# systemd 251 is the first release in which LoadCredentialEncrypted= looks up a credential in
# /etc/credstore.encrypted/ without a path (NEWS, "CHANGES WITH 251"). systemd-creds itself
# exists since 250.
MIN_ENCRYPTED_VERSION = 251

# The directories systemd searches for system credentials, created by systemd itself with
# mode 0700 root:root since 253 (tmpfiles.d/credstore.conf).
ENCRYPTED_DIR = '/etc/credstore.encrypted'
PLAIN_DIR = '/etc/credstore'

# Owner of the store and its files. Module constants, so that the unit tests can run them
# without root.
OWNER_UID = 0
OWNER_GID = 0

# Keeps the name a plain file name inside the store: no `/`, no `..`, no leading dot, no control
# characters (systemd rejects those as credential names).
NAME_REGEX = re.compile(r'[A-Za-z0-9_-][A-Za-z0-9_.-]*')


class StoreError(Exception):
    """The credential store is in a state the module refuses to work with."""


def is_valid_name(name):
    """Return True if `name` is a safe credential (file) name."""
    return bool(NAME_REGEX.fullmatch(name)) and len(name) <= 255


def parse_systemd_version(output):
    """Return the major version from `systemctl show --property=Version --value` (`252-51.el9`,
    `257.13-1~deb13u1`) or from the first line of `systemctl --version`
    (`systemd 252 (252-51.el9)`), or None if it cannot be parsed.
    """
    match = re.match(r'^(?:systemd )?(\d+)', output.strip())
    return int(match.group(1)) if match else None


def ensure_store_dir(path, check_mode):
    """Make `path` a directory owned by root with mode 0700. Refuses a symlink or anything else
    that is not a directory, since following it would put the secret somewhere else. Returns
    True if something changed.
    """
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        if not check_mode:
            os.mkdir(path, 0o700)
            os.chown(path, OWNER_UID, OWNER_GID)
            os.chmod(path, 0o700)
        return True
    if not stat.S_ISDIR(st.st_mode):
        raise StoreError(
            f'{path} is not a directory (or a symlink). Remove it and run again.'
        )
    changed = False
    if (st.st_uid, st.st_gid) != (OWNER_UID, OWNER_GID):
        changed = True
        if not check_mode:
            os.chown(path, OWNER_UID, OWNER_GID)
    if stat.S_IMODE(st.st_mode) != 0o700:
        changed = True
        if not check_mode:
            os.chmod(path, 0o700)
    return changed


def is_regular_file(path):
    """Return True if `path` is a regular file, not following a symlink."""
    try:
        return stat.S_ISREG(os.lstat(path).st_mode)
    except FileNotFoundError:
        return False


def ensure_file_attributes(path, check_mode):
    """Make the regular file `path` owned by root with mode 0600. Returns True if something
    changed.
    """
    st = os.lstat(path)
    changed = False
    if (st.st_uid, st.st_gid) != (OWNER_UID, OWNER_GID):
        changed = True
        if not check_mode:
            os.chown(path, OWNER_UID, OWNER_GID)
    if stat.S_IMODE(st.st_mode) != 0o600:
        changed = True
        if not check_mode:
            os.chmod(path, 0o600)
    return changed


def read_plain(path):
    """Return the content of the regular file `path` as bytes, or None if it is missing or not
    a regular file (a symlink, a FIFO, ...), so that it gets replaced.
    """
    if not is_regular_file(path):
        return None
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, 'rb') as f:
        return f.read()


def fsync_dir(path):
    """Persist a rename in the directory `path`."""
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_atomic(dest, data):
    """Write `data` (bytes) to `dest`, owned by root with mode 0600, via a temporary file in the
    same directory and an atomic rename, which also replaces a symlink at `dest` instead of
    following it. os.rename() instead of AnsibleModule.atomic_move(), which gives a new file the
    mode 0666 minus the umask, so mostly world-readable. Synced before and after the rename, so
    that a crash does not leave an empty credential behind.
    """
    directory = os.path.dirname(dest)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix='.ansible-')
    try:
        with os.fdopen(fd, 'wb') as f:
            os.fchown(f.fileno(), OWNER_UID, OWNER_GID)
            os.fchmod(f.fileno(), 0o600)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.rename(tmp, dest)
        fsync_dir(directory)
    finally:
        if os.path.lexists(tmp):
            os.unlink(tmp)


def remove(path, check_mode):
    """Remove the file `path` if it exists. Returns True if it existed."""
    if not os.path.lexists(path):
        return False
    if not check_mode:
        os.unlink(path)
    return True


def decrypts_to(module, creds_bin, name, path, data):
    """Return True if the encrypted credential at `path` decrypts to `data`. A file that cannot
    be decrypted (wrong host key, other name, corrupt) or is not a regular file counts as
    different, so that it gets replaced. The decrypted secret never leaves this function.
    """
    if not is_regular_file(path):
        return False
    rc, stdout, _ = module.run_command(
        [creds_bin, 'decrypt', f'--name={name}', path, '-'],
        binary_data=True,
        encoding=None,
    )
    return rc == 0 and stdout == data


def encrypt(module, creds_bin, name, data):
    """Return `data` (bytes, passed on stdin) encrypted by systemd-creds. The ciphertext comes
    back on stdout, so that write_atomic() writes it with the right owner and mode, instead of
    systemd-creds' own temporary file with mode 0666 minus the umask.
    """
    rc, stdout, stderr = module.run_command(
        [creds_bin, 'encrypt', f'--name={name}', '-', '-'],
        data=data,
        binary_data=True,
        encoding=None,
    )
    if rc != 0 or not stdout:
        module.fail_json(
            msg='systemd-creds encrypt failed: '
            + stderr.decode('utf-8', errors='replace').strip(),
        )
    return stdout


def get_systemd_version(module):
    """Return the major version of the running service manager, which decides how
    LoadCredentialEncrypted= behaves. `systemctl --version` would report the installed client,
    which differs after an upgrade without a reboot. Falls back to it where systemd is not
    PID 1 (e.g. in a container).
    """
    rc, stdout, _ = module.run_command(
        ['systemctl', 'show', '--property=Version', '--value']
    )
    version = parse_systemd_version(stdout) if rc == 0 else None
    if version is None:
        rc, stdout, _ = module.run_command(['systemctl', '--version'])
        version = parse_systemd_version(stdout) if rc == 0 else None
    return version


def apply(module, name, data, state, encrypted, creds_bin, check_mode):
    """Bring the credential `name` into the desired state. Returns (changed, path)."""
    encrypted_path = os.path.join(ENCRYPTED_DIR, name)
    plain_path = os.path.join(PLAIN_DIR, name)

    if state == 'absent':
        changed = remove(encrypted_path, check_mode)
        changed |= remove(plain_path, check_mode)
        return changed, ''

    if encrypted:
        path, other_path = encrypted_path, plain_path
        changed = ensure_store_dir(ENCRYPTED_DIR, check_mode)
        is_current = decrypts_to(module, creds_bin, name, encrypted_path, data)
    else:
        path, other_path = plain_path, encrypted_path
        changed = ensure_store_dir(PLAIN_DIR, check_mode)
        is_current = read_plain(plain_path) == data

    if not is_current:
        changed = True
        if not check_mode:
            content = encrypt(module, creds_bin, name, data) if encrypted else data
            write_atomic(path, content)
    else:
        changed |= ensure_file_attributes(path, check_mode)

    # Since systemd 252, LoadCredential= and LoadCredentialEncrypted= search the encrypted store
    # first, so a stale copy in the other store has to go: a plain one would leave the secret in
    # plain text (e.g. after an upgrade from RHEL 8), an encrypted one would be loaded instead.
    changed |= remove(other_path, check_mode)
    return changed, path


def main():
    module = AnsibleModule(
        argument_spec=dict(
            content=dict(type='str', no_log=True),
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['absent', 'present']),
        ),
        required_if=[('state', 'present', ['content'])],
        supports_check_mode=True,
    )
    name = module.params['name']
    state = module.params['state']

    if os.geteuid() != 0:
        module.fail_json(msg='The module has to run as root (become: true).')
    if not is_valid_name(name):
        module.fail_json(
            msg=f'Invalid credential name {name!r}: use letters, digits, "_", "-" and "." only,'
            ' not starting with a dot.',
        )
    if state == 'present' and not module.params['content']:
        module.fail_json(msg='content must not be empty.')

    systemd_version = get_systemd_version(module)
    if systemd_version is None:
        module.fail_json(msg='Cannot determine the systemd version.')

    creds_bin = module.get_bin_path('systemd-creds')
    encrypted = systemd_version >= MIN_ENCRYPTED_VERSION and creds_bin is not None
    data = module.params['content'].encode('utf-8') if state == 'present' else b''

    try:
        changed, path = apply(
            module, name, data, state, encrypted, creds_bin, module.check_mode
        )
    except StoreError as e:
        module.fail_json(msg=str(e))

    module.exit_json(
        changed=changed, encrypted=encrypted, path=path, systemd_version=systemd_version
    )


if __name__ == '__main__':
    main()
