# Roles

* Reading the README must be enough to understand and use a role.
* Idempotency: a second run with the same parameters neither changes nor reports changes, and never damages an existing installation (even without tags), e.g. `create user if not exists` with a `changed_when` / `failed_when` that recognizes the "already exists" error.
* Run without tags, a role delivers a completely installed application.
* Do not over-engineer; the role can grow later.
* One role per software application, supporting all its versions (e.g. PHP 7.1, 7.2, 7.3).
* No role dependencies via `meta/main.yml`; dependencies are handled in playbooks.
* Do not use the general-purpose roles `apps`, `files` and `systemd_unit` as dependent roles (via `__dependent_var`); they are driven from the inventory, and wiring into them over-restricts the playbook order. Do such tasks in the consuming role.
* List inputs are lists of dictionaries with `state: present/absent`, see [Combined Variables](variables.md#combined-variables).
* Fail loudly. Avoid constructs that suppress errors, like `IfModule` in Apache httpd.
* Do not support EOL software versions.
* For a new application, consider security, monitoring and backups.
* Backups: `duplicity` backs up the fixed list `duplicity__backup_sources__role_var` (`roles/duplicity/defaults/main.yml`). A role storing data outside of it adds the directory there and to `roles/duplicity/README.md`; setup playbooks cannot inject it, since they do not run `duplicity`. Databases are backed up by a dump to `/backup` (see `mariadb_server`, `postgresql_server`, `mongodb`, `influxdb`), never by their live data directory.
* For mailing, use `sendmail`, which is consistent across distros.
* All user-facing information goes into the README; comments are for developers only.
* Avoid breaking changes as far as possible, but don't let them stand in the way of improvements.
* Document all changes in the [CHANGELOG.md](https://github.com/Linuxfabrik/lfops/blob/main/CHANGELOG.md).


## README

`roles/example/README.md` is the canonical template. Keep these sections in this order, drop optional ones that do not apply, invent no new top-level sections:

```
# Ansible Role linuxfabrik.lfops.<name>   + intro paragraph(s)        (mandatory)
[ "This role is compatible with the following <x> versions:" + list ] (optional)
*Available since LFOps `X.X.X`.*                                      (mandatory)
## How the Role Behaves                                               (optional)
## Known Limitations                                                  (optional)
## Dependent Roles                                                    (optional)
## Requirements                                                       (optional)
## Single-Node Setup / Cluster Setup / Adding a Node ... / <descriptive>  (optional walkthrough)
## Post-Installation Steps                                            (optional)
## Tags                                                               (mandatory)
## Mandatory Role Variables                                           (optional)
## Recommended Role Variables                                         (optional)
## Optional Role Variables                                            (optional)
## Optional Role Variables - <Subgroup>                               (optional, repeatable)
## Troubleshooting                                                    (optional)
## License                                                            (mandatory)
## Author Information                                                 (mandatory)
```

* **`*Available since LFOps`**: the release the role first shipped in; set once, never change. A new role gets the literal line `*Available in the next LFOps release.*`, rewritten with `sed` at release time.
* **How the Role Behaves**: proactive, non-obvious notes (who needs network access to what, overwrite-on-rerun, upgrade path, what the role does NOT do, security caveats). Troubleshooting is reactive error->fix, Known Limitations are hard constraints.
* **Dependent Roles vs Requirements**:
    * An LFOps role that **this role's own playbook** (`X.yml` or a bundling `setup_X.yml`) runs goes under `## Dependent Roles`, as a declarative state naming the role ("The X repository must be enabled (role: ...)"). Default roles form the first list under the lead-in "Any LFOps playbook that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables."; feature-optional ones are marked "Optional:". Roles off by default go under "These roles are not enabled by default; enable them via the playbook's skip variables if needed:". Skip-variable names and play order live solely in `playbooks/README.md`.
    * A value the user supplies is a variable, documented under `## ... Role Variables` only.
    * Everything else the operator provides goes under `## Requirements`: host resources, external accounts or subscriptions, credentials as plain bullets; hands-on procedures (run a SEPARATE playbook, mint a token in a web console, install on the controller, configure DNS) imperatively under a "Manual steps:" list-title. A dependency needing a separate playbook is a manual step, not a dependent role. Mark feature-optional items "Optional:".
* **Variable subgroups**: large roles MAY split variables into `## Optional Role Variables - <Subgroup>` (or Mandatory) sections, named after the upstream module, the variable prefix as code span, or a functional label, each with its own `Example:` block. Mandatory and Optional of one subgroup MAY stay paired (as in `apache_httpd`). A grouping is always its own `##` section, never a `###`.
* **Subheadings and walkthroughs**: `###` only as sub-structure inside a section, never as a variable subgroup. The walkthrough slot accepts a descriptive title (e.g. `bind` `## Primary-Secondary Example`). Sections are separated by two blank lines, including around the `*Available since*` marker.
* **Special roles**: utility roles (e.g. `shared`) MAY replace `## Tags` and `## *Role Variables` with `## Available Tasks` and `## Usage Example`; controller-side API roles (e.g. `uptimerobot`) MAY add `## Running the Role`, `## Example Inventory` and `## Read-Only Inspection`. Both keep the mandatory frame.
* **Reference-grade sections**: a role MAY add a focused section where no canonical one fits (e.g. `apache_tomcat` `## Multiple Tomcat Instances`). Keep these minimal.


## Handlers

* Use handlers instead of `some_result is changed` if no `meta: flush_handlers` is required or if it avoids duplicate code.
* Prefix handlers with the role name, since handlers are global.
* Chain handlers (notify) when validation should precede the action, e.g. a config check notifying a restart.
* A restart or reload handler skips when the service was just started or should be stopped:

    ```yaml
    - name: 'example: restart example'
      ansible.builtin.service:
        name: 'example'
        state: 'restarted'
      when:
        - '__example__service_state_result is not changed'
        - 'example__service_state != "stopped"'
    ```


## Reboots

A role never reboots the host on its own. It files a request with [schedule_reboot](https://github.com/Linuxfabrik/lfops/tree/main/roles/schedule_reboot), and the host reboots once at its maintenance window, together with every other pending reason. `lfops__reboot_now: true` (as `--extra-vars`, or in `group_vars` for hosts needing no window) makes the role perform it in the same run. It defaults to `false` and is documented once in the [README](../../README.md#lfops__reboot_now). Both paths write the same spool file, so both keep the notification mail, the Icinga downtime and the grace period, and coalesce with earlier requests.

| Situation                                                     | Behaviour                                                                            |
| ---                                                           | ---                                                                                  |
| Nothing changed                                               | No request and no message.                                                           |
| Changed, `lfops__reboot_now` set, schedule_reboot is deployed | Requests the reboot, triggers it, waits for the host to come back.                   |
| Changed, schedule_reboot is deployed                          | Requests the reboot. It happens at the window.                                       |
| Changed, schedule_reboot is absent                            | Reports that the operator has to reboot. The run succeeds.                           |
| `lfops__reboot_now` set, schedule_reboot is absent            | The run aborts before changing anything, naming both remedies.                       |
| The request itself fails                                      | The run aborts. A lost reboot request must never be reported as a successful deploy. |

A consuming role wires in two task files of the `shared` role and never spells out the mechanism itself:

* `shared/tasks/assert-reboot-possible.yml` in the validation block, tagged `always`, not gated on whether this run needs a reboot, so the run is refused before anything is written.
* `shared/tasks/request-reboot.yml` where the role knows whether it changed something, gated on that, with `shared__reboot_reason` (e.g. the role name) and `shared__reboot_detail` (e.g. `'kernel command line changed'`).

Reference: [roles/bootloader](https://github.com/Linuxfabrik/lfops/tree/main/roles/bootloader); also `crypto_policy`, `kernel_modules`, `selinux`.

* **Gate on this run having changed something**, not on the host still needing a reboot: `ansible.posix.selinux` reports `reboot_required` until the reboot, which would fail the Molecule `idempotence` step. The spool file in `/run` keeps the first request.
* **No request without runtime effect**, e.g. a module blocklist only needs a reboot if such a module is loaded (`roles/kernel_modules` reads `/proc/modules`).
* **Never reboot with `ansible.builtin.reboot` on your own**: it bypasses mail, downtime and coalescing, and hides the state from `schedule_reboot`.
* **Check mode needs no extra guards**; neither `command` nor `reboot` acts under `--check`.

Constraints of `request-reboot.yml`:

* Detect the reboot by the boot ID over Ansible's own connection (`ansible.builtin.reboot` polls `/proc/sys/kernel/random/boot_id`), never by a controller-side `wait_for` on the SSH port, which misjudges hosts behind an `ssh_config` alias, jump host or `ProxyCommand`. Waiting only for the host to come back fails too, since the actor mails and calls Icinga before its grace period.
* Start the actor with `systemctl start --no-block`, not `schedule-reboot --now`, because the `Type=oneshot` service only returns once the host reboots. The request is filed beforehand with the same `schedule-reboot` call as the windowed path.
* `reboot_timeout` also covers grace period, mail and Icinga call; a reboot not happening within it fails the run.

A role that requests reboots also:

* Runs `schedule_reboot` before itself in its playbook, gated by `<playbook>__skip_schedule_reboot` (see `playbooks/bootloader.yml`).
* Lists the mechanism as optional under `## Dependent Roles` and describes the effect under `## How the Role Behaves`.
* Tests the windowed path in its ordinary scenario (request file waits in `/run/schedule-reboot/`, host still up) and the immediate path in a destructive sub-scenario (change effective when `verify.yml` starts) with a non-zero grace period. References: `extensions/molecule/bootloader/install` and `.../reboot_now`.


## Preflight Checks

A role checks what the host or the outside world has to provide (a file in a Git repository, a reachable server) before it changes anything, and puts these checks into `tasks/preflight.yml`: read-only, carrying the role's tags, imported at the top of `tasks/main.yml`. References: `roles/firewall`, `roles/icinga2_agent`.

A playbook that runs many roles, such as `setup_basic`, aborts on a missing prerequisite before its first role changes the host. Otherwise a run aborting after hundreds of tasks leaves SSH hardened and the firewall replaced, and the next run may no longer connect with the bootstrap user. In its `pre_tasks`, such a playbook:

* includes `shared/tasks/validate-role-arguments.yml`, tagged `always`, with the roles it runs. It lists them in `<playbook>__roles__internal_var`, each with the condition under which the play skips it; `tests/unit/test_playbooks.py` keeps the list in sync with the play.
* includes the `preflight.yml` of each role that has one, with `tasks_from`, gated on the role's skip variable and tagged like the role.
* imports the `rpm` role first, since every package task reads the RPM database, then the `dnf` role, so that every package task gets its mirror settings, and the `network` role ahead of a preflight that has to reach a server by name, since the image of a fresh VM can bring a dead nameserver. These are the only roles that change the host before the preflight checks.

Disk space needs go through `shared/tasks/assert-disk-space.yml`, never into a README alone. A role with a fixed need calls it in its `preflight.yml` (reference: `roles/graylog_server`). A playbook whose roles only fill up the disk together passes all of them at once, since the task adds them up per filesystem (reference: `playbooks/setup_icinga2_master.yml`). Measure the numbers on a real installation, and give every requirement a `creates`, so that an installed host with a full disk can still be re-configured.


## Reporting a Manual Step to the Operator

When a role ends with something the operator has to do by hand, it prints the message with `ansible.builtin.debug` and appends it to `__shared__end_of_play_messages` with `ansible.builtin.set_fact`, both under the same condition. `roles/shared/tasks/print-messages.yml` in every playbook's `post_tasks` prints the collected list as one block above the `PLAY RECAP`. The inline `debug` stays for plays outside this collection. Define the text once:

```yaml
# roles/example/vars/main.yml
__example__end_of_play_message: 'example: The kernel command line has changed. Please reboot the server manually to apply it.'
# roles/example/tasks/main.yml, set_fact
__shared__end_of_play_messages: '{{ __shared__end_of_play_messages | d([]) + [__example__end_of_play_message] }}'
```

* Prefix each message with the role name, and append with `| d([])`.
* Never use `cacheable: true`; the recommended `jsonfile` fact cache would resurface the entry on unrelated runs.
* `__shared__` is the namespace for shared internals (`roles/shared/`); the user-facing LFOps-wide prefix is `lfops__`.
* Append only for a real manual step, under a condition that is false once converged. The printer reports `changed`, so a message on every run fails the `idempotence` step.
* A handler appends via a second handler task with the same `listen`, as in [roles/mongodb](https://github.com/Linuxfabrik/lfops/blob/main/roles/mongodb/handlers/main.yml).
* References: `roles/bootloader`, `roles/kernel_settings`, `roles/network`.

Known limitation: `post_tasks` do not run when the play fails (`force_handlers` does not help); the inline messages cover that case.


## Tags

* Naming scheme: `role_name` and `role_name:section`, e.g. `apache_httpd:vhosts`.
* A tag does only what its name says: `mariadb:users` only manages MariaDB users.
* The README lists the tags and what they do.
* Set tags in the role, not in the playbook.
* Base package installation needs no tag like `apache:install`.
* A task usually has multiple tags; consider every area it belongs to.
* Reuse a section name from the vocabulary below whenever one fits. Invent one (e.g. `mariadb_server:galera_new_cluster`) only if none fits.

Vocabulary: `:certs` (TLS certificates and keys), `:configure` (configuration and settings; everything not covered by a more specific section), `:containers` (containers and their systemd units), `:databases`, `:dump` (scheduled dumps / backups), `:enroll` (register the node with a remote service), `:firewalls` (cloud firewall / security-group rules), `:logrotate`, `:modules` (OS-level pluggable modules, e.g. PHP, SELinux, Apache), `:networks` (cloud VM, libvirt or container networks), `:plugins` (application plugins / add-ons, e.g. Grafana), `:remove` (uninstall and remove artifacts), `:state` (start / stop / enable / disable services, timers, sockets), `:update` (update the application), `:upgrade` (post-update migration steps), `:users` (application or service accounts).

`always` and `never` keep their built-in meaning. `always` marks prerequisites: loading platform variables, `assert` validation of the inventory (`argument_specs` already runs under `always`), and discovery of host state that another role or tag needs (e.g. `__php__installed_version`). Tag them `always` instead of listing the role's tags, which would miss tags added later.

`always` tasks also run when their role is not selected (`setup_nextcloud --tags apache_httpd` on a fresh host), so they must work where the rest of the role never ran:

* Read host state so that absence is reported, not fatal: the `exists` key of `ansible.builtin.stat`, `"php" in ansible_facts["packages"]` before indexing it.
* Leave a discovered fact undefined while the software is missing, never guess. Consumers guard with `is defined`.
* Prefer a value the inventory already carries, such as a declared version.

Such a role gets a `foreign_tags` Molecule sub-scenario running the playbook with another role's tag against hosts without the software (reference: `extensions/molecule/php/foreign_tags`).


## Roles with Special Features

Unusual techniques and the role to read before reusing them; all other roles follow `roles/example`.


### Build from source (autotools)

* `libmaxminddb`: GitHub release tarball, `./configure`, `make`, `make check`, `make install`.


### Custom SELinux policy modules

* `selinux`: compiles inventory-defined `.te` source (`checkmodule`, `semodule_package`, `semodule --install`) and applies modules → booleans / file contexts / ports → restorecon → setenforce, so new types are usable in the same run.
* `php`: publishes `php__selinux__modules__dependent_var` from `vars/main.yml` (several playbooks run `selinux` before `php`), with the source inline in `content_te`, since a role has no controller directory for `src`.
* `fail2ban`: templates a CIL module and loads it with `semodule --install` right after its package, because the module needs `fail2ban_t`, which RHEL 10 only gets from the package's `fail2ban-selinux` dependency, after the `selinux` role has run. CIL needs no policy compiler on the host.

Before adding an `allow` rule, work out what it buys an attacker **on top of** the DAC gates and record it next to the rule: `ptrace_may_access()` and similar run DAC and capability checks before the LSM hook. Example: `lfops_php_fpm_slowlog` in `roles/php/vars/main.yml`.


### FACL with multi-user / inherited access

* `mirror`: RW for webserver and service user, plus `default:` ACLs for inheritance.


### Multi-OS coverage (Linux + Windows)

* `monitoring_plugins`: separate `linux-*.yml` and `windows-*.yml` task files.


### Non-default Jinja2 delimiters

* `telegraf`: `#jinja2:variable_start_string:'[%', variable_end_string:'%]'` in `telegraf.conf.j2` keeps Telegraf's own `{{ ... }}`.


### Permission management via `find -exec chmod`

* `grav`: four `chmod` passes (files `664`, `bin/` `775`, directories `775`, setgid), `changed_when` from `--changes`.


### Python dependencies for air-gapped targets

* `monitoring_plugins` installs a hash-pinned lockfile into a venv on a target without PyPI access:
    * The target reports `platform.python_version()` (pip reads a bare `3.9` as 3.9.0, which e.g. cryptography excludes) and `platform.libc_ver()`.
    * The controller runs `pip download --no-deps --require-hashes --implementation cp --python-version <full version>` with one `--platform manylinux_2_<n>_<arch>` per glibc minor from 17 up to the target's plus `manylinux2014_<arch>` (pip does not widen these). `--no-deps` allows pure-Python sdists; their build backend (`setuptools`, `wheel`, ...) is fetched with `--only-binary=:all:` into the same directory.
    * The files go below a root-owned path on the target, never `/tmp`, since pip trusts that directory and its requirements file holds the hashes.
    * `ansible.builtin.pip` with `extra_args: '--no-index --find-links <dir> --require-hashes'` keeps pip offline and syncs an existing venv on every run.


### Reboot requests

* `bootloader`: see "Reboots".


### Setting options in a packaged file instead of templating it

* Use it when the packaged file is fine as shipped, the role only sets single options, and a template would silently drop settings made by hand.
* `dnf`: `community.general.ini_file` with `backup: true` sets only the entries of a `name` / `value` / `state` list in `/etc/dnf/dnf.conf`; `state: 'absent'` removes an option. The file has no `ansible_managed` header, and options set by hand stay.


### systemd socket activation with an on-demand backend

* `chromium_headless`: a `.socket` unit plus `systemd-socket-proxyd` fronts Chromium on `127.0.0.1`; the proxy exits when idle, and `BindsTo=` starts and stops the backend with it.


### Other

* `apache_solr`: OpenJDK package per platform and Solr major version via `vars/<platform>.yml` (RHEL 10 and Debian 13 ship no Java 17), asserted per platform; `security.json` hashes computed on the controller with a host- and user-derived salt, so the file only changes with a password; `solr.in.sh` and `log4j2.xml` per Solr major (`9-`, `10-`), since Solr 10 renamed their variables.
* `borg_local`: the passphrase and the Icinga2 API login are systemd credentials, see [Secrets for systemd Services](systemd.md#secrets-for-systemd-services).
* `duplicity`: the backend password is a systemd credential, see [Secrets for systemd Services](systemd.md#secrets-for-systemd-services); `duba exec` runs duplicity with the environment of the backup.
* `mariadb_server`: the dump login is a systemd credential, see [Secrets for systemd Services](systemd.md#secrets-for-systemd-services).
* `mongodb`: `state: skip` in `mongodb__databases` / `mongodb__users` leaves an entry untouched; the dump login is a systemd credential, see [Secrets for systemd Services](systemd.md#secrets-for-systemd-services).
* `moodle`: patch tag discovered via `api.github.com/repos/moodle/moodle/tags`, first match of `^v<configured-version>`.
* `nextcloud`: a state file skips install-only tasks after the initial installation; concise "Tags" README section; the Icinga2 API login of `nextcloud-update` is a systemd credential, see [Secrets for systemd Services](systemd.md#secrets-for-systemd-services).
* `php`: present/absent split of `php__modules__combined_var` into two batched package calls.
* `redis`: installed version via `package_facts` selects `<version>-redis.conf.j2`; systemd via unit-file overrides.
