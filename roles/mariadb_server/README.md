# Ansible Role mariadb_server

This role installs and configures a [MariaDB](https://mariadb.org/) server.

This role is only compatible with MariaDB versions

* 10.5
* 10.6

FQCN: linuxfabrik.lfops.mariadb_server

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Enable the official [MariaDB Package Repository](https://mariadb.com/kb/en/mariadb-package-repository-setup-and-usage/). This can be done using the [linuxfabrik.lfops.repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb) role.
* Install the `python3-PyMySQL` library. This can be done using the [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python) role.

### Optional

* repo-mydumper # TODO


## Tags

| Tag                                | What it does                                                                                                                    |
| ---                                | ------------                                                                                                                    |
| mariadb_server                     | Installs and configures the MariaDB server                                                                                      |
| mariadb_server:configure           | Configures the MariaDB server (except sys_schema)                                                                               |
| mariadb_server:database            | Create or delete mariadb databases                                                                                              |
| mariadb_server:dump                | Configues dumps (backups) of the MariaDB server                                                                                 |
| mariadb_server:secure_installation | Secures the installation the same way mysql_secure_installation does                                                            |
| mariadb_server:state               | Manages the state of the MariaDB service                                                                                        |
| mariadb_server:sys_schema          | Deploys a collection of views, functions and procedures to help MariaDB administrators get insight in to MariaDB Database usage. This does not run by default, only when explicitly called. |
| mariadb_server:user                | Create, update or delete MariaDB users                                                                                          |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/mariadb_server/defaults/main.yml) for the variable defaults.


### Mandatory

#### mariadb_server__version

The MariaDB version to install. [Have a look at the MariaDB Download Site for the list of available releases](https://mariadb.org/download/?t=mariadb&p=mariadb&os=Linux&cpu=x86_64). Also, have a look at the [MariaDB Server Releases page](https://mariadb.com/kb/en/mariadb-server-release-dates/) to check which version is a "long-term support MariaDB stable" or "short-term support MariaDB development" release.

You also have to provide the same version number in ``repo_mariadb__version`` if using ``repo_mariadb`` and therefore installing from the official MariaDB repository.

Example:
```yaml
mariadb_server__version: '10.6'
```

#### mariadb_server__admin_login

The user account for the database administrator. Also have a look at `mariadb_server__admin_host`.

Example:
```yaml
mariadb_server__admin_login:
  username: 'admin'
  password: 'my-secret-password'
```


### Optional

#### mariadb_server__admin_host

todo

Default:
```yaml
mariadb_server__admin_host:
  - '127.0.0.1'
  - '::1'
  - 'localhost'
```

#### mariadb_server__cnf_* config directives

Variables for `z00-linuxfabrik.cnf` directives and their default values, defined and supported by this role.

| Role Variable                                         | Default                           | Documentation                                                                                         |
|---------------                                        |---------                          |---------------                                                                                        |
| mariadb_server__cnf_character_set_server              | 'utf8mb4'                         | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_collation_server                  | 'utf8mb4_unicode_ci'              | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_expire_logs_days                  | 0                                 | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_innodb_buffer_pool_size           | '128M'                            | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_innodb_file_per_table             | 'ON'                              | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_innodb_flush_log_at_trx_commit    | 1                                 | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_innodb_io_capacity                | 200                               | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_innodb_log_file_size              | '96M'                             | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_join_buffer_size                  | '256K'                            | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_log_error                         | '/var/log/mariadb/mariadb.log'    | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_lower_case_table_names            | 0                                 | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_max_allowed_packet                | '16M'                             | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_max_connections                   | 64                                | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_max_heap_table_size               | '16M'                             | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_performance_schema                | 'ON'                              | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_query_cache_limit                 | '1M'                              | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_query_cache_size                  | 0                                 | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_query_cache_type                  | 'OFF'                             | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_skip_name_resolve                 | 'ON'                              | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |
| mariadb_server__cnf_tmp_table_size                    | '16M'                             | [mariadb.com](https://mariadb.com/kb/en/full-list-of-mariadb-options-system-and-status-variables/)    |


#### mariadb_server__dump_login

todo

Default: unset

Example:
```yaml
mariadb_server__dump_login:
  username: 'mariadb-backup'
  password: 'my-secret-password'
```


#### mariadb_server__logrotate

Log files are rotated `count` days before being removed or mailed to the address specified in a `logrotate` mail directive. If count is `0`, old versions are removed rather than rotated. If count is `-1`, old logs are not removed at all (use with caution, may waste performance and disk space).

Default:
```yaml
mariadb_server__logrotate: 14
```


#### mariadb_server__monitoring_login

todo

Default: unset

Example:
```yaml
mariadb_server__monitoring_login:
  username: 'mariadb-monitoring'
  password: 'my-secret-password'
```


#### mariadb_server__host_databases / mariadb_server__group_databases

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

todo

Default:
```yaml
mariadb_server__group_databases: []
mariadb_server__host_databases: []
```

Example:
```yaml
mariadb_server__host_databases:
  - name: 'test-db'
    collation: 'utf8_general_ci' # default
    encoding: 'utf8' # default
    state: 'present' # default
```


#### mariadb_server__host_users / mariadb_server__group_users

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

todo

Default:
```yaml
mariadb_server__group_users: []
mariadb_server__host_users: []
```

Example:
```yaml
mariadb_server__host_users:
  - username: 'user1'
    password: 'my-secret-password' # default omit
    host: 'localhost' # default
    priv: # default omit
      - '{{ icingaweb2_db }}.*:SELECT,INSERT,UPDATE,DELETE,DROP,CREATE VIEW,INDEX,EXECUTE'
      - 'wiki.*:ALL'
    state: 'present' # default
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
