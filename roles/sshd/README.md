# Ansible Role linuxfabrik.lfops.sshd

This role ensures that sshd is configured. Do not apply this role if you want to configure Crypto Policies via [linuxfabrik.lfops.crypto_policy](https://github.com/Linuxfabrik/lfops/tree/main/roles/crypto_policy) (using Crypto Policies is recommended).


## Mandatory Requirements

* Install Python 3, and the python3-policycoreutils module (required for the SELinux Ansible tasks). This can be done using the [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils) role.


## Tags

| Tag         | What it does                                  |
| ---         | ------------                                  |
| `sshd`       | Configures sshd                               |
| `sshd:state` | Manages the state of the sshd systemd service |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `sshd__password_authentication` | Specifies whether password authentication is allowed. | `false` |
| `sshd__permit_root_login` | Specifies whether root can log in using ssh. Possible options:<br> * `yes`<br> * `prohibit-password`<br> * `forced-commands-only`<br> * `no` | `'yes'` |
| `sshd__port` | Which port the sshd server should use. | `22` |
| `sshd__service_enabled` | Enables or disables the sshd service, analogous to `systemctl enable/disable`. | `true` |
| `sshd__service_state` | Changes the state of the sshd service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |
| `sshd__use_dns` | Specifies whether sshd should look up the remote hostname, and to check that the resolved host name for the remote IP address maps back to the very same IP address. | `false` |

Example:
```yaml
# optional
sshd__password_authentication: false
sshd__permit_root_login: 'yes'
sshd__port: 22
sshd__service_enabled: true
sshd__service_state: 'started'
sshd__use_dns: false
```

## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
