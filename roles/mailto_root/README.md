# Ansible Role mailto_root

This role configures mail to root.

FQCN: linuxfabrik.lfops.mailto_root

Tested on

* Debian
* Fedora Server 35
* RHEL 7 (and compatible)
* RHEL 8 (and compatible)

## Requirements

### Mandatory

mailx
postfix


### Optional

This role does not have any optional requirements.


## Tags

| Tag                    | What it does                             |
| ---                    | ------------                             |
| mailto_root            | Configures mailto_root                   |
| mailto_root:configure  | Configures mailto_root without testmail  |
| mailto_root:testmail   | Sends a test mail to root                |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/mailto_root/defaults/main.yml) for the variable defaults.


### Mandatory

#### mailto_root__to

mailto_root_to: 'root@linuxfabrik.ch'
# mailto_root_to: 'root@linuxfabrik.ch, root@otherdomain.ch'
mailto_root_from: 'noreply@linuxfabrik.ch'


### Optional

This role does not have any mandatory variables.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
