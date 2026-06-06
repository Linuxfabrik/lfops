# Ansible Role linuxfabrik.lfops.sshd

This role deploys `/etc/ssh/sshd_config` for [OpenSSH](https://www.openssh.com/) (the standard SSH server on Linux). It exposes the most commonly tuned options as variables (port, address family, password / GSSAPI / root login, log level, forwarding, session limits, sftp subsystem) plus a `sshd__raw` escape hatch for `Match` blocks etc.

Note that the role does not make use of `/etc/ssh/sshd_config.d/` since not all options can be overwritten there (e.g. `Subsystem 'sftp' already defined`); the full `sshd_config` is templated instead.

The option descriptions below are condensed from `sshd_config(5)`.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

The role ships hardened defaults for several options that differ from the OpenSSH (or distribution) defaults: `X11Forwarding`, agent forwarding and TCP keepalives are off, `MaxAuthTries` and `ClientAliveCountMax` are stricter, and `LogLevel` is `VERBOSE` (which logs the key fingerprint used for each login). Each is overridable via the variables below.

`MaxAuthTries` defaults to `3`. Every public key an SSH agent offers counts as one attempt, so a client with more than three keys loaded in its agent may be rejected before the matching key is tried. In that case use `IdentitiesOnly yes` / an explicit `IdentityFile` on the client, or raise `sshd__max_auth_tries`.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* Python 3 and the python3-policycoreutils module must be installed (required for the SELinux Ansible tasks) (role: [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils)).


## Tags

`sshd`

* Configures sshd.
* Triggers: `sshd: sshd -t; reload sshd`.

`sshd:state`

* Manages the state of the sshd systemd service.
* Triggers: none.


## Optional Role Variables

`sshd__address_family`

* Specifies which address family should be used. Possible options: `any`, `inet` (use IPv4 only) or `inet6` (use IPv6 only).
* Type: String.
* Default: `'any'`

`sshd__allow_agent_forwarding`

* Specifies whether `ssh-agent(1)` forwarding is permitted. OpenSSH defaults to `true`; this role disables it. For the finer-grained variants use `sshd__raw`.
* Type: Bool.
* Default: `false`

`sshd__allow_tcp_forwarding`

* Specifies whether TCP forwarding is permitted. Rendered as `yes`/`no`; for the `local` / `remote` / `all` variants use `sshd__raw`.
* Type: Bool.
* Default: `true`

`sshd__client_alive_count_max`

* Number of client alive messages sshd may send without receiving any back from the client before it disconnects the session. Unlike `TCPKeepAlive`, these messages go through the encrypted channel and cannot be spoofed. Only takes effect together with a non-zero `ClientAliveInterval` (`0` by default, set it via `sshd__raw`).
* Type: Number.
* Default: `2` (OpenSSH default: `3`)

`sshd__gssapi_authentication`

* Specifies whether user authentication based on GSSAPI is allowed.
* Type: Bool.
* Default: `true`

`sshd__log_level`

* Verbosity level used when logging messages from sshd. Possible values: `QUIET`, `FATAL`, `ERROR`, `INFO`, `VERBOSE`, `DEBUG`, `DEBUG1`, `DEBUG2`, `DEBUG3`. `VERBOSE` additionally logs the key fingerprint used for each login. `DEBUG*` levels violate user privacy and are not recommended.
* Type: String.
* Default: `'VERBOSE'` (OpenSSH default: `INFO`)

`sshd__max_auth_tries`

* Maximum number of authentication attempts permitted per connection. Once the number of failures reaches half this value, additional failures are logged. Note that each key an SSH agent offers counts as one attempt (see "How the Role Behaves").
* Type: Number.
* Default: `3` (OpenSSH default: `6`)

`sshd__max_sessions`

* Maximum number of open shell, login or subsystem (e.g. sftp) sessions permitted per network connection. `1` disables session multiplexing; `0` prevents shell, login and subsystem sessions while still permitting forwarding.
* Type: Number.
* Default: `10`

`sshd__password_authentication`

* Specifies whether password authentication is allowed.
* Type: Bool.
* Default: `false`

`sshd__permit_root_login`

* Specifies whether root can log in using ssh. Possible options: `yes`, `prohibit-password`, `forced-commands-only`, `no`.
* Type: String.
* Default: `'yes'`

`sshd__port`

* Which port the sshd server should use.
* Type: Number.
* Default: `22`

`sshd__raw`

* Raw (user-defined) SSH-Config. Will be placed at the end of the `/etc/ssh/sshd_config` file. Useful for `Match` directives.
* Type: String.
* Default: unset

`sshd__service_enabled`

* Enables or disables the sshd service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`sshd__service_state`

* Changes the state of the sshd service, analogous to `systemctl start/stop/restart/reload`. Possible options: `started`, `stopped`, `restarted`, `reloaded`.
* Type: String.
* Default: `'started'`

`sshd__sftp_subsystem`

* Which command should be used for the sftp subsystem.
* Type: String.
* Default: RHEL: `'/usr/libexec/openssh/sftp-server'`, Debian: `'/usr/lib/openssh/sftp-server'`

`sshd__tcp_keep_alive`

* Specifies whether the system sends TCP keepalive messages to the other side. The TCP keepalive is spoofable; `sshd__client_alive_count_max` (through the encrypted channel) is the non-spoofable alternative. Disabling it avoids dropping sessions on temporary route outages.
* Type: Bool.
* Default: `false` (OpenSSH default: `yes`)

`sshd__use_dns`

* Specifies whether sshd should look up the remote hostname, and to check that the resolved host name for the remote IP address maps back to the very same IP address.
* Type: Bool.
* Default: `false`

`sshd__x11_forwarding`

* Specifies whether X11 forwarding is permitted. OpenSSH defaults to `no`, but the stock RHEL and Debian `sshd_config` enable it; this role disables it again.
* Type: Bool.
* Default: `false`

Example:

```yaml
# optional
sshd__address_family: 'inet'
sshd__allow_agent_forwarding: false
sshd__allow_tcp_forwarding: true
sshd__client_alive_count_max: 2
sshd__gssapi_authentication: false
sshd__log_level: 'VERBOSE'
sshd__max_auth_tries: 3
sshd__max_sessions: 10
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
sshd__tcp_keep_alive: false
sshd__use_dns: false
sshd__x11_forwarding: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
