#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch
# The Unlicense (see LICENSE or https://unlicense.org/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
module: nextcloud_occ_app

short_description: Install, enable, disable or remove a Nextcloud app via occ

description:
  - Drives the Nextcloud C(occ app:install), C(app:enable), C(app:disable) and C(app:remove) commands to bring a single app into the desired state.
  - The current state is determined from C(occ app:list --output=json) (or from a pre-fetched listing passed via I(installed_apps_json)) and is one of C(enabled), C(disabled) or C(absent). Subsequent C(occ) commands are only run when the current state does not already match I(state).
  - Going from C(absent) to C(enabled) installs the app with C(--keep-disabled) and then enables it as a separate step, so the install path is the same regardless of whether the app should end up enabled or just present.

requirements:
  - A working Nextcloud installation with the C(occ) command available.

author:
  - Linuxfabrik GmbH, Zurich, Switzerland, https://www.linuxfabrik.ch

version_added: "6.0.0"

options:
  name:
    description:
      - Name of the Nextcloud app (the app ID, e.g. C(notify_push), C(comments)).
    type: str
    required: true
  state:
    description:
      - Desired state of the app.
      - C(enabled) - install the app if missing and enable it.
      - C(disabled) - disable the app if it is currently enabled. Does nothing if the app is already disabled or absent.
      - C(present) - install the app if missing but leave it disabled. Does nothing if the app already exists in any state.
      - C(absent) - remove the app entirely.
    type: str
    choices: ['absent', 'disabled', 'enabled', 'present']
    default: 'enabled'
  force:
    description:
      - Pass C(--force) to C(app:install) and C(app:enable) so that Nextcloud installs apps that are not officially compatible with the running version.
    type: bool
    default: false
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
  installed_apps_json:
    description:
      - Pre-fetched output of C(occ app:list --output=json), as either a JSON string or an already-parsed dict. When set, the module skips the C(app:list) call and reads the current state from this value, which avoids running C(occ) once per app when looping over a list.
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
  description: Whether the app state had to be changed.
  returned: always
  type: bool
current_state:
  description: State of the app before any changes were applied. One of C(enabled), C(disabled) or C(absent).
  returned: always
  type: str
rc:
  description: Exit code of the last C(occ) command that was executed. Only the last one is reported, since failure of any earlier one aborts the module.
  returned: when changed and not in check mode
  type: int
stderr:
  description: Standard error of the last C(occ) command that was executed.
  returned: when changed and not in check mode
  type: str
stdout:
  description: Standard output of the last C(occ) command that was executed.
  returned: when changed and not in check mode
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
