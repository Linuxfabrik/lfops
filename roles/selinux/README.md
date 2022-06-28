# Ansible Role selinux

This role sets the state of SELinux and optionally toggles SELinux booleans.

FQCN: linuxfabrik.lfops.selinux

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* Install the SELinux python bindings. This can be done using the [linuxfabrik.lfops.libselinux_python](https://github.com/Linuxfabrik/lfops/tree/main/roles/libselinux_python) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag              | What it does                                                   |
| ---              | ------------                                                   |
| selinux          | Sets the SELinux state and optionally toggles SELinux booleans |
| selinux:state    | Sets the SELinux state                                         |
| selinux:booleans | Toggles SELinux booleans                                       |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/selinux/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### selinux__host_booleans / selinux__group_booleans

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

A list of dictionaries containing SELinux booleans.

Subkeys:

* `key`: Mandatory, string. Key of the SELinux boolean.
* `value`: Mandatory, string. Value of the SELinux boolean.

Default:
```yaml
selinux__host_booleans: []
selinux__group_booleans: []
```

Example:
```yaml
selinux__host_booleans:
  - key: 'httpd_can_network_connect'
    value: 1
```

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
