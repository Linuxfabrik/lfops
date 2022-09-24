# Ansible Role linuxfabrik.lfops.php

This role installs and configures PHP (and PHP-FPM) on the system, optionally with additional modules.

Note that this role does NOT let you specify a particular PHP version. It simply installs the latest available PHP version from the repos configured in the system. If you want or need to install a specific or the latest PHP version available, use the [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) beforehand.

Nevertheless, this role is only compatible with the following PHP versions:

* 7.2
* 7.3
* 7.4
* 8.0
* 8.1

Rules of thumb:

* Specify memory values in MB (M).
* `memory_limit` should be larger than `post_max_size`.
* `post_max_size` can stay at `16M`, even if you have `upload_max_filesize` > `10000M` for example.
* If disabling `opcache.validate_timestamps`, `opcache.revalidate_freq` is ignored.

This role never exposes to the world that PHP is installed on the server.

Runs on

* RHEL 8 (and compatible)


## Optional Requirements

* Enable the [Remi's RPM repository](https://rpms.remirepo.net/) to get newer versions of PHP. This can be done using the [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) role.


## Tags

| Tag         | What it does                                                                   |
| ---         | ------------                                                                   |
| `php`       | Installs and configures PHP on the system, optionally with additional modules. |
| `php:state` | Manages the state of the php-fpm service                                       |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `php__fpm_service_enabled` | Enables or disables the php-fpm service, analogous to `systemctl enable/disable --now`. | `true` |
| `php__fpm_pools__host_var` /<br> `php__fpm_pools__group_var` | List of PHP-FPM pools. Subkeys:<br> * `name`: Required, string. The name of the pool. Will also be used as the filename and for logfiles.<br> * `state`: Required, boolean. State of the pool. Possible options: `absent`, `present`.<br> * `user`: Optional, string. Defaults to `apache`. The Unix user running the pool processes.<br> * `group`: Optional, string. Defaults to `apache`. The Unix group running the pool processes.<br> * `raw`: Optional, string: Raw content which will be added to the end of the pool config.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `{}` |
| `php__modules__host_var` /<br> `php__modules__group_var` | List of additional PHP modules that should be installed via the standard package manager. Subkeys:<br> * `name`: Required, string. Name of the module package.<br> * `state`: State of the module package. Possible options: `absent`, `present`.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | * `php-opcache` |

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
php__fpm_pools__group_var: []
php__modules__host_var:
  - name: 'php-mysqlnd'
    state: 'present'
php__modules__group_var: []
```


### `php__ini_*` config directives

Variables for `php.ini` directives and their default values, defined and supported by this role.

| Role Variable                              | Documentation                                                         | Default Value                                           |
| -------------                              | -------------                                                         | -------------                                           |
| `php__ini_date_timezone__group_var` / `php__ini_date_timezone__host_var`                   | [php.net](https://www.php.net/manual/en/datetime.configuration.php)   | `'Europe/Zurich'`                                       |
| `php__ini_default_socket_timeout__group_var` / `php__ini_default_socket_timeout__host_var`          | [php.net](https://www.php.net/manual/en/filesystem.configuration.php) | `10`                                                    |
| `php__ini_display_errors__group_var` / `php__ini_display_errors__host_var`                 | This determines whether errors should be printed to the screen as part of the output or if they should be hidden from the user. This is a feature to support your development and should never be used on production systems (e.g. systems connected to the internet). [php.net](https://www.php.net/manual/en/errorfunc.configuration.php)  | `'Off'`                                                 |
| `php__ini_display_startup_errors__group_var` / `php__ini_display_startup_errors__host_var`          | Even when display_errors is on, errors that occur during PHP's startup sequence are not displayed. It's strongly recommended to keep  [php.net](https://www.php.net/manual/en/errorfunc.configuration.php)  | `'Off'`                                                 |
| `php__ini_error_reporting__group_var` / `php__ini_error_reporting__host_var`                 | Set the error reporting level. [php.net](https://www.php.net/manual/en/errorfunc.configuration.php)  | `'E_ALL & ~E_NOTICE & ~E_DEPRECATED & ~E_STRICT'`       |
| `php__ini_max_execution_time__group_var` / `php__ini_max_execution_time__host_var`              | This sets the maximum time in seconds a script is allowed to run before it is terminated by the parser. This helps prevent poorly written scripts from tying up the server. The default setting is 30. When running PHP from the command line the default setting is 0. [php.net](https://www.php.net/manual/en/info.configuration.php)       | `30`                                                    |
| `php__ini_max_file_uploads__group_var` / `php__ini_max_file_uploads__host_var`                | The maximum number of files allowed to be uploaded simultaneously. [php.net](https://www.php.net/manual/en/ini.core.php)                 | `50`                                                    |
| `php__ini_max_input_time__group_var` / `php__ini_max_input_time__host_var`                  | This sets the maximum time in seconds a script is allowed to parse input data, like POST and GET. Timing begins at the moment PHP is invoked at the server and ends when execution begins. The default setting is -1, which means that max_execution_time is used instead. Set to 0 to allow unlimited time. [php.net](https://www.php.net/manual/en/info.configuration.php)       | `-1`                                                    |
| `php__ini_memory_limit__group_var` / `php__ini_memory_limit__host_var`               | This sets the maximum amount of memory in bytes that ONE RUNNING SCRIPT is allowed to allocate. This helps prevent poorly written scripts for eating up all available memory on a server. Note that to have no memory limit, set this directive to -1. memory_limit should be larger than post_max_size. Again: PHP memory_limit is per-script, just as a highway's speed limit is per-vehicle. [php.net](https://www.php.net/manual/en/ini.core.php)                 | `'128M'`                                                |
| `php__ini_opcache_blacklist_filename__group_var` / `php__ini_opcache_blacklist_filename__host_var`      | A blacklist file is a text file containing the names of files that should not be accelerated, one per line. Wildcards are allowed, and prefixes can also be provided. Lines starting with a semi-colon are ignored as comments. [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `'/etc/php-zts.d/opcache*.blacklist'`                   |
| `php__ini_opcache_enable__group_var` / `php__ini_opcache_enable__host_var`                  | Enables the opcode cache. When disabled, code is not optimised or cached.[php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `1`                                                     |
| `php__ini_opcache_enable_cli__group_var` / `php__ini_opcache_enable_cli__host_var`              | Enables the opcode cache for the CLI version of PHP. [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `1`                                                     |
| `php__ini_opcache_huge_code_pages__group_var` / `php__ini_opcache_huge_code_pages__host_var`         | [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `1`                                                     |
| `php__ini_opcache_interned_strings_buffer__group_var` / `php__ini_opcache_interned_strings_buffer__host_var` | The amount of memory used to store interned strings, in megabytes. [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `12`                                                    |
| `php__ini_opcache_max_accelerated_files__group_var` / `php__ini_opcache_max_accelerated_files__host_var`   | The maximum number of keys (and therefore scripts) in the OPcache hash table. The actual value ;used will be the first number in the set of prime numbers { 223, 463, 983, 1979, 3907, 7963, 16229, 32531, 65407, 130987, 262237, 524521, 1048793 } that is greater than or equal to the configured value. [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `7963`                                                  |
| `php__ini_opcache_memory_consumption__group_var` / `php__ini_opcache_memory_consumption__host_var`      | The size of the shared memory storage used by OPcache, in megabytes. The minimum permissible value is "8", which is enforced if a smaller value is set. [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `128`                                                   |
| `php__ini_opcache_revalidate_freq__group_var` / `php__ini_opcache_revalidate_freq__host_var`         | How often to check script timestamps for updates, in seconds. 0 will result in OPcache checking for updates on every request. [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `60`                                                    |
| `php__ini_opcache_save_comments__group_var` / `php__ini_opcache_save_comments__host_var`           | If disabled, all documentation comments will be discarded from the opcode cache to reduce the size of the optimised code. Disabling this configuration directive may break applications and frameworks that rely on comment parsing for annotations. [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `1`                                                     |
| `php__ini_opcache_validate_timestamps__group_var` / `php__ini_opcache_validate_timestamps__host_var`     | If enabled, OPcache will check for updated scripts every opcache.revalidate_freq seconds. When this directive is disabled, you must reset OPcache manually via opcache_reset(), opcache_invalidate() or by restarting the Web server for changes to the filesystem to take effect. [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `1`                                                     |
| `php__ini_post_max_size__group_var` / `php__ini_post_max_size__host_var`                   | Sets max size of post data allowed. This setting also affects file upload. To upload large files, this value must be larger than upload_max_filesize. Generally speaking, memory_limit should be larger than post_max_size. [php.net](https://www.php.net/manual/en/ini.core.php)                 | `'16M'`                                                 |
| `php__ini_session_sid_length__group_var` / `php__ini_session_sid_length__host_var`              | [php.net](https://www.php.net/manual/en/session.configuration.php)    | `32`                                                    |
| `php__ini_session_trans_sid_tags__group_var` / `php__ini_session_trans_sid_tags__host_var`          | [php.net](https://www.php.net/manual/en/session.configuration.php)    | `'a=href,area=href,frame=src,input=src,form=fakeentry'` |
| `php__ini_smtp__group_var` / `php__ini_smtp__host_var`                            | [php.net](https://www.php.net/manual/en/mail.configuration.php)       | `'localhost'`                                           |
| `php__ini_upload_max_filesize__group_var` / `php__ini_upload_max_filesize__host_var`             | The maximum size of an uploaded file. [php.net](https://www.php.net/manual/en/ini.core.php)                 | `'20M'`                                                 |

Note that setting `php__ini_opcache_huge_code_pages__group_var` or `php__ini_opcache_huge_code_pages__host_var` to `1` might require enabling the SELinux boolean `httpd_execmem` on RHEL systems.

Example:
```yaml
# optional
php__ini_max_execution_time__host_var: 3600
php__ini_max_file_uploads__host_var: 100
php__ini_memory_limit__host_var: '1024M'
php__ini_upload_max_filesize__host_var: '10000M'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
