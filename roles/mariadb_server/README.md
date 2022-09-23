# Ansible Role linuxfabrik.lfops.mariadb_server

This role installs and configures a [MariaDB](https://mariadb.org/) server.

It also tunes the following Kernel settings:
* `fs.aio-max-nr`: `1048576`
* `vm.swapiness`: `10`

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

* For some machines you might need to set `ansible_python_interpreter: '/usr/bin/python3'` to prevent the error message `A MySQL module is required: for Python 2.7 either PyMySQL, or MySQL-python, or for Python 3.X mysqlclient or PyMySQL. Consider setting ansible_python_interpreter to use the intended Python version.`.
* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Install the `python3-PyMySQL` library. This can be done using the [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python) role.


## Optional Requirements

* Enable the official [MariaDB Package Repository](https://mariadb.com/kb/en/mariadb-package-repository-setup-and-usage/). This can be done using the [linuxfabrik.lfops.repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb) role.
* Enable the a repository for [mydumper](https://github.com/mydumper/mydumper). This can be done using the [linuxfabrik.lfops.repo_mydumper](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mydumper) role.


## Tags

| Tag                                  | What it does                                                                                                                     |
| ---                                  | ------------                                                                                                                     |
| `mariadb_server`                     | * `dnf -y install mariadb-server libzstd`<br> * Get the list of installed packages<br> * Get mariadb-server version<br> * Load default values for {{ mariadb_server__installed_version }}<br> * `mkdir /var/log/mariadb`<br> * `touch /var/log/mariadb/mariadb.log; chown mysql:mysql /var/log/mariadb/mariadb.log`<br> * Deploy /etc/my.cnf.d/z00-linuxfabrik.cnf<br> * `mkdir -p /etc/systemd/system/mariadb.service.d/`<br> * Deploy /etc/systemd/system/mariadb.service.d/socket-selinux-workaround.conf<br> * `systemctl daemon-reload`<br> * Deploy /etc/logrotate.d/mariadb<br> * `systemctl {{ mariadb_server__enabled \| bool \| ternary("enable", "disable") }} mariadb.service`<br> * `systemctl {{ mariadb_server__state[:-2] }} mariadb.service`<br> * Create DBA "{{ mariadb_server__admin_user["username"] }}"<br> * Remove all "root" users<br> * Secure installation: Remove anonymous users<br> * Secure installation: Remove test database<br> * Secure installation: Remove test database (privileges)<br> * Secure installation: Reload privilege tables<br> * `dnf -y install {{ mariadb_server__dump_mydumper_package }}`<br> * Deploy /usr/local/bin/mariadb-dump<br> * Deploy /etc/mariadb-dump.conf<br> * Grant backup privileges on dbs.tables to {{ mariadb_server__dump_user["username"] }}@localhost<br> * Deploy /etc/systemd/system/mariadb-dump.service<br> * Deploy /etc/systemd/system/mariadb-dump.timer<br> * `systemctl enable mariadb-dump.timer --now`<br> * Create or delete mariadb databases<br> * Create, update or delete MariaDB users<br> * Show databases<br> * `wget https://github.com/FromDual/mariadb-sys/archive/refs/heads/master.tar.gz`<br> * `mkdir /tmp/mariadb-sys-schema`<br> * `tar xzvf /tmp/mariadb-sys-schema.tar.gz`<br> * `mysql --user "{{ mariadb_server__admin_user["username"] }}" --password="..." < ./sys_10.sql`<br> * `rm -rf /tmp/mariadb-sys-schema` |
| `mariadb_server:configure`           | * `dnf -y install mariadb-server libzstd`<br> * Get the list of installed packages<br> * Get mariadb-server version<br> * Load default values for {{ mariadb_server__installed_version }}<br> * `mkdir /var/log/mariadb`<br> * `touch /var/log/mariadb/mariadb.log; chown mysql:mysql /var/log/mariadb/mariadb.log`<br> * Deploy /etc/my.cnf.d/z00-linuxfabrik.cnf<br> * `mkdir -p /etc/systemd/system/mariadb.service.d/<br> * Deploy /etc/systemd/system/mariadb.service.d/socket-selinux-workaround.conf<br> * `systemctl daemon-reload`<br> * Deploy /etc/logrotate.d/mariadb`<br> * `systemctl {{ mariadb_server__enabled \| bool \| ternary("enable", "disable") }} mariadb.service`<br> * `systemctl {{ mariadb_server__state[:-2] }} mariadb.service`<br> * `dnf -y install {{ mariadb_server__dump_mydumper_package }}`<br> * Deploy /usr/local/bin/mariadb-dump<br> * Deploy /etc/mariadb-dump.conf<br> * Grant backup privileges on dbs.tables to {{ mariadb_server__dump_user["username"] }}@localhost<br> * Deploy /etc/systemd/system/mariadb-dump.service<br> * Deploy /etc/systemd/system/mariadb-dump.timer<br> * `systemctl enable mariadb-dump.timer --now` |
| `mariadb_server:database`            | * Get the list of installed packages<br> * Get mariadb-server version<br> * Load default values for {{ mariadb_server__installed_version }}<br> * Create or delete mariadb databases |
| `mariadb_server:dump`                | * Get the list of installed packages<br> * Get mariadb-server version<br> * Load default values for {{ mariadb_server__installed_version }}<br> * `dnf -y install {{ mariadb_server__dump_mydumper_package }}`<br> * Deploy /usr/local/bin/mariadb-dump<br> * Deploy /etc/mariadb-dump.conf<br> * Grant backup privileges on dbs.tables to {{ mariadb_server__dump_user["username"] }}@localhost<br> * Deploy /etc/systemd/system/mariadb-dump.service<br> * Deploy /etc/systemd/system/mariadb-dump.timer<br> * `systemctl enable mariadb-dump.timer --now` |
| `mariadb_server:secure_installation` | * Get the list of installed packages<br> * Get mariadb-server version<br> * Load default values for {{ mariadb_server__installed_version }}<br> * Remove all "root" users<br> * Secure installation: Remove anonymous users<br> * Secure installation: Remove test database<br> * Secure installation: Remove test database (privileges)<br> * Secure installation: Reload privilege tables |
| `mariadb_server:state`               | * Get the list of installed packages<br> * Get mariadb-server version<br> * Load default values for {{ mariadb_server__installed_version }}<br> * `systemctl {{ mariadb_server__enabled \| bool \| ternary("enable", "disable") }} mariadb.service`<br> * `systemctl {{ mariadb_server__state[:-2] }} mariadb.service` |
| `mariadb_server:sys_schema`          | * Get the list of installed packages<br> * Get mariadb-server version<br> * Load default values for {{ mariadb_server__installed_version }}<br> * Show databases<br> * `wget https://github.com/FromDual/mariadb-sys/archive/refs/heads/master.tar.gz`<br> * `mkdir /tmp/mariadb-sys-schema`<br> * `tar xzvf /tmp/mariadb-sys-schema.tar.gz`<br> * `mysql --user "{{ mariadb_server__admin_user["username"] }}" --password="..." < ./sys_10.sql`<br> * `rm -rf /tmp/mariadb-sys-schema` |
| `mariadb_server:user`                | * Get the list of installed packages<br> * Get mariadb-server version<br> * Load default values for {{ mariadb_server__installed_version }}<br> * `mkdir /var/log/mariadb`<br> * `touch /var/log/mariadb/mariadb.log; chown mysql:mysql /var/log/mariadb/mariadb.log`<br> * Create DBA "{{ mariadb_server__admin_user["username"] }}"<br> * Create, update or delete MariaDB users |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `mariadb_server__admin_user` | The main user account for the database administrator. To create additional ones, use the `mariadb_server__users__*` variables. Subkeys:<br> * `username`: Username<br> * `password`: Password<br> * `host`: Optional, list. Defaults to `["localhost", "127.0.0.1", "::1"]`. Host-part(s). |

Example:
```yaml
# mandatory
mariadb_server__admin_user:
  username: 'mariadb-admin'
  password: 'linuxfabrik'
```


## Optional Role Variables - Specific to this role


| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `mariadb_server__admin_host` | Host-part(s) for creating the DBA user account after a fresh installation. | `['127.0.0.1', '::1', 'localhost']` |
| `mariadb_server__databases__host_var` / `mariadb_server__databases__group_var` | List of dictionaries of databases to create. Subkeys:<br> * `name`: Required, string. Name of the databse schema. <br> * `collation`: DB collation<br> * `encoding`: DB encoding<br> * `state`: `present` or `absent` <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `mariadb_server__dump_directory` | Dump output directory name. | `'/backup/mariadb-dump'`|
| `mariadb_server__dump_mydumper_package` | Name of the "mydumper" package. Also takes an URL to GitHub if no repo server is available, see the example below. | `'mydumper'` |
| `mariadb_server__dump_on_calendar` | The `OnCalendar` definition for the systemd timer. Have a look at `man systemd.time(7)` for the format. | `'*-*-* 21:{{ 59 | random(start=0, seed=inventory_hostname) }}:00'`|
| `mariadb_server__dump_threads` | The number of threads to use for dumping data. | `4`|
| `mariadb_server__dump_user` | User to whom backup privileges are granted to. Subkeys:<br> * `username`: Username<br> * `password`: Password<br> * `priv`: Optional, list. Defaults to `["*.*:event,lock tables,reload,select,show view,super,trigger"]`. User privileges.<br> * `state`: Optional, string. Defaults to `'present'`. Possible Options:<br> * `'present'`<br> * `'absent'` | unset |
| `mariadb_server__enabled`| Enables or disables the Systemd unit. | `true` |
| `mariadb_server__logrotate` | Number. Log files are rotated `count` days before being removed or mailed to the address specified in a `logrotate` mail directive. If count is `0`, old versions are removed rather than rotated. If count is `-1`, old logs are not removed at all (use with caution, may waste performance and disk space). | `{{ logrotate__rotate \| d(14) }}` |
| `mariadb_server__skip_sys_schema` | Skip the deployment of the MariaDB sys schema (a collection of views, functions and procedures to help MariaDB administrators get insight in to MariaDB Database usage). If a `sys` schema exists, it will never be overwritten.| `false` |
| `mariadb_server__state`| Controls the Systemd service. One of<br> * `started`<br> * `stopped`<br> * `reloaded` | `'started'` |
| `mariadb_server__users__host_var` / `mariadb_server__users__group_var` | List of dictionaries of users to create (this is NOT used for the first DBA user - here, use `mariadb_server__admin_user`). Subkeys:<br> * `username`: Required, String. Username. <br> * `host`: Required, String. Host. <br> * `password`<br> * `priv`<br> * `state`<br> For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |

```yaml
# optional - role variables
mariadb_server__admin_host:
  - '127.0.0.1'
  - '::1'
  - 'localhost'
mariadb_server__databases__host_var:
  - name: 'mydb'
    collation: 'utf8mb4_unicode_ci'
    encoding: 'utf8mb4'
    state: 'present'
mariadb_server__dump_directory: '/backup/mariadb-dump'
mariadb_server__dump_mydumper_package: 'https://github.com/mydumper/mydumper/releases/download/v0.12.6-1/mydumper-0.12.6-1.el8.x86_64.rpm'
mariadb_server__dump_on_calendar: '*-*-* 21:{{ 59 | random(start=0, seed=inventory_hostname) }}:00'
mariadb_server__dump_threads: 4
mariadb_server__dump_user:
  username: 'mariadb-dump'
  password: 'password'
  priv:
    - '*.*:event,lock tables,reload,select,show view,super,trigger'
  state: 'present'
mariadb_server__enabled: true
mariadb_server__logrotate: 7
mariadb_server__skip_sys_schema: false
mariadb_server__state: 'started'
mariadb_server__users__host_var:
  - username: 'user1'
    host: 'localhost'
    password: 'linuxfabrik'
    priv:
      - '{{ icingaweb2_db }}.*:SELECT,INSERT,UPDATE,DELETE,DROP,CREATE VIEW,INDEX,EXECUTE'
      - 'wiki.*:ALL'
    state: 'present'
  - username: 'mariadb-dump'
    host: '127.0.0.1'
    password: 'linuxfabrik'
    priv:
      - '*.*:event,lock tables,reload,select,show view,super,trigger'
    state: 'present'
```


## Optional Role Variables - `mariadb_server__cnf_*` Config Directives

Variables for `z00-linuxfabrik.cnf` directives and their default values, defined and supported by this role.

| Role Variable                                        | Documentation                                                                                      | Default Value (v10.6)                    |
| -------------                                        | -------------                                                                                      | -------------                    |
| `mariadb_server__cnf_character_set_server__group_var` / `mariadb_server__cnf_character_set_server__host_var`           | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#character_set_server) | `'utf8mb4'`                      |
| `mariadb_server__cnf_collation_server__group_var` / `mariadb_server__cnf_collation_server__host_var`               | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#collation_server) | `'utf8mb4_unicode_ci'`           |
| `mariadb_server__cnf_expire_logs_days__group_var` / `mariadb_server__cnf_expire_logs_days__host_var`               | [mariadb.com](https://mariadb.com/kb/en/replication-and-binary-log-system-variables/#expire_logs_days) | `0.000000`                              |
| `mariadb_server__cnf_innodb_buffer_pool_size__group_var` / `mariadb_server__cnf_innodb_buffer_pool_size__host_var`        | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_buffer_pool_size) | `'128M'`                         |
| `mariadb_server__cnf_innodb_file_per_table__group_var` / `mariadb_server__cnf_innodb_file_per_table__host_var`          | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_file_per_table) | `'ON'`                           |
| `mariadb_server__cnf_innodb_flush_log_at_trx_commit__group_var` / `mariadb_server__cnf_innodb_flush_log_at_trx_commit__host_var` | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_flush_log_at_trx_commit) | `1`                              |
| `mariadb_server__cnf_innodb_io_capacity__group_var` / `mariadb_server__cnf_innodb_io_capacity__host_var`             | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_io_capacity) | `200`                            |
| `mariadb_server__cnf_innodb_log_file_size__group_var` / `mariadb_server__cnf_innodb_log_file_size__host_var`           | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_log_file_size) | `'96M'`                          |
| `mariadb_server__cnf_join_buffer_size__group_var` / `mariadb_server__cnf_join_buffer_size__host_var`               | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#join_buffer_size) | `'256K'`                         |
| `mariadb_server__cnf_log_error__group_var` / `mariadb_server__cnf_log_error__host_var`                      | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#log_error) | `'/var/log/mariadb/mariadb.log'` |
| `mariadb_server__cnf_lower_case_table_names__group_var` / `mariadb_server__cnf_lower_case_table_names__host_var`         | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#lower_case_table_names) | `0`                              |
| `mariadb_server__cnf_max_allowed_packet__group_var` / `mariadb_server__cnf_max_allowed_packet__host_var`             | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#max_allowed_packet) | `'16M'`                          |
| `mariadb_server__cnf_max_connections__group_var` / `mariadb_server__cnf_max_connections__host_var`                | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#max_connections) | `64`                             |
| `mariadb_server__cnf_max_heap_table_size__group_var` / `mariadb_server__cnf_max_heap_table_size__host_var`            | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#max_heap_table_size) | `'16M'`                          |
| `mariadb_server__cnf_performance_schema__group_var` / `mariadb_server__cnf_performance_schema__host_var`             | [mariadb.com](https://mariadb.com/kb/en/performance-schema-system-variables/#performance_schema) | `'ON'`                           |
| `mariadb_server__cnf_query_cache_limit__group_var` / `mariadb_server__cnf_query_cache_limit__host_var`              | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#query_cache_limit) | `'1M'`                           |
| `mariadb_server__cnf_query_cache_size__group_var` / `mariadb_server__cnf_query_cache_size__host_var`               | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#query_cache_size) | `0`                              |
| `mariadb_server__cnf_query_cache_type__group_var` / `mariadb_server__cnf_query_cache_type__host_var`               | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#query_cache_type) | `'OFF'`                          |
| `mariadb_server__cnf_skip_name_resolve__group_var` / `mariadb_server__cnf_skip_name_resolve__host_var`              | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#skip_name_resolve) | `'ON'`                           |
| `mariadb_server__cnf_tmp_table_size__group_var` / `mariadb_server__cnf_tmp_table_size__host_var`                 | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#tmp_table_size) | `'16M'`                          |

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
