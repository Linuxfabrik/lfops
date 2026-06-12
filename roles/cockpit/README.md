# Ansible Role linuxfabrik.lfops.cockpit

[Cockpit](https://cockpit-project.org/) is a web-based admin UI for Linux servers (services, logs, networking, terminal, container management). This role can either install all `cockpit*` packages or remove them again from a host (for hardening / attack-surface-reduction reasons).


*Available since LFOps `2.0.0`.*


## Tags

`cockpit`

* Installs or removes cockpit packages.
* Triggers: none.

`cockpit:state`

* Manages the state of the systemd socket.
* Triggers: none.


## Optional Role Variables

`cockpit__additional_packages`

* Additional cockpit packages to install, to extend the functionality of the web console.
* Type: List of strings.
* Default: unset

`cockpit__socket_enabled`

* Enables or disables the `cockpit.socket`, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`cockpit__state`

* State of the cockpit packages. Possible Options: `'absent'`, `'present'`.
* Type: String.
* Default: `'absent'`

Example:
```yaml
# optional
cockpit__additional_packages:
  - 'cockpit-machines' # for KVM administration
cockpit__socket_enabled: true
cockpit__state: 'present'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
