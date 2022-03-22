# Ansible Role at

This role creates and manages various [Python 3 virtual environments (venv)](https://docs.python.org/3/library/venv.html). These are placed below `/opt/python-venv/` on the target system.

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
| at-systemctl | start or disable atd                         |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/at/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### at__service_enabled / at__service_state

These 2 Variables change the enablement and state of the atd service

Default:
```
at__service_enabled: True
at__service_state: 'started'
```

Example:
```
at__service_enabled: False
at__service_state: 'stopped'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)

