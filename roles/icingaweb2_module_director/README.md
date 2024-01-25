# Ansible Role linuxfabrik.lfops.icingaweb2_module_director

This role installs and configures the [IcingaWeb2 Director Module](https://icinga.com/docs/icinga-director/latest/doc/01-Introduction/), and deploys the baskets from the [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins).

Runs on

* RHEL 8 (and compatible)

This role is tested with the following IcingaWeb2 Director Module versions:

* 1.10.2
* 1.10.2.2023042001


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.
* A SQL database and user. This can be done using the [linuxfabrik.lfops.mariadb_server](https://github.com/linuxfabrik/lfops/tree/main/roles/mariadb_server) role.


## Tags

| Tag                                 | What it does                                                                                                      |
| ---                                 | ------------                                                                                                      |
| `icingaweb2_module_director`        | Installs and configures the IcingaWeb2 Director Module                                                            |
| `icingaweb2_module_director:basket` | Deploys the baskets from the [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins). |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `icingaweb2_module_director__api_user_login` | The account for accessing the Icinga2 API. |
| `icingaweb2_module_director__database_login` | The user account for accessing the Director SQL database. Currently, only MySQL is supported. |
| `icingaweb2_module_director__enrolment_user_login` | A IcingaWeb2 account with the `module/director,director/api,director/hosts` permissions, allowing it to enrol new hosts in the Icinga Director. Note that the username has to be `enrolment-user` for the account to have the correct permissions. |
| `icingaweb2_module_director__version` | The module version to install. Possible options from either:<ul><li>https://github.com/Icinga/icingaweb2-module-director/releases</li><li>https://git.linuxfabrik.ch/linuxfabrik/icingaweb2-module-director/-/releases</li></ul>Have a look at `icingaweb2_module_director__url`. |

Example:
```yaml
# mandatory
icingaweb2_module_director__api_user_login:
  username: 'icinga-director-api'
  password: 'linuxfabrik'
icingaweb2_module_director__database_login:
  username: 'icinga_director_user'
  password: 'linuxfabrik'
icingaweb2_module_director__enrolment_user_login:
  username: 'enrolment-user'
  password: 'linuxfabrik'
icingaweb2_module_director__version: 'v1.8.1.2021090901'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icingaweb2_module_director__api_endpoint` | The endpoint name for accessing the Icinga2 API. | `'{{ icinga2_master__cn }}'` |
| `icingaweb2_module_director__api_host` | The host for accessing the Icinga2 API. | `'localhost'` |
| `icingaweb2_module_director__api_port` | The port for accessing the Icinga2 API. | `5665` |
| `icingaweb2_module_director__database_host` | The host of the SQL database server. | `'localhost'` |
| `icingaweb2_module_director__database_name` | The name of the Director SQL database. | `'icinga_director'` |
| `icingaweb2_module_director__monitoring_plugins_version` | Which version of the monitoring plugins should be used for generating the Director baskets? Possible options:<ul><li>`latest`: The **latest stable** release. See the [Releases](https://github.com/Linuxfabrik/monitoring-plugins/releases).</li><li>`main`: The development version. Use with care.</li><li>A specific release, for example `2022030201`. See the [Releases](https://github.com/Linuxfabrik/monitoring-plugins/releases).</li></ul> | `'{{ lfops__monitoring_plugins_version \| default("latest") }}'` |
| `icingaweb2_module_director__skip_basket_import` | Bool. Should the Linuxfabrik Monitoring Plugins Basket be generated and imported or not? | `false` |
| `icingaweb2_module_director__url` | The URL from where to download the Director. Defaults to the Linuxfabrik Fork of the Icinga Director. If using the official Icinga Director, the link is `'https://codeload.github.com/Icinga/icingaweb2-module-director/tar.gz/refs/tags/{{ icingaweb2_module_director__version }}'` | `https://github.com/Linuxfabrik/icingaweb2-module-director/archive/{{ icingaweb2_module_director__version }}.tar.gz` |

Example:
```yaml
# optional
icingaweb2_module_director__api_endpoint: '{{ icinga2_master__cn }}'
icingaweb2_module_director__api_host: 'localhost'
icingaweb2_module_director__api_port: 5665
icingaweb2_module_director__database_host: 'localhost'
icingaweb2_module_director__database_name: 'icinga_director'
icingaweb2_module_director__monitoring_plugins_version: 'latest'
icingaweb2_module_director__skip_basket_import: true
icingaweb2_module_director__url: 'https://github.com/Icinga/icingaweb2-module-director/archive/{{ icingaweb2_module_director__version }}.tar.gz'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
