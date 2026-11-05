# Ansible Role linuxfabrik.lfops.nextcloud

This role installs Nextcloud including the tools needed by the most popular business plugins and [notify_push](https://github.com/nextcloud/notify_push). By default, the latest available version is installed. You can choose wether to use

* local block storage (default)
* S3 object storage backend (by providing `nextcloud__storage_backend_s3`)
* Swift object storage backend (by providing `nextcloud__storage_backend_swift`)

After installing Nextcloud, head over to your http(s)://nextcloud/index.php/settings/admin to set or verify your email server configuration. Afterwards, use the "Send email" button below the form to verify your settings.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* App updates are applied automatically by the `nextcloud-app-update.timer` (enabled by default, disable via `nextcloud__timer_app_update_enabled`). The timer runs `/usr/local/bin/nextcloud-app-update`, which first checks whether any app update is pending. Nextcloud is switched into maintenance mode only when there is something to update; when everything is up to date the instance keeps serving requests untouched. After updating, the recommended database migrations (`db:add-missing-indices`, `db:add-missing-columns`, `db:add-missing-primary-keys`) are applied. A failed run leaves maintenance mode disabled again, so the instance does not stay offline, and reports the failure to systemd.
* Before it changes anything, the role aborts if `nextcloud__database_login` is missing, or if it names the database user of the installed Nextcloud with another password, since the run would set that password for the MariaDB user and lock Nextcloud out of its database. The error message tells how to read the login from `config.php` with `occ`. `setup_nextcloud` runs this check before its first role.
* A fresh installation enforces two-factor authentication for all users (TOTP is enabled by default) and runs the Nextcloud mimetype migrations. An existing installation keeps its enforcement state. `/usr/local/bin/nextcloud-update` runs the mimetype migrations after each update.
* A fresh installation keeps deleted files and old file versions for at least 30 days and deletes them when space runs out (`auto, 30`). An existing installation keeps its retention.
* A fresh installation gets the full list of apps and app settings from the role defaults. On an existing installation, the role only manages the apps and settings of the inventory and the ones it relies on, so apps that the Nextcloud admin enables or disables in the web interface stay as they are. See `nextcloud__apps__host_var` and `nextcloud__app_configs__host_var`.
* `admin_audit` is enabled and writes `audit.log` to the data directory. Previews are limited to 2048 px at JPEG quality 60, and the web updater is disabled in favour of `/usr/local/bin/nextcloud-update`.
* MariaDB listens on `127.0.0.1` and `::1` only, which needs MariaDB 10.11 or newer. Redis and Valkey evict the least recently used keys when they are full. Change this with `nextcloud__mariadb_server__cnf_bind_address__dependent_var`, `nextcloud__redis__conf_maxmemory_policy` and `nextcloud__valkey__conf_maxmemory_policy`; in `setup_nextcloud`, these take precedence over the variables of the `mariadb_server`, `redis` and `valkey` roles.
* The mail server is taken from `nextcloud__mail_smtp_*`, which default to the relay host of the `postfix` role, and is only set while Nextcloud has no `mail_domain`, so a mail server configured by hand stays untouched. The SMTP password ends up in `config.php`.
* The installation downloads the release archive, its signature and the Nextcloud key on the Ansible controller and copies them to the target. The controller needs outbound access to `download.nextcloud.com` and `nextcloud.com`. The run aborts unless the key with the fingerprint `28806A878AE423A28372792ED75899B9A724937A` signed the archive. Under `--check`, the signature is not verified. An existing installation downloads nothing.
* `setup_nextcloud` keeps PHP sessions for 24 hours, deviating from the upstream default of 1440 seconds, because Nextcloud caps its `session_lifetime` at `session.gc_maxlifetime`. It lets the Nextcloud vHost wait 3600 seconds for PHP and for clients, deviating from the upstream default of 60 seconds to match `max_execution_time`, and removes the time limit for reading a request body, so that slow uploads and the assembly of large files are not cut off. A reverse proxy in front of Nextcloud needs the same `conf_timeout`, `conf_proxy_timeout` and `conf_request_read_timeout`. Change this with `nextcloud__php__ini_session_gc_maxlifetime__dependent_var` and `nextcloud__apache_httpd__vhosts__dependent_var`.
* The local cache lives in APCu, the distributed cache and file locking in Redis or Valkey, as in the Nextcloud admin manual and the Nextcloud All-in-One image. `setup_nextcloud` gives APCu 128 MB of shared memory and enables it for `occ` and the cron jobs, deviating from the upstream defaults of 32 MB and disabled, so that the CLI gets a local cache of its own instead of none. Change this with `nextcloud__php__ini_apc_shm_size__dependent_var` and `nextcloud__php__ini_apc_enable_cli__dependent_var`.
* This automatic update covers app updates only. Updating the Nextcloud server itself is a separate, manual step via `/usr/local/bin/nextcloud-update`.
* `/usr/local/bin/nextcloud-update` sets an Icinga2 downtime with the login from `nextcloud__icinga2_api_user_login`, which is stored as the systemd credential `nextcloud-update-icinga2-login.curlrc`. With systemd 251 and newer (RHEL 9 and newer, Debian 12 and newer, Ubuntu 24.04 and newer), it is encrypted in `/etc/credstore.encrypted/` with the host key `/var/lib/systemd/credential.secret`, which the backup does not include. On RHEL 8 and Ubuntu 22.04, it stays in plain text in `/etc/credstore/`, readable by root only. `nextcloud-update` therefore has to run as root. With a TPM2 chip, the credential is bound to the Secure Boot state: after a firmware or Secure Boot change, `nextcloud-update` updates Nextcloud without a downtime until the role runs again.


## Known Limitations

* RHEL 8 ships httpd 2.4.37, which reads `RequestReadTimeout` only from the default vHost of an address and port. There the time limit for reading a request body stays in place unless the default vHost sets `conf_request_read_timeout` as well.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* On RHEL-compatible systems, the EPEL repository must be enabled (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)).
* A web server (for example Apache httpd) must be installed, with a virtual host for Nextcloud (role: [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd)).
* MariaDB must be installed, in a version the installed Nextcloud supports, with the Nextcloud database and the user from `nextcloud__database_login` (role: [linuxfabrik.lfops.mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server)).
* PHP must be installed, in a version the installed Nextcloud supports (roles: [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) and [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php)).
* Valkey must be installed on RHEL 10, Redis on the other platforms, listening on the Unix socket in `nextcloud__redis_unixsocket` (roles: [linuxfabrik.lfops.valkey](https://github.com/Linuxfabrik/lfops/tree/main/roles/valkey), or [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) and [linuxfabrik.lfops.redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis)).
* Optional: Collabora (role: [linuxfabrik.lfops.collabora](https://github.com/Linuxfabrik/lfops/tree/main/roles/collabora)) provides online document editing.
* Optional: Coturn (role: [linuxfabrik.lfops.coturn](https://github.com/Linuxfabrik/lfops/tree/main/roles/coturn)) provides the TURN server for Nextcloud Talk.

These roles are not enabled by default; enable them via the playbook's skip variables if needed:

* The Collabora repository (role: [linuxfabrik.lfops.repo_collabora](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_collabora)) serves the Collabora packages from the official Collabora repository instead of the CODE repository.


## Requirements

Manual steps:

* Size the `/tmp` partition for your upload load. For example, to allow 5 simultaneous uploads of 10 GB each, set it to 50 GB+.
* Set up the reverse proxy in front of Nextcloud, including the path `/push/` for notify_push, before running `setup_nextcloud`, see "Reverse Proxy in Front of Nextcloud" below. Otherwise set `nextcloud__skip_notify_push` until it is in place.


## Reverse Proxy in Front of Nextcloud

The Nextcloud vHost of `setup_nextcloud` serves plain HTTP on port 80 (`nextcloud__vhost_virtualhost_port`), and [notify_push](https://github.com/nextcloud/notify_push) listens on port 7867. TLS ends on the reverse proxy, which forwards `https://<nextcloud__fqdn>/push/` to notify_push and everything else to the vHost. `setup_nextcloud` registers notify_push with `occ notify_push:setup https://<nextcloud__fqdn>/push`, which checks the whole way through the proxy, so the proxy has to forward `/push/` by then.

On the reverse proxy, forward with `ProxyPass`, the notify_push paths first, since Apache uses the first `ProxyPass` that matches:

```apache
ProxyPass           /push/ws ws://nextcloud-host.example.com:7867/ws
ProxyPass           /push/ http://nextcloud-host.example.com:7867/
ProxyPassReverse    /push/ http://nextcloud-host.example.com:7867/
ProxyPass           / http://nextcloud-host.example.com/ nocanon
ProxyPassReverse    / http://nextcloud-host.example.com/
```

Do not forward with `RewriteRule ... [proxy]`. mod_rewrite matches against the decoded path and passes it on decoded, so a `?` in a file name reaches Nextcloud as the start of the query string: renaming such a file in the web interface fails with "File not found", and the Windows client does not sync it. `ProxyPass` passes the path on encoded, and `nocanon` passes it on exactly as the client sent it. The characters that cause this are also on the list of characters the role forbids in file names (`forbidden_filename_characters` in `nextcloud__sysconfig__role_var`).

On the Nextcloud side, the reverse proxy goes into `config.php` (`trusted_proxies`, `overwriteprotocol` and so on, see the example of `nextcloud__sysconfig__host_var`), and the proxy needs the timeouts described under "How the Role Behaves".

If the reverse proxy runs the `apache-404` jail of the `fail2ban` role, exclude the 404 responses that Nextcloud and Collabora give in normal use: WebDAV and OCS answer with 404 for files that were just moved or deleted, for circles without an avatar and for the user status heartbeat, the login flow polls until the login in the browser is completed, and Collabora requests icons it does not ship. A user who restructures their files otherwise exceeds the jail's limit within seconds and is banned. Unauthenticated WebDAV and OCS requests get 401, so scanners still hit the jail. fail2ban removes the timestamp from the line before it applies these expressions, so do not match it with `\[...\]`:

```yaml
fail2ban__filter_apache_404_ignoreregex:
  - '^[^"]*"\S+ /(remote\.php/(dav|webdav)|ocs/v[12]\.php)/'
  - '^[^"]*"POST /index\.php/login/v2/poll '
  - '^[^"]*"GET /browser/[0-9a-f]+/images/'
```


## Connecting Collabora Online

`setup_nextcloud` installs Collabora Online (role `collabora`) on the Nextcloud host and allows `nextcloud__fqdn` as WOPI host, but leaves the connection to the reverse proxy and to Nextcloud to the inventory. The browser loads the editor from a hostname of its own, such as `office.example.com`, which the reverse proxy terminates like the Nextcloud hostname. Collabora itself serves plain HTTP on port 9980 (`collabora__coolwsd_ssl_termination: true`).

On the reverse proxy, forward the Collabora hostname to port 9980 of the Nextcloud host, with the WebSockets and without decoding encoded slashes:

```apache
AllowEncodedSlashes NoDecode
ProxyPreserveHost On
ProxyPass           /browser http://nextcloud-host.example.com:9980/browser retry=0
ProxyPassReverse    /browser http://nextcloud-host.example.com:9980/browser
ProxyPass           /hosting/discovery http://nextcloud-host.example.com:9980/hosting/discovery retry=0
ProxyPassReverse    /hosting/discovery http://nextcloud-host.example.com:9980/hosting/discovery
ProxyPass           /hosting/capabilities http://nextcloud-host.example.com:9980/hosting/capabilities retry=0
ProxyPassReverse    /hosting/capabilities http://nextcloud-host.example.com:9980/hosting/capabilities
ProxyPassMatch      "/cool/(.*)/ws$" ws://nextcloud-host.example.com:9980/cool/$1/ws nocanon
ProxyPass           /cool/adminws ws://nextcloud-host.example.com:9980/cool/adminws
ProxyPass           /cool http://nextcloud-host.example.com:9980/cool
ProxyPassReverse    /cool http://nextcloud-host.example.com:9980/cool
```

In Nextcloud, enable the Nextcloud Office app and point it at the Collabora hostname. Collabora calls back into Nextcloud through the reverse proxy. Depending on `trusted_proxies` (and on `mod_remoteip`, see `apache_httpd__mod_remoteip_internal_proxy`), Nextcloud sees either the reverse proxy or the Nextcloud host itself as the sender, since the proxy passes the Nextcloud host in `X-Forwarded-For`. The WOPI allow list therefore names both; otherwise documents fail to load with "Unauthorized WOPI host", and `nextcloud.log` reports "WOPI request denied from ...":

```yaml
nextcloud__apps__host_var:
  - name: 'richdocuments'
    state: 'enabled'
nextcloud__app_configs__host_var:
  - key: 'richdocuments public_wopi_url'
    value: 'https://office.example.com'
    state: 'present'
  - key: 'richdocuments wopi_allowlist'
    value: '192.0.2.7,192.0.2.10' # IPs of the reverse proxy and the Nextcloud host
    state: 'present'
  - key: 'richdocuments wopi_url'
    value: 'https://office.example.com'
    state: 'present'
```


## Tags

`nextcloud`

* Installs and configures the whole Nextcloud server.
* Triggers: none.

`nextcloud:apps`

* Enables, disables apps and sets their settings.
* Triggers: none.

`nextcloud:configure`

* Deploys the `nextcloud__sysconfig__*_var` and configures notify_push.
* Triggers: none.

`nextcloud:cron`

* Sets the Nextcloud background job setting to cron, deploys and manages the state of `nextcloud-app-update.{service,timer}`, `nextcloud-app-update` script, `nextcloud-jobs.{service,timer}`, `nextcloud-ldap-show-remnants.{service,timer}`, `nextcloud-ldap-show-remnants` script, `nextcloud-scan-files.{service,timer}`.
* Triggers: none.

`nextcloud:notify_push`

* Configures notify_push.
* Triggers: none.

`nextcloud:scripts`

* Deploys `/usr/local/bin/nextcloud-update` and stores the Icinga2 API login it uses as a systemd credential.
* Triggers: none.

`nextcloud:state`

* Manages the state of `nextcloud-jobs.timer`, `nextcloud-app-update.timer`, `nextcloud-scan-files.timer`, `nextcloud-ldap-show-remnants.timer`.
* Triggers: none.


## Mandatory Role Variables

`nextcloud__database_login`

* The MariaDB user Nextcloud connects as. The playbook `setup_nextcloud` creates it with the privileges the Nextcloud installer would grant, on the Nextcloud database only. Nextcloud takes it over at the installation; an existing installation keeps the database user it was set up with. For an existing installation, take the login from `sudo -u apache php /var/www/html/nextcloud/occ config:system:get dbuser` and `... dbpassword`.
* Type: Dictionary.
* Subkeys:

    * `username`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Mandatory. Password.
        * Type: String.

`nextcloud__fqdn`

* The FQDN of the Nextcloud instance.
* Type: String.

`nextcloud__users`

* List of dictionaries containing the user accounts to create. Attention: The first user has to be the primary administrator account.
* Type: List of dictionaries.
* Subkeys:

    * `username`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Mandatory. Password.
        * Type: String.

    * `group`:

        * Optional. Group of the user.
        * Type: String.
        * Default: unset

    * `settings`:

        * Optional. Nextcloud settings for the user. Have a look at the example below.
        * Type: List of strings.
        * Default: `[]`

`nextcloud__version`

* Which version to download for a new installation. One of `'latest-XX'`, such as `'latest-35'`, or `'nextcloud-XX.X.XX'`. Have a look at https://download.nextcloud.com/server/releases/ for a list of available releases. Updates of an installed Nextcloud run through `/usr/local/bin/nextcloud-update`, not through this variable.
* Type: String.

Example:
```yaml
# mandatory
nextcloud__database_login:
  username: 'nextcloud'
  password: 'linuxfabrik'
nextcloud__fqdn: 'cloud.example.com'
nextcloud__users:
  # first user has to be the admin account
  - username: 'nextcloud-admin'
    password: 'linuxfabrik'
    group: 'admin'
    settings:
      - 'core lang en'
      - 'core locale de_CH'
      - 'core timezone Europe/Zurich'
      - 'files quota "50 MB"'
      - 'firstrunwizard show 0'
      - 'settings email info@example.org'
nextcloud__version: 'latest-35'
```


## Optional Role Variables

`nextcloud__app_configs__host_var` / `nextcloud__app_configs__group_var`

* List of dictionaries containing key-value pairs for configuring apps in Nextcloud.
* The role defaults apply in full on a fresh installation only. On an existing installation, the role sets the entries of the inventory and the settings it relies on (`dav buildCalendarSearchIndex`, `password_policy enforceHaveIBeenPwned`, `password_policy minLength`, `preview jpeg_quality`), and leaves all other settings to the Nextcloud admin.
* Type: List of dictionaries.
* Default: Have a look at [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/nextcloud/defaults/main.yml)
* Deviates from the upstream default `'no'` for `support hide-app`: the Support section is hidden from the administration settings. Set it to `'no'` to enter an Enterprise subscription key there. The `support` app only accepts the string `'yes'`, not a boolean.
* Deviates from the upstream default `80` for `preview jpeg_quality`: previews are generated at quality 60, as in the Nextcloud All-in-One image, which keeps them smaller.
* Subkeys:

    * `key`:

        * Mandatory. The app and the name of its config option, separated by a space, for example `password_policy minLength`.
        * Type: String.

    * `value`:

        * Mandatory. The configuration value.
        * Type: String.

    * `type`:

        * Optional. Type of the value, either `array`, `boolean`, `float`, `integer` or `string`.
        * Type: String.
        * Default: `'string'`

    * `state`:

        * Optional. State of the config option, either `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`nextcloud__apps__host_var` / `nextcloud__apps__group_var`

* List of dictionaries containing Nextcloud apps to install, enable, disable or remove.
* An entry overrides only the subkeys it sets. The role default disables some apps, for example `activity`, `notifications` and `systemtags`; an entry for such an app without `state` keeps it disabled, so set `state: 'enabled'` explicitly.
* The role defaults apply in full on a fresh installation only. On an existing installation, the role manages the apps of the inventory and the apps it relies on (`admin_audit`, `notify_push`, `password_policy`, `support`, `twofactor_totp`), and leaves all other apps to the Nextcloud admin, who may enable or disable them in the web interface.
* Type: List of dictionaries.
* Default: Have a look at [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/nextcloud/defaults/main.yml)
* Subkeys:

    * `name`:

        * Mandatory. The app name.
        * Type: String.

    * `force`:

        * Optional. Set to `true` to install the app regardless of the Nextcloud version requirement.
        * Type: Bool.
        * Default: `false`

    * `state`:

        * Optional. State of the app:

            * `absent`: Removes the app.
            * `disabled`: Disables the app if it is enabled.
            * `enabled`: Installs the app if it is missing, and enables it.
            * `present`: Installs the app if it is missing, but leaves it disabled.

        * Type: String.
        * Default: `'enabled'`

`nextcloud__database_host`

* Host where MariaDB is located. The role writes it to `dbhost` in `config.php` on every run. With `'localhost'`, it writes the path to the MariaDB socket instead, so Nextcloud and notify_push both connect through the socket.
* Type: String.
* Default: `'localhost'`

`nextcloud__database_login_host`

* Host from which the MariaDB user in `nextcloud__database_login` may connect.
* Type: String.
* Default: `'localhost'`

`nextcloud__database_name`

* Name of the Nextcloud database in MariaDB.
* Type: String.
* Default: `'nextcloud'`

`nextcloud__datadir`

* Where to store the user files. Nextcloud takes it over at the installation; changing it afterwards does not move an existing data directory.
* Type: String.
* Default: `'/data'`

`nextcloud__icinga2_api_url`

* The URL of the Icinga2 API (usually on the Icinga2 Master). This will be used to set a downtime for the corresponding host and all its services in the `/usr/local/bin/nextcloud-update` script.
* Type: String.
* Default: `'https://{{ icinga2_agent__icinga2_master_host | d(icinga2_agent__icinga2_master_cn | d("")) }}:{{ icinga2_agent__icinga2_master_port | d(5665) }}'`

`nextcloud__icinga2_api_user_login`

* The Icinga2 API User to set the downtime for the corresponding host and all its services in the `/usr/local/bin/nextcloud-update` script. Defaults to the downtime API user the `icinga2_master` role creates. When neither is set, no downtime is set.
* Type: Dictionary.
* Default: `'{{ icinga2_master__downtime_api_user | d({}) }}'`

`nextcloud__icinga2_hostname`

* The hostname of the Icinga2 host on which the downtime should be set.
* Type: String.
* Default: `'{{ ansible_facts["nodename"] }}'`

`nextcloud__jobs_timeout_start_sec`

* Time the `nextcloud-jobs.service` may take to finish before systemd considers the start-up failed and kills it. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format.
* Type: String.
* Default: `'10m'`

`nextcloud__mail_from`

* Sender used in the `From:` header and as the envelope sender (`sendmail -f`) of the monthly `ldap:show-remnants` report. Defaults to the global `mailto_root__from`.
* Type: String.
* Default: `'{{ mailto_root__from }}'`

`nextcloud__mail_recipients`

* Recipients of the monthly `ldap:show-remnants` report (users removed from LDAP that still have remnants in Nextcloud) sent by `/usr/local/bin/nextcloud-ldap-show-remnants`. Defaults to the global `mailto_root__to`. The report is always printed to stdout; when recipients are set it is additionally mailed to them.
* Type: List.
* Default: `'{{ mailto_root__to | d([]) }}'`

`nextcloud__mail_smtp_host`

* SMTP server Nextcloud sends its mails through. Without a value, the role does not configure a mail server.
* Type: String.
* Default: The host part of `postfix__relayhost`

`nextcloud__mail_smtp_password`

* Password for the SMTP server. Without a value, Nextcloud does not authenticate.
* Type: String.
* Default: `'{{ postfix__relayhost_password | d("") }}'`

`nextcloud__mail_smtp_port`

* Port of the SMTP server.
* Type: Number.
* Default: The port part of `postfix__relayhost`, otherwise `25`

`nextcloud__mail_smtp_username`

* Username for the SMTP server.
* Type: String.
* Default: `'{{ postfix__relayhost_username | d(nextcloud__mail_from) }}'`

`nextcloud__on_calendar_app_update`

* Time to update the Nextcloud apps. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format.
* Type: String.
* Default: `'06,18,23:{{ 59 | random(seed=inventory_hostname) }}'`

`nextcloud__on_calendar_jobs`

* Run interval of OCC background jobs. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format.
* Type: String.
* Default: `'*:0/5'`

`nextcloud__on_calendar_scan_files`

* Run interval of rescanning filesystem. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format.
* Type: String.
* Default: `'*:50:15'`

`nextcloud__redis_group`

* Group that may connect to the Unix socket of Redis or Valkey. The role adds the web server user to it.
* Type: String.
* Default: `'valkey'` on RHEL 10, `'redis'` elsewhere

`nextcloud__redis_unixsocket`

* Unix socket through which Nextcloud reaches Redis or Valkey for the distributed cache and file locking (the local cache is APCu), the one that `setup_nextcloud` installs. Set it to `''` to connect to `127.0.0.1:6379` over TCP instead.
* Type: String.
* Default: `'/run/valkey/valkey.sock'` on RHEL 10, `'/run/redis/redis.sock'` on RHEL 8 and 9, `'/run/redis/redis-server.sock'` on Debian and Ubuntu

`nextcloud__skip_apps`

* Completely skips the management of Nextcloud apps. Set this to prevent changes via the WebGUI from being overwritten.
* Type: Bool.
* Default: `false`

`nextcloud__skip_notify_push`

* Skips the configuration of notify_push. Use this if the DNS setup is not done yet when running the role.
* Type: Bool.
* Default: `false`

`nextcloud__storage_backend_s3`

* S3 Storage Backend. If ommitted, local storage is used. If both S3 and Swift are provided, S3 is configured. Have a look at the example below on how to configure.
* Type: Dictionary.
* Default: unset

`nextcloud__storage_backend_swift`

* Swift Storage Backend. If ommitted, local storage is used. If both S3 and Swift are provided, S3 is configured. Have a look at the example below on how to configure.
* Type: Dictionary.
* Default: unset

`nextcloud__sysconfig__host_var` / `nextcloud__sysconfig__group_var`

* List of dictionaries containing key-value pairs for Nextcloud system config settings. Also use this setting to configure [Nextcloud behind a reverse proxy](https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/reverse_proxy_configuration.html), have a look at the example below on how to configure.
* Type: List of dictionaries.
* Default: Have a look at [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/nextcloud/defaults/main.yml)
* Subkeys:

    * `key`:

        * Mandatory. The name of the config option to set.
        * Type: String.

    * `value`:

        * Mandatory. The configuration value.
        * Type: String.

    * `type`:

        * Optional. The type of the configuration value.
        * Type: String.
        * Default: `'string'`

    * `state`:

        * Optional. Either `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`nextcloud__timer_app_update_enabled`

* Enables/disables Systemd-Timer for updating apps.
* Type: Bool.
* Default: `true`

`nextcloud__timer_jobs_enabled`

* Enables/disables Systemd-Timer for running OCC background jobs.
* Type: Bool.
* Default: `true`

`nextcloud__timer_ldap_show_remnants_enabled`

* Enables/disables Systemd-Timer for mailing once a month which users are not available on LDAP anymore, but have remnants in Nextcloud. Will only be applied if the app `users_ldap` is present.
* Type: Bool.
* Default: `true`

`nextcloud__timer_scan_files_enabled`

* Enables/disables Systemd-Timer for re-scanning the Nextcloud files.
* Type: Bool.
* Default: `true`

`nextcloud__twofactor_enforced`

* Enforce two-factor authentication for all users on a fresh installation. Has no effect on an existing installation; use `twofactor_enforced` with the value `'true'` in `nextcloud__sysconfig__host_var` there.
* Type: Bool.
* Default: `true`

`nextcloud__vhost_virtualhost_ip`

* Used within the `<VirtualHost {{ virtualhost_ip }}:{{ virtualhost_port }}>` directive.
* Type: String.
* Default: `*`

`nextcloud__vhost_virtualhost_port`

* Used within the `<VirtualHost {{ virtualhost_ip }}:{{ virtualhost_port }}>` directive.
* Type: Number.
* Default: `80`

Example:
```yaml
# optional
nextcloud__app_configs__host_var:
  - key: 'core shareapi_default_expire_date'
    value: 'yes'
    state: 'present'
  - key: 'theming imprintUrl'
    value: 'https://www.example.com'
    state: 'present'
nextcloud__apps__host_var:
  - name: 'activity'
    state: 'enabled'
  - name: 'deck'
    state: 'enabled'
  - name: 'weather_status'
    state: 'disabled'
nextcloud__database_host: 'localhost'
nextcloud__database_login_host: 'localhost'
nextcloud__database_name: 'nextcloud'
nextcloud__datadir: '/data'
nextcloud__icinga2_api_url: 'https://icinga.example.com:5665'
nextcloud__icinga2_api_user_login:
  username: 'downtime-user'
  password: 'linuxfabrik'
nextcloud__icinga2_hostname: 'myhost.example.com'
nextcloud__jobs_timeout_start_sec: '10m'
nextcloud__mail_from: '{{ mailto_root__from | d("") }}'
nextcloud__mail_recipients:
  - 'info@example.com'
nextcloud__on_calendar_app_update: '06,18,23:{{ 59 | random(seed=inventory_hostname) }}'
nextcloud__on_calendar_jobs: '*:0/5'
nextcloud__on_calendar_scan_files: '*:50:15'
nextcloud__skip_apps: true
nextcloud__skip_notify_push: true
# if not local storage, then either one of s3 ...
nextcloud__storage_backend_s3:
  autocreate: true
  bucket: 'mybucket'
  hostname: 's3.pub1.infomaniak.cloud'
  key: '428fc7e2-b532-4704-9df0-a764c7253a15'
  port: 9000
  region: 'us-east-1'
  secret: 'linuxfabrik'
  use_path_style: true
  use_ssl: true
# ... or swift
nextcloud__storage_backend_swift:
  autocreate: true
  bucket: 'mybucket'
  region: 'dc3-a'
  scope_project_domain_name: 'Default'
  scope_project_name: 'PCP-XXXXXX'
  service_name: 'swift'
  url: 'https://api.pub1.infomaniak.cloud/identity/v3'
  user_domain_name: 'Default'
  user_name: 'PCU-XXXXXX'
  user_password: 'linuxfabrik'
nextcloud__sysconfig__host_var:
  - key: 'check_for_working_wellknown_setup'
    value: 'true'
    type: 'boolean'
    state: 'present'
  - key: 'updatechecker'
    value: 'false'
    type: 'boolean'
    state: 'present'
  - key: 'redis timeout'
    value: '0.5'
    type: 'double'
    state: 'present'
  # reverse proxy config
  - key: 'overwrite.cli.url'
    value: 'https://cloud.example.com'
    state: 'present'
  - key: 'overwritecondaddr'
    value: '^192\.0\.2\.7$' # IP of the reverse proxy
    state: 'present'
  - key: 'overwritehost'
    value: 'cloud.example.com'
    state: 'present'
  - key: 'overwriteprotocol'
    value: 'https'
    state: 'present'
  - key: 'overwritewebroot'
    value: '/'
    state: 'present'
  - key: 'trusted_proxies 0'
    value: '192.0.2.7' # IP of the reverse proxy
    state: 'present'

nextcloud__timer_app_update_enabled: true
nextcloud__timer_jobs_enabled: true
nextcloud__timer_ldap_show_remnants_enabled: true
nextcloud__timer_scan_files_enabled: true
nextcloud__twofactor_enforced: true
nextcloud__vhost_virtualhost_ip: '127.0.0.1'
nextcloud__vhost_virtualhost_port: '81'
```


## Troubleshooting

**The run aborts with `Nextcloud XX needs PHP X.Y or newer, but older than X.Z, and MariaDB XX.Y or newer.`**

* The role compares the installed PHP and MariaDB with what the installed Nextcloud major version requires, before it changes anything, and aborts if they do not fit. The message names the versions it expects and the ones it found. Nextcloud itself refuses to run on a PHP outside that range. Upgrade PHP (for example via `repo_remi__enabled_php_version`) or MariaDB (`repo_mariadb__version`), then run the role again.

**The run aborts with `Nextcloud XX is not supported by this role.`**

* The role knows the requirements of the Nextcloud major versions listed in the message only. Pin `nextcloud__version` to a supported major version for a new installation, or add the requirements of the new major version to `__nextcloud__requirements` in `vars/main.yml`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
