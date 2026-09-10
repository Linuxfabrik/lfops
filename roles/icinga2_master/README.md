# Ansible Role linuxfabrik.lfops.icinga2_master

This role installs and configures [Icinga2](https://icinga.com/docs/icinga-2/latest/doc/01-about/) as a monitoring master.


*Available since LFOps `2.0.0`.*


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* InfluxDB must be installed with a database and a user for said database (role: [linuxfabrik.lfops.influxdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/influxdb)).
* MariaDB must be installed with a database and a user for said database (role: [linuxfabrik.lfops.mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server)).
* On RHEL-compatible systems, the `icinga2_can_connect_all`, `icinga2_run_sudo` and `nagios_run_sudo` SELinux booleans must be enabled (role: [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux)).

## Tags

`icinga2_master`

* Installs and configures Icinga2 as a master.
* Triggers: icinga2.service restart.

`icinga2_master:api_users`

* Manages the Icinga2 API users.
* Triggers: icinga2.service restart.

`icinga2_master:logrotate`

* Deploys the Icinga2 logrotate config. Serves as a hotfix for the following issue: [RLIMIT permission warnings](https://github.com/Icinga/icinga2/issues/10617).
* Triggers: none.

`icinga2_master:state`

* Manages the state of the Icinga2 service.
* Triggers: none.

`icinga2_agent:systemd_override`

* Deploys: `/etc/systemd/system/icinga2.service.d/z00-after-sssd.conf`.
* Triggers: none.


## Mandatory Role Variables

`icinga2_master__enrolment_api_user`

* The API account for generating tickets. This can be used to enrol new hosts.
* Type: Dictionary.

`icinga2_master__influxdb_login`

* The user account for accessing the Icinga2 InfluxDB database.
* Type: Dictionary.

Example:
```yaml
# mandatory
icinga2_master__enrolment_api_user:
  username: 'enrolment-user'
  password: 'linuxfabrik'
icinga2_master__influxdb_login:
  username: 'icinga2'
  password: 'linuxfabrik'
```


## Optional Role Variables

`icinga2_master__api_users__host_var` / `icinga2_master__api_users__group_var`

* A list of dictionaries for the Icinga2 API users.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `password`:

        * Mandatory. The password of the API user.
        * Type: String.

    * `permissions`:

        * Mandatory. The permissions for the API user. Have a look at the example and https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#icinga2-api-permissions.
        * Type: List or String.

    * `state`:

        * Optional. Either `present` or `absent`.
        * Type: String.

    * `username`:

        * Mandatory. The username of the API user.
        * Type: String.

`icinga2_master__bind_host`

* The bind host. This allows restricting on which IP addresses Icinga2 is listening.
* Type: String.
* Default: unset

`icinga2_master__cn`

* The common name of the Icinga2 master. Tries to default to the FQDN of the server.
* Type: String.
* Default: `'{{ ansible_facts["nodename"] }}'`

`icinga2_master__downtime_api_user`

* An Icinga2 API user that may only schedule and remove downtimes (`actions/schedule-downtime`, `actions/remove-downtime`). The [borg_local](https://github.com/Linuxfabrik/lfops/tree/main/roles/borg_local), [nextcloud](https://github.com/Linuxfabrik/lfops/tree/main/roles/nextcloud), [schedule_reboot](https://github.com/Linuxfabrik/lfops/tree/main/roles/schedule_reboot) and [tools](https://github.com/Linuxfabrik/lfops/tree/main/roles/tools) roles use it by default to set a downtime around a backup, a Nextcloud update or a reboot, unless their own `*__icinga2_api_user_login` is set.
* Set it in `group_vars` that cover the Icinga2 master and every monitored host, since the monitored hosts read it as well. With the `linuxfabrik.lfops.bitwarden_item` lookup, pass a fixed `hostname` instead of `inventory_hostname`, so that all hosts get the same credential.
* If `icinga2_master__api_users__*_var` contains an API user with the same `username`, both end up as one `ApiUser` and the keys set in that inventory entry win. A different `password` there makes the downtime requests of the other roles fail, and a `permissions` list there replaces the two downtime permissions, so include them when adding more. An API user with a different `username` is left alone; remove it once no host uses it any more.
* Must be a different user than `icinga2_master__enrolment_api_user`.
* Type: Dictionary.
* Default: unset

`icinga2_master__influxdb_database_name`

* The name of the InfluxDB database.
* Type: String.
* Default: `'icinga2'`

`icinga2_master__influxdb_host`

* The host on which the InfluxDB database is reachable.
* Type: String.
* Default: `'localhost'`

`icinga2_master__influxdb_retention`

* Determines how long InfluxDB should keep the Icinga2 data. If specified, it should be `INF` or at least one hour.
* Type: String.
* Default: `'216d'`

`icinga2_master__service_enabled`

* Enables or disables the Icinga2 service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`icinga2_master__service_state`

* Changes the state of the Icinga2 service, analogous to `systemctl start/stop/restart/reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `icinga2_master__service_enabled` is `true`, else `'stopped'`

Example:
```yaml
# optional
icinga2_master__api_users__group_var: []
icinga2_master__api_users__host_var:
  - username: 'dashboard' # for example for grafinga
    password: "{{ lookup('linuxfabrik.lfops.bitwarden_item',
        {
          'hostname': inventory_hostname,
          'purpose': 'Icinga2 API',
          'username': 'dashboard',
          'collection_id': lfops__bitwarden_collection_id,
          'organization_id': lfops__bitwarden_organization_id,
        },
      )['password'] }}"
    permissions:
      - 'objects/query/*'
      - 'status/query'
  - username: 'ticket-user'
    password: 'linuxfabrik'
    permissions:
      - 'actions/generate-ticket'
    state: 'present'
  - username: 'check-logfile-windows-api-user'
    password: 'linuxfabrik'
    permissions: |-
      [
      {% raw %}
        {
          permission = "objects/query/Service"
          filter = {{ regex("^check-logfile-windows-api-user", service.vars.logfile_windows_icinga_username ) }}
        }
      {% endraw %}
      ]
    state: 'present'
