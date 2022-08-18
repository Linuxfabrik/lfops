# Ansible Role linuxfabrik.lfops.icingaweb2_module_vspheredb

This role installs and configures the [IcingaWeb2 vSphereDB Module](https://github.com/Icinga/icingaweb2-module-vspheredb).

Tested on

* RHEL 7 (and compatible)


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.


## Tags

| Tag                           | What it does                                            |
| ---                           | ------------                                            |
| `icingaweb2_module_vspheredb` | Installs and configures the IcingaWeb2 vSphereDB Module |


## Mandatory Role Variables

| Variable                               | Description                                                                                                         |
| --------                               | -----------                                                                                                         |
| `icingaweb2_module_vspheredb__version` | The Module version to install. Can be found [here](https://github.com/Icinga/icingaweb2-module-vspheredb/releases). |

Example:
```yaml
# mandatory
icingaweb2_module_vspheredb__version: '1.4.0'
```


## Optional Role Variables

| Variable                                    | Description               | Default Value       |
| --------                                    | -----------               | -------------       |
| `icingaweb2_module_vspheredb__daemon_group` | The systemd daemon group. | `'icingaweb2'`      |
| `icingaweb2_module_vspheredb__daemon_user`  | The systemd daemon user.  | `'icingavspheredb'` |
| `icingaweb2_module_vspheredb_resource`      | The resource DB name.     | `'vSphereDB'`       |

Example:
```yaml
# optional
icingaweb2_module_vspheredb__daemon_group: 'icingaweb2'
icingaweb2_module_vspheredb__daemon_user: 'icingavspheredb'
icingaweb2_module_vspheredb__resource: 'vSphereDB'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
