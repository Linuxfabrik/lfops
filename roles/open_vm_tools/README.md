# Ansible Role linuxfabrik.lfops.open_vm_tools

This role installs the [Open VM Tools](https://github.com/vmware/open-vm-tools/), a *set of services and modules that enable several features in VMware products for better management of, and seamless user interactions with, guests. It includes kernel modules for enhancing the performance of virtual machines running Linux or other VMware supported Unix like guest operating systems.* It also manages `vmtoolsd.service`.

This role only makes sense on VMware-virtualized guests. On other virtualization platforms (KVM, Hyper-V, ...) the package may install but the daemon will not have anything useful to talk to.


## Tags

`open_vm_tools`

* Installs `open-vm-tools` and manages `vmtoolsd.service`.
* Triggers: none.

`open_vm_tools:state`

* Manages the state of `vmtoolsd.service` (enable/disable at boot, plus start/stop/restart/reload).
* Triggers: none.


## Optional Role Variables

`open_vm_tools__service_enabled`

* Whether `vmtoolsd.service` is enabled at boot, analogous to `systemctl enable / disable`.
* Type: Bool.
* Default: `true`

`open_vm_tools__service_state`

* State of `vmtoolsd.service`, analogous to `systemctl start / stop / restart / reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `open_vm_tools__service_enabled` is `true`, otherwise `'stopped'`.

Example:
```yaml
# optional
open_vm_tools__service_enabled: true
open_vm_tools__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