icinga2_master__bind_host: '192.0.2.12'
icinga2_master__cn: '{{ ansible_facts["nodename"] }}'
icinga2_master__downtime_api_user:
  username: 'downtime-user'
  password: 'linuxfabrik'
icinga2_master__influxdb_database_name: 'icinga2'
icinga2_master__influxdb_host: 'localhost'
icinga2_master__influxdb_retention: '216d'
icinga2_master__service_enabled: true
icinga2_master__service_state: 'started'
```


## Optional Role Variables - Primary-Secondary Setup

Adjust the following variables for the secondary Icinga2 master.

`icinga2_master__additional_master_endpoints`

* A list of endpoints which should be in the Icinga2 master zone. For example, the primary Icinga2 master endpoint on the secondary, and vice versa.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `cn`:

        * Mandatory. The common name of the additional Icinga2 master. This should be equal to `icinga2_master__cn` on the additional master.
        * Type: String.

    * `host`:

        * Mandatory. The hostname or IP of the additional Icinga2 master.
        * Type: String.

    * `port`:

        * Optional. Icinga2 Port.
        * Type: Number.
        * Default: `5665`

`icinga2_master__api_ticket_login`

* Only used on a secondary master (`icinga2_master__node_role: 'secondary'`). The secondary logs in on the Icinga2 API of the primary with this user and requests the ticket that gets its own certificate signed automatically ([CSR auto-signing](https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#generate-ticket)). The user has to exist on the primary with the `actions/generate-ticket` permission, which `icinga2_master__enrolment_api_user` has. Agents request their ticket with `icinga2_agent__icinga2_api_user_login` instead.
* The default works when both masters have the same `icinga2_master__enrolment_api_user`. Set this variable to the credentials of the primary's enrolment user when they differ per master, for example because the `linuxfabrik.lfops.bitwarden_item` lookup uses `inventory_hostname`.
* Type: Dictionary.
* Default: `'{{ icinga2_master__enrolment_api_user }}'`

`icinga2_master__influxdb_enable_ha`

* If high availability should be enabled for the InfluxDB database or not. Have a look at https://icinga.com/docs/icinga-2/latest/doc/14-features/#influxdb-in-cluster-ha-zones.
* Type: Bool.
* Default: `false`

`icinga2_master__influxdb_ssl_enable`

* If SSL should be enabled for the InfluxDB database connection. Have a look at https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#objecttype-influxdbwriter.
* Type: Bool.
* Default: `false`

`icinga2_master__node_role`

* The role of this Icinga2 node. Possible options: `primary`, `secondary`.
* Type: String.
* Default: `'primary'`

`icinga2_master__primary_host`

* The host on which the Icinga2 master is running. Needs to be reachable from the secondary node.
* Type: String.
* Default: unset

`icinga2_master__primary_port`

* The port on which the Icinga2 master is running. Needs to be reachable from the secondary node.
* Type: Number.
* Default: `5665`

Example:
```yaml
# primary-secondary
icinga2_master__additional_master_endpoints:
  - cn: 'master1.example.com'
    host: 'master1.example.com'
    port: 5666
icinga2_master__api_ticket_login:
  username: 'ticket-user'
  password: 'linuxfabrik'
icinga2_master__influxdb_enable_ha: false
icinga2_master__influxdb_ssl_enable: false
icinga2_master__node_role: 'primary'
icinga2_master__primary_host: 'master1.example.com'
icinga2_master__primary_port: 5666
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
