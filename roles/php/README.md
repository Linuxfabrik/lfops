# Ansible Role php

This role installs and configures PHP (and PHP-FPM) on the system, optionally with additional modules.

Note that this role does NOT let you specify a particular PHP version. It simply installs the latest available PHP version from the repos configured in the system. If you want or need to install a specific PHP version, use the [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) beforehand.

Nevertheless, this role is only compatible with PHP versions

* 7.2
* 7.3
* 7.4
* 8.0

FQCN: linuxfabrik.lfops.php

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

This role does not have any mandatory requirements.

### Optional

* Enable the [Remi's RPM repository](https://rpms.remirepo.net/) to get newer versions of PHP. This can be done using the [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) role.


## Tags

| Tag       | What it does                                                                   |
| ---       | ------------                                                                   |
| php       | Installs and configures PHP on the system, optionally with additional modules. |
| php:state | Manages the state of the php-fpm service                                       |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/php/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### php__host_modules / php__group_modules

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

List of additional PHP modules that should be installed via the standard package manager.

Default:
```yaml
php__group_modules: []
php__host_modules: []
php__role_modules:
  - 'php-opcache'
```


#### php__fpm_service_enabled

Enables or disables the php-fpm service, analogous to `systemctl enable/disable --now`. Possible options:

* true
* false


Default:
```yaml
php__fpm_service_enabled: true
```


#### php__ini_* config directives

Variables for `php.ini` directives and their default values, defined and supported by this role.

| Role Variable                             | Default                               | Documentation                                                 |
|---------------                            |---------                              |---------------                                                |
| php__ini_date_timezone                    | 'Europe/Zurich'                       | [php.net](https://www.php.net/manual/en/datetime.configuration.php)      |
| php__ini_default_socket_timeout           | 10                                    | [php.net](https://www.php.net/manual/en/filesystem.configuration.php)    |
| php__ini_display_errors                   | 'Off'                                 | [php.net](https://www.php.net/manual/en/errorfunc.configuration.php)     |
| php__ini_display_startup_errors           | 'Off'                                 | [php.net](https://www.php.net/manual/en/errorfunc.configuration.php)     |
| php__ini_error_reporting                  | 'E_ALL & ~E_NOTICE & ~E_DEPRECATED & ~E_STRICT' | [php.net](https://www.php.net/manual/en/errorfunc.configuration.php) |
| php__ini_max_execution_time               | 30                                    | [php.net](https://www.php.net/manual/en/info.configuration.php)          |
| php__ini_max_file_uploads                 | 50                                    | [php.net](https://www.php.net/manual/en/ini.core.php)                    |
| php__ini_max_input_time                   | -1                                    | [php.net](https://www.php.net/manual/en/info.configuration.php)          |
| php__ini_memory_limit                     | '128M'                                | [php.net](https://www.php.net/manual/en/ini.core.php)                    |
| php__ini_opcache_blacklist_filename       | '/etc/php-zts.d/opcache*.blacklist'   | [php.net](https://www.php.net/manual/en/opcache.configuration.php)       |
| php__ini_opcache_enable                   | 1                                     | [php.net](https://www.php.net/manual/en/opcache.configuration.php)       |
| php__ini_opcache_enable_cli               | 1                                     | [php.net](https://www.php.net/manual/en/opcache.configuration.php)       |
| php__ini_opcache_huge_code_pages          | 1                                     | [php.net](https://www.php.net/manual/en/opcache.configuration.php)       |
| php__ini_opcache_interned_strings_buffer  | 12                                    | [php.net](https://www.php.net/manual/en/opcache.configuration.php)       |
| php__ini_opcache_max_accelerated_files    | 7963                                  | [php.net](https://www.php.net/manual/en/opcache.configuration.php)       |
| php__ini_opcache_memory_consumption       | 128                                   | [php.net](https://www.php.net/manual/en/opcache.configuration.php)       |
| php__ini_opcache_revalidate_freq          | 60                                    | [php.net](https://www.php.net/manual/en/opcache.configuration.php)       |
| php__ini_opcache_save_comments            | 1                                     | [php.net](https://www.php.net/manual/en/opcache.configuration.php)       |
| php__ini_opcache_validate_timestamps      | 1                                     | [php.net](https://www.php.net/manual/en/opcache.configuration.php)       |
| php__ini_post_max_size                    | '16M'                                 | [php.net](https://www.php.net/manual/en/ini.core.php)                    |
| php__ini_session_sid_length               | 32                                    | [php.net](https://www.php.net/manual/en/session.configuration.php)       |
| php__ini_session_trans_sid_tags           | 'a=href,area=href,frame=src,input=src,form=fakeentry' | [php.net](https://www.php.net/manual/en/session.configuration.php) |
| php__ini_smtp                             | 'localhost'                           | [php.net](https://www.php.net/manual/en/mail.configuration.php)          |
| php__ini_upload_max_filesize              | '20M'                                 | [php.net](https://www.php.net/manual/en/ini.core.php)                    |


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
