# Ansible Role linuxfabrik.lfops.icingaweb2_module_director

This role installs and configures the [IcingaWeb2 Director Module](https://icinga.com/docs/icinga-director/latest/doc/01-Introduction/), and deploys the baskets from the [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins).

This role is tested with the following IcingaWeb2 Director Module versions:

* 1.10.2
* 1.10.2.2023042001


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.
* A SQL database and user. This can be done using the [linuxfabrik.lfops.mariadb_server](https://github.com/linuxfabrik/lfops/tree/main/roles/mariadb_server) role.


## Tags

`icingaweb2_module_director`

* Installs and configures the IcingaWeb2 Director Module.
* Triggers: none.

`icingaweb2_module_director:basket`

* Only runs if explicitly called. Deploys the baskets from the [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins).
* Triggers: none.

`icingaweb2_module_director:configure`

* Configures the IcingaWeb2 Director Module.
* Triggers: none.


## Mandatory Role Variables

`icingaweb2_module_director__api_user_login`

* The account for accessing the Icinga2 API.
* Type: Dictionary.

`icingaweb2_module_director__database_login`

* The user account for accessing the Director SQL database. Currently, only MySQL is supported.
* Type: Dictionary.

`icingaweb2_module_director__enrolment_user_login`

* A IcingaWeb2 account with the `module/director,director/api,director/hosts` permissions, allowing it to enrol new hosts in the Icinga Director. Note that the username has to be `enrolment-user` for the account to have the correct permissions.
* Type: Dictionary.

`icingaweb2_module_director__monitoring_plugins_version`

* Which version of the monitoring plugins should be deployed? Possible options:

    * A specific release, for example `1.2.0.11`. See the [Releases](https://github.com/Linuxfabrik/monitoring-plugins/releases).
    * `dev`: The development version (main branch). Use with care. Only works with `monitoring_plugins__install_method: 'source'`.

* Type: String.
* Default: `'{{ lfops__monitoring_plugins_version | default() }}'`

`icingaweb2_module_director__version`

* The module version to install. Possible options from either:

    * https://github.com/Icinga/icingaweb2-module-director/releases
    * https://git.linuxfabrik.ch/linuxfabrik/icingaweb2-module-director/-/releases

    Have a look at `icingaweb2_module_director__url`.

* Type: String.

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
icingaweb2_module_director__monitoring_plugins_version: '1.2.0.11'
icingaweb2_module_director__version: 'v1.8.1.2021090901'
```


## Optional Role Variables

`icingaweb2_module_director__api_endpoint`

* The endpoint name for accessing the Icinga2 API.
* Type: String.
* Default: `'{{ icinga2_master__cn }}'`

`icingaweb2_module_director__api_host`

* The host for accessing the Icinga2 API.
* Type: String.
* Default: `'localhost'`

`icingaweb2_module_director__api_port`

* The port for accessing the Icinga2 API.
* Type: Number.
* Default: `5665`

`icingaweb2_module_director__database_host`

* The host of the SQL database server.
* Type: String.
* Default: `'localhost'`

`icingaweb2_module_director__database_name`

* The name of the Director SQL database.
* Type: String.
* Default: `'icinga_director'`

`icingaweb2_module_director__force_kickstart`

* Force run the kickstart. Sometimes the check if it is required is flawed.
* Type: Bool.
* Default: `false`

`icingaweb2_module_director__service_enabled`

* Enables or disables the director service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`icingaweb2_module_director__skip_basket_import`

* Should the Linuxfabrik Monitoring Plugins Basket be generated and imported or not?
* Type: Bool.
* Default: `false`

`icingaweb2_module_director__url`

* The URL from where to download the Director. Defaults to the Linuxfabrik Fork of the Icinga Director. If using the official Icinga Director, the link is `'https://codeload.github.com/Icinga/icingaweb2-module-director/tar.gz/refs/tags/{{ icingaweb2_module_director__version }}'`.
* Type: String.
* Default: `'https://github.com/Linuxfabrik/icingaweb2-module-director/archive/{{ icingaweb2_module_director__version }}.tar.gz'`

Example:

```yaml
# optional
icingaweb2_module_director__api_endpoint: '{{ icinga2_master__cn }}'
icingaweb2_module_director__api_host: 'localhost'
icingaweb2_module_director__api_port: 5665
icingaweb2_module_director__database_host: 'localhost'
icingaweb2_module_director__database_name: 'icinga_director'
icingaweb2_module_director__force_kickstart: true
icingaweb2_module_director__service_enabled: true
icingaweb2_module_director__skip_basket_import: true
icingaweb2_module_director__url: 'https://github.com/Icinga/icingaweb2-module-director/archive/{{ icingaweb2_module_director__version }}.tar.gz'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
