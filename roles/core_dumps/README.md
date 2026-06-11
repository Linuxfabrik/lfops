# Ansible Role linuxfabrik.lfops.core_dumps

This role hardens a system by disabling core dumps. Core dumps can leak sensitive data (passwords, keys) from a crashed process's memory to disk, so they are usually unwanted on production servers.


*Available since LFOps `7.0.0`.*


## How the Role Behaves

The role disables core dumps through the three mechanisms a modern Linux system uses, following the CIS Benchmark recommendations:

* `* hard core 0` in `/etc/security/limits.d/` stops the shell / PAM from writing core dumps.
* `fs.suid_dumpable = 0` (sysctl) prevents core dumps of setuid / setgid processes. This value is not written by this role directly; it is handed to the `kernel_settings` role, which owns sysctl management.
* `Storage=none` and `ProcessSizeMax=0` in `/etc/systemd/coredump.conf.d/` keep `systemd-coredump` from storing core dumps.

The `hard core` limit applies to login sessions started after the change.


## Dependent Roles

Any LFOps playbook that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* The `fs.suid_dumpable` sysctl is applied through the `kernel_settings` role (role: [kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings)).


## Tags

`core_dumps`

* Deploys the core dump configuration.
* Triggers: none.


## Optional Role Variables

`core_dumps__limits_hard_core`

* The `hard core` limit written to `/etc/security/limits.d/`. `0` disables core dumps for all users.
* Type: Number.
* Default: `0`

`core_dumps__systemd_process_size_max`

* The `ProcessSizeMax` value in `/etc/systemd/coredump.conf.d/`. `0` disables processing of core dumps by `systemd-coredump`.
* Type: Number.
* Default: `0`

`core_dumps__systemd_storage`

* The `Storage` value in `/etc/systemd/coredump.conf.d/`. `none` keeps `systemd-coredump` from storing core dumps.
* Type: String.
* Default: `'none'`

Example:
```yaml
# optional
core_dumps__limits_hard_core: 0
core_dumps__systemd_process_size_max: 0
core_dumps__systemd_storage: 'none'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
