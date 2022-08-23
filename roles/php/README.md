# Ansible Role linuxfabrik.lfops.php

This role installs and configures PHP (and PHP-FPM) on the system, optionally with additional modules.

Note that this role does NOT let you specify a particular PHP version. It simply installs the latest available PHP version from the repos configured in the system. If you want or need to install a specific PHP version, use the [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) beforehand.

Nevertheless, this role is only compatible with the following PHP versions:

* 7.2
* 7.3
* 7.4
* 8.0
* 8.1

Tested on

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
| `php__host_fpm_pools` /<br> `php__group_fpm_pools` | List of PHP-FPM pools. Subkeys:<br> * `name`: Required, string. The name of the pool. Will also be used as the filename and for logfiles.<br> * `state`: Required, boolean. State of the pool. Possible options: `absent`, `present`.<br> * `user`: Optional, string. Defaults to `apache`. The Unix user running the pool processes.<br> * `group`: Optional, string. Defaults to `apache`. The Unix group running the pool processes.<br> * `raw`: Optional, string: Raw content which will be added to the end of the pool config.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `php__host_modules` /<br> `php__group_modules` | List of additional PHP modules that should be installed via the standard package manager.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `['php-opcache']` |

Example:
```yaml
# optional
php__fpm_service_enabled: true
php__host_fpm_pools: []
  - name: 'librenms'
    user: 'librenms'
    group: 'librenms'
    raw: |-
      env[PATH] = /usr/local/bin:/usr/bin:/bin
php__group_fpm_pools: []
php__host_modules:
  - 'php-opcache'
  - 'php-mysqlnd'
  - 'php-bcmath'
  - 'php-common'
  - 'php-json'
  - 'php-mbstring'
  - 'php-pdo'
  - 'php-xml'
php__group_modules: []
```


### `php__ini_*` config directives

TODO

Variables for `php.ini` directives and their default values, defined and supported by this role.

| Role Variable                              | Documentation                                                         | Default Value                                           |
| -------------                              | -------------                                                         | -------------                                           |
| `php__ini_date_timezone`                   | [php.net](https://www.php.net/manual/en/datetime.configuration.php)   | `'Europe/Zurich'`                                       |
| `php__ini_default_socket_timeout`          | [php.net](https://www.php.net/manual/en/filesystem.configuration.php) | `10`                                                    |
| `php__ini_display_errors`                  | [php.net](https://www.php.net/manual/en/errorfunc.configuration.php)  | `'Off'`                                                 |
| `php__ini_display_startup_errors`          | [php.net](https://www.php.net/manual/en/errorfunc.configuration.php)  | `'Off'`                                                 |
| `php__ini_error_reporting`                 | [php.net](https://www.php.net/manual/en/errorfunc.configuration.php)  | `'E_ALL & ~E_NOTICE & ~E_DEPRECATED & ~E_STRICT'`       |
| `php__ini_max_execution_time`              | [php.net](https://www.php.net/manual/en/info.configuration.php)       | `30`                                                    |
| `php__ini_max_file_uploads`                | [php.net](https://www.php.net/manual/en/ini.core.php)                 | `50`                                                    |
| `php__ini_max_input_time`                  | [php.net](https://www.php.net/manual/en/info.configuration.php)       | `-1`                                                    |
| `php__ini_opcache_blacklist_filename`      | [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `'/etc/php-zts.d/opcache*.blacklist'`                   |
| `php__ini_opcache_enable_cli`              | [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `1`                                                     |
| `php__ini_opcache_enable`                  | [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `1`                                                     |
| `php__ini_opcache_huge_code_pages`         | [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `1`                                                     |
| `php__ini_opcache_interned_strings_buffer` | [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `12`                                                    |
| `php__ini_opcache_max_accelerated_files`   | [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `7963`                                                  |
| `php__ini_opcache_memory_consumption`      | [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `128`                                                   |
| `php__ini_opcache_revalidate_freq`         | [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `60`                                                    |
| `php__ini_opcache_save_comments`           | [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `1`                                                     |
| `php__ini_opcache_validate_timestamps`     | [php.net](https://www.php.net/manual/en/opcache.configuration.php)    | `1`                                                     |
| `php__ini_post_max_size`                   | [php.net](https://www.php.net/manual/en/ini.core.php)                 | `'16M'`                                                 |
| `php__ini_role_memory_limit`               | [php.net](https://www.php.net/manual/en/ini.core.php)                 | `'128M'`                                                |
| `php__ini_session_sid_length`              | [php.net](https://www.php.net/manual/en/session.configuration.php)    | `32`                                                    |
| `php__ini_session_trans_sid_tags`          | [php.net](https://www.php.net/manual/en/session.configuration.php)    | `'a=href,area=href,frame=src,input=src,form=fakeentry'` |
| `php__ini_smtp`                            | [php.net](https://www.php.net/manual/en/mail.configuration.php)       | `'localhost'`                                           |
| `php__ini_upload_max_filesize`             | [php.net](https://www.php.net/manual/en/ini.core.php)                 | `'20M'`                                                 |

Note that setting `php__ini_opcache_huge_code_pages` to 1 might require enabling the SELinux boolean `httpd_execmem`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
