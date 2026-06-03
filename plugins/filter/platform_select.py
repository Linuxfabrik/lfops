#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.errors import AnsibleFilterError

DOCUMENTATION = r'''
  name: platform_select
  version_added: "6.0.2"
  short_description: Pick the value matching the target host from a platform-keyed dictionary
  description:
    - Picks a value from a dictionary whose keys are platform identifiers, returning the entry that matches the target host most specifically.
    - The selection precedence mirrors C(roles/shared/tasks/platform-variables.yml). From least to most specific the order is C(os_family), C(os_family + distribution_major_version), C(os_family + distribution_version), C(distribution), C(distribution + distribution_major_version), C(distribution + distribution_version). The most specific present key wins, even when less specific keys are also present.
    - Intended for the C(__dependent_var) pattern, where a role publishes a value that an earlier role in the same play consumes. C(vars/<os>.yml) cannot serve this case because those files are loaded only when the publishing role's tasks run, which is too late. Defining the value as a platform-keyed dict in the publishing role's C(vars/main.yml) and selecting through this filter resolves the timing problem without losing the C(vars/) precedence.
  positional: _input, ansible_facts
  options:
    _input:
      description: Platform-keyed dictionary. Keys are platform identifiers (e.g. C(RedHat), C(RedHat8), C(Rocky8.10), C(Debian), C(Suse)).
      type: dict
      required: true
    ansible_facts:
      description: The host's C(ansible_facts) dictionary. The filter reads C(os_family), C(distribution), C(distribution_major_version), and C(distribution_version) from it; missing fact keys are tolerated and skip the affected precedence steps.
      type: dict
      required: true
    default:
      description: Value to return when no key in I(_input) matches the target host. If omitted, an unmatched call raises C(AnsibleFilterError).
      type: raw
      required: false
'''

EXAMPLES = r'''
# in a role's vars/main.yml (auto-loaded at play parse, so visible to roles
# that run earlier in the same play via the `__dependent_var` pattern):
mariadb_server__python__modules__dependent_var:
  Debian:
    - name: 'python3-pymysql'
  RedHat:
    - name: 'python3-PyMySQL'

# in any playbook that feeds this value into an earlier role:
- name: 'Install python modules and the database'
  hosts: 'all'
  roles:
    - role: 'linuxfabrik.lfops.python'
      python__modules__dependent_var: '{{
          mariadb_server__python__modules__dependent_var
          | linuxfabrik.lfops.platform_select(ansible_facts)
        }}'

    - role: 'linuxfabrik.lfops.mariadb_server'


# combining selections from multiple roles, with a safe default for hosts
# whose platform is not in the dict:
- role: 'linuxfabrik.lfops.python'
  python__modules__dependent_var: '{{
      (mariadb_server__python__modules__dependent_var
        | linuxfabrik.lfops.platform_select(ansible_facts, default=[]))
      + (apache_httpd__python__modules__dependent_var
        | linuxfabrik.lfops.platform_select(ansible_facts, default=[]))
    }}'
'''

RETURN = r'''
  _value:
    description: The value associated with the most specific matching key in I(_input), or the supplied I(default) if no key matches.
    type: raw
'''


_SENTINEL = object()


def platform_select(values, ansible_facts, default=_SENTINEL):
    """Return the value of the most specific platform key that matches ansible_facts.

    Precedence mirrors `roles/shared/tasks/platform-variables.yml`. See module
    DOCUMENTATION for details.
    """
    if not isinstance(values, dict):
        raise AnsibleFilterError(
            "platform_select: input must be a dict keyed by platform identifier, "
            f"got {type(values).__name__}"
        )
    if not isinstance(ansible_facts, dict):
        raise AnsibleFilterError(
            "platform_select: ansible_facts must be a dict, "
            f"got {type(ansible_facts).__name__}"
        )

    os_family = ansible_facts.get('os_family')
    distribution = ansible_facts.get('distribution')
    major = ansible_facts.get('distribution_major_version')
    version = ansible_facts.get('distribution_version')

    # Most-specific first. This is the reverse of the loop in
    # `shared/tasks/platform-variables.yml`, where include_vars is run from
    # least to most specific and the later (more specific) call wins.
    candidates = [
        f'{distribution}{version}' if distribution and version else None,
        f'{distribution}{major}'   if distribution and major   else None,
        distribution,
        f'{os_family}{version}'    if os_family    and version else None,
        f'{os_family}{major}'      if os_family    and major   else None,
        os_family,
    ]
    for key in candidates:
        if key and key in values:
            return values[key]

    if default is not _SENTINEL:
        return default
    raise AnsibleFilterError(
        f"platform_select: no key in the input dict matched the target host "
        f"(os_family={os_family!r}, distribution={distribution!r}, "
        f"distribution_major_version={major!r}, distribution_version={version!r}); "
        f"input keys: {sorted(values)}"
    )


class FilterModule(object):
    """Register custom filter plugins in Ansible"""

    def filters(self):
        return {
            'platform_select': platform_select,
        }
