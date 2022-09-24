# Ansible Role linuxfabrik.lfops.postfix

This role installs and configures [postfix](https://www.postfix.org/).

Runs on

* Debian
* Fedora 35
* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Ubuntu 16


## Tags

| Tag             | What it does                                     |
| ---             | ------------                                     |
| `postfix`       | Installs and configures postfix                  |
| `postfix:state` | Manages the state of the postfix systemd service |


## Mandatory Role Variables

| Variable                      | Description                              |
| --------                      | -----------                              |
| `postfix__relayhost`          | Host name of the mail server.            |
| `postfix__relayhost_username` | Username with access to the mail server. |

Example:
```yaml
# mandatory
postfix__relayhost: 'mail.example.com:587'
postfix__relayhost_username: 'noreply@example.com'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `postfix__inet_protocols` | The Internet protocols Postfix will attempt to use when making or accepting connections. Specify one or more of `ipv4` or `ipv6`, separated by whitespace or commas. The form `all` is equivalent to `ipv4, ipv6` or `ipv4`, depending on whether the operating system implements IPv6. | `'all'` |
| `postfix__relayhost_password` | Password for the specified user | `''` |
| `postfix__service_enabled` | Enables or disables the postfix service, analogous to `systemctl enable/disable`. | `true` |
| `postfix__service_state` | Changes the state of the postfix service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |
| `postfix__smtp_sasl_auth_enable` | Enable SASL authentication in the Postfix SMTP client. By default, the Postfix SMTP client uses no authentication. | `true` |

Example:
```yaml
# optional
postfix__inet_protocols: 'all'
postfix__relayhost_password: ''
postfix__service_enabled: true
postfix__service_state: 'started'
postfix__smtp_sasl_auth_enable: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
