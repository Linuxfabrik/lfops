#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
module: nextcloud_occ_system_config

short_description: Manage a Nextcloud system configuration value via occ

description:
  - Drives C(occ config:system:set) and C(config:system:delete) to bring a single system config key into the desired state.
  - The current value is read from C(occ config:system:get) (or from a pre-fetched C(occ config:list --output=json --private) listing passed via I(installed_config_json)). C(occ config:system:set) is only called when the stored value does not already match I(value).
  - When I(name) contains spaces, each whitespace-separated token is passed as a separate argument to C(occ), matching how Nextcloud addresses nested keys (e.g. C(name="trusted_domains 0"), C(name="forbidden_filename_characters 0")).
  - Booleans are normalized for C(occ). I(value) values C(true)/C(1)/C(on)/C(yes) (case-insensitive) become the literal string C(true); everything else becomes C(false). This matches what Nextcloud's CastHelper accepts on C(config:system:set). Note that this differs from C(nextcloud_occ_app_config), which stores booleans as C(1)/C(0).

requirements:
  - A working Nextcloud installation with the C(occ) command available.

author:
  - Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch

version_added: "6.0.0"

options:
  name:
    description:
      - Configuration key. Multiple whitespace-separated tokens are forwarded as separate arguments to C(occ), which is how Nextcloud addresses nested keys.
    type: str
    required: true
  value:
    description:
      - Target value for the configuration key. Required when I(state=C(present)).
    type: str
  type:
    description:
      - Data type C(occ config:system:set) records for the value. Note that C(occ) names the floating point type C(double), not C(float).
    type: str
    choices: ['string', 'integer', 'double', 'boolean']
    default: 'string'
  state:
    description:
      - C(present) creates or updates the key, C(absent) deletes it.
    type: str
    choices: ['absent', 'present']
    default: 'present'
  occ_path:
    description:
      - Absolute path to the Nextcloud C(occ) command.
    type: str
    default: '/var/www/html/nextcloud/occ'
  php_path:
    description:
      - PHP binary to invoke C(occ) with. A bare C(php) relies on C($PATH); pass an absolute path to pin a specific PHP version.
    type: str
    default: 'php'
  installed_config_json:
    description:
      - Pre-fetched output of C(occ config:list --output=json --private), as either a JSON string or an already-parsed dict. When set, the module skips the C(config:system:get) call and walks I(name) through the dict tree (descending into both dicts and lists by index), which avoids running C(occ) once per key when looping over many keys.
    type: raw
'''

EXAMPLES = r'''
- name: 'Set a system configuration value'
  linuxfabrik.lfops.nextcloud_occ_system_config:
    name: 'check_for_working_wellknown_setup'
    value: true
    type: 'boolean'

- name: 'Set an array subkey'
  linuxfabrik.lfops.nextcloud_occ_system_config:
    name: 'forbidden_filename_characters 0'
    value: '*'
'''

RETURN = r'''
changed:
  description: Whether the value had to be changed.
  returned: always
  type: bool
current_value:
  description: Stored value (as a string) before any changes were applied. Empty string when the key did not exist. Booleans are returned lowercase (C(true)/C(false)) to match what C(occ config:system:set) accepts.
  returned: always
  type: str
rc:
  description: Exit code of the C(occ config:system:set) or C(config:system:delete) command.
  returned: when changed and not in check mode
  type: int
stderr:
  description: Standard error of the C(occ config:system:set) or C(config:system:delete) command.
  returned: when changed and not in check mode
  type: str
stdout:
  description: Standard output of the C(occ config:system:set) or C(config:system:delete) command.
  returned: when changed and not in check mode
  type: str
