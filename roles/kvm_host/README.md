# Ansible Role kvm_host

This role installs the required packages and configures the host as a KVM host.

FQCN: linuxfabrik.lfops.kvm_host

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* Install Python 3, and the python3-libvirt and python3-lxml modules.


### Optional

This role does not have any optional requirements.


## Tags

| Tag      | What it does                                                       |
| ---      | ------------                                                       |
| kvm_host | Install the required packages and configure the host as a KVM host |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/kvm_host/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### kvm_host__libvirt_guests_on_shutdown

What should happen with the guests (VMs) when the host shuts down. Possible options:

* shutdown
* suspend

Default:
```yaml
kvm_host__libvirt_guests_on_shutdown: 'shutdown'
```


#### kvm_host__libvirt_guests_parallel_shutdown

Number of guests will be shutdown concurrently.

Default:
```yaml
kvm_host__libvirt_guests_parallel_shutdown: 5
```


#### kvm_host__libvirt_guests_shutdown_timeout

Number of seconds we're willing to wait for a guest to shut down.

Default:
```yaml
kvm_host__libvirt_guests_shutdown_timeout: 300
```


#### kvm_host__libvirt_guests_service_enabled

Enables or disables the libvirt-guests service, analogous to `systemctl enable/disable --now`. Possible options:

* true
* false

Default:
```yaml
kvm_host__libvirt_guests_service_enabled: true
```


#### kvm_host__libvirtd_service_enabled

Enables or disables the libvirtd service, analogous to `systemctl enable/disable --now`. Possible options:

* true
* false

Default:
```yaml
kvm_host__libvirtd_service_enabled: true
```



## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
