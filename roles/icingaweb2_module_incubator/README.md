# Ansible Role icingaweb2_module_incubator

This role installs and enables the [IcingaWeb2 Incubator Module](https://github.com/Icinga/icingaweb2-module-incubator).

FQCN: linuxfabrik.lfops.icingaweb2_module_incubator

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag                         | What it does                                         |
| ---                         | ------------                                         |
| icingaweb2_module_incubator | Installs and enables the IcingaWeb2 Incubator Module |


## Role Variables

### Mandatory


The module version to install. Possible options: https://github.com/Icinga/icingaweb2-module-incubator/releases.

Example:
```yaml
icingaweb2_module_incubator__version: 'v0.16.1'
```


### Optional

This role does not have any optional variables.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
