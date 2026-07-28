# Ansible Role linuxfabrik.lfops.librenms

This role installs and configures [LibreNMS](https://www.librenms.org/).


*Available since LFOps `2.0.0`.*


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* Python 3, and the python3-policycoreutils module (required for the SELinux Ansible tasks) must be installed (role: [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils)).
* MariaDB must be installed, with a database and a user for said database created (role: [linuxfabrik.lfops.mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server)).
* A web server (for example Apache httpd) must be installed, with a virtual host for LibreNMS configured (role: [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd)).
* PHP version >= 7.3 must be installed (role: [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php)).
* On RHEL-compatible systems, the `httpd_can_connect_ldap` and `httpd_setrlimit` SELinux booleans must be enabled (role: [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux)).
* On RHEL-compatible systems, the appropriate SELinux file contexts must be set (have a look at `librenms__selinux__fcontexts__dependent_var` in the `defaults/main.yml`) (role: [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux)).


## Tags

`librenms`

* Installs and configures LibreNMS.
* Triggers: none.

`librenms:configure`

* Configures LibreNMS.
* Triggers: none.


## Mandatory Role Variables

`librenms__database_login`

* The user account for accessing the MySQL database.
* Type: Dictionary.

`librenms__fqdn`

* The fully qualified domain name under which LibreNMS is accessible.
* Type: String.

Example:
```yaml
# mandatory
librenms__database_login:
  username: 'librenms'
  password: 'linuxfabrik'
librenms__fqdn: 'librenms.example.com'
```


## Optional Role Variables

`librenms__config_app_trusted_proxies`

* A list of trusted reverse proxy IPs or CIDR ranges, joined into the comma separated `APP_TRUSTED_PROXIES` setting in `/opt/librenms/.env`. Have a look at https://docs.librenms.org/Support/Environment-Variables/. An empty list leaves the setting untouched.
* Type: List.
* Default: `[]`

`librenms__config_app_url`

* The base URL used for generated URLs, for example when running behind a reverse proxy. Have a look at https://docs.librenms.org/Support/Environment-Variables/. An empty string leaves the `APP_URL` setting in `/opt/librenms/.env` untouched.
* Type: String.
* Default: `''`

`librenms__config_auth_mechanism`

* Which authentication mechanism LibreNMS should use. Have a look at https://docs.librenms.org/Extensions/Authentication/. Note that only one mechanism can be active at the same time. Possible options: `active_directory`, `http-auth`, `ldap`, `ldap-authorization`, `mysql`, `sso`.
* Type: String.
* Default: `'mysql'`

`librenms__config_rrd_purge`

* Number in days of how long to keep old rrd files. `0` disables this feature.
* Type: Number.
* Default: `0`

`librenms__config_update_channel`

* Which update channel LibreNMS should use during automatic updates. Possible options: `master`, `release`.
* Type: String.
* Default: `'release'`

`librenms__database_host`

* The host on which the MySQL database is reachable.
* Type: String.
* Default: `'localhost'`

`librenms__database_name`

* The name of the SQL database.
* Type: String.
* Default: `'librenms'`

Example:
```yaml
# optional
librenms__config_app_trusted_proxies:
  - '192.0.2.0/24'
  - '198.51.100.7'
librenms__config_app_url: 'https://librenms.example.com'
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
