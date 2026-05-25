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
module: nextcloud_occ_app_config

short_description: Manage a Nextcloud app configuration value via occ

description:
  - Drives C(occ config:app:set) and C(config:app:delete) to bring a single app config key into the desired state.
  - The current value and type are read from C(occ config:app:get --details --output=json) (or from a pre-fetched C(occ config:list --output=json --private) listing passed via I(installed_config_json)). C(occ config:app:set) is only called when the stored value or type does not already match.
  - When I(name) contains spaces, each whitespace-separated token is passed as a separate argument to C(occ), matching how Nextcloud addresses nested keys (e.g. C(name="endpoint enabled")).
  - Booleans are normalized for Nextcloud's storage. I(value) values C(true)/C(1)/C(on)/C(yes) (case-insensitive) become C(1) in the database; everything else becomes C(0). When reading via I(installed_config_json), the type is inferred from the JSON value type (Python C(bool)/C(int)/C(float)/C(list)/C(str)), since C(occ config:list) returns values already cast by C(convertTypedValue()).

requirements:
  - A working Nextcloud installation with the C(occ) command available.

author:
  - Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch

version_added: "6.0.0"

options:
  app:
    description:
      - App ID whose configuration is being managed (e.g. C(core), C(files_sharing), C(notify_push)).
    type: str
    required: true
  name:
    description:
      - Configuration key. Multiple whitespace-separated tokens are forwarded as separate arguments to C(occ), which is how Nextcloud addresses nested keys.
    type: str
    required: true
  value:
    description:
      - Target value for the configuration key. Required when I(state=C(present)).
      - When I(type=C(array)), pass a valid JSON array literal; this module forwards the string verbatim and lets C(occ) parse it.
    type: str
  type:
    description:
      - Data type C(occ config:app:set) records for the value.
    type: str
    choices: ['string', 'integer', 'float', 'boolean', 'array']
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
      - Pre-fetched output of C(occ config:list --output=json --private), as either a JSON string or an already-parsed dict. When set, the module skips the C(config:app:get) call and reads the current value from this value, which avoids running C(occ) once per key when looping over many keys.
    type: raw
'''

EXAMPLES = r'''
- name: 'Set an app configuration value'
  linuxfabrik.lfops.nextcloud_occ_app_config:
    app: 'core'
    name: 'shareapi_expire_after_n_days'
    value: 90
    type: 'integer'
    occ_path: '/data/nextcloud/occ'
    php_path: '/usr/bin/php'
'''

RETURN = r'''
changed:
  description: Whether the value or type had to be changed.
  returned: always
  type: bool
current_type:
  description: Stored type before any changes were applied. Empty string when the key did not exist.
  returned: always
  type: str
current_value:
  description: Stored value (as a string) before any changes were applied. Empty string when the key did not exist. Booleans are normalized to C(1)/C(0) to match how Nextcloud stores them.
  returned: always
  type: str
rc:
  description: Exit code of the C(occ config:app:set) or C(config:app:delete) command.
  returned: when changed and not in check mode
  type: int
stderr:
  description: Standard error of the C(occ config:app:set) or C(config:app:delete) command.
  returned: when changed and not in check mode
  type: str
stdout:
  description: Standard output of the C(occ config:app:set) or C(config:app:delete) command.
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
            app=dict(type='str', required=True),
            name=dict(type='str', required=True),
            value=dict(type='str'),
            type=dict(type='str', choices=['string', 'integer', 'float', 'boolean', 'array'], default='string'),
            state=dict(type='str', choices=['absent', 'present'], default='present'),
            occ_path=dict(type='str', default='/var/www/html/nextcloud/occ'),
            php_path=dict(type='str', default='php'),
            installed_config_json=dict(type='raw'),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ('state', 'present', ('value',)),
        ],
    )

    # extract the variables to make the code more readable
    app = module.params['app']
    name = module.params['name']
    value = module.params['value']
    value_type = module.params['type']
    state = module.params['state']
    occ_path = module.params['occ_path']
    php_path = module.params['php_path']

    # nextcloud stores app config booleans as 1/0 in the database.
    # ConfigManager::convertToBool() accepts: true/1/on/yes and false/0/off/no
    if value_type == 'boolean' and value is not None:
        value = '1' if value.lower() in ('true', '1', 'on', 'yes') else '0'

    installed_config_json = module.params['installed_config_json']

    # we promised to always return these keys
    result = {
        'changed': False,
        'current_type': '',
        'current_value': '',
    }

    # get the current value, either from cache or by running occ
    if installed_config_json:
        if isinstance(installed_config_json, str):
            try:
                installed_config_json = json.loads(installed_config_json)
            except (json.JSONDecodeError, ValueError):
                module.fail_json(msg='Failed to parse installed_config_json')

        app_configs = installed_config_json.get('apps', {}).get(app, {})
        key_exists = name in app_configs
        if key_exists:
            raw = app_configs[name]
            # infer the type from the JSON value's Python type,
            # since config:list returns values through convertTypedValue()
            # which converts based on the DB type column.
            # must check bool before int, as bool is a subclass of int.
            if isinstance(raw, bool):
                current_value = '1' if raw else '0'
                current_type = 'boolean'
            elif isinstance(raw, int):
                current_value = str(raw)
                current_type = 'integer'
            elif isinstance(raw, float):
                current_value = str(raw)
                current_type = 'float'
            elif isinstance(raw, list):
                current_value = str(raw)
                current_type = 'array'
            else:
                current_value = str(raw)
                current_type = 'string'
        else:
            current_value = ''
            current_type = ''
    else:
        get_cmd = [
            php_path,
            occ_path,
            '--no-interaction',
            '--details',
            '--output=json',
            'config:app:get',
            app,
        ] + name.split() # occ expects each part of the name as a separate argument

        try:
            get_rc, get_stdout, _ = module.run_command(get_cmd)
        except Exception as e:
            module.fail_json(msg=to_native(e), exception=traceback.format_exc())

        try:
            current = json.loads(get_stdout) if get_rc == 0 else {}
        except (json.JSONDecodeError, ValueError):
            module.fail_json(msg=f'Failed to parse JSON from occ config:app:get output: {get_stdout}')

        key_exists = get_rc == 0
        current_type = current.get('type', '')
        current_value = current.get('value', '')

    result['current_type'] = current_type
    result['current_value'] = current_value

    if state == 'present':
        # check if the current value and type match the desired settings
        if current_value == value and current_type == value_type:
            module.exit_json(**result)

        # else, the value will be changed
        result['changed'] = True

        # add diff if required
        if module._diff:
            result['diff'] = dict(
                before=f'{app} {name}: value={current_value}, type={current_type}\n',
                after=f'{app} {name}: value={value}, type={value_type}\n',
            )

        # in check mode, exit here, indicating that a change would occur
        if module.check_mode:
            module.exit_json(**result)

        # build the occ set command
        set_cmd = [
            php_path,
            occ_path,
            '--no-interaction',
            'config:app:set',
            f'--value={value}',
            f'--type={value_type}',
            app,
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
                before=f'{app} {name}: value={current_value}, type={current_type}\n',
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
            'config:app:delete',
            app,
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
