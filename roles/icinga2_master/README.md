# Ansible Role linuxfabrik.lfops.icinga2_master

This role installs and configures [Icinga2](https://icinga.com/docs/icinga-2/latest/doc/01-about/) as a monitoring master.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Install InfluxDB, and create a database and a user for said database. This can be done using the [linuxfabrik.lfops.influxdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/influxdb) role.
* Install MariaDB, and create a database and a user for said database. This can be done using the [linuxfabrik.lfops.mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server) role.


## Tags

| Tag                        | What it does                                |
| ---                        | ------------                                |
| `icinga2_master`           | Installs and configures Icinga2 as a master |
| `icinga2_master:api_users` | Manages the Icinga2 API users               |
| `icinga2_master:state`     | Manages the state of the Icinga2 service    |


## Mandatory Role Variables

| Variable                             | Description                                                                                  |
| --------                             | -----------                                                                                  |
| `icinga2_master__database_login`     | The user account for accessing the Icinga2 ido database. Currently, only MySQL is supported. |
| `icinga2_master__enrolment_api_user` | The API account for generating tickets. This can be used to enrol new hosts.                 |
| `icinga2_master__influxdb_login`     | The user account for accessing the Icinga2 InfluxDB database.                                |

Example:
```yaml
# mandatory
icinga2_master__database_login:
  username: 'icinga2'
  password: 'linuxfabrik'
icinga2_master__enrolment_api_user:
  username: 'enrolment-user'
  password: 'linuxfabrik'
icinga2_master__influxdb_login:
  username: 'icinga2'
  password: 'linuxfabrik'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icinga2_master__cn` | The common name of the Icinga2 master. Tries to default to the FQDN of the server. | `'{{ ansible_facts["nodename"] }}'` |
| `icinga2_master__database_host` | The host on which the ido database is reachable. | `'localhost'` |
| `icinga2_master__database_name` | The name of the ido database. | `'icinga2_ido'` |
| `icinga2_master__api_users__group_var` | A list of dictionaries for the Icinga2 API users. Subkeys:<br> * `username`: Required, string. The username of the API user.<br> * `password`: Required, string. The password of the API user.<br> * `permissions`: Required, list or raw string. The permissions for the API user. Have a look at the example and https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#icinga2-api-permissions.<br>For the usage in `group_vars` (can only be used in one group at a time). | `[]` |
| `icinga2_master__api_users__host_var` | A list of dictionaries for the Icinga2 API users. Subkeys:<br> * `username`: Required, string. The username of the API user.<br> * `password`: Required, string. The password of the API user.<br> * `permissions`: Required, list or raw string. The permissions for the API user. Have a look at the example and https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#icinga2-api-permissions.<br>For the usage in `host_vars`. | `[]` |
| `icinga2_master__influxdb_database_name` | The name of the InfluxDB database. | `'icinga2'` |
| `icinga2_master__influxdb_host` | The host on which the InfluxDB database is reachable. | `'localhost'` |
| `icinga2_master__influxdb_retention` | Determines how long InfluxDB should keep the Icinga2 data. If specified, it should be `INF` or at least one hour. | `'216d'` |
| `icinga2_master__service_enabled` | Enables or disables the Icinga2 service, analogous to `systemctl enable/disable --now`. | `true` |

Example:
```yaml
# optional
icinga2_master__cn: '{{ ansible_facts["nodename"] }}'
icinga2_master__database_host: 'localhost'
icinga2_master__database_name: 'icinga2_ido'
icinga2_master__api_users__group_var: []
icinga2_master__api_users__host_var:
  - username: 'ticket-user'
    password: 'linuxfabrik'
    permissions:
      - 'actions/generate-ticket'
  - username: 'downtime-user'
    password: 'linuxfabrik'
    permissions:
      - 'actions/schedule-downtime'
      - 'actions/remove-downtime'
      - 'actions/reschedule-check'
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
icinga2_master__influxdb_database_name: 'icinga2'
icinga2_master__influxdb_host: 'localhost'
icinga2_master__influxdb_retention: '216d'
icinga2_master__service_enabled: true
```

### Primary-Secondary Setup

Adjust the following variables for the secondary Icinga2 master.

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icinga2_master__additional_master_endpoints` | A list of endpoints which should be in the Icinga2 master zone. For example, the primary Icinga2 master endpoint. Subkeys: <br> * `cn`: Mandatory, string. The common name of the additional Icinga2 master. This should be equal to `icinga2_master__cn` on the additional master. <br> * `host`: Mandatory, string. The hostname or IP of the additional Icinga2 master. <br> * `port`: Optional, int. Icinga2 Port. Defaults to 5665. | `[]` |
| `icinga2_master__api_ticket_login` | The Icinga2 API user which should be used to create a ticket for CSR (certificate signing request) [auto-signing](https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#generate-ticket). The user needs to have the `actions/generate-ticket` permission. | `'{{ icinga2_master__enrolment_api_user }}'` |
| `icinga2_master__database_enable_ha` | If high availability should be enabled for the ido database or not. Have a look at https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/#high-availability-with-db-ido. | `false` |
| `icinga2_master__influxdb_enable_ha` | If high availability should be enabled for the ido database or not. Have a look at https://icinga.com/docs/icinga-2/latest/doc/14-features/#influxdb-in-cluster-ha-zones. | `false` |
| `icinga2_master__node_role` | The role of this Icinga2 node. Possible options:<br> * `primary`<br> * `secondary` | `'primary'` |
| `icinga2_master__primary_host` | The host on which the Icinga2 master is running. Needs to be reachable from the secondary node. | unset |
| `icinga2_master__primary_port` | The port on which the Icinga2 master is running. Needs to be reachable from the secondary node. | `5665` |

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
icinga2_master__database_enable_ha: false
icinga2_master__influxdb_enable_ha: false
icinga2_master__node_role: 'primary'
icinga2_master__primary_host: 'master1.example.com'
icinga2_master__primary_port: 5666
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
