# Ansible Role linuxfabrik.lfops.icingaweb2_module_director

This role installs and configures the [IcingaWeb2 Director Module](https://icinga.com/docs/icinga-director/latest/doc/01-Introduction/).

Tested on

* RHEL 8 (and compatible)


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.
* A SQL database and user. This can be done using the [linuxfabrik.lfops.mariadb_server](https://github.com/linuxfabrik/lfops/tree/main/roles/mariadb_server) role.


## Tags

| Tag                                 | What it does                                                                                                                                                                   |
| ---                                 | ------------                                                                                                                                                                   |
| `icingaweb2_module_director`        | Installs and configures the IcingaWeb2 Director Module                                                                                                                         |
| `icingaweb2_module_director:basket` | Deploys the baskets from the [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins). This does not run by default, only when explicitly called. |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `icingaweb2_module_director__api_user_login` | The account for accessing the Icinga2 API. |
| `icingaweb2_module_director__database_login` | The user account for accessing the Director SQL database. Currently, only MySQL is supported. |
| `icingaweb2_module_director__enrolment_user_login` | A IcingaWeb2 account with the `module/director,director/api,director/hosts` permissions, allowing it to enrol new users in the Icinga Director. Note that the username has to be `enrolment-user` for the account to have the correct permissions. |
| `icingaweb2_module_director__version` | The module version to install. Possible options from either:<br> * https://github.com/Icinga/icingaweb2-module-director/releases<br> * https://git.linuxfabrik.ch/linuxfabrik/icingaweb2-module-director/-/releases<br> Have a look at `icingaweb2_module_director__url`. |

Example:
```yaml
# mandatory
icingaweb2_module_director__api_user_login:
  username: 'icinga-director-api'
  password: 'my-secret-password'
icingaweb2_module_director__database_login:
  username: 'icinga_director_user'
  password: 'my-secret-password'
icingaweb2_module_director__enrolment_user_login:
  username: 'enrolment-user'
  password: 'my-secret-password'
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
| `icingaweb2_module_director__monitoring_plugins_version` | Which version of the monitoring plugins should be used for generating the Director baskets? Possible options:<br> * `latest`: The **latest stable** release. See the [Releases](https://github.com/Linuxfabrik/monitoring-plugins/releases).<br> * `main`: The development version. Use with care.<br> * A specific release, for example `2022030201`. See the [Releases](https://github.com/Linuxfabrik/monitoring-plugins/releases). | `'latest'` |
| `icingaweb2_module_director__url` | The URL from where to download the Director. Defaults to the Linuxfabrik Fork of the Icinga Director. | `git.linuxfabrik.ch/api/v4/projects/133/repository/archive?sha={{ icingaweb2_module_director__version }}'` |

Example:
```yaml
# optional
icingaweb2_module_director__api_endpoint: '{{ icinga2_master__cn }}'
icingaweb2_module_director__api_host: 'localhost'
icingaweb2_module_director__api_port: 5665
icingaweb2_module_director__database_host: 'localhost'
icingaweb2_module_director__database_name: 'icinga_director'
icingaweb2_module_director__monitoring_plugins_version: 'latest'
icingaweb2_module_director__url: 'https://github.com/Icinga/icingaweb2-module-director/archive/{{ icingaweb2_module_director__version }}.tar.gz'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
