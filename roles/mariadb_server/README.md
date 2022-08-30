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
* Enable the official [MariaDB Package Repository](https://mariadb.com/kb/en/mariadb-package-repository-setup-and-usage/). This can be done using the [linuxfabrik.lfops.repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb) role.
* Install the `python3-PyMySQL` library. This can be done using the [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python) role.

## Optional Requirements

* Enable the a repository for [mydumper](https://github.com/mydumper/mydumper). This can be done using the [linuxfabrik.lfops.repo_mydumper](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mydumper) role.


## Tags

| Tag                                  | What it does                                                                                                                                                                                |
| ---                                  | ------------                                                                                                                                                                                |
| `mariadb_server`                     | Installs and configures the MariaDB server                                                                                                                                                  |
| `mariadb_server:configure`           | Configures the MariaDB server (except sys_schema)                                                                                                                                           |
| `mariadb_server:database`            | Create or delete mariadb databases                                                                                                                                                          |
| `mariadb_server:dump`                | Configues dumps (backups) of the MariaDB server                                                                                                                                             |
| `mariadb_server:secure_installation` | Secures the installation the same way mysql_secure_installation does                                                                                                                        |
| `mariadb_server:state`               | Manages the state of the MariaDB service                                                                                                                                                    |
| `mariadb_server:sys_schema`          | Deploys a collection of views, functions and procedures to help MariaDB administrators get insight in to MariaDB Database usage. This does not run by default, only when explicitly called. |
| `mariadb_server:user`                | Create, update or delete MariaDB users                                                                                                                                                      |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `mariadb_server__admin_login` | The user account for the database administrator. Also have a look at `mariadb_server__admin_host`. |

Example:
```yaml
# mandatory
mariadb_server__admin_login:
  username: 'admin'
  password: 'my-secret-password'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `mariadb_server__admin_host` | todo | `['127.0.0.1', '::1', 'localhost']` |
| `mariadb_server__dump_login` | todo | unset |
| `mariadb_server__databases__host_var` /<br> `mariadb_server__databases__group_var` | todo<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `mariadb_server__users__host_var` /<br> `mariadb_server__users__group_var` | todo<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `mariadb_server__logrotate` | Log files are rotated `count` days before being removed or mailed to the address specified in a `logrotate` mail directive. If count is `0`, old versions are removed rather than rotated. If count is `-1`, old logs are not removed at all (use with caution, may waste performance and disk space). | `14` |

Example:
```yaml
# optional
mariadb_server__admin_host:
  - '127.0.0.1'
  - '::1'
  - 'localhost'
mariadb_server__dump_login:
  username: 'mariadb-backup'
  password: 'my-secret-password'
mariadb_server__databases__host_var:
  - name: 'test-db'
    collation: 'utf8_general_ci' # default
    encoding: 'utf8' # default
    state: 'present' # default
mariadb_server__databases__group_var: []
mariadb_server__users__host_var:
  - username: 'user1'
    password: 'my-secret-password' # default omit
    host: 'localhost' # default
    priv: # default omit
      - '{{ icingaweb2_db }}.*:SELECT,INSERT,UPDATE,DELETE,DROP,CREATE VIEW,INDEX,EXECUTE'
      - 'wiki.*:ALL'
    state: 'present' # default
mariadb_server__users__group_var: []
mariadb_server__logrotate: 14
```


### `mariadb_server__cnf_*` config directives

Variables for `z00-linuxfabrik.cnf` directives and their default values, defined and supported by this role.

| Role Variable                                        | Documentation                                                                                      | Default Value                    |
| -------------                                        | -------------                                                                                      | -------------                    |
| `mariadb_server__cnf_character_set_server`           | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `'utf8mb4'`                      |
| `mariadb_server__cnf_collation_server`               | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `'utf8mb4_unicode_ci'`           |
| `mariadb_server__cnf_expire_logs_days`               | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/) | `0`                              |
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


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
