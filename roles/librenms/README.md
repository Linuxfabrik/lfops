# Ansible Role librenms

This role installs and configures [LibreNMS](https://www.librenms.org/).

FQCN: linuxfabrik.lfops.librenms

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* Install Python 3, and the python3-policycoreutils module (required for the SELinux Ansible tasks). This can be done using the [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils) role.
* Install MariaDB, and create a database and a user for said database. This can be done using the [linuxfabrik.lfops.influxdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/influxdb) role.
* Install a web server (for example Apache httpd), and configure a virtual host for LibreNMS. This can be done using the [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role.
* Install PHP version >= 7.3. This can be done using the [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag      | What it does                     |
| ---      | ------------                     |
| librenms | Installs and configures LibreNMS |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/librenms/defaults/main.yml) for the variable defaults.


### Mandatory


#### librenms__database_login

The user account for accessing the MySQL database.

Example:
```yaml
librenms__database_login:
  username: 'librenms'
  password: 'my-secret-password'
```


#### librenms__fqdn

The fully qualified domain name under which LibreNMS is accessible.

Example:
```yaml
librenms__fqdn: 'librenms.example.com'
```


### Optional

#### librenms__config_auth_mechanism

Which authentication mechanism LibreNMS should use. Have a look at https://docs.librenms.org/Extensions/Authentication/.
Note that only one mechanism can be active at the same time.

Possible options:
* active_directory
* http-auth
* ldap
* ldap-authorization
* mysql
* sso

Default:
```yaml
librenms__config_auth_mechanism: 'mysql'
```


#### librenms__config_update_channel

Which update channel LibreNMS should use during automatic updates. Possible options:

* master
* release

Default:
```yaml
librenms__config_update_channel: 'release'
```


#### librenms__database_host

The host on which the MySQL database is reachable.

Default:
```yaml
librenms__database_host: 'localhost'
```


#### librenms__database_name

The name of the SQL database.

Default:
```yaml
librenms__database_name: 'librenms'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
