# Ansible Role linuxfabrik.lfops.icingadb_web

[IcingaDB](https://icinga.com/docs/icinga-db/latest/doc/01-About/) consists of multiple components. This role only installs [IcingaDB Web](https://icinga.com/docs/icinga-db-web). Generally, the [IcingaDB daemon](https://github.com/Icinga/icingadb) is also required, use the [linuxfabrik.lfops.icingadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingadb) role for that. Run the linuxfabrik.lfops.icingadb role first to initialise the database.


## Mandatory Requirements

* A configured Icinga2 Master Setup. This can be done using the [linuxfabrik.lfops.setup_icinga2_master](https://github.com/linuxfabrik/lfops/tree/main/playbooks/setup_icinga2_master.yml) playbook.


## Tags

| Tag            | What it does                          |
| ---            | ------------                          |
| `icingadb_web` | Installs and configures IcingaDB Web. |


## Mandatory Role Variables

| Variable                       | Description                                |
| --------                       | -----------                                |
| `icingadb_web__api_user_login` | The account for accessing the Icinga2 API. |

Example:
```yaml
# mandatory
icingadb_web__api_user_login:
  username: 'icingadb-api-user'
  password: 'linuxfabrik'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icingadb_web__api_host` | The host on which the Icinga2 API is reachable. | `'localhost'` |
| `icingadb_web__api_port` | The port on which the Icinga2 API is reachable. | `5665` |
| `icingadb_web__database_host` | The host on which the IcingaDB SQL database is reachable. | `'{{ icingadb__database_host }}'` |
| `icingadb_web__database_login` | The user account for accessing the IcingaDB SQL database. Currently, only MySQL is supported. | `'{{ icingadb__database_login }}'` |
| `icingadb_web__database_name` | The name of the IcingaDB SQL database. | `'{{ icingadb__database_name }}'` |
| `icingadb_web__redis_host` | The host on which Redis instance is reachable. | `'{{ icingadb__redis_host }}'` |
| `icingadb_web__redis_password` | The password for the Redis instance, if authentication is enabled. | `'{{ icingadb__redis_password | d() }}'` |
| `icingadb_web__redis_port` | The port on which Redis instance is reachable. | `'{{ icingadb__redis_port }}'` |
| `icingadb_web__plugin_output_character_limit` | Number. Sets the maximum number of characters to display in plugin output. | `20000` |

Example:
```yaml
# optional
icingadb_web__api_host: 'localhost'
icingadb_web__api_port: 5665
icingadb_web__database_host: '127.0.0.1'
icingadb_web__database_login:
  username: 'icingadb'
  password: 'linuxfabrik'
icingadb_web__database_name: 'icingadb'
icingadb_web__plugin_output_character_limit: 20000
icingadb_web__redis_host: '127.0.0.1'
icingadb_web__redis_password: 'linuxfabrik'
icingadb_web__redis_port: 6379
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
