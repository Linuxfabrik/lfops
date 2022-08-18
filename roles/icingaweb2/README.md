# Ansible Role linuxfabrik.lfops.icingaweb2

This role installs and configures [IcingaWeb2](https://icinga.com/docs/icinga-web-2/latest/doc/01-About/).

Tested on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Install MariaDB, and create a database and a user for said database. This can be done using the [linuxfabrik.lfops.influxdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/influxdb) role.
* Install a web server (for example Apache httpd), and configure a virtual host for IcingaWeb2.  This can be done using the [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role.
* Install PHP version >= 7.3. This can be done using the [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role.


## Optional Requirements

* For exports to PDF also the following PHP modules are required: mbstring, GD, Imagick.
* LDAP PHP library when using Active Directory or LDAP for authentication.


## Tags

| Tag                | What it does                       |
| ---                | ------------                       |
| `icingaweb2`       | Installs and configures IcingaWeb2 |
| `icingaweb2:user`  | Creates user accounts              |
| `icingaweb2:icons` | Deploys icon assets for IcingaWeb2 |


## Mandatory Role Variables

| Variable                     | Description                                                                          |
| --------                     | -----------                                                                          |
| `icingaweb2__api_user_login` | The account for accessing the Icinga2 API.                                           |
| `icingaweb2__database_login` | The user account for accessing the SQL database. Currently, only MySQL is supported. |

Example:
```yaml
# mandatory
icingaweb2__api_user_login:
  username: 'icingaweb2-api-user'
  password: 'my-secret-password'
icingaweb2__database_login:
  username: 'icingaweb2_user'
  password: 'my-secret-password'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icingaweb2__database_host` | The host on which the SQL database is reachable. | `'localhost'` |
| `icingaweb2__database_name` | The name of the SQL database. | `'icingaweb2'` |
| `icingaweb2__default_theme` | The application-wide default theme for the web interface. | `'Icinga'` |
| `icingaweb2__host_authentications` /<br> `icingaweb2__group_authentications` | A list of dictionaries defining the authentication backends (e.g. database) for IcingaWeb2. Have a look at https://icinga.com/docs/icinga-web-2/latest/doc/05-Authentication/. Subkeys:<br> * `name`: Required, string. The name of the authentication backend.<br> * free-from: Optional, string. Will be used as the key-value pair in the resulting ini file.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | IcingaWeb2 Database |
| `icingaweb2__host_groups` /<br> `icingaweb2__group_groups` | A list of dictionaries defining the available user groups for IcingaWeb2. Have a look at https://icinga.com/docs/icinga-web-2/latest/doc/05-Authentication/#groups. Subkeys:<br> * `name`: Required, string. The name of the user group.<br> * free-from: Optional, string. Will be used as the key-value pair in the resulting ini file.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `icingaweb2__host_navigation_menu_entries` /<br> `icingaweb2__group_navigation_menu_entries` | A list of dictionaries defining additional menu entries in the IcingaWeb2 navigation bar. Subkeys:<br> * `name`: Required, string. The name of the navigation entry.<br> * free-from: Optional, string. Will be used as the key-value pair in the resulting ini file.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | IcingaWeb2 Database |
| `icingaweb2__host_resources` /<br> `icingaweb2__group_resources` | A list of dictionaries defining the resources for IcingaWeb2 (entities that provide data to IcingaWeb2). Have a look at https://icinga.com/docs/icinga-web-2/latest/doc/04-Resources/#resources. Subkeys:<br> * `name`: Required, string. The name of the resource.<br> * free-from: Optional, string. Will be used as the key-value pair in the resulting ini file.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `icingaweb2__host_roles` /<br> `icingaweb2__group_roles` | A list of dictionaries defining the user roles for IcingaWeb2. Have a look at https://icinga.com/docs/icinga-web-2/latest/doc/06-Security/#security-roles. Subkeys:<br> * `name`: Required, string. The name of the user role.<br> * free-from: Optional, string. Will be used as the key-value pair in the resulting ini file.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `icingaweb2__host_users` /<br>`icingaweb2__group_users` | A list of dictionaries containing the IcingaWeb2 users. Note that they are only created once, and not updated. Subkeys:<br> * `username`: Required, string. The username of the IcingaWeb2 user.<br> * `password`: Required, string. The password of the IcingaWeb2 user.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |

Example:
```yaml
# optional
icingaweb2__database_host: 'localhost'
icingaweb2__database_name: 'icingaweb2'
icingaweb2__default_theme: 'Icinga'
icingaweb2__host_authentications: []
  - name: 'AD'
    resource: 'ldap'
    backend: 'msldap'
  - name: 'autologin'
    backend: 'external'
icingaweb2__group_authentications: []
icingaweb2__host_groups: []
  - name: 'AD_groups'
    backend: 'msldap'
    resource: 'ldap'
    nested_group_search: '1'
    base_dn: 'DC=ad,DC=example,DC=com'
icingaweb2__group_groups: []
icingaweb2__host_navigation_menu_entries: []
  - name: 'New link'
    users: '*'
    groups: '*'
    type: 'menu-item'
    target: '_main'
    url: 'https://example.com/'
    icon: 'globe'
    owner: 'admin-user'
icingaweb2__group_navigation_menu_entries: []
icingaweb2__host_resources: []
icingaweb2__group_resources: []
icingaweb2__host_roles:
  - name:        'Administrators'
    users:       'admin-user'
    permissions: '*'
    groups:      'Administrators'
icingaweb2__group_roles: []
icingaweb2__host_users:
  - username: 'admin-user'
    password: 'my-secret-password'
icingaweb2__group_users: []
```


## License

[The Unlicense]()


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
