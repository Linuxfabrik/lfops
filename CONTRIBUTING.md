# Contributing


## Linuxfabrik Standards

The following standards apply to all Linuxfabrik repositories.


### Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).


### Issue Tracking

Open issues are tracked on GitHub Issues in the respective repository. In addition to the GitHub default labels (`bug`, `documentation`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`), the following project-specific labels are used:

| Label | Use for |
|---|---|
| `build` | Packaging, build scripts, distribution artifacts. |
| `ci/cd` | Continuous integration, GitHub Actions workflows, release automation, test automation. |
| `dependencies` | Pull requests opened by Dependabot. |
| `github_actions` | Pull requests that update GitHub Actions workflow definitions or pinned action SHAs. |
| `python` | Pull requests that update Python dependencies. |

When opening a new issue, attach the label that matches the area of work. The `build` and `ci/cd` labels mirror the conventional commit scopes used in the same areas (`fix(build): ...`, `chore(ci/cd): ...`).


### Pre-commit

Some repositories use [pre-commit](https://pre-commit.com/) for automated linting and formatting checks. If the repository contains a `.pre-commit-config.yaml`, install [pre-commit](https://pre-commit.com/#install) and configure the hooks after cloning:

```bash
pre-commit install
```


### Commit Messages

Commit messages follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification:

```
<type>(<scope>): <subject>
```

If there is a related issue, append `(fix #N)`:

```
<type>(<scope>): <subject> (fix #N)
```

`<type>` must be one of:

- `chore`: Changes to the build process or auxiliary tools and libraries
- `docs`: Documentation only changes
- `feat`: A new feature
- `fix`: A bug fix
- `perf`: A code change that improves performance
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `style`: Changes that do not affect the meaning of the code (whitespace, formatting, etc.)
- `test`: Adding missing tests


### Changelog

Document all changes in `CHANGELOG.md` following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Sort entries within sections alphabetically.

The audience is a Linux system engineer with 30 seconds to decide whether an update is worth it. Write for that reader:

* **Lead with highlights.** Begin every release section with three to five sentences of running text, directly below the version heading and above the first `###` section. Cover what drives the update decision, including any manual step it requires. No bullet list, no issue links, no repetition of the individual entries. A release with only a handful of entries does not need one, since the entries themselves already fit on a screen.
* **State the change before its scope.** Up to five affected components keep the `component: what changed` form. From six on, put the statement first and close it with either a collective name (`all *-version checks`) or the components in parentheses, so the entry is understood from its first line. These broad entries come first in their subsection, ahead of the alphabetically sorted per-component entries.
* **One sentence per entry.** `Added`, `Changed` and `Fixed` say what an administrator notices. Root cause, reproduction steps and internal reasoning belong in the commit body and the issue.
* **Migration instructions only under `Breaking Changes`.** Wording such as "rename x to y" or "set z to restore the previous behaviour" anywhere else means the entry sits in the wrong section. Entries under `Breaking Changes` may run longer than one sentence.
* **Only what an administrator can observe.** An entry needs a yes to at least one of three questions: does something on a managed host end up different, does the administrator have to change inventory, tags or workflow, does a run that used to succeed now fail or the other way round? A clearer message in front of a failure that happened before as well, a renamed internal variable, or a guard that changes no outcome is not an entry, however much work it was. The commit message carries it. When in doubt, ask whether the line could change anyone's decision to update.
* **Leave out contributor-only changes.** Lockfile and pin bumps, Dependabot and pre-commit configuration, GitHub Actions bumps and test infrastructure are covered by the git history and the pull request. Keep an entry only where an administrator sees the effect, for example when it changes the released artifact.

A release section starts like this:

```markdown
## [v6.1.0] - 2026-09-15

**Highlights:** Two long-standing sources of false alarms are gone, and container workloads are now covered. Cumulative counters are reported as rates instead of totals, so any dashboard built on them has to be re-imported.

### Added
```

The scope rule, on an entry affecting 43 components. Instead of:

```markdown
* about-me, borgbackup, deb-lastactivity, file-ownership, fs-xfs-stats, getent, ...: `--always-ok` to force an OK result
```

write:

```markdown
* `--always-ok` forces an OK result on 43 further components (about-me, borgbackup, deb-lastactivity, ...)
```


### Language

Code, comments, commit messages, and documentation must be written in English.


### CI Supply Chain

GitHub Actions in `.github/workflows/` are pinned by commit SHA, not by tag. Dependabot's `github-actions` ecosystem keeps these pins up to date.

Python packages installed via `pip` inside workflows follow a two-tier policy:

- `pre-commit` is installed from a hash-pinned requirements file at `.github/pre-commit/requirements.txt`, generated with `pip-compile --allow-unsafe --generate-hashes --strip-extras` from `.github/pre-commit/requirements.in`. Dependabot's `pip` ecosystem watches that directory and maintains both files.
- Every other tool a workflow installs with `pip` (`ansible-builder`, `build`, `mkdocs`, `pdoc`, `ruff`, `tox`, ...) follows the same model: a version pin in `.github/<name>/requirements.in`, a hash-pinned `requirements.txt` generated from it the same way, `pip install --require-hashes --requirement .github/<name>/requirements.txt` in the workflow, and a Dependabot `pip` entry for that directory. Dependabot does not read `run:` lines, so a version pinned there (`package==X.Y.Z`) is never updated, and a Scorecard `pipCommand not pinned by hash` finding on it is a real one.


### Coding Conventions

- Sort variables, parameters, lists, and similar items alphabetically where possible.
- Always use long parameters when using shell commands.
- Use RFC [5737](https://datatracker.ietf.org/doc/html/rfc5737), [3849](https://datatracker.ietf.org/doc/html/rfc3849), [7042](https://datatracker.ietf.org/doc/html/rfc7042#section-2.1.1), and [2606](https://datatracker.ietf.org/doc/html/rfc2606) in examples and documentation:
    - IPv4: `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`
    - IPv6: `2001:DB8::/32`
    - MAC: `00-00-5E-00-53-00` through `00-00-5E-00-53-FF` (unicast), `01-00-5E-90-10-00` through `01-00-5E-90-10-FF` (multicast)
    - Domains: `*.example`, `example.com`


---


## Ansible Development Guidelines

To see these concepts in practice, have a look at the [example role](https://github.com/Linuxfabrik/lfops/tree/main/roles/example).


### Style Guide

YAML:

* No `---` at the top of YAML files; it is only required if YAML directives precede it.
* Use the `.yml` extension (consistent with `ansible-galaxy init`).
* Indent YAML with 2 spaces, everything else preferably with 4.
* Use `true` / `false`, not `yes` / `no`.
* Always quote strings, preferably with single quotes. Double quotes only nested within single quotes (e.g. Jinja map reference) or when the string needs escapes (e.g. `\n`).
* For long strings use a folded scalar (`>` converts newlines to spaces, `|` keeps them) without further quoting.
* Do not quote booleans (`true`), numbers (`42`) or octal numbers (`0o755`).
* Put whitespace around Jinja filters: `{{ my_var | d("my_default") }}`.
* Indent list items below their key (`list1:` then `  - item1`). No unindented items, no flow sequences like `[ 'tag1', 'tag2' ]`.

Ansible:

* Keep 2 empty lines before each `- block:`.
* Prefer `item["subkey"]` to `item.subkey`, since that notation always works.
* Use no special characters other than underscores in variable names.
* Name tasks after their respective shell commands, so sysadmins understand what is going on.
* No colon at the end of task names: `- name: 'Combined Users:'` renders as `Combined Users:]`.
* Split long Jinja2 expressions into multiple lines.
* Use `| length > 0` instead of bare `| length` in conditionals; Ansible 2.19+ requires bool, not int.
* Apply `| bool` to bare variables (an expression of just one variable reference), everywhere including module parameters. In a `when:` the string `'false'` is truthy.
* Order module parameters semantically, not alphabetically: target, then action, then ownership and permissions (e.g. `backup`, `src`, `dest`, `owner`, `group`, `mode`). This is an exception to the "sort alphabetically" rule.

Commit scopes:

* Use the role or playbook path as scope, e.g. `fix(roles/graylog_server): prevent warn on receiveBufferSize (fix #341)`.
* The first commit is `feat(roles/<role-name>): add role` or `feat(playbooks/<playbook-name>): add playbook`.
* A commit that adds or changes a Molecule scenario takes the scope of the role or playbook it tests, e.g. `test(roles/apache_tomcat): add install and foreign_tags scenarios`. The bare `extensions/molecule` scope is only for the shared setup no single scenario owns (`config.yml`, shared inventory, provisioning playbooks).


### Deliverables

A new role delivers:

* The role itself.
* `roles/<role-name>/README.md`, following `roles/example/README.md` and "README" below.
* `roles/<role-name>/meta/argument_specs.yml` declaring all user-facing variables.
* Updates to `playbooks/README.md`, `playbooks/all.yml`, `COMPATIBILITY.md` and `CHANGELOG.md`.
* An update to `.ansible-lint-ignore` if the role defines a `__combined_var`.


### OS Coverage

A new or changed role covers the **full operating-system matrix** in [COMPATIBILITY.md](COMPATIBILITY.md) (currently Debian 12 and 13, RHEL 8, 9 and 10, Ubuntu 22.04, 24.04 and 26.04). COMPATIBILITY.md is authoritative; add a column there before supporting a new release.

* Abstract OS differences (package names, paths, unit names, users, ...) into per-OS vars files, see "OS-specific Variables". Reference roles: `sshd`, `clamav`.
* Validate empirically on each family before claiming support: one podman container per OS (e.g. `rockylinux/rockylinux:10`, `debian:13`, `ubuntu:24.04`), systemd-enabled when services are managed.
* Mark a cell `x` only once it is proven to run; `(x)` means "expected to work but not verified".


### Security by Default

A host deployed with LFOps and no further inventory should already be in the state a security review would ask for: where the safe value also works, it is the default, even if upstream ships the permissive one. Document the deviation per "Deviating from an Upstream Default".


### Changelog Sections

The "Changelog" rules above apply, except that entries are sorted newest first, because operators running playbooks need to see what changed most recently.

* Each subsection (`### Added`, ...) appears at most once per release section; append to the existing one.
* Order: `Breaking Changes`, `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`. Omit empty subsections.
* Add new entries at the top of a subsection, even if this results in multiple entries for the same role.


### Playbooks

* Each playbook contains all dependencies to run flawlessly against a newly installed machine.
* Playbooks that install an application together with packages that are complex to configure (`apache_httpd`, `mariadb_server` and/or `php`) are prefixed by `setup_`, e.g. `setup_nextcloud`.
* Name the play `- name: 'Playbook linuxfabrik.lfops.example'`.
* Document a new playbook in `playbooks/README.md` and add it to `playbooks/all.yml`.
* Import `shared/tasks/log-start.yml` and `shared/tasks/global-variables.yml` in `pre_tasks` and `shared/tasks/log-end.yml` in `post_tasks`, tagged `always`, so every run is logged to `/var/log/linuxfabrik-lfops.log` and the LFOps-wide variables are loaded. Copy the frame from `playbooks/example.yml`.


### Roles

* Reading the README must be enough to understand and use a role.
* Idempotency: a second run with the same parameters neither changes nor reports changes, and never damages an existing installation (even without tags), e.g. `create user if not exists` with a `changed_when` / `failed_when` that recognizes the "already exists" error.
* Run without tags, a role delivers a completely installed application.
* Do not over-engineer; the role can grow later.
* One role per software application, supporting all its versions (e.g. PHP 7.1, 7.2, 7.3).
* No role dependencies via `meta/main.yml`; dependencies are handled in playbooks.
* Do not use the general-purpose roles `apps`, `files` and `systemd_unit` as dependent roles (via `__dependent_var`); they are driven from the inventory, and wiring into them over-restricts the playbook order. Do such tasks in the consuming role.
* List inputs are lists of dictionaries with `state: present/absent`, see "Combined Variables".
* Fail loudly. Avoid constructs that suppress errors, like `IfModule` in Apache httpd.
* Do not support EOL software versions.
* For a new application, consider security, monitoring and backups.
* Backups: `duplicity` backs up the fixed list `duplicity__backup_sources__role_var` (`roles/duplicity/defaults/main.yml`). A role storing data outside of it adds the directory there and to `roles/duplicity/README.md`; setup playbooks cannot inject it, since they do not run `duplicity`. Databases are backed up by a dump to `/backup` (see `mariadb_server`, `postgresql_server`, `mongodb`, `influxdb`), never by their live data directory.
* For mailing, use `sendmail`, which is consistent across distros.
* All user-facing information goes into the README; comments are for developers only.
* Avoid breaking changes as far as possible, but don't let them stand in the way of improvements.
* Document all changes in the [CHANGELOG.md](https://github.com/Linuxfabrik/lfops/blob/main/CHANGELOG.md).


#### README

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


#### Tasks

* Always use the FQCN of the module.
* Use meta modules: `ansible.builtin.package` instead of `yum` / `dnf` / `apt`, `ansible.builtin.service` instead of `systemd`.
* Prefer `ansible.builtin.command` (or `ansible.windows.win_command`) over `shell` over `raw`, and `ansible.builtin.template` over `copy`, `lineinfile` or `blockinfile`.
* Pin `ansible.builtin.shell` to `executable: '/bin/bash'` (in `args:` or next to `cmd:`): Debian's `/bin/sh` is `dash`, which rejects `set -o pipefail`, `[[ ... ]]` and `source`. `/bin/bash` resolves with or without usrmerge, `/usr/bin/bash` does not.
* Never `state: 'latest'` with `ansible.builtin.package`, use `state: 'present'`.
* Use `delegate_to: 'localhost'`, never `local_action`.
* Set both `become: false` and `vars: ansible_become: false # noqa var-naming[pattern]` on every task or block delegated to localhost. Play-level `become: true` propagates to delegated tasks, and `ansible_become: true` in the inventory overrides the `become: false` keyword; only the task variable overrides the inventory. Otherwise the task fails with `sudo: a password is required`, or runs as root on the controller. Verified with ansible-core 2.16 and 2.18.
* Avoid `run_once: true`: it evaluates `when` (also that of an enclosing block or include) against the first host only, and if that host skips, every host skips. Let controller-side tasks run per host:
    * `ansible.builtin.get_url` writing a single file is race-safe (temp file plus atomic rename); with a version-pinned `dest` only the first host downloads.
    * Tasks mutating a shared controller path in place (`ansible.builtin.git` into a shared working dir, `command` / `shell` building files under `/tmp`) get `throttle: 1` with a comment `# serialize: ...`.
    * `run_once` stays only for a single read-only lookup shared to all hosts, e.g. a GitHub release API query stored with `set_fact`.
* Download on the controller (`delegate_to: 'localhost'`) and copy to the target: release artifacts, Git checkouts, language packages. Only the controller needs outbound access; say who needs what in "How the Role Behaves". See `roles/example` and "Python dependencies for air-gapped targets".
* Retry every download with `retries: 3` and `delay: 10`: `get_url`, `git`, `rpm_key` with a URL, `uri` lookups such as the GitHub release API, and every `package`, `apt`, `dnf` and `pip` task that installs or updates (not `state: 'absent'`). Since ansible-core 2.16 `retries` without `until` repeats until success. Never retry calls that change something, such as an API `POST`.
* Always give `command` and `shell` tasks `changed_when`, `creates` or `removes`; `changed_when: false` when read-only.
* Prefer `chown -R --changes` over `ansible.builtin.file` with `recurse: true` (slow on large trees), with `changed_when: '<result>["stdout"] | length > 0'`.
* With `ansible.builtin.template`, always set `backup`, `src`, `dest`, `owner`, `group` and `mode`.
* Prefer `ansible.builtin.assert` over `ansible.builtin.fail` with `when`, for consistency.
* Optionally add `ansible.builtin.debug` tasks for `__combined_var` variables.
* Split service `enabled` and `state` into separate tasks, see "Handlers".
* Check `ansible_facts["selinux"]["status"] != "disabled"` before managing SELinux ports, file contexts or booleans.


#### Handlers

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


#### Reboots

A role never reboots the host on its own. It files a request with [schedule_reboot](https://github.com/Linuxfabrik/lfops/tree/main/roles/schedule_reboot), and the host reboots once at its maintenance window, together with every other pending reason. `lfops__reboot_now: true` (as `--extra-vars`, or in `group_vars` for hosts needing no window) makes the role perform it in the same run. It defaults to `false` and is documented once in the [README](./README.md#lfops__reboot_now). Both paths write the same spool file, so both keep the notification mail, the Icinga downtime and the grace period, and coalesce with earlier requests.

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


#### Reporting a Manual Step to the Operator

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

Known limitation: `post_tasks` do not run when the play fails (`--force-handlers` does not help); the inline messages cover that case.


#### Tags

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


#### Variables

* `./vars`: not to be edited by users. `./defaults`: may be overridden in the inventory.
* Document all user-facing variables in the README, formatted as in `roles/example/README.md`.
* No defaults for mandatory variables, and none for secrets (passwords, tokens etc.).
* Software versions are always mandatory, never role defaults: a bumped default silently changes what an existing inventory deploys.
* Naming: `<role name>__<optional: config file>_<setting name>`, e.g. `apache_httpd__server_admin`, reusing config file key names where possible (`redis__conf_maxmemory`).
* Prefix role-internal variables with `__`, e.g. `__example__sysconfig_path`.
* Put large static lists and "magic values" into `vars/main.yml`, not into the playbook.
* Seed random but idempotent values with `inventory_hostname`: `{{ 59 | random(seed=inventory_hostname) }}`.
* Guard optional strings or lists with `is defined and my_var | length > 0`. Bare `is defined` is fine for dict subkeys where presence is the signal and for result attributes.
* Group credentials as subkeys of one dict (e.g. `<role>__login` with `username`, `password`), matching the `linuxfabrik.lfops.bitwarden_item` lookup.
* Use `ansible_facts["os_family"]`, not `ansible_os_family`.


##### Deviating from an Upstream Default

Where a role default differs from what the software ships (as installed from the repository the role uses, which may differ from upstream docs), say so and why. Otherwise the next person either keeps a wrong value or "corrects" a deliberate one.

* Where the value is defined (`defaults/main.yml`, `vars/<version>.yml`, `vars/<os>.yml`), add the value only: `example__conf_max_connections__role_var: 100  # upstream default: 151`.
* In the README, add a last bullet below `Default:` with the reasoning in one sentence, for the administrator. Mention version- or platform-specific defaults there ("MariaDB 11.8 ships it on, older releases ship it off"). The reasoning lives in the README only.

    ```markdown
    * Default: `100`
    * Deviates from the upstream default `151`: each connection reserves its own buffers, and 151 of them exhaust the memory of the 2 GB VMs this role is typically deployed on.
    ```

Keep evidence of upstream defaults in the repository where a role needs it, as `roles/mariadb_server/vars/vendor/` does: a `mariadbd --help --verbose` dump per supported version from a clean installation, package recorded in the header, so `git diff` shows moved defaults.


##### Variable Validation with `argument_specs`

Every role has a `meta/argument_specs.yml` declaring all variables documented in the README, including the `__host_var` / `__group_var` / `__dependent_var` variants, but not `__role_var` and `__combined_var`. `__dependent_var` is required because `setup_*` playbooks pass it via `vars:`; without it, role entry fails with `Supported parameters include: ...`.

* `required: true` for mandatory variables.
* Use `type` and `choices`. For injection variables with an `''` default but another actual type, use `type: 'raw'`.
* Dicts fed by external lookups (e.g. `bitwarden_item`) get `type: 'dict'` without `options:`, since they carry extra keys; document the expected keys in the README.
* Omit `default` when it is a Jinja2 expression, set it when static (`true`, `'started'`, `[]`).
* Sort entries alphabetically.

What `argument_specs` cannot express (ranges, regexes, cross-variable dependencies) goes into `ansible.builtin.assert` in a block tagged `always`. Reference: `roles/example/meta/argument_specs.yml`.


##### Combined Variables

The user overrides *parts* of the role default (`__role_var`) from the inventory (`__host_var` / `__group_var`), and other roles inject defaults via `__dependent_var` (above the role default, below the inventory). Define in `defaults/main.yml`, slots sorted alphabetically; precedence lives in the lazily evaluated expression only:

```yaml
# for list of dictionaries
my_role__my_var__combined_var: '{{ (
      my_role__my_var__role_var +
      my_role__my_var__dependent_var +
      my_role__my_var__group_var +
      my_role__my_var__host_var
    ) | linuxfabrik.lfops.combine_lod
  }}'
my_role__my_var__dependent_var: []
my_role__my_var__group_var: []
my_role__my_var__host_var: []
my_role__my_var__role_var: []

# for simple values like strings, numbers or booleans
my_role__my_var__combined_var: '{{
    my_role__my_var__host_var if (my_role__my_var__host_var | string | length) else
    my_role__my_var__group_var if (my_role__my_var__group_var | string | length) else
    my_role__my_var__dependent_var if (my_role__my_var__dependent_var | string | length) else
    my_role__my_var__role_var
  }}'
my_role__my_var__dependent_var: ''
my_role__my_var__group_var: ''
my_role__my_var__host_var: ''
my_role__my_var__role_var: ''
```

* Always implement a `state` key (default `present`), otherwise the user cannot remove a default element: e.g. the default localhost vHost of `apache_httpd` is removed by setting the same element with `state: 'absent'`. Handle it with `when: 'item["state"] | d("present") == "absent"'` (remove) and `!= "absent"` (create); in templates `{% for item in ... if item['state'] | d('present') != 'absent' %}`. For `ansible.builtin.package`, pass present and absent names as two lists instead of looping (see `roles/php`).
* `combine_lod` merges items on `unique_key` (default `name`); combine several keys where one is not unique, e.g. `combine_lod(unique_key=["conf_server_name", "virtualhost_port"])`. See `ansible-doc --type filter linuxfabrik.lfops.combine_lod`.
* Use lists of dictionaries or simple values, never dictionaries: their key names cannot be templated, which breaks passing values on, especially via `__dependent_var` (<https://docs.linuxfabrik.ch/software/ansible.html#besonderheiten-von-ansible>).
* A simple-value `__combined_var` is always a string; convert it to an integer when needed.


##### `skip_role` Variables in Playbooks

`<playbook>__<role>__skip_role` and `<playbook>__<role>__skip_role_injections` let the user skip a role or its injections, see the [README.md](./README.md#skipping-roles-in-a-playbook). Set two internal variables between `hosts:` and `roles:` and use them:

```yaml
vars:

  setup_icinga2_master__icingaweb2__skip_injections__internal_var: '{{ setup_icinga2_master__icingaweb2__skip_injections | d(setup_icinga2_master__icingaweb2__skip_role__internal_var) }}'
  setup_icinga2_master__icingaweb2__skip_role__internal_var:       '{{ setup_icinga2_master__icingaweb2__skip_role       | d(false) }}'

roles:

  - role: 'linuxfabrik.lfops.icingaweb2'
    when:
      - 'not setup_icinga2_master__icingaweb2__skip_role__internal_var'

  - role: 'linuxfabrik.lfops.icinga2_master'
    # several injections: concatenate, so the list needs no flattening
    icinga2_master__api_users__dependent_var: '{{
        (not setup_icinga2_master__icingadb__skip_injections__internal_var) | ternary(icingadb__icinga2_master__api_users__dependent_var, []) +
        (not setup_icinga2_master__icingaweb2__skip_injections__internal_var) | ternary(icingaweb2__icinga2_master__api_users__dependent_var, [])
      }}'
```


#### Templates

* Always use `ansible.builtin.template`, never `copy`, even without variables: easier to extend, and it allows the header.
* Always set `backup: true` (timestamped copy, e.g. `keycloak.conf.23875.2025-02-14@15:19:16~`).
* Start every template with `# {{ ansible_managed }}` and a `# YYYYMMDDNN` version line (e.g. `# 2021081601`), in the target's comment syntax.
* Never use `{{ template_run_date }}`, it breaks idempotency.
* Mirror the target path below `templates/` (`templates/etc/httpd/sites-available/default.conf.j2`) and always use `.j2`.
* Deploy self-written scripts to `/usr/local/sbin` (SELinux). Helpers run only by a systemd unit (not by an admin, not exec'd by a confined domain) MAY live in `/usr/local/libexec`: as `usr_t`, a root `oneshot` service in `init_t` runs them via `execute_no_trans` without AVC denial on RHEL 8, 9 and 10. Admin-invokable commands stay in `/usr/local/sbin`, and a script a confined domain must exec never goes to `/usr/local/libexec`.
* Keep templates as close to the original file as possible, which eases rpmnew/rpmsave handling.
* If the role picks a file by the installed version (`<version>-<name>.conf.j2`, `vars/<version>.yml`), list the shipped versions in `vars/main.yml` and assert against them right after reading the version, as `roles/example` does (`__example__supported_versions`), so the admin gets the supported versions instead of a missing-file path. Document the abort under `## Troubleshooting` (pin a supported version, or add the file).
* After deploying a file that may get rpmnew / rpmsave files (or Debian equivalents), include `shared` with `tasks_from: 'remove-rpmnew-rpmsave.yml'` and `shared__remove_rpmnew_rpmsave_config_file`, as in `roles/example`.


#### systemd Drop-ins and Service Ordering

* Override units with drop-ins under `/etc/systemd/system/<unit>.d/`, never by templating the unit file. Name them after their purpose (`z00-linuxfabrik.conf` for the role's `[Service]` settings, `z00-after-<dependency>.conf` for ordering) and run `systemctl daemon-reload` when changed.
* For a unit of *another* software, use `z00-<role>.conf` (e.g. `roles/librenms` writes `rrdcached.service.d/z00-librenms.conf`), so the role owning that software does not overwrite it.
* If a role's `<role>__kernel_settings__*__dependent_var` sets a value its service reads only at startup (e.g. `net.core.somaxconn`, applied in `listen()`), add a `z00-after-tuned.conf` with `[Unit]` `After=tuned.service`; otherwise the service may start before TuneD and keep the old value. Continuously honoured values (`vm.swappiness`, `net.bridge.bridge-nf-call-iptables`) need none; decide per parameter.
* Put the ordering into the consuming unit, never a `Before=` list into the dependency: it would need syncing per host and invites ordering cycles, which systemd breaks by silently dropping an edge. Ordering on a missing unit is ignored.
* Ordering drop-ins trigger no restart; they take effect at the next boot.
* `roles/example` implements the chain (`example__kernel_settings__sysctl__dependent_var`, fed into `kernel_settings` by `playbooks/example.yml`, plus the drop-in). `roles/icinga2_agent` shows a non-TuneD case (`z00-after-sssd.conf`).


#### OS-specific Variables

Put values differing by platform (packages, paths, services) into `vars/` files, overriding from least to most specific: `os_family` (`RedHat`), `distribution` (`CentOS`), `distribution_major_version` (`CentOS7`), `distribution_version` (`CentOS7.9`).

* With a `vars/Debian.yml`, always create an explicit `vars/Ubuntu.yml`, even as an identical copy, so Ubuntu stays visible and drift has a home.
* Load them in `tasks/main.yml` by importing `shared` with `tasks_from: 'platform-variables.yml'`, tagged `always` (other roles may reference them).
* `vars/` outrank the inventory, so user-overridable defaults go into `__role_var` (see "Combined Variables") or into an internal `__my_role__my_value` in `vars/<os>.yml`, referenced from `defaults/main.yml` as `my_role__my_value: '{{ __my_role__my_value }}'`.


#### OS-specific Dependent Variables

When a role running *earlier* consumes the value (the `__dependent_var` pattern), `vars/<os>.yml` loads too late. Keep the platform-keyed dictionary internal in the publishing role's `vars/main.yml` (loaded at play parse, visible to every role) and publish a selection via `linuxfabrik.lfops.platform_select`:

```yaml
# roles/mariadb_server/vars/main.yml
__mariadb_server__python__modules__dependent_var:
  Debian:
    - name: 'python3-pymysql'
  RedHat:
    - name: 'python3-PyMySQL'
mariadb_server__python__modules__dependent_var: '{{
    __mariadb_server__python__modules__dependent_var
    | linuxfabrik.lfops.platform_select(ansible_facts, default=[])
  }}'
```

Consumers reference the public variable directly. The filter mirrors `shared/tasks/platform-variables.yml` (least to most specific: `os_family`, `os_family + distribution_major_version`, `os_family + distribution_version`, `distribution`, `distribution + distribution_major_version`, `distribution + distribution_version`); without `default`, an unmatched platform raises an error.

A published `__dependent_var` must be valid on every host, whether or not its role runs there: ansible-core up to 2.18 resolves all variables of an expression, even in an untaken `ternary()` / `if` branch, and `skip_injections: false` uses a skipped role's injection on purpose. So:

* Always pass `default=[]` (or the consumer's empty value) to `platform_select`.
* If the publishing role cannot work without the value, it asserts its supported platforms in its own `always` validation block (reference: `roles/duplicity`).
* Never derive it from a variable the consuming role sets at runtime: a consumer with `argument_specs` templates all parameters at role entry, and one undefined value aborts with `input must be a dict keyed by platform identifier, got AnsibleUndefined`. If unavoidable, publish an empty list until the value exists; the parameter is re-templated on every use:

```yaml
# roles/nextcloud/vars/main.yml
nextcloud__php__modules__dependent_var: '{{
    (__nextcloud__php__modules__dependent_var
      | linuxfabrik.lfops.platform_select(ansible_facts))
    if __php__installed_version is defined else []
  }}'
```


#### LFOps-wide Shared Variables

Platform values shared by many roles (currently the Apache httpd user and group) live once in `roles/shared/vars/<os>.yml`, loaded by `roles/shared/tasks/global-variables.yml` in every playbook's `pre_tasks`. Reference them directly (e.g. `owner: '{{ __shared__apache_httpd_user }}'`), and add new ones there.


#### OS-specific Tasks

Platform-specific tasks go into `tasks/<platform>.yml`; only the most specific match runs, then `main.yml` (a CentOS 7.9 host with `CentOS7.4.yml`, `CentOS7.yml`, `RedHat.yml` runs `CentOS7.yml`). Include them with the `include_tasks` + `first_found` task (`skip: true`) from `roles/example/tasks/main.yml`, which tries `distribution` + `distribution_version`, `distribution` + `distribution_major_version`, `distribution`, then the same for `os_family`. Tag `always` on the `include_tasks` task itself, not on a surrounding block, which would pass the tag on to all included tasks.


### Handling of GPG Keys under Debian (APT Keyring)

`/etc/apt/trusted.gpg.d` trusts a key for all repositories, so `apt-key` and `ansible.builtin.apt_key` are deprecated. Instead:

1. Store the key in `/etc/apt/keyrings/` with the extension matching `file`: `PGP public key block Public-Key (old)` is `.asc`, `OpenPGP Public Key` is `.gpg`.
2. Reference it in `/etc/apt/sources.list.d/`: `deb [signed-by=/etc/apt/keyrings/icinga.asc] https://...`.

References: `roles/repo_icinga/tasks/Debian.yml` (ASCII-armored), `roles/repo_mariadb/tasks/Debian.yml` (binary).


### Roles with Special Features

Unusual techniques and the role to read before reusing them; all other roles follow `roles/example`.


#### Build from source (autotools)

* `libmaxminddb`: GitHub release tarball, `./configure`, `make`, `make check`, `make install`.


#### Custom SELinux policy modules

* `selinux`: compiles inventory-defined `.te` source (`checkmodule`, `semodule_package`, `semodule --install`) and applies modules → booleans / file contexts / ports → restorecon → setenforce, so new types are usable in the same run.
* `php`: publishes `php__selinux__modules__dependent_var` from `vars/main.yml` (several playbooks run `selinux` before `php`), with the source inline in `content_te`, since a role has no controller directory for `src`.

Before adding an `allow` rule, work out what it buys an attacker **on top of** the DAC gates and record it next to the rule: `ptrace_may_access()` and similar run DAC and capability checks before the LSM hook. Example: `lfops_php_fpm_slowlog` in `roles/php/vars/main.yml`.


#### FACL with multi-user / inherited access

* `mirror`: RW for webserver and service user, plus `default:` ACLs for inheritance.


#### Multi-OS coverage (Linux + Windows)

* `monitoring_plugins`: separate `linux-*.yml` and `windows-*.yml` task files.


#### Non-default Jinja2 delimiters

* `telegraf`: `#jinja2:variable_start_string:'[%', variable_end_string:'%]'` in `telegraf.conf.j2` keeps Telegraf's own `{{ ... }}`.


#### Permission management via `find -exec chmod`

* `grav`: four `chmod` passes (files `664`, `bin/` `775`, directories `775`, setgid), `changed_when` from `--changes`.


#### Python dependencies for air-gapped targets

* `monitoring_plugins` installs a hash-pinned lockfile into a venv on a target without PyPI access:
    * The target reports `platform.python_version()` (pip reads a bare `3.9` as 3.9.0, which e.g. cryptography excludes) and `platform.libc_ver()`.
    * The controller runs `pip download --no-deps --require-hashes --implementation cp --python-version <full version>` with one `--platform manylinux_2_<n>_<arch>` per glibc minor from 17 up to the target's plus `manylinux2014_<arch>` (pip does not widen these). `--no-deps` allows pure-Python sdists; their build backend (`setuptools`, `wheel`, ...) is fetched with `--only-binary=:all:` into the same directory.
    * The files go below a root-owned path on the target, never `/tmp`, since pip trusts that directory and its requirements file holds the hashes.
    * `ansible.builtin.pip` with `extra_args: '--no-index --find-links <dir> --require-hashes'` keeps pip offline and syncs an existing venv on every run.


#### Reboot requests

* `bootloader`: see "Reboots".


#### systemd socket activation with an on-demand backend

* `chromium_headless`: a `.socket` unit plus `systemd-socket-proxyd` fronts Chromium on `127.0.0.1`; the proxy exits when idle, and `BindsTo=` starts and stops the backend with it.


#### Other

* `apache_solr`: OpenJDK package per platform and Solr major version via `vars/<platform>.yml` (RHEL 10 and Debian 13 ship no Java 17), asserted per platform; `security.json` hashes computed on the controller with a host- and user-derived salt, so the file only changes with a password.
* `mongodb`: `state: skip` in `mongodb__databases` / `mongodb__users` leaves an entry untouched.
* `moodle`: patch tag discovered via `api.github.com/repos/moodle/moodle/tags`, first match of `^v<configured-version>`.
* `nextcloud`: a state file skips install-only tasks after the initial installation; concise "Tags" README section.
* `php`: present/absent split of `php__modules__combined_var` into two batched package calls.
* `redis`: installed version via `package_facts` selects `<version>-redis.conf.j2`; systemd via unit-file overrides.


### Vendored Plugins

Some plugins are vendored from upstream (local patches, upstream needs a newer ansible-core, or the dependency must ship to the managed node). Keep them in lockstep with upstream; re-sync or drop them when the condition is met.

* `plugins/modules/ipagroup.py`, `ipahbacrule.py`, `ipahostgroup.py`, `ipapwpolicy.py`, `ipasudocmd.py`, `ipasudocmdgroup.py`, `ipasudorule.py`, `ipauser.py`: from <https://github.com/freeipa/ansible-freeipa>, with `--diff` support from PR [#1415](https://github.com/freeipa/ansible-freeipa/pull/1415). Drop when a release contains it; switch to `freeipa.ansible_freeipa.<module>`.
* `plugins/modules/lvm_pv.py`: from community.general (PR [#10070](https://github.com/ansible-collections/community.general/pull/10070), in 11.0.0, which needs ansible-core >= 2.18; LFOps still supports RHEL 8 / Python 3.6). Local patch, keep on re-sync: `from __future__ import annotations` replaced by `from __future__ import absolute_import, division, print_function`. Drop when LFOps requires ansible-core >= 2.18; switch to `community.general.lvm_pv` and update `roles/lvm`.
* `plugins/module_utils/gnupg.py` (with `gnupg.py_LICENSE.txt`): byte-identical [python-gnupg](https://github.com/vsajip/python-gnupg), revision in its `__version__`, used by `gpg_key` on the managed node to avoid a pip install there. Not expected to be dropped; re-sync unmodified.


### Plugins

In-house plugins live in `plugins/{filter,lookup,modules,module_utils}/`.

* Start with the standard Linuxfabrik Python header (copy it from any in-house plugin), followed by `from __future__ import absolute_import, division, print_function` and `__metaclass__ = type`.
* Use single quotes and f-strings (vendored plugins keep their upstream style).
* Carry valid-YAML `DOCUMENTATION` (and `RETURN` / `EXAMPLES` where applicable). A `description` bullet with a colon followed by a space becomes a mapping and breaks `ansible-doc`; rephrase or quote it. Verify with `ansible-doc -t <filter|lookup|module> linuxfabrik.lfops.<name>`; `tests/unit/test_plugin_docs.py` guards this.
* Set `version_added` to the first release, never change it.
* `module_utils` holds shared code. Do not import the Linuxfabrik Python Libraries (`lib`); copy what you need and note the origin.


#### Plugin Tests

Unit tests are **mandatory** for every in-house plugin; a pull request adding or changing a plugin adds or updates its test.

* `tests/unit/` mirrors the plugin tree, `test_<plugin>.py` (e.g. `tests/unit/plugins/filter/test_combine_lod.py`). Plugins with collection-qualified imports are imported via `ansible_collections.linuxfabrik.lfops...`, which `tests/conftest.py` makes resolvable. Assert behavior, not implementation details.
* Controller plugins (`filter/`, `lookup/`) run on the controller's Python (>= 3.10). Managed-node plugins (`modules/`, `module_utils/`) must work down to Python 3.6 (RHEL 8); their tests also run in UBI 8 (`[testenv:py36-target]`), so test code must be valid Python 3.6 too.
* Run with `tox`, `tox -e py311-ansible216`, `tox -f py311` or `pytest tests/unit`, see `tests/README.md`. The `Linuxfabrik: Unit Tests` workflow runs both tiers on every push and pull request.


### Testing

Molecule tests the playbooks (and thereby the roles) in `extensions/molecule`. When you change a role or playbook, update its scenario in the same step: new or changed behaviour into `verify.yml`, changed inputs (renamed or new variables, other defaults) into its `inventory`.

* `<playbook>/` (e.g. `apps/`), optionally with sub-scenarios (`install/`, `remove/`): `converge.yml` runs the playbook, `verify.yml` checks the result, `molecule.yml` (required, may override `config.yml`, e.g. VM vs container), `inventory/` (`hosts.yml` puts shared-inventory hosts into the playbook's group, `group_vars/systems_under_test.yml` holds the variables).
* `config.yml` applies to all scenarios; `default/` is unused but required; `inventory/` is the shared inventory (`hosts.yml` required); `playbooks/` holds the provisioning playbooks.
* `example/` is the fully commented reference scenario; copy it for a new test.


#### Preparing the controller

* **Collection path**: the scenarios import playbooks by FQCN, so symlink the checkout, from the very directory you run `molecule` in: `ln --symbolic --no-target-directory --force "$(pwd)" ~/.ansible/collections/ansible_collections/linuxfabrik/lfops`. For several worktrees see "Running scenarios in parallel".
* **`libvirt` group** membership; VM provisioning does not escalate.
* **Storage pool** in a directory no package owns, not the distribution's `default` pool (package upgrades reset its mode, and a `chmod` rewrites the ACL mask, so the grant decays to `#effective:--x` and `qemu-img` fails with `Permission denied`):

    ```bash
    sudo mkdir --parents /var/lib/libvirt/images-lfops-molecule
    sudo chown "$(id -un):$(id -gn)" /var/lib/libvirt/images-lfops-molecule
    sudo chmod 0751 /var/lib/libvirt/images-lfops-molecule  # qemu only traverses
    # SELinux; restorecon has no long options
    sudo semanage fcontext --add --type virt_image_t '/var/lib/libvirt/images-lfops-molecule(/.*)?'
    sudo restorecon -R -v /var/lib/libvirt/images-lfops-molecule
    sudo virsh pool-define-as lfops-molecule dir --target /var/lib/libvirt/images-lfops-molecule
    sudo virsh pool-autostart lfops-molecule
    sudo virsh pool-start lfops-molecule
    # keeps cached base images replaceable after libvirt chowns them to qemu
    setfacl --default --modify "user:$(id -un):rw" /var/lib/libvirt/images-lfops-molecule
    ```

    `lfops-molecule` is the expected name (`LFOPS_TEST_POOL` selects another). `create` re-fetches a newer rolling `latest` cloud image only while the pool holds no boot disk, so `--destroy=never` keeps images pinned. Delete images from before the `setfacl` once. Never run `virsh pool-build` on it, and keep it outside your home (qemu cannot traverse a `0700` home).
* **libvirt network `default`** (check with `virsh --connect qemu:///system net-list --all`): `sudo virsh net-define /usr/share/libvirt/networks/default.xml`, then `net-autostart default` and `net-start default`. If `virbr0` or `192.168.122.0/24` are taken, define it from a copy edited with `sed --expression="s/name='virbr0'/name='virbr1'/" --expression='s/192\.168\.122\./192.168.123./g'`.


#### Running a scenario

Run `molecule test --scenario-name apps/install` from the repository root with Molecule 26+. Otherwise `config.yml` is not read (or, measured with 25.12, sub-scenario names are not resolved), and the scenario "passes" against an empty inventory.

* `LFOPS_TEST_TARGETS='rocky*'`: comma-separated subset of targets (`localhost` is always included); also scopes `molecule destroy` to rebuild one target, keeping the SSH keypair and inventory of the others.
* `LFOPS_TEST_POOL`: storage pool, default `lfops-molecule`.
* `LFOPS_TEST_ID`: see "Running scenarios in parallel".

`molecule test` destroys the instances at the end, also on failure; `--destroy=never` keeps them for inspection. There is no leading `destroy`, so the next run reuses them. Remove them with `molecule destroy --scenario-name apps/install`.

Whole suite, each scenario independently, skipping `default` and `example` (`bash` and `zsh`):

```bash
failed=()
while IFS= read -r scenario; do
    echo "### ${scenario}"
    molecule test --scenario-name "${scenario}" || failed+=("${scenario}")
done < <(find extensions/molecule -name molecule.yml -printf '%P\n' \
    | sed 's#/molecule.yml$##' \
    | grep --invert-match --extended-regexp '^(default|example(/|$))' \
    | sort)
[ "${#failed[@]}" -eq 0 ] && echo 'All scenarios passed.' || printf 'FAILED: %s\n' "${failed[@]}"
```


#### Running scenarios in parallel

Parallel runs (e.g. two worktrees) need, opt-in:

* **A collection path per worktree**, kept in the shell that runs `molecule` (e.g. `direnv`). Prerun then logs `Found symlinked collection, skipping its installation`; `requirements.yml` collections are installed into the worktree on the first run.

    ```bash
    export ANSIBLE_HOME="$(pwd)/.ansible"
    mkdir --parents "${ANSIBLE_HOME}/collections/ansible_collections/linuxfabrik"
    ln --symbolic --no-target-directory --force "$(pwd)" \
        "${ANSIBLE_HOME}/collections/ansible_collections/linuxfabrik/lfops"
    ```

* **Own instance names** via `LFOPS_TEST_ID='pr248'`: `rocky9-vm` becomes `lfops-molecule-pr248-rocky9-vm` with its own boot disk, so one run's `destroy` does not take the other's VMs. `molecule destroy` only removes instances of the given `LFOPS_TEST_ID`. The pool is shared on purpose.


#### Known Limitations

* `libvirt` group membership is root-equivalent, and owning the pool adds filesystem write access; no reduction over passwordless sudo, only explicit. `qemu:///session` is not usable, since address discovery needs the `default` network of `qemu:///system`.
* Not usable inside an Ansible Execution Environment: provisioning acts on the host's libvirt, podman and pool directory from `localhost`.


#### How a scenario runs

The `test_sequence` in `config.yml`: `dependency` (collections from `requirements.yml`), `create` (VMs or containers), `prepare` (wait, gather facts), `converge`, `verify`, `idempotence` (second run, fails on any change), `verify` again, `destroy`.


#### What to verify

Verify what only the running system can confirm, not the role's steps. An assertion that still passes while the service is dead or misconfigured tests the wrong thing.

* Do not re-check what comes for free: a failing playbook fails `converge`, and `idempotence` checks the second run.
* Do **not** assert that a templated file exists or contains a line, nor make "the package is installed" the goal (a one-line smoke check is fine).
* Do assert that the service runs and is enabled (`ansible.builtin.service_facts`), is reachable (`ansible.builtin.wait_for` or a request), and actually *uses* the configured values: ask it (`ansible.builtin.uri` against an API, or a CLI printing the effective configuration) for the value set in `group_vars`. Also assert end state outside packages and files (users, databases, API objects), or its absence in a removal scenario.


#### Troubleshooting

**Prerun aborts with `ansible_compat.errors.InvalidPrerequisiteError: Command ansible-galaxy collection install -vvv --force /path/to/lfops`**: `galaxy.yml` carries the non-semver `version: main`. Either set `prerun: false` top-level in `config.yml` and install LFOps yourself, or make the collection symlink (under `ANSIBLE_HOME`) resolve to the directory you run `molecule` in.


#### Why libvirt VMs and Podman containers, and not microVMs

libkrun microVMs (`podman run --runtime=krun`) were evaluated and not adopted: `podman exec` into them fails ([crun#2090](https://github.com/containers/crun/issues/2090)), they run libkrun's kernel instead of the distro's, and init images exist only for the Red Hat family. systemd as PID 1 works with `KRUN_INIT_PID1=1`. Revisit if crun#2090 lands.


### Credits

* <https://github.com/whitecloud/ansible-styleguide>
* <https://redhat-cop.github.io/automation-good-practices>
* <https://docs.openstack.org/openstack-ansible/latest/contributors/code-rules.html>
