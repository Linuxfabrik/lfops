# Ansible Role linuxfabrik.lfops.icingaweb2_module_reporting

This role installs and configures the [IcingaWeb2 Reporting Module](https://icinga.com/docs/icinga-reporting/).

This role is tested with the following IcingaWeb2 Reporting Module versions:

* 1.0.2


*Available since LFOps `3.0.0`.*


## Requirements

Manual steps:

* Deploy a configured IcingaWeb2 by running the [icingaweb2](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/icingaweb2.yml) playbook (role: [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2)).
* Deploy a SQL database server and create the database and user by running the [mariadb_server](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/mariadb_server.yml) playbook (role: [linuxfabrik.lfops.mariadb_server](https://github.com/linuxfabrik/lfops/tree/main/roles/mariadb_server)).
* Optional: deploy the IcingaWeb2 PDF Export Module by running the [icingaweb2_module_pdfexport](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/icingaweb2_module_pdfexport.yml) playbook (role: [linuxfabrik.lfops.icingaweb2_module_pdfexport](https://github.com/Linuxfabrik/lfops/tree/main/roles/icingaweb2_module_pdfexport)). It enables exporting to PDF (else only CSV and JSON are available).


## Tags

`icingaweb2_module_reporting`

* Installs and configures the IcingaWeb2 Reporting Module.
* Triggers: icingaweb2_module_reporting: systemctl daemon-reload.


## Mandatory Role Variables

`icingaweb2_module_reporting__database_login`

* The user account for accessing the reporting SQL database. Currently, only MySQL is supported.
* Type: Dictionary.

`icingaweb2_module_reporting__version`

* The module version to install. Possible options: https://github.com/Icinga/icingaweb2-module-reporting/releases.
* Type: String.

Example:

```yaml
# mandatory
icingaweb2_module_reporting__database_login:
  username: 'icinga_reporting_user'
  password: 'linuxfabrik'
icingaweb2_module_reporting__version: 'v1.0.2'
```


## Optional Role Variables

`icingaweb2_module_reporting__database_host`

* The host of the SQL database server.
* Type: String.
* Default: `'localhost'`

`icingaweb2_module_reporting__database_name`

* The name of the reporting SQL database.
* Type: String.
* Default: `'icinga_reporting'`

`icingaweb2_module_reporting__service_enabled`

* Enables or disables the reporting service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

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
