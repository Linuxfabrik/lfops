# Ansible Role coturn

This role installs and configures [coturn](https://github.com/coturn/coturn).

FQCN: linuxfabrik.lfops.coturn

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag    | What it does                   |
| ---    | ------------                   |
| coturn | Installs and configures coturn |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/coturn/defaults/main.yml) for the variable defaults.


### Mandatory

#### coturn__denied_peer_ip

List of IP address ranges which never be used as peer IPs. This should be used to prevent the coturn server from accessing private IPs. Given the turn server is likely behind your firewall, remember to include any privileged public IPs too.

Default: unset

Example:
```yaml
coturn_denied_peer_ip:
  - '10.117.17.0-10.255.255.255'
```


#### coturn__realm

The default realm to be used for the users.
Hint: Should be the domain of the coturn server for the usage with Nextcloud.

Example:
```yaml
coturn__realm: 'turn.example.com'
```



#### coturn__static_auth_secret

Static authentication secret value (a string) for TURN REST API only.

Example:
```yaml
coturn__static_auth_secret: 'egi7eesa9eik4kae9ov9quohpheequ9XighaivobuThoo7ooKuo3aikooNuy9edei4fu3jaikeepai4j'
```


### Optional

#### coturn__allowed_peer_ip

List of IP address ranges which are excepted from `coturn__denied_peer_ip`.

Default:
```yaml
coturn__allowed_peer_ip:
  - '{{ ansible_facts["default_ipv4"]["address"] }}'
```


#### coturn__listening_port

TURN listener port for UDP and TCP listeners

Default:
```yaml
coturn__listening_port: 3478
```


#### coturn__max_port

Upper bound of the UDP port range for relay endpoints allocation.

Default:
```yaml
coturn__max_port: 65535
```


#### coturn__min_port

Lower bound of the UDP port range for relay endpoints allocation.

Default:
```yaml
coturn__min_port: 49152
```


#### coturn__service_enabled

Enables or disables the coturn service, analogous to `systemctl enable/disable --now`. Possible options:

* true
* false

Default:
```yaml
coturn__service_enabled: true
```


#### coturn__state_nonce

Use extra security with nonce value having limited lifetime, in seconds. Set it to 0 for unlimited nonce lifetime.

Default:
```yaml
coturn__state_nonce: 0
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
