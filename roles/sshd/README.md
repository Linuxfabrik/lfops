# Ansible Role sshd

This role ensures that sshd is configured.

FQCN: linuxfabrik.lfops.sshd

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Requirements

### Mandatory

This role does not have any mandatory requirements.


### Optional

This role does not have any optional requirements.


## Tags

| Tag           | What it does                                   |
| ---           | ------------                                   |
| ssh           | Configures sshd                                |
| ssh:state     | Manages the state of the sshd systemd service  |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/sshd/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### sshd__use_dns

Specifies whether sshd should look up the remote hostname, and to check that the resolved host name for the remote IP address maps back to the very same IP address.

Possible options:

* true
* false

Example:
```yaml
sshd__use_dns: false
```

#### sshd__ciphers

Specifies the ciphers allowed. Multiple ciphers must be comma-separated.

Example:
```yaml
sshd__ciphers: 'chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr'
```

#### sshd__kex

Specifies the available KEX (Key Exchange) algorithms. Multiple algorithms must be comma-separated.

Example:
```yaml
sshd__kex: 'curve25519-sha256@libssh.org'
```

#### sshd__macs

Specifies the available MAC (message authentication code) algorithms. The MAC algorithm is used for data integrity protection. Multiple algorithms must be comma-separated.

Example:
```yaml
sshd__macs: 'hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com'
```

#### sshd__password_authentication

Specifies whether password authentication is allowed.

Possible options:

* true
* false

Example:
```yaml
sshd__password_authentication: false
```


#### sshd__port

Which port the sshd server should use.

Default:
```yaml
sshd__port: 22
```


#### sshd__service_enabled

Enables or disables the sshd service, analogous to `systemctl enable/disable`. Possible options:

* true
* false

Default:
```yaml
sshd__service_enabled: true
```


#### sshd__service_state:

Changes the state of the sshd service, analogous to `systemctl start/stop/restart/reload`. Possible options:

* started
* stopped
* restarted
* reloaded

Default:
```yaml
sshd__service_state: 'started'
```

## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
