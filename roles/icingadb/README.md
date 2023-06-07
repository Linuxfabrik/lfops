# Ansible Role linuxfabrik.lfops.icingadb

This role installs and configures [IcingaDB](https://github.com/Icinga/icingadb).

When running the `icingadb:migration` tag, it also tries to prepare the configuration file required for the migration from the IDO feature to Icinga DB. Note that the migration requires the following manual steps after running the role:
1. Double check the values in `/tmp/icingadb-migration.yml`
2. Run the migration: `icingadb-migrate --config /tmp/icingadb-migration.yml --cache /tmp/icingadb-migration.cache`
3. Clean up: `rmdir /tmp/icingadb-migration.cache`
4. If everything works, disable the IcingaWeb2 monitoring module: `icingacli module disable monitoring`

Notes on high availability / Icinga2 Master clusters:
* Redis: "High availability setups require a dedicated Redis server per Icinga 2 node and therefore a dedicated Icinga DB instance that connects to it."
* SQL database: "In high availability setups, all Icinga DB instances must write to the same database."
* Have a look at the [official documentation](https://icinga.com/docs/icinga-db/latest/doc/03-Configuration/) and this [community thread](https://community.icinga.com/t/missed-ha-instructions-for-icinga-2-12rc/3939).

Runs on

* RHEL 8 (and compatible)


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
| `icingadb__api_user_login` | The account for accessing the Icinga2 API. |
| `icingadb__database_login` | The user account for accessing the IcingaDB SQL database. Currently, only MySQL is supported. |

Example:
```yaml
# mandatory
icingadb__api_user_login:
  username: 'icingadb-api-user'
  password: 'linuxfabrik'
icingadb__database_login:
  username: 'icingadb'
  password: 'linuxfabrik'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icingadb__api_host` | The host on which the Icinga2 API is reachable. | `'localhost'` |
| `icingadb__api_port` | The port on which the Icinga2 API is reachable. | `5665` |
| `icingadb__database_host` | The host on which the IcingaDB SQL database is reachable. | `127.0.0.1` |
| `icingadb__database_login_host` | The Host-part of the SQL database user. | `127.0.0.1` |
| `icingadb__database_name` | The name of the IcingaDB SQL database. | `'icingadb'` |
| `icingadb__redis_host` | The host on which Redis instance is reachable. | `'127.0.0.1'` |
| `icingadb__redis_password` | The password for the Redis instance, if authentication is enabled. | unset |
| `icingadb__redis_port` | The port on which Redis instance is reachable. | `6379` |
| `icingadb__service_enabled` | Enables or disables the IcingaDB service, analogous to `systemctl enable/disable --now`. | `true` |

Example:
```yaml
# optional
icingadb__api_host: 'localhost'
icingadb__api_port: 5665
icingadb__database_host: '127.0.0.1'
icingadb__database_login_host: 'localhost'
icingadb__database_name: 'icingadb'
icingadb__redis_host: '127.0.0.1'
icingadb__redis_password: 'linuxfabrik'
icingadb__redis_port: 6379
icingadb__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
