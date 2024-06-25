# Ansible Role linuxfabrik.lfops.postgresql_server

This role installs and configures a [PostgreSQL](https://www.postgresql.org/) server.


## Mandatory Requirements

* Install the `python3-psycopg2` library. This can be done using the [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python) role.

If you use the [postgresql_server Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/postgresql_server.yml), this is automatically done for you.


## Optional Requirements

* Enable the official [PostgreSQL Yum Repository](https://yum.postgresql.org/). This can be done using the [linuxfabrik.lfops.repo_postgresql](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_postgresql) role.

If you use the [postgresql_server Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/postgresql_server.yml), this is automatically done for you.


## Tags

| Tag                           | What it does                                       |
| ---                           | ------------                                       |
| `postgresql_server`           | Installs and configures PostgreSQL                 |
| `postgresql_server:state`     | Manages the state of the PostgreSQL service        |
| `postgresql_server:users`     | Creates, updates and deletes PostgreSQL users      |
| `postgresql_server:databases` | Creates, updates and deletes PostgreSQL databases  |
| `postgresql_server:privs`     | Creates, updates and deletes PostgreSQL privileges |
| `postgresql_server:dump`      | Configures database dumping (backups) |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `postgresql_server__conf_listen_addresses` | List of IP address(es) to listen on. Use `*` for all. | `['localhost']` |
| `postgresql_server__conf_max_connections` | Determines the maximum number of concurrent connections to the database server. | `100` |
| `postgresql_server__conf_password_encryption` | Determines the algorithm to use to encrypt passwords when creating new users / roles. Possible options:<ul><li>`'scram-sha-256'`</li><li>`'md5'`</li></ul>| `'scram-sha-256'` |
| `postgresql_server__conf_port` | The TCP port the server listens on. | `5432` |
| `postgresql_server__databases__host_var` / `postgresql_server__databases__group_var` | List of dictionaries of databases to create. Subkeys:<ul><li>`name`: Mandatory, string. Name of the database. </li><li>`lc_collate`: Optional, string. DB Collation order. Defaults to `'en_US.UTF-8'`.</li><li>`lc_ctype`: Optional, string. DB Character classification. Defaults to `'en_US.UTF-8'`.</li><li>`encoding`: Optional, string. DB encoding. Defaults to `'UTF-8'`.</li><li>`encoding`: Optional, string. DB template. Defaults to `'template0'`.</li><li>`owner`: Optional, string. DB owner. Defaults to `'postgres'`.</li><li>`state`: Optional, string. `present` or `absent`. Defaults to `'present'`.</li></ul> For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `postgresql_server__enabled` | Enables or disables the service, analogous to `systemctl enable/disable`. Possible options: `true`, `false`. | `true` |
| `postgresql_server__pg_hba_entries` | List of [host based authentication](https://www.postgresql.org/docs/current/static/auth-pg-hba-conf.html) entries. Subkeys:<ul><li>`type`: Mandatory, string. Record type.</li><li>`database`: Mandatory, string. Specifies which database name(s) this record matches.</li><li>`user`: Mandatory, string. Specifies which database user name(s) this record matches.</li><li>`address`: Optional, string. Specifies the client machine address(es) that this record matches. Defaults to `''`.</li><li>`auth_method`: Optional, string. Specifies the authentication method to use when a connection matches this record. Defaults to `'scram-sha-256'`.</li><li>`auth_options`: Optional, string. Options for the `auth_method`. Defaults to `''`.</li></ul> | Allow `scram-sha-256` for all `local` and `host` |
| `postgresql_server__privs__host_var` / `postgresql_server__privs__group_var` | List of dictionaries containing PostgreSQL privileges to apply. Subkeys:<ul><li>`privs`: Optional, list of strings. List of privileges to grant/revoke. Defaults to unset.</li><li>`type`: Optional, string. Type of database object to set privileges on. Defaults to `'database'`.</li><li>`objs`: Mandatory, list of strings. List of database objects (of type `type`) to set privileges on.</li><li>`grant_option`: Mandatory, boolean. Whether the role may grant/revoke the specified privileges/group memberships to others. Defaults to unset.</li></ul> For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `postgresql_server__state` | Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options:<ul><li>`started`</li><li>`stopped`</li><li>`restarted`</li><li>`reloaded`</li></ul> | `'started'` |
| `postgresql_server__users__host_var` / `postgresql_server__users__group_var` | List of dictionaries of users to create . Subkeys:<ul><li>`username`: Mandatory, string. Username. </li><li>`password`: Optional, string. Password. Defaults to unset. </li><li>`role_attr_flags`: Optional, list of strings. List of [PostgreSQL user attributes](https://www.postgresql.org/docs/current/role-attributes.html). Defaults to unset. </li><li>`state`: Optional, string. `present` or `absent`. Defaults to `'present'`.</li></ul>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `postgresql_server__version` | Specifies the PostgreSQL verison to install (use only the major version number like `'14'`. The latest minor version is used). Set this when using the official PostgreSQL Repo. | `''` |


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
    state: 'present'
postgresql_server__enabled: true
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
