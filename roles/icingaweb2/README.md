# Ansible Role linuxfabrik.lfops.icingaweb2

This role installs and configures [IcingaWeb2](https://icinga.com/docs/icinga-web-2/latest/doc/01-About/).


## Mandatory Requirements

* Install MariaDB, and create a database and a user for said database. This can be done using the [linuxfabrik.lfops.mariadb-server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb-server) role.
* Install a web server (for example Apache httpd), and configure a virtual host for IcingaWeb2.  This can be done using the [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role.
* Install PHP version >= 7.3. This can be done using the [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role.


## Optional Requirements

* For exports to PDF also the following PHP modules are required: mbstring, GD, Imagick.
* LDAP PHP library when using Active Directory or LDAP for authentication.


## Tags

| Tag                | What it does                                      |
| ---                | ------------                                      |
| `icingaweb2`       | Installs and configures IcingaWeb2                |
| `icingaweb2:configure` | Configures Authentication, Resources, Navigation and IcingaWeb2 settings. |
| `icingaweb2:resources` | Deploys `/etc/icingaweb2/resources.ini`       |
| `icingaweb2:user`  | Creates user accounts and deploys the role config |


## Mandatory Role Variables

| Variable                     | Description                                                                          |
| --------                     | -----------                                                                          |
| `icingaweb2__api_user_login` | The account for accessing the Icinga2 API.                                           |
| `icingaweb2__database_login` | The user account for accessing the SQL database. Currently, only MySQL is supported. |
| `icingaweb2__url_host`       | The host part of the URL for IcingaWeb2. Will be used for the Apache HTTPd vHost.    |

Example:
```yaml
# mandatory
icingaweb2__api_user_login:
  username: 'icingaweb2-api-user'
  password: 'linuxfabrik'
icingaweb2__database_login:
  username: 'icingaweb2_user'
  password: 'linuxfabrik'
icingaweb2__url_host: 'monitoring.example.com'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icingaweb2__authentications__host_var` /<br> `icingaweb2__authentications__group_var` | A list of dictionaries defining the authentication backends (e.g. database) for IcingaWeb2. Have a look at https://icinga.com/docs/icinga-web-2/latest/doc/05-Authentication/. Subkeys:<br> * `name`: Mandatory, string. The name of the authentication backend.<br> * free-form: Optional, string. Will be used as the key-value pair in the resulting ini file.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | IcingaWeb2 Database |
| `icingaweb2__database_host` | The host on which the SQL database is reachable. | `'localhost'` |
| `icingaweb2__database_login_host` | The Host-part of the SQL database user. | `'localhost'` |
| `icingaweb2__database_name` | The name of the SQL database. | `'icingaweb2'` |
| `icingaweb2__default_theme` | The application-wide default theme for the web interface. | `'Icinga'` |
| `icingaweb2__groups__host_var` /<br> `icingaweb2__groups__group_var` | A list of dictionaries defining the available user groups for IcingaWeb2. Have a look at https://icinga.com/docs/icinga-web-2/latest/doc/05-Authentication/#groups. Subkeys:<br> * `name`: Mandatory, string. The name of the user group.<br> * free-form: Optional, string. Will be used as the key-value pair in the resulting ini file.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `icingaweb2__navigation_host_actions_entries__host_var` /<br> `icingaweb2__navigation_host_actions_entries__group_var` | A list of dictionaries defining additional actions entries in the deprecated IcingaWeb2 Monitoring host view. Use `icingaweb2__navigation_icingadb_host_actions_entries__*_var` with IcingaDB. Subkeys:<br> * `name`: Mandatory, string. The name of the action.<br> * free-form: Optional, string. Will be used as the key-value pair in the resulting ini file.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `icingaweb2__navigation_icingadb_host_actions_entries__host_var` /<br> `icingaweb2__navigation_icingadb_host_actions_entries__group_var` | A list of dictionaries defining additional actions entries in the IcingaWeb2 IcingaDB host view. Subkeys:<br> * `name`: Mandatory, string. The name of the action.<br> * free-form: Optional, string. Will be used as the key-value pair in the resulting ini file.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `icingaweb2__navigation_icingadb_service_actions_entries__host_var` /<br> `icingaweb2__navigation_icingadb_service_actions_entries__group_var` | A list of dictionaries defining additional actions entries in the IcingaWeb2 IcingaDB service view. Subkeys:<br> * `name`: Mandatory, string. The name of the action.<br> * free-form: Optional, string. Will be used as the key-value pair in the resulting ini file.<br>For the usage in `service_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `icingaweb2__navigation_menu_entries__host_var` /<br> `icingaweb2__navigation_menu_entries__group_var` | A list of dictionaries defining additional menu entries in the IcingaWeb2 navigation bar. Subkeys:<br> * `name`: Mandatory, string. The name of the navigation entry.<br> * free-form: Optional, string. Will be used as the key-value pair in the resulting ini file.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | IcingaWeb2 Database |
| `icingaweb2__navigation_service_actions_entries__host_var` /<br> `icingaweb2__navigation_service_actions_entries__group_var` | A list of dictionaries defining additional actions entries in the IcingaWeb2 service view. Use `icingaweb2__navigation_icingadb_service_actions_entries__*_var` with IcingaDB. Subkeys:<br> * `name`: Mandatory, string. The name of the action.<br> * free-form: Optional, string. Will be used as the key-value pair in the resulting ini file.<br>For the usage in `service_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `icingaweb2__resources__host_var` /<br> `icingaweb2__resources__group_var` | A list of dictionaries defining the resources for IcingaWeb2 (entities that provide data to IcingaWeb2). Have a look at https://icinga.com/docs/icinga-web-2/latest/doc/04-Resources/#resources. Subkeys:<br> * `name`: Mandatory, string. The name of the resource.<br> * free-form: Optional, string. Will be used as the key-value pair in the resulting ini file.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `icingaweb2__roles__host_var` /<br> `icingaweb2__roles__group_var` | A list of dictionaries defining the user roles for IcingaWeb2. Have a look at https://icinga.com/docs/icinga-web-2/latest/doc/06-Security/#security-roles. Subkeys:<br> * `name`: Mandatory, string. The name of the user role.<br> * free-form: Optional, string. Will be used as the key-value pair in the resulting ini file.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `icingaweb2__url_port` | The port of the URL for IcingaWeb2. Will be used for the Apache HTTPd vHost. | `80` |
| `icingaweb2__users__host_var` /<br> `icingaweb2__users__group_var` | A list of dictionaries containing the IcingaWeb2 users. Subkeys: <ul><li>`username`: Mandatory, string. The username of the IcingaWeb2 user.</li><li>`password`: Mandatory, string. The password of the IcingaWeb2 user. Note that it is only set once, so the user can change it themselves.</li><li>`state`: Optional, string. State of the user. Either `present` (insert only, no update), `updated` (changes the password, but not idempotent) or `absent`. Defaults to `present`.</li></ul> For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |

Example:
```yaml
# optional
icingaweb2__authentications__host_var:
  - name: 'AD'
    resource: 'ldap'
    backend: 'msldap'
  - name: 'autologin'
    backend: 'external'
icingaweb2__authentications__group_var: []
icingaweb2__database_host: 'localhost'
icingaweb2__database_login_host: 'localhost'
icingaweb2__database_name: 'icingaweb2'
icingaweb2__default_theme: 'Icinga'
icingaweb2__groups__host_var:
  - name: 'AD_groups'
    backend: 'msldap'
    resource: 'ldap'
    nested_group_search: '1'
    base_dn: 'DC=ad,DC=example,DC=com'
icingaweb2__navigation_host_actions_entries__host_var:
  - name: 'vSphereDB VM'
    type: 'host-action'
    target: '_next'
    url: 'vspheredb/vm?uuid=$_host_uuid$'
    filter: '_host_uuid!='
    users: '*'
    groups: '*'
    owner: 'admin-user'
  - name: 'vSphereDB Host'
    type: 'host-action'
    target: '_next'
    url: 'vspheredb/host?uuid=$_host_esx_uuid$'
    filter: '_host_esx_uuid!='
    users: '*'
    groups: '*'
    owner: 'admin-user'
  - name: 'LibreNMS'
    type: 'host-action'
    target: '_blank'
    url: 'https://librenms.example.com/device/$_host_librenms_device_id$'
    filter: '_host_librenms_device_id!='
    icon: 'librenms-alerts.png'
    users: '*'
    groups: '*'
    owner: 'admin-user'
icingaweb2__navigation_icingadb_host_actions_entries__host_var:
  - name: 'vSphereDB VM'
    type: 'icingadb-host-action'
    target: '_next'
    url: 'vspheredb/vm?uuid=$host.vars.uuid$'
    filter: 'host.vars.uuid~*'
    icon: 'cloud'
    users: '*'
    groups: '*'
    owner: 'admin-user'
  - name: 'vSphereDB Host'
    type: 'icingadb-host-action'
    target: '_next'
    url: 'vspheredb/host?uuid=$host.vars.esx_uuid$'
    filter: 'host.vars.esx_uuid~*'
    icon: 'cloud'
    users: '*'
    groups: '*'
    owner: 'admin-user'
  - name: 'LibreNMS'
    type: 'icingadb-host-action'
    target: '_blank'
    url: 'https://librenms.example.com/device/$host.vars.librenms_device_id$'
    filter: 'host.vars.librenms_device_id~*'
    icon: 'librenms-alerts.png'
    users: '*'
    groups: '*'
    owner: 'admin-user'
icingaweb2__navigation_icingadb_service_actions_entries__host_var:
  - name: 'vSphereDB VM'
    type: 'icingadb-service-action'
    target: '_next'
    url: 'vspheredb/vm?uuid=$host.vars.uuid$'
    filter: 'host.vars.uuid~*'
    icon: 'cloud'
    users: '*'
    groups: '*'
    owner: 'admin-user'
  - name: 'vSphereDB Host'
    type: 'icingadb-service-action'
    target: '_next'
    url: 'vspheredb/host?uuid=$host.vars.esx_uuid$'
    filter: 'host.vars.esx_uuid~*'
    icon: 'cloud'
    users: '*'
    groups: '*'
    owner: 'admin-user'
  - name: 'LibreNMS'
    type: 'icingadb-service-action'
    target: '_blank'
    url: 'https://librenms.example.com/device/$host.vars.librenms_device_id$'
    filter: 'host.vars.librenms_device_id~*'
    icon: 'librenms-alerts.png'
    users: '*'
    groups: '*'
    owner: 'admin-user'
icingaweb2__navigation_menu_entries__host_var:
  - name: 'New link'
    users: '*'
    groups: '*'
    type: 'menu-item'
    target: '_main'
    url: 'https://example.com/'
    icon: 'globe'
    owner: 'admin-user'
icingaweb2__navigation_service_actions_entries__host_var:
  - name: 'vSphereDB VM'
    type: 'service-action'
    target: '_next'
    url: 'vspheredb/vm?uuid=$_host_uuid$'
    icon: 'icon-cloud'
    filter: '_host_uuid!='
    users: '*'
    groups: '*'
    owner: 'admin-user'
  - name: 'vSphereDB Host'
    type: 'service-action'
    target: '_next'
    url: 'vspheredb/host?uuid=$_host_esx_uuid$'
    filter: '_host_esx_uuid!='
    users: '*'
    groups: '*'
    owner: 'admin-user'
  - name: 'LibreNMS'
    type: 'service-action'
    target: '_blank'
    url: 'https://librenms.example.com/device/$_host_librenms_device_id$'
    filter: '_host_librenms_device_id!='
    icon: 'librenms-alerts.png'
    users: '*'
    groups: '*'
    owner: 'admin-user'
icingaweb2__navigation_menu_entries__group_var: []
icingaweb2__resources__host_var: []
icingaweb2__resources__group_var:
  - name: 'ldap'
    type: 'ldap'
    hostname: 'ad.example.com'
    port: '389'
    base_dn: 'DC=ad,DC=example,DC=com'
    bind_dn: 'ldap-user'
    bind_pw: 'linuxfabrik'
icingaweb2__roles__host_var:
  - name: 'Administrators'
    users: 'admin-user'
    permissions: '*'
    groups: 'Administrators'
icingaweb2__roles__group_var: []
icingaweb2__url_port: 81
icingaweb2__users__host_var:
  - username: 'admin-user'
    password: 'linuxfabrik'
icingaweb2__users__group_var: []
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
