#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import collections

from ansible.errors import AnsibleFilterError

DOCUMENTATION = r'''
  name: combine_lod
  version_added: "3.0.0"
  short_description: Merge lists of dictionaries by a unique key
  description:
    - Merges one or more lists of dictionaries into a single list. Dictionaries that share the same value under I(unique_key) are folded into one entry; later entries overwrite earlier ones (non-recursive, like Python C(dict.update)).
    - The folding also collapses duplicates inside a single input list, so passing one list with duplicates is a valid way to deduplicate it.
    - Useful for layering inventory. A role can ship sensible defaults, and the user can selectively override individual keys per item from their inventory without having to redeclare the whole list.
    - Sub-dictionaries and sub-lists are replaced wholesale, not merged recursively. To merge nested structures, build the nested values up using this filter at each level.
    - The result keeps the order in which each unique key is first seen across all input lists; later updates to an existing key do not move it.
    - Every list item must be a dictionary; a non-dictionary item raises an error.
    - Every input dictionary must contain the unique key (or all of them, when a list of keys is passed). Each key is the item's identity and must be set explicitly; it may not rely on a default applied elsewhere.
    - Only an absent key raises an error. A key that is present with a falsy value (C(0), empty string, C(False)) is kept as a distinct identity, so e.g. a port of C(0) is valid. This applies to a single key and to every component of a key list alike.
  positional: _input, _dicts
  options:
    _input:
      description: First list of dictionaries to combine.
      type: list
      elements: dictionary
      required: true
    _dicts:
      description: Zero or more additional lists of dictionaries to combine. Items are folded in the order the lists are passed; the last occurrence of a unique key wins.
      type: list
      elements: dictionary
      required: false
    unique_key:
      description:
        - Dictionary key (or list of keys, for composite keys) used to decide which entries belong together.
        - Pass a list when no single key is unique on its own (e.g. C(["server_name", "server_port"]) for vHosts where the same hostname can appear on multiple ports).
      type: raw
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
        allow_all: false
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

# => (keys keep their first-seen order)
# - name: setting 1
#   first_value: better setting for me
#   second_value: sensible default for second value
# - name: setting 2
#   allow_all: false
#   allowed_users:
#   - linuxfabrik


# composite unique_key: the same server_name on different ports stays separate
- name: 'merge vhosts by name + port'
  debug:
    msg: >-
      {{ [{'server_name': 'example.com', 'server_port': 80, 'root': '/var/www'},
          {'server_name': 'example.com', 'server_port': 443, 'root': '/var/www'}]
         | linuxfabrik.lfops.combine_lod([{'server_name': 'example.com', 'server_port': 443, 'root': '/srv/tls'}],
                                         unique_key=['server_name', 'server_port']) }}

# =>
# - server_name: example.com
#   server_port: 80
#   root: /var/www
# - server_name: example.com
#   server_port: 443
#   root: /srv/tls


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
                raise AnsibleFilterError('found a non-dictionary item in the list, this is not supported')

            # A unique_key is the item's identity, so every key must be set
            # explicitly and may not be left to a default applied elsewhere:
            # otherwise one item omitting it and another stating that same
            # default would resolve to the same identity yet not merge.
            # Presence is checked, not truthiness, so a legitimately falsy
            # identity value (e.g. `port: 0` for a unix socket) is still
            # accepted. Single and composite keys behave the same way.
            if isinstance(unique_key, collections.abc.MutableSequence):
                missing = [k for k in unique_key if k not in item]
                if missing:
                    # Show the unique-key components the item does set, so the
                    # offending item can be located in a long inventory. These
                    # are identifiers, never secrets (a password is never a
                    # unique_key). Fall back to the item's field names if none
                    # of the components are set.
                    set_keys = {k: item[k] for k in unique_key if k in item}
                    raise AnsibleFilterError(
                        f'found a dictionary missing the unique key(s) {missing} '
                        f'(required by unique_key={list(unique_key)}); '
                        f'the item sets {set_keys or sorted(item.keys())}'
                    )
                key = tuple(item[k] for k in unique_key)
            else:
                if unique_key not in item:
                    raise AnsibleFilterError(
                        f"found a dictionary missing the unique key '{unique_key}'; "
                        f'the item sets the keys {sorted(item.keys())}'
                    )
                key = item[unique_key]

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
