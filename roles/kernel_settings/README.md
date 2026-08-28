# Ansible Role linuxfabrik.lfops.kernel_settings

This role configures kernel settings. The settings are made permanently and activated simultaneously at runtime.

The role does nothing on its own and relies on the [linux_system_roles.kernel_settings role](https://github.com/linux-system-roles/kernel_settings).


*Available since LFOps `2.0.0`.*


## Known Limitations

* TuneD applies the settings when its daemon starts, and systemd starts `tuned.service` in parallel with other services. A service that reads kernel parameters at its own startup can therefore come up before TuneD has applied the profile and then keeps the old values for its whole runtime. `sysctl` and `tuned-adm verify` report the new values in the meantime, because both look at the current kernel state rather than at the state the service saw.
* Example: the kernel applies the `net.core.somaxconn` clamp inside `listen()`, so Redis keeps the old accept queue size until it is restarted.
* Wherever a service depends on a parameter this role sets, that service needs a systemd drop-in ordering it after TuneD.
* Put the ordering into the consuming unit rather than collecting a `Before=` list in a drop-in for `tuned.service`: the requirement belongs to the service that has it, a central list has to be kept in sync with every host, and a long `Before=` list invites ordering cycles, which systemd resolves by silently dropping an arbitrary edge. An ordering dependency on a unit that is not installed is ignored without a warning, so the same drop-in is safe on hosts without TuneD.
* The ordering works because `tuned.service` is `Type=dbus` and TuneD claims `com.redhat.tuned` only after the profile has been applied. That guarantee comes from the TuneD implementation, not from a documented contract, so it is worth re-checking after a major TuneD version jump.
* Ordering only applies while systemd computes a transaction. Restarting `tuned.service` on a running host does not restart the consuming services, so they keep their stale values until they are restarted themselves.

Example:
```ini
# /etc/systemd/system/redis.service.d/z00-after-tuned.conf
# TuneD claims its D-Bus name only after applying the profile, so ordering
# this service After=tuned.service guarantees the sysctls are in place first.
# Verified against tuned 2.22.1 on Rocky 8: daemon.py calls start_tuning()
# before exports.start(), which reaches dbus.service.BusName() in
# dbus_exporter.py, where Type=dbus readiness is signalled.
[Unit]
After=tuned.service
```


## Requirements

Manual steps:

* Install the [Linux System Roles](https://linux-system-roles.github.io/) on the Ansible control node, for example by calling `ansible-galaxy collection install fedora.linux_system_roles`.


## Tags

`kernel_settings`

* Configures kernel settings.
* Triggers: none.


## Optional Role Variables

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

* `kernel_settings__sysctl__host_var`, `kernel_settings__sysctl__group_var`
* `kernel_settings__sysfs__host_var`, `kernel_settings__sysfs__group_var`
* `kernel_settings__systemd_cpu_affinity__host_var`, `kernel_settings__systemd_cpu_affinity__group_var`
* `kernel_settings__transparent_hugepages_defrag__host_var`, `kernel_settings__transparent_hugepages_defrag__group_var`
* `kernel_settings__transparent_hugepages__host_var`, `kernel_settings__transparent_hugepages__group_var`

For details have a look at the available role variables from the [linux_system_roles.kernel_settings role](https://github.com/linux-system-roles/kernel_settings/blob/master/README.md).

Example:
```yaml
# optional
kernel_settings__sysctl__group_var:
  - name: 'vm.overcommit_memory'
    value: 1
  - name: 'net.core.somaxconn'
    value: 1024
kernel_settings__sysfs__group_var:
  - name: '/sys/kernel/debug/x86/pti_enabled'
    value: 0
  - name: '/sys/kernel/debug/x86/retp_enabled'
    value: 0
kernel_settings__systemd_cpu_affinity__group_var: '1,3,5,7'
kernel_settings__transparent_hugepages__group_var: 'madvise'
kernel_settings__transparent_hugepages_defrag__group_var: 'defer'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
