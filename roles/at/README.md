# Ansible Role at

This role installs at, a daemon that allows commands to be run at a specified time.

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

| Tag          | What it does                          |
| ---          | ------------                          |
| at           | Installs and configures at/atd        |
| at:systemctl | Controls the state of the atd service |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/at/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### at__service_enabled

Enables or disables the atd service, analogous to `systemctl enable/disable`. Possible options:

* true
* false

Default:
```yaml
at__service_enabled: true
```


#### at__service_state

Changes the state of the atd service, analogous to `systemctl start/stop/restart/reload`. Possible options:

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
