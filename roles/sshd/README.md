# Ansible Role linuxfabrik.lfops.sshd

This role ensures that sshd is configured. Do not apply this role if you want to configure Crypto Policies via [linuxfabrik.lfops.crypto_policy](https://github.com/Linuxfabrik/lfops/tree/main/roles/crypto_policy) (using Crypto Policies is recommended).

Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Mandatory Requirements

* Install Python 3, and the python3-policycoreutils module (required for the SELinux Ansible tasks). This can be done using the [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils) role.


## Tags

| Tag         | What it does                                  |
| ---         | ------------                                  |
| `ssh`       | Configures sshd                               |
| `ssh:state` | Manages the state of the sshd systemd service |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `sshd__ciphers` | Specifies the ciphers allowed. Multiple ciphers must be comma-separated. | `'chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr'` |
| `sshd__kex` | Specifies the available KEX (Key Exchange) algorithms. Multiple algorithms must be comma-separated. | `'curve25519-sha256@libssh.org'` |
| `sshd__macs` | Specifies the available MAC (message authentication code) algorithms. The MAC algorithm is used for data integrity protection. Multiple algorithms must be comma-separated. | `'hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com'` |
| `sshd__password_authentication` | Specifies whether password authentication is allowed. | `false` |
| `sshd__permit_root_login` | Specifies whether root can log in using ssh. Possible options:<br> * `yes`<br> * `prohibit-password`<br> * `forced-commands-only`<br> * `no` | `'yes'` |
| `sshd__port` | Which port the sshd server should use. | `22` |
| `sshd__service_enabled` | Enables or disables the sshd service, analogous to `systemctl enable/disable`. | `true` |
| `sshd__service_state` | Changes the state of the sshd service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |
| `sshd__use_dns` | Specifies whether sshd should look up the remote hostname, and to check that the resolved host name for the remote IP address maps back to the very same IP address. | `false` |

Example:
```yaml
# optional
sshd__ciphers: 'chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr'
sshd__kex: 'curve25519-sha256@libssh.org'
sshd__macs: 'hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com'
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
