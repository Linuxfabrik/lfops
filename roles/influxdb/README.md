# Ansible Role linuxfabrik.lfops.influxdb

This role installs and configures [InfluxDB](https://www.influxdata.com/products/influxdb-overview/).

Runs on

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
  password: 'linuxfabrik'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `influxdb__conf_continuous_queries_log_enabled` | Controls whether queries are logged when executed by the continuous query service. Make sure to also set `influxdb__conf_logging_level: 'debug'` if this is enabled. | `false` |
| `influxdb__conf_continuous_queries_run_interval` | Interval for how often continuous queries will be checked if they need to run. | `'1s'` |
| `influxdb__conf_https` | Determines whether HTTPS is enabled or not. Also have a look at `influxdb__validate_certs`. Subkeys: <ul><li>`certificate_path`: Mandatory, string. The path of the certificate file used for SSL encryption.</li><li>`privatekey_path`: Mandatory, string. The path of the certificate key file used for SSL encryption.</li></ul> | unset |
| `influxdb__conf_log_queries_after` | The time threshold when a query will be logged as a slow query. Setting the value to 0 disables the slow query logging. | `'0s'` |
| `influxdb__conf_logging_level` | Determines which level of logs will be emitted. Possible options: `'error'`, `'warn'`, `'info'`, `'debug'`. | `'warn'` |
| `influxdb__dump_timer_enabled` | Enables or disables the influxdb service, analogous to `systemctl enable/disable --now`. | `true` |
| `influxdb__databases__host_var` /<br> `influxdb__databases__group_var` | List of InfluxDB databases that should be created or deleted.<br> Subkeys:<br> * `name`: Mandatory, string. Name of the database.<br> * `state`: Optional, string. Defaults to `present`. The state of the database. Possible options: `present`, `absent`.<br> * `retention`: Mandatory, string. Determines how long InfluxDB should keep the data. If specified, it should be `INF` or at least one hour.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `influxdb__users__host_var` /<br> `influxdb__users__group_var` | List of InfluxDB users that should be created, updated or deleted.<br> Subkeys:<br> * `name`: Mandatory, string. The name of the account.<br> * `password`: Mandatory, string. The password of the account.<br> * `state`: Optional, string. Defaults to `present`. The state of the account. Possible options: `present`, `absent`.<br> * `admin`: Optional, boolean. Defaults to `false`. Whether the user should be in the admin role or not.<br> * `grants`: Optional, list. Defaults to omit. Takes a list of dicts containing the `database` and `privilege` keys.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `influxdb__service_enabled` | Enables or disables the influxdb service, analogous to `systemctl enable/disable --now`. | `true` |
| `influxdb__validate_certs` | If set to `false`, the role will not validate SSL certificates when connecting to InfluxDB. This is useful when using self-signed certificates. | `true` |

Example:
```yaml
# optional
influxdb__conf_continuous_queries_log_enabled: true
influxdb__conf_continuous_queries_run_interval: '1s'
influxdb__conf_https:
  certificate_path: '/etc/ssl/ssl-certificate.crt'
  private_key_path: '/etc/ssl/ssl-certificate.key'
influxdb__conf_log_queries_after: '0s'
influxdb__conf_logging_level: 'warn'
influxdb__dump_timer_enabled: true
influxdb__databases__host_var:
  - name: 'database1'
    state: 'present'
    retention: '216d'
influxdb__users__host_var:
  - name: 'user1'
    password: 'linuxfabrik'
    state: 'present'
    admin: false
    grants:
      - database: 'database1'
        privilege: 'ALL'
influxdb__service_enabled: true
influxdb__validate_certs: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
