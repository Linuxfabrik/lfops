# Ansible Role at

TODO

FQCN: linuxfabrik.lfops.at

Tested on

* RHEL 8 (and compatible)
* Fedora Server 35

## Requirements

### Mandatory

This role does not have any mandatory requirements.

### Optional

This role does not have any optional requirements.


## Tags

| Tag          | What it does                                 |
| ---          | ------------                                 |
| at           | Installs and configures at/atd               |
| at:systemctl | Start or disable atd                         |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/at/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### at__service_enabled 

Sets if the atd service is started on boot. Possible options:

* True
* False

Default:
```yaml
at__service_enabled: True
```


#### at__service_state

Sets the state of the atd service. Possible options:

* started
* stopped
* restarted
* reloaded

Default:
```yaml
at__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
