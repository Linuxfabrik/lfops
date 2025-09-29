# Ansible Role linuxfabrik.lfops.icingaweb2_module_reporting

This role installs and configures the [IcingaWeb2 Reporting Module](https://icinga.com/docs/icinga-reporting/).

This role is tested with the following IcingaWeb2 Reporting Module versions:

* 1.0.2


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.
* A SQL database and user. This can be done using the [linuxfabrik.lfops.mariadb_server](https://github.com/linuxfabrik/lfops/tree/main/roles/mariadb_server) role.

If you use the [Setup Icinga2 Master Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_icinga2_master.yml) and set `setup_icinga2_master__skip_icingaweb2_module_reporting: false`, this is automatically done for you.

* Additionally, the [IcingaWeb2 PDF Export Module](https://github.com/Icinga/icingaweb2-module-pdfexport) for exporting to PDF (else only CSV and JSON are available).


## Tags

| Tag                      | What it does                                       | Reload / Restart |
| ---                      | ------------                                       | ---------------- |
| `icingaweb2_module_reporting` | Installs and configures the IcingaWeb2 Reporting Module | - |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `icingaweb2_module_reporting__database_login` | The user account for accessing the reporting SQL database. Currently, only MySQL is supported. |
| `icingaweb2_module_reporting__version` | The module version to install. Possible options: https://github.com/Icinga/icingaweb2-module-reporting/releases |

Example:
```yaml
# mandatory
icingaweb2_module_reporting__database_login:
  username: 'icinga_reporting_user'
  password: 'linuxfabrik'
icingaweb2_module_reporting__version: 'v1.0.2'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icingaweb2_module_reporting__database_host` | The host of the SQL database server. | `'localhost'` |
| `icingaweb2_module_reporting__database_name` | The name of the reporting SQL database. | `'icinga_reporting'` |
| `icingaweb2_module_reporting__service_enabled` | Enables or disables the reporting service, analogous to `systemctl enable/disable --now`. | `true` on the primary Icinga2 Master |

Example:
```yaml
# optional
icingaweb2_module_reporting__database_host: 'localhost'
icingaweb2_module_reporting__database_name: 'icinga_reporting'
icingaweb2_module_reporting__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
