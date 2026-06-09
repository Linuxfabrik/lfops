# Ansible Role linuxfabrik.lfops.php

This role installs and configures PHP (and PHP-FPM) on the system, optionally with additional modules.

Note that this role does NOT let you specify a particular PHP version. It simply installs the latest available PHP version from the repos configured in the system. If you want or need to install a specific or the latest PHP version available, use the [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) (Red Hat family) or [linuxfabrik.lfops.repo_sury](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_sury) (Debian family) beforehand.

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


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* Optional: [Remi's RPM repository](https://rpms.remirepo.net/) (role: [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi)) provides newer PHP versions on the Red Hat family.
* [Sury repository](https://deb.sury.org/) (role: [linuxfabrik.lfops.repo_sury](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_sury)) provides newer PHP versions on the Debian family.


## Tags

`php`

* Install php php-fpm composer.
* Get the list of installed packages.
* Ensure PHP modules are absent.
* Ensure PHP modules are present.
* Get PHP version.
* Load default values for `{{ __php__installed_version }}`.
* Deploy the /etc/php.d/z00-linuxfabrik.ini.
* `systemctl {{ php__fpm_service_enabled | bool | ternary("enable", "disable") }} --now php-fpm`.
* Ensure the shared opcache directory exists.
* Create the per-pool session directories.
* Remove absent pools from `/etc/php-fpm.d`.
* Deploy the pools to `/etc/php-fpm.d/`.
* Triggers: php-fpm.service restart.

`php:fpm`

* Ensure the shared opcache directory exists.
* Create the per-pool session directories.
* Remove absent pools from /etc/php-fpm.d.
* Deploy the pools to /etc/php-fpm.d/.
* Triggers: php-fpm.service restart.

`php:ini`

* Get PHP version.
* Load default values for `{{ __php__installed_version }}`.
* Deploy the `/etc/php.d/z00-linuxfabrik.ini`.
* Triggers: php-fpm.service restart.

`php:state`

* `systemctl {{ php__fpm_service_enabled | bool | ternary("enable", "disable") }} --now php-fpm`.
* Remove absent pools from `/etc/php-fpm.d`.
* Deploy the pools to `/etc/php-fpm.d/`.
* Triggers: none.

`php:update`

* Updates the PHP Packages and the configuration. Do not forget to update the repo beforehand.
* Triggers: php-fpm.service restart.


## Optional Role Variables

`php__fpm_service_enabled`

* Enables or disables the php-fpm service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

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

Example:
```yaml
# optional
php__fpm_service_enabled: true
php__fpm_pools__host_var:
  - name: 'librenms'
    user: 'librenms'
    group: 'librenms'
    raw: |-
      env[PATH] = /usr/local/bin:/usr/bin:/bin
php__modules__host_var:
  - name: 'php-mysqlnd'
    state: 'present'
```


## Optional Role Variables - `php__ini_*` Config Directives

Variables for `php.ini` directives and their default values, defined and supported by this role.

`php__ini_date_timezone__group_var` / `php__ini_date_timezone__host_var`

* The default timezone used by all date/time functions. [php.net](https://www.php.net/manual/en/datetime.configuration.php)
* Type: String.
* Default: `'Europe/Zurich'`

`php__ini_default_socket_timeout__group_var` / `php__ini_default_socket_timeout__host_var`

* [php.net](https://www.php.net/manual/en/filesystem.configuration.php)
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
* Default: 7.2 - 8.4: `'E_ALL & ~E_NOTICE & ~E_DEPRECATED & ~E_STRICT'`, 8.5: `'E_ALL & ~E_NOTICE & ~E_DEPRECATED'` (`E_STRICT` is deprecated as of PHP 8.4)

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
* Default: `'/etc/php-zts.d/opcache*.blacklist'`

`php__ini_opcache_enable__group_var` / `php__ini_opcache_enable__host_var`

* Enables the opcode cache. When disabled, code is not optimised or cached. [php.net](https://www.php.net/manual/en/opcache.configuration.php)
* Type: Number.
* Default: `1`

`php__ini_opcache_enable_cli__group_var` / `php__ini_opcache_enable_cli__host_var`

* Enables the opcode cache for the CLI version of PHP. [php.net](https://www.php.net/manual/en/opcache.configuration.php)
* Type: Number.
* Default: `1`

`php__ini_opcache_huge_code_pages__group_var` / `php__ini_opcache_huge_code_pages__host_var`

* [php.net](https://www.php.net/manual/en/opcache.configuration.php)
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

* [php.net](https://www.php.net/manual/en/session.configuration.php)
* Type: String.
* Default: `'Off'`

`php__ini_session_cookie_secure__group_var` / `php__ini_session_cookie_secure__host_var`

* [php.net](https://www.php.net/manual/en/session.configuration.php)
* Type: String.
* Default: `'Off'`

`php__ini_session_gc_maxlifetime__group_var` / `php__ini_session_gc_maxlifetime__host_var`

* [php.net](https://www.php.net/manual/en/session.configuration.php)
* Type: Number.
* Default: `1440`

`php__ini_session_sid_length__group_var` / `php__ini_session_sid_length__host_var`

* [php.net](https://www.php.net/manual/en/session.configuration.php)
* Type: Number.
* Default: 7.2 - 8.4: `32`. Not managed on 8.5, where PHP's built-in default applies.

`php__ini_session_trans_sid_tags__group_var` / `php__ini_session_trans_sid_tags__host_var`

* [php.net](https://www.php.net/manual/en/session.configuration.php)
* Type: String.
* Default: `'a=href,area=href,frame=src,input=src,form=fakeentry'`

`php__ini_smtp__group_var` / `php__ini_smtp__host_var`

* [php.net](https://www.php.net/manual/en/mail.configuration.php)
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
php__ini_max_execution_time__host_var: 3600
php__ini_max_file_uploads__host_var: 100
php__ini_memory_limit__host_var: '1024M'
php__ini_upload_max_filesize__host_var: '10000M'
```


## Optional Role Variables - PHP-FPM Pool Config Directives

Variables for PHP-FPM Pool Config directives and their default values, defined and supported by this role.

For every pool the role creates a dedicated session directory below the distribution's session base (`/var/lib/php/session` on RedHat, `/var/lib/php/sessions` on Debian) and a single shared opcache directory (`/var/lib/php/opcache`). On Debian, stale session files are reaped by the packaged `sessionclean` timer, which recurses the session base using the global `session.gc_maxlifetime`. A per-pool `session.gc_maxlifetime` is therefore not honored by the cleanup on Debian, and a session that stays open but idle longer than the lifetime may be removed.

Each pool listens on its own Unix socket below the FPM runtime directory (`/run/php-fpm/{{ item["name"] }}.sock` on RedHat, `/run/php/{{ item["name"] }}.sock` on Debian). On Debian, the packaged php-fpm systemd unit additionally maintains a version-agnostic `update-alternatives` alias at `/run/php/php-fpm.sock` that points at the socket of the default `www` pool. This alias only ever tracks `www`, not the pools created by this role, so configure your web server with the explicit per-pool socket path rather than the generic `/run/php/php-fpm.sock`. RedHat ships no such alias.

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

* The timeout for serving a single request after which a PHP backtrace will be dumped to the slowlog file. A value of `0` means off. Available units: s(econds, default), m(inutes), h(ours), or d(ays).
* Type: Number.
* Default: `0`

`php__fpm_pool_conf_request_terminate_timeout__group_var` / `php__fpm_pool_conf_request_terminate_timeout__host_var`

* The timeout for serving a single request after which the worker process will be killed. This option should be used when the `max_execution_time` ini option does not stop script execution for some reason. A value of `0` means off. Available units: s(econds, default), m(inutes), h(ours), or d(ays).
* Type: Number.
* Default: `0`

`php__fpm_pools__host_var` / `php__fpm_pools__group_var`

* List of dictionaries containing PHP-FPM pools.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: One pool named `www`.
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
        * Default: `'apache'` (RedHat), `www-data` (Debian)

    * `group`:

        * Optional. The Unix group running the pool processes. [php.net](https://www.php.net/install.fpm.configuration.php#group)
        * Type: String.
        * Default: `'apache'` (RedHat), `www-data` (Debian)

    * `pm`:

        * Optional. Choose how the process manager will control the number of child processes. [php.net](https://www.php.net/install.fpm.configuration.php#pm)
        * Type: String.
        * Default: `{{ php__fpm_pool_conf_pm__combined_var }}` (which defaults to `'dynamic'`)

    * `pm_max_children`:

        * Optional. The number of child processes to be created when pm is set to `'static'` and the maximum number of child processes when pm is set to `'dynamic'` or `'ondemand'`. [php.net](https://www.php.net/install.fpm.configuration.php#pm.max-children)
        * Type: Number.
        * Default: `{{ php__fpm_pool_conf_pm_max_children__combined_var }}` (which defaults to `50`)

    * `pm_start_servers`:

        * Optional. The number of child processes created on startup. Must be greater than `pm_min_spare_servers` but less than `pm_max_spare_servers`. Used only when `pm` is set to `'dynamic`'. [php.net](https://www.php.net/install.fpm.configuration.php#pm.start-servers)
        * Type: Number.
        * Default: `{{ php__fpm_pool_conf_pm_start_servers__combined_var }}` (which defaults to `5`)

    * `pm_min_spare_servers`:

        * Optional. The desired minimum number of idle server processes. Used only when `pm` is set to `'dynamic'`. [php.net](https://www.php.net/install.fpm.configuration.php#pm.min-spare-servers)
        * Type: Number.
        * Default: `{{ php__fpm_pool_conf_pm_min_spare_servers__combined_var }}` (which defaults to `5`)

    * `pm_max_spare_servers`:

        * Optional. The desired maximum number of idle server processes. Used only when `pm` is set to `'dynamic'`. [php.net](https://www.php.net/install.fpm.configuration.php#pm.max-spare-servers)
        * Type: Number.
        * Default: `{{ php__fpm_pool_conf_pm_max_spare_servers__combined_var }}` (which defaults to `35`)

    * `pm_max_spawn_rate`:

        * Optional. The number of rate to spawn child processes at once. Used only when `pm` is set to `'dynamic'`. [php.net](https://www.php.net/install.fpm.configuration.php#pm.max-spawn-rate)
        * Type: Number.
        * Default: `32`

    * `pm_process_idle_timeout`:

        * Optional. The number of seconds after which an idle process will be killed. Used only when `pm` is set to `'ondemand'`. Available units: s(econds, default), m(inutes), h(ours), or d(ays). [php.net](https://www.php.net/install.fpm.configuration.php#pm.process-idle-timeout)
        * Type: String.
        * Default: `'10s'`

    * `pm_max_requests`:

        * Optional. The number of requests each child process should execute before respawning. For endless request processing specify `0`. [php.net](https://www.php.net/install.fpm.configuration.php#pm.max-requests)
        * Type: Number.
        * Default: `500`

    * `pm_status_path`:

        * Optional. Path to view FPM status page. [php.net](https://www.php.net/install.fpm.configuration.php#pm.status-path)
        * Type: String.
        * Default: `'/{{ item["name"] }}-fpm-status'`

    * `ping_path`:

        * Optional. The ping path to check if FPM is alive and responding. [php.net](https://www.php.net/install.fpm.configuration.php#ping.path)
        * Type: String.
        * Default: `'/{{ item["name"] }}-fpm-ping'`

    * `request_slowlog_timeout`:

        * Optional. The timeout for serving a single request after which a PHP backtrace will be dumped to the slowlog file. A value of `0` means off. Available units: s(econds, default), m(inutes), h(ours), or d(ays). [php.net](https://www.php.net/install.fpm.configuration.php#request-slowlog-timeout)
        * Type: Number.
        * Default: `{{ php__fpm_pool_conf_request_slowlog_timeout__combined_var }}` (which defaults to `0`)

    * `request_slowlog_trace_depth`:

        * Optional. Depth of slow log stack trace. [php.net](https://www.php.net/install.fpm.configuration.php#request-slowlog-trace-depth)
        * Type: Number.
        * Default: `20`

    * `request_terminate_timeout`:

        * Optional. The timeout for serving a single request after which the worker process will be killed. This option should be used when the `max_execution_time` ini option does not stop script execution for some reason. A value of `0` means off. Available units: s(econds, default), m(inutes), h(ours), or d(ays).
        * [php.net](https://www.php.net/install.fpm.configuration.php#request-terminate-timeout)
        * Type: Number.
        * Default: `{{ php__fpm_pool_conf_request_terminate_timeout__combined_var }}` (which defaults to `0`)

    * `php_admin_value_session_save_path`:

        * Optional. The role creates this directory, owned by the pool's `user` / `group` with mode `0700`, so pools cannot read each other's sessions. On RedHat it inherits the `httpd_var_run_t` SELinux type from the session base; if you point it outside the session base, you have to label it yourself. [php.net](https://www.php.net/session.save_path)
        * Type: String.
        * Default: `/var/lib/php/session/{{ item["name"] }}` (RedHat), `/var/lib/php/sessions/{{ item["name"] }}` (Debian)

    * `php_admin_value_max_execution_time`:

        * Optional. [php.net](https://www.php.net/max_execution_time)
        * Type: Number.
        * Default: `{{ php__ini_max_execution_time__combined_var }}`

    * `php_admin_value_max_input_vars`:

        * Optional. [php.net](https://www.php.net/max_input_vars)
        * Type: Number.
        * Default: `{{ php__ini_max_input_vars__combined_var }}`

    * `php_admin_value_memory_limit`:

        * Optional. [php.net](https://www.php.net/memory_limit)
        * Type: String.
        * Default: `'{{ php__ini_memory_limit__combined_var }}'`

    * `php_admin_value_open_basedir`:

        * Optional. [php.net](https://www.php.net/open_basedir)
        * Type: String.
        * Default: unset

    * `php_admin_value_post_max_size`:

        * Optional. [php.net](https://www.php.net/post_max_size)
        * Type: String.
        * Default: `'{{ php__ini_post_max_size__combined_var }}'`

    * `php_admin_value_upload_max_filesize`:

        * Optional. [php.net](https://www.php.net/upload_max_filesize)
        * Type: String.
        * Default: `'{{ php__ini_upload_max_filesize__combined_var }}'`

    * `raw`:

        * Optional. Raw content which will be added to the end of the pool config.
        * Type: String.
        * Default: unset

Example:
```yaml
# optional
php__fpm_pools__host_var:
  - name: 'librenms'
    user: 'librenms'
    group: 'librenms'
    pm: 'dynamic'
    pm_max_children: 50
    pm_max_spare_servers: 35
    pm_min_spare_servers: 5
    pm_start_servers: 5
    request_slowlog_timeout: '10s'
    request_terminate_timeout: '60s'
    php_admin_value_session_save_path: '/var/lib/php/session' # use the shared session dir instead of the per-pool default /var/lib/php/session/librenms
    raw: |-
      env[PATH] = /usr/local/bin:/usr/bin:/bin
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
