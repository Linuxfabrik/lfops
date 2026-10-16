# Ansible Role linuxfabrik.lfops.cron

This role installs the cron daemon (cronie on the Red Hat family, cron on Debian and Ubuntu), keeps it running, and restricts the system-wide cron configuration to root, as the CIS Benchmarks require.


*Available in the next LFOps release.*


## How the Role Behaves

* `/etc/crontab` and `/etc/cron.deny` get mode `0600`, and `/etc/cron.d`, `/etc/cron.hourly`, `/etc/cron.daily`, `/etc/cron.weekly`, `/etc/cron.monthly` and `/etc/cron.yearly` get mode `0700`, all owned by `root:root`. Paths the platform does not ship (for example `/etc/cron.yearly` on the Red Hat family, `/etc/cron.deny` on Debian and Ubuntu) are left alone. Unprivileged users can no longer list the system cron jobs. The cron daemon reads these paths as root, and `crontab` only reads `/etc/cron.deny`, as root (it is setuid root on the Red Hat family), so both keep working.
* A package update may restore the modes the package ships. The next run of this role sets them again.
* The role does not manage cron jobs, and it does not create `/etc/cron.allow`, so every user may still keep a personal crontab.


## Tags

`cron`

* Installs the cron daemon.
* Restricts the modes of the system-wide cron configuration.
* Ensures the cron daemon is in the desired state.
* Triggers: none.

`cron:state`

* Manages the state of the cron daemon (enable/disable at boot, plus start/stop/restart/reload).
* Triggers: none.


## Optional Role Variables

`cron__service_enabled`

* Whether the cron daemon (`crond.service` on the Red Hat family, `cron.service` on Debian and Ubuntu) is enabled at boot, analogous to `systemctl enable / disable`.
* Type: Bool.
* Default: `true`

`cron__service_state`

* State of the cron daemon, analogous to `systemctl start / stop / restart / reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `cron__service_enabled` is `true`, otherwise `'stopped'`.

Example:
```yaml
# optional
cron__service_enabled: true
cron__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
