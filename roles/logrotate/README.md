# Ansible Role logrotate

This role ensures that logrotate is installed and configured.

FQCN: linuxfabrik.lfops.logrotate

Tested on

* Fedora
* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Requirements

### Mandatory

This role does not have any mandatory requirements.


### Optional

This role does not have any optional requirements.


## Tags

| Tag         | What it does                        |
| ---         | ------------                        |
| logrotate   | Install and configure logrotation   |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/logrotate/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### logrotate__rotate_days

After how many days should the log files be rotated.

Default:
```yaml
logrotate__rotate_days: 14
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)

