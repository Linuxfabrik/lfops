# Ansible Role kdump

This role stops and disables the `kdump` service. Since most of the time, kdump is not required, but permanently reserves space in the memory for the capture kernel, we usually disable it.

FQCN: linuxfabrik.lfops.kdump

Tested on

* RHEL 8 (and compatible)


## Requirements

This role does not have any requirements.


## Tags

| Tag   | What it does                           |
| ---   | ------------                           |
| kdump | Stops and disables the `kdump` service |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/kdump/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### kdump__service_enabled

Enables or disables the kdump service, analogous to `systemctl enable/disable`. Possible options:

* true
* false

Default:
```yaml
kdump__service_enabled: false
```


#### kdump__service_state

Changes the state of the kdump service, analogous to `systemctl start/stop/restart/reload`. Possible options:

* started
* stopped
* restarted
* reloaded

Default:
```yaml
kdump__service_state: 'stopped'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
