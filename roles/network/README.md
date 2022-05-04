# Ansible Role Network

This role configures the network settings on the server. It also disables the [zeroconf](http://www.zeroconf.org/).

The role heavily relies on the [linux_system_roles.network Role](https://github.com/linux-system-roles/network).

FQCN: linuxfabrik.lfops.network

Tested on

* RHEL 8 (and compatible)


## Requirements

## Mandatory

* Install the [Linux System Roles](https://linux-system-roles.github.io/) on the Ansible control node. For example by calling `ansible-galaxy collection install fedora.linux_system_roles`.

## Optional

This role does not have optional requirements.


## Tags

| Tag     | What it does                    |
| ---     | ------------                    |
| network | Configures the network settings |



## Role Variables

Have a look at the available role variables from the [linux_system_roles.network Role](https://github.com/linux-system-roles/network/blob/main/README.md).


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
