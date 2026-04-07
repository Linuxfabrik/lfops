# Ansible Role linuxfabrik.lfops.example

This role installs and configures [Example](https://example.com/). Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

This role also serves as a reference for consistent role development across LFOps. All `ansible.builtin.*` modules used in `tasks/main.yml` are documented alphabetically with their most common parameters.


## Mandatory Requirements

* Enable the example repository. This can be done using the [linuxfabrik.lfops.repo_example](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_example) role.

If you use the [Example Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/example.yml), this is automatically done for you.


## Tags

`example`

* Installs required packages.
* Creates the example system user and group.
* Deploys the configuration files.
* Ensures the example service is in the desired state.
* Triggers: example.service restart.

`example:configure`

* Deploys configuration files.
* Runs database migrations if needed.
* Triggers: example.service restart.

`example:state`

* Manages the service state (start, stop, enable, disable).
* Waits for the service to become available.
* Triggers: none.

`example:user`

* Manages the example system user and application users.
* Triggers: none.


## Mandatory Role Variables

`example__version`

* The version of example to install.
* Type: String.

Example:
```yaml
# mandatory
example__version: '3.2.1'
```


## Optional Role Variables

`example__conf_log_level__host_var` / `example__conf_log_level__group_var`

* The log level.
* Type: String. One of `debug`, `info`, `warn`, `error`.
* Default: `'info'`

`example__conf_max_connections__host_var` / `example__conf_max_connections__group_var`

* Maximum number of concurrent connections.
* Type: Number.
* Default: `100`

`example__logrotate`

* Log files are rotated `count` days before being removed. If count is `0`, old versions are removed rather than rotated. If count is `-1`, old logs are not removed at all (use with caution, may waste performance and disk space).
* Type: Number.
* Default: `{{ logrotate__rotate | d(14) }}`

`example__service_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`example__service_state`

* Changes the state of the service, analogous to `systemctl start/stop/restart/reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'`

`example__users__host_var` / `example__users__group_var`

* Application users to manage.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:
    * `name`: Mandatory, string. Username.
    * `comment`: Optional, string. User description.
    * `group`: Optional, string. Primary group.
    * `home`: Optional, string. Home directory.
    * `shell`: Optional, string. Login shell.
    * `state`: Optional, string. `present` or `absent`. Defaults to `'present'`.

Example:
```yaml
# optional
example__conf_log_level__host_var: 'debug'
example__conf_max_connections__host_var: 200
example__logrotate: 7
example__service_enabled: true
example__service_state: 'started'
example__users__host_var:
  - name: 'app-user'
    comment: 'Application User'
    group: 'example'
    shell: '/bin/bash'
  - name: 'old-user'
    state: 'absent'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
