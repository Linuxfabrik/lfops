#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Helpers to unit-test an Ansible module's main() function.

Standard ansible-test pattern: feed arguments via set_module_args(), then
patch AnsibleModule.exit_json / fail_json so they raise instead of calling
sys.exit(), so a test can assert on the outcome. tests/conftest.py puts the
tests/ directory on sys.path so test modules can `import ansible_harness`.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import unittest.mock

from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes


class AnsibleExitJson(Exception):
    """Raised in place of AnsibleModule.exit_json()."""


class AnsibleFailJson(Exception):
    """Raised in place of AnsibleModule.fail_json()."""


def set_module_args(args):
    """Prepare module arguments as if passed in by Ansible."""
    basic._ANSIBLE_ARGS = to_bytes(json.dumps({'ANSIBLE_MODULE_ARGS': args}))
    # ansible-core 2.19+ also requires a serialization profile to decode the args.
    if hasattr(basic, '_ANSIBLE_PROFILE'):
        basic._ANSIBLE_PROFILE = 'legacy'


def _exit_json(self, **kwargs):
    kwargs.setdefault('changed', False)
    raise AnsibleExitJson(kwargs)


def _fail_json(self, **kwargs):
    kwargs.setdefault('failed', True)
    raise AnsibleFailJson(kwargs)


def patch_module():
    """Return a mock.patch.multiple context manager for exit_json / fail_json."""
    return unittest.mock.patch.multiple(
        basic.AnsibleModule,
        exit_json=_exit_json,
        fail_json=_fail_json,
    )
