# Ansible Role linuxfabrik.lfops.aide

This role installs and configures [AIDE](https://aide.github.io/) (Advanced Intrusion Detection Environment), creates the AIDE database, and schedules a regular file integrity check with `aidecheck.timer`, following the filesystem integrity recommendations of the CIS benchmarks.

This role is compatible with the following aide versions:

* 0.16 (RHEL 8)
* 0.17 (Ubuntu 22.04)
* 0.18 (Debian 12, Ubuntu 24.04)
* 0.19 (Debian 13, RHEL 9, RHEL 10, Ubuntu 26.04)


*Available in the next LFOps release.*


## How the Role Behaves

* Before it deploys `/etc/aide.conf`, the role has aide check the new file (`aide --config-check`) and aborts the run if aide does not accept it, for example because of a typo in a rule or in `aide__conf_raw`. The file on the host stays as it was.
* `/etc/aide.conf` is fully templated, with the same path, database (`/var/lib/aide/aide.db.gz`) and rules on every platform. The options and the attribute groups (`NORMAL`, `CONTENT`, `PERMS`, ...) follow the installed aide version. All groups use sha512 as their only checksum. The rules come from `aide__rules__*_var`, whose default is the rule list RHEL 9 and 10 ship, extended by the Debian and Ubuntu counterparts of its paths and by the audit tool rules the CIS benchmarks ask for. A path a host does not have is skipped.
* Rules from the inventory with a path of their own are placed above the default rules, so that a rule such as `/root/\.bashrc$` takes effect instead of the default `/root/\..*` rule. A default rule changed from the inventory keeps its place.
* On Debian and Ubuntu the role installs aide without its recommended packages and purges `aide-common` if it is installed. `aide-common` runs a daily check of its own next to `aidecheck.timer`, which mails its report instead of failing, writes the same `/var/log/aide/aide.log`, and pulls in cron and a mail transport agent (exim4 on Debian, postfix on Ubuntu). The role purges it, including its configuration in `/etc/aide`.
* The aide binaries of Debian and Ubuntu are built without a default config file. All aide runs of LFOps take the lock `/run/aide.lock` and run one after the other, since a second aide run exits with 21 while another one runs. Run aide by hand the same way, on every platform: `flock /run/aide.lock aide --config=/etc/aide.conf --check`.
* On the first run the role creates the database (`/var/lib/aide/aide.db.gz`), after it has deployed the config and the systemd units and after the pending handlers of the play have run. Depending on the size of the file system, `aide --init` can take several minutes. In a playbook that combines several roles, run aide last, as `setup_basic` does, so that the database contains what the other roles deployed.
* `aidecheck.service` runs `aide --check` at a low CPU and IO priority, by `aidecheck.timer` and after every boot, once the services have started. Any finding (added, removed or changed files) makes the check exit non-zero, which leaves `aidecheck.service` in the failed state. The [aide-logfile](https://github.com/Linuxfabrik/monitoring-plugins/tree/main/check-plugins/aide-logfile) monitoring plugin evaluates the report, and monitoring failed systemd units alerts as well. The full report is written to `/var/log/aide/aide.log`, overwritten by every check. From aide 0.17 on, a summary (whether and how many files changed) additionally goes to syslog (`journalctl --unit aidecheck.service`), from where rsyslog forwards it. aide 0.16 (RHEL 8) cannot limit the syslog report, so there the report only goes to the file. The role sends no mail.
* `/etc/logrotate.d/aide` rotates the report weekly with `copy` instead of the `copytruncate` the RHEL package ships, which would leave `/var/log/aide/aide.log` empty until the next check, as if the check had aborted.
* A check that is due while the [system_update](https://github.com/Linuxfabrik/lfops/tree/main/roles/system_update) role or `unattended-upgrades` installs packages waits until the update has finished. Conversely, `system_update` and the dpkg hook wait for a running check before they update the database. The role waits for it for 5 minutes at most and then aborts the run (see "Troubleshooting"). After every database update the role starts a check, so that `/var/log/aide/aide.log` shows the state of the host rather than the changes the update accepted.
* When the role changes `/etc/aide.conf`, its own units or whether `aidecheck.service` or `aidecheck.timer` is enabled, it updates the database afterwards, so that the next check does not report every path the new rules add or drop. It only does so if the last check had not reported changes: re-baselining a failing check would silently accept whatever changed on the host, an intrusion included. The same applies to a database the role finds on a host where it has not deployed `aidecheck.service` yet, for example one left by a previous AIDE setup: no check of this role has vouched for it. In both cases the database is left alone and the run tells you so. Review `/var/log/aide/aide.log` or the output of `aide --check`, and accept the current state with `--tags aide:update_db_force`.
* The re-baseline after a change of the role accepts everything that changed since the last check, not only the change the role made. The shorter the check interval, the smaller that window.
* Every LFOps playbook checks the result of the last check before it changes anything on the host, and stops if that check reported changes. After a clean start, `aide-update.service` updates the database once the run has finished, so the changes of the run are not reported. The playbook does not wait for the update. See `lfops__skip_aide_check_before_run` in the [LFOps README](https://github.com/Linuxfabrik/lfops#lfops__skip_aide_check_before_run--lfops__skip_aide_update_db_after_run) for the details and how to skip either step.
* Changes to monitored files made outside LFOps, packages installed by hand included, are reported by the next check. The [system_update](https://github.com/Linuxfabrik/lfops/tree/main/roles/system_update) role knows about `aidecheck.service`: it runs a check before it updates packages and updates the database afterwards if that check was clean.
* On Debian and Ubuntu the same applies to the updates of `unattended-upgrades`: a dpkg hook (`/usr/local/sbin/aide-dpkg-hook`, wired in by `/etc/apt/apt.conf.d/z00-linuxfabrik-aide`) runs a check before `unattended-upgrades` installs its first package, and if that check was clean, `aide-dpkg-update.service` updates the database once the upgrade has finished. `unattended-upgrades` installs in several steps, one dpkg run each, but the check and the update run only once per upgrade. The upgrade takes longer by that one check, while apt holds its lock. The hook only acts on dpkg runs of `unattended-upgrades`, so a package installed with apt by hand is reported, as on the Red Hat family. Changes made on the host while the upgrade runs are accepted along with it.
* On Debian and Ubuntu the role creates an empty `/etc/apt/sources.list` if there is none, as on hosts with only `/etc/apt/sources.list.d/*.sources`. `unattended-upgrades` creates that file on every run otherwise, and the check before the first upgrade would report it.
* The [duplicity](https://github.com/Linuxfabrik/lfops/tree/main/roles/duplicity) role backs up `/var/lib/aide` by default. An attacker with root privileges can replace the local database. The database only changes when it is updated (by this role, `--tags aide:update_db` or `aide:update_db_force`, `aide-update.service` after an LFOps run, the system_update role or `aide-dpkg-update.service`), so a local database that differs from the backup of a day without such an update points to tampering.
* Before it creates the database, the role waits for running package jobs: `apt-daily.service` and `apt-daily-upgrade.service` on Debian and Ubuntu, `dnf-automatic.service` and `dnf-automatic-install.service` on the Red Hat family, and `security-update.service` and `update-and-reboot.service` of the [system_update](https://github.com/Linuxfabrik/lfops/tree/main/roles/system_update) role everywhere. A package installation during `aide --init` would leave entries without checksums in the database.


## Known Limitations

* Non-recursive negative rules (`-/path`) are not available, since aide 0.16 to 0.18 do not know them.
* Python byte code that a package does not compile when it is installed is written on its first use and reported by the next check as added, for example below `/usr/lib/python3/dist-packages/netplan/__pycache__` on Ubuntu 22.04 after a netplan update. Review and accept it with `--tags aide:update_db_force`.
* The CIS benchmarks for Debian 12 and Ubuntu 22.04 expect `aide-common` to be installed, and the one for Debian 12 accepts no other check than its `dailyaidecheck.timer`. The role removes `aide-common` instead, since its check never fails on a finding, so these recommendations are reported as not met there.
* On RHEL 8 the audit script of the CIS benchmark for the audit tool rules fails whatever `/etc/aide.conf` contains: it locates the file with `whereis aide.conf`, which util-linux 2.32 answers with `/usr/sbin/aide`. The rules are in place all the same.


## Tags

`aide`

* Installs aide.
* Deploys `/etc/aide.conf` and `/etc/logrotate.d/aide`, and on Debian and Ubuntu the dpkg hook and `aide-dpkg-update.service`.
* Deploys `aidecheck.service` and `aidecheck.timer`, enables both and sets the state of the timer.
* Deploys `aide-update.service`, which updates the database on request, for example after every LFOps run.
* Creates the AIDE database if it does not exist yet.
* Triggers: AIDE database update.

`aide:configure`

* Deploys `/etc/aide.conf` and `/etc/logrotate.d/aide`, and on Debian and Ubuntu the dpkg hook and `aide-dpkg-update.service`.
* Triggers: AIDE database update.

`aide:state`

* Enables or disables `aidecheck.service` and `aidecheck.timer`, and sets the state of the timer.
* Triggers: AIDE database update.

`aide:update_db`

* Not run by default, only when the tag is given explicitly.
* Updates the AIDE database to the current state of the host, but only if the last check had not reported changes, the same condition under which the role updates the database after a change of its own. Otherwise the database is left alone and the run tells you so. Every LFOps playbook already has the database updated after the run (see "How the Role Behaves"), so the tag is for changes made outside a playbook run: `ansible-playbook --inventory inventory linuxfabrik.lfops.aide --limit myhost --tags aide:update_db`. Like that update, it accepts everything that changed since the last check, not only the changes of the run.
* Triggers: none.

`aide:update_db_force`

* Not run by default, only when the tag is given explicitly.
* Updates the AIDE database to the current state of the host, whatever the last check reported, and clears the failed state of `aidecheck.service`. Use it after reviewing a finding, to accept the reported changes.
* Triggers: none.


## Optional Role Variables

`aide__check_on_calendar`

* When `aidecheck.timer` runs the check. The default runs it twice a day, after the update and reboot window of the [system_update](https://github.com/Linuxfabrik/lfops/tree/main/roles/system_update) and [schedule_reboot](https://github.com/Linuxfabrik/lfops/tree/main/roles/schedule_reboot) roles (04:00 by default), so that a finding shows up during office hours. If you move that window, move the check along with it: a check that runs while an update installs packages reports them, and the database is then no longer updated after updates. See [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/latest/systemd.time.html) for the format.
* Type: String.
* Default: `'*-*-* 07,12:{{ 59 | random(seed=inventory_hostname) }}:00'`

`aide__conf_raw`

* Raw content inserted into `/etc/aide.conf` between the attribute groups and the rules. Groups and macros defined here can be used by `aide__rules__*_var`, and a rule here takes precedence over the rules from `aide__rules__*_var` that belong to the same directory (see `aide__rules__host_var`). A negative rule excludes its paths wherever it is. Declare the value as `!unsafe` if it contains `{{` or `{%`.
* Type: Multiline string.
* Default: `''`

`aide__conf_report_level`

* How much the report in `/var/log/aide/aide.log` tells about each finding, from least to most:

    * `minimal`: whether there are findings.
    * `summary`: plus their number.
    * `database_attributes`: plus the checksums of the database.
    * `list_entries`: plus the names of added, removed and changed files.
    * `changed_attributes`: plus old and new value of each changed attribute.
    * `added_removed_attributes`: plus the attributes a rule starts or stops checking.
    * `added_removed_entries`: plus all attributes of added and removed files.

* On aide 0.16 (RHEL 8) the role translates the value into `verbose`, where `minimal` and `summary`, and `database_attributes` and `list_entries`, give the same report.
* Type: String. One of `added_removed_attributes`, `added_removed_entries`, `changed_attributes`, `database_attributes`, `list_entries`, `minimal`, `summary`.
* Default: `'added_removed_entries'`
* Deviates from the upstream default `changed_attributes`: an added file is otherwise reported by its name only, while its owner, permissions and checksums are what tells a harmless file from an intruder's, also after it has been deleted again.

`aide__rules__host_var` / `aide__rules__group_var`

* The rules in `/etc/aide.conf`. See [aide.conf(5)](https://github.com/aide/aide/blob/master/doc/aide.conf.5) for the rule syntax. Items are identified by their `path`: an item with the `path` of a default rule changes that rule in place, `state: 'absent'` removes it, and items with a new `path` are placed above the default rules, in the order they are listed. The order matters within a directory: aide assigns each rule to the directory its fixed path prefix lies in (`/root/\.bashrc$` and `/root/\..*` to `/root`, `/etc/apt` to `/etc`, `/etc` to `/`), checks a path against the rules of the deepest such directory first, and applies the first rule that matches within a directory. Use `aide --config=/etc/aide.conf --path-check=f:/path/to/file` (aide 0.17 and newer) to see which rule applies to a file. A `negative` rule always wins, wherever it is.
* Type: List of dictionaries.
* Default: the rule list RHEL 9 and 10 ship, extended by the Debian and Ubuntu counterparts of its paths, see `aide__rules__role_var` in [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/aide/defaults/main.yml).
* Deviates from the upstream default, so that all hosts are checked against the same rules without reporting what changes during normal operation:

    * The RHEL 9 / 10 list is used on every platform, extended by the Debian and Ubuntu counterparts of its paths. On Debian and Ubuntu the rules of `aide-common` are not used.
    * `!/root/\.ansible/tmp` is added, since Ansible creates and deletes a directory there for every task it runs as root.
    * `!/root/\.cache` is added. It holds disposable caches only and gains pip cache entries on every run of the python_venv role.
    * `!/usr/lib/sysimage/rpm` is added. The RPM database lives there on RHEL 10, and every rpm or dnf query rewrites it.
    * The audit tool rules of the CIS benchmarks are added.
    * `/etc/ld.so.cache` and `/etc/udev/hwdb.bin` are checked without their inode (`DATAONLY`), since systemd rebuilds both on the first boot after an update.
    * `/etc/aliases.db` is checked for permissions only (`PERMS`), since postfix on the Red Hat family rebuilds it on its start.
    * `/etc/resolv.conf` is checked for permissions only (`PERMS`), since DHCP clients and NetworkManager rewrite it at runtime.

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

`aide__service_enabled`

* Whether `aidecheck.service` is enabled, which runs the check after every boot, once the services have started.
* Type: Bool.
* Default: `true`

`aide__timer_enabled`

* Whether `aidecheck.timer` is enabled, which runs the check by `aide__check_on_calendar`.
* Type: Bool.
* Default: `true`

`aide__timer_state`

* State of `aidecheck.timer`.
* Type: String. One of `restarted`, `started`, `stopped`.
* Default: `'started'`

Example:
```yaml
# optional
aide__check_on_calendar: '*-*-* 03:30:00'
aide__conf_raw: |-
  APP = p+u+g+sha512
  !/var/lib/app/cache
aide__conf_report_level: 'changed_attributes'
aide__rules__host_var:
  - path: '/root/\.bashrc$'
    attributes: 'APP' # references APP defined in `aide__conf_raw`
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
aide__service_enabled: true
aide__timer_enabled: true
aide__timer_state: 'started'
```


## Troubleshooting

**The run aborts with `aide X.Y is not supported by this role`**

* The enabled repositories offer an aide version the role has no config for. The role supports aide 0.16, 0.17, 0.18 and 0.19. Pin the host to a supported version, or add a `roles/aide/templates/etc/<version>-aide.conf.j2` and list the version in `roles/aide/vars/main.yml`.

**The run aborts at `Deploy /etc/aide.conf` with `failed to validate`**

* aide rejected the new config, and `/etc/aide.conf` was left as it was. The message quotes the line aide stumbled over, typically a rule from `aide__rules__*_var` or a line in `aide__conf_raw` with an undefined group, an attribute the installed aide version does not know, or an invalid regular expression. Fix the inventory and run the role again.

**The run aborts at a task that waits up to 5 minutes**

* An AIDE check (`aidecheck.service`) or a package job was still running after 5 minutes. A check takes longer on a large file system or a busy disk. Wait until `systemctl is-active aidecheck.service` and the package jobs the task names no longer report `active` or `activating`, then run the role again.

**The run stops with `aide: The last AIDE check reported changes`**

* Every LFOps playbook stops on a host whose last check reported changes, before it changes anything. Read the report in `/var/log/aide/aide.log`. If the changes are expected, accept them with `ansible-playbook --inventory inventory linuxfabrik.lfops.aide --limit myhost --tags aide:update_db_force`, then run the playbook again. To deploy without accepting them, run the playbook with `--extra-vars='lfops__skip_aide_check_before_run=true'`; the database is then not updated after the run.

**`aidecheck.service` is failed**

* The last check found added, removed or changed files. Read the report in `/var/log/aide/aide.log`. If the changes are expected, accept them with `ansible-playbook --inventory inventory linuxfabrik.lfops.aide --limit myhost --tags aide:update_db_force`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
