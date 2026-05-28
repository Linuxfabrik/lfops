#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

"""Unit tests for the `combine_lod` filter plugin.

`combine_lod` is a filter plugin and therefore runs on the Ansible
controller only. The controller requires Python >= 3.10 (ansible-core
2.16/2.17) or >= 3.11 (2.18), so this test runs on the controller
matrix, not on the Python 3.6 (RHEL 8) managed-node tier. See
`tests/README.md`.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import importlib.util
import os
import textwrap
import unittest

import yaml

from ansible.errors import AnsibleFilterError

# The plugin lives outside any importable package, so load it by path
# (repo_root/plugins/filter/combine_lod.py) relative to this test file.
_PLUGIN_PATH = os.path.join(
    os.path.dirname(__file__),
    '..', '..', '..', '..',
    'plugins', 'filter', 'combine_lod.py',
)
_spec = importlib.util.spec_from_file_location('combine_lod', _PLUGIN_PATH)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
combine_lod = _module.combine_lod


class Test(unittest.TestCase):

    def test_combine_lod_non_dict_item(self):
        """non-dictionary list elements are not supported"""

        input1 = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          value: 'test1'
        - 'im a string'
        '''))

        with self.assertRaises(AnsibleFilterError):
            combine_lod(input1)

    def test_combine_lod_last(self):
        """the last element should always win and overwrite the earlier ones"""

        input1 = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          value: 'test1'
        '''))

        input2 = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          value: 'test2'
        '''))

        expected = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          value: 'test2'
        '''))

        result = combine_lod(input1, input2)
        self.assertEqual(result, expected)

    def test_combine_lod_multiple(self):
        """test the basic functionality if there are multiple list elements"""

        input1 = yaml.safe_load(textwrap.dedent('''
        - name: 'first variable'
          value: 'test1'
        - name: 'second variable'
          value: 'test2'
        - name: 'other_var'
          value: 'linuxfabrik'
        '''))

        input2 = yaml.safe_load(textwrap.dedent('''
        - name: 'first variable'
          value: 'test1 - edited'
        - name: 'second variable'
          value: 'test2 - edited'
          new_value: 'new here'
        '''))

        expected = yaml.safe_load(textwrap.dedent('''
        - name: 'first variable'
          value: 'test1 - edited'
        - name: 'second variable'
          value: 'test2 - edited'
          new_value: 'new here'
        - name: 'other_var'
          value: 'linuxfabrik'
        '''))

        result = combine_lod(input1, input2)
        self.assertEqual(result, expected)

    def test_combine_lod_single_input(self):
        """test if everything works if the lists are already combined beforehand"""

        input1 = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          value: 'test1'
        - name: 'myvar'
          value: 'test2'
        '''))

        expected = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          value: 'test2'
        '''))

        result = combine_lod(input1)
        self.assertEqual(result, expected)

    def test_combine_lod_replace_given_keys(self):
        """only the given keys are overwritten, not the whole list element"""

        input1 = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          value: 'value 1'
          my_list:
            - 'input1'
            - 'lots of default entries'
        '''))

        input2 = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          value: 'value 2'
        '''))

        expected = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          value: 'value 2'
          my_list:
            - 'input1'
            - 'lots of default entries'
        '''))

        result = combine_lod(input1, input2)
        self.assertEqual(result, expected)

    def test_combine_lod_different_single_unique_key(self):
        """test if using a different single unique_key works"""

        input1 = yaml.safe_load(textwrap.dedent('''
        - filename: 'myvar 1'
          value: 'value 1'
        - filename: 'myvar 2'
          value: 'value 1'
        '''))

        input2 = yaml.safe_load(textwrap.dedent('''
        - filename: 'myvar 1'
          value: 'value 1 - edited'
        '''))

        expected = yaml.safe_load(textwrap.dedent('''
        - filename: 'myvar 1'
          value: 'value 1 - edited'
        - filename: 'myvar 2'
          value: 'value 1'
        '''))

        result = combine_lod(input1, input2, unique_key="filename")
        self.assertEqual(result, expected)

    def test_combine_lod_different_list_unique_key(self):
        """test if using a list of unique_keys works"""

        input1 = yaml.safe_load(textwrap.dedent('''
        - server_name: 'myvar'
          server_port: 80
          value: 'value 80'
        - server_name: 'myvar'
          server_port: 443
          value: 'value 443'
        '''))

        input2 = yaml.safe_load(textwrap.dedent('''
        - server_name: 'myvar'
          server_port: 80
          value: 'value 81'
        '''))

        expected = yaml.safe_load(textwrap.dedent('''
        - server_name: 'myvar'
          server_port: 80
          value: 'value 81'
        - server_name: 'myvar'
          server_port: 443
          value: 'value 443'
        '''))

        result = combine_lod(input1, input2, unique_key=["server_name", "server_port"])
        self.assertEqual(result, expected)

    def test_combine_lod_missing_unique_key(self):
        """the plugin should throw an error if it cannot find the unique_key for all list elements"""

        input1 = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          value: 'value 1'
        '''))

        input2 = yaml.safe_load(textwrap.dedent('''
        - wrong_name: 'myvar'
          value: 'value 1'
        '''))

        with self.assertRaises(AnsibleFilterError):
            combine_lod(input1, input2)

    def test_combine_lod_composite_key_missing_component(self):
        """a composite key with a missing component must raise, not silently group under None"""

        input1 = yaml.safe_load(textwrap.dedent('''
        - server_name: 'myvar'
          server_port: 80
          value: 'value 80'
        - server_name: 'myvar'
          value: 'no port here'
        '''))

        with self.assertRaises(AnsibleFilterError):
            combine_lod(input1, unique_key=["server_name", "server_port"])

    def test_combine_lod_composite_key_all_components_missing(self):
        """a composite key where every component is missing must raise as well"""

        input1 = yaml.safe_load(textwrap.dedent('''
        - value: 'no keys at all'
        '''))

        with self.assertRaises(AnsibleFilterError):
            combine_lod(input1, unique_key=["server_name", "server_port"])

    def test_combine_lod_list_merge(self):
        """a key holding a list should be replaced wholesale, no append / prepend"""

        input1 = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          my_list:
            - 'input1'
            - 'input_repeated'
        '''))

        input2 = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          my_list:
            - 'input2'
            - 'input_repeated'
        '''))

        expected = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          my_list:
            - 'input2'
            - 'input_repeated'
        '''))

        result = combine_lod(input1, input2)
        self.assertEqual(result, expected)

    def test_combine_lod_no_recursion(self):
        """the plugin should not recurse into dicts or lists"""

        input1 = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          value: 'value 1'
          my_list:
            - 'input1'
            - name: 'my sub var'
              value: 'sub value 1'
            - 'input_repeated'
        '''))

        input2 = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          value: 'value 2'
          my_dict:
            name: 'my sub var'
            value: 'sub value 1'
        '''))

        expected = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          value: 'value 2'
          my_list:
            - 'input1'
            - name: 'my sub var'
              value: 'sub value 1'
            - 'input_repeated'
          my_dict:
            name: 'my sub var'
            value: 'sub value 1'
        '''))

        result = combine_lod(input1, input2)
        self.assertEqual(result, expected)

    def test_combine_lod_no_modification(self):
        """in this case the plugin should not modify anything"""

        input1 = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          value: 'value 1'
        '''))

        input2 = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          value: 'value 1'
        '''))

        expected = yaml.safe_load(textwrap.dedent('''
        - name: 'myvar'
          value: 'value 1'
        '''))

        result = combine_lod(input1, input2)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
