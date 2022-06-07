# Ansible Role icingaweb2

This role installs and configures [IcingaWeb2](https://icinga.com/docs/icinga-web-2/latest/doc/01-About/).

FQCN: linuxfabrik.lfops.icingaweb2

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* Install MariaDB, and create a database and a user for said database. This can be done using the [linuxfabrik.lfops.influxdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/influxdb) role.
* Install a web server (for example Apache httpd), and configure a virtual host for IcingaWeb2.
* Install PHP version >= 7.3. This can be done using the [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role.


### Optional

* For exports to PDF also the following PHP modules are required: mbstring, GD, Imagick.
* LDAP PHP library when using Active Directory or LDAP for authentication.


## Tags

| Tag              | What it does                       |
| ---              | ------------                       |
| icingaweb2       | Installs and configures IcingaWeb2 |
| icingaweb2:user  | Creates user accounts              |
| icingaweb2:icons | Deploys icon assets for IcingaWeb2 |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/icingaweb2/defaults/main.yml) for the variable defaults.


### Mandatory

#### icingaweb2__api_user_login

The account for accessing the Icinga2 API.

Example:
```yaml
icingaweb2__api_user_login:
  username: 'icingaweb2-api-user'
  password: 'my-secret-password'
```


#### icingaweb2__database_login

The user account for accessing the SQL database. Currently, only MySQL is supported.

Example:
```yaml
icingaweb2__database_login:
  username: 'icingaweb2_user'
  password: 'my-secret-password'
```


### Optional

#### icingaweb2__database_host

The host on which the SQL database is reachable.

Default:
```yaml
icingaweb2__database_host: 'localhost'
```


#### icingaweb2__database_name

The name of the SQL database.

Default:
```yaml
icingaweb2__database_name: 'icingaweb2'
```


#### icingaweb2__default_theme

The application-wide default theme for the web interface.

Default:
```yaml
icingaweb2__default_theme: 'Icinga'
```


#### icingaweb2__host_users / icingaweb2__group_users

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

A list of dictionaries containing the IcingaWeb2 users.
Note that they are only created once, and not updated.

Subkeys:

* `username`: Required, string. The username of the IcingaWeb2 user.
* `password`: Required, string. The password of the IcingaWeb2 user.

Default:
```yaml
icingaweb2__group_users: []
icingaweb2__host_users: []
icingaweb2__role_users: []
```

Example:
```yaml
icingaweb2__users:
  - username: 'admin-user'
    password: 'my-secret-password'
```


#### icingaweb2__host_authentications / icingaweb2__group_authentications

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

A list of dictionaries defining the authentication backends (e.g. database) for IcingaWeb2. Have a look at https://icinga.com/docs/icinga-web-2/latest/doc/05-Authentication/.

Subkeys:

* `name`: Required, string. The name of the authentication backend.
* free-from: Optional, string. Will be used as the key-value pair in the resulting ini file.

Default:
```yaml
icingaweb2__group_authentications: []
icingaweb2__host_authentications: []
icingaweb2__role_authentications:
  - name: '{{ icingaweb2__database_name }}'
    backend: 'db'
    resource: '{{ icingaweb2__database_name }}'
```


#### icingaweb2__host_groups / icingaweb2__group_groups

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

A list of dictionaries defining the available user groups for IcingaWeb2. Have a look at https://icinga.com/docs/icinga-web-2/latest/doc/05-Authentication/#groups.

Subkeys:

* `name`: Required, string. The name of the user group.
* free-from: Optional, string. Will be used as the key-value pair in the resulting ini file.

Default:
```yaml
icingaweb2__group_groups: []
icingaweb2__host_groups: []
icingaweb2__role_groups: []
```


#### icingaweb2__host_navigation_menu_entries / icingaweb2__group_navigation_menu_entries

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

A list of dictionaries defining additional menu entries in the IcingaWeb2 navigation bar.

Subkeys:

* `name`: Required, string. The name of the navigation entry.
* free-from: Optional, string. Will be used as the key-value pair in the resulting ini file.


Default:
```yaml
icingaweb2__group_navigation_menu_entries: []
icingaweb2__host_navigation_menu_entries: []
icingaweb2__role_navigation_menu_entries: []
```


#### icingaweb2__host_resources / icingaweb2__group_resources

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

A list of dictionaries defining the resources for IcingaWeb2 (entities that provide data to IcingaWeb2). Have a look at https://icinga.com/docs/icinga-web-2/latest/doc/04-Resources/#resources.

Subkeys:

* `name`: Required, string. The name of the resource.
* free-from: Optional, string. Will be used as the key-value pair in the resulting ini file.


Default:
```yaml
icingaweb2__group_resources: []
icingaweb2__host_resources: []
icingaweb2__role_resources:
  - name: '{{ icingaweb2__database_name }}'
    type: 'db'
    db: 'mysql'
    host: '{{ icingaweb2__database_host }}'
    port: 3306
    dbname: '{{ icingaweb2__database_name }}'
    username: '{{ icingaweb2__database_login.username }}'
    password: '{{ icingaweb2__database_login.password }}'
    charset: 'utf8mb4'
```


#### icingaweb2__host_roles / icingaweb2__group_roles

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

A list of dictionaries defining the user roles for IcingaWeb2. Have a look at https://icinga.com/docs/icinga-web-2/latest/doc/06-Security/#security-roles.

Subkeys:

* `name`: Required, string. The name of the user role.
* free-from: Optional, string. Will be used as the key-value pair in the resulting ini file.


Default:
```yaml
icingaweb2__group_roles: []
icingaweb2__host_roles: []
icingaweb2__role_roles: []
```

Example:
```yaml
icingaweb2__host_roles:
  - name:        'Administrators'
    users:       'admin-user,other-user'
    permissions: '*'
    groups:      'Administrators'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
