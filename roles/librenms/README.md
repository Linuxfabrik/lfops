# Ansible Role linuxfabrik.lfops.librenms

This role installs and configures [LibreNMS](https://www.librenms.org/).


## Mandatory Requirements

* Install Python 3, and the python3-policycoreutils module (required for the SELinux Ansible tasks). This can be done using the [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils) role.
* Install MariaDB, and create a database and a user for said database. This can be done using the [linuxfabrik.lfops.mariadb-server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb-server) role.
* Install a web server (for example Apache httpd), and configure a virtual host for LibreNMS. This can be done using the [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role.
* Install PHP version >= 7.3. This can be done using the [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role.
* On RHEL-compatible systems, enable the `httpd_can_connect_ldap` and `httpd_setrlimit` SELinux booleans. This can be done using the [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux) role.
* On RHEL-compatible systems, set the appropriate SELinux file contexts (have a look at `librenms__selinux__fcontexts__dependent_var` in the `defaults/main.yml`). This can be done using the [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux) role.

If you use the ["Setup LibreNMS" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_librenms.yml), this is automatically done for you.

## Tags

| Tag                  | What it does                     |
| ---                  | ------------                     |
| `librenms`           | Installs and configures LibreNMS |
| `librenms:configure` | Configures LibreNMS              |


## Mandatory Role Variables

| Variable                   | Description                                                         |
| --------                   | -----------                                                         |
| `librenms__database_login` | The user account for accessing the MySQL database.                  |
| `librenms__fqdn`           | The fully qualified domain name under which LibreNMS is accessible. |

Example:
```yaml
# mandatory
librenms__database_login:
  username: 'librenms'
  password: 'linuxfabrik'
librenms__fqdn: 'librenms.example.com'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `librenms__config_auth_mechanism` | Which authentication mechanism LibreNMS should use. Have a look at https://docs.librenms.org/Extensions/Authentication/. Note that only one mechanism can be active at the same time. Possible options: * `active_directory`<br> * `http-auth`<br> * `ldap`<br> * `ldap-authorization`<br> * `mysql`<br> * `sso` | `'mysql'` |
| `librenms__config_rrd_purge` | Number in days of how long to keep old rrd files. `0` disables this feature. | `0` |
| `librenms__config_update_channel` | Which update channel LibreNMS should use during automatic updates. Possible options:<br> * `master`<br> * `release` | `'release'` |
| `librenms__database_host` | The host on which the MySQL database is reachable. | `'localhost'` |
| `librenms__database_name` | The name of the SQL database. | `'librenms'` |

Example:
```yaml
# optional
librenms__config_auth_mechanism: 'mysql'
librenms__config_rrd_purge: 730
librenms__config_update_channel: 'release'
librenms__database_host: 'localhost'
librenms__database_name: 'librenms'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
