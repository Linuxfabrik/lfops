# Ansible Role linuxfabrik.lfops.icingaweb2_module_cube

This role installs and configures the [IcingaWeb2 Cube Module](https://github.com/Icinga/icingaweb2-module-cube).

This role is tested with the following IcingaWeb2 Cube Module versions:

* 1.3.3


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.


## Tags

| Tag                      | What it does                                       |
| ---                      | ------------                                       |
| `icingaweb2_module_cube` | Installs and configures the IcingaWeb2 Cube Module |


## Mandatory Role Variables

| Variable                          | Description                                                                                                 |
| --------                          | -----------                                                                                                 |
| `icingaweb2_module_cube__version` | The module version to install. Possible options: https://github.com/Icinga/icingaweb2-module-cube/releases. |

Example:
```yaml
# mandatory
icingaweb2_module_cube__version: 'v1.3.3'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icingaweb2_module_cube__url` | The URL from where to download the IcingaWeb2 Cube Module. | `https://github.com/Icinga/icingaweb2-module-cube/archive/{{ icingaweb2_module_cube__version }}.tar.gz` |

Example:
```yaml
# optional
icingaweb2_module_cube__url: 'https://github.com/Linuxfabrik/icingaweb2-module-cube/archive/{{ icingaweb2_module_cube__version }}.tar.gz'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
