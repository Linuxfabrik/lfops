# Ansible Role linuxfabrik.lfops.kernel_modules

This role disables kernel modules by deploying `/etc/modprobe.d/linuxfabrik-kernel-modules.conf`. It is used to harden a system by preventing rarely used or potentially dangerous drivers (FireWire storage, uncommon network protocols, USB storage, ...) from being loaded.


*Available since LFOps `7.0.0`.*


## How the Role Behaves

* For each module, the role writes an `install <module> /bin/true` line. This prevents the module from being loaded, both automatically (e.g. on device hotplug) and via a manual `modprobe`. This is stronger than `blacklist`, which only prevents automatic loading.
* By default the role disables the modules that the CIS Benchmarks recommend disabling and that are safe to disable on a typical server: the FireWire storage stack (`firewire-core`, `firewire-ohci`, `firewire-sbp2`), the legacy / obscure filesystems `cramfs`, `freevxfs`, `hfs`, `hfsplus` and `jffs2`, and the uncommon network protocols `atm`, `can`, `dccp`, `rds`, `sctp` and `tipc`.
* Some modules that CIS also lists are **not** disabled by default, because doing so would break common workloads: `overlay` (used by Docker / Podman), `squashfs` (used by snap on Ubuntu and by live / appliance images), `udf` (mounting DVDs / UDF images) and `usb-storage` (USB flash drives). Disable any of these explicitly where wanted.
* A module that is already loaded when the role runs stays loaded until the next reboot. When the configuration changed and at least one of the blocked modules is loaded, the role requests a reboot at the next maintenance window through the [schedule_reboot](https://github.com/Linuxfabrik/lfops/tree/main/roles/schedule_reboot) mechanism (spool entry `kernel_modules`); without that mechanism it only prints a message and leaves the reboot to the operator. Unloading the module by hand with `modprobe -r` applies the change without a reboot. A host that has none of the blocked modules loaded is already in the target state and gets no request, which is why deploying the defaults to a fresh host does not reboot it.
* To re-enable a module that the role disables by default, set its `enabled` to `true` in your inventory.
* Only the run that changes the configuration requests the reboot. A later run finds the file already correct and stays quiet, even while the modules are still loaded and the reboot is still pending.
* `lfops__reboot_now` makes the role reboot in the same run instead of waiting for the window. The reboot still goes through the same mechanism, so the notification mail, the Icinga downtime and the grace period all apply, and a reboot another role requested earlier in the run is carried out together with this one. The role then waits for the host to come back before the play continues. Have a look at the [README](https://github.com/Linuxfabrik/lfops/blob/main/README.md#lfops__reboot_now). With the variable set on a host where the `schedule_reboot` mechanism is missing, the run aborts rather than reporting a reboot it cannot perform.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* Optional: the reboot mechanism should be in place (role: [linuxfabrik.lfops.schedule_reboot](https://github.com/Linuxfabrik/lfops/tree/main/roles/schedule_reboot)), so blocking a module that is still loaded reboots the host at the maintenance window instead of waiting for a manual reboot.


## Tags

`kernel_modules`

* Deploys the modprobe configuration that disables the configured kernel modules.
* Requests a reboot when a module that is still loaded got blocked, or performs it in the same run when `lfops__reboot_now` is set.
* Triggers: none.


## Optional Role Variables

`kernel_modules__modules__host_var` / `kernel_modules__modules__group_var`

* List of kernel modules to manage. Each item has a `name` and an optional `enabled`: `false` (the default; the module is blocked from loading) or `true` (the module is left loadable, e.g. to override a module the role disables by default).
* Type: List of dictionaries.
* Default: `atm`, `can`, `cramfs`, `dccp`, `firewire-core`, `firewire-ohci`, `firewire-sbp2`, `freevxfs`, `hfs`, `hfsplus`, `jffs2`, `rds`, `sctp` and `tipc` are disabled.

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
