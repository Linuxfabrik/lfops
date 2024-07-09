# Ansible Role linuxfabrik.lfops.icingaweb2_module_generictts

This role installs and configures the [IcingaWeb2 GenericTTS Module](https://github.com/Icinga/icingaweb2-module-generictts).

This role is tested with the following IcingaWeb2 GenericTTS Module versions:

* 2.1.0


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.


## Tags

| Tag                            | What it does                                             |
| ---                            | ------------                                             |
| `icingaweb2_module_generictts` | Installs and configures the IcingaWeb2 GenericTTS Module |


## Mandatory Role Variables

| Variable                                | Description                                                                                                       |
| --------                                | -----------                                                                                                       |
| `icingaweb2_module_generictts__version` | The module version to install. Possible options: https://github.com/Icinga/icingaweb2-module-generictts/releases. |

Example:
```yaml
# mandatory
icingaweb2_module_generictts__version: 'v2.1.0'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icingaweb2_module_generictts__url` | The URL from where to download the IcingaWeb2 GenericTTS Module. | `https://github.com/Icinga/icingaweb2-module-generictts/archive/{{ icingaweb2_module_generictts__version }}.tar.gz` |

Example:
```yaml
# optional
icingaweb2_module_generictts__url: 'https://github.com/Linuxfabrik/icingaweb2-module-generictts/archive/{{ icingaweb2_module_generictts__version }}.tar.gz'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
