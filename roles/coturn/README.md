# Ansible Role linuxfabrik.lfops.coturn

This role installs and configures [coturn](https://github.com/coturn/coturn).


*Available since LFOps `2.0.0`.*


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* On RHEL-compatible systems, the EPEL repository must be enabled (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)).


## Tags

`coturn`

* Installs and configures coturn.
* Triggers: coturn.service restart.

`coturn:sate`

* Manages the state of the coturn systemd service.
* Triggers: none.


## Mandatory Role Variables

`coturn__denied_peer_ip`

* List of IP address ranges which never be used as peer IPs. This should be used to prevent the coturn server from accessing private IPs. Given the turn server is likely behind your firewall, remember to include any privileged public IPs too.
* Type: List of strings.

`coturn__realm`

* The default realm to be used for the users. Hint: Should be the domain of the coturn server for the usage with Nextcloud.
* Type: String.

`coturn__static_auth_secret`

* Static authentication secret value (a string) for TURN REST API only.
* Type: String.

Example:
```yaml
# mandatory
coturn__denied_peer_ip:
  - '192.0.2.0-192.0.255.255'
coturn__realm: 'turn.example.com'
coturn__static_auth_secret: 'egi7eesa9eik4kae9ov9quohpheequ9XighaivobuThoo7ooKuo3aikooNuy9edei4fu3jaikeepai4j'
```


## Optional Role Variables

`coturn__allowed_peer_ip`

* List of IP address ranges which are excepted from `coturn__denied_peer_ip`.
* Type: List of strings.
* Default: `['{{ ansible_facts["default_ipv4"]["address"] }}']`

`coturn__listening_port`

* TURN listener port for UDP and TCP listeners.
* Type: Number.
* Default: `3478`

`coturn__max_port`

* Upper bound of the UDP port range for relay endpoints allocation.
* Type: Number.
* Default: `65535`

`coturn__min_port`

* Lower bound of the UDP port range for relay endpoints allocation.
* Type: Number.
* Default: `49152`

`coturn__service_enabled`

* Enables or disables the coturn service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`coturn__service_state`

* Changes the state of the coturn service, analogous to `systemctl start/stop/restart/reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `coturn__service_enabled` is `true`, else `'stopped'`

`coturn__state_nonce`

* Use extra security with nonce value having limited lifetime, in seconds. Set it to 0 for unlimited nonce lifetime.
* Type: Number.
* Default: `0`

Example:
```yaml
# optional
coturn__allowed_peer_ip:
  - '{{ ansible_facts["default_ipv4"]["address"] }}'
coturn__listening_port: 3478
coturn__max_port: 65535
coturn__min_port: 49152
coturn__service_enabled: true
coturn__service_state: 'started'
coturn__state_nonce: 0
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
