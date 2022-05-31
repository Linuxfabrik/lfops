# Ansible Role icinga2_master

This role installs and configures [Icinga2](https://icinga.com/docs/icinga-2/latest/doc/01-about/) as a monitoring master.

FQCN: linuxfabrik.lfops.icinga2_master

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* Install InfluxDB, and create a database and a user for said database. This can be done using the [linuxfabrik.lfops.influxdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/influxdb) role.
* Install MariaDB, and create a database and a user for said database. This can be done using the [linuxfabrik.lfops.influxdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/influxdb) role.
* Install `tar`. This can be done using the [linuxfabrik.lfops.tar](https://github.com/Linuxfabrik/lfops/tree/main/roles/tar) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag                      | What it does                                |
| ---                      | ------------                                |
| icinga2_master           | Installs and configures Icinga2 as a master |
| icinga2_master:api_users | Manages the Icinga2 API users               |
| icinga2_master:state     | Manages the state of the Icinga2 service    |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/icinga2_master/defaults/main.yml) for the variable defaults.


### Mandatory


#### icinga2_master__database_login

The user account for accessing the icinga2 ido database. Currently, only MySQL is supported.

Example:
```yaml
icinga2_master__database_login:
  username: ''
  password: ''
```


#### icinga2_master__influxdb_login

The user account for accessing the icinga2 InfluxDB database.

Example:
```yaml
icinga2_master__influxdb_login:
  username: ''
  password: ''
```


### Optional

#### icinga2_master__api_users

A list of dictionaries for the icinga2 API users.

Subkeys:

* `username`: Required, string. The username of the API user.
* `password`: Required, string. The password of the API user.
* `permissions`: Requried, list or raw string. The permissions for the API user. Have a look at the example and https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#icinga2-api-permissions.


Default:
```yaml
icinga2_master__api_users: []
```

Example:
```yaml
icinga2_master__api_users:

  - username: 'ticket-user'
    password: 'password'
    permissions:
      - 'actions/generate-ticket'

  - username: 'downtime-user'
    password: 'password'
    permissions:
      - 'actions/schedule-downtime'
      - 'actions/remove-downtime'
      - 'actions/reschedule-check'

  - username: 'check-logfile-windows-api-user'
    password: 'password'
    permissions: |-
      [
      {% raw %}
        {
          permission = "objects/query/Service"
          filter = {{ regex("^check-logfile-windows-api-user", service.vars.logfile_windows_icinga_username ) }}
        }
      {% endraw %}
      ]
```


#### icinga2_master__cn

The common name of the Icinga2 master. Tries to default to the FQDN of the server.

Default:
```yaml
icinga2_master__cn: '{{ ansible_facts["nodename"] }}'
```


#### icinga2_master__database_host

The host on which the ido database is reachable.

Default:
```yaml
icinga2_master__database_host: 'localhost'
```


#### icinga2_master__database_name

The name of the ido database.

Default:
```yaml
icinga2_master__database_name: 'icinga2_ido'
```


#### icinga2_master__influxdb_host

The host on which the InfluxDB database is reachable.

Default:
```yaml
icinga2_master__influxdb_host: 'localhost'
```


#### icinga2_master__influxdb_database_name

The name of the InfluxDB database.

Default:
```yaml
icinga2_master__influxdb_database_name: 'icinga2'
```


#### icinga2_master__influxdb_retention

Determines how long InfluxDB should keep the Icinga2 data. If specified, it should be `INF` or at least one hour.

Default:
```yaml
icinga2_master__influxdb_retention: '216d'
```

#### icinga2_master__service_enabled

Enables or disables the Icinga2 service, analogous to `systemctl enable/disable --now`. Possible options:

* true
* false

Default:
```yaml
icinga2_master__service_enabled: true
```


### Primary-Secondary Setup

Adjust the following variables for the secondary Icinga2 master.

#### icinga2_master__node_role

The role of this Icinga2 node. Possible options:

* primary
* secondary

Default:
```yaml
icinga2_master__node_role: 'primary'
```


#### icinga2_master__additional_master_endpoints

A list of endpoints which should be in the Icinga2 master zone. For example, the primary Icinga2 master endpoint.

Default:
```yaml
icinga2_master__additional_master_endpoints: []
```

Example:
```yaml
icinga2_master__additional_master_endpoints:
  - 'master1.example.com'
```


#### icinga2_master__primary_host

The host on which the Icinga2 master is running. Needs to be reachable from the secondary node.

Default:
```yaml
icinga2_master__primary_host: unset
```


#### icinga2_master__primary_port

The port on which the Icinga2 master is running. Needs to be reachable from the secondary node.

Default:
```yaml
icinga2_master__primary_port: unset
```


#### icinga2_master__api_ticket_login

The Icinga2 API user which should be used to create a ticket for CSR (certificate signing request) auto-signing (https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#generate-ticket). The user needs to have the `actions/generate-ticket` permission.

Default: unset

Example:
```yaml
icinga2_master__api_ticket_login:
  password: 'ticket-user'
  password: 'my-secret-password'
```


#### icinga2_master__database_enable_ha

If high availability should be enabled for the ido database or not. Have a look at https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/#high-availability-with-db-ido.

Default:
```yaml
icinga2_master__database_enable_ha: false
```


#### icinga2_master__influxdb_enable_ha

If high availability should be enabled for the ido database or not. Have a look at https://icinga.com/docs/icinga-2/latest/doc/14-features/#influxdb-in-cluster-ha-zones.

Default:
```yaml
icinga2_master__influxdb_enable_ha: false
```



## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
