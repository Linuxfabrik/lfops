# Ansible Role postfix

This role installs and configures [postfix](https://www.postfix.org/).

FQCN: linuxfabrik.lfops.postfix

Tested on

* Debian
* Fedora
* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Requirements

### Mandatory

This role does not have any mandatory requirements.


### Optional

This role does not have any optional requirements.


## Tags

| Tag     | What it does     |
| ---     | ------------     |
| postfix | Installs postfix |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/postfix/defaults/main.yml) for the variable defaults.


### Mandatory

#### postfix__relayhost

Host name of the mail server.

#### postfix__relayhost_username

Username with access to the mail server.


### Optional

#### postfix__relayhost_password:

Password for the specified user


#### postfix__inet_protocols

Default:
```yaml
postfix__inet_protocols: 'all'
```


#### postfix__smtp_sasl_auth_enable

Default:
```yaml
postfix__smtp_sasl_auth_enable: 'yes'
```


#### postfix__service_enabled

Default:
```yaml
postfix__service_enabled: True
```


#### postfix__service_state:

Default:
```yaml
postfix__service_state: 'started'
```


#### postfix__debconf_selections:

Default:
```yaml
postfix__debconf_selections:
 - name: postfix
   question: postfix/main_mailer_type
   value: No configuration
   vtype: select
```

## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
