#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-
#
# Author:  Linuxfabrik GmbH, Zurich, Switzerland
# Contact: info (at) linuxfabrik (dot) ch
#          https://www.linuxfabrik.ch/
# License: The Unlicense, see LICENSE file.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: uptimerobot_psp_info
short_description: List UptimeRobot Public Status Pages
version_added: '6.0.2'
description:
    - Calls C(getPSPs) on the UptimeRobot v2 API and returns every public status page on the account.
    - Enum-coded fields are translated to human-readable labels - C(sort) becomes C(a-z)/C(z-a)/C(up-down-paused)/C(down-up-paused), C(status) becomes C(paused)/C(active). The API field C(custom_url) is also exposed under the write-side name C(custom_domain) so it can be diffed against I(custom_domain) on the write module.
    - Read-only; the module always reports C(changed=false) and is safe to run in check mode.
author:
    - Linuxfabrik GmbH, Zurich, Switzerland (info (at) linuxfabrik (dot) ch)
options:
    api_key:
        description: UptimeRobot API key. See C(uptimerobot_monitor) for the resolution order.
        type: str
        no_log: true
    api_key_file:
        description: Path to a file whose first line is the UptimeRobot API key. Tilde-expanded.
        type: str
        default: '~/.uptimerobot'
    friendly_name:
        description:
            - Filter the returned list to the PSP whose C(friendly_name) is an exact match for this value. The result is still a list (length 0 or 1) for shape stability.
        type: str
'''


EXAMPLES = r'''
# 1) List every public status page on the account.
- name: 'Capture all public status pages'
  linuxfabrik.lfops.uptimerobot_psp_info:
  register: 'ur_psps'

- ansible.builtin.debug:
    msg: '{{ ur_psps.psps | length }} public status pages on the account'

# 2) Look up a single PSP by friendly_name.
- linuxfabrik.lfops.uptimerobot_psp_info:
    friendly_name: 'Status - example.com'
  register: 'ur_psp'

- ansible.builtin.debug:
    msg: '{{ ur_psp.psps[0].standard_url }} (sort: {{ ur_psp.psps[0].sort }})'

# 3) Reporting: list every paused PSP plus its monitor count.
- linuxfabrik.lfops.uptimerobot_psp_info:
  register: 'ur_all'

- ansible.builtin.debug:
    msg: >-
      Paused PSPs: {{
        ur_all.psps
        | selectattr("status", "equalto", "paused")
        | map(attribute="friendly_name")
        | list
      }}
'''


RETURN = r'''
psps:
    description: List of PSP dicts. Empty list when nothing matched.
    type: list
    returned: always
    elements: dict
debug:
    description: Diagnostic information about the API call. Stable enough to assert against, not stable enough to be load-bearing.
    type: dict
    returned: always
    sample:
        operation: 'list'
        count: 2
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.linuxfabrik.lfops.plugins.module_utils import uptimerobot as ur


def main():
    argument_spec = dict(
        api_key=dict(type='str', no_log=True),
        api_key_file=dict(type='str', default='~/.uptimerobot'),
        friendly_name=dict(type='str'),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    api_key = ur.resolve_api_key(module, module.params.get('api_key'), module.params.get('api_key_file'))
    friendly_name = module.params.get('friendly_name')

    module.log('uptimerobot_psp_info: fetching public status pages')
    success, psps = ur.get_psps(module, api_key)
    if not success:
        module.fail_json(msg=f'Could not list PSPs: {psps}')

    if friendly_name:
        match = ur.find_by_friendly_name(psps, friendly_name)
        psps = [match] if match else []

    module.exit_json(changed=False, psps=psps, debug={
        'operation': 'list',
        'count': len(psps),
    })


if __name__ == '__main__':
    main()
