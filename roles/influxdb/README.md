# Ansible Role influxdb

This role installs and configures [InfluxDB](https://www.influxdata.com/products/influxdb-overview/).

FQCN: linuxfabrik.lfops.influxdb

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* Install `influxdb` and `requests` into a Python 3 virtual environment in `/opt/python-venv/influxdb`. This can be done using the [linuxfabrik.lfops.python_venv](https://github.com/Linuxfabrik/lfops/tree/main/roles/python_venv) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag               | What it does                                      |
| ---               | ------------                                      |
| influxdb          | Installs and configures InfluxDB                  |
| influxdb:database | Creates or deletes InfluxDB databases             |
| influxdb:dump     | Configures dumps (backups) of the InfluxDB server |
| influxdb:state    | Manages the state of the InfluxDB service         |
| influxdb:user     | Creates, updates or deletes InfluxDB users        |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/influxdb/defaults/main.yml) for the variable defaults.


### Mandatory


#### influxdb__admin_login

The user account for the database administrator.

Subkeys:

* `username`: Mandatory, string. The admin username.
* `password`: Mandatory, string. The admin password.

Example:
```yaml
influxdb__admin_login:
  username: 'influxdb-admin'
  password: 'some-secret-password'
```


### Optional

#### influxdb__databases

List of InfluxDB databases that should be created or deleted.

Subkeys:

* `name`: Mandatory, string. Name of the database.
* `state`: Optional, string. Defaults to `present`. The state of the database. Possible options: `present`, `absent`.
* `retention`: Mandatory, string. Determines how long InfluxDB should keep the data. If specified, it should be `INF` or at least one hour.

Example:
```yaml
influxdb_databases:
  - name: 'database1'
    state: 'present'
    retention: '216d'
```


#### influxdb__users

List of InfluxDB users that should be created, updated or deleted.

Subkeys:

* `name`: Mandatory, string. The name of the account.
* `password`: Mandatory, string. The password of the account.
* `state`: Optional, string. Defaults to `present`. The state of the account. Possible options: `present`, `absent`.
* `admin`: Optional, boolean. Defaults to `false`. Whether the user should be in the admin role or not.
* `grants`: Optional, list. Defaults to omit. Takes a list of dicts containing the `database` and `privilege` keys.

Example:
```yaml
influxdb_users:
  - name: 'user1'
    password: 'some-secret-password'
    state: 'present'
    admin: false
    grants:
      - database: 'database1'
        privilege: 'ALL'
```


#### influxdb__dump_timer_enabled

Enables or disables the named service, analogous to `systemctl enable/disable --now`. Possible options:

* true
* false

Default:
```yaml
influxdb__dump_timer_enabled: true
```


#### influxdb__service_enabled

Enables or disables the named service, analogous to `systemctl enable/disable --now`. Possible options:

* true
* false

Default:
```yaml
influxdb__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
