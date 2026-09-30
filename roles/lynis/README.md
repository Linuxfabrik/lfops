# Ansible Role linuxfabrik.lfops.lynis

This role installs [Lynis](https://cisofy.com/lynis/), the security auditing tool, runs an audit of the host once a day through a systemd timer, and deploys `/etc/lynis/custom.prf`, which lists the Lynis tests accepted on the host. The results are left in `/var/log/lynis.log` and `/var/log/lynis-report.dat` for the [lynis-logfile monitoring plugin](https://github.com/Linuxfabrik/monitoring-plugins/tree/main/check-plugins/lynis-logfile) to evaluate.


*Available in the next LFOps release.*


## How the Role Behaves

* The role installs the `lynis` package of the distribution, from EPEL on the Red Hat family and from the distribution repositories on Debian and Ubuntu.
* The Lynis release of the distribution is several releases behind upstream on Debian 12 and Ubuntu 22.04. On Debian and Ubuntu the package disables the online check for a newer release (`skip-upgrade-test=yes` in `/etc/lynis/default.prf`), so an outdated release is not reported there. On the Red Hat family Lynis looks up the latest release in a DNS TXT record on every audit and reports an outdated release (test `LYNIS`), as a suggestion first and as a warning once it is ten releases behind.
* `lynis.timer` starts `lynis.service` once a day at `lynis__on_calendar`, which runs `lynis audit system --cronjob --quiet` as root with low CPU and I/O priority. A run takes about two minutes. A host that was down at that time catches up after the next boot (`Persistent=true`).
* The role deploys both units to `/etc/systemd/system` on every platform. On Debian and Ubuntu they replace the `lynis.timer` and `lynis.service` the package ships, so the audit runs at the same time and with the same options everywhere.
* Every audit overwrites `/var/log/lynis.log` and `/var/log/lynis-report.dat`. `lynis show details <TEST-ID>` explains a finding from that log.
* `/etc/lynis/custom.prf` is fully templated from `lynis__skip_tests`. On every run it is re-rendered (a timestamped backup is kept), so a hand-edited `custom.prf` is overwritten. Every audit on the host reads it: the daily one of `lynis.timer`, and a network scan with the lynis monitoring plugin from a management host.
* To accept a finding the monitoring plugin reports, take its test ID from the plugin output. Where the plugin says "add `skip-test=NETW-3015` to `/etc/lynis/custom.prf`", add `- name: 'NETW-3015'` to `lynis__skip_tests__host_var` or `lynis__skip_tests__group_var`, and state the reason in `comment`. The finding disappears with the next audit.
* The role validates each test ID before it writes the file. Lynis refuses to run at all if a setting line of a profile contains a character outside of letters, digits and `/[]()_|,.:;=-`, so a typo would otherwise silence the whole audit instead of one test.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* On RHEL-compatible systems, the EPEL repository must be enabled (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)).
* On Rocky 9+, the CRB ("Code Ready Builder") repository must be enabled, since EPEL packages depend on it (role: [linuxfabrik.lfops.repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos)).


## Tags

`lynis`

* Installs Lynis.
* Deploys `/etc/lynis/custom.prf`.
* Deploys `lynis.service` and `lynis.timer` and ensures the timer is in the desired state.
* Triggers: none.

`lynis:configure`

* Deploys `/etc/lynis/custom.prf`.
* Triggers: none.

`lynis:cron`

* Deploys `lynis.service` and `lynis.timer` and ensures the timer is in the desired state.
* Triggers: none.

`lynis:state`

* Manages the state of `lynis.timer` (start, stop, enable, disable).
* Triggers: none.


## Optional Role Variables

`lynis__on_calendar`

* When `lynis.timer` runs the audit, in the calendar event format of `systemd.time(7)`.
* Type: String.
* Default: `'*-*-* 02:{{ 59 | random(seed=inventory_hostname) }}'`
* Deviates from the upstream default `daily` (midnight, randomized by up to 30 minutes): the audit runs at a fixed minute per host, so the results are in place at a predictable time.

`lynis__skip_tests__host_var` / `lynis__skip_tests__group_var`

* Lynis tests to skip on the host, written to `/etc/lynis/custom.prf` as `skip-test=<name>` lines. Use this to accept a finding or a suggestion, for example one the lynis-logfile monitoring plugin reports.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. The Lynis test ID as the monitoring plugin reports it, for example `NETW-3015`. To skip a single check within a test, append it after a colon, for example `SSH-7408:loglevel`. `lynis show details <TEST-ID>` on the host explains a test.
        * Type: String.

    * `comment`:

        * Optional. Why the test is skipped. Written as a comment line above the `skip-test` line, so the reason is on the host as well.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`lynis__timer_enabled`

* Enables or disables `lynis.timer`, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`lynis__timer_state`

* Changes the state of `lynis.timer`, analogous to `systemctl start/stop/restart`.
* Type: String. One of `restarted`, `started`, `stopped`.
* Default: `'started'`

Example:
```yaml
# optional
lynis__on_calendar: '*-*-* 03:15'
lynis__skip_tests__host_var:
  - name: 'SSH-7408:loglevel'
    comment: 'sshd logs to a central log server with its own log level'
  - name: 'HRDN-7222'
    state: 'absent'
lynis__timer_enabled: true
lynis__timer_state: 'started'
```


## Troubleshooting

**The run aborts with `lynis__skip_tests: "..." is not a Lynis test ID`**

* An entry in `lynis__skip_tests__*_var` is not of the form `NETW-3015`, `KRB5-1030` or `SSH-7408:loglevel`. Copy the test ID from the output of the monitoring plugin or from `lynis show details`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