'''

import json
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native

def main():
    # define available arguments/parameters a user can pass to this module
    module_args = dict(
            name=dict(type='str', required=True),
            value=dict(type='str'),
            type=dict(type='str', choices=['string', 'integer', 'double', 'boolean'], default='string'),
            state=dict(type='str', choices=['absent', 'present'], default='present'),
            occ_path=dict(type='str', default='/var/www/html/nextcloud/occ'),
            php_path=dict(type='str', default='php'),
            installed_config_json=dict(type='raw'),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if this module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ('state', 'present', ('value',)),
        ],
    )

    # extract the variables to make the code more readable
    name = module.params['name']
    value = module.params['value']
    value_type = module.params['type']
    state = module.params['state']
    occ_path = module.params['occ_path']
    php_path = module.params['php_path']

    installed_config_json = module.params['installed_config_json']

    # nextcloud's CastHelper only accepts 'true'/'false' for config:system:set.
    # coerce all truthy/falsy representations to what nextcloud expects.
    if value_type == 'boolean' and value is not None:
        value = 'true' if value.lower() in ('true', '1', 'on', 'yes') else 'false'

    # we promised to always return these keys
    result = {
        'changed': False,
        'current_value': '',
    }

    # get the current value, either from cache or by running occ
    if installed_config_json:
        if isinstance(installed_config_json, str):
            try:
                installed_config_json = json.loads(installed_config_json)
            except (json.JSONDecodeError, ValueError):
                module.fail_json(msg=f'Failed to parse installed_config_json')

        # navigate nested config by path parts (e.g. "trusted_domains 0")
        current = installed_config_json.get('system', {})
        key_exists = True
        for part in name.split():
            if isinstance(current, dict):
                if part in current:
                    current = current[part]
                else:
                    key_exists = False
                    break
            elif isinstance(current, list):
                try:
                    current = current[int(part)]
                except (ValueError, IndexError):
                    key_exists = False
                    break
            else:
                key_exists = False
                break

        if key_exists:
            if isinstance(current, bool):
                current_value = str(current).lower()
            else:
                current_value = str(current)
        else:
            current_value = ''
    else:
        get_cmd = [
            php_path,
            occ_path,
            '--no-interaction',
            'config:system:get',
        ] + name.split() # occ expects each part of the name as a separate argument

        try:
            get_rc, get_stdout, _ = module.run_command(get_cmd)
        except Exception as e:
            module.fail_json(msg=to_native(e), exception=traceback.format_exc())

        key_exists = get_rc == 0
        current_value = get_stdout.strip() if key_exists else ''

    result['current_value'] = current_value

    if state == 'present':
        # check if the current value matches the desired value
        if current_value == value:
            module.exit_json(**result)

        # else, the value will be changed
        result['changed'] = True

        # add diff if required
        if module._diff:
            result['diff'] = dict(
                before=f'{name}: {current_value}\n',
                after=f'{name}: {value}\n',
            )

        # in check mode, exit here, indicating that a change would occur
        if module.check_mode:
            module.exit_json(**result)

        # build the occ set command
        set_cmd = [
            php_path,
            occ_path,
            '--no-interaction',
            'config:system:set',
            f'--value={value}',
            f'--type={value_type}',
        ] + name.split() # occ expects each part of the name as a separate argument

        try:
            set_rc, set_stdout, set_stderr = module.run_command(set_cmd, check_rc=True)
        except Exception as e:
            module.fail_json(msg=to_native(e), exception=traceback.format_exc())

        result['rc'] = set_rc
        result['stdout'] = set_stdout
        result['stderr'] = set_stderr
        module.exit_json(**result)


    elif state == 'absent':
        if not key_exists:
            # config does not exist, so there is no change
            module.exit_json(**result)

        # else, there will be a change
        result['changed'] = True

        # add diff if required
        if module._diff:
            result['diff'] = dict(
                before=f'{name}: {current_value}\n',
                after='',
            )

        # in check mode, exit here, indicating that a change would occur
        if module.check_mode:
            module.exit_json(**result)

        # build the occ delete command
        delete_cmd = [
            php_path,
            occ_path,
            '--no-interaction',
            'config:system:delete',
        ] + name.split() # occ expects each part of the name as a separate argument

        try:
            delete_rc, delete_stdout, delete_stderr = module.run_command(delete_cmd, check_rc=True)
        except Exception as e:
            module.fail_json(msg=to_native(e), exception=traceback.format_exc())

        result['rc'] = delete_rc
        result['stdout'] = delete_stdout
        result['stderr'] = delete_stderr
        module.exit_json(**result)


if __name__ == '__main__':
    main()
