# Ansible Role php

This role installs and configures PHP on the system, optionally with additional modules.

FQCN: linuxfabrik.lfops.php

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

This role does not have any mandatory requirements.

### Optional

* Enable the [Remi's RPM repository](https://rpms.remirepo.net/) to get newer versions of PHP. This can be done using the [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) role.


## Tags

| Tag           | What it does                                                                   |
| ---           | ------------                                                                   |
| php           | Installs and configures PHP on the system, optionally with additional modules. |
| php:configure | Configures PHP, optionally installing additional modules.                      |


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

TODO: document other variables


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
