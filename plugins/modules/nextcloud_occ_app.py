#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
module: nextcloud_occ_app

short_description: Manage Nextcloud apps using occ commands.

description:
  - This module manages Nextcloud apps using C(occ).
  - It retrieves the current app state via C(app:list --output=json) and
    only performs actions if the current state differs from the desired one.

requirements:
  - Nextcloud installation with C(occ) available.

author:
  - Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch

version_added: "2.0.1"

options:
  name:
    description:
      - The name of the app to manage.
    type: str
    required: true
  state:
    description:
      - The desired state of the app.
      - C(enabled) installs (if absent) and enables the app.
      - C(disabled) disables the app if it is currently enabled.
      - C(present) installs the app but keeps it disabled.
      - C(absent) removes the app.
    type: str
    choices: ['absent', 'disabled', 'enabled', 'present']
    default: 'enabled'
  force:
    description:
      - Whether to use the C(--force) flag for C(app:install) and C(app:enable).
    type: bool
    default: false
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
  installed_apps_json:
    description:
      - Pre-fetched JSON output from C(occ app:list --output=json).
      - When provided, the module skips calling C(app:list) itself,
        avoiding repeated occ invocations in a loop.
    type: raw
'''

EXAMPLES = r'''
- name: 'Enable a Nextcloud app'
  linuxfabrik.lfops.nextcloud_occ_app:
    name: 'notify_push'
    state: 'enabled'

- name: 'Disable a Nextcloud app'
  linuxfabrik.lfops.nextcloud_occ_app:
    name: 'comments'
    state: 'disabled'

- name: 'Remove a Nextcloud app'
  linuxfabrik.lfops.nextcloud_occ_app:
    name: 'survey_client'
    state: 'absent'

- name: 'Install a Nextcloud app without enabling it'
  linuxfabrik.lfops.nextcloud_occ_app:
    name: 'notify_push'
    state: 'present'
    force: true
'''

RETURN = r'''
changed:
  description: Indicates if the app state was changed.
  returned: always
  type: bool
current_state:
  description: The current state of the app before any changes.
  returned: always
  type: str
rc:
  description: The return code from the last C(occ) command.
  returned: when changed
  type: int
stderr:
  description: The standard error from the last C(occ) command.
  returned: when changed
  type: str
stdout:
  description: The standard output from the last C(occ) command.
  returned: when changed
  type: str
'''

import json
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native


def get_current_state(module, php_path, occ_path, name, installed_apps_json):
    """Determine the current state of an app by querying occ app:list."""
    if installed_apps_json:
        if isinstance(installed_apps_json, str):
            try:
                app_list = json.loads(installed_apps_json)
            except (json.JSONDecodeError, ValueError):
                module.fail_json(msg=f'Failed to parse installed_apps_json: {installed_apps_json}')
        else:
            app_list = installed_apps_json
    else:
        list_cmd = [
            php_path,
            occ_path,
            '--no-interaction',
            '--output=json',
            'app:list',
        ]

        try:
            rc, stdout, stderr = module.run_command(list_cmd)
        except Exception as e:
            module.fail_json(msg=to_native(e), exception=traceback.format_exc())

        if rc != 0:
            module.fail_json(msg=f'Failed to list apps (rc={rc}): {stderr}')

        try:
            app_list = json.loads(stdout)
        except (json.JSONDecodeError, ValueError):
            module.fail_json(msg=f'Failed to parse JSON from occ app:list output: {stdout}')

    enabled_apps = app_list.get('enabled', {})
    disabled_apps = app_list.get('disabled', {})

    if name in enabled_apps:
        return 'enabled'
    if name in disabled_apps:
        return 'disabled'
    return 'absent'


def main():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', choices=['absent', 'disabled', 'enabled', 'present'], default='enabled'),
        force=dict(type='bool', default=False),
        occ_path=dict(type='str', default='/var/www/html/nextcloud/occ'),
        php_path=dict(type='str', default='php'),
        installed_apps_json=dict(type='raw'),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    name = module.params['name']
    state = module.params['state']
    force = module.params['force']
    occ_path = module.params['occ_path']
    php_path = module.params['php_path']

    installed_apps_json = module.params['installed_apps_json']

    current_state = get_current_state(module, php_path, occ_path, name, installed_apps_json)

    result = {
        'changed': False,
        'current_state': current_state,
    }

    # determine which occ commands need to be run
    commands = []

    if state == 'enabled':
        if current_state == 'enabled':
            module.exit_json(**result)
        elif current_state == 'disabled':
            cmd = [php_path, occ_path, '--no-interaction', 'app:enable']
            if force:
                cmd.append('--force')
            cmd.append(name)
            commands.append(cmd)
        elif current_state == 'absent':
            install_cmd = [php_path, occ_path, '--no-interaction', 'app:install', '--keep-disabled']
            if force:
                install_cmd.append('--force')
            install_cmd.append(name)
            commands.append(install_cmd)
            enable_cmd = [php_path, occ_path, '--no-interaction', 'app:enable']
            if force:
                enable_cmd.append('--force')
            enable_cmd.append(name)
            commands.append(enable_cmd)

    elif state == 'disabled':
        if current_state == 'enabled':
            commands.append([php_path, occ_path, '--no-interaction', 'app:disable', name])
        else:
            module.exit_json(**result)

    elif state == 'present':
        if current_state == 'absent':
            install_cmd = [php_path, occ_path, '--no-interaction', 'app:install', '--keep-disabled']
            if force:
                install_cmd.append('--force')
            install_cmd.append(name)
            commands.append(install_cmd)
        else:
            module.exit_json(**result)

    elif state == 'absent':
        if current_state == 'absent':
            module.exit_json(**result)
        else:
            commands.append([php_path, occ_path, '--no-interaction', 'app:remove', name])

    # if we get here, there are commands to run
    result['changed'] = True

    if module._diff:
        result['diff'] = dict(
            before=f'{name}: {current_state}\n',
            after=f'{name}: {state}\n' if state != 'absent' else '',
        )

    if module.check_mode:
        module.exit_json(**result)

    # execute the commands
    for cmd in commands:
        try:
            rc, stdout, stderr = module.run_command(cmd, check_rc=True)
        except Exception as e:
            module.fail_json(msg=to_native(e), exception=traceback.format_exc())

    # return results from the last command
    result['rc'] = rc
    result['stdout'] = stdout
    result['stderr'] = stderr
    module.exit_json(**result)


if __name__ == '__main__':
    main()
