# Ansible Role icingaweb2_module_director

This role installs and configures the [IcingaWeb2 Director Module](https://icinga.com/docs/icinga-director/latest/doc/01-Introduction/).

FQCN: linuxfabrik.lfops.icingaweb2_module_director

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.
* A SQL database and user. This can be done using the [linuxfabrik.lfops.mariadb_server](https://github.com/linuxfabrik/lfops/tree/main/roles/mariadb_server) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag                               | What it does                                                                                                                                                                |
| ---                               | ------------                                                                                                                                                                |
| icingaweb2_module_director        | Installs and configures the IcingaWeb2 Director Module                                                                                                                      |
| icingaweb2_module_director:basket | Deploys the baskets from the [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins). This does not run by default, only when explicitly called |


## Role Variables

This role does not have any variables.

### Mandatory

#### icingaweb2_module_director__version

The module version to install. Possible options from either:

* https://github.com/Icinga/icingaweb2-module-incubator/releases
* https://git.linuxfabrik.ch/linuxfabrik/icingaweb2-module-director/-/releases

Have a look at `icingaweb2_module_director__url`.

Example:
```yaml
icingaweb2_module_director__version: 'v1.8.1.2021090901'
```


#### icingaweb2_module_director__api_user_login

The account for accessing the Icinga2 API.

Example:
```yaml
icingaweb2_module_director__api_user_login:
  username: 'icinga-director-api'
  password: 'my-secret-password'
```


#### icingaweb2_module_director__database_login

The user account for accessing the Director SQL database. Currently, only MySQL is supported.

Default:
```yaml
icingaweb2_module_director__database_login:
  username: 'icinga_director_user'
  password: 'my-secret-password'
```


### Optional

#### icingaweb2_module_director__api_endpoint

The endpoint name for accessing the Icinga2 API.

Default:
```yaml
icingaweb2_module_director__api_endpoint: '{{ icinga2_master__cn }}'
```


#### icingaweb2_module_director__api_host

The host for accessing the Icinga2 API.

Default:
```yaml
icingaweb2_module_director__api_host: 'localhost'
```


#### icingaweb2_module_director__api_port

The port for accessing the Icinga2 API.

Default:
```yaml
icingaweb2_module_director__api_port: 5665
```


#### icingaweb2_module_director__database_host

The host of the SQL database server.

Default:
```yaml
icingaweb2_module_director__database_host: 'localhost'
```


#### icingaweb2_module_director__database_name

The name of the Director SQL database.

Default:
```yaml
icingaweb2_module_director__database_name: 'icinga_director'
```


#### icingaweb2_module_director__url

The URL from where to download the Director. Defaults to the Linuxfabrik Fork of the Icinga Director.

Default:
```yaml
icingaweb2_module_director__url: 'https://git.linuxfabrik.ch/api/v4/projects/133/repository/archive?sha={{ icingaweb2_module_director__version }}'
```


#### icingaweb2_module_director__monitoring_plugins_version

Which version of the monitoring plugins should be used for generating the Director baskets? Possible options:

* `latest`: The **latest stable** release. See the [Releases](https://github.com/Linuxfabrik/monitoring-plugins/releases).
* `main`: The development version. Use with care.
* A specific release, for example `2022030201`. See the [Releases](https://github.com/Linuxfabrik/monitoring-plugins/releases).

Default:
```yaml
icingaweb2_module_director__monitoring_plugins_version: 'latest'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
