# Ansible Role linuxfabrik.lfops.cron_permissions

This role restricts the system-wide cron configuration to root, as the CIS Benchmarks require for hosts on which cron is installed. It neither installs nor starts cron: LFOps schedules its own jobs with systemd timers.


*Available in the next LFOps release.*


## How the Role Behaves

* `/etc/crontab` and `/etc/cron.deny` get mode `0600`, and `/etc/cron.d`, `/etc/cron.hourly`, `/etc/cron.daily`, `/etc/cron.weekly`, `/etc/cron.monthly` and `/etc/cron.yearly` get mode `0700`, all owned by `root:root`. Paths that do not exist are left alone: on a host without cron the role changes nothing, and not every platform ships every path (for example `/etc/cron.yearly` on the Red Hat family, `/etc/cron.deny` on Debian and Ubuntu).
* Unprivileged users can no longer list the system cron jobs. The cron daemon reads these paths as root, and `crontab` only reads `/etc/cron.deny`, as root (it is setuid root on the Red Hat family), so both keep working.
* A package update may restore the modes the package ships. The next run of this role sets them again.
* The role does not manage cron jobs, and it does not create `/etc/cron.allow`, so every user may still keep a personal crontab.


## Tags

`cron_permissions`

* Restricts the modes of the system-wide cron configuration.
* Triggers: none.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
