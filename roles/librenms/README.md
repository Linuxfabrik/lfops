# Ansible Role linuxfabrik.lfops.librenms

This role installs and configures [LibreNMS](https://www.librenms.org/).


*Available since LFOps `2.0.0`.*


## How the Role Behaves

LibreNMS stores its time series in RRD files below `/opt/librenms/rrd`. By default the role puts [RRDCached](https://docs.librenms.org/Extensions/RRDCached/) in front of them, which collects the updates of a poll cycle in memory and writes them out every 30 minutes instead of on every update. This typically cuts the disk I/O of the poller by 30% to 40%.

* The RRD files stay where they are and keep their format, so enabling or disabling RRDCached needs no data migration. Only who writes them changes.
* RRDCached runs as `librenms` and listens on the Unix socket `/run/rrdcached.sock`. It is not reachable over the network, and the socket is deliberately not in `/tmp`, which `httpd` and `php-fpm` cannot see because both run with `PrivateTmp=true`.
* The role configures the `rrdcached.service` of the `rrdtool` package with a systemd drop-in and disables the `rrdcached.socket` unit shipped alongside it, because socket activation would make RRDCached ignore the configured socket path.
* On RHEL-compatible systems RRDCached needs the `rrdcached_librenms` SELinux policy module, without which it cannot write the RRD files and the web interface cannot draw graphs. The module is declared in `librenms__selinux__modules__dependent_var` and deployed by the `selinux` role, so skipping that role in the playbook leaves RRDCached without it.
* Up to 30 minutes of collected data live in memory only. RRDCached journals them to `/var/tmp` and replays the journal after a crash.
* Setting `librenms__rrdcached_enabled` to `false` stops and disables `rrdcached.service`, which flushes the collected data to the RRD files on the way out, and points LibreNMS at the files directly. The systemd drop-in, the `rrdcached_librenms` SELinux policy module and the RRD files themselves stay in place, so the switch can be reversed with another run of the role.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* Python 3, and the python3-policycoreutils module (required for the SELinux Ansible tasks) must be installed (role: [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils)).
* MariaDB must be installed, with a database and a user for said database created (role: [linuxfabrik.lfops.mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server)).
* A web server (for example Apache httpd) must be installed, with a virtual host for LibreNMS configured (role: [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd)).
* PHP version >= 8.4 must be installed (role: [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php)).
* The Python modules the poller and the discovery need must be installed (have a look at `librenms__python__modules__dependent_var` in the `defaults/main.yml`) (role: [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python)).
* On RHEL-compatible systems, the SELinux booleans in `librenms__selinux__booleans__dependent_var` must be enabled (role: [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux)).
* On RHEL-compatible systems, the appropriate SELinux file contexts must be set (have a look at `librenms__selinux__fcontexts__dependent_var` in the `defaults/main.yml`) (role: [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux)).
* On RHEL-compatible systems, the `http_fping` and `rrdcached_librenms` SELinux policy modules must be installed (have a look at `librenms__selinux__modules__dependent_var` in the `defaults/main.yml`) (role: [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux)).


## Tags

`librenms`

* Installs and configures LibreNMS.
* Triggers: none.

`librenms:configure`

* Configures LibreNMS.
* Triggers: none.

`librenms:rrdcached`

* Installs and configures RRDCached, and manages its service.
* Triggers: rrdcached.service restart.


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

* A list of trusted reverse proxy IPs or CIDR ranges, joined into the comma separated `APP_TRUSTED_PROXIES` setting in `/opt/librenms/.env`, and written on every run. Have a look at https://docs.librenms.org/Support/Environment-Variables/. The empty default trusts no proxy at all, so LibreNMS ignores the `X-Forwarded-*` headers of any host: list your proxy here if one sits in front of LibreNMS, otherwise client addresses and the detected protocol are those of the proxy.
* Type: List.
* Default: `[]`
* Deviates from the upstream default `127.0.0.1`: a proxy on the LibreNMS host itself is not the common case in LFOps, and a host that trusts one accepts spoofed `X-Forwarded-For` headers from anything able to reach it locally.

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

`librenms__rrdcached_enabled`

* Whether LibreNMS reads and writes its RRD files through RRDCached. Set this to `false` to stop and disable RRDCached and have LibreNMS access the files directly. Have a look at "How the Role Behaves" above.
* Type: Boolean.
* Default: `true`

`librenms__rrdcached_service_enabled`

* Enables or disables the RRDCached service, analogous to `systemctl enable/disable --now`. Only used if `librenms__rrdcached_enabled` is `true`.
* Type: Bool.
* Default: `true`

`librenms__rrdcached_service_state`

* Changes the state of the RRDCached service, analogous to `systemctl start/stop/restart/reload`. Only used if `librenms__rrdcached_enabled` is `true`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `librenms__rrdcached_service_enabled` is `true`, else `'stopped'`

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
librenms__rrdcached_enabled: true
librenms__rrdcached_service_enabled: true
librenms__rrdcached_service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
