# Ansible Role linuxfabrik.lfops.core_dumps

This role hardens a system by disabling core dumps. Core dumps can leak sensitive data (passwords, keys) from a crashed process's memory to disk, so they are usually unwanted on production servers.


*Available in the next LFOps release.*


## How the Role Behaves

The role disables core dumps through the three mechanisms a modern Linux system uses, following the CIS Benchmark recommendations:

* `* hard core 0` in `/etc/security/limits.d/` stops the shell / PAM from writing core dumps.
* `fs.suid_dumpable = 0` (sysctl) prevents core dumps of setuid / setgid processes.
* `Storage=none` and `ProcessSizeMax=0` in `/etc/systemd/coredump.conf.d/` keep `systemd-coredump` from storing core dumps.

The `hard core` limit applies to login sessions started after the change. The sysctl value is applied immediately via `sysctl --system`.


## Tags

`core_dumps`

* Deploys the core dump configuration.
* Triggers: `core_dumps: sysctl --system`.


## Optional Role Variables

`core_dumps__limits_hard_core`

* The `hard core` limit written to `/etc/security/limits.d/`. `0` disables core dumps for all users.
* Type: Number.
* Default: `0`

`core_dumps__sysctl_suid_dumpable`

* The `fs.suid_dumpable` sysctl value. `0` prevents core dumps of setuid / setgid processes.
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
core_dumps__sysctl_suid_dumpable: 0
core_dumps__systemd_process_size_max: 0
core_dumps__systemd_storage: 'none'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
