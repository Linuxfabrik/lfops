# Ansible Role linuxfabrik.lfops.php

This role installs and configures PHP (and PHP-FPM) on the system, optionally with additional modules.

By default this role does not select a PHP version. It installs the latest version the configured repos offer. On RedHat that is deterministic, because the module stream pins the version at repo level: use [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) beforehand to choose it.

Debian has no repo-level equivalent. Its unversioned metapackages (`php-cli`, `php-fpm`, `php-curl`, ...) point at whatever the configured repo declares as its default, which never moves within a Debian release but does move with the [sury](https://packages.sury.org/php/) repo, whenever sury promotes a new PHP version. On a sury host an ordinary `apt upgrade` therefore migrates PHP to a new major version without anyone deciding to. Set `php__version` to prevent that.

Consuming roles that inject `php__modules__dependent_var` on Debian must build the package names from the detected version, for example `php{{ __php__installed_version }}-curl`, because the unversioned names would reintroduce exactly that drift. See `roles/nextcloud/vars/main.yml` for the platform-keyed pattern.

This role is compatible with the following PHP versions:

* 7.2
* 7.3
* 7.4
* 8.0
* 8.1
* 8.2
* 8.3
* 8.4
* 8.5

Rules of thumb:

* Specify memory values in MB (M).
* `memory_limit` should be larger than `post_max_size`.
* `post_max_size` can stay at `16M`, even if you have `upload_max_filesize` > `10000M` for example.
* If disabling `opcache.validate_timestamps`, `opcache.revalidate_freq` is ignored.

This role never exposes to the world that PHP is installed on the server, no matter what.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* On RedHat the role ships a small SELinux policy module, `lfops_php_fpm_slowlog`, and hands it to the `selinux` role through `php__selinux__modules__dependent_var`. It grants the `httpd_t` domain the `sys_ptrace` capability and `ptrace` on itself, which the PHP-FPM master needs to read the backtrace out of a worker that exceeded `php__fpm_pool_conf_request_slowlog_timeout__*_var`. Without it, PHP-FPM logs `failed to ptrace(ATTACH) child <pid>: Operation not permitted (1)` and leaves the slowlog empty. The targeted policy grants neither permission and offers no boolean for it, so the rules have to come from a module.
* The module is installed regardless of the configured `request_slowlog_timeout`, so that turning the slowlog on later is a pure configuration change. The permissions it grants apply to the whole `httpd_t` domain, Apache httpd included. Its rules are unconditional and therefore not subject to the `deny_ptrace` boolean: on a host hardened with `setsebool -P deny_ptrace on`, `httpd_t` can still ptrace itself. Set `php__skip_selinux: true` in the playbook to leave the host's policy untouched.
* Every pool gets a dedicated session directory below the distribution's session base (`/var/lib/php/session` on RedHat, `/var/lib/php/sessions` on Debian), owned by the pool's `user` and `group` with mode `0700`, so pools cannot read each other's sessions. On RedHat the `/var/lib/php/session(/.*)?` file context gives it the `httpd_var_run_t` type php-fpm needs. On Debian the packaged `sessionclean` timer recurses the session base using the global `session.gc_maxlifetime`, so a per-pool `session.gc_maxlifetime` is not honored by the cleanup there, and a session that stays open but idle longer than the lifetime may be removed.
* Each pool writes its `error_log` and `slowlog` into a per-service log directory (`/var/log/php-fpm` on RedHat, `/var/log/<service>` on Debian, e.g. `/var/log/php8.4-fpm`), which the role creates. On RedHat the package's logrotate config already rotates `/var/log/php-fpm/*log`; on Debian the role ships `/etc/logrotate.d/linuxfabrik-php-fpm` for the per-pool logs, since the packaged config only covers the single global log file.
* Each pool listens on its own Unix socket below the FPM runtime directory (`/run/php-fpm/<pool>.sock` on RedHat, `/run/php/<pool>.sock` on Debian). On Debian the packaged php-fpm systemd unit additionally maintains a version-agnostic `update-alternatives` alias at `/run/php/php-fpm.sock` pointing at the socket of the default `www` pool. That alias only ever tracks `www`, so configure the web server with the explicit per-pool socket path rather than the generic one. RedHat ships no such alias.
* Every pool answers on the same two FPM-internal endpoints, `/fpm-status` (the status page) and `/fpm-ping` (a liveness check returning `pong`). Which pool answers is decided by the socket the request arrives on, not by the path, so a second pool is published by giving it its own `Location` pointing at that pool's socket while keeping `/fpm-status` as the path sent to FPM. The `localhost` vHost of the [apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role does this for the `www` pool, which is what the `php-fpm-status` and `php-fpm-ping` [Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins) check by default; `php-fpm-status` accepts `--url` several times for the additional pools. Both endpoints are reachable for anyone who can reach the pool socket, so take care with a vHost that forwards its whole URI space to a pool, or with a reverse proxy that passes unknown paths through. Set `pm_status_path` and / or `ping_path` to an empty string to turn them off for a pool.


## Known Limitations

* Setting a pool to `state: 'absent'` removes its pool configuration file, but leaves its session directory and its `error_log` / `slowlog` behind. Remove them by hand once the pool is gone for good.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* On RedHat, the `lfops_php_fpm_slowlog` policy module must be compiled and installed (roles: [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils) and [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux)).
* Optional: The EPEL repository, and CRB on Rocky 9 and newer, must be enabled (roles: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) and [linuxfabrik.lfops.repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos)). Remi's packages link against EPEL content: on RedHat 8 for example `php-opcache` needs `libcapstone`, which neither the default repositories nor PowerTools carry.
* Optional: [Remi's RPM repository](https://rpms.remirepo.net/) (role: [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi)) provides newer PHP versions.


## Tags

`php`

* Installs php, php-fpm and composer.
* Installs and removes the configured PHP modules.
* Deploys the `z00-linuxfabrik.ini` for every SAPI.
* Deploys and removes the PHP-FPM pools, together with their session, opcache and log directories.
* Manages the state of the php-fpm service.
* Pins the `php`, `phar` and `phar.phar` alternatives (Debian with `php__version` set only).
* Triggers: php-fpm.service restart.

`php:alternatives`

* Debian with `php__version` set only. Pins the `php`, `phar` and `phar.phar` alternatives to the declared version, so installing another version does not silently switch the CLI.
* Triggers: none.

`php:fpm`

* Deploys and removes the PHP-FPM pools. On Debian these live under the declared version's tree, on RedHat under `/etc/php-fpm.d`.
* Creates the shared opcache directory, the php-fpm log directory and one session directory per pool, and relabels them on SELinux hosts.
* Deploys `/etc/logrotate.d/linuxfabrik-php-fpm` on Debian, where the packaged logrotate config does not cover the per-pool logs.
* Triggers: php-fpm.service restart.

`php:ini`

* Deploys the `z00-linuxfabrik.ini`. RedHat has a single `/etc/php.d`, Debian one conf.d per SAPI (apache2, cli and fpm) below the declared version's tree.
* Triggers: php-fpm.service restart.

`php:modules`

* Installs and removes the PHP modules from `php__modules__combined_var`.
* Triggers: none.

`php:state`

* Enables or disables the php-fpm service and brings it into the state requested by `php__fpm_service_state`.
* Triggers: none.

`php:update`

* Updates the PHP packages, composer and the PHP modules, and reasserts the ini, the pools, the service state and the alternatives. Do not forget to update the repo beforehand.
* On Debian with `php__version` set, this is also how a major version change is carried out: raise `php__version`, then run this tag. It installs the declared version, moves the pools, alternatives and the FPM service over to it, and purges the stacks of all other versions.
* Triggers: php-fpm.service restart.


## Optional Role Variables

`php__fpm_pools__host_var` / `php__fpm_pools__group_var`

* List of dictionaries containing PHP-FPM pools.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. The name of the pool. Will also be used as the filename and for logfiles.
        * Type: String.

    * `state`:

        * Optional. State of the pool. Possible options: `absent`, `present`.
        * Type: String.
        * Default: `'present'`

    * `user`:

        * Optional. The Unix user running the pool processes. [php.net](https://www.php.net/install.fpm.configuration.php#user)
        * Type: String.
        * Default: `'apache'` (RedHat), `'www-data'` (Debian)

    * `group`:

        * Optional. The Unix group running the pool processes. [php.net](https://www.php.net/install.fpm.configuration.php#group)
        * Type: String.
        * Default: `'apache'` (RedHat), `'www-data'` (Debian)

    * `pm`:

        * Optional. Choose how the process manager will control the number of child processes. [php.net](https://www.php.net/install.fpm.configuration.php#pm)
        * Type: String.
        * Default: `{{ php__fpm_pool_conf_pm__combined_var }}` (which defaults to `'dynamic'`)

    * `pm_max_children`:

        * Optional. The number of child processes to be created when `pm` is set to `'static'`, and the maximum number of child processes when `pm` is set to `'dynamic'` or `'ondemand'`. [php.net](https://www.php.net/install.fpm.configuration.php#pm.max-children)
        * Type: Number.
        * Default: `{{ php__fpm_pool_conf_pm_max_children__combined_var }}` (which defaults to `50`)

    * `pm_start_servers`:

        * Optional. The number of child processes created on startup. Must be greater than `pm_min_spare_servers` but less than `pm_max_spare_servers`. Used only when `pm` is set to `'dynamic'`. [php.net](https://www.php.net/install.fpm.configuration.php#pm.start-servers)
        * Type: Number.
        * Default: `{{ php__fpm_pool_conf_pm_start_servers__combined_var }}` (which defaults to `5`)

    * `pm_min_spare_servers`:

        * Optional. The desired minimum number of idle server processes. Used only when `pm` is set to `'dynamic'`. [php.net](https://www.php.net/install.fpm.configuration.php#pm.min-spare-servers)
        * Type: Number.
        * Default: `{{ php__fpm_pool_conf_pm_min_spare_servers__combined_var }}` (which defaults to `5`)

    * `pm_max_spare_servers`:

        * Optional. The desired maximum number of idle server processes. Used only when `pm` is set to `'dynamic'`. Idle workers are only reaped down to this number, so on a host with several pools this is what they cost at rest. [php.net](https://www.php.net/install.fpm.configuration.php#pm.max-spare-servers)
        * Type: Number.
        * Default: `{{ php__fpm_pool_conf_pm_max_spare_servers__combined_var }}` (which defaults to `35`)

    * `pm_max_spawn_rate`:

        * Optional. The number of child processes to spawn at once. Used only when `pm` is set to `'dynamic'`. Only rendered on PHP 8.1 and newer, where the directive exists. [php.net](https://www.php.net/install.fpm.configuration.php#pm.max-spawn-rate)
        * Type: Number.
        * Default: `32`

    * `pm_process_idle_timeout`:

        * Optional. The number of seconds after which an idle process will be killed. Used only when `pm` is set to `'ondemand'`. Available units: s(econds, default), m(inutes), h(ours), or d(ays). [php.net](https://www.php.net/install.fpm.configuration.php#pm.process-idle-timeout)
        * Type: String.
        * Default: `'10s'`

    * `pm_max_requests`:

        * Optional. The number of requests each child process should execute before respawning, which bounds the damage a leaking third-party library can do. For endless request processing specify `0`. [php.net](https://www.php.net/install.fpm.configuration.php#pm.max-requests)
        * Type: Number.
        * Default: `500`

    * `pm_status_path`:

        * Optional. Path to view the FPM status page. Set to an empty string to disable the status page for this pool. [php.net](https://www.php.net/install.fpm.configuration.php#pm.status-path)
        * Type: String.
        * Default: `'/fpm-status'`

    * `ping_path`:

        * Optional. The ping path to check if FPM is alive and responding. Set to an empty string to disable the ping endpoint for this pool. [php.net](https://www.php.net/install.fpm.configuration.php#ping.path)
        * Type: String.
        * Default: `'/fpm-ping'`

    * `request_slowlog_timeout`:

        * Optional. The timeout for serving a single request after which a PHP backtrace will be dumped to the slowlog file. A value of `0` means off. Available units: s(econds, default), m(inutes), h(ours), or d(ays). [php.net](https://www.php.net/install.fpm.configuration.php#request-slowlog-timeout)
        * Type: Number.
        * Default: `{{ php__fpm_pool_conf_request_slowlog_timeout__combined_var }}` (which defaults to `0`)

    * `request_slowlog_trace_depth`:

        * Optional. Depth of the slowlog stack trace. [php.net](https://www.php.net/install.fpm.configuration.php#request-slowlog-trace-depth)
        * Type: Number.
        * Default: `20`

    * `request_terminate_timeout`:

        * Optional. The timeout for serving a single request after which the worker process will be killed. A value of `0` means off. Available units: s(econds, default), m(inutes), h(ours), or d(ays). [php.net](https://www.php.net/install.fpm.configuration.php#request-terminate-timeout)
        * Type: String.
        * Default: `{{ php__fpm_pool_conf_request_terminate_timeout__combined_var }}` (which defaults to `'60s'`)

    * `php_admin_value_max_execution_time`:

        * Optional. Enforced as `php_admin_value`, so an application cannot raise it at runtime via `ini_set()`. [php.net](https://www.php.net/max_execution_time)
        * Type: Number.
        * Default: `{{ php__ini_max_execution_time__combined_var }}`

    * `php_admin_value_max_input_vars`:

        * Optional. Enforced as `php_admin_value`. [php.net](https://www.php.net/max_input_vars)
        * Type: Number.
        * Default: `{{ php__ini_max_input_vars__combined_var }}`

    * `php_admin_value_memory_limit`:

        * Optional. Enforced as `php_admin_value`. [php.net](https://www.php.net/memory_limit)
        * Type: String.
        * Default: `'{{ php__ini_memory_limit__combined_var }}'`

    * `php_admin_value_open_basedir`:

        * Optional. Limits the files the pool may access to the given paths. [php.net](https://www.php.net/open_basedir)
        * Type: String.
        * Default: unset

    * `php_admin_value_post_max_size`:

        * Optional. Enforced as `php_admin_value`. [php.net](https://www.php.net/post_max_size)
        * Type: String.
        * Default: `'{{ php__ini_post_max_size__combined_var }}'`

    * `php_admin_value_session_save_path`:

        * Optional. The role creates this directory, owned by the pool's `user` / `group` with mode `0700`. On RedHat it inherits the `httpd_var_run_t` SELinux type from the session base; pointing it outside that base means labeling it yourself. [php.net](https://www.php.net/session.save_path)
        * Type: String.
        * Default: `/var/lib/php/session/<pool>` (RedHat), `/var/lib/php/sessions/<pool>` (Debian)

    * `php_admin_value_upload_max_filesize`:

        * Optional. Enforced as `php_admin_value`. [php.net](https://www.php.net/upload_max_filesize)
        * Type: String.
        * Default: `'{{ php__ini_upload_max_filesize__combined_var }}'`

    * `raw`:

        * Optional. Raw content which will be added to the end of the pool config.
        * Type: String.
        * Default: unset

`php__fpm_service_enabled`

* Enables or disables the php-fpm service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`php__fpm_service_state`

* Changes the state of the php-fpm service, analogous to `systemctl start/stop/restart/reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `php__fpm_service_enabled` is `true`, else `'stopped'`

`php__modules__host_var` / `php__modules__group_var`

* List of dictionaries containing additional PHP modules that should be installed via the standard package manager.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the module package.
        * Type: String.

    * `state`:

        * Optional. State of the module package. Possible options: `absent`, `present`.
        * Type: String.
        * Default: `'present'`

`php__version`

* Debian only. The PHP version this host runs, for example `'8.4'`. Makes the role install the versioned packages (`php8.4-cli`, `php8.4-fpm`, ...) instead of the unversioned metapackages, pin the `php` alternatives to it, and purge other versions on `php:update`. Empty adopts whatever version the configured repos provide, which is correct without the sury repo. Has no effect on RedHat, where the module stream pins the version at repo level.
* Type: String.
* Default: `''`

Example:
```yaml
# optional
php__fpm_service_enabled: true
php__fpm_service_state: 'started'
php__fpm_pools__host_var:
  - name: 'librenms'
    user: 'librenms'
    group: 'librenms'
    raw: |-
      env[PATH] = /usr/local/bin:/usr/bin:/bin
php__modules__host_var:
  - name: 'php-mysqlnd'
    state: 'present'
php__version: '8.4'
```


## Optional Role Variables - `php__ini_*` Config Directives

Variables for `php.ini` directives and their default values, defined and supported by this role.

`php__ini_date_timezone__group_var` / `php__ini_date_timezone__host_var`

* The default timezone used by all date/time functions. [php.net](https://www.php.net/manual/en/datetime.configuration.php)
* Type: String.
* Default: `'Europe/Zurich'`

`php__ini_default_socket_timeout__group_var` / `php__ini_default_socket_timeout__host_var`

* Default timeout in seconds for socket based streams (e.g. HTTP, FTP). [php.net](https://www.php.net/manual/en/filesystem.configuration.php)
* Type: Number.
* Default: `10`

`php__ini_display_errors__group_var` / `php__ini_display_errors__host_var`

* This determines whether errors should be printed to the screen as part of the output or if they should be hidden from the user. This is a feature to support your development and should never be used on production systems (e.g. systems connected to the internet). [php.net](https://www.php.net/manual/en/errorfunc.configuration.php)
* Type: String.
* Default: `'Off'`

`php__ini_display_startup_errors__group_var` / `php__ini_display_startup_errors__host_var`

* Even when display_errors is on, errors that occur during PHP's startup sequence are not displayed. It's strongly recommended to keep this off. [php.net](https://www.php.net/manual/en/errorfunc.configuration.php)
* Type: String.
* Default: `'Off'`

`php__ini_error_reporting__group_var` / `php__ini_error_reporting__host_var`

* Set the error reporting level. [php.net](https://www.php.net/manual/en/errorfunc.configuration.php)
* Type: String.
* Default: `'E_ALL & ~E_NOTICE & ~E_DEPRECATED'`

`php__ini_max_execution_time__group_var` / `php__ini_max_execution_time__host_var`

* This sets the maximum time in seconds a script is allowed to run before it is terminated by the parser. This helps prevent poorly written scripts from tying up the server. The default setting is 30. When running PHP from the command line the default setting is 0. [php.net](https://www.php.net/manual/en/info.configuration.php)
* Type: Number.
* Default: `30`

`php__ini_max_file_uploads__group_var` / `php__ini_max_file_uploads__host_var`

* The maximum number of files allowed to be uploaded simultaneously. [php.net](https://www.php.net/manual/en/ini.core.php)
* Type: Number.
* Default: `50`

`php__ini_max_input_time__group_var` / `php__ini_max_input_time__host_var`

* This sets the maximum time in seconds a script is allowed to parse input data, like POST and GET. Timing begins at the moment PHP is invoked at the server and ends when execution begins. The default setting is -1, which means that max_execution_time is used instead. Set to 0 to allow unlimited time. [php.net](https://www.php.net/manual/en/info.configuration.php)
* Type: Number.
* Default: `-1`

`php__ini_max_input_vars__group_var` / `php__ini_max_input_vars__host_var`

* How many input variables may be accepted (limit is applied to `$_GET`, `$_POST` and `$_COOKIE` superglobal separately). Use of this directive mitigates the possibility of denial of service attacks which use hash collisions. If there are more input variables than specified by this directive, an E_WARNING is issued, and further input variables are truncated from the request. [php.net](https://www.php.net/manual/en/info.configuration.php)
* Type: Number.
* Default: `1000`

`php__ini_memory_limit__group_var` / `php__ini_memory_limit__host_var`

* This sets the maximum amount of memory in bytes that ONE RUNNING SCRIPT is allowed to allocate. This helps prevent poorly written scripts for eating up all available memory on a server. Note that to have no memory limit, set this directive to -1. Again: PHP memory_limit is per-script, just as a highway's speed limit is per-vehicle. [php.net](https://www.php.net/manual/en/ini.core.php)
* Type: String.
* Default: `'128M'`

`php__ini_opcache_blacklist_filename__group_var` / `php__ini_opcache_blacklist_filename__host_var`

* A blacklist file is a text file containing the names of files that should not be accelerated, one per line. Wildcards are allowed, and prefixes can also be provided. Lines starting with a semi-colon are ignored as comments. [php.net](https://www.php.net/manual/en/opcache.configuration.php)
* Type: String.
* Default: `'/etc/opcache.blacklist'`

`php__ini_opcache_enable__group_var` / `php__ini_opcache_enable__host_var`

* Enables the opcode cache. When disabled, code is not optimised or cached. [php.net](https://www.php.net/manual/en/opcache.configuration.php)
* Type: Number.
* Default: `1`

`php__ini_opcache_enable_cli__group_var` / `php__ini_opcache_enable_cli__host_var`

* Enables the opcode cache for the CLI version of PHP. [php.net](https://www.php.net/manual/en/opcache.configuration.php)
* Type: Number.
* Default: `1`

`php__ini_opcache_huge_code_pages__group_var` / `php__ini_opcache_huge_code_pages__host_var`

* Enables or disables copying of PHP code (text segment) into HUGE PAGES. This should improve performance, but requires appropriate OS configuration. [php.net](https://www.php.net/manual/en/opcache.configuration.php)
* Type: Number.
* Default: `0`

`php__ini_opcache_interned_strings_buffer__group_var` / `php__ini_opcache_interned_strings_buffer__host_var`

* The amount of memory used to store interned strings, in megabytes. [php.net](https://www.php.net/manual/en/opcache.configuration.php)
* Type: Number.
* Default: `12`

`php__ini_opcache_max_accelerated_files__group_var` / `php__ini_opcache_max_accelerated_files__host_var`

* The maximum number of keys (and therefore scripts) in the OPcache hash table. The actual value used will be the first number in the set of prime numbers { 223, 463, 983, 1979, 3907, 7963, 16229, 32531, 65407, 130987, 262237, 524521, 1048793 } that is greater than or equal to the configured value. [php.net](https://www.php.net/manual/en/opcache.configuration.php)
* Type: Number.
* Default: `7963`

`php__ini_opcache_memory_consumption__group_var` / `php__ini_opcache_memory_consumption__host_var`

* The size of the shared memory storage used by OPcache, in megabytes. The minimum permissible value is "8", which is enforced if a smaller value is set. [php.net](https://www.php.net/manual/en/opcache.configuration.php)
* Type: Number.
* Default: `128`

`php__ini_opcache_revalidate_freq__group_var` / `php__ini_opcache_revalidate_freq__host_var`

* How often to check script timestamps for updates, in seconds. 0 will result in OPcache checking for updates on every request. [php.net](https://www.php.net/manual/en/opcache.configuration.php)
* Type: Number.
* Default: `60`

`php__ini_opcache_save_comments__group_var` / `php__ini_opcache_save_comments__host_var`

* If disabled, all documentation comments will be discarded from the opcode cache to reduce the size of the optimised code. Disabling this configuration directive may break applications and frameworks that rely on comment parsing for annotations. [php.net](https://www.php.net/manual/en/opcache.configuration.php)
* Type: Number.
* Default: `1`

`php__ini_opcache_validate_timestamps__group_var` / `php__ini_opcache_validate_timestamps__host_var`

* If enabled, OPcache will check for updated scripts every opcache.revalidate_freq seconds. When this directive is disabled, you must reset OPcache manually via opcache_reset(), opcache_invalidate() or by restarting the Web server for changes to the filesystem to take effect. [php.net](https://www.php.net/manual/en/opcache.configuration.php)
* Type: Number.
* Default: `1`

`php__ini_post_max_size__group_var` / `php__ini_post_max_size__host_var`

* Sets max size of post data allowed. This setting also affects file upload. To upload large files, this value must be larger than upload_max_filesize. [php.net](https://www.php.net/manual/en/ini.core.php)
* Type: String.
* Default: `'8M'`

`php__ini_session_cookie_httponly__group_var` / `php__ini_session_cookie_httponly__host_var`

* Marks the session cookie as HttpOnly, so it is not accessible to JavaScript via `document.cookie`, mitigating cookie theft via XSS. [php.net](https://www.php.net/manual/en/session.configuration.php)
* Type: String.
* Default: `'On'`

`php__ini_session_cookie_secure__group_var` / `php__ini_session_cookie_secure__host_var`

* Sends the session cookie only over HTTPS. Leave off on hosts that also serve sessions over plain HTTP. [php.net](https://www.php.net/manual/en/session.configuration.php)
* Type: String.
* Default: `'Off'`

`php__ini_session_gc_maxlifetime__group_var` / `php__ini_session_gc_maxlifetime__host_var`

* Number of seconds after which session data is treated as garbage and cleaned up by the session garbage collector. [php.net](https://www.php.net/manual/en/session.configuration.php)
* Type: Number.
* Default: `1440`

`php__ini_session_sid_length__group_var` / `php__ini_session_sid_length__host_var`

* Length of the session ID string. Only takes effect on PHP versions that still honor the directive; PHP deprecates any value other than the built-in `32`. [php.net](https://www.php.net/manual/en/session.configuration.php)
* Type: Number.
* Default: `32`

`php__ini_session_trans_sid_tags__group_var` / `php__ini_session_trans_sid_tags__host_var`

* HTML tags whose attributes are rewritten to include the session ID when transparent SID support is enabled. [php.net](https://www.php.net/manual/en/session.configuration.php)
* Type: String.
* Default: `'a=href,area=href,frame=src,input=src,form=fakeentry'`

`php__ini_smtp__group_var` / `php__ini_smtp__host_var`

* Host used by the `mail()` function to send mail (Windows only; ignored on Unix, where the `sendmail_path` binary is used). [php.net](https://www.php.net/manual/en/mail.configuration.php)
* Type: String.
* Default: `'localhost'`

`php__ini_upload_max_filesize__group_var` / `php__ini_upload_max_filesize__host_var`

* The maximum size of an uploaded file. [php.net](https://www.php.net/manual/en/ini.core.php)
* Type: String.
* Default: `'2M'`

Note that setting `php__ini_opcache_huge_code_pages__group_var` or `php__ini_opcache_huge_code_pages__host_var` to `1` might require enabling the SELinux boolean `httpd_execmem` on RHEL systems.

Example:
```yaml
# optional
php__ini_date_timezone__host_var: 'Europe/Zurich'
php__ini_default_socket_timeout__host_var: 10
php__ini_display_errors__host_var: 'Off'
php__ini_display_startup_errors__host_var: 'Off'
php__ini_error_reporting__host_var: 'E_ALL & ~E_NOTICE & ~E_DEPRECATED'
php__ini_max_execution_time__host_var: 3600
php__ini_max_file_uploads__host_var: 100
php__ini_max_input_time__host_var: -1
php__ini_max_input_vars__host_var: 1000
php__ini_memory_limit__host_var: '1024M'
php__ini_opcache_blacklist_filename__host_var: '/etc/opcache.blacklist'
php__ini_opcache_enable__host_var: 1
php__ini_opcache_enable_cli__host_var: 1
php__ini_opcache_huge_code_pages__host_var: 0
php__ini_opcache_interned_strings_buffer__host_var: 12
php__ini_opcache_max_accelerated_files__host_var: 7963
php__ini_opcache_memory_consumption__host_var: 128
php__ini_opcache_revalidate_freq__host_var: 60
php__ini_opcache_save_comments__host_var: 1
php__ini_opcache_validate_timestamps__host_var: 1
php__ini_post_max_size__host_var: '8M'
php__ini_session_cookie_httponly__host_var: 'On'
php__ini_session_cookie_secure__host_var: 'Off'
php__ini_session_gc_maxlifetime__host_var: 1440
php__ini_session_sid_length__host_var: 32
php__ini_session_trans_sid_tags__host_var: 'a=href,area=href,frame=src,input=src,form=fakeentry'
php__ini_smtp__host_var: 'localhost'
php__ini_upload_max_filesize__host_var: '10000M'
```


## Optional Role Variables - PHP-FPM Pool Config Directives

Variables for PHP-FPM pool directives and their default values, defined and supported by this role.

`php__fpm_pool_conf_pm__group_var` / `php__fpm_pool_conf_pm__host_var`

* Choose how the process manager will control the number of child processes.
* Type: String.
* Default: `'dynamic'`

`php__fpm_pool_conf_pm_max_children__group_var` / `php__fpm_pool_conf_pm_max_children__host_var`

* The number of child processes to be created when pm is set to 'static' and the maximum number of child processes when pm is set to 'dynamic' or 'ondemand'.
* Type: Number.
* Default: `50`

`php__fpm_pool_conf_pm_max_spare_servers__group_var` / `php__fpm_pool_conf_pm_max_spare_servers__host_var`

* The desired maximum number of idle server processes.
* Type: Number.
* Default: `35`

`php__fpm_pool_conf_pm_min_spare_servers__group_var` / `php__fpm_pool_conf_pm_min_spare_servers__host_var`

* The desired minimum number of idle server processes.
* Type: Number.
* Default: `5`

`php__fpm_pool_conf_pm_start_servers__group_var` / `php__fpm_pool_conf_pm_start_servers__host_var`

* The number of child processes created on startup. Must be greater than `php__fpm_pool_conf_pm_min_spare_servers__*_var` but less than `php__fpm_pool_conf_pm_max_spare_servers__*_var`.
* Type: Number.
* Default: `5`

`php__fpm_pool_conf_request_slowlog_timeout__group_var` / `php__fpm_pool_conf_request_slowlog_timeout__host_var`

* The timeout for serving a single request after which a PHP backtrace will be dumped to the slowlog file. A value of `0` means off. Available units: s(econds, default), m(inutes), h(ours), or d(ays). The slowlog is written to `/var/log/php-fpm/<pool>-slow.log` on RedHat and to `log/<pool>-slow.log` below the FPM prefix on Debian. On RedHat the backtrace also needs the `lfops_php_fpm_slowlog` SELinux module, see "How the Role Behaves".
* Type: Number.
* Default: `0`

`php__fpm_pool_conf_request_terminate_timeout__group_var` / `php__fpm_pool_conf_request_terminate_timeout__host_var`

* The timeout for serving a single request after which the worker process will be killed. This is the backstop for requests that `max_execution_time` cannot stop, because the script is blocked in a system call (a database query, an outgoing HTTP request) rather than executing PHP. Without it such a worker occupies its slot until it returns on its own, which fills up `pm.max_children` under load long after the web server or a reverse proxy in front of it gave up on the request. Keep it above `php__ini_max_execution_time__*_var` (default `30`), so a script still hits PHP's own limit first and gets a proper error and log entry, and above the web server's own timeout (`apache_httpd__conf_timeout`, default `10`). A value of `0` means off. Available units: s(econds, default), m(inutes), h(ours), or d(ays).
* Type: String.
* Default: `'60s'`

`php__fpm_pools__group_var` / `php__fpm_pools__host_var`

* List defining pool configuration.
* Type: List of dictionaries.
* Default: `name: 'www'` `user: 'apache'` `group: 'apache'`
* Subkeys:

    * `name`:

        * Mandatory. Pool name.
        * Type: String.

    * `user`:

        * Optional. The Unix user running the pool processes.
        * Type: String.

    * `group`:

        * Optional. The Unix group running the pool processes.
        * Type: String.

    * `raw`:

        * Optional. Raw content which will be added to the end of the pool config.
        * Type: String.

Example:
```yaml
# optional
php__fpm_pool_conf_pm__host_var: 'dynamic'
php__fpm_pool_conf_pm_max_children__host_var: 50
php__fpm_pool_conf_pm_max_spare_servers__host_var: 35
php__fpm_pool_conf_pm_min_spare_servers__host_var: 5
php__fpm_pool_conf_pm_start_servers__host_var: 5
php__fpm_pool_conf_request_slowlog_timeout__host_var: '10s'
php__fpm_pool_conf_request_terminate_timeout__host_var: '60s'
php__fpm_pools__host_var:
  - name: 'librenms'
    user: 'librenms'
    group: 'librenms'
    pm: 'ondemand'
    pm_max_children: 10
    pm_process_idle_timeout: '60s'
    php_admin_value_memory_limit: '256M'
    php_admin_value_open_basedir: '/opt/librenms:/tmp'
    request_terminate_timeout: '120s'
    raw: |-
      env[PATH] = /usr/local/bin:/usr/bin:/bin
```


## Troubleshooting

**The run aborts with `PHP X.Y is not supported by this role`**

* The enabled repositories offer a PHP version this role ships no ini template and vars file for. Either pin the host to a supported version via `php__version`, or add the matching `roles/php/templates/etc/php.d/<version>-z00-linuxfabrik.ini.j2` and `roles/php/vars/<version>.yml`, and list the version in `roles/php/vars/main.yml`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
