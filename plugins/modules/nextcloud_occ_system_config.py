#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
module: nextcloud_occ_system_config

short_description: Manage Nextcloud System configuration using occ commands.

description:
  - This module sets Nextcloud configuration values using C(occ).
  - It retrieves the current value via C(config:system:get) and
    only changes it if the value differs from the desired one.

requirements:
  - Nextcloud installation with C(occ) available.

author:
  - Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch

version_added: "2.0.1"

options:
  name:
    description:
      - Name of the configuration key to manage.
    type: str
    required: true
  value:
    description:
      - The desired value for the configuration key.
    type: str
    required: true
  type:
    description:
      - The data type of the configuration value.
    type: str
    choices: ['string', 'integer', 'double', 'boolean']
    default: 'string'
  state:
    description:
      - The state of the config key. If C(present) the key will be set to the value,
        if C(absent) the config key will be deleted.
    type: str
    choices: ['absent', 'present']
    default: 'present'
  occ_path:
    description:
      - The full path to the C(occ) command.
    type: str
    default: '/var/www/html/nextcloud/occ'
  php_path:
    description:
      - The full path to the PHP binary to use.
    type: str
    default: 'php'
'''

EXAMPLES = r'''
- name: 'Set a system configuration value'
  linuxfabrik.lfops.nextcloud_occ_system_config:
    config_type: 'system'
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
  description: Indicates if the configuration was changed.
  returned: always
  type: bool
current_value:
  description: The current configuration value.
  returned: always
  type: str
rc:
  description: The return code from the C(occ config:system:set) command.
  returned: when changed
  type: int
stderr:
  description: The standard error from the C(occ config:system:set) command.
  returned: when changed
  type: str
stdout:
  description: The standard output from the C(occ config:system:set) command.
  returned: when changed
  type: str
'''

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native

def main():
    # define available arguments/parameters a user can pass to this module
    module_args = dict(
            name=dict(type='str', required=True),
            value=dict(type='str', required=True),
            type=dict(type='str', choices=['string', 'integer', 'double', 'boolean'], default='string'),
            state=dict(type='str', choices=['absent', 'present'], default='present'),
            occ_path=dict(type='str', default='/var/www/html/nextcloud/occ'),
            php_path=dict(type='str', default='php'),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if this module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    # extract the variables to make the code more readable
    name = module.params['name']
    value = module.params['value']
    value_type = module.params['type']
    state = module.params['state']
    occ_path = module.params['occ_path']
    php_path = module.params['php_path']

    # ansible will convert all yaml boolean values to True/False
    # however, nextcloud always uses lowercase booleans
    if value_type == 'boolean':
        value = value.lower()

    # we promised to always return these keys
    result = {
        'changed': False,
        'current_value': '',
    }

    # build the occ get command
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

    current_value = get_stdout.strip() if get_rc == 0 else ''
    result['current_value'] = current_value

    if state == 'present':
        # check if the current value matches the desired value
        if current_value == value:
            module.exit_json(**result)

        # else, the value will be changed
        result['changed'] = True

        # add diff if required
        if module._diff:
            # result['diff'] = dict(
            #     before=f'{current_value}\n',
            #     after=f'{value}\n',
            # )

            # sadly we cannot easily color this output, as we cannot import ansible.utils.color from modules
            result['diff'] = dict(
                prepared=f'* "{name}" changed from "{current_value}" to "{value}"',
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
        # the return code is 1 if the config does not exist
        if get_rc == 1:
            # so there is no change
            module.exit_json(**result)

        # else, there will be a change
        result['changed'] = True

        # add diff if required
        if module._diff:
            # result['diff'] = dict(
            #     before=f'{current_value}\n',
            #     after=f'{value}\n',
            # )

            # sadly we cannot easily color this output, as we cannot import ansible.utils.color in here
            result['diff'] = dict(
                prepared=f'* deleted "{name}" with value "{current_value}"',
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
