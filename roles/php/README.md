# Ansible Role php

This role installs and configures PHP (and PHP-FPM) on the system, optionally with additional modules.

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


#### php__ini_display_errors

The value for the php `display_errors` setting. Have a look at the [php documentation](https://www.php.net/manual/en/errorfunc.configuration.php#ini.display-errors).

Default:
```yaml
php__ini_display_errors: 'Off'
```


#### php__ini_display_startup_errors

The value for the php `display_startup_errors` setting. Have a look at the [php documentation](https://www.php.net/manual/en/errorfunc.configuration.php#ini.display-startup-errors).

Default:
```yaml
php__ini_display_startup_errors: 'Off'
```


#### php__ini_error_reporting

The value for the php `error_reporting` setting. Have a look at the [php documentation](https://www.php.net/manual/en/errorfunc.configuration.php#ini.error-reporting).

Default:
```yaml
php__ini_error_reporting: 'E_ALL & ~E_NOTICE & ~E_DEPRECATED & ~E_STRICT'
```


#### php__ini_max_execution_time

todo
The value for the PHP `max_execution_time` setting. Have a look at the [php documentation](https://www.php.net/manual/en/info.configuration.php#ini.max-execution-time).

Default:
```yaml
php__ini_max_execution_time: 30
```


#### php__ini_max_file_uploads

The value for the PHP `max_file_uploads` setting. Have a look at the [php documentation](https://www.php.net/manual/en/ini.core.php#ini.max-file-uploads).

Default:
```yaml
php__ini_max_file_uploads: 50
```


#### php__ini_max_input_time

The value for the php `max_input_time` setting. Have a look at the [php documentation](https://www.php.net/manual/en/info.configuration.php#ini.max-input-time).

Default:
```yaml
php__ini_max_input_time: 300
```


#### php__ini_memory_limit

The value for the PHP `memory_limit` setting. Have a look at the [php documentation](https://www.php.net/manual/en/ini.core.php#ini.memory-limit).

Default:
```yaml
php__ini_memory_limit: '64M'
```


#### php__ini_post_max_size

The value for the PHP `post_max_size` setting. Have a look at the [php documentation](https://www.php.net/manual/en/ini.core.php#ini.post-max-size).

Default:
```yaml
php__ini_post_max_size: '50M'
```


#### php__ini_session_sid_length

The value for the PHP `session.sid_length` setting. Have a look at the [php documentation](https://www.php.net/manual/en/session.configuration.php#ini.session.sid-length).

Default:
```yaml
php__ini_session_sid_length: 32
```


#### php__ini_session_trans_sid_tags

The value for the PHP `session.trans_sid_tags` setting. Have a look at the [php documentation](https://www.php.net/manual/en/session.configuration.php#ini.session.trans-sid-tags).

Default:
```yaml
php__ini_session_trans_sid_tags: 'a=href,area=href,frame=src,input=src,form=fakeentry'
```


#### php__ini_smtp

The value for the PHP `SMTP` setting. Have a look at the [php documentation](https://www.php.net/manual/en/mail.configuration.php#ini.smtp).

Default:
```yaml
php__ini_smtp: 'localhost'
```


#### php__ini_upload_max_filesize

The value for the PHP `upload_max_filesize` setting. Have a look at the [php documentation](https://www.php.net/manual/en/ini.core.php#ini.upload-max-filesize).

Default:
```yaml
php__ini_upload_max_filesize: '20M'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
