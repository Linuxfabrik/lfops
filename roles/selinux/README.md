# Ansible Role selinux

This role sets the state of SELinux.

FQCN: linuxfabrik.lfops.selinux

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* Install the SELinux python bindings. This can be done using the [linuxfabrik.lfops.libselinux_python](https://github.com/Linuxfabrik/lfops/tree/main/roles/libselinux_python) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag     | What it does           |
| ---     | ------------           |
| selinux | Sets the SELinux state |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/selinux/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### selinux__state

The SELinux state. Possible options:

* disabled
* enforcing
* permissive

Default:
```yaml
selinux__state: 'enforcing'
```

## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
