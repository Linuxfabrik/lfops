# Ansible Role acme_sh

This role installs [acme.sh](https://github.com/acmesh-official/acme.sh), and allows to issue certificates using [Let's encrypt](https://letsencrypt.org).

FQCN: linuxfabrik.lfops.acme_sh

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* Install `openssl`. This can be done using the [linuxfabrik.lfops.openssl](https://github.com/Linuxfabrik/lfops/tree/main/roles/openssl) role.
* Install `tar`. This can be done using the [linuxfabrik.lfops.tar](https://github.com/Linuxfabrik/lfops/tree/main/roles/tar) role.
* Have a configured webserver.


### Optional

This role does not have any optional requirements.


## Tags

| Tag                  | What it does                                  |
| ---                  | ------------                                  |
| acme_sh              | Installs acme.sh and issues certificates      |
| acme_sh:certificates | Issues certificates                           |
| acme_sh:state        | Manages the state of the weekly acme.sh timer |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/acme_sh/defaults/main.yml) for the variable defaults.


### Mandatory

#### acme_sh__account_email

Email address for the Let's encrypt account. This address will receive expiry emails.

Default:
```yaml
acme_sh__account_email: 'info@example.com'
```


### Optional

#### acme_sh__certificates

List of certificates that should be issued.

Default:
```yaml
acme_sh__certificates: []
```

Example:
```yaml
acme_sh__certificates:
  - 'test.example.com'
  - 'other.example.com'
```


#### acme_sh__reload_cmd

Command to execute after issue/renew to reload the server.

Default:
```yaml
acme_sh__reload_cmd: 'systemctl reload httpd'
```


#### acme_sh__timer_enabled

Enables or disables the weekly acme.sh timer, analogous to `systemctl enable/disable --now`. Possible options:

* true
* false

Default:
```yaml
acme_sh__timer_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
