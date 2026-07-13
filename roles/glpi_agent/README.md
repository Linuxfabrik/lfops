# Ansible Role linuxfabrik.lfops.glpi_agent

This role installs and configures the [GLPI Agent](https://glpi-agent.readthedocs.io).


*Available since LFOps `3.0.0`.*


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* On RHEL-compatible systems, the EPEL repository must be enabled (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)).


## Tags

`glpi_agent`

* Installs and configure GLPI Agent.
* Triggers: glpi-agent.service restart.

`glpi_agent:configure`

* Deploys the configuration file.
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

`glpi_agent__database_inventory_credentials`

* The GLPI Agent `--credentials` string used by the scheduled database inventory, for example `type:login_password,login:glpi-reader,password:...`. Since the daemon rejects `--credentials`, the database inventory runs as a separate one-shot via a systemd timer. This value is written to the `0600` environment file `/etc/glpi-agent/db-inventory.env` and referenced from the service unit via `EnvironmentFile`, so it is not exposed by `systemctl show`. Use a dedicated read-only database account and store this value in Ansible Vault. Mandatory when `glpi_agent__database_inventory_enabled` is `true`.
* Type: String.
* Default: `''`

`glpi_agent__database_inventory_enabled`

* Deploys a systemd timer that periodically runs `glpi-agent --partial=database` with `glpi_agent__database_inventory_credentials`, and disables the `database` category on the always-on daemon so it no longer connects to the database as root. When `false`, the timer, service and credentials file are removed.
* Type: Bool.
* Default: `false`

`glpi_agent__database_inventory_on_calendar`

* The `OnCalendar` schedule of the database inventory timer. Defaults to every 6 hours; the timer also applies a `RandomizedDelaySec` of 30 minutes to avoid overlapping with fixed maintenance windows such as system updates.
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
glpi_agent__database_inventory_credentials: 'type:login_password,login:glpi-reader,password:...'
glpi_agent__database_inventory_enabled: false
glpi_agent__database_inventory_on_calendar: '*-*-* 00/6:17:00'
glpi_agent__service_enabled: true
glpi_agent__service_state: 'started'
glpi_agent__version: 'latest'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
