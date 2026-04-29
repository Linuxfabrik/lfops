#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: uptimerobot_psp_info
short_description: List UptimeRobot Public Status Pages
version_added: '6.1.0'
description:
    - Returns the full list of public status pages on the UptimeRobot account,
      with enum-style fields translated to human-readable labels (C(sort),
      C(status)).
    - Equivalent of C(utr get psps).
    - Read-only. Reports C(changed=false).
author:
    - Linuxfabrik GmbH, Zurich, Switzerland (info (at) linuxfabrik (dot) ch)
options:
    api_key:
        description: UptimeRobot API key. See C(uptimerobot_monitor) for the resolution order.
        type: str
        no_log: true
    api_key_file:
        description: Path to a file containing the API key. Default C(~/.uptimerobot).
        type: str
    friendly_name:
        description:
            - If set, only the PSP with this exact friendly name is returned
              (or none, if no match).
        type: str
'''


EXAMPLES = r'''
# 1) Equivalent to `utr get psps`.
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
    description: List of PSP dicts (empty list if none matched).
    type: list
    returned: always
    elements: dict
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.linuxfabrik.lfops.plugins.module_utils import uptimerobot as ur


def main():
    argument_spec = dict(
        api_key=dict(type='str', no_log=True),
        api_key_file=dict(type='str'),
        friendly_name=dict(type='str'),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    api_key = ur.resolve_api_key(module, module.params.get('api_key'), module.params.get('api_key_file'))
    friendly_name = module.params.get('friendly_name')

    module.log('uptimerobot_psp_info: fetching public status pages')
    success, psps = ur.get_psps(module, api_key)
    if not success:
        module.fail_json(msg='Could not list PSPs: {0}'.format(psps))

    if friendly_name:
        match = ur.find_by_friendly_name(psps, friendly_name)
        psps = [match] if match else []

    module.exit_json(changed=False, psps=psps, debug={
        'operation': 'list',
        'count': len(psps),
    })


if __name__ == '__main__':
    main()
