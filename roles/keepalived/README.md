# Ansible Role linuxfabrik.lfops.keepalived

This role installs and configures [keepalived](https://www.keepalived.org/).

Runs on

* RHEL 8 (and compatible)

## Tags

| Tag                 | What it does                                      |
| ---                 | ------------                                      |
| `keepalived`          | Installs and configures keepalived                  |
| `keepalived:state`    | Manages the state of the keepalived service         |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `keepalived__notification_email_addresses` | The email addresses for notifications. |
| `keepalived__password` | The password for the communication between the MASTER and BACKUP instances. |
| `keepalived__state` | Determines whether to be the MASTER or BACKUP. |
| `keepalived__virtual_ipaddress` | The IP address to be shared between the MASTER and BACKUP. |

Example:
```yaml
# mandatory
keepalived__notification_email_addresses:
  - 'root@example.com'
keepalived__password: 'linuxfabrik'
keepalived__state: 'MASTER'
keepalived__virtual_ipaddress: '192.0.2.1'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `keepalived__interface` | The network interface keepalived should use. | `{{ ansible_facts["default_ipv4"]["interface"] }}` |
| `keepalived__notification_email_from` | The email address keepalived should use the sender address for email notifications. | `root@{{ ansible_facts["hostname"] }}` |
| `keepalived__smtp_server` | The SMTP server keepalived should use in order to send email notifications. | `localhost` |

Example:
```yaml
# optional
keepalived__interface: 'eth'
keepalived__notification_email_from: 'root@server.loc'
keepalived__smtp_server: 'smtp.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
