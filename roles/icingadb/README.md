# Ansible Role linuxfabrik.lfops.icingadb

[IcingaDB](https://icinga.com/docs/icinga-db/latest/doc/01-About/) consists of multiple components. This role only installs the [IcingaDB daemon](https://github.com/Icinga/icingadb). Generally, [IcingaDB Web](https://icinga.com/docs/icinga-db-web) is also required, use the [linuxfabrik.lfops.icingadb_web](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingadb_web) role for that.

When running the `icingadb:migration` tag, the role tries to prepare the configuration file required for the migration from the old IDO feature to Icinga DB. Note that the migration requires the following manual steps after running the role:
1. Double check the values in `/tmp/icingadb-migration.yml`
2. Run the migration: `icingadb-migrate --config /tmp/icingadb-migration.yml --cache /tmp/icingadb-migration.cache`
3. Clean up: `rm -rf /tmp/icingadb-migration.cache /tmp/icingadb-migration.yml`
4. If everything works, disable the old IcingaWeb2 monitoring module: `icingacli module disable monitoring`
Also have a look at https://icinga.com/docs/icinga-db-web/latest/doc/10-Migration/ for other migration steps.

Notes on high availability / Icinga2 Master clusters:
* Redis: "Each of the master nodes must have the Icinga DB feature enabled and have their own dedicated Redis server set up for it."
* SQL database: "Icinga DB instances must write to the same database, which of course can be replicated or a cluster."
* Environment ID: Make sure that `/var/lib/icinga2/icingadb.env` is the same on all master nodes.
* "Although Icinga DB can run anywhere in an Icinga environment, we recommend to install it where the corresponding Icinga 2 node and Redis server is running to keep latency between the components low."
* Have a look at the [official documentation](https://icinga.com/docs/icinga-db/latest/doc/05-Distributed-Setups/).


## Mandatory Requirements

* A configured Icinga2 Master Setup. This can be done using the [linuxfabrik.lfops.setup_icinga2_master](https://github.com/linuxfabrik/lfops/tree/main/playbooks/setup_icinga2_master.yml) playbook.


## Tags

| Tag        | What it does                                 |
| ---        | ------------                                 |
| `icingadb` | Installs and configures IcingaDB. |
| `icingadb:migration` | Not normally run. Prepares the migration of the history from the IDO feature to Icinga DB. |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `icingadb__database_login` | The user account for accessing the IcingaDB SQL database. Currently, only MySQL is supported. |

Example:
```yaml
# mandatory
icingadb__database_login:
  username: 'icingadb'
  password: 'linuxfabrik'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icingadb__database_host` | The host on which the IcingaDB SQL database is reachable. | `127.0.0.1` |
| `icingadb__database_login_host` | The Host-part of the SQL database user. | `127.0.0.1` |
| `icingadb__database_name` | The name of the IcingaDB SQL database. | `'icingadb'` |
| `icingadb__logging_level` | The loglevel of IcingaDB. One of` 'fatal'`, `'error'`, `'warn'`, `'info'` or `'debug'`. | `'info'` |
| `icingadb__redis_host` | The host on which Redis instance is reachable. | `'127.0.0.1'` |
| `icingadb__redis_password` | The password for the Redis instance, if authentication is enabled. | unset |
| `icingadb__redis_port` | The port on which Redis instance is reachable. | `6379` |
| `icingadb__retention_history_days` | Number of days to retain full historical data. By default, historical data is retained forever. | unset |
| `icingadb__service_enabled` | Enables or disables the IcingaDB service, analogous to `systemctl enable/disable --now`. | `true` |

Example:
```yaml
# optional
icingadb__database_host: '127.0.0.1'
icingadb__database_login_host: 'localhost'
icingadb__database_name: 'icingadb'
icingadb__logging_level: 'debug'
icingadb__redis_host: '127.0.0.1'
icingadb__redis_password: 'linuxfabrik'
icingadb__redis_port: 6379
icingadb__retention_history_days: 360
icingadb__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
