# Ansible Role postfix

This role installs and configures [postfix](https://www.postfix.org/).

FQCN: linuxfabrik.lfops.postfix

Tested on

* Debian
* Fedora
* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Requirements

This role does not have any requirements.


## Tags

| Tag             | What it does                                   |
| ---             | ------------                                   |
| postfix         | Installs and configures postfix                |
| postfix:state   | Manages the state of the postfix systemd service  |

## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/postfix/defaults/main.yml) for the variable defaults.


### Mandatory

#### postfix__relayhost

Host name of the mail server.

Example:
```yaml
postfix__relayhost: 'mail.example.com:587'
```

#### postfix__relayhost_username

Username with access to the mail server.

Example:
```yaml
postfix__relayhost_username: 'noreply@example.com'
```


### Optional

#### postfix__relayhost_password

Password for the specified user

Default:
```yaml
postfix__relayhost_password: ''
```


#### postfix__smtp_sasl_auth_enable

Enable SASL authentication in the Postfix SMTP client. By default, the Postfix SMTP client uses no authentication. Possible options:

* true
* false

Default:
```yaml
postfix__smtp_sasl_auth_enable: true
```


#### postfix__inet_protocols

The Internet protocols Postfix will attempt to use when making or accepting connections. Specify one or more of `ipv4` or `ipv6`, separated by whitespace or commas. The form `all` is equivalent to `ipv4, ipv6` or `ipv4`, depending on whether the operating system implements IPv6.

Default:
```yaml
postfix__inet_protocols: 'all'
```


#### postfix__service_enabled

Enables or disables the postfix service, analogous to `systemctl enable/disable`. Possible options:

* true
* false

Default:
```yaml
postfix__service_enabled: true
```


#### postfix__service_state

Changes the state of the postfix service, analogous to `systemctl start/stop/restart/reload`. Possible options:

* started
* stopped
* restarted
* reloaded

Default:
```yaml
postfix__service_state: 'started'
```


#### postfix__debconf_selections

Default:
```yaml
postfix__debconf_selections:
 - name: 'postfix'
   question: 'postfix/main_mailer_type'
   value: 'No configuration'
   vtype: 'select'
```

## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
