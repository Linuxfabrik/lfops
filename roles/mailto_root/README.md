# Ansible Role linuxfabrik.lfops.mailto_root

This role enables relaying all mail that is sent to the root user (or other service accounts on the system) to an actual mail account. For example, any output of crontab is sent tho the configured address if this role is applied to the system.

Runs on

* RHEL 8 (and compatible)
* RHEL 9 (and compatible)
* Ubuntu 16


## Mandatory Requirements

* Install and configure postfix. This can be done using the [linuxfabrik.lfops.postfix](https://github.com/Linuxfabrik/lfops/tree/main/roles/postfix) role.
* Install mailx. This can be done using the [linuxfabrik.lfops.mailx](https://github.com/Linuxfabrik/lfops/tree/main/roles/mailx) role.


## Tags

| Tag                     | What it does                                         |
| ---                     | ------------                                         |
| `mailto_root`           | Configures mailto_root                               |
| `mailto_root:configure` | Configures mailto_root without sending any test mail |
| `mailto_root:testmail`  | Sends 2 test mails to root                           |


## Mandatory Role Variables

| Variable            | Description                                                     |
| --------            | -----------                                                     |
| `mailto_root__from` | The sender address from which the relayed mail should be sent.  |
| `mailto_root__to`   | List recipient addresses to which the mails should be relayed.  |

Example:
```yaml
# mandatory
mailto_root__from: 'noreply@example.com'
mailto_root__to:
  - 'root@example.com'
  - 'root@other.example'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
