# Ansible Role linuxfabrik.lfops.icingaweb2_module_x509

This role installs and configures the [IcingaWeb2 x509 Module](https://icinga.com/docs/icinga-certificate-monitoring/latest/doc/01-About/).

Runs on

* RHEL 8 (and compatible)

This role is tested with the following IcingaWeb2 x509 Module versions:

* 1.3.1


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.
* A SQL database and user. This can be done using the [linuxfabrik.lfops.mariadb_server](https://github.com/linuxfabrik/lfops/tree/main/roles/mariadb_server) role.

If you use the [Setup Icinga2 Master Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_icinga2_master.yml) and set `setup_icinga2_master__skip_icingaweb2_module_x509: false`, this is automatically done for you.


## Tags

| Tag                      | What it does                                       |
| ---                      | ------------                                       |
| `icingaweb2_module_x509` | Installs and configures the IcingaWeb2 x509 Module |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `icingaweb2_module_x509__database_login` | The user account for accessing the x509 SQL database. Currently, only MySQL is supported. |
| `icingaweb2_module_x509__version` | The module version to install. Possible options: https://github.com/Icinga/icingaweb2-module-x509/releases |

Example:
```yaml
# mandatory
icingaweb2_module_x509__database_login:
  username: 'icinga_x509_user'
  password: 'linuxfabrik'
icingaweb2_module_x509__version: 'v1.3.1'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icingaweb2_module_x509__database_host` | The host of the SQL database server. | `'localhost'` |
| `icingaweb2_module_x509__database_name` | The name of the x509 SQL database. | `'icinga_x509'` |

Example:
```yaml
# optional
icingaweb2_module_x509__database_host: 'localhost'
icingaweb2_module_x509__database_name: 'icinga_x509'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
