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
| `sshd__address_family` | String. Specifies which address family should be used. Possible options: `any`, `inet` (use IPv4 only) or `inet6` (use IPv6 only). | `'any'` |
| `sshd__allow_groups__host_var` / `sshd__allow_groups__group_var` | List of dictionaries. If specified, login is allowed only for users whose primary group or supplementary group list matches one of the patterns. Subkeys:<br> * `name`: Mandatory, string. The group name or pattern.<br> * `state`: Optional, string. `present` or `absent`. Defaults to `present`. | `[]` |
| `sshd__allow_users__host_var` / `sshd__allow_users__group_var` | List of dictionaries. If specified, login is allowed only for user names that match one of the patterns. Subkeys:<br> * `name`: Mandatory, string. The user name or pattern.<br> * `state`: Optional, string. `present` or `absent`. Defaults to `present`. | `[]` |
| `sshd__client_alive_count_max` | Number. Sets the number of client alive messages which may be sent without sshd receiving any messages back from the client. | `3` |
| `sshd__client_alive_interval` | Number. Sets a timeout interval in seconds after which if no data has been received from the client, sshd will send a message through the encrypted channel to request a response from the client. | `15` |
| `sshd__deny_groups__host_var` / `sshd__deny_groups__group_var` | List of dictionaries. Login is disallowed for users whose primary group or supplementary group list matches one of the patterns. Subkeys:<br> * `name`: Mandatory, string. The group name or pattern.<br> * `state`: Optional, string. `present` or `absent`. Defaults to `present`. | `[]` |
| `sshd__deny_users__host_var` / `sshd__deny_users__group_var` | List of dictionaries. Login is disallowed for user names that match one of the patterns. Subkeys:<br> * `name`: Mandatory, string. The user name or pattern.<br> * `state`: Optional, string. `present` or `absent`. Defaults to `present`. | `[]` |
| `sshd__disable_forwarding` | Bool. Disables all forwarding features, including X11, ssh-agent, TCP and StreamLocal. | `true` |
| `sshd__gssapi_authentication` | Bool. Specifies whether user authentication based on GSSAPI is allowed. | `true` |
| `sshd__log_level` | Sets the log level | `'INFO'` |
| `sshd__login_grace_time` | Number. The time in seconds after which the server disconnects if the user has not successfully logged in. | `60` |
| `sshd__max_auth_tries` | Number. Specifies the maximum number of authentication attempts permitted per connection. | `4` |
| `sshd__max_sessions` | Number. Specifies the maximum number of open shell, login or subsystem (e.g. sftp) sessions permitted per network connection. | `10` |
| `sshd__max_startups` | String. Specifies the maximum number of concurrent unauthenticated connections to the SSH daemon. Format: `start:rate:full` - randomly refuse connections with probability `rate/100` once there are `start` unauthenticated connections, up to a maximum of `full` at which point all new connections are refused. | `'10:30:60'` |
| `sshd__password_authentication` | Bool. Specifies whether password authentication is allowed. | `false` |
| `sshd__permit_empty_passwords` | Bool. Specifies whether the server allows login to accounts with empty password strings. | `false` |
| `sshd__permit_root_login` | String. Specifies whether root can log in using ssh. Possible options:<br> * `yes`<br> * `prohibit-password`<br> * `forced-commands-only`<br> * `no` | `'yes'` |
| `sshd__permit_user_environment` | Bool. Specifies whether `~/.ssh/environment` and `environment=` options in `~/.ssh/authorized_keys` are processed by sshd. | `false` |
| `sshd__port` | Number. Which port the sshd server should use. | `22` |
| `sshd__raw` | String. Raw (user-defined) SSH-Config. Will be placed at the end of the `/etc/ssh/sshd_config` file. Useful for `Match` directives. | unset |
| `sshd__service_enabled` | Bool. Enables or disables the sshd service, analogous to `systemctl enable/disable`. | `true` |
| `sshd__service_state` | String. Changes the state of the sshd service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |
| `sshd__sftp_subsystem` | String. Which command should be used for the sftp subsystem. | RHEL: `'/usr/libexec/openssh/sftp-server'`, Debian: `/usr/lib/openssh/sftp-server` |
| `sshd__use_dns` | Bool. Specifies whether sshd should look up the remote hostname, and to check that the resolved host name for the remote IP address maps back to the very same IP address. | `false` |

Example:
```yaml
# optional
sshd__address_family: 'inet'
sshd__allow_groups__host_var:
  - name: 'wheel'
  - name: 'sshusers'
sshd__allow_users__host_var:
  - name: 'admin'
  - name: 'deploy'
sshd__client_alive_count_max: 3
sshd__client_alive_interval: 15
sshd__deny_groups__host_var:
  - name: 'nobody'
sshd__deny_users__host_var:
  - name: 'root'
sshd__disable_forwarding: false
sshd__gssapi_authentication: false
sshd__log_level: 'INFO'
sshd__login_grace_time: 60
sshd__max_auth_tries: 4
sshd__max_sessions: 10
sshd__max_startups: '10:30:60'
sshd__password_authentication: false
sshd__permit_empty_passwords: false
sshd__permit_root_login: 'yes'
sshd__permit_user_environment: false
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
