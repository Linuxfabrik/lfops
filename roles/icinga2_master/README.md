# Ansible Role icinga2_master

This role installs and configures [Icinga2](https://icinga.com/docs/icinga-2/latest/doc/01-about/) as a monitoring master.

FQCN: linuxfabrik.lfops.icinga2_master

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* TODO, have a look at old readme + current playbook
* Install `tar`. This can be done using the [linuxfabrik.lfops.tar](https://github.com/Linuxfabrik/lfops/tree/main/roles/tar) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag                      | What it does                                |
| ---                      | ------------                                |
| icinga2_master           | Installs and configures Icinga2 as a master |
| icinga2_master:state     | Manages the state of the Icinga2 service    |
| icinga2_master:api_users | Manages the Icinga2 API users               |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/icinga2_master/defaults/main.yml) for the variable defaults.


### Mandatory

#### icinga2_master__api_login

todo, this should be optional, only required to register the secondary - we need a list of api users for the primary

Example:
```yaml
icinga2_master__api_login:
```


#### icinga2_master__database_login

The user account for accessing the icinga2 ido database. Currently, only MySQL is supported.

Example:
```yaml
icinga2_master__database_login:
  username: ''
  password: ''
```


#### icinga2_master__influxdb_login

The user account for accessing the icinga2 InfluxDB database.

Example:
```yaml
icinga2_master__influxdb_login:
  username: ''
  password: ''
```


### Optional

#### icinga2_master__additional_api_users_raw

todo

Default:
```yaml
icinga2_master__additional_api_users_raw: unset
```


#### icinga2_master__additional_master_endpoints

todo

Default:
```yaml
icinga2_master__additional_master_endpoints: []
```


#### icinga2_master__cn

todo

Default:
```yaml
icinga2_master__cn: '{{ ansible_facts["nodename"] }}'
```


#### icinga2_master__database_enable_ha

todo

Default:
```yaml
icinga2_master__database_enable_ha: false
```


#### icinga2_master__database_host

todo

Default:
```yaml
icinga2_master__database_host: 'localhost'
```


#### icinga2_master__database_name

todo

Default:
```yaml
icinga2_master__database_name: 'icinga2_ido'
```


#### icinga2_master__influxdb_database

todo

Default:
```yaml
icinga2_master__influxdb_database: 'icinga2'
```


#### icinga2_master__influxdb_enable_ha

todo

Default:
```yaml
icinga2_master__influxdb_enable_ha: false
```


#### icinga2_master__influxdb_host

todo

Default:
```yaml
icinga2_master__influxdb_host: 'localhost'
```


#### icinga2_master__influxdb_retention

todo

Default:
```yaml
icinga2_master__influxdb_retention: '216d'
```


#### icinga2_master__primary_host

todo

Default:
```yaml
icinga2_master__primary_host: unset
```


#### icinga2_master__primary_port

todo

Default:
```yaml
icinga2_master__primary_port: unset
```


#### icinga2_master__service_enabled

todo

Default:
```yaml
icinga2_master__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
