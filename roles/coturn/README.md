# Ansible Role linuxfabrik.lfops.coturn

This role installs and configures [coturn](https://github.com/coturn/coturn).

Tested on

* RHEL 8 (and compatible)


## Mandatory Requirements

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.


## Tags

| Tag      | What it does                   |
| ---      | ------------                   |
| `coturn` | Installs and configures coturn |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `coturn__denied_peer_ip` | List of IP address ranges which never be used as peer IPs. This should be used to prevent the coturn server from accessing private IPs. Given the turn server is likely behind your firewall, remember to include any privileged public IPs too. |
| `coturn__realm` | The default realm to be used for the users. Hint: Should be the domain of the coturn server for the usage with Nextcloud. |
| `coturn__static_auth_secret` | Static authentication secret value (a string) for TURN REST API only. |


Example:
```yaml
# mandatory
coturn__denied_peer_ip:
  - '192.0.2.0-192.0.255.255'
coturn__realm: 'turn.example.com'
coturn__static_auth_secret: 'egi7eesa9eik4kae9ov9quohpheequ9XighaivobuThoo7ooKuo3aikooNuy9edei4fu3jaikeepai4j'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `coturn__allowed_peer_ip` | List of IP address ranges which are excepted from `coturn__denied_peer_ip`. | `['{{ ansible_facts["default_ipv4"]["address"] }}']` |
| `coturn__listening_port` | TURN listener port for UDP and TCP listeners | `3478` |
| `coturn__max_port` | Upper bound of the UDP port range for relay endpoints allocation. | `65535` |
| `coturn__min_port` | Lower bound of the UDP port range for relay endpoints allocation. | `49152` |
| `coturn__service_enabled` | Enables or disables the coturn service, analogous to `systemctl enable/disable --now`. Possible options: | `true` |
| `coturn__state_nonce` | Use extra security with nonce value having limited lifetime, in seconds. Set it to 0 for unlimited nonce lifetime. | `0` |

Example:
```yaml
# optional
coturn__allowed_peer_ip:
  - '{{ ansible_facts["default_ipv4"]["address"] }}'
coturn__listening_port: 3478
coturn__max_port: 65535
coturn__min_port: 49152
coturn__service_enabled: true
coturn__state_nonce: 0
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
