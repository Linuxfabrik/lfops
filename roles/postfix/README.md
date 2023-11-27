# Ansible Role linuxfabrik.lfops.postfix

This role installs and configures [postfix](https://www.postfix.org/).

Runs on

* Debian
* Fedora 35
* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* RHEL 9 (and compatible)
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

Example:
```yaml
# mandatory
postfix__relayhost: 'mail.example.com:587'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `postfix__inet_interfaces` | The local network interface addresses that this mail system receives mail on. | `'127.0.0.1'` |
| `postfix__inet_protocols` | The Internet protocols Postfix will attempt to use when making or accepting connections. Specify one or more of `ipv4` or `ipv6`, separated by whitespace or commas. The form `all` is equivalent to `ipv4, ipv6` or `ipv4`, depending on whether the operating system implements IPv6. | `'all'` |
| `postfix__relayhost_password` | Password for the specified user | `''` |
| `postfix__relayhost_username` | Username with access to the mail server. | `'{{ mailto_root__from }}'` |
| `postfix__service_enabled` | Enables or disables the postfix service, analogous to `systemctl enable/disable`. | `true` |
| `postfix__service_state` | Changes the state of the postfix service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |
| `postfix__smtp_sasl_auth_enable` | Enable SASL authentication in the Postfix SMTP client. By default, the Postfix SMTP client uses no authentication. | `true` |
| `postfix__smtp_sasl_security_options` | Postfix SMTP client SASL security options, separated by commas. Possible options:<br>* `noplaintext`<br>* `noactive`<br>* `nodictionary`<br>* `noanonymous`<br>* `mutual_auth` | `'noplaintext, noanonymous'` |
| `postfix__smtp_tls_security_level`| SMTPS wrappermode (TCP port 465) requires setting "smtp_tls_wrappermode = yes", and "smtp_tls_security_level = encrypt" (or stronger). The default SMTP TLS security level for the Postfix SMTP client. When a non-empty value is specified, this overrides the obsolete parameters smtp_use_tls, smtp_enforce_tls, and smtp_tls_enforce_peername; when no value is specified for smtp_tls_enforce_peername or the obsolete parameters, the default SMTP TLS security level is none. | unset |
| `postfix__smtp_tls_wrappermode` | SMTPS wrappermode (TCP port 465) requires setting "smtp_tls_wrappermode = yes", and "smtp_tls_security_level = encrypt" (or stronger). Request that the Postfix SMTP client connects using the SUBMISSIONS/SMTPS protocol instead of using the STARTTLS command. | `false` |

Example:
```yaml
# optional
postfix__inet_interfaces: 'all'
postfix__inet_protocols: 'all'
postfix__relayhost_password: ''
postfix__relayhost_username: ''
postfix__service_enabled: true
postfix__service_state: 'started'
postfix__smtp_sasl_auth_enable: true
postfix__smtp_sasl_security_options:
  - 'noanonymous'
  - 'noplaintext'
postfix__smtp_tls_security_level: 'encrypt'
postfix__smtp_tls_wrappermode: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
