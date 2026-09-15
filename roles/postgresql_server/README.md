# Ansible Role linuxfabrik.lfops.postgresql_server

This role installs and configures a [PostgreSQL](https://www.postgresql.org/) server.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* PostgreSQL is installed from the PostgreSQL Yum Repository, not from the distribution packages. The cluster lives in `/var/lib/pgsql/<version>/data` and runs as `postgresql-<version>.service`. The role does not upgrade the data: changing `postgresql_server__version` on an existing host installs and initializes a second, empty cluster next to the old one, which fails to start while the old one listens on the same port.
* Settings that only take effect after a restart (`postgresql_server__conf_listen_addresses`, `__conf_max_connections`, `__conf_port`) are written to `conf.d/z00-linuxfabrik.conf`, and changing them restarts PostgreSQL. `postgresql_server__conf_password_encryption` is written to `conf.d/z00-linuxfabrik-reload.conf`, and a change there or in `pg_hba.conf` only reloads PostgreSQL, which keeps open connections.
* Before the reload or restart, the role checks the configuration files with `postgres -C` and asks the running server for errors in `pg_hba.conf` through the `pg_hba_file_rules` view. A broken setting aborts the run with the error message, and the running server keeps its current configuration. The file with the error is already deployed at that point: fix the inventory and run the role again before PostgreSQL is restarted for any other reason.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* The `python3-psycopg2` library must be installed (role: [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python)).
* The [PostgreSQL Yum Repository](https://yum.postgresql.org/) must be enabled (role: [linuxfabrik.lfops.repo_postgresql](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_postgresql)).


## Tags

`postgresql_server`

* Installs and configures PostgreSQL, and manages its users, databases, privileges and the dump timer.
* Triggers: postgresql-<version>.service reload or restart, after the configuration check.

`postgresql_server:state`

* Manages the state of the PostgreSQL service.
* Triggers: none.

`postgresql_server:users`

* Creates, updates and deletes PostgreSQL users.
* Triggers: none.

`postgresql_server:databases`

* Creates, updates and deletes PostgreSQL databases.
* Triggers: none.

`postgresql_server:privs`

* Creates, updates and deletes PostgreSQL privileges.
* Triggers: none.

`postgresql_server:dump`

* Configures database dumping (backups).
* Triggers: none.


## Mandatory Role Variables

`postgresql_server__version`

* The major version of PostgreSQL to install from the PostgreSQL Yum Repository, for example `'18'`. The latest minor release of that version is installed.
* Type: String.

Example:
```yaml
# mandatory
postgresql_server__version: '18'
```


## Optional Role Variables

`postgresql_server__conf_listen_addresses`

* List of IP address(es) to listen on. Use `*` for all.
* Type: List.
* Default: `['localhost']`

`postgresql_server__conf_max_connections`

* Determines the maximum number of concurrent connections to the database server.
* Type: Number.
* Default: `100`

`postgresql_server__conf_password_encryption`

* Determines the algorithm to use to encrypt passwords when creating new users / roles or changing their passwords. Possible options: `'scram-sha-256'`, `'md5'`. PostgreSQL deprecates MD5 passwords and logs a warning for them.
* Type: String.
* Default: `'scram-sha-256'`

`postgresql_server__conf_port`

* The TCP port the server listens on.
* Type: Number.
* Default: `5432`

`postgresql_server__databases__host_var` / `postgresql_server__databases__group_var`

* List of dictionaries of databases to create.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the database.
        * Type: String.

    * `lc_collate`:

        * Optional. Collation order of the database. Only used when the database is created, PostgreSQL cannot change it afterwards.
        * Type: String.
        * Default: `'C.UTF-8'`
        * Deviates from the upstream default, the locale of the template database, which `initdb` takes from the environment of the host: `C.UTF-8` exists on every host, also where only the minimal glibc language pack is installed, and does not change its sort order with a glibc update. It sorts by code point, not by language rules (`B` before `a`); set `'en_US.UTF-8'` or another installed locale for linguistic sorting.

    * `lc_ctype`:

        * Optional. Character classification of the database. Only used when the database is created, PostgreSQL cannot change it afterwards.
        * Type: String.
        * Default: `'C.UTF-8'`
        * Deviates from the upstream default for the same reason as `lc_collate`.

    * `encoding`:

        * Optional. DB encoding.
        * Type: String.
        * Default: `'UTF-8'`

    * `template`:

        * Optional. DB template.
        * Type: String.
        * Default: `'template0'`

    * `owner`:

        * Optional. DB owner.
        * Type: String.
        * Default: `'postgres'`

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`postgresql_server__dump_directory`

* The directory where `postgresql-dump` stores its dumps: one file `dump-<database>.sql.gz` per database, and `globals.sql.gz` with the roles and tablespaces, which pg_dump does not include in a database dump. Restore `globals.sql.gz` first. The directory is emptied at the start of every dump.
* Type: String.
* Default: `'/backup/postgresql-dump'`

`postgresql_server__dump_on_calendar`

* Sets the `OnCalendar=` directive for `postgresql-dump.timer`.
* Type: String.
* Default: `'*-*-* 21:{{ 59 | random(start=0, seed=inventory_hostname) }}:00'`

`postgresql_server__enabled`

* Enables or disables the service, analogous to `systemctl enable/disable`. Possible options: `true`, `false`.
* Type: Bool.
* Default: `true`

`postgresql_server__login_password`

* The password for the `postgres` user to establish the PostgreSQL session.
* Type: String.
* Default: unset

`postgresql_server__pg_hba_host_entries__host_var` / `postgresql_server__pg_hba_host_entries__group_var`

* [Client authentication](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html) records for TCP/IP connections (`host`, `hostssl`, `hostnossl`, `hostgssenc`, `hostnogssenc`). Entries are identified by `type`, `database`, `user` and `address` together.
* PostgreSQL uses the first record that matches a connection. The role renders the entries from the inventory in their inventory order, followed by the role defaults, which are catch-all records. An entry that uses the same identifying keys as a default replaces that default in place.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default:

    ```yaml
    - type: 'host'
      database: 'all'
      user: 'all'
      address: '127.0.0.1/32'
      auth_method: 'scram-sha-256'
    - type: 'host'
      database: 'all'
      user: 'all'
      address: '::1/128'
      auth_method: 'scram-sha-256'
    ```

* Subkeys:

    * `type`:

        * Mandatory. Record type. One of `host`, `hostgssenc`, `hostnogssenc`, `hostnossl`, `hostssl`.
        * Type: String.

    * `database`:

        * Mandatory. Database name(s) this record matches, for example `all` or `db1,db2`.
        * Type: String.

    * `user`:

        * Mandatory. Database user name(s) this record matches, for example `all` or `user1`.
        * Type: String.

    * `address`:

        * Mandatory. Client address(es) this record matches, for example `192.0.2.0/24`, `all`, `samenet` or a host name.
        * Type: String.

    * `auth_method`:

        * Optional. Authentication method for a connection that matches this record.
        * Type: String.
        * Default: `'scram-sha-256'`

    * `auth_options`:

        * Optional. Options for the `auth_method`.
        * Type: String.
        * Default: `''`

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`postgresql_server__pg_hba_local_entries__host_var` / `postgresql_server__pg_hba_local_entries__group_var`

* [Client authentication](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html) records of type `local`, for connections over the Unix-domain socket. Entries are identified by `database` and `user` together.
* PostgreSQL uses the first record that matches a connection. The role renders the entries from the inventory in their inventory order, followed by the role defaults, which are catch-all records. An entry that uses the same identifying keys as a default replaces that default in place.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default:

    ```yaml
    - database: 'all'
      user: 'postgres'
      auth_method: 'peer'
    - database: 'all'
      user: 'all'
      auth_method: 'scram-sha-256'
    ```

* Subkeys:

    * `database`:

        * Mandatory. Database name(s) this record matches, for example `all` or `db1,db2`.
        * Type: String.

    * `user`:

        * Mandatory. Database user name(s) this record matches, for example `all` or `user1`.
        * Type: String.

    * `auth_method`:

        * Optional. Authentication method for a connection that matches this record.
        * Type: String.
        * Default: `'scram-sha-256'`

    * `auth_options`:

        * Optional. Options for the `auth_method`.
        * Type: String.
        * Default: `''`

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`postgresql_server__privs__host_var` / `postgresql_server__privs__group_var`

* List of dictionaries containing PostgreSQL privileges to apply.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `roles`:

        * Mandatory. List of roles the privileges are granted to or revoked from.
        * Type: List of strings.

    * `privs`:

        * Optional. List of privileges to grant/revoke.
        * Type: List of strings.
        * Default: unset

    * `type`:

        * Optional. Type of database object to set privileges on.
        * Type: String.
        * Default: `'database'`

    * `objs`:

        * Mandatory. List of database objects (of type `type`) to set privileges on.
        * Type: List of strings.

    * `grant_option`:

        * Optional. Whether the roles may grant/revoke the specified privileges/group memberships to others. Only has an effect when `state` is `present`.
        * Type: Bool.
        * Default: `false`

    * `state`:

        * Optional. Whether the privileges are granted or revoked. Possible options: `present`, `absent`.
        * Type: String.
        * Default: `'present'`

`postgresql_server__state`

* Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options: `started`, `stopped`, `restarted`, `reloaded`.
* Type: String.
* Default: `'started'`

`postgresql_server__users__host_var` / `postgresql_server__users__group_var`

* List of dictionaries of users to create.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `username`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Optional. Password.
        * Type: String.
        * Default: unset

    * `role_attr_flags`:

        * Optional. List of [PostgreSQL user attributes](https://www.postgresql.org/docs/current/role-attributes.html).
        * Type: List of strings.
        * Default: unset

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`


Example:
```yaml
# optional
postgresql_server__conf_listen_addresses:
  - 'localhost'
postgresql_server__conf_max_connections: 100
postgresql_server__conf_password_encryption: 'scram-sha-256'
postgresql_server__conf_port: 5432
postgresql_server__databases__host_var:
  - name: 'database1'
    owner: 'user1'
    lc_collate: 'en_US.UTF-8'
    lc_ctype: 'en_US.UTF-8'
    state: 'present'
postgresql_server__dump_directory: '/backup/postgresql-dump'
postgresql_server__dump_on_calendar: '*-*-* 21:30:00'
postgresql_server__enabled: true
postgresql_server__login_password: 'linuxfabrik'
postgresql_server__pg_hba_host_entries__host_var:
  - type: 'hostssl'
    database: 'database1'
    user: 'user1'
    address: '192.0.2.0/24'
postgresql_server__pg_hba_local_entries__host_var:
  - database: 'all'
    user: 'all'
    auth_method: 'reject'
  - database: 'database1'
    user: 'user1'
postgresql_server__privs__host_var:
  - privs:
      - 'CONNECT'
    type: 'database'
    objs:
      - 'database1'
    roles:
      - 'user1'
    state: 'present'
postgresql_server__state: 'started'
postgresql_server__users__host_var:
  - username: 'user1'
    password: 'linuxfabrik'
    state: 'present'
```


## Troubleshooting

**The run aborts with `This host has a PostgreSQL cluster of the distribution package in /var/lib/pgsql/data`**

* The host runs PostgreSQL from the distribution packages, which the role does not manage. Move the data to the PostgreSQL Yum Repository release before running the role, for example: dump the cluster with `pg_dumpall`, stop and disable `postgresql.service`, rename `/var/lib/pgsql/data`, run the role, and restore the dump into the new cluster.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
