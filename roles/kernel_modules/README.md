# Ansible Role linuxfabrik.lfops.kernel_modules

This role disables kernel modules by deploying `/etc/modprobe.d/linuxfabrik-kernel-modules.conf`. It is used to harden a system by preventing rarely used or potentially dangerous drivers (FireWire storage, uncommon network protocols, USB storage, ...) from being loaded.


*Available in the next LFOps release.*


## How the Role Behaves

For each module, the role writes an `install <module> /bin/true` line. This prevents the module from being loaded, both automatically (e.g. on device hotplug) and via a manual `modprobe`. This is stronger than `blacklist`, which only prevents automatic loading.

By default the role disables the modules that the CIS Benchmarks recommend disabling and that are safe to disable on a typical server: the FireWire storage stack (`firewire-core`, `firewire-ohci`, `firewire-sbp2`), the legacy / obscure filesystems `cramfs`, `freevxfs`, `hfs`, `hfsplus` and `jffs2`, and the uncommon network protocols `atm`, `can`, `dccp`, `rds`, `sctp` and `tipc`.

Some modules that CIS also lists are **not** disabled by default, because doing so would break common workloads: `overlay` (used by Docker / Podman), `squashfs` (used by snap on Ubuntu and by live / appliance images), `udf` (mounting DVDs / UDF images) and `usb-storage` (USB flash drives). Disable any of these explicitly where wanted.

A module that is already loaded when the role runs stays loaded until the next reboot. Reboot the host (or unload the module manually with `modprobe -r`) to fully apply the change.

To re-enable a module that the role disables by default, set its `enabled` to `true` in your inventory.


## Tags

`kernel_modules`

* Deploys the modprobe configuration that disables the configured kernel modules.
* Triggers: none.


## Optional Role Variables

`kernel_modules__modules__host_var`, `kernel_modules__modules__group_var`

* List of kernel modules to manage. Each item has a `name` and an optional `enabled`: `false` (the default; the module is blocked from loading) or `true` (the module is left loadable, e.g. to override a module the role disables by default).
* Type: List of dictionaries.
* Default: unset (the role default disables `atm`, `can`, `cramfs`, `dccp`, `firewire-core`, `firewire-ohci`, `firewire-sbp2`, `freevxfs`, `hfs`, `hfsplus`, `jffs2`, `rds`, `sctp` and `tipc`).

Example:
```yaml
# optional
kernel_modules__modules__group_var:
  # additionally disable USB storage ('enabled: false' is the default and can be omitted)
  - name: 'usb-storage'
    enabled: false
  # re-enable SCTP, which the role disables by default
  - name: 'sctp'
    enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
