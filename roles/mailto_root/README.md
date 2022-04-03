# Ansible Role mailto_root

This role enables relaying all mail that is sent to the root user (or other service accounts on the system) to an actual mail account. For example, the output of crontab is sent tho the configured address.

FQCN: linuxfabrik.lfops.mailto_root

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* Installed mailx. This can be done using the [linuxfabrik.lfops.mailx](https://github.com/Linuxfabrik/lfops/tree/main/roles/mailx) role.
* Installed and configured postfix. This can be done using the [linuxfabrik.lfops.postfix](https://github.com/Linuxfabrik/lfops/tree/main/roles/postfix) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag                   | What it does                                         |
| ---                   | ------------                                         |
| mailto_root           | Configures mailto_root                               |
| mailto_root:configure | Configures mailto_root without sending any test mail |
| mailto_root:testmail  | Sends 2 test mails to root                           |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/mailto_root/defaults/main.yml) for the variable defaults.


### Mandatory

#### mailto_root__to

List recipient addresses, to which the mails should be relayed.

Example:
```yaml
mailto_root__to:
  - 'root@example.com'
  - 'root@other.example'
```

#### mailto_root_from

The sender address from which the relayed mail should be sent.

Example:
```yaml
mailto_root_from: 'noreply@example.com'
```


### Optional

This role does not have any optional variables.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
