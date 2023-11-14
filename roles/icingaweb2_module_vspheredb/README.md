# Ansible Role linuxfabrik.lfops.icingaweb2_module_vspheredb

This role installs and configures the [IcingaWeb2 vSphereDB Module](https://github.com/Icinga/icingaweb2-module-vspheredb).

Runs on

* RHEL 8 (and compatible)

This role is tested with the following IcingaWeb2 vSphereDB Module versions:

* 1.6.0
* 1.7.1


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.
* A SQL database and user. This can be done using the [linuxfabrik.lfops.mariadb_server](https://github.com/linuxfabrik/lfops/tree/main/roles/mariadb_server) role.

If you use the [Setup Icinga2 Master Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_icinga2_master.yml) and set `setup_icinga2_master__skip_icingaweb2_module_vspheredb: false`, this is automatically done for you.


## Tags

| Tag                           | What it does                                            |
| ---                           | ------------                                            |
| `icingaweb2_module_vspheredb` | Installs and configures the IcingaWeb2 vSphereDB Module |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `icingaweb2_module_vspheredb__database_login` | The user account for accessing the vSphereDB SQL database. Currently, only MySQL is supported. |
| `icingaweb2_module_vspheredb__version` | The Module version to install. Can be found [here](https://github.com/Icinga/icingaweb2-module-vspheredb/releases). |

Example:
```yaml
# mandatory
icingaweb2_module_vspheredb__database_login:
  username: 'icinga_vspheredb_user'
  password: 'linuxfabrik'
icingaweb2_module_vspheredb__version: '1.6.0'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icingaweb2_module_vspheredb__database_host` | The host of the SQL database server. | `'localhost'` |
| `icingaweb2_module_vspheredb__database_name` | The name of the vspheredb SQL database. | `'icinga_vspheredb'` |
| `icingaweb2_module_vspheredb__service_enabled` | Enables or disables the vSphereDB service, analogous to `systemctl enable/disable --now`. | `true` on the primary Icinga2 Master |

Example:
```yaml
# optional
icingaweb2_module_vspheredb__database_host: 'localhost'
icingaweb2_module_vspheredb__database_name: 'icinga_vspheredb'
icingaweb2_module_vspheredb__service_enabled: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
