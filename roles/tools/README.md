# Ansible Role tools

This role ensures that tools is installed and configured.

FQCN: linuxfabrik.lfops.tools

Tested on

* Fedora
* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Requirements

### Mandatory

linuxfabrik.lfops.repo_epel


### Optional

This role does not have any optional requirements.


## Tags

| Tag       | What it does                         |
| ---       | ------------                         |
| tools     | Installs and configures some tools   |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/tools/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### tools__editor

Standard editor like for example for crontab.

Default:
```yaml
tools__editor: 'nano'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
