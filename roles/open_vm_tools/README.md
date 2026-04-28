# Ansible Role linuxfabrik.lfops.open_vm_tools

This role installs the [Open VM Tools](https://github.com/vmware/open-vm-tools/), a *set of services and modules that enable several features in VMware products for better management of, and seamless user interactions with, guests. It includes kernel modules for enhancing the performance of virtual machines running Linux or other VMware supported Unix like guest operating systems.* It also starts and enables `vmtoolsd.service`.

This role only makes sense on VMware-virtualized guests. On other virtualization platforms (KVM, Hyper-V, ...) the package may install but the daemon will not have anything useful to talk to.

Unlike `qemu_guest_agent` or `haveged`, this role does not expose a `__service_enabled` variable; the service is always enabled and started.


## Tags

`open_vm_tools`

* Installs open-vm-tools and enables vmtoolsd.service.
* Triggers: none.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
