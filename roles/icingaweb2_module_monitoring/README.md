# Ansible Role icingaweb2_module_monitoring

This role installs and configures the [IcingaWeb2 Monitoring Module](https://icinga.com/docs/icinga-web-2/latest/modules/monitoring/doc/01-About/).

FQCN: linuxfabrik.lfops.icingaweb2_module_monitoring

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag                          | What it does                                             |
| ---                          | ------------                                             |
| icingaweb2_module_monitoring | Installs and configures the IcingaWeb2 Monitoring Module |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/icingaweb2_module_monitoring/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### icingaweb2_module_monitoring__api_host

The host for accessing the Icinga2 API.

Default:
```yaml
icingaweb2_module_monitoring__api_host: 'localhost'
```


#### icingaweb2_module_monitoring__api_port

The port for accessing the Icinga2 API.

Default:
```yaml
icingaweb2_module_monitoring__api_port: 5665
```


#### icingaweb2_module_monitoring__api_user_login

The account for accessing the Icinga2 API. Defaults to the `icingaweb2__api_user_login`.

Default:
```yaml
icingaweb2_module_monitoring__api_user_login: '{{ icingaweb2__api_user_login }}'
```

Example:
```yaml
icingaweb2_module_monitoring__api_user_login:
  username: 'icingaweb2-api-user'
  password: 'my-secret-password'
```


#### icingaweb2_module_monitoring__backend_database_name

The name of the Icinga2 ido database.

Default:
```yaml
icingaweb2_module_monitoring__backend_database_name: '{{ icinga2_master__database_name }}'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
