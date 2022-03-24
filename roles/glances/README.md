# Ansible Role glances

This role installs [glances](https://nicolargo.github.io/glances/). It also aliases `top` to `glances -t 1`.

FQCN: linuxfabrik.lfops.glances

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag     | What it does                              |
| ---     | ------------                              |
| glances | Installs glances and configures the alias |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/glances/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

This role does not have any optional variables.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
