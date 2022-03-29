# Ansible Role Timezone

This role sets the desired timezone.

FQCN: linuxfabrik.lfops.timezone

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Fedora


## Requirements

### Mandatory

This role does not have any mandatory requirements.

### Optional

This role does not have any optional requirements.


## Tags

| Tag          | What it does                         |
| ---          | ------------                         |
| timezone     | Set timezone to timezone__timezone   |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/timezone/defaults/main.yml) for the variable defaults.

### Mandatory

This role does not have any mandatory variables.

### Optional

#### timezone__timezone

Set timezone. Have a look at the [Wikipedia List](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) for the options.

Default:
```yaml
timezone__timezone: 'Europe/Zurich'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
