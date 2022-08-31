# Ansible Role linuxfabrik.lfops.influxdb

This role installs and configures [InfluxDB](https://www.influxdata.com/products/influxdb-overview/).

Tested on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Install `influxdb` and `requests` into a Python 3 virtual environment in `/opt/python-venv/influxdb`. This can be done using the [linuxfabrik.lfops.python_venv](https://github.com/Linuxfabrik/lfops/tree/main/roles/python_venv) role.
* Enable the official [InfluxDB repository](https://docs.influxdata.com/influxdb/v1.8/introduction/install/?t=Red+Hat+%26amp%3B+CentOS). This can be done using the [linuxfabrik.lfops.repo_influxdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_influxdb) role.


## Tags

| Tag                 | What it does                                      |
| ---                 | ------------                                      |
| `influxdb`          | Installs and configures InfluxDB                  |
| `influxdb:database` | Creates or deletes InfluxDB databases             |
| `influxdb:dump`     | Configures dumps (backups) of the InfluxDB server |
| `influxdb:state`    | Manages the state of the InfluxDB service         |
| `influxdb:user`     | Creates, updates or deletes InfluxDB users        |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `influxdb__admin_login` | The user account for the database administrator. |

Example:
```yaml
# mandatory
influxdb__admin_login:
  username: 'influxdb-admin'
  password: 'some-secret-password'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `influxdb__dump_timer_enabled` | Enables or disables the influxdb service, analogous to `systemctl enable/disable --now`. | `true` |
| `influxdb__databases__host_var` /<br> `influxdb__databases__group_var` | List of InfluxDB databases that should be created or deleted.<br> Subkeys:<br> * `name`: Mandatory, string. Name of the database.<br> * `state`: Optional, string. Defaults to `present`. The state of the database. Possible options: `present`, `absent`.<br> * `retention`: Mandatory, string. Determines how long InfluxDB should keep the data. If specified, it should be `INF` or at least one hour.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `influxdb__users__host_var` /<br> `influxdb__users__group_var` | List of InfluxDB users that should be created, updated or deleted.<br> Subkeys:<br> * `name`: Mandatory, string. The name of the account.<br> * `password`: Mandatory, string. The password of the account.<br> * `state`: Optional, string. Defaults to `present`. The state of the account. Possible options: `present`, `absent`.<br> * `admin`: Optional, boolean. Defaults to `false`. Whether the user should be in the admin role or not.<br> * `grants`: Optional, list. Defaults to omit. Takes a list of dicts containing the `database` and `privilege` keys.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `influxdb__service_enabled` | Enables or disables the influxdb service, analogous to `systemctl enable/disable --now`. | `true` |

Example:
```yaml
# optional
influxdb__dump_timer_enabled: true
influxdb__databases__host_var:
  - name: 'database1'
    state: 'present'
    retention: '216d'
influxdb__users__host_var:
  - name: 'user1'
    password: 'some-secret-password'
    state: 'present'
    admin: false
    grants:
      - database: 'database1'
        privilege: 'ALL'
influxdb__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
