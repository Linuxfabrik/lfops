# Ansible Role linuxfabrik.lfops.mariadb_server

This role installs and configures a [MariaDB](https://mariadb.org/) server.

It also tunes the following Kernel settings:

* `fs.aio-max-nr = 1048576`
* `sunrpc.tcp_slot_table_entries = 128`
* `vm.swapiness = 10`

Note that this role does NOT let you specify a particular MariaDB server version. It simply installs the latest available MariaDB server version from the repos configured in the system. If you want or need to install a specific MariaDB server version, use the [linuxfabrik.lfops.repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb) beforehand.

This role is compatible with the following MariaDB versions:

* 10.5
* 10.6 LTS
* 10.11 LTS
* 11.4 LTS

The role provides the `mariadb_server:upgrade` tag to update the MariaDB server. The tag upgrades to the newest available version, therefore make sure to switch the module stream or update the repository (optionally using the [linuxfabrik.lfops.repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb) role).

By default, Ansible runs each task on all hosts affected by a play before starting the next task on any host, using 5 forks. This role manages one MariaDB host at a time (serially), e.g. to make cluster management as reliable and save as possible.

Hardenings that can be covered by this role: See [STIGs](https://github.com/Linuxfabrik/lfops/blob/main/STIGs.md)


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
| `mariadb_server`                     | * Install mariadb-server<br> * Optionally install galera-4 and rsync<br> * Plus all of the tags below, except `mariadb_server:galera_new_cluster` and `mariadb_server:upgrade` |
| `mariadb_server:clone_datadir`       | * If the current `datadir` directory (dir1) on the MariaDB server is different from the one in the Ansible inventory (dir2), copy dir1 to dir2 and configure MariaDB accordingly. MariaDB must be up and running to perform this task. For disaster recovery purposes, you will need to remove dir1 yourself. |
| `mariadb_server:configure`           | * Deploy MariaDB server configuration file<br> * Deploy MariaDB logrotate configuration file<br> * Enable/Disable `mariadb.service`<br> * Install mydumper/myloader<br> * Grant backup privileges on dbs.tables<br> * Deploy `mariadb-dump.service`<br> * Enable `mariadb-dump.timer` |
| `mariadb_server:dare`                | * Deploys the keyfile for the [File Key Management Encryption Plugin](https://mariadb.com/kb/en/file-key-management-encryption-plugin/) and restarts MariaDB if ncecessary. |
| `mariadb_server:database`            | * Create or delete mariadb databases |
| `mariadb_server:dump`                | * Install mydumper/myloader<br> * Grant backup privileges on dbs.tables<br> * Deploy `mariadb-dump.service`<br> * Enable `mariadb-dump.timer`  |
| `mariadb_server:galera_new_cluster`  | * Runs `galera_new_cluster`, but only if `mariadb_server__run_galera_new_cluster` is true. Use in combination with `--extra-vars='{"mariadb_server__run_galera_new_cluster": true}'` |
| `mariadb_server:secure_installation` | * Remove all "root" users<br> * Run `mariadb-secure-installation`<br> * Apply some universal CIS hardenings |
| `mariadb_server:state`               | * Enable/Disable `mariadb.service`  |
| `mariadb_server:sys_schema`          | * Install sys schema from https://github.com/FromDual/mariadb-sys/archive/refs/heads/master.tar.gz |
| `mariadb_server:upgrade`             | * Remove old mariadb-server package<br> * Install latest mariadb-server<br> * Update mariadb-client, mariadb-common, mariadb-shared on Red Hat<br> * Deploy MariaDB server configuration file<br> * Deploy MariaDB logrotate configuration file<br> * Enable/Disable `mariadb.service`<br> * Run `mysql_upgrade`<br> * Must be explicitly called |
| `mariadb_server:user`                | * Create DBA<br> * Create, update or delete MariaDB users |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `mariadb_server__admin_user` | The main user account for the database administrator. To create additional ones, use the `mariadb_server__users__*` variables. Subkeys: <ul><li>`username`: Mandatory, string. Username.</li><li>`password`: Mandatory, string. Password</li><li>`host`: Optional, list. Defaults to `["localhost", "127.0.0.1", "::1"]`. Host-part(s).</li><li>`old_password`: String, optional. The old password. Set this when changing the password.</li><li>`plugin`: String, optional. Authentication plugin to use for the admin user (e.g. `mysql_native_password`, `unix_socket`).</li></ul> |

Example:
```yaml
# mandatory
mariadb_server__admin_user:
  username: 'mariadb-admin'
  password: 'linuxfabrik'
  plugin: 'unix_socket'  # optional, e.g. for socket authentication
  # old_password: 'previous-linuxfabrik'
```


## Recommended Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `mariadb_server__dump_user` | String. For mydumper: User to whom backup privileges are granted to. Setting this user automatically enables daily MariaDB-Dumps. Subkeys:<br> * `username`: Username<br> * `password`: Password<br> * `priv`: Optional, list. Defaults to `["*.*:event,lock tables,reload,select,show view,super,trigger"]`. User privileges.<br> * `state`: Optional, string. Defaults to `'present'`. Possible Options: `'present'`, `'absent'` | unset |

Example:
```yaml
# recommended
mariadb_server__dump_user:
  username: 'mariadb-backup'
  password: 'linuxfabrik'
  state: 'present'
```


## Optional Role Variables - Specific to this role

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `mariadb_server__databases__host_var` / `mariadb_server__databases__group_var` | List of dictionaries of databases to create. Subkeys:<br> * `name`: Mandatory, string. Name of the databse schema. <br> * `collation`: DB collation<br> * `encoding`: DB encoding<br> * `state`: `present` or `absent` <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `mariadb_server__datadir_mode__host_var` / `mariadb_server__datadir_mode__group_var` | Octal. Mode (permissions) of the MariaDB `datadir`. Use `0o750` for CIS, but make sure that the socket is not inside the datadir in that case, else other users (eg apache) cannot reach it. | `0o755` |
| `mariadb_server__dump_compress` | String/Bool. For mydumper: Compress output files. One of `''` or `false` (no compression, extremely fast), `'ZSTD'` or `'GZIP'` (both very slow). | `''` (no compression) |
| `mariadb_server__dump_directory` | String. For mydumper: Dump output directory name. | `'/backup/mariadb-dump'`|
| `mariadb_server__dump_long_query_guard` | Integer. For mydumper: Set long query timer in seconds. | `60` |
| `mariadb_server__dump_mydumper_package` | String. For mydumper: Name of the "mydumper" package. Also takes an URL to GitHub if no repo server is available, see the example below. | `'mydumper'` |
| `mariadb_server__dump_on_calendar` | String. For mydumper: The `OnCalendar` definition for the systemd timer. Have a look at `man systemd.time(7)` for the format. | `'*-*-* 21:{{ 59 \| random(start=0, seed=inventory_hostname) }}:00'`|
| `mariadb_server__dump_raw` | String. For mydumper: Any additional parameters you want to add. | `''` |
| `mariadb_server__dump_threads` | Integer. For mydumper: The number of threads to use for dumping data. `0` means to use number of CPUs. | `0`|
| `mariadb_server__enabled`| Enables or disables the Systemd unit. | `true` |
| `mariadb_server__logrotate` | Integer. Log files are rotated `count` days before being removed or mailed to the address specified in a `logrotate` mail directive. If count is `0`, old versions are removed rather than rotated. If count is `-1`, old logs are not removed at all (use with caution, may waste performance and disk space). | `{{ logrotate__rotate \| d(14) }}` |
| `mariadb_server__roles__group_var` / `mariadb_server__roles__host_var` | List of dictionaries of MariaDB roles. Subkeys: <ul><li>`name`: Mandatory, string. Role name.</li><li>`priv`: Mandatory, list of dicts. List of privileges for the role.</li><li>`state`: Optional, string. Possible Options: `'present'`, `'absent'`. Defaults to `'present'`. </li></ul><br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `mariadb_server__service_limit_memlock` | Integer. Systemd: LimitMEMLOCK setting. | `524288` |
| `mariadb_server__service_limit_nofile` | Integer. Systemd: Resource limit directive for the number of file descriptors. | `32768` |
| `mariadb_server__service_timeout_start_sec` | String. Systemd: Configures the time to wait for start-up. If the MariaDB server does not signal start-up completion within the configured time, the service will be considered failed and will be shut down again. | `'15min'` |
| `mariadb_server__service_timeout_stop_sec` | String. Systemd: First, it configures the time to wait for the ExecStop= command. Second, it configures the time to wait for the MariaDB server itself to stop. If the MariaDB server doesn't terminate in the specified time, it will be forcibly terminated by SIGKILL. | `'15min'` |
| `mariadb_server__skip_sys_schema` | Skip the deployment of the MariaDB sys schema (a collection of views, functions and procedures to help MariaDB administrators get insight in to MariaDB Database usage). If a `sys` schema exists, it will never be overwritten.| `false` |
| `mariadb_server__state`| Controls the Systemd service. One of<br> * `started`<br> * `stopped`<br> * `reloaded` | `'started'` |
| `mariadb_server__users__host_var` / `mariadb_server__users__group_var` | List of dictionaries of users to create (this is NOT used for the first DBA user - use `mariadb_server__admin_user` for that). Subkeys: <ul><li>`username`: Mandatory, string. Username.</li><li>`host`: Optional, string. Host-part. Defaults to `'localhost'`.</li><li>`password`: Optional, string. Password. Defaults to unset.</li><li>`plugin`: Optional, string. Plugin to authenticate the user with. Defaults to unset.</li><li>`tls_requires`: Optional, dict. Specify for client TLS auth. Have a look at the example. Defaults to unset.</li><li>`priv`: Optional, list of dicts. List of privileges for the user. Defaults to unset. Note: Never set to `[]`, the least privileges are `['*.*:USAGE']`.</li><li>`roles`: Optional, list. List of roles. Defaults to `[]`.</li><li>`default_role`: Optional, string. Default role for the user, will be activated upon login. Defaults to unset.</li><li>`state`: Optional, string. Possible Options: `'present'`, `'absent'`. Defaults to `'present'`. </li></ul><br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |


Example:
```yaml
# optional - role variables
mariadb_server__databases__host_var:
  - name: 'mydb'
    collation: 'utf8mb4_unicode_ci'
    encoding: 'utf8mb4'
    state: 'present'
mariadb_server__datadir_mode__host_var: 0o750
mariadb_server__dump_compress: 'GZIP'
mariadb_server__dump_directory: '/backup/mariadb-dump'
mariadb_server__dump_long_query_guard: 60
mariadb_server__dump_mydumper_package: 'https://github.com/mydumper/mydumper/releases/download/v0.12.6-1/mydumper-0.12.6-1.el8.x86_64.rpm'
mariadb_server__dump_on_calendar: '*-*-* 21:{{ 59 | random(start=0, seed=inventory_hostname) }}:00'
mariadb_server__dump_raw: ''
mariadb_server__dump_threads: 4
mariadb_server__enabled: true
mariadb_server__logrotate: 7
mariadb_server__roles__host_var:
  - name: 'dba'
    priv:
      - '*.*:ALL'
    state: 'present'
  - name: 'read_only'
    priv:
      - '*.*:SELECT'
    state: 'present'
mariadb_server__service_limit_memlock: 524288
mariadb_server__service_limit_nofile: 32768
mariadb_server__service_timeout_start_sec: '15min'
mariadb_server__service_timeout_stop_sec: '15min'
mariadb_server__skip_sys_schema: false
mariadb_server__state: 'started'
mariadb_server__users__host_var:
  - username: 'user1'
    host: 'localhost'
    password: 'linuxfabrik'
    priv:
      - '{{ icingaweb2_db }}.*:create view,delete,drop,execute,index,insert,select,update'
      - 'wiki.*:ALL'
    state: 'present'

  # user with client TLS auth
  - username: 'admin1'
    host: 'localhost'
    tls_requires:
      subject: '/CN=admin1' # Note: Make sure to include the CN in the SAN of the certificate.
    priv:
      - '*.*:ALL'
    state: 'present'
  # user with `unix_socket` auth
  - username: 'mariadb_admin'
    host: 'localhost'
    plugin: 'unix_socket'
    state: 'present'
  # user with roles
  - username: 'user2'
    password: 'linuxfabrik'
    roles:
      - 'dba'
      - 'read_only'
    default_role: 'read_only'
    state: 'present'
```


## Optional Role Variables - `mariadb_server__cnf_*` Config Directives

Variables for `z00-linuxfabrik.cnf` directives and their default values, defined and supported by this role.

| Role Variable                                        | Documentation                                                                                      | Default Value                    |
| -------------                                        | -------------                                                                                      | -------------                    |
| `mariadb_server__cnf_bind_address__group_var` / `mariadb_server__cnf_bind_address__host_var` | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#bind_address) | `''` |
| `mariadb_server__cnf_binlog_format__group_var` / `mariadb_server__cnf_binlog_format__host_var` | [mariadb.com](https://mariadb.com/kb/en/replication-and-binary-log-system-variables/#binlog_format) | `'MIXED'` |
| `mariadb_server__cnf_bulk_insert_buffer_size__group_var` / `mariadb_server__cnf_bulk_insert_buffer_size__host_var`                 | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#bulk_insert_buffer_size) | `8M`                          |
| `mariadb_server__cnf_character_set_server__group_var` / `mariadb_server__cnf_character_set_server__host_var`           | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#character_set_server) | 10.11-: `'utf8mb4'`, 11.1+: `'uca1400'`                      |
| `mariadb_server__cnf_collation_server__group_var` / `mariadb_server__cnf_collation_server__host_var`               | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#collation_server) | 10.11-: `'utf8mb4_unicode_ci'`, 11.1+: `'utf8mb3=utf8mb3_uca1400_ai_ci,ucs2=ucs2_uca1400_ai_ci,utf8mb4=utf8mb4_uca1400_ai_ci,utf16=utf16_uca1400_ai_ci,utf32=utf32_uca1400_ai_ci'`           |
| `mariadb_server__cnf_datadir__group_var` / `mariadb_server__cnf_datadir__host_var` | String. [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#datadir) | `'/var/lib/mysql/'` |
| `mariadb_server__cnf_default_storage_engine__group_var` / `mariadb_server__cnf_default_storage_engine__host_var` | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#default_storage_engine) | `'InnoDB'` |
| `mariadb_server__cnf_expire_logs_days__group_var` / `mariadb_server__cnf_expire_logs_days__host_var`               | [mariadb.com](https://mariadb.com/kb/en/replication-and-binary-log-system-variables/#expire_logs_days) | `0.000000`                              |
| `mariadb_server__cnf_extra_max_connections__group_var` / `mariadb_server__cnf_extra_max_connections__host_var` | [mariadb.com](https://mariadb.com/kb/en/thread-pool-system-status-variables/#extra_max_connections) | `3` |
| `mariadb_server__cnf_extra_port__group_var` / `mariadb_server__cnf_extra_port__host_var` | [mariadb.com](https://mariadb.com/kb/en/thread-pool-system-status-variables/#extra_port) | `3307` |
| `mariadb_server__cnf_general_log__group_var` / `mariadb_server__cnf_general_log__host_var` | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#general_log) | `'OFF'` |
| `mariadb_server__cnf_general_log_file__group_var` / `mariadb_server__cnf_general_log_file__host_var` | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#general_log_file) | `'/var/log/mariadb/mariadb-general.log'` |
| `mariadb_server__cnf_innodb_autoinc_lock_mode__group_var` / `mariadb_server__cnf_innodb_autoinc_lock_mode__host_var` | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_autoinc_lock_mode) | `1` |
| `mariadb_server__cnf_innodb_buffer_pool_chunk_size__group_var` / `mariadb_server__cnf_innodb_buffer_pool_chunk_size__host_var` | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_buffer_pool_chunk_size) | 10.08-: `'128M'`, 10.8+: `0` (autosize) |
| `mariadb_server__cnf_innodb_buffer_pool_size__group_var` / `mariadb_server__cnf_innodb_buffer_pool_size__host_var`        | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_buffer_pool_size) | `'128M'`                         |
| `mariadb_server__cnf_innodb_doublewrite__group_var` / `mariadb_server__cnf_innodb_doublewrite__host_var` | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_doublewrite) | `ON` |
| `mariadb_server__cnf_innodb_file_per_table__group_var` / `mariadb_server__cnf_innodb_file_per_table__host_var`          | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_file_per_table) | `'ON'` (Deprecated: MariaDB 11.0.1 )                           |
| `mariadb_server__cnf_innodb_flush_log_at_trx_commit__group_var` / `mariadb_server__cnf_innodb_flush_log_at_trx_commit__host_var` | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_flush_log_at_trx_commit) | `1`                              |
| `mariadb_server__cnf_innodb_io_capacity__group_var` / `mariadb_server__cnf_innodb_io_capacity__host_var`             | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_io_capacity) | `200`                            |
| `mariadb_server__cnf_innodb_log_file_size__group_var` / `mariadb_server__cnf_innodb_log_file_size__host_var`           | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_log_file_size) | `'32M'`                          |
| `mariadb_server__cnf_interactive_timeout__group_var` / `mariadb_server__cnf_interactive_timeout__host_var`                 | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#interactive_timeout) | `28800`                          |
| `mariadb_server__cnf_join_buffer_size__group_var` / `mariadb_server__cnf_join_buffer_size__host_var`               | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#join_buffer_size) | `'256K'`                         |
| `mariadb_server__cnf_log_bin__group_var` / `mariadb_server__cnf_log_bin__host_var`                      | [mariadb.com](https://mariadb.com/kb/en/replication-and-binary-log-system-variables/#log_bin). Attention: the variable is *not* a boolean! Instead it either requires a string to enable it, or has to be unset. For convenience this role unsets the variable if it is set to `'OFF'`. | `''` |
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
| `mariadb_server__cnf_slow_query_log__group_var` / `mariadb_server__cnf_slow_query_log__host_var` | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#slow_query_log) | `'OFF'` |
| `mariadb_server__cnf_slow_query_log_file__group_var` / `mariadb_server__cnf_slow_query_log_file__host_var` | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#slow_query_log_file) | `'/var/log/mariadb/mariadb-slowquery.log'` |
| `mariadb_server__cnf_socket__group_var` / `mariadb_server__cnf_socket__host_var` | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#socket) | RHEL: `'/run/mariadb/mariadb.sock'`, Debian: `'/run/mysqld/mysqld.sock'` |
| `mariadb_server__cnf_sql_mode__group_var` / `mariadb_server__cnf_sql_mode__host_var` | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#sql_mode) | `'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'` |
| `mariadb_server__cnf_table_definition_cache__group_var` / `mariadb_server__cnf_table_definition_cache__host_var`                 | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#table_definition_cache) | 400
| `mariadb_server__cnf_tls_version__group_var` / `mariadb_server__cnf_tls_version__host_var`                 | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#tls_version) | `'TLSv1.2,TLSv1.3'`                          |
| `mariadb_server__cnf_tmp_table_size__group_var` / `mariadb_server__cnf_tmp_table_size__host_var`                 | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#tmp_table_size) | `'16M'`                          |
| `mariadb_server__cnf_wait_timeout__group_var` / `mariadb_server__cnf_wait_timeout__host_var`                 | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#wait_timeout) | `28800`                          |

Example:
```yaml
# optional - cnf directives
mariadb_server__cnf_bind_address__host_var: '0.0.0.0'
mariadb_server__cnf_binlog_format__host_var: 'MIXED'
mariadb_server__cnf_bulk_insert_buffer_size__host_var: '8M'
mariadb_server__cnf_character_set_server__host_var: 'utf8mb4'
mariadb_server__cnf_collation_server__host_var: 'utf8mb4_unicode_ci'
mariadb_server__cnf_datadir__host_var: '/data/mariadb'
mariadb_server__cnf_default_storage_engine__host_var: 'InnoDB'
mariadb_server__cnf_expire_logs_days__host_var: 0.000000
mariadb_server__cnf_extra_max_connections__host_var: 10
mariadb_server__cnf_extra_port__host_var: 3308
mariadb_server__cnf_general_log__host_var: 'OFF'
mariadb_server__cnf_general_log_file__host_var: '/var/log/mariadb/mariadb-general.log'
mariadb_server__cnf_innodb_autoinc_lock_mode__host_var: 2
mariadb_server__cnf_innodb_buffer_pool_chunk_size__host_var: '{{ (mariadb_server__cnf_innodb_buffer_pool_size__host_var / 64 ) | int }}'
mariadb_server__cnf_innodb_buffer_pool_size__host_var: '{{ (ansible_facts["memtotal_mb"] * 0.8) | int }}M'
mariadb_server__cnf_innodb_doublewrite__host_var: 1
mariadb_server__cnf_innodb_file_per_table__host_var: 'ON'
mariadb_server__cnf_innodb_flush_log_at_trx_commit__host_var: 1
mariadb_server__cnf_innodb_io_capacity__host_var: 200
mariadb_server__cnf_innodb_log_file_size__host_var: '96M'
mariadb_server__cnf_interactive_timeout__host_var: 28800
mariadb_server__cnf_join_buffer_size__host_var: '256K'
mariadb_server__cnf_log_bin__host_var: 'log_bin'
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
mariadb_server__cnf_slow_query_log__host_var: 'OFF'
mariadb_server__cnf_slow_query_log_file__host_var: '/var/log/mariadb/mariadb-slowquery.log'
mariadb_server__cnf_socket__host_var: '/var/run/mariadb/mariadb.sock' # use /var/run instead of /run to avoid collisions with selinux fcontexts (`File spec /run/mariadb/mariadb\.sock conflicts with equivalency rule '/run /var/run'`)
mariadb_server__cnf_sql_mode__host_var: 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'
mariadb_server__cnf_table_definition_cache__host_var: 400
mariadb_server__cnf_tls_version__host_var: 'TLSv1.2,TLSv1.3'
mariadb_server__cnf_tmp_table_size__host_var: '16M'
mariadb_server__cnf_wait_timeout__host_var: 28800
```


## Optional Role Variables - `mariadb_server__cnf_*` Config Directives for SSL/TLS

This are a several options and system variables related to [SSL/TLS Connections](https://mariadb.com/kb/en/securing-connections-for-client-and-server).

Variables for `z00-linuxfabrik.cnf` directives and their default values, defined and supported by this role for SSL/TLS.

| Role Variable | Documentation | Default Value |
| ------------- | ------------- | ------------- |
| `mariadb_server__cnf_client_ssl_ca__group_var` / `mariadb_server__cnf_client_ssl_ca__host_var` | Client configuration. Path to the SSL CA file. Will be used to verify the server cert.          | `'{{ mariadb_server__cnf_ssl_ca__combined_var }}'` |
| `mariadb_server__cnf_client_ssl_cert__group_var` / `mariadb_server__cnf_client_ssl_cert__host_var` | Client configuration. Path to an SSL cert that will be used to authenticate against the server. | `''` |
| `mariadb_server__cnf_client_ssl_key__group_var` / `mariadb_server__cnf_client_ssl_key__host_var` | Client configuration. Path to an SSL key that will be used to authenticate against the server.  | `''` |
| `mariadb_server__cnf_client_ssl_verify_server_cert__group_var` / `mariadb_server__cnf_client_ssl_verify_server_cert__host_var` | Boolean. Client configuration. Enables/disables verification of the server cert. | 10.11-: `false`, 11.4+: `true` |
| `mariadb_server__cnf_require_secure_transport__group_var` / `mariadb_server__cnf_require_secure_transport__host_var` | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#require_secure_transport) | `'OFF'` |
| `mariadb_server__cnf_ssl_ca__group_var` / `mariadb_server__cnf_ssl_ca__host_var` | [mariadb.com](https://mariadb.com/kb/en/ssltls-system-variables/#ssl_ca). Note: the CA should be world-readable (e.g. so that both the server & client can access it). | `''` |
| `mariadb_server__cnf_ssl_cert__group_var` / `mariadb_server__cnf_ssl_cert__host_var` | [mariadb.com](https://mariadb.com/kb/en/ssltls-system-variables/#ssl_cert). Note: the role changes the owner to `mysql` to make sure that mariadb can read the file. | `''` |
| `mariadb_server__cnf_ssl_key__group_var` / `mariadb_server__cnf_ssl_key__host_var` | [mariadb.com](https://mariadb.com/kb/en/ssltls-system-variables/#ssl_key). Note: the role changes the owner to `mysql` to make sure that mariadb can read the file. | `''` |

Example:
```yaml
# optional - SSL/TLS directives
mariadb_server__cnf_client_ssl_ca__host_var: '/etc/pki/tls/certs/ca.crt'
mariadb_server__cnf_client_ssl_cert__host_var: '/etc/pki/tls/certs/admin1.crt'
mariadb_server__cnf_client_ssl_key__host_var: '/etc/pki/tls/private/admin1.key'
mariadb_server__cnf_client_ssl_verify_server_cert__host_var: true
mariadb_server__cnf_require_secure_transport__host_var: 'ON'
mariadb_server__cnf_ssl_ca__host_var: '/etc/pki/tls/certs/ca.crt'
mariadb_server__cnf_ssl_cert__host_var: '/etc/pki/tls/certs/mariadb-server.crt'
mariadb_server__cnf_ssl_key__host_var: '/etc/pki/tls/private/mariadb-server.key'
```


## Optional Role Variables - `mariadb_server__cnf_*` Config Directives for DARE

To enable [Data Encryption at rest](https://mariadb.com/kb/en/data-at-rest-encryption-overview/) (DARE) using the [File Key Management plugin](https://mariadb.com/kb/en/file-key-management-encryption-plugin), you have to [define the DARE keys](https://mariadb.com/kb/en/file-key-management-encryption-plugin/#creating-the-key-file) in your inventory like so (every encryption key itself needs to be provided in hex-encoded form using 128-bit/16-byte/32 chars, 192-bit/24-byte/48 chars or 256-bit/32-byte/64 chars):

```yaml
# using 256-bit/32-byte/64 chars encryption keys
mariadb_server__dare_keys:
  - key_id: 1
    key: 'a7addd9adea9978fda19f21e6be987880e68ac92632ca052e5bb42b1a506939a'
  - key_id: 2
    key: '49c16acc2dffe616710c9ba9a10b94944a737de1beccb52dc1560abfdd67388b'
  - key_id: 100
    key: '8db1ee74580e7e93ab8cf157f02656d356c2f437d548d5bf16bf2a56932954a3'
```

Variables for `z00-linuxfabrik.cnf` directives and their default values, defined and supported by this role for DARE.

| Role Variable                                        | Documentation                                                                                      | Default Value                   |
| -------------                                        | -------------                                                                                      | -------------                    |
| `mariadb_server__cnf_encrypt_binlog__group_var` / `mariadb_server__cnf_encrypt_binlog__host_var` | [mariadb.com](https://mariadb.com/kb/en/replication-and-binary-log-server-system-variables/#encrypt_binlog) | `'ON'` |
| `mariadb_server__cnf_encrypt_tmp_files__group_var` / `mariadb_server__cnf_encrypt_tmp_files__host_var` | [mariadb.com](https://mariadb.com/kb/en/server-system-variables/#encrypt_tmp_files) | `'ON'` |
| `mariadb_server__cnf_file_key_management_encryption_algorithm__group_var` / `mariadb_server__cnf_file_key_management_encryption_algorithm__host_var` | [mariadb.com](https://mariadb.com/kb/en/file-key-management-encryption-plugin#file_key_management_encryption_algorithm) | `'AES_CTR'` |
| `mariadb_server__cnf_file_key_management_filename__group_var` / `mariadb_server__cnf_file_key_management_filename__host_var` | [mariadb.com](https://mariadb.com/kb/en/file-key-management-encryption-plugin#file_key_management_filename) | `'/etc/my.cnf.d/keyfile'` |
| `mariadb_server__cnf_innodb_default_encryption_key_id__group_var` / `mariadb_server__cnf_innodb_default_encryption_key_id__host_var` | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_default_encryption_key_id) | `1` |
| `mariadb_server__cnf_innodb_encrypt_log__group_var` / `mariadb_server__cnf_innodb_encrypt_log__host_var` | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_encrypt_log) | `'ON'` |
| `mariadb_server__cnf_innodb_encrypt_tables__group_var` / `mariadb_server__cnf_innodb_encrypt_tables__host_var` | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_encrypt_tables) | `'ON'` |
| `mariadb_server__cnf_innodb_encrypt_temporary_tables__group_var` / `mariadb_server__cnf_innodb_encrypt_temporary_tables__host_var` | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_encrypt_temporary_tables) | `'ON'` |
| `mariadb_server__cnf_innodb_encryption_rotate_key_age__group_var` / `mariadb_server__cnf_innodb_encryption_rotate_key_age__host_var` | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_encryption_rotate_key_age) | `1` |
| `mariadb_server__cnf_innodb_encryption_threads__group_var` / `mariadb_server__cnf_innodb_encryption_threads__host_var` | [mariadb.com](https://mariadb.com/kb/en/innodb-system-variables/#innodb_encryption_threads) | `4` |
| `mariadb_server__cnf_plugin_load_add__group_var` / `mariadb_server__cnf_plugin_load_add__host_var` | [mariadb.com](https://mariadb.com/docs/server/ref/mdb/cli/mariadbd/plugin-load-add/) | `'file_key_management'` |

Example:
```yaml
# optional - DARE directives
mariadb_server__cnf_encrypt_binlog__host_var: 'ON'
mariadb_server__cnf_encrypt_tmp_files__host_var: 'ON'
mariadb_server__cnf_file_key_management_encryption_algorithm__host_var: 'AES_CTR'
mariadb_server__cnf_file_key_management_filename__host_var: '/etc/my.cnf.d/keyfile'
mariadb_server__cnf_innodb_default_encryption_key_id__host_var: 1
mariadb_server__cnf_innodb_encrypt_log__host_var: 'ON'
mariadb_server__cnf_innodb_encrypt_tables__host_var: 'ON'
mariadb_server__cnf_innodb_encrypt_temporary_tables__host_var: 'ON'
mariadb_server__cnf_innodb_encryption_rotate_key_age__host_var: 1
mariadb_server__cnf_innodb_encryption_threads__host_var: 4
mariadb_server__cnf_plugin_load_add__host_var: 'file_key_management'
```


## Optional Role Variables - `mariadb_server__cnf_*` Config Directives for MariaDB Audit Plugin

This are a several options and system variables related to the [MariaDB Audit Plugin](https://mariadb.com/kb/en/server_audit-mariadb-audit-plugin/).

`server_audit` is set to `FORCE_PLUS_PERMANENT`, which always enables the plugin. If the plugin cannot be initialized, then the server will fail to start with an error. In addition, the plugin cannot be uninstalled with `UNINSTALL SONAME` or `UNINSTALL PLUGIN` while the server is running.

| Role Variable   | Documentation   | Default Value   |
| -------------   | -------------   | -------------   |
| `mariadb_server__cnf_server_audit_events` | [mariadb.com](https://mariadb.com/kb/en/mariadb-audit-plugin-options-and-system-variables/#server_audit_events) | `'CONNECT,QUERY_DDL'` |
| `mariadb_server__cnf_server_audit_excl_users` | [mariadb.com](https://mariadb.com/kb/en/mariadb-audit-plugin-options-and-system-variables/#server_audit_excl_users) | `''` |
| `mariadb_server__cnf_server_audit_file_path` | [mariadb.com](https://mariadb.com/kb/en/mariadb-audit-plugin-options-and-system-variables/#server_audit_file_path) | `'/var/log/mariadb/server_audit.log'` |
| `mariadb_server__cnf_server_audit_file_rotate_now` | [mariadb.com](https://mariadb.com/kb/en/mariadb-audit-plugin-options-and-system-variables/#server_audit_file_rotate_now) | `'OFF'` |
| `mariadb_server__cnf_server_audit_file_rotate_size` | [mariadb.com](https://mariadb.com/kb/en/mariadb-audit-plugin-options-and-system-variables/#server_audit_file_rotate_size) | `'10M'` |
| `mariadb_server__cnf_server_audit_file_rotations` | [mariadb.com](https://mariadb.com/kb/en/mariadb-audit-plugin-options-and-system-variables/#server_audit_file_rotations) | `9` |
| `mariadb_server__cnf_server_audit_incl_users` | [mariadb.com](https://mariadb.com/kb/en/mariadb-audit-plugin-options-and-system-variables/#server_audit_incl_users) | `''` |
| `mariadb_server__cnf_server_audit_logging` | [mariadb.com](https://mariadb.com/kb/en/mariadb-audit-plugin-options-and-system-variables/#server_audit_logging) | `'ON'` |
| `mariadb_server__cnf_server_audit_output_type` | [mariadb.com](https://mariadb.com/kb/en/mariadb-audit-plugin-options-and-system-variables/#server_audit_output_type) | `'file'` |
| `mariadb_server__cnf_server_audit_query_log_limit` | [mariadb.com](https://mariadb.com/kb/en/mariadb-audit-plugin-options-and-system-variables/#server_audit_query_log_limit) | `1024` |
| `mariadb_server__cnf_server_audit_syslog_facility` | [mariadb.com](https://mariadb.com/kb/en/mariadb-audit-plugin-options-and-system-variables/#server_audit_syslog_facility) | `'LOG_USER'` |
| `mariadb_server__cnf_server_audit_syslog_ident` | [mariadb.com](https://mariadb.com/kb/en/mariadb-audit-plugin-options-and-system-variables/#server_audit_syslog_ident) | `'mysql-server_auditing'` |
| `mariadb_server__cnf_server_audit_syslog_info` | [mariadb.com](https://mariadb.com/kb/en/mariadb-audit-plugin-options-and-system-variables/#server_audit_syslog_info) | `''` |
| `mariadb_server__cnf_server_audit_syslog_priority` | [mariadb.com](https://mariadb.com/kb/en/mariadb-audit-plugin-options-and-system-variables/#server_audit_syslog_priority) | `'LOG_INFO'` |

Example:
```yaml
# optional - MariaDB Audit Plugin directives
mariadb_server__cnf_server_audit_events: 'CONNECT,QUERY_DDL'
mariadb_server__cnf_server_audit_excl_users: ''
mariadb_server__cnf_server_audit_file_path: '/var/log/mariadb/server_audit.log'
mariadb_server__cnf_server_audit_file_rotate_now: 'OFF'
mariadb_server__cnf_server_audit_file_rotate_size: '10M'
mariadb_server__cnf_server_audit_file_rotations: '9'
mariadb_server__cnf_server_audit_incl_users: ''
mariadb_server__cnf_server_audit_logging: 'ON'
mariadb_server__cnf_server_audit_output_type: 'FILE'
mariadb_server__cnf_server_audit_query_log_limit: '1024'
mariadb_server__cnf_server_audit_syslog_facility: 'LOG_USER'
mariadb_server__cnf_server_audit_syslog_ident: 'mysql-server_auditing'
mariadb_server__cnf_server_audit_syslog_info: ''
mariadb_server__cnf_server_audit_syslog_priority: 'LOG_INFO'
```


## Optional Role Variables - `mariadb_server__cnf_*` Config Directives for Galera

Install the first node with `--extra-vars='{"mariadb_server__run_galera_new_cluster": true}'` to bootstrap the cluster. Then run the role against the remaining nodes to add them to the cluster.

Set `mariadb_server__admin_user` to the same value for all nodes. Once the nodes are joined, users and databases will be shared, so they only need to be created on one of the nodes.

It is easily possible to add further nodes at a later date (e.g. two additional nodes to an existing 3-node system).

For Galera to work, also set the following variables:
```yaml
mariadb_server__cnf_bind_address__group_var: '0.0.0.0'
mariadb_server__cnf_binlog_format__group_var: 'ROW'
mariadb_server__cnf_default_storage_engine__group_var: 'InnoDB'
mariadb_server__cnf_innodb_autoinc_lock_mode__group_var: 2 # ensure the InnoDB locking mode for generating auto-increment values is set to interleaved lock mode
mariadb_server__cnf_innodb_doublewrite__group_var: 'ON' # this is the default value, and should not be changed
mariadb_server__cnf_innodb_flush_log_at_trx_commit__group_var: 0 #  inconsistencies can always be fixed by recovering from another node
```

| Role Variable   | Documentation   | Default Value   |
| -------------   | -------------   | -------------   |
| `mariadb_server__cnf_wsrep_cluster_addresses` | List of strings. [mariadb.com](https://mariadb.com/kb/en/galera-cluster-system-variables/#wsrep_cluster_address). DNS names work as well, IPs are preferred for performance. | unset |
| `mariadb_server__cnf_wsrep_cluster_name` | String. [mariadb.com](https://mariadb.com/kb/en/galera-cluster-system-variables/#wsrep_cluster_name) | `'lfops_galera_cluster'` |
| `mariadb_server__cnf_wsrep_node_address` | String. [mariadb.com](https://mariadb.com/kb/en/galera-cluster-system-variables/#wsrep_node_address) | `'{{ ansible_facts["default_ipv4"]["address"] }}'` |
| `mariadb_server__cnf_wsrep_node_name` | String. [mariadb.com](https://mariadb.com/kb/en/galera-cluster-system-variables/#wsrep_node_name) | `'{{ ansible_facts["nodename"] }}'` |
| `mariadb_server__cnf_wsrep_on` | Boolean. [mariadb.com](https://mariadb.com/kb/en/galera-cluster-system-variables/#wsrep_on). Also installs the packages required for Galera. | `false` |
| `mariadb_server__cnf_wsrep_provider_options` | String. [mariadb.com](https://mariadb.com/kb/en/galera-cluster-system-variables/#wsrep_provider_options) | `'gcache.size=300M; gcache.page_size=300M'` |
| `mariadb_server__cnf_wsrep_slave_threads` | Integer. [mariadb.com](https://mariadb.com/kb/en/galera-cluster-system-variables/#wsrep_slave_threads). Four slave threads can typically saturate one CPU core. | `'{{ 1 if ansible_facts["processor_nproc"] == 1 else (ansible_facts["processor_nproc"] - 1) * 4 }}'` |
| `mariadb_server__run_galera_new_cluster` | Boolean. [mariadb.com](https://mariadb.com/kb/en/mariadbd-options/#-wsrep-new-cluster). Do not set in the inventory, use via `--extra-vars`. This bootstraps the Galera cluster. Only set this to `true` during the deployment of the first node, or when recovering / restarting a stopped cluster. | `false` |
| `mariadb_server__cnf_wsrep_sst_auth` | String. [mariadb.com](https://mariadb.com/kb/en/galera-cluster-system-variables/#wsrep_sst_auth) | `''` |
| `mariadb_server__cnf_wsrep_sst_method` | String. [mariadb.com](https://mariadb.com/kb/en/galera-cluster-system-variables/#wsrep_sst_method). Use `'mariabackup'` to prevent blocking of the donor. | `'rsync'` |

Example:
```yaml
# optional - Galera directives
mariadb_server__cnf_wsrep_cluster_addresses:
  - '192.0.2.10'
  - '192.0.2.20'
  - '192.0.2.30'
mariadb_server__cnf_wsrep_cluster_name: 'lfops_galera_cluster'
mariadb_server__cnf_wsrep_node_address: '192.0.2.10'
mariadb_server__cnf_wsrep_node_name: 'db10'
mariadb_server__cnf_wsrep_on: true
mariadb_server__cnf_wsrep_provider_options: 'gcache.size=300M; gcache.page_size=300M'
mariadb_server__cnf_wsrep_slave_threads: 4
mariadb_server__cnf_wsrep_sst_auth: 'sst_user:linuxfabrik'
mariadb_server__cnf_wsrep_sst_method: 'mariabackup'
```


## Troubleshooting

Q: `A MySQL module is required: for Python 2.7 either PyMySQL, or MySQL-python, or for Python 3.X mysqlclient or PyMySQL. Consider setting ansible_python_interpreter to use the intended Python version.`

A: Install the `python3-PyMySQL` library. This can be done using the [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python) role, or run the full `mariadb_server` playbook, not limited by some tags.


Q: I always get `[Warning] Access denied for user 'root'@'localhost'` in mariadb.log when running this role.

A: This is due to `check_implicit_admin: true`. This checks if MariaDB allows login as root/nopassword before trying the supplied credentials. If successful, the login_user/login_password passed will be ignored. This is especially needed for the first run of this role.

Q: I get `IndexError: list index out of range` during "Create, update or delete MariaDB users".

A: Check that the user's `priv` is not set to `[]`. The lowest privileges allowed are `['*.*:USAGE']`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
