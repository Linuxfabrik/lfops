# Ansible Role linuxfabrik.lfops.kvm_host

This role installs the required packages and configures the host as a KVM host.


## Mandatory Requirements

* Install Python 3, and the python3-libvirt and python3-lxml modules.


## Tags

`kvm_host`

* Install the required packages and configure the host as a KVM host.
* Triggers: none.

`kvm_host:networks`

* Manage libvirt networks.
* Triggers: none.

`kvm_host:pools`

* Manage libvirt storage pools.
* Triggers: none.


## Optional Role Variables

`kvm_host__libvirt_guests_on_shutdown`

* What should happen with the guests (VMs) when the host shuts down. Possible options: `shutdown`, `suspend`.
* Type: String.
* Default: `'shutdown'`

`kvm_host__libvirt_guests_parallel_shutdown`

* Number of guests will be shutdown concurrently.
* Type: Number.
* Default: `5`

`kvm_host__libvirt_guests_service_enabled`

* Enables or disables the libvirt-guests service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`kvm_host__libvirt_guests_shutdown_timeout`

* Number of seconds we're willing to wait for a guest to shut down.
* Type: Number.
* Default: `300`

`kvm_host__libvirtd_service_enabled`

* Enables or disables the libvirtd service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`kvm_host__networks`

* A list of libvirt network definitions.
* Subkeys:

    * `name`:

        * Mandatory. The name of the network.
        * Type: String.

    * `bridge`:

        * Optional. If set, will be used as the network bridge.
        * Type: String.

    * `ip_address`:

        * Optional. If set, will be used the IP address for the interface.
        * Type: String.

    * `subnet`:

        * Optional. Subnet mask for the network.
        * Type: String.
        * Default: `'255.255.255.0'` (if the `ip_address` is set)

    * `dhcp_start`:

        * Optional. Start of the DHCP range. Requires `dhcp_end` to be set as well.
        * Type: String.

    * `dhcp_end`:

        * Optional. End of the DHCP range. Requires `dhcp_start` to be set as well.
        * Type: String.

    * `forward_mode`:

        * Optional. When set to `'nat'` will configure the network to use NAT for the port range 1024-65535.
        * Type: String.

* Type: List of dictionaries.
* Default: `[]`

`kvm_host__pools`

* A list of libvirt storage pool definitions. Currently only supports directory pools.
* Subkeys:

    * `name`:

        * Mandatory. The name of the pool. Use `default` to overwrite the default pool.
        * Type: String.

    * `path`:

        * Mandatory. Path to the directory that should be used as the storage pool.
        * Type: String.

* Type: List of dictionaries.
* Default: `[]`

Example:
```yaml
# optional
kvm_host__libvirt_guests_on_shutdown: 'shutdown'
kvm_host__libvirt_guests_parallel_shutdown: 5
kvm_host__libvirt_guests_service_enabled: true
kvm_host__libvirt_guests_shutdown_timeout: 300
kvm_host__libvirtd_service_enabled: true
kvm_host__networks:
  - name: 'default'
    bridge: 'virbr0'
    ip_address: '192.0.2.0.1'
    subnet: '255.255.255.0'
    dhcp_start: '192.0.2.0.10'
    dhcp_end: '192.0.2.0.254'
    forward_mode: 'nat'
kvm_host__pools:
  - name: 'default'
    path: '/data/kvm/images'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
