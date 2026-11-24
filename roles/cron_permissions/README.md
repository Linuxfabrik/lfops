# Ansible Role linuxfabrik.lfops.cron_permissions

This role restricts cron to root, as the CIS Benchmarks require for hosts on which cron is installed. It neither installs nor starts cron: LFOps schedules its own jobs with systemd timers.


*Available in the next LFOps release.*


## How the Role Behaves

* `/etc/crontab` and `/etc/cron.deny` get mode `0600`, and `/etc/cron.d`, `/etc/cron.hourly`, `/etc/cron.daily`, `/etc/cron.weekly`, `/etc/cron.monthly` and `/etc/cron.yearly` get mode `0700`, all owned by `root:root`. Paths that do not exist are left alone: on a host without cron the role changes nothing, and not every platform ships every path (for example `/etc/cron.yearly` on the Red Hat family, `/etc/cron.deny` on Debian and Ubuntu).
* Unprivileged users can no longer list the system cron jobs. The cron daemon reads these paths as root, so the system cron jobs keep running.
* Only root and the users in `cron_permissions__allow_users__*_var` may manage a personal crontab. The role writes them to `/etc/cron.allow`, which makes `crontab` ignore `/etc/cron.deny`. Crontabs installed before still run, but their owners can no longer list or change them.
* On Debian and Ubuntu, root cannot use `crontab -u <user>` for a user not listed either, which also affects `ansible.builtin.cron` with `user`. The Red Hat family lets root do so.
* On the Red Hat family, `/etc/cron.allow` gets mode `0600`, owned by `root:root`. On Debian and Ubuntu, `crontab` reads it as group `crontab`, so it gets `root:crontab` `0640`. Do not change this to `root:root`: if `crontab` cannot read `/etc/cron.allow` there, it refuses every user but root, including the listed ones.
* `/etc/cron.allow` is overwritten on every run, a timestamped backup is kept. On a host without `/usr/bin/crontab`, the role does not create it.
* A package update may restore the modes the package ships. The next run of this role sets them again.
* The role does not manage cron jobs.


## Tags

`cron_permissions`

* Restricts the modes of the system-wide cron configuration.
* Deploys `/etc/cron.allow`.
* Triggers: none.


## Optional Role Variables

`cron_permissions__allow_users__host_var` / `cron_permissions__allow_users__group_var`

* Users besides root that may manage a personal crontab.
* Type: List of dictionaries.
* Default: `[]`
* Deviates from the upstream default, which ships no `/etc/cron.allow` and so lets every user not listed in `/etc/cron.deny` schedule jobs: an allow list cannot miss an account added later.
* Subkeys:

    * `name`:

        * Mandatory. User name.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

Example:
```yaml
# optional
cron_permissions__allow_users__host_var:
  - name: 'backup'
  - name: 'olduser'
    state: 'absent'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
