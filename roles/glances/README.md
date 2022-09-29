# Ansible Role linuxfabrik.lfops.glances

This role installs [glances](https://nicolargo.github.io/glances/). It also aliases `top` to `glances -t 1`.

Runs on

* RHEL 8 (and compatible)
* Ubuntu 16


## Mandatory Requirements

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.


## Tags

| Tag       | What it does                              |
| ---       | ------------                              |
| `glances` | Installs glances and configures the alias |


# License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
