# Ansible Role linuxfabrik.lfops.aide

This role installs and configures [AIDE](https://aide.github.io/) (Advanced Intrusion Detection Environment), creates the AIDE database, and schedules a regular file integrity check with `aide-check.timer`.

This role is Red Hat-family only. It does not run on Debian / Ubuntu.

This role is compatible with the following aide versions:

* 0.16 (RHEL 8)
* 0.19 (RHEL 9, RHEL 10)


*Available in the next LFOps release.*


## How the Role Behaves

* `/etc/aide.conf` is fully templated. The options and the attribute groups (`NORMAL`, `CONTENT`, `PERMS`, ...) follow the installed aide version. The rules come from `aide__rules__*_var`, whose default is the rule list RHEL 9 and 10 ship, used on RHEL 8 as well. It additionally excludes `/root/.ansible/tmp`, where Ansible keeps a temporary directory while a task runs.
* On the first run the role creates the database (`/var/lib/aide/aide.db.gz`), after it has deployed the config and the systemd units. Depending on the size of the file system, `aide --init` can take several minutes.
* `aide-check.service` runs `aide --check` at a low CPU and IO priority. Any finding (added, removed or changed files) makes the check exit non-zero, which leaves `aide-check.service` in the failed state. Monitor failed systemd units to get alerted. The report is written to `/var/log/aide/aide.log` and to the journal (`journalctl --unit aide-check.service`). The role sends no mail.
* When the role changes `/etc/aide.conf`, its own units or whether `aide-check.timer` is enabled, it updates the database afterwards, so that the next check does not report every path the new rules add or drop. It only does so if the last check had not reported changes: re-baselining a failing check would silently accept whatever changed on the host, an intrusion included. The same applies to a database the role finds on a host where it has not deployed `aide-check.service` yet, for example one left by a previous AIDE setup: no check of this role has vouched for it. In both cases the database is left alone and the run tells you so. Review `/var/log/aide/aide.log` or the output of `aide --check`, and accept the current state with `--tags aide:update_db`.
* The re-baseline accepts everything that changed since the last check, not only the change the role made. The shorter the check interval, the smaller that window.
* Changes to monitored files made by anyone else, other LFOps roles and package updates included, are reported by the next check. The [system_update](https://github.com/Linuxfabrik/lfops/tree/main/roles/system_update) role knows about `aide-check.service` and updates the database after it has updated packages, provided the last check was clean.


## Known Limitations

* Debian and Ubuntu are not supported.
* Non-recursive negative rules (`-/path`) are not available, since aide 0.16 on RHEL 8 does not know them.


## Tags

`aide`

* Installs aide.
* Deploys `/etc/aide.conf`.
* Deploys `aide-check.service` and `aide-check.timer`, and sets the state of the timer.
* Creates the AIDE database if it does not exist yet.
* Triggers: AIDE database update.

`aide:configure`

* Deploys `/etc/aide.conf`.
* Triggers: AIDE database update.

`aide:cron`

* Deploys `aide-check.service` and `aide-check.timer`.
* Triggers: AIDE database update.

`aide:state`

* Enables or disables `aide-check.timer` and sets its state.
* Triggers: AIDE database update.

`aide:update_db`

* Not run by default, only when the tag is given explicitly.
* Updates the AIDE database to the current state of the host and clears the failed state of `aide-check.service`. Use it after reviewing a finding, to accept the reported changes.
* Triggers: none.


## Optional Role Variables

`aide__check_on_calendar`

* When `aide-check.timer` runs the check. See [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/latest/systemd.time.html) for the format.
* Type: String.
* Default: `'*-*-* 06:{{ 59 | random(seed=inventory_hostname) }}:00'`

`aide__rules__host_var` / `aide__rules__group_var`

* The rules in `/etc/aide.conf`. See [aide.conf(5)](https://github.com/aide/aide/blob/master/doc/aide.conf.5) for the rule syntax. Items are identified by their `path`: an item with the `path` of a default rule changes that rule in place, `state: 'absent'` removes it, and a new `path` is appended at the end. The order matters, since within one directory aide applies the first rule that matches. A `negative` rule always wins, wherever it is.
* Type: List of dictionaries.
* Default: the rule list RHEL 9 and 10 ship, see `aide__rules__role_var` in [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/aide/defaults/main.yml).
* Deviates from the upstream default in two places: the role adds `!/root/\.ansible/tmp`, since Ansible creates and deletes a directory there for every task it runs as root, and on RHEL 8 it uses the RHEL 9 / 10 list instead of the one aide 0.16 ships, so that all hosts are checked against the same rules.
* Subkeys:

    * `path`:

        * Mandatory. The regular expression the rule matches, for example `/opt/app` or `/etc/app.conf$`. It always matches from the start of the path.
        * Type: String.

    * `attributes`:

        * Mandatory for rules of type `regular` and `equal`. The attributes or group to check, for example `NORMAL`, `CONTENT`, `PERMS` or `p+u+g+sha512`.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

    * `type`:

        * Optional. `regular` monitors the path and everything below it. `equal` monitors only the path itself (`=`). `negative` excludes the path and everything below it from monitoring (`!`), also when another rule covers it.
        * Type: String. One of `equal`, `negative`, `regular`.
        * Default: `'regular'`

`aide__timer_enabled`

* Whether `aide-check.timer` is enabled at boot.
* Type: Bool.
* Default: `true`

`aide__timer_state`

* State of `aide-check.timer`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'`

Example:
```yaml
# optional
aide__check_on_calendar: '*-*-* 03:30:00'
aide__rules__host_var:
  - path: '/usr'
    attributes: 'CONTENT'
  - path: '/etc/cups'
    state: 'absent'
  - path: '/srv/app'
    attributes: 'NORMAL'
  - path: '/srv/app/cache'
    type: 'negative'
  - path: '/srv$'
    type: 'equal'
    attributes: 'DIR'
aide__timer_enabled: true
aide__timer_state: 'started'
```


## Troubleshooting

**The run aborts with `aide X.Y is not supported by this role`**

* The enabled repositories offer an aide version the role has no config for. The role supports aide 0.16 (RHEL 8) and 0.19 (RHEL 9 / 10). Pin the host to a supported version, or add the version to `roles/aide/vars/main.yml` and to the version branches in `roles/aide/templates/etc/aide.conf.j2`.

**`aide-check.service` is failed**

* The last check found added, removed or changed files. Read the report in `/var/log/aide/aide.log`. If the changes are expected, accept them with `ansible-playbook --inventory inventory linuxfabrik.lfops.aide --limit myhost --tags aide:update_db`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
