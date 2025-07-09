# Ansible Role linuxfabrik.lfops.icingaweb2_module_pdfexport

This role installs and enables the [IcingaWeb2 pdfexport Module](https://github.com/Icinga/icingaweb2-module-pdfexport).

This role is tested with the following IcingaWeb2 PDF Export Module versions:

* 0.11.0


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.


## Tags

| Tag                           | What it does                                         |
| ---                           | ------------                                         |
| `icingaweb2_module_pdfexport` | Installs and enables the IcingaWeb2 pdfexport Module |


## Mandatory Role Variables

| Variable                               | Description                                                                                                      |
| --------                               | -----------                                                                                                      |
| `icingaweb2_module_pdfexport__version` | The module version to install. Possible options: https://github.com/Icinga/icingaweb2-module-pdfexport/releases. |

Example:
```yaml
# mandatory
icingaweb2_module_pdfexport__version: 'v0.11.0'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
