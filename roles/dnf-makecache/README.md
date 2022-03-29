# Ansible Role DNF-Makecache

This role ensures that the Systemd-Service DNF-Makecache is disabled.

FQCN: linuxfabrik.lfops.dnf-makecache

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

This role does not have any mandatory requirements.


### Optional

This role does not have any optional requirements.


## Tags

| Tag           | What it does                                    |
| ---           | ------------                                    |
| dnf-makecache | Ensures that the Service Makecache is disabled  |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/dnf-makecache/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### dnf_makecache__service_enabled

Enables or disables the dnf-makecache service, analogous to `systemctl enable/disable`. Possible options:

* True
* False

Default:
```yaml
dnf_makecache__service_enabled: False
```

#### dnf_makecache__service_state

Changes the state of the dnf-makecache service, analogous to `systemctl start/stop/restart/reload`. Possible options:

* started
* stopped
* restarted
* reloaded

Default:
```yaml
dnf_makecache__service_state: 'stopped'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
