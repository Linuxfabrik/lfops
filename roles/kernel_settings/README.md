# Ansible Role linuxfabrik.lfops.kernel_settings

This role configures kernel settings. The settings are made permanently and activated simultaneously at runtime.

The role does nothing on its own and relies on the [linux_system_roles.kernel_settings role](https://github.com/linux-system-roles/kernel_settings).


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* If any `sunrpc.*` setting is configured (the mariadb_server role sets `sunrpc.tcp_slot_table_entries`), the role loads the `sunrpc` kernel module and lists it in `/etc/modules-load.d/sunrpc.conf`, since the `sunrpc.*` settings only exist while the module is loaded and nothing else loads it at boot on a host without NFS. `options sunrpc` lines in `/etc/modprobe.d/` are commented out in the process. The file stays in place when the `sunrpc.*` settings are removed later.
* On Ubuntu 22.04 the role removes `kernel.sched_min_granularity_ns` and `kernel.sched_wakeup_granularity_ns` from the TuneD profile it builds on (a `drop` entry in its own profile). The TuneD release of Ubuntu 22.04 sets them although its 5.15 kernel has neither, and TuneD's own verification would otherwise fail on every run.


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

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time. For details on the values have a look at the [linux_system_roles.kernel_settings role](https://github.com/linux-system-roles/kernel_settings/blob/master/README.md).

`kernel_settings__sysctl__host_var` / `kernel_settings__sysctl__group_var`

* sysctl settings. Entries are identified by `name`, so an entry from the inventory is merged into the default entry of the same name.
* Type: List of dictionaries.
* Default: on Ubuntu 22.04

    ```yaml
    - name: 'drop'
      value: 'kernel.sched_min_granularity_ns,kernel.sched_wakeup_granularity_ns'
    ```

    `[]` on all other platforms.

* Deviates from the upstream default `[]` on Ubuntu 22.04: the TuneD profile there sets two scheduler sysctls that the 5.15 kernel does not have, and TuneD's own verification would fail on every run (see "How the Role Behaves").
* Subkeys:

    * `name`:

        * Mandatory. Name of the sysctl, or `drop` to remove options from the TuneD profile the role builds on. An inventory entry named `drop` replaces the value of the default one, so list the two scheduler sysctls there as well on Ubuntu 22.04.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`. `absent` removes the setting from the profile.
        * Type: String.
        * Default: `'present'`

    * `value`:

        * Mandatory for `state: 'present'` entries. Value of the sysctl, or the comma-separated options for `drop`.
        * Type: String or Number.

`kernel_settings__sysfs__host_var` / `kernel_settings__sysfs__group_var`

* sysfs settings. Entries are identified by `name`.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Path below `/sys`.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`. `absent` removes the setting from the profile.
        * Type: String.
        * Default: `'present'`

    * `value`:

        * Mandatory for `state: 'present'` entries. Value to write.
        * Type: String or Number.

`kernel_settings__systemd_cpu_affinity__host_var` / `kernel_settings__systemd_cpu_affinity__group_var`

* The CPUs systemd pins its processes to, for example `'1,3,5,7'`.
* Type: String.
* Default: `''` (not set by the role, the TuneD profile's value applies)

`kernel_settings__transparent_hugepages__host_var` / `kernel_settings__transparent_hugepages__group_var`

* The transparent hugepages mode.
* Type: String. One of `always`, `madvise`, `never`.
* Default: `''` (not set by the role, the TuneD profile's value applies)

`kernel_settings__transparent_hugepages_defrag__host_var` / `kernel_settings__transparent_hugepages_defrag__group_var`

* The transparent hugepages defrag mode.
* Type: String. One of `always`, `defer`, `defer+madvise`, `madvise`, `never`.
* Default: `''` (not set by the role, the TuneD profile's value applies)

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
