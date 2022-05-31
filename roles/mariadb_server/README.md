# Ansible Role mariadb_server

This installs and configures a [MariaDB](https://mariadb.org/) server.

FQCN: linuxfabrik.lfops.mariadb_server

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* python3-PyMySQL
* Enable the official [MariaDB Package Repository](https://mariadb.com/kb/en/mariadb-package-repository-setup-and-usage/). This can be done using the [linuxfabrik.lfops.repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb) role.
* Install the `python3-PyMySQL` library. This can be done using the [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python) role.

### Optional

* repo-mydumper # TODO


## Tags

| Tag                                | What it does                                                                                                                    |
| ---                                | ------------                                                                                                                    |
| mariadb_server                     | Installs and configures the MariaDB server                                                                                      |
| mariadb_server:configure           | Configures the MariaDB server                                                                                                   |
| mariadb_server:database            | Create or delete mariadb databases                                                                                              |
| mariadb_server:dump                | Configues dumps (backups) of the MariaDB server                                                                                 |
| mariadb_server:secure_installation | Secures the installation the same way mysql_secure_installation does                                                            |
| mariadb_server:state               | Manages the state of the MariaDB service                                                                                        |
| mariadb_server:sys_schema          | Deploys a collection of views, functions and procedures to help MariaDB administrators get insight in to MariaDB Database usage |
| mariadb_server:user                | Create, update or delete MariaDB users                                                                                          |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/mariadb_server/defaults/main.yml) for the variable defaults.


### Mandatory

#### mariadb_server__version

The MariaDB version to install.

Example:
```yaml
mariadb_server__version: 10.5
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

#### mariadb_server__dump_login

todo

Default: unset

Example:
```yaml
mariadb_server__dump_login:
  username: 'mariadb-backup'
  password: 'my-secret-password'
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
      - todo
    state: 'present' # default
```




## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
