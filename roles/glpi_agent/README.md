# Ansible Role linuxfabrik.lfops.glpi_agent

This role installs and configures the [GLPI Agent](https://glpi-agent.readthedocs.io).


*Available since LFOps `3.0.0`.*


## How the Role Behaves

The scheduled database inventory runs as a one-shot via a systemd timer instead of as part of the always-on daemon, because the agent refuses `--credentials` in daemon mode and offers no equivalent configuration directive.

Enabling the scheduled inventory also disables the `database` category on the always-on daemon. Without credentials the daemon falls back to its default database access (root via the local socket) on every cycle, which the dedicated account is meant to replace.

The one-shot must not inherit that `no-category` setting, otherwise the agent would discard its own `--partial=database` run. It therefore gets its own configuration file at `/etc/glpi-agent/db-inventory.cfg`, passed via `--conf-file`, which carries the same settings without the `no-category` directive. Both files are rendered from the same template, so they cannot drift apart. Note that the file lives outside `conf.d`, since the daemon would otherwise read it too.

The credentials are assembled from `glpi_agent__database_inventory_login` into the `0600` environment file `/etc/glpi-agent/db-inventory.env` and pulled into the unit via `EnvironmentFile`, so they are not part of the unit file itself. systemd expands the variable into the command line when it starts the job, so the password is readable in the process list for as long as the one-shot runs. Use a dedicated read-only database account, and keep the password in Ansible Vault.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* On RHEL-compatible systems, the EPEL repository must be enabled (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)).


## Tags

`glpi_agent`

* Installs and configure GLPI Agent.
* Triggers: glpi-agent.service restart.

`glpi_agent:configure`

* Deploys the configuration files.
* Triggers: glpi-agent.service restart.

`glpi_agent:database_inventory`

* Deploys the optional database inventory timer, service and credentials file.
* Triggers: systemctl daemon-reload.

`glpi_agent:state`

* Manages the state of the systemd service.
* Triggers: none.


## Mandatory Role Variables

`glpi_agent__conf_server`

* Specifies the server to use both as a controller for the agent, and as a recipient for task execution output.
* Type: String.
* Default: none

Example:
```yaml
# mandatory
glpi_agent__conf_server: 'https://glpi.example.com'
```


## Optional Role Variables

`glpi_agent__conf_local`

* Write the results of the tasks execution locally.
* Type: String.
* Default: `'/tmp'`

`glpi_agent__conf_no_category`

* List of inventory categories to disable via the `no-category` directive (for example `database` to stop the agent from inventorying local databases). When `glpi_agent__database_inventory_enabled` is `true`, the `database` category is added automatically.
* Type: List.
* Default: `[]`

`glpi_agent__conf_no_ssl_check`

* Ignore self-signed certificates of the server.
* Type: Bool.
* Default: `false`

`glpi_agent__conf_ssl_fingerprint`

* Specifies the fingerprint of the ssl server certificate to trust. The fingerprint to use can be retrieved in agent log by temporarily enabling `glpi_agent__conf_no_ssl_check` option.
* Type: String.
* Default: unset

`glpi_agent__database_inventory_enabled`

* Deploys a systemd timer that periodically runs `glpi-agent --partial=database`, and disables the `database` category on the always-on daemon. When `false`, the timer, service, configuration and environment file are removed.
* Type: Bool.
* Default: `false`

`glpi_agent__database_inventory_login`

* The database account used by the scheduled database inventory. Mandatory when `glpi_agent__database_inventory_enabled` is `true`.
* Type: Dictionary.
* Default: none

`glpi_agent__database_inventory_on_calendar`

* The `OnCalendar` schedule of the database inventory timer. The timer also applies a `RandomizedDelaySec` of 30 minutes, so the job does not collide with fixed maintenance windows such as system updates.
* Type: String.
* Default: `'*-*-* 00/6:17:00'`

`glpi_agent__service_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`glpi_agent__service_state`

* Changes the state of the GLPI Agent service, analogous to `systemctl start/stop/restart/reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `glpi_agent__service_enabled` is `true`, else `'stopped'`

`glpi_agent__version`

* The version of blocky to install. Possible options: `'latest'`, or any from https://github.com/glpi-project/glpi-agent/releases.
* Type: String.
* Default: `'latest'`

Example:
```yaml
# optional
glpi_agent__conf_local: '/tmp'
glpi_agent__conf_no_category: []
glpi_agent__conf_no_ssl_check: false
glpi_agent__conf_ssl_fingerprint: 'sha256$...'
glpi_agent__database_inventory_enabled: false
glpi_agent__database_inventory_login:
  username: 'glpi-reader'
  password: 'linuxfabrik'
glpi_agent__database_inventory_on_calendar: '*-*-* 00/6:17:00'
glpi_agent__service_enabled: true
glpi_agent__service_state: 'started'
glpi_agent__version: 'latest'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
