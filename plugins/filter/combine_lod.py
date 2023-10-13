# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function
__metaclass__ = type

import collections

from ansible.errors import AnsibleFilterError

DOCUMENTATION = r'''
  name: combine_lod
  version_added: "2.0.1"
  short_description: combine a list of dictionaries
  description:
    - Create list a dictionaries (hashes/associative arrays) as a result of merging existing lists of dictionaries.
    - This is very useful if you want to set sensible defaults in a role, while still allowing the user to selectively overwrite specific parts of the defaults in their inventory.
  positional: _input, _dicts, unique_key
  options:
    _input:
      description: First list of dictionaries to combine.
      type: list
      elements: dictionary
      required: true
    _dicts:
      description: The other lists of dictionaries to combine.
      type: list
      elements: dictionary
      required: true
    unique_key:
      description:
        The dictionary key to be used as an indicator to merge the related dictionaries together.
        The key has to be unique.
        It is possible to pass a list of keys in case a single key would not be unique.
      type: str or list
      elements: str
      default: name
'''

EXAMPLES = r'''
# create two lists of dictionaries
- set_fact:
    # this list could be in the role defaults
    role_defaults:
      - name: 'setting 1'
        first_value: 'sensible default for first value'
        second_value: 'sensible default for second value'
      - name: 'setting 2'
        allow_all: False
        allowed_users:
          - 'root'

    # this list could be in the users inventory
    my_user_adjustments:
      - name: 'setting 1'
        first_value: 'better setting for me'
      - name: 'setting 2'
        # only allow linuxfabrik, nobody else
        allowed_users:
          - 'linuxfabrik'

- name: 'combine for the actual use in the role'
  debug:
    msg: '{{ role_defaults | linuxfabrik.lfops.combine_lod(my_user_adjustments) }}'

# =>
# (reordered for readability)
# - name: setting 1
#   first_value: better setting for me
#   second_value: sensible default for second value
# - name: setting 2
#   allow_all: false
#   allowed_users:
#   - linuxfabrik


# more complicated example
# defaults:
mariadb_server__kernel_settings__sysctl__dependent_var:
  - name: 'fs.aio-max-nr'
    value: 1048576
  - name: 'sunrpc.tcp_slot_table_entries'
    value: 128
  - name: 'vm.swappiness'
    value: 10

redis__kernel_settings__sysctl__dependent_var:
  - name: 'vm.overcommit_memory'
    value: 1
  - name: 'net.core.somaxconn'
    value: 1024

kernel_settings__sysctl__dependent_var: '{{
    mariadb_server__kernel_settings__sysctl__dependent_var | d([]) +
    redis__kernel_settings__sysctl__dependent_var | d([])
  }}'

kernel_settings__sysctl__host_var:
  - name: 'net.core.somaxconn'
    value: 2048

kernel_settings__sysctl__group_var: []
kernel_settings__sysctl__role_var: []
kernel_settings__sysctl__combined_var: '{{ (
  kernel_settings__sysctl__role_var +
  kernel_settings__sysctl__dependent_var +
  kernel_settings__sysctl__group_var +
  kernel_settings__sysctl__host_var
  ) | linuxfabrik.lfops.combine_lod
 }}'

# tasks:
  - name: 'display combined var'
    debug:
      msg: '{{ kernel_settings__sysctl__combined_var }}'

# =>
# - name: fs.aio-max-nr
#   value: 1048576
# - name: sunrpc.tcp_slot_table_entries
#   value: 128
# - name: vm.swappiness
#   value: 10
# - name: vm.overcommit_memory
#   value: 1
# - name: net.core.somaxconn
#   value: 2048
'''

RETURN = r'''
  _value:
    description: Resulting merged list of dictionaries.
    type: list
    elements: dictionary
'''


def combine_lod(*args, **kwargs):
    """Combines a list of dictionaries based on an unique_key.

    Optional arguments:
        unique_key
            string or list. The dictionary key to be used as an indicator to
            merge the related dictionaries together.
            The key has to be unique.
            It is possible to pass a list of keys in case a single key would not be unique.
            Defaults to `name`.
    """
    unique_key = kwargs.pop('unique_key', 'name')
    if kwargs:
        raise AnsibleFilterError("'unique_key' is the only valid keyword argument")

    result = collections.defaultdict(dict)

    # we iterate the args as it is possible to pass multiple lists.
    # lod = list of dictionaries
    for lod in list(args):
        for item in lod:
            if not isinstance(item, collections.abc.MutableMapping):
                raise AnsibleFilterError("found non-dictionary item in the list, this is not supported")

            if isinstance(unique_key, collections.abc.MutableSequence):
                key = tuple(item.get(k, None) for k in unique_key)
            else:
                key = item.get(unique_key, None)

            if not key:
                raise AnsibleFilterError("found an dictionary without the unique key, this is not supported")

            # the python dict.update function does exactly what we want.
            # it is also used for ansible.builtin.combine(..., recurse=False, list_merge='replace').
            result[key].update(item)

    return list(result.values())



class FilterModule(object):
    """Register custom filter plugins in Ansible"""

    def filters(self):
        return {
            'combine_lod': combine_lod,
        }



if __name__ == '__main__':
    import textwrap
    import unittest

    import yaml

    class Test(unittest.TestCase):

        def test_combine_lod_non_dict_item(self):
            '''
            non-dictionaries list elements are not supported
            '''

            input1 = yaml.safe_load(textwrap.dedent('''
            - name: 'myvar'
              value: 'test1'
            - 'im a string'
            '''))

            with self.assertRaises(AnsibleFilterError):
                combine_lod(input1)


        def test_combine_lod_last(self):
            '''
            the last element should always win and overwrite the earlier ones
            '''

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

            # print('input1:')
            # print(yaml.dump(input1, default_flow_style=False))
            # print('input2:')
            # print(yaml.dump(input2, default_flow_style=False))
            # print('result:')
            # print(yaml.dump(result, default_flow_style=False))
            # print('expected:')
            # print(yaml.dump(expected, default_flow_style=False))

            self.assertEqual(result, expected)


        def test_combine_lod_multiple(self):
            '''
            test the basic functionality if there are multiple list elements
            '''

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
              value: 'test1'
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
            '''
            test if everything works if the lists are already combined beforehand
            '''

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
            '''
            only the given keys are overwritten, not the whole list element
            '''

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
            '''
            test if using a different single unique_key works
            '''

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
            '''
            test if using a a list of unique_keys works
            '''

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
            '''
            the plugin should throw an error if it cannot find the unique_key for all list elements
            '''

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


        def test_combine_lod_list_merge(self):
            '''
            if one of the keys in the dictionaries contains a list,
            the list should just replace the previous lists.
            no append / prepend of the list elements
            '''

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
            '''
            the plugin should not recurse into dicts or lists
            '''

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
            '''
            in this case the plugin should not modify anything
            '''

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


    unittest.main()
