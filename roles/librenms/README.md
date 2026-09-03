# Ansible Role linuxfabrik.lfops.librenms

This role installs and configures [LibreNMS](https://www.librenms.org/).


*Available since LFOps `2.0.0`.*


## How the Role Behaves

The role installs LibreNMS from a git checkout on the target host, not on the Ansible controller, and checks out the latest upstream release on every run. The version is not pinned, so a run updates an existing installation to whatever upstream currently offers. Between runs LibreNMS keeps itself up to date as well: the cron jobs are the ones upstream ships, and their nightly `daily.sh` updates the code on its own. `librenms__config_update_channel` selects the channel it follows.

`librenms__url` is the one place the address of the instance is configured. The role writes it to `base_url` in `/opt/librenms/config.php`, which overrides the URL LibreNMS otherwise detects from each request, and to `APP_URL` in `/opt/librenms/.env`, which Laravel uses wherever there is no request to detect from, alert notifications above all. Both are needed: LibreNMS builds part of its links itself and leaves the rest to Laravel. Note that `base_url` ties the instance to that address, so opening the web interface under a different name makes the built-in validation fail rather than only warn. `config.php` outranks the `config` database table, so a `base_url` set through the web interface or `lnms config:set` on an existing host is masked from the next run onwards.

The Python packages LibreNMS lists in its `requirements.txt` are installed with `pip` into the user site of the `librenms` user, `/opt/librenms/.local`. That is where LibreNMS looks for them itself: its nightly `daily.sh` runs the same `pip` call, and the requirements check behind `validate.php` reads the installed distribution metadata from there. Distribution packages cannot cover this, because no RHEL release ships `command_runner` and the `psutil` of RHEL 8 and 9 is older than LibreNMS requires. On RHEL 8 the role installs a current `pip` into that same user site first, since the `pip` of the distribution cannot use the prebuilt `psutil` wheel and would need a compiler on the host to build it. A host that carries such packages from an earlier manual `pip install` as `root` keeps them; they are outranked by the user site for LibreNMS, but `pip3 uninstall` as `root` is worth running once so only one place provides them.

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


## Requirements

* Outbound HTTPS access from the target host to `github.com`, both for the release lookup and for the git checkout, to `packagist.org` for the PHP dependencies Composer installs, and to `pypi.org` and `files.pythonhosted.org` for the Python packages `pip` installs. The role does no downloading on the Ansible controller.


## Post-Installation Steps

* The role prepares the database credentials in `/opt/librenms/.env`, but creates neither the database schema nor an account to log in with. Open `<librenms__url>/install` and follow the web installer, which does both. An administrator can also be added on the host with `lnms user:add <username>`.


## Tags

`librenms`

* Installs and configures LibreNMS.
* Triggers: rrdcached.service restart.

`librenms:configure`

* Deploys the LibreNMS configuration, the scheduled jobs and the logrotate configuration.
* Triggers: none.

`librenms:cron`

* Deploys the cron jobs and the units of the LibreNMS scheduler.
* Triggers: none.

`librenms:logrotate`

* Deploys the logrotate configuration.
* Triggers: none.

`librenms:rrdcached`

* Installs and configures RRDCached, and manages its service.
* Triggers: rrdcached.service restart.

`librenms:state`

* Manages the state of the LibreNMS scheduler timer (start, stop, enable, disable).
* Triggers: none.


## Mandatory Role Variables

`librenms__database_login`

* The user account for accessing the MySQL database.
* Type: Dictionary.
* Subkeys:

    * `username`:

        * Mandatory. The database user.
        * Type: String.

    * `password`:

        * Mandatory. The password of the database user.
        * Type: String.

`librenms__url`

* The URL under which LibreNMS is reachable, including the scheme and, where applicable, a port or a subdirectory. It is the single source for three settings: the `ServerName` of the vHost gets its host part, `APP_URL` in `/opt/librenms/.env` and `base_url` in `/opt/librenms/config.php` get the URL itself. Use the URL your users type in the browser, which with a TLS-terminating reverse proxy in front is an `https://` URL even though Apache httpd on the host serves plain HTTP.
* Type: String.

Example:
```yaml
# mandatory
librenms__database_login:
  username: 'librenms'
  password: 'linuxfabrik'
librenms__url: 'https://librenms.example.com'
```


## Optional Role Variables

`librenms__config_app_trusted_proxies`

* A list of trusted reverse proxy IPs or CIDR ranges, joined into the comma separated `APP_TRUSTED_PROXIES` setting in `/opt/librenms/.env`, and written on every run. Have a look at https://docs.librenms.org/Support/Environment-Variables/. The empty default trusts no proxy at all, so LibreNMS ignores the `X-Forwarded-*` headers of any host: list your proxy here if one sits in front of LibreNMS, otherwise client addresses and the detected protocol are those of the proxy. Have a look at "Troubleshooting" below for how to check what a running instance makes of the setting.
* Type: List.
* Default: `[]`
* Deviates from the upstream default `127.0.0.1`: a proxy on the LibreNMS host itself is not the common case in LFOps, and a host that trusts one accepts spoofed `X-Forwarded-For` headers from anything able to reach it locally.

`librenms__config_auth_mechanism`

* Which authentication mechanism LibreNMS should use. Have a look at https://docs.librenms.org/Extensions/Authentication/. Note that only one mechanism can be active at the same time. Possible options: `active_directory`, `http-auth`, `ldap`, `ldap-authorization`, `mysql`, `sso`.
* Type: String.
* Default: `'mysql'`

`librenms__config_rrd_purge`

* Number in days of how long to keep old rrd files. `0` disables this feature.
* Type: Number.
* Default: `0`

`librenms__config_session_secure_cookie`

* Whether LibreNMS marks its session cookie as secure, so a browser only sends it over HTTPS. Sets `SESSION_SECURE_COOKIE` in `/opt/librenms/.env` on every run. Defaults to `true` as soon as `librenms__url` names an `https://` URL, which is the host's own statement that it serves HTTPS. Do not set it to `true` on a host that is reachable over plain HTTP only: the browser then never sends the cookie back and the login fails with "419 Page Expired". LibreNMS is a Laravel application and issues this cookie itself, so `php__ini_session_cookie_secure` of the `php` role does not reach it.
* Type: Boolean.
* Default: `true` if `librenms__url` starts with `https://`, else `false`

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
* Deviates from the upstream default `false`: LibreNMS writes every RRD file on every poll cycle without it, which is the bulk of the disk I/O of a poller and the first thing to hurt once a host monitors more than a handful of devices.

`librenms__rrdcached_service_enabled`

* Enables or disables the RRDCached service, analogous to `systemctl enable/disable --now`. Only used if `librenms__rrdcached_enabled` is `true`.
* Type: Bool.
* Default: `true`

`librenms__rrdcached_service_state`

* Changes the state of the RRDCached service, analogous to `systemctl start/stop/restart/reload`. Only used if `librenms__rrdcached_enabled` is `true`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `librenms__rrdcached_service_enabled` is `true`, else `'stopped'`

`librenms__scheduler_service_enabled`

* Enables or disables the timer of the LibreNMS scheduler, analogous to `systemctl enable/disable --now`. The scheduler runs the maintenance and alerting jobs of LibreNMS.
* Type: Bool.
* Default: `true`

`librenms__scheduler_service_state`

* Changes the state of the timer of the LibreNMS scheduler, analogous to `systemctl start/stop/restart/reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `librenms__scheduler_service_enabled` is `true`, else `'stopped'`

Example:
```yaml
# optional
librenms__config_app_trusted_proxies:
  - '192.0.2.0/24'
  - '198.51.100.7'
librenms__config_auth_mechanism: 'mysql'
librenms__config_rrd_purge: 730
librenms__config_session_secure_cookie: true
librenms__config_update_channel: 'release'
librenms__database_host: 'localhost'
librenms__database_name: 'librenms'
librenms__rrdcached_enabled: true
librenms__rrdcached_service_enabled: true
librenms__rrdcached_service_state: 'started'
librenms__scheduler_service_enabled: true
librenms__scheduler_service_state: 'started'
```


## Troubleshooting

**Logs and access control show the address of the reverse proxy instead of the client's**

* LibreNMS honours the `X-Forwarded-*` headers only from an address listed in `librenms__config_app_trusted_proxies`, and the empty default trusts none. To check what a running instance does, log in through the proxy and open "Auth History" under Settings in the web interface: the "IP Address" column of the top row is the address LibreNMS derived from the request, so it has to show the client and not the proxy. Reading that page requires the admin or the global-read role.
* To confirm that a host which is not listed cannot forge an address, repeat the login from such a host with an `X-Forwarded-For` header of its own. The row in "Auth History" has to carry that host's own address; if it carries the forged one, the host is trusted.
* `sudo -u librenms lnms config:show trustedproxy` prints the list as the application resolved it. This tells an unset `APP_TRUSTED_PROXIES`, where LibreNMS falls back to trusting `127.0.0.1`, apart from one that is deliberately empty.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
