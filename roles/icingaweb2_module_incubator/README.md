# Ansible Role linuxfabrik.lfops.icingaweb2_module_incubator

This role installs and enables the [IcingaWeb2 Incubator Module](https://github.com/Icinga/icingaweb2-module-incubator).

Runs on

* RHEL 8 (and compatible)

This role is tested with the following IcingaWeb2 Grafana Module versions:

* 0.17.0
* 0.20.0


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.


## Tags

| Tag                           | What it does                                         |
| ---                           | ------------                                         |
| `icingaweb2_module_incubator` | Installs and enables the IcingaWeb2 Incubator Module |


## Mandatory Role Variables

| Variable                               | Description                                                                                                      |
| --------                               | -----------                                                                                                      |
| `icingaweb2_module_incubator__version` | The module version to install. Possible options: https://github.com/Icinga/icingaweb2-module-incubator/releases. |

Example:
```yaml
# mandatory
icingaweb2_module_incubator__version: 'v0.16.1'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
