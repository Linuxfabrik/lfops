# Ansible Role linuxfabrik.lfops.network

This role configures the network settings on the server. It also disables the [zeroconf](http://www.zeroconf.org/).

The role heavily relies on the [linux_system_roles.network Role](https://github.com/linux-system-roles/network).


## Mandatory Requirements

* Install the [Linux System Roles](https://linux-system-roles.github.io/) on the Ansible control node. For example by calling `ansible-galaxy collection install fedora.linux_system_roles`.


## Tags

| Tag       | What it does                    |
| ---       | ------------                    |
| `network` | Configures the network settings |


## Role Variables

Have a look at the available role variables from the [linux_system_roles.network Role](https://github.com/linux-system-roles/network/blob/main/README.md).

On RHEL 7 `ipv6_disabled` is not supported.

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
