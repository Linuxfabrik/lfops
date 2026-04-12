# Ansible Role linuxfabrik.lfops.example

This role installs and configures [Example](https://example.com/). Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

This role also serves as a reference for consistent role development across LFOps. All `ansible.builtin.*` modules used in `tasks/main.yml` are documented with their most common parameters.

This role is compatible with the following example versions:

* 1.0.0
* 2.0.0

## Mandatory Requirements

* Enable the example repository. This can be done using the [linuxfabrik.lfops.repo_example](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_example) role.

If you use the [Example Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/example.yml), this is automatically done for you.


## Optional Requirements

* Install the optional dependency. This can be done using the [linuxfabrik.lfops.optional_dependency](https://github.com/Linuxfabrik/lfops/tree/main/roles/optional_dependency) role.


## Tags

`example`

* Installs required packages and plugins.
* Creates the example system user and group.
* Deploys the configuration files.
* Ensures the example service is in the desired state.
* Triggers: example.service restart.

`example:configure`

* Deploys configuration files.
* Triggers: example.service restart.

`example:state`

* Manages the service state (start, stop, enable, disable).
* Triggers: none.

`example:plugin`

* Manages optional example plugins (install/remove).
* Triggers: none.

`example:user`

* Manages application users via the REST API.
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

* Maximum number of concurrent connections. Must be between 1 and 10000.
* Type: Number.
* Default: `100`

`example__conf_worker_threads`

* Number of worker threads for request processing.
* Type: Number.
* Default: 1.0.0: `4`, 2.0.0: `8`

`example__lib_version`

* The version of the [Linuxfabrik Python Libraries](https://github.com/Linuxfabrik/lib) to install.
* Type: String.

`example__listeners__host_var` / `example__listeners__group_var`

* Network listeners for the example service. Items are identified by a composite key of `name` + `port`, allowing the same name on different ports.
* Type: List of dictionaries.
* Default:

    ```yaml
    - name: 'default'
      port: 8080
    - name: 'default'
      port: 8443
      ssl: true
    ```

* Subkeys:

    * `name`:

        * Mandatory. Listener name.
        * Type: String.

    * `port`:

        * Mandatory. Port number.
        * Type: Number.

    * `ssl`:

        * Optional. Enable SSL for this listener.
        * Type: Bool.
        * Default: `false`

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`example__logrotate`

* Log files are rotated `count` days before being removed. If count is `0`, old versions are removed rather than rotated. If count is `-1`, old logs are not removed at all (use with caution, may waste performance and disk space).
* Type: Number.
* Default: `{{ logrotate__rotate | d(14) }}`

`example__maintenance_cron_minute`

* Minute of the hour at which the maintenance cron job runs.
* Type: Number.
* Default: `{{ 59 | random(seed=inventory_hostname) }}`

`example__plugins__host_var` / `example__plugins__group_var`

* Optional plugins to install as OS packages.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Package name of the plugin.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

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

    * `name`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Mandatory for `state: 'present'` users. Password.
        * Type: String.

    * `comment`:

        * Optional. User description.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

Example:
```yaml
# optional
example__conf_log_level__host_var: 'debug'
example__conf_max_connections__host_var: 200
example__conf_worker_threads: 16
example__lib_version: '2.4.0'
example__listeners__host_var:
  - name: 'default'
    port: 8443
    state: 'absent'
  - name: 'api'
    port: 9090
example__logrotate: 7
example__maintenance_cron_minute: 30
example__plugins__host_var:
  - name: 'example-plugin-auth-ldap'
  - name: 'example-plugin-cache-redis'
  - name: 'example-plugin-legacy-api'
    state: 'absent'
example__service_enabled: true
example__service_state: 'started'
example__users__host_var:
  - name: 'example-admin'
    password: 'linuxfabrik'
    comment: 'Admin Account'
  - name: 'old-user'
    state: 'absent'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
