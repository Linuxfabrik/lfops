TODO umbauen:

mariadb_server__admin_user:  # replaces mariadb_server__admin_host
  username: 'mariadb-admin'
  password: 'password'
  host:
    - 'localhost'
    - '127.0.0.1'
    - '::1'
  priv:
    - '*.*:all,grant'
  state: 'present'

mariadb_server__dump_user:  # replaces mariadb_server__dump_login, mariadb_server__dump_user_host, mariadb_server__dump_user_priv, mariadb_server__dump_user_state
  username: 'mariadb-dump'
  password: 'password'
  host:
    - 'localhost'
    - '127.0.0.1'
    - '::1'
  priv:
    - '*.*:event,lock tables,reload,select,show view,super,trigger'
  state: 'present'


Plus TODO: Alle Rollen sollten einen Systemd Start/Stop/Enable/Disable gleich behandeln. Generell mit den Variablen role__enabled und role__state arbeiten. Es gibt Unterschiede in
* Apache Tomcat <= bevorzugt für alle? Kurz testen
* Apache httpd
* MariaDB

--------------------


# Ansible Role linuxfabrik.lfops.mariadb_server

This role installs and configures a [MariaDB](https://mariadb.org/) server.

Note that this role does NOT let you specify a particular MariaDB server version. It simply installs the latest available MariaDB server version from the repos configured in the system. If you want or need to install a specific MariaDB server version, use the [linuxfabrik.lfops.repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb) beforehand.

This role is only compatible with the following MariaDB versions:

* 10.3
* 10.4
* 10.5
* 10.6 (preferred - long-term support MariaDB stable)

We will add the next long-term support release as soon as it's available (therefore currently not implementing 10.7+).

Tested on

* RHEL 8 (and compatible)


## Mandatory Requirements

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Install the `python3-PyMySQL` library. This can be done using the [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python) role.


## Optional Requirements

* Enable the official [MariaDB Package Repository](https://mariadb.com/kb/en/mariadb-package-repository-setup-and-usage/). This can be done using the [linuxfabrik.lfops.repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb) role.
* Enable the a repository for [mydumper](https://github.com/mydumper/mydumper). This can be done using the [linuxfabrik.lfops.repo_mydumper](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mydumper) role.


## Tags

| Tag                                  | What it does                                                                                                                     |
| ---                                  | ------------                                                                                                                     |
| `mariadb_server`                     | Installs and configures the MariaDB server                                                                                       |
| `mariadb_server:configure`           | Configures the MariaDB server                                                                                                    |
| `mariadb_server:database`            | Create or delete mariadb databases                                                                                               |
| `mariadb_server:dump`                | Configues dumps (backups) of the MariaDB server                                                                                  |
| `mariadb_server:secure_installation` | Secures the installation the same way mysql_secure_installation does                                                             |
| `mariadb_server:state`               | Manages the state of the MariaDB service                                                                                         |
| `mariadb_server:sys_schema`          | Deploys a collection of views, functions and procedures to help MariaDB administrators get insight in to MariaDB Database usage. |
| `mariadb_server:user`                | Create, update or delete MariaDB users                                                                                           |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `mariadb_server__admin_login` | The user account for the database administrator. Subkeys:<br>* `username`: Username<br>* `password`: Password<br>Also have a look at `mariadb_server__admin_host`. |

Example:
```yaml
# mandatory
mariadb_server__admin_login:
  username: 'admin'
  password: 'my-secret-password'
```


## Optional Role Variables - Specific to this role


| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `mariadb_server__admin_host` | Host-part(s) for creating the DBA user account after a fresh installation. | `['127.0.0.1', '::1', 'localhost']` |
| `mariadb_server__databases__host_var` / `mariadb_server__databases__group_var` | Dict of databases to create. The item keyname is used for the name of the database schema. Subkeys:<br>* `collation`: DB collation<br>* `encoding`: DB encoding<br>* `state`: `present` or `absent` | unset |
| `mariadb_server__logrotate` | Log files are rotated `count` days before being removed or mailed to the address specified in a `logrotate` mail directive. If count is `0`, old versions are removed rather than rotated. If count is `-1`, old logs are not removed at all (use with caution, may waste performance and disk space). | `14` |
| `mariadb_server__dump_login` | User to whom backup privileges are granted to. Subkeys:<br>* `username`: Username<br>* `password`: Password | unset |
| `mariadb_server__dump_mydumper_package` | Name of the "mydumper" package. Also takes an URL to GitHub if no repo server is available, for example `'https://github.com/mydumper/mydumper/releases/download/v0.12.6-1/mydumper-0.12.6-1.el8.x86_64.rpm'`. | `'mydumper'` |
mariadb_server__dump_user_host
mariadb_server__dump_user_priv
mariadb_server__dump_user_state
mariadb_server__enabled
| `mariadb_server__skip_sys_schema` | Skip the deployment of the MariaDB sys schema (a collection of views, functions and procedures to help MariaDB administrators get insight in to MariaDB Database usage). If a `sys` schema exists, it will never be overwritten.| `false` |
mariadb_server__state
| `mariadb_server__users__host_var` / `mariadb_server__users__group_var` | List of users to create. | `[]` |

Example: TODO siehe librenms
```yaml
# optional - role variables
mariadb_server__admin_host:
  - '127.0.0.1'
  - '::1'
  - 'localhost'
mariadb_server__dump_login:
  username: 'mariadb-dump'
  password: 'password'
mariadb_server__databases__host_var:
  'mydb':
    collation: 'utf8mb4_unicode_ci'
    encoding: 'utf8mb4'
    state: 'present'
mariadb_server__dump_login:
  username: 'mariadb-backup'
  password: 'my-secret-password'
mariadb_server__logrotate: 14
mariadb_server__skip_sys_schema: false
mariadb_server__users__host_var:
  - username: 'user1'
    password: 'my-secret-password' # default omit
    host: 'localhost' # default
    priv: # default omit
      - '{{ icingaweb2_db }}.*:SELECT,INSERT,UPDATE,DELETE,DROP,CREATE VIEW,INDEX,EXECUTE'
      - 'wiki.*:ALL'
    state: 'present' # default
```


## Optional Role Variables - `mariadb_server__cnf_*` Config Directives

Variables for `z00-linuxfabrik.cnf` directives and their default values, defined and supported by this role.

| Role Variable                                        | Documentation                                                                                      | Default Value (v10.6)                    |
| -------------                                        | -------------                                                                                      | -------------                    |
| `mariadb_server__cnf_character_set_server`           | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `'utf8mb4'`                      |
| `mariadb_server__cnf_collation_server`               | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `'utf8mb4_unicode_ci'`           |
| `mariadb_server__cnf_expire_logs_days`               | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `0.000000`                              |
| `mariadb_server__cnf_innodb_buffer_pool_size`        | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `'128M'`                         |
| `mariadb_server__cnf_innodb_file_per_table`          | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `'ON'`                           |
| `mariadb_server__cnf_innodb_flush_log_at_trx_commit` | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `1`                              |
| `mariadb_server__cnf_innodb_io_capacity`             | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `200`                            |
| `mariadb_server__cnf_innodb_log_file_size`           | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `'96M'`                          |
| `mariadb_server__cnf_join_buffer_size`               | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `'256K'`                         |
| `mariadb_server__cnf_log_error`                      | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `'/var/log/mariadb/mariadb.log'` |
| `mariadb_server__cnf_lower_case_table_names`         | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `0`                              |
| `mariadb_server__cnf_max_allowed_packet`             | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `'16M'`                          |
| `mariadb_server__cnf_max_connections`                | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `64`                             |
| `mariadb_server__cnf_max_heap_table_size`            | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `'16M'`                          |
| `mariadb_server__cnf_performance_schema`             | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `'ON'`                           |
| `mariadb_server__cnf_query_cache_limit`              | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `'1M'`                           |
| `mariadb_server__cnf_query_cache_size`               | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `0`                              |
| `mariadb_server__cnf_query_cache_type`               | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `'OFF'`                          |
| `mariadb_server__cnf_skip_name_resolve`              | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `'ON'`                           |
| `mariadb_server__cnf_tmp_table_size`                 | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `'16M'`                          |

Example:
```yaml
# optional - cnf directives
mariadb_server__cnf_character_set_server__host_var: 'utf8mb4'
mariadb_server__cnf_collation_server__host_var: 'utf8mb4_unicode_ci'
mariadb_server__cnf_expire_logs_days__host_var: 0.000000
mariadb_server__cnf_innodb_buffer_pool_size__host_var: '128M'
mariadb_server__cnf_innodb_file_per_table__host_var: 'ON'
mariadb_server__cnf_innodb_flush_log_at_trx_commit__host_var: 1
mariadb_server__cnf_innodb_io_capacity__host_var: 200
mariadb_server__cnf_innodb_log_file_size__host_var: '96M'
mariadb_server__cnf_join_buffer_size__host_var: '256K'
mariadb_server__cnf_log_error__host_var: '/var/log/mariadb/mariadb.log'
mariadb_server__cnf_lower_case_table_names__host_var: 0
mariadb_server__cnf_max_allowed_packet__host_var: '16M'
mariadb_server__cnf_max_connections__host_var: 64
mariadb_server__cnf_max_heap_table_size__host_var: '16M'
mariadb_server__cnf_performance_schema__host_var: 'ON'
mariadb_server__cnf_query_cache_limit__host_var: '1M'
mariadb_server__cnf_query_cache_size__host_var: 0
mariadb_server__cnf_query_cache_type__host_var: 'OFF'
mariadb_server__cnf_skip_name_resolve__host_var: 'ON'
mariadb_server__cnf_tmp_table_size__host_var: '16M'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
