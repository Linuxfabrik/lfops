# Ansible Role linuxfabrik.lfops.acme_sh

This role installs [acme.sh](https://github.com/acmesh-official/acme.sh), and allows to issue certificates using [Let's encrypt](https://letsencrypt.org).

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Install `openssl`. This can be done using the [linuxfabrik.lfops.openssl](https://github.com/Linuxfabrik/lfops/tree/main/roles/openssl) role.
* Install `tar`. This can be done using the [linuxfabrik.lfops.tar](https://github.com/Linuxfabrik/lfops/tree/main/roles/tar) role.
* Have a configured webserver.


## Tags

| Tag                    | What it does                                  |
| ---                    | ------------                                  |
| `acme_sh`              | Installs acme.sh and issues certificates      |
| `acme_sh:certificates` | Issues certificates                           |
| `acme_sh:state`        | Manages the state of the weekly acme.sh timer |


## Mandatory Role Variables

| Variable                 | Description                                                                           |
| --------                 | -----------                                                                           |
| `acme_sh__account_email` | Email address for the Let's encrypt account. This address will receive expiry emails. |

Example:
```yaml
# mandatory
acme_sh__account_email: 'info@example.com'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `acme_sh__certificates` | List of certificates that should be issued. | `[]` |
| `acme_sh__reload_cmd` | Command to execute after issue/renew to reload the server. | `'systemctl reload httpd'` |
| `acme_sh__timer_enabled` | Enables or disables the weekly acme.sh timer, analogous to `systemctl enable/disable --now`. | `true` |


Example:
```yaml
# optional
acme_sh__certificates:
  - 'other.example.com'
  - 'test.example.com'
acme_sh__reload_cmd: 'systemctl reload httpd'
acme_sh__timer_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
