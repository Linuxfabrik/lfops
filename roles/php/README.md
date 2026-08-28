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

**Where PHP-FPM logs, and what a monitoring check sees there.** PHP-FPM keeps two kinds of log apart, and only one of them is the process manager's own. The master writes its error log to the path the distribution's `php-fpm.conf` names (`/var/log/php-fpm/error.log` on RedHat, `/var/log/phpX.Y-fpm.log` on Debian); that file holds pool saturation, worker crashes, request timeouts and the start / reload / shutdown markers, and it is what the [php-fpm-logfile](https://linuxfabrik.github.io/monitoring-plugins/check-plugins/php-fpm-logfile.html) check reads. The applications' own errors go to `/var/log/php-fpm/<pool>-error.log`, in PHP's format, and need a separate check. Nothing of either reaches the journal: the unit's journal entries are systemd's own start and stop lines.

**Pool logs need a directory the workers may write to.** `/var/log/php-fpm` is created owned by the web server user, mode `0770`, mirroring what the RedHat package ships. A pool that runs as a different user than `php__fpm_pools__*_var` defaults to cannot create its log there; give it its own directory and point `raw` at it.

**The `[global]` section is deployed as a drop-in.** `php-fpm.conf` belongs to the package, so the role writes `z00-linuxfabrik-global.conf` into the pool directory instead. That covers `log_level` and the two `emergency_restart_*` directives. It deliberately does not set `error_log`: RedHat reads the pool directory *before* its own `[global]` and would override the value again, while Debian and Fedora read it after and would not, so the same drop-in would move the log on some hosts and not on others.

**Spawn pressure is loud by design.** Whenever `pm.min_spare_servers` cannot be met, PHP-FPM doubles its spawn rate every second and logs a `seems busy` warning from rate 8 on, once per second, unthrottled. A single traffic spike therefore writes a block of warnings even when the pool never fills up. `php__fpm_pool_conf_pm_start_servers__*_var` and `php__fpm_pool_conf_pm_min_spare_servers__*_var` keep a warm reserve that pushes the point where this starts; on a host where spikes are normal, pass `--ignore='seems busy'` to the monitoring check so that only the actual pool saturation alerts.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* Optional: The EPEL repository, and CRB on Rocky 9 and newer, must be enabled (roles: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) and [linuxfabrik.lfops.repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos)). Remi's packages link against EPEL content: on RedHat 8 for example `php-opcache` needs `libcapstone`, which neither the default repositories nor PowerTools carry.
* Optional: [Remi's RPM repository](https://rpms.remirepo.net/) (role: [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi)) provides newer PHP versions.


## Tags

`php`

* Installs php, php-fpm and composer.
* Installs and removes the configured PHP modules.
* Deploys the `z00-linuxfabrik.ini` for every SAPI.
* Deploys and removes the PHP-FPM pools, and the `[global]` drop-in next to them.
* Creates the PHP-FPM log directory.
* Deploys the logrotate configuration for the per-pool logs (Debian only).
* Manages the state of the php-fpm service.
* Pins the `php`, `phar` and `phar.phar` alternatives (Debian with `php__version` set only).
* Triggers: php-fpm.service restart.

`php:alternatives`

* Debian with `php__version` set only. Pins the `php`, `phar` and `phar.phar` alternatives to the declared version, so installing another version does not silently switch the CLI.
* Triggers: none.

`php:fpm`

* Deploys and removes the PHP-FPM pools, the `[global]` drop-in and the log directory. On Debian the configuration lives under the declared version's tree, on RedHat under `/etc/php-fpm.d`.
* Triggers: php-fpm.service restart.

`php:ini`

* Deploys the `z00-linuxfabrik.ini`. RedHat has a single `/etc/php.d`, Debian one conf.d per SAPI (apache2, cli and fpm) below the declared version's tree.
* Triggers: php-fpm.service restart.

`php:logrotate`

* Debian only. Deploys `/etc/logrotate.d/php-fpm-pools` for the per-pool logs. On RedHat the packaged logrotate configuration already covers them.
* Triggers: none.

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

        * Optional. The Unix user running the pool processes.
        * Type: String.
        * Default: `'apache'`

    * `group`:

        * Optional. The Unix group running the pool processes.
        * Type: String.
        * Default: `'apache'`

    * `raw`:

        * Optional. Raw content which will be added to the end of the pool config.
        * Type: String.

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


## Optional Role Variables - PHP-FPM Global Config Directives

Variables for the `[global]` section of the PHP-FPM configuration, deployed as `z00-linuxfabrik-global.conf` next to the pools.

`php__fpm_conf_emergency_restart_interval__group_var` / `php__fpm_conf_emergency_restart_interval__host_var`

* The window `php__fpm_conf_emergency_restart_threshold__*_var` counts within. Available units: s(econds), m(inutes), h(ours), or d(ays).
* Type: String.
* Default: `'1m'`
* Deviates from the upstream default `0`: PHP-FPM needs a non-zero threshold and a non-zero interval before it reloads itself after repeated worker crashes, so leaving either at zero turns the safety net off.

`php__fpm_conf_emergency_restart_threshold__group_var` / `php__fpm_conf_emergency_restart_threshold__host_var`

* Reload PHP-FPM once this many workers died on `SIGSEGV` or `SIGBUS` within `php__fpm_conf_emergency_restart_interval__*_var`. A value of `0` means off.
* Type: Number.
* Default: `10`
* Deviates from the upstream default `0`: an extension or opcode cache that corrupts its workers otherwise keeps crashing them until someone notices, while a reload of the master usually restores service. PHP-FPM writes a WARNING when it triggers, so the underlying crash still surfaces in monitoring rather than being papered over.

`php__fpm_conf_log_level__group_var` / `php__fpm_conf_log_level__host_var`

* The log level of PHP-FPM's own error log. Possible values: `alert`, `error`, `warning`, `notice`, `debug`.
* Type: String.
* Default: `'notice'`
* Matches the upstream default, but is pinned rather than left unset: PHP-FPM keeps the unset value at zero internally, so `php-fpm -tt` dumps `log_level = unknown value` and an administrator cannot read the level that is actually in effect. Raising it to `warning` drops the start, reload and shutdown markers that make a pool restarting in a loop visible.

Example:
```yaml
# optional
php__fpm_conf_emergency_restart_interval__host_var: '1m'
php__fpm_conf_emergency_restart_threshold__host_var: 10
php__fpm_conf_log_level__host_var: 'notice'
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
* Default: `10`
* Deviates from the upstream default (`5` on RedHat, `1` on Debian): against `php__fpm_pool_conf_pm_max_children__*_var` of 50 the packaged value keeps so small a warm reserve that an ordinary traffic spike exhausts it in seconds, and PHP-FPM then forks in doubling bursts and logs a `seems busy` warning every second. Each idle worker costs its own memory, so lower it again on hosts that are tight.

`php__fpm_pool_conf_pm_start_servers__group_var` / `php__fpm_pool_conf_pm_start_servers__host_var`

* The number of child processes created on startup. Must be greater than `php__fpm_pool_conf_pm_min_spare_servers__*_var` but less than `php__fpm_pool_conf_pm_max_spare_servers__*_var`.
* Type: Number.
* Default: `10`
* Deviates from the upstream default (`5` on RedHat, `2` on Debian): the first requests after a restart otherwise arrive while the pool is still forking.

`php__fpm_pool_conf_request_slowlog_timeout__group_var` / `php__fpm_pool_conf_request_slowlog_timeout__host_var`

* The timeout for serving a single request after which a PHP backtrace will be dumped to the slowlog file. A value of `0` means off. Available units: s(econds, default), m(inutes), h(ours), or d(ays).
* Type: Number.
* Default: `0`
* Off by default on purpose. PHP-FPM collects the backtrace with `ptrace`, which SELinux denies to the `httpd_t` domain the master and its workers both run in. On an enforcing RedHat host every slow request therefore produces `ERROR: failed to ptrace(ATTACH) child N: Operation not permitted` in the error log while the slowlog stays empty, which turns a monitoring check reading that log critical without a finding. Set it on Debian, or on RedHat only together with an SELinux policy module that grants `httpd_t` the `sys_ptrace` capability.

`php__fpm_pool_conf_request_terminate_timeout__group_var` / `php__fpm_pool_conf_request_terminate_timeout__host_var`

* The timeout for serving a single request after which the worker process will be killed. This option should be used when the `max_execution_time` ini option does not stop script execution for some reason. A value of `0` means off. Available units: s(econds, default), m(inutes), h(ours), or d(ays).
* Type: Number.
* Default: `3900`
* Deviates from the upstream default `0`: a worker blocked in a system call, on a database socket that never answers for example, holds its slot forever and the pool bleeds capacity until it is full. The value sits five minutes above the 3600 seconds Nextcloud raises `max_execution_time` to for large uploads, so PHP's own limit always fires first and this one only catches what PHP cannot stop itself. Raise it for workloads with legitimately longer requests, or set `0` to restore the previous behaviour.

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
php__fpm_pool_conf_pm_min_spare_servers__host_var: 10
php__fpm_pool_conf_pm_start_servers__host_var: 10
php__fpm_pool_conf_request_slowlog_timeout__host_var: 0
php__fpm_pool_conf_request_terminate_timeout__host_var: '3900s'
php__fpm_pools__host_var:
  - name: 'librenms'
    user: 'librenms'
    group: 'librenms'
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
