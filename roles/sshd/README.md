# Ansible Role linuxfabrik.lfops.sshd

This role ensures that sshd is configured.

Note that the role does not make use of `/etc/ssh/sshd_config.d/` since not all options can be overwritten (eg. `Subsystem 'sftp' already defined`).


## Mandatory Requirements

* Install Python 3, and the python3-policycoreutils module (required for the SELinux Ansible tasks). This can be done using the [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils) role.


## Tags

| Tag         | What it does                                  | Reload / Restart |
| ---         | ------------                                  | ---------------- |
| `sshd`       | Configures sshd                               | Reloads sshd.service |
| `sshd:state` | Manages the state of the sshd systemd service | - |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `sshd__address_family` | Specifies which address family should be used. Possible options: `any`, `inet` (use IPv4 only) or `inet6` (use IPv6 only). | `'any'` |
| `sshd__gssapi_authentication` | Specifies whether user authentication based on GSSAPI is allowed | `true` |
| `sshd__log_level` | Sets the log level | `'INFO'` |
| `sshd__password_authentication` | Specifies whether password authentication is allowed. | `false` |
| `sshd__permit_root_login` | Specifies whether root can log in using ssh. Possible options:<br> * `yes`<br> * `prohibit-password`<br> * `forced-commands-only`<br> * `no` | `'yes'` |
| `sshd__port` | Which port the sshd server should use. | `22` |
| `sshd__raw` | Raw (user-defined) SSH-Config. Will be placed at the end of the `/etc/ssh/sshd_config` file. Useful for `Match` directives. | unset |
| `sshd__service_enabled` | Enables or disables the sshd service, analogous to `systemctl enable/disable`. | `true` |
| `sshd__service_state` | Changes the state of the sshd service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |
| `sshd__sftp_subsystem` | Which command should be used for the sftp subsystem. | RHEL: `'/usr/libexec/openssh/sftp-server'`, Debian: `/usr/lib/openssh/sftp-server` |
| `sshd__use_dns` | Specifies whether sshd should look up the remote hostname, and to check that the resolved host name for the remote IP address maps back to the very same IP address. | `false` |

Example:
```yaml
# optional
sshd__address_family: 'inet'
sshd__gssapi_authentication: false
sshd__password_authentication: false
sshd__permit_root_login: 'yes'
sshd__port: 22
sshd__raw: |-
  Match Group sftpusers
    ChrootDirectory /data
    DisableForwarding yes
    ForceCommand internal-sftp
sshd__service_enabled: true
sshd__service_state: 'started'
sshd__use_dns: false
```

## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
