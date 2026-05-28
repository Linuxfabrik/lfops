#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Guard against the DOCUMENTATION YAML bug that breaks `ansible-doc`.

In a `description` block (a YAML list), a bullet that contains a colon
followed by a space is parsed as a mapping instead of a string, e.g.

    description:
        - Useful for X: it does Y.    # parsed as {"Useful for X": "it does Y."}

`ansible-doc` then aborts with "expected str instance, AnsibleMapping
found". This test parses every in-house plugin's DOCUMENTATION (and
RETURN) and asserts that every `description` is a string or a list of
strings, catching the bug at unit-test time instead of at render time.

Vendored plugins keep their upstream docs and are out of scope.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import ast
import glob
import os
import unittest

import yaml

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_PLUGIN_GLOBS = [
    'plugins/filter/*.py',
    'plugins/lookup/*.py',
    'plugins/modules/*.py',
]
# Vendored plugins are kept in lockstep with upstream and not restyled here.
_VENDORED_PREFIXES = ('ipa',)
_VENDORED_NAMES = {'lvm_pv.py'}


def _in_house_plugin_files():
    files = []
    for pattern in _PLUGIN_GLOBS:
        for path in glob.glob(os.path.join(_REPO_ROOT, pattern)):
            name = os.path.basename(path)
            if name.startswith(_VENDORED_PREFIXES) or name in _VENDORED_NAMES:
                continue
            files.append(path)
    return sorted(files)


def _extract_doc_constants(source):
    """Return {const_name: yaml_obj} for DOCUMENTATION/RETURN string assignments."""
    tree = ast.parse(source)
    docs = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        for wanted in ('DOCUMENTATION', 'RETURN'):
            if wanted in names and isinstance(node.value, ast.Constant) \
                    and isinstance(node.value.value, str):
                docs[wanted] = yaml.safe_load(node.value.value)
    return docs


def _iter_description_problems(obj, path=''):
    """Yield human-readable paths where a `description` is not str / list[str]."""
    if isinstance(obj, dict):
        # Inside an `options` / `suboptions` collection the dict keys are
        # option names (one of which may legitimately be "description"), not
        # field names. Skip the description field-name check at that level.
        in_options_collection = path.endswith('.options') or path.endswith('.suboptions')
        for key, value in obj.items():
            if key == 'description' and not in_options_collection:
                if isinstance(value, str):
                    pass
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        if not isinstance(item, str):
                            yield f'{path}.description[{i}] is {type(item).__name__}, expected str'
                else:
                    yield f'{path}.description is {type(value).__name__}, expected str or list[str]'
            yield from _iter_description_problems(value, f'{path}.{key}')
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            yield from _iter_description_problems(item, f'{path}[{i}]')


class TestPluginDocs(unittest.TestCase):

    def test_in_house_plugins_have_renderable_descriptions(self):
        files = _in_house_plugin_files()
        self.assertTrue(files, 'no in-house plugin files found')
        for path in files:
            with self.subTest(plugin=os.path.relpath(path, _REPO_ROOT)):
                with open(path, 'r') as f:
                    source = f.read()
                docs = _extract_doc_constants(source)
                problems = []
                for const_name, doc in docs.items():
                    problems += [f'{const_name}{p}' for p in _iter_description_problems(doc)]
                self.assertEqual(
                    problems, [],
                    'description fields must be str or list[str] '
                    '(a colon + space in a bullet makes ansible-doc fail):\n  '
                    + '\n  '.join(problems),
                )


if __name__ == '__main__':
    unittest.main()
