# Ansible Role logrotate

This role ensures that logrotate is installed and configured.

FQCN: linuxfabrik.lfops.logrotate

Tested on

* Fedora
* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Requirements

This role does not have any requirements.


## Tags

| Tag       | What it does                         |
| ---       | ------------                         |
| logrotate | Installs and configures log rotation |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/logrotate/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### logrotate__rotate_days

For how many days the rotated files should be kept.

Default:
```yaml
logrotate__rotate_days: 14
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
