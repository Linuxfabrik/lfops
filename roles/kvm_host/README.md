# Ansible Role linuxfabrik.lfops.kvm_host

This role installs the required packages and configures the host as a KVM host.

Tested on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Install Python 3, and the python3-libvirt and python3-lxml modules.


## Tags

| Tag        | What it does                                                       |
| ---        | ------------                                                       |
| `kvm_host` | Install the required packages and configure the host as a KVM host |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `kvm_host__libvirt_guests_on_shutdown` | What should happen with the guests (VMs) when the host shuts down. Possible options:<br> * `shutdown`<br> * `suspend` | `'shutdown'` |
| `kvm_host__libvirt_guests_parallel_shutdown` | Number of guests will be shutdown concurrently. | `5` |
| `kvm_host__libvirt_guests_service_enabled` | Enables or disables the libvirt-guests service, analogous to `systemctl enable/disable --now`. | `true` |
| `kvm_host__libvirt_guests_shutdown_timeout` | Number of seconds we're willing to wait for a guest to shut down. | `300` |
| `kvm_host__libvirtd_service_enabled` | Enables or disables the libvirtd service, analogous to `systemctl enable/disable --now`. | `true` |
| `kvm_host__networks` | A list of libvirt network definitions. Subkeys:<br> * `name`: Mandatory, string. The name of the network.<br> * `bridge`: Optional, string. If set, will be used as the network bridge.<br> * `ip_address`: Optional, string. If set, will be used the IP address for the interface.<br> * `subnet`: Optional, string. Subnet mask for the network. Defaults to `255.255.255.0` if the `ip_address` is set.<br> * `dhcp_start`: Optional, string. Start of the DHCP range. Requires `dhcp_end` to be set as well.<br> * `dhcp_end`: Optional, string. End of the DHCP range. Requires `dhcp_start` to be set as well. | `[]` |
| `kvm_host__pools` | A list of libvirt storage pool definitions. Currently only supports directory pools. Subkeys:<br> * `name`: Mandatory, string. The name of the pool. Use `default` to overwrite the default pool.<br> * `path`: Mandatory, string. Path to the directory that should be used as the storage pool. | `[]` |

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
kvm_host__pools:
  - name: 'default'
    path: '/data/kvm/images'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
