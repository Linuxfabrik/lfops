# Ansible Role linuxfabrik.lfops.postgresql_server

This role installs and configures a [PostgreSQL](https://www.postgresql.org/) server.


## Mandatory Requirements

* Install the `python3-psycopg2` library. This can be done using the [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python) role.

If you use the [postgresql_server Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/postgresql_server.yml), this is automatically done for you.


## Optional Requirements

* Enable the official [PostgreSQL Yum Repository](https://yum.postgresql.org/). This can be done using the [linuxfabrik.lfops.repo_postgresql](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_postgresql) role.

If you use the [postgresql_server Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/postgresql_server.yml), this is automatically done for you.


## Tags

`postgresql_server`

* Installs and configures PostgreSQL.
* Triggers: posgresql.service restart.

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

* Determines the algorithm to use to encrypt passwords when creating new users / roles. Possible options: `'scram-sha-256'`, `'md5'`.
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

        * Optional. DB Collation order.
        * Type: String.
        * Default: `'en_US.UTF-8'`

    * `lc_ctype`:

        * Optional. DB Character classification.
        * Type: String.
        * Default: `'en_US.UTF-8'`

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

* The directory where `postgresql-dump` stores its database dumps.
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

`postgresql_server__pg_hba_entries`

* List of [host based authentication](https://www.postgresql.org/docs/current/static/auth-pg-hba-conf.html) entries.
* Type: List of dictionaries.
* Default: Allow `scram-sha-256` for all `local` and `host`
* Subkeys:

    * `type`:

        * Mandatory. Record type.
        * Type: String.

    * `database`:

        * Mandatory. Specifies which database name(s) this record matches.
        * Type: String.

    * `user`:

        * Mandatory. Specifies which database user name(s) this record matches.
        * Type: String.

    * `address`:

        * Optional. Specifies the client machine address(es) that this record matches.
        * Type: String.
        * Default: `''`

    * `auth_method`:

        * Optional. Specifies the authentication method to use when a connection matches this record.
        * Type: String.
        * Default: `'scram-sha-256'`

    * `auth_options`:

        * Optional. Options for the `auth_method`.
        * Type: String.
        * Default: `''`

`postgresql_server__privs__host_var` / `postgresql_server__privs__group_var`

* List of dictionaries containing PostgreSQL privileges to apply.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

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

        * Mandatory. Whether the role may grant/revoke the specified privileges/group memberships to others.
        * Type: Bool.
        * Default: unset

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

`postgresql_server__version`

* Specifies the PostgreSQL verison to install (use only the major version number like `'14'`. The latest minor version is used). Set this when using the official PostgreSQL Repo.
* Type: String.
* Default: `''`


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
postgresql_server__enabled: true
postgresql_server__login_password: 'linuxfabrik'
postgresql_server__pg_hba_entries:
  - type: 'local'
    database: 'all'
    user: 'all'
  - type: 'host'
    database: 'all'
    user: 'all'
postgresql_server__state: 'started'
postgresql_server__users__host_var:
  - username: 'user1'
    password: 'linuxfabrik'
    state: 'present'
postgresql_server__version: '14'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
