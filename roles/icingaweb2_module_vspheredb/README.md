# Ansible Role icingaweb2_module_vspheredb

This role installs the Icinga vSphereDB Module.

FQCN: linuxfabrik.lfops.icingaweb2_module_vspheredb

Tested on

* RHEL 7 (and compatible)


## Requirements

### Mandatory

* Configured IcingaWeb2


### Optional

This role does not have any optional requirements.


## Tags

| Tag                         | What it does                              |
| ---                         | ------------                              |
| icingaweb2_module_vspheredb | Installs the IcingaWeb2 vSphereDB Module  |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/icingaweb2_module_vspheredb/defaults/main.yml) for the variable defaults.


### Mandatory

#### icingaweb2_module_vspheredb__version

The Module version to install. Can be found [here](https://github.com/Icinga/icingaweb2-module-vspheredb/releases).

Example:
```yaml
icingaweb2_module_vspheredb__version: '1.4.0'
```


### Optional

#### icingaweb2_module_vspheredb_resource

The resource DB name.

Default:
```yaml
icingaweb2_module_vspheredb__resource: 'vSphereDB'
```


#### icingaweb2_module_vspheredb__daemon_user

The systemd daemon user.

Default:
```yaml
icingaweb2_module_vspheredb__daemon_user: 'icingavspheredb'
```


#### icingaweb2_module_vspheredb__daemon_group

The systemd daemon group.

Default:
```yaml
icingaweb2_module_vspheredb__daemon_group: 'icingaweb2'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
