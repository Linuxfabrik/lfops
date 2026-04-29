# Ansible Role linuxfabrik.lfops.network

This role is a thin wrapper around the [`fedora.linux_system_roles.network` role](https://github.com/linux-system-roles/network), the upstream Linux System Role for declaring network connections (ethernet, bonds, bridges, VLANs, IP / DNS / route configuration, ...) on top of NetworkManager. It additionally cleans up Hetzner-specific cruft that conflicts with NetworkManager.

Concretely, this role:

* Calls `fedora.linux_system_roles.network` with whatever `network_connections` you pass in (host or group vars).
* On Red Hat-family hosts only: removes the `hc-utils` package (Hetzner Cloud utilities). They install legacy ifcfg scripts that fight with NetworkManager. The task tolerates the package not being installed (`ignore_errors: true`).
* Prints a reminder that NetworkManager may need to be restarted by hand (`systemctl restart NetworkManager`) for the new configuration to take full effect — the upstream role applies connections via NetworkManager APIs, but a few changes (e.g. plugin reloads) require a service restart.


*Available since LFOps `2.0.0`.*


## Mandatory Requirements

* Install the [Linux System Roles](https://linux-system-roles.github.io/) on the Ansible control node, e.g. via `ansible-galaxy collection install fedora.linux_system_roles`.


## Tags

`network`

* Configures the network and removes `hc-utils` (Hetzner) on Red Hat hosts.
* Triggers: none.


## Role Variables

This role does not define its own variables. All configuration is passed straight through to `fedora.linux_system_roles.network`. See the [upstream README](https://github.com/linux-system-roles/network/blob/main/README.md) for the full list (`network_connections`, `network_provider`, `network_state`, ...).

Example:

```yaml
network_connections:

  - name: 'eth0'
    type: 'ethernet'
    autoconnect: true
    ip:
      address:
        - '192.0.2.26/32'
      dhcp4: false
      ipv6_disabled: true
      gateway4: '192.0.2.1'
      auto_gateway: true
      dns:
        - '1.1.1.1'
      dns_search:
        - 'example.com'
    state: 'up'

  # remove the default connections
  - name: 'System eth0'
    persistent_state: 'absent'
  - name: 'System eth1'
    persistent_state: 'absent'
  - name: 'System eth2'
    persistent_state: 'absent'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
