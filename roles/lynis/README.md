# Ansible Role linuxfabrik.lfops.lynis

This role installs [Lynis](https://cisofy.com/lynis/), the security auditing tool, and deploys `/etc/lynis/custom.prf`, which lists the Lynis tests accepted on the host. It is the prerequisite for the [lynis monitoring plugin](https://github.com/Linuxfabrik/monitoring-plugins/tree/main/check-plugins/lynis), which runs the audit on the host once a day and reports the hardening index and the Lynis findings.


*Available in the next LFOps release.*


## How the Role Behaves

* The role installs the `lynis` package of the distribution, from EPEL on the Red Hat family and from the distribution repositories on Debian and Ubuntu. It does not run an audit itself.
* The Debian and Ubuntu packages ship `lynis.timer` and enable it on installation, which runs a daily `lynis audit system --cronjob` of its own. The role disables and stops it by default, so that the audit of the monitoring plugin is the only one. Two audits running at the same time make the plugin report UNKNOWN. The EPEL package ships no active timer.
* `/etc/lynis/custom.prf` is fully templated from `lynis__skip_tests`. On every run it is re-rendered (a timestamped backup is kept), so a hand-edited `custom.prf` is overwritten. Every audit on the host reads it, the one of the lynis monitoring plugin included, also when the plugin audits the host over SSH from a management host.
* To accept a finding the monitoring plugin reports, take its test ID from the plugin output. Where the plugin says "add `skip-test=NETW-3015` to `/etc/lynis/custom.prf`", add `- name: 'NETW-3015'` to `lynis__skip_tests__host_var` or `lynis__skip_tests__group_var`, and state the reason in `comment`. The finding disappears with the next audit.
* The role validates each test ID before it writes the file. Lynis refuses to run at all if a setting line of a profile contains a character outside of letters, digits and `/[]()_|,.:;=-`, so a typo would otherwise silence the whole audit instead of one test.


## Known Limitations

* The role installs the Lynis release the distribution ships, which is several releases behind upstream on Debian 12 and Ubuntu 22.04. Lynis reports such a release as outdated (test `LYNIS`), as a suggestion first and as a warning once it is ten releases behind.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* On RHEL-compatible systems, the EPEL repository must be enabled (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)).


## Tags

`lynis`

* Installs Lynis.
* Deploys `/etc/lynis/custom.prf`.
* Ensures `lynis.timer` is in the desired state (Debian and Ubuntu).
* Triggers: none.

`lynis:configure`

* Deploys `/etc/lynis/custom.prf`.
* Triggers: none.

`lynis:state`

* Manages the state of `lynis.timer` (Debian and Ubuntu).
* Triggers: none.


## Optional Role Variables

`lynis__skip_tests__host_var` / `lynis__skip_tests__group_var`

* Lynis tests to skip on the host, written to `/etc/lynis/custom.prf` as `skip-test=<name>` lines. Use this to accept a finding or a suggestion, for example one the lynis monitoring plugin reports.
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

* Whether `lynis.timer` is enabled at boot. Debian and Ubuntu only.
* Type: Bool.
* Default: `false`
* Deviates from the upstream default `true` on Debian and Ubuntu: the lynis monitoring plugin already runs a daily audit, and a second one at the same time makes it report UNKNOWN.

`lynis__timer_state`

* State of `lynis.timer`. Debian and Ubuntu only.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `lynis__timer_enabled` is `true`, otherwise `'stopped'`.

Example:
```yaml
# optional
lynis__skip_tests__group_var:
  - name: 'HRDN-7222'
    comment: 'Compilers are needed on our build hosts'
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

* An entry in `lynis__skip_tests__*_var` is not of the form `NETW-3015` or `SSH-7408:loglevel`. Copy the test ID from the output of the monitoring plugin or from `lynis show details`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
