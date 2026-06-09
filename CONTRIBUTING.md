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


### Language

Code, comments, commit messages, and documentation must be written in English.


### CI Supply Chain

GitHub Actions in `.github/workflows/` are pinned by commit SHA, not by tag. Dependabot's `github-actions` ecosystem keeps these pins up to date.

Python packages installed via `pip` inside workflows follow a two-tier policy:

- `pre-commit` is installed from a hash-pinned requirements file at `.github/pre-commit/requirements.txt`, generated with `pip-compile --generate-hashes --strip-extras` from `.github/pre-commit/requirements.in`. Dependabot's `pip` ecosystem watches that directory and maintains both files.
- One-shot installs such as `ansible-builder`, `build`, `mkdocs`, `pdoc`, and `ruff` in release, docs, or test workflows are version-pinned only (`package==X.Y.Z`) and kept fresh by Dependabot. Scorecard's `pipCommand not pinned by hash` findings for these are considered acceptable risk and may be dismissed.


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

* Do not use `---` at the top of YAML files. It is only required if one specifies YAML directives above it.
* For YAML files, use the `.yml` extension. This is consistent with `ansible-galaxy init`.
* In YAML files, use 2 spaces for indentation. Elsewhere prefer 4 spaces.
* Use `true` / `false` instead of `yes` / `no`, as they are actually part of YAML.
* Always quote strings and prefer single quotes over double quotes. The only time you should use double quotes is when they are nested within single quotes (e.g. Jinja map reference), or when the string requires escaping characters (e.g. using `\n` to represent a newline). Even though strings are the default type for YAML, syntax highlighting looks better when types are set explicitly. It also helps troubleshooting malformed strings.
* If you must write a long string, use the "folded scalar" (`>` converts newlines to spaces, `|` keeps newlines) style and omit all special quoting.
* Do not quote booleans (e.g. `true`/`false`).
* Do not quote numbers (e.g. `42`).
* Do not quote octal numbers (e.g. `0o755`).
* Insert whitespaces around Jinja filters like so: `{{ my_var | d("my_default") }}`.
* Indent list items:

    Do:

    ```yaml
    list1:
      - item1
      - item2
    ```

    Don't:

    ```yaml
    list2:
    - item1
    - item2
    list3: [ 'tag1', 'tag2' ]
    ```

Ansible:

* Keep 2 empty lines before each `- block:`.
* Prefer `item["subkey"]` to `item.subkey`, since that notation always works.
* Do not use special characters other than underscores in variable names.
* Try to name tasks after their respective shell commands. This makes it easy for sysadmins to understand what is going on.
* Do not use colons at the end of task names. `- name: 'Combined Users:'` renders as `Combined Users:]` in the output.
* Split long Jinja2 expressions into multiple lines.
* Always use `| length > 0` instead of bare `| length` in conditionals. Ansible 2.19+ requires conditional results to be bool, not int.
* Use the `| bool` filter when using bare variables (expressions consisting of just one variable reference without any operator). This guards against YAML quoting mistakes where a boolean ends up as a string: in a `when:` clause, the string `'false'` is truthy (non-empty string) and would incorrectly evaluate to true without `| bool`. Applying it consistently — including in module parameters where Ansible's type coercion would handle it — avoids having to think about where it matters.
* Order module parameters semantically, not alphabetically. The general order is: first identify the target, then describe the action, then set ownership and permissions. For example:

    ```yaml
    - name: 'mkdir -p /etc/example'
      ansible.builtin.file:
        path: '/etc/example'
        state: 'directory'
        owner: 'root'
        group: 'root'
        mode: 0o755

    - name: 'Deploy /etc/example/example.conf'
      ansible.builtin.template:
        backup: true
        src: 'etc/example/example.conf.j2'
        dest: '/etc/example/example.conf'
        owner: 'root'
        group: 'root'
        mode: 0o644
    ```

    This is an exception to the general "sort alphabetically" rule, as alphabetical ordering would obscure what the task operates on.

Commit scopes:

* Use the role or playbook path as commit scope:

    ```
    fix(roles/graylog_server): prevent warn on receiveBufferSize (fix #341)
    ```

* For the first commit, use the message `Add roles/<role-name>` or `Add playbooks/<playbook-name>`.


### Deliverables

When creating a new role, make sure to deliver:

* The role itself.
* `roles/<role-name>/README.md`, following `roles/example/README.md` as a template and the section menu under "README" below.
* `roles/<role-name>/meta/argument_specs.yml` declaring all user-facing variables.
* Update `playbooks/README.md`.
* Update `playbooks/all.yml`.
* Update `COMPATIBILITY.md`.
* Update `CHANGELOG.md`.


### OS Coverage

When creating a new role or changing an existing one, pull through the **full operating-system matrix** declared in [COMPATIBILITY.md](COMPATIBILITY.md) (currently Debian 12 and 13, RHEL 8, 9 and 10, and Ubuntu 22.04, 24.04 and 26.04). COMPATIBILITY.md is the authoritative list; support what it lists, and add a column there before supporting a new release.

* Abstract OS differences (package names, configuration paths, service / unit names, users, ...) into per-OS vars files; see "OS-specific Variables" below for the mechanism and the explicit-`vars/Ubuntu.yml` rule. Reference roles: `sshd`, `clamav`.
* Validate empirically on each family before claiming support. Spin up a container per OS (podman, e.g. `rockylinux/rockylinux:10`, `debian:13`, `ubuntu:24.04`) and confirm the role runs end to end. A full systemd run (service enable / start / reload) needs a systemd-enabled container.
* Only mark a cell `x` in COMPATIBILITY.md once it is proven to run; use `(x)` for "expected to work but not verified".


### Changelog

LFOps overrides the project-agnostic "Changelog" rule above (alphabetical sorting): entries are sorted newest first, because operators running playbooks need to see what changed most recently.

* Each subsection (`### Added`, `### Changed`, ...) appears at most once per release section. Never create a duplicate, append to the existing one.
* Order the subsections as `Breaking Changes`, `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`: the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) order, with the LFOps-specific `Breaking Changes` first. Omit subsections with no entries.
* Within a subsection, add new entries at the top (newest first), even if this results in multiple entries for the same role.


### Playbooks

* Each playbook must contain all dependencies to run flawlessly against a newly installed machine.
* Playbooks installing an application together with software packages that are complex to configure (`apache_httpd`, `mariadb_server` and/or `php`) as a dependency are prefixed by `setup_`. Example: `setup_nextcloud` because Nextcloud also needs Apache httpd, MariaDB Server etc.
* The name of the playbook should be `- name: 'Playbook linuxfabrik.lfops.example'`.
* After creating a new playbook, document it in `playbooks/README.md` and add it in the `playbooks/all.yml`.
* Every run of the playbooks should be logged to `/var/log/linuxfabrik-lfops.log`. Include the following code in the playbook for this:

    ```yaml
    pre_tasks:
      - ansible.builtin.import_role:
          name: 'shared'
          tasks_from: 'log-start.yml'
        tags:
          - 'always'

      - ansible.builtin.import_role:
          name: 'shared'
          tasks_from: 'global-variables.yml'
        tags:
          - 'always'

    roles:

      - role: 'example'

    post_tasks:
      - ansible.builtin.import_role:
          name: 'shared'
          tasks_from: 'log-end.yml'
        tags:
          - 'always'
    ```


### Roles

* To understand/use a role, reading the README must be enough.
* Idempotency: Roles should not perform changes when applied a second time to the same system with the same parameters, and they should not report that changes have been done if they have not been done. More importantly, it should not damage an existing installation when applied a second time (even without tags). Example:
    ```yaml
    - name: 'Create new DBA "{{ mariadb_root["user"] }}" after a fresh installation'
      ansible.builtin.command: 'mysql --unbuffered --execute "{{ item }}"'
      loop:
        - 'create user if not exists "{{ mariadb_root["user"] }}"@"%" identified by "{{ mariadb_root.password }}";'
        - 'grant all privileges on *.* to "{{ mariadb_root["user"] }}"@"%" with grant option;'
        - 'flush privileges;'
      register: 'mariadb_new_dba_result'
      changed_when: 'mariadb_new_dba_result["stderr"] is not match("ERROR \d+ \(28000\).*")'
      failed_when: 'mariadb_new_dba_result["rc"] != 0 and mariadb_new_dba_result["stderr"] is not match("ERROR \d+ \(28000\).*")'
    ```
* If a role was run without tags, it should deliver a completely installed application (assuming it installs an application).
* Do not over-engineer the role during the development — it should fulfill its use case, but can grow and be improved on later.
* There should be one role per software application. If there are multiple versions of the software, e.g. PHP 7.1, 7.2, 7.3, etc., they all should be supported by a single role.
* Do not use role dependencies via `meta/main.yml`. Dependencies are handled in playbooks.
* Do not use the general-purpose roles `apps`, `files`, and `systemd_unit` as dependent roles (via `__dependent_var`). They are meant to be driven directly by the user from the inventory; wiring dependencies into them makes the order in which playbooks can run overly restrictive. Perform such tasks in the consuming role directly instead.
* Whenever the role requires a list as an input, use a list of dictionaries with `state: present/absent`. See "Combined Variables" below.
* Fail loudly. Avoid constructs that could suppress error messages, like `IfModule` in Apache HTTPd. This makes debugging and troubleshooting a lot easier.
* Do not support software versions that are EOL.
* When implementing a role for a new application, consider security, monitoring and backups.
* For mailing, use the `sendmail` utility, as it provides a consistent interface across distros.
* All user-facing information should be included in the README. Comments are intended for developers only.
* Avoid breaking changes as far as possible, but don't let them stand in the way of improvements.
* Document all changes in the [CHANGELOG.md](https://github.com/Linuxfabrik/lfops/blob/main/CHANGELOG.md) file.


#### README

`roles/example/README.md` is the canonical template. Keep the following sections in this order, drop the optional ones that do not apply, and do not invent new top-level sections:

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

* **`*Available since LFOps`**: marks the LFOps release in which the role first shipped. Set it once and never change it afterwards. When you add a new role you do not know the next version tag yet, so write the literal line `*Available in the next LFOps release.*` instead; it is rewritten to the real version with `sed` when the next release is cut.
* **How the Role Behaves**: proactive, non-obvious design/runtime notes (controller-vs-target download split and who needs network access, idempotency / overwrite-on-rerun, the upgrade path, what the role does NOT do, security caveats). Distinct from Troubleshooting (reactive error->fix) and Known Limitations (hard constraints the operator cannot work around).
* **Dependent Roles vs Requirements**: these answer "which other LFOps roles does the playbook wire in" vs "what must the operator provide themselves". Decide where an item goes by what it is:
    * Another LFOps role that **this role's own playbook** (`X.yml`, or a bundling `setup_X.yml`) runs goes under `## Dependent Roles`. Write each bullet declaratively as a state ("The X repository must be enabled (role: ...)") and name the role. Roles run by default form the first list, right under the lead-in ("Any LFOps playbook that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables."); mark feature-optional ones with "Optional:". Roles the playbook ships but leaves off by default go under a "These roles are not enabled by default; enable them via the playbook's skip variables if needed:" list-title. Do not list skip-variable names or the exact play order - those live solely in `playbooks/README.md`.
    * A value the user supplies is a variable: document it under `## ... Role Variables` only, never as a dependency or requirement.
    * Everything else the operator must provide goes under `## Requirements`: host resources, an external account or subscription, or credentials as plain bullets; hands-on procedures (run a SEPARATE playbook for a dependency, mint a token in a web console, install on the Ansible controller, configure DNS) under a "Manual steps:" list-title, written imperatively. A dependency that needs a separate playbook is a manual step here, not a dependent role. Mark feature-optional items with "Optional:".
* **Variable subgroups**: large roles MAY split optional (or mandatory) variables into `## Optional Role Variables - <Subgroup>` sections, using the upstream module name, the variable prefix as a code span, or a functional label. These are the same canonical section repeated; give each its own `Example:` block. A subgroup MAY keep its Mandatory and Optional sections paired together (group-by-module, as in `apache_httpd`) instead of forcing all mandatory subgroups before all optional ones. A variable grouping must always be its own `##` section, never a `###` subheading inside `## Optional Role Variables`.
* **Subheadings and walkthroughs**: `###` subheadings are allowed only as sub-structure inside a section (e.g. procedural steps within a walkthrough), never as a stand-in for a variable subgroup. The walkthrough slot accepts a descriptive role-specific title when none of `Single-Node Setup` / `Cluster Setup` / `Adding a Node to an Existing Cluster` fits (e.g. `bind` `## Primary-Secondary Example`). Sections are separated by two blank lines, including above and below the `*Available since*` marker.
* **Special roles**: utility/meta roles (e.g. `shared`) MAY replace `## Tags` and the `## *Role Variables` sections with `## Available Tasks` and `## Usage Example`. Controller-side API roles (e.g. `uptimerobot`) MAY add `## Running the Role`, `## Example Inventory` and `## Read-Only Inspection`. Both MUST keep the mandatory frame (title, marker, License, Author Information).
* **Reference-grade sections**: a role MAY add a focused role-specific section where no canonical section fits (e.g. `monitoring_plugins` `## Installation Methods`, `keycloak` `## Using a reverse proxy`). Keep these to a minimum; prefer folding behaviour notes into `## How the Role Behaves` and error/fix notes into `## Troubleshooting`.


#### Tasks

* Always use the FQCN of the module.
* Always use meta modules wherever possible:
    * `ansible.builtin.package` instead of `ansible.builtin.yum`, `ansible.builtin.dnf` or `ansible.builtin.apt`
    * `ansible.builtin.service` instead of `ansible.builtin.systemd`
* Use the following modules in preference to their alternatives:
    * `ansible.builtin.command` or `ansible.windows.win_command` over `ansible.builtin.shell` over `ansible.builtin.raw`
    * `ansible.builtin.template` over `ansible.builtin.copy`, `ansible.builtin.lineinfile` or `ansible.builtin.blockinfile`. Templating the whole file leads to more consistent, deterministic, and expected results.
* Do not use `state: 'latest'` for the `ansible.builtin.package` module as this is not idempotent. Always use `state: 'present'`.
* Always use `delegate_to: 'localhost'` instead of `local_action`.
* Always set `become: false` on every task delegated to localhost. When a play sets `become: true` at the play level (not typical for lfops, but useful if others import our roles in their playbooks), it propagates to delegated tasks too and tries to escalate via sudo on the Ansible controller. On a controller without passwordless sudo this fails with `sudo: a password is required`, even though the delegated task only writes to `/tmp` or hits a remote API and does not need root locally. Example:

    ```yaml
    - name: 'curl --output /tmp/ansible.example.tar.gz https://example.com/releases/example.tar.gz'
      ansible.builtin.get_url:
        url: 'https://example.com/releases/example.tar.gz'
        dest: '/tmp/ansible.example.tar.gz'
        mode: 0o644
      delegate_to: 'localhost'
      become: false
      changed_when: false # not an actual config change on the target
      check_mode: false # run task even if `--check` is specified
    ```

* Avoid `run_once: true`. It binds the task to the first host of the batch and evaluates the task's `when` (including an enclosing `block:` `when` or a conditional role/task include) against that host only. If the first host skips, the task is skipped for every host, even hosts that needed it. The usual case is a controller-side download or build delegated to localhost: drop `run_once` and let the task run per host.

    * For `ansible.builtin.get_url` writing a single file this is already race-safe and effectively runs once: the module downloads to a unique temp file and atomically renames it into the shared `/tmp` destination, and with a version-pinned `dest` the first host downloads while the rest find the file present. Nothing else is needed.
    * For tasks that mutate a shared path on the controller in place (`ansible.builtin.git` into a shared working dir, `ansible.builtin.shell`/`ansible.builtin.command` that build or flatten files under `/tmp`), running per host in parallel races across `forks`. Drop `run_once` and add `throttle: 1` so the task still runs per host (no first-host-skip) but only one host at a time touches the shared path:

        ```yaml
        - name: 'Clone the example git repo to localhost'
          ansible.builtin.git:
            repo: 'https://github.com/Linuxfabrik/example.git'
            dest: '/tmp/ansible.example-repo'
            depth: 1
          delegate_to: 'localhost'
          become: false
          throttle: 1 # serialize: shared git working dir on the controller, avoid races between hosts
          check_mode: false # run task even if `--check` is specified
        ```

    * Two cases legitimately keep `run_once`. First, a single read-only lookup whose result is shared to all hosts (e.g. querying a GitHub release API once and storing the version with `set_fact`); running it per host would only multiply API calls and risk rate limiting, and there is no shared-path race. Second, a task whose `when` is deliberately computed across `ansible_play_hosts_all` (not against the first host), so the first-host-skip problem does not apply (see `roles/firewall/tasks/main.yml`).

* Always provide `changed_when`, `creates`, or `removes` for `ansible.builtin.command` and `ansible.builtin.shell` tasks to ensure idempotency. Use `changed_when: false` for read-only commands.
* Prefer a `chown -R --changes` command over `ansible.builtin.file` with `recurse: true`; the module's recursive mode is slow on large trees. Register the result and derive `changed_when` from the `--changes` output for idempotency:

    ```yaml
    - name: 'chown -R --changes apache:apache {{ wordpress__install_dir | quote }}'
      ansible.builtin.command: 'chown -R --changes apache:apache {{ wordpress__install_dir | quote }}'
      register: '__wordpress__chown_result'
      changed_when: '__wordpress__chown_result["stdout"] | length > 0'
    ```
* When deploying files with `ansible.builtin.template`, always set `backup`, `src`, `dest`, `owner`, `group`, and `mode`.
* Prefer `ansible.builtin.assert` over `ansible.builtin.fail` with `when` for validation checks. There is basically no technical difference; this guideline is only for consistency.
* Optionally add `ansible.builtin.debug` tasks for `__combined_var` variables so the user can see what the role will do.
* Split the service `enabled` and `state` into separate tasks. This is relevant for handlers that would restart the service, see "Handlers" below.
* Always check if SELinux is enabled before managing ports, file contexts, or booleans:

    ```yaml
    - name: 'semanage port --add --type example_port_t --proto tcp 8080'
      community.general.seport:
        ports: 8080
        proto: 'tcp'
        setype: 'example_port_t'
        state: 'present'
      when:
        - 'ansible_facts["selinux"]["status"] != "disabled"'
    ```


#### Handlers

* Use handlers in favor to `some_result is changed` if no `meta: flush_handlers` is required or if it would prevent duplicate code.
* Since handlers are global, prefix them with the role name to make sure the correct one is used.
* Use chained handlers (notify) when a validation step should precede the actual action, e.g. a config validation handler that notifies a restart handler.
* Handlers that restart or reload a service should skip execution when the service was just started (redundant) or when the user wants it stopped. For this, the result of the service state task has to be registered and checked. Example:

    ```yaml
    - name: 'example: restart example'
      ansible.builtin.service:
        name: 'example'
        state: 'restarted'
      when:
        - '__example__service_state_result is not changed'
        - 'example__service_state != "stopped"'
    ```


#### Tags

* Naming scheme: `role_name` and `role_name:section`. For example `apache_httpd` and `apache_httpd:vhosts`.
* The role should only do what one expects from the tag name. For example, the `mariadb:users` tag only manages MariaDB users.
* The README of a role should provide a list of the available tags and what they do.
* The tags should be set in the role itself. Do not set them in the playbook.
* Blocks/tasks that install base packages do not require tags such as `apache:pkgs`, `apache:setup` or `apache:install`. There is no real world scenario where it makes sense to only run the installation via Ansible, some configuration is always required.
* For each task, consider to which areas it belongs. A task will usually have multiple tags.
* Reuse a section name from the controlled vocabulary below whenever one fits, so that `--tags` / `--skip-tags` behave the same way across roles. Only invent a role-specific section name (e.g. `apache_httpd:vhosts`, `mariadb_server:galera_new_cluster`) when a task covers an area that none of the standard names describe.

Controlled vocabulary of standard `role_name:section` tags (alphabetical):

* `role_name:certs`: Deploys and renews the role's TLS certificates and private keys.
* `role_name:configure`: Renders and deploys the role's configuration files and applies settings. The most common section; everything that is neither install, state, nor one of the more specific sections below belongs here.
* `role_name:containers`: Manages the role's containers and their systemd container units.
* `role_name:cron`: Deploys the role's scheduled jobs (cron entries or systemd timers).
* `role_name:databases`: Creates, updates and deletes the databases managed by the role.
* `role_name:dump`: Sets up scheduled dumps / backups of the role's data.
* `role_name:enroll`: Registers (enrolls) the node with a remote service or controller.
* `role_name:firewalls`: Manages the cloud provider firewall / security-group rules (VM provisioning roles).
* `role_name:logrotate`: Deploys the role's logrotate configuration.
* `role_name:modules`: Installs, enables and removes the role's pluggable modules (e.g. PHP, SELinux, Apache modules).
* `role_name:networks`: Manages the role's networks (cloud VM, libvirt or container networks).
* `role_name:plugins`: Installs and removes the role's optional application plugins / add-ons (distinct from OS-level `:modules`; e.g. Grafana or CMS plugins).
* `role_name:remove`: Uninstalls the managed software and removes its artifacts.
* `role_name:state`: Manages the runtime state of the role's services, timers and sockets (start / stop / enable / disable).
* `role_name:update`: Updates the managed application to a newer version.
* `role_name:upgrade`: Runs the post-update migration / upgrade steps after the package itself was updated.
* `role_name:users`: Creates, updates and deletes the application or service user accounts managed by the role.

The Ansible built-in tags `always` and `never` are reserved for their built-in meaning: tag the platform-variable loading and `assert` validation tasks with `always` so the variables and checks are present even when the role runs with a specific `--tags` selection.


#### Variables

* `./vars`: Variables that are not to be edited by users.
* `./defaults`: Default variables for the role, might be overridden by the user in the inventory.
* Document all user-facing variables in the README. Have a look at `roles/example/README.md` for the format.
* Do not set defaults for mandatory variables.
* Software versions must always be mandatory variables, never role defaults. A default version drifts: bumping it in the role silently changes what an existing inventory deploys, effectively a breaking change on every bump. Forcing the user to pin the version keeps inventory and the deployed state consistent.
* Naming scheme: `<role name>__<optional: config file>_<setting name>`, for example `apache_httpd__server_admin`.
* No need to invent new names, use the key-names from the config file (if possible), for example `redis__conf_maxmemory`.
* Prefix role-internal variables with `__`, for example `__example__sysconfig_path`. This makes it easy to determine which variables are user-facing and therefore should be in the README.
* Avoid embedding large lists or "magic values" directly into the playbook. Such static lists should be placed into the `vars/main.yml` file and named appropriately.
* If you need random but predictable/idempotent values, use the `inventory_hostname` as seed. Example for setting the minutes of an hour: `{{ 59 | random(seed=inventory_hostname) }}`.
* When guarding optional role variables (strings or lists) that may be undefined, use `is defined and my_var | length > 0`. This catches both undefined variables and empty values (e.g. `my_var: ''`). Bare `is defined` is fine for dict subkeys where presence alone is the signal (e.g. `item["cidr"] is defined`) or for result attributes (e.g. `result["failed"] is defined`).
* Any secrets (passwords, tokens etc.) should not be provided with default values in the role. It is important for a secure-by-default implementation to ensure that an environment is not vulnerable due to the production use of default secrets. Users must be forced to properly provide their own secret variable values.
* Group credentials as subkeys of a single dictionary variable (e.g. `<role>__login` with `username` and `password` subkeys) rather than as separate top-level variables. This integrates cleanly with the `linuxfabrik.lfops.bitwarden_item` lookup, which returns the whole item as one dict.
* Always use the `ansible_facts` dictionary (e.g. `ansible_facts["os_family"]` instead of `ansible_os_family`). The old pre-2.5 "facts injected as separate variables" naming system will be deprecated in a future release of Ansible.


##### Variable Validation with `argument_specs`

Every role should include a `meta/argument_specs.yml` that declares all user-facing variables with their types. Ansible validates these automatically at role entry (before any tasks run), catching type mismatches and missing required variables without manual assert code.

Include all variables documented in the README: mandatory variables, simple optional variables, and the `__host_var`/`__group_var`/`__dependent_var` variants of injection variables. Do not include the purely internal `__role_var` and `__combined_var` slots. `__dependent_var` must be declared even though it is conceptually internal, because `setup_*` playbooks pass it into the role via `vars:` and Ansible validates role-vars against `argument_specs`. Omitting it causes `Supported parameters include: ...` errors at role entry.

Guidelines for `argument_specs`:

* Use `required: true` for mandatory variables (replaces manual `assert` + `is defined` checks).
* Use `type` and `choices` where applicable. For injection variables where the default is `''` (empty string) but the actual value is a different type (e.g. int), use `type: 'raw'` to avoid rejecting the empty default.
* For dict variables fed by external lookups (e.g. `linuxfabrik.lfops.bitwarden_item`), declare `type: 'dict'` without `options:`. The lookup returns the full Bitwarden item with extra keys (`id`, `notes`, `fields`, ...), and a strict sub-option spec would reject them. Document the expected keys in the role's README instead.
* Omit `default` when the default in `defaults/main.yml` is a Jinja2 expression (e.g. `'{{ __example__conf_worker_threads }}'`), as `argument_specs` cannot evaluate it.
* Set `default` when it is a static value (e.g. `true`, `'started'`, `[]`).
* Sort entries alphabetically.

Use `ansible.builtin.assert` in the tasks for validations that `argument_specs` cannot express: value ranges, regex patterns, or cross-variable dependencies. Tag the assert block with `always` so it runs even when other roles reference the validated variables.

Have a look at the `example` role's `meta/argument_specs.yml` for a complete reference.


##### Combined Variables

The goal of combined variables is that variables can be set in multiple places, and then merged in order to be used in the role. For example, the user can overwrite *parts* of the role's default (`__role_var`) from their inventory (`__host_var` / `__group_var`).

Furthermore, other roles can also inject their sensible defaults via the `__dependent_var`, with a higher precedence than the role defaults, but lower than the user's inventory.

To enable this behavior, you must define the `__combined_var` in the `defaults/main.yml` as follows:
```yaml
# for list of dictionaries
my_role__my_var__dependent_var: []
my_role__my_var__group_var: []
my_role__my_var__host_var: []
my_role__my_var__role_var: []
my_role__my_var__combined_var: '{{ (
      my_role__my_var__role_var +
      my_role__my_var__dependent_var +
      my_role__my_var__group_var +
      my_role__my_var__host_var
    ) | linuxfabrik.lfops.combine_lod
  }}'

# for simple values like strings, numbers or booleans
my_role__my_var__dependent_var: ''
my_role__my_var__group_var: ''
my_role__my_var__host_var: ''
my_role__my_var__role_var: ''
my_role__my_var__combined_var: '{{
    my_role__my_var__host_var if (my_role__my_var__host_var | string | length) else
    my_role__my_var__group_var if (my_role__my_var__group_var | string | length) else
    my_role__my_var__dependent_var if (my_role__my_var__dependent_var | string | length) else
    my_role__my_var__role_var
  }}'
```

The `__combined_var` will then be used in the tasks or templates of the role.

The role must always implement some sort of `state` key, otherwise the user cannot unset a value defined in the defaults. Suppose the user wants to disable the default localhost vHost of the Apache HTTPd role:
```yaml
# defaults/main.yml
apache_httpd__vhosts__role_var:
  - conf_server_name: 'localhost'
    virtualhost_port: 80
    template: 'localhost'
```

Without the `state` key, the user has no way of achieving this, as they cannot remove previously defined elements from the list via the inventory. With the `state` key, the role knows it has to remove the vHost:
```yaml
# inventory
apache_httpd__vhosts__role_var:
  - conf_server_name: 'localhost'
    virtualhost_port: 80
    state: 'absent'
```

The handling of the state in the role should look something like this, assuming the default value for `state` is `present`:
```yaml
- name: 'Remove sites-available vHosts'
  ansible.builtin.file:
    path: '...'
    state: 'absent'
  loop: '{{ apache_httpd__vhosts__combined_var }}'
  loop_control:
    label: '{{ item["name"] }}'
  when:
    - 'item["state"] | d("present") == "absent"'

- name: 'Create sites-available vHosts'
  ansible.builtin.template:
    src: '...'
    dest: '...'
  loop: '{{ apache_httpd__vhosts__combined_var }}'
  loop_control:
    label: '{{ item["name"] }}'
  when:
    - 'item["state"] | d("present") != "absent"'
```

Other times it is useful to generate a list of present and absent elements, for example when using `ansible.builtin.package`, as providing the packages as a list is much faster than looping through them.
```yaml
- name: 'Ensure PHP modules are absent'
  ansible.builtin.package:
    name: '{{ php__modules__combined_var | selectattr("state", "defined") | selectattr("state", "eq", "absent") | map(attribute="name") }}'
    state: 'absent'

- name: 'Ensure PHP modules are present'
  ansible.builtin.package:
    name: '{{ (php__modules__combined_var | selectattr("state", "defined") | selectattr("state", "ne", "absent") | map(attribute="name"))
        + (php__modules__combined_var | selectattr("state", "undefined") | map(attribute="name")) }}'
    state: 'present'
```

Or in a Jinja2 template:
```
{% for item in apache_tomcat__roles__combined_var if item['state'] | d('present') != 'absent' %}
<role rolename="{{ item['name'] }}"/>
{% endfor %}
```

The vHost example above can be used to demonstrate another feature of `linuxfabrik.lfops.combine_lod`. Normally, the list items are combined based on a `unique_key` that should match, for example, the `name` key. However, this does not work with `conf_server_name` because you can have a vHost with the same `conf_server_name` for multiple ports. This means that the `unique_key` must be a *combination* of `conf_server_name` and `virtualhost_port`:
```yaml
apache_httpd__vhosts__combined_var: '{{ (
      apache_httpd__vhosts__role_var +
      apache_httpd__vhosts__dependent_var +
      apache_httpd__vhosts__group_var +
      apache_httpd__vhosts__host_var
    ) | linuxfabrik.lfops.combine_lod(unique_key=["conf_server_name", "virtualhost_port"])
  }}'
```

Note:

* Have a look at `ansible-doc --type filter linuxfabrik.lfops.combine_lod`.
* Always use lists of dictionaries or simple values. Never use dictionaries directly, even though they allow overwriting of earlier elements, since one cannot template the keyname using Jinja2. This would prevent passing on of variables, especially in `__dependent_var` (for details have a look at <https://docs.linuxfabrik.ch/software/ansible.html#besonderheiten-von-ansible>).
* Simple value `__combined_var` are always returned as strings. Convert them to integers when needed.


##### `skip_role` Variables in Playbooks

The `playbook_name__role_name__skip_role` and `playbook_name__role_name__skip_role_injections` variables should provide the user an option to skip the role and the role's injections respectively. Have a look at the [README.md](./README.md#skipping-roles-in-a-playbook).

For this, we need to set the following two internal variables at the top of the playbook (between the `hosts:` and `roles:`):

```yaml
vars:

  setup_icinga2_master__icingaweb2__skip_injections__internal_var: '{{ setup_icinga2_master__icingaweb2__skip_injections | d(setup_icinga2_master__icingaweb2__skip_role__internal_var) }}'
  setup_icinga2_master__icingaweb2__skip_role__internal_var:       '{{ setup_icinga2_master__icingaweb2__skip_role       | d(false) }}'
```

Then use them with the roles as follows:

```yaml
- role: 'linuxfabrik.lfops.icingaweb2'
  when:
    - 'not setup_icinga2_master__icingaweb2__skip_role__internal_var'

- role: 'linuxfabrik.lfops.mariadb_server'
  mariadb_server__databases__dependent_var: '{{
      (not setup_icinga2_master__icingaweb2__skip_injections__internal_var) | ternary(icingaweb2__mariadb_server__databases__dependent_var, [])
    }}'
  mariadb_server__users__dependent_var: '{{
      (not setup_icinga2_master__icingaweb2__skip_injections__internal_var) | ternary(icingaweb2__mariadb_server__users__dependent_var, []) +
    }}'
```

Make sure to use the following format when passing multiple injections to avoid needing to flatten the list:

```yaml
- role: 'linuxfabrik.lfops.icinga2_master'
  icinga2_master__api_users__dependent_var: '{{
      (not setup_icinga2_master__icingadb__skip_injections__internal_var) | ternary(icingadb__icinga2_master__api_users__dependent_var, []) +
      (not setup_icinga2_master__icingaweb2_module_director__skip_injections__internal_var) | ternary(icingaweb2_module_director__icinga2_master__api_users__dependent_var, []) +
      (not setup_icinga2_master__icingaweb2__skip_injections__internal_var) | ternary(icingaweb2__icinga2_master__api_users__dependent_var, [])
    }}'
```


#### Templates

* Always use the `ansible.builtin.template` module instead of the `ansible.builtin.copy` module, even if there are currently no variables in the file. This makes it easier to extend later on, and allows the usage of an automatically generated header.
* Always create a backup file including the timestamp information (e.g. `keycloak.conf.23875.2025-02-14@15:19:16~`) so you can get the original file back if you somehow clobbered it incorrectly, by using `backup: true`.
* Always add the following to the top of templates, using the appropriate comment syntax:
    ```
    # {{ ansible_managed }}
    # 2021081601
    ```
* Do not use `{{ template_run_date }}` inside the template. It is the date that the template was rendered, which is done during every Ansible run. This means that the task will always be changed, even if nothing else changed in the template, therefore breaking idempotency.
* Use the target path for the file in the `template` folder, for example: `templates/etc/httpd/sites-available/default.conf.j2`. This makes it clear what the file is for, and avoids name collisions.
* Always use the `.j2` file extension for files in the `template` folder.
* If deploying self-written scripts, copy them to `/usr/local/sbin` (due to SELinux).
* Keep templates as close to the original file as possible. This makes handling of rpmnew/rpmsave files easier.
* Add the following task after deploying a file that might get rpmnew or rpmsave files (or their Debian equivalents):
    ```yaml
    - name: 'Remove rpmnew / rpmsave (and Debian equivalents)'
      ansible.builtin.include_role:
        name: 'shared'
        tasks_from: 'remove-rpmnew-rpmsave.yml'
      vars:
        shared__remove_rpmnew_rpmsave_config_file: '{{ item }}'
      loop: '{{ repo_epel__repo_files }}'
    ```


#### OS-specific Variables

If some variables need to be parameterized according to distribution and version (name of packages, configuration file paths, names of services), use OS-specific vars-files inside the `vars/` of your role.

Variables with the same name are overridden by the files in `vars/` in order from least specific to most specific:

* `os_family` covers a group of closely related platforms (e.g. `RedHat` covers `RHEL`, `CentOS`, `Fedora`)
* `distribution` (e.g. `CentOS`) is more specific than os_family
* `distribution_major_version` (e.g. `CentOS7`) is more specific than distribution
* `distribution_version` (e.g. `CentOS7.9`) is the most specific

When a role has a `vars/Debian.yml`, always create an explicit `vars/Ubuntu.yml` too, even if it is currently an identical copy. Ubuntu (a `distribution`) is loaded on top of its `Debian` os_family, so a full copy is redundant today, but it keeps Ubuntu visible at a glance and gives later Ubuntu-specific drift a dedicated home instead of silently inheriting Debian values.

To load the variables include the `platform-variables.yml` in the `tasks/main.yml` like this:
```yaml
- name: 'Set platform/version specific variables'
  ansible.builtin.import_role:
    name: 'shared'
    tasks_from: 'platform-variables.yml'
  tags:
    - 'always'
```

Use the `always` tag so the variables are available even when running with a specific tag — other roles in the playbook may reference these variables.

Note that since `vars/` are higher up in the [Ansible variable precedence](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence) than inventory variables we cannot directly define our defaults there. Instead, we either need to use the `my_role__my_var__role_var` (as these already support overwriting of `role_vars`; see "Combined Variables") or to define an internal variable (prefixed with `__`) in the `vars/` file:

```yaml
__my_role__my_simple_value: 'os-dependant default'
```

Then, in `defaults/main.yml`, we reference that internal variable as our public default:

```yaml
my_role__my_simple_value: '{{ __my_role__my_simple_value }}'
```

This allows the user to overwrite `my_role__my_simple_value` in their inventory.


#### OS-specific Dependent Variables

A variant of the OS-specific Variables pattern applies when the value has to be consumed by a *different* role that runs *earlier* in the same play (the `__dependent_var` pattern, see "Combined Variables"). `vars/<os>.yml` files cannot be used there because they are loaded only when the publishing role's tasks run, which is too late for an earlier consumer. Instead, in the publishing role's `vars/main.yml`, keep the OS-specific dictionary as a role-internal (`__`-prefixed) variable and expose a public variable that selects from it with the `linuxfabrik.lfops.platform_select` filter:

```yaml
# roles/mariadb_server/vars/main.yml
__mariadb_server__python__modules__dependent_var:
  Debian:
    - name: 'python3-pymysql'
  RedHat:
    - name: 'python3-PyMySQL'
mariadb_server__python__modules__dependent_var: '{{
    __mariadb_server__python__modules__dependent_var
    | linuxfabrik.lfops.platform_select(ansible_facts)
  }}'
```

`vars/main.yml` is auto-loaded at play parse, visible to every role in the play, and non-overridable from inventory like other `vars/`. Jinja evaluation is lazy, so the filter only runs when a consumer actually references the public variable.

Consumers stay simple - they reference the public variable directly, with no awareness of the selection mechanism:

```yaml
- role: 'linuxfabrik.lfops.python'
  python__modules__dependent_var: '{{ mariadb_server__python__modules__dependent_var }}'

- role: 'linuxfabrik.lfops.mariadb_server'
```

The filter mirrors the precedence of `shared/tasks/platform-variables.yml` (least to most specific: `os_family`, `os_family + distribution_major_version`, `os_family + distribution_version`, `distribution`, `distribution + distribution_major_version`, `distribution + distribution_version`) and returns the value of the most specific present key. Pass `default=[]` (or whatever the consumer expects) when the value is optional on platforms not listed in the dict; otherwise an unmatched call raises an error.


#### LFOps-wide Shared Variables

A small set of platform values is identical across many roles (currently the Apache httpd user and group). To avoid repeating these in every role's `vars/<os>.yml`, they live once in `roles/shared/vars/<os>.yml` and are loaded into every playbook by `roles/shared/tasks/global-variables.yml`, imported from each playbook's `pre_tasks` next to `log-start.yml`. They are then available to every role in the play. The available variables can be found at `roles/shared/vars/<os>.yml`.

Reference them directly in tasks, templates, and `defaults/main.yml`, for example:

```yaml
- name: 'Deploy /etc/example/example.conf'
  ansible.builtin.template:
    backup: true
    src: 'etc/example/example.conf.j2'
    dest: '/etc/example/example.conf'
    owner: '{{ __shared__apache_httpd_user }}'
    group: '{{ __shared__apache_httpd_group }}'
    mode: 0o644
```

When adding a new LFOps-wide platform value, define it in `roles/shared/vars/<os>.yml` and it becomes available to every role.


#### OS-specific Tasks

In order to run only certain tasks based on the operating system platform, files need to be placed in `tasks/` with the filename of the supported "os family".

Assume you have the following OS-specific task files, in order of most specific to least specific:

* `tasks/CentOS7.4.yml`
* `tasks/CentOS7.yml`
* `tasks/RedHat.yml`
* `tasks/main.yml`

Now, if you run Ansible against a *CentOS 7.9* host, for example, only these tasks are processed in the following order:

1. `tasks/CentOS7.yml`
2. `tasks/main.yml`

Include the OS-specific tasks in the `tasks/main.yml` like this:

```yaml
- name: 'Perform platform/version specific tasks'
  ansible.builtin.include_tasks: '{{ __task_file }}'
  when: '__task_file | length > 0'
  vars:
    __task_file: '{{ lookup("ansible.builtin.first_found", __first_found_options) }}'
    __first_found_options:
      files:
        - '{{ ansible_facts["distribution"] }}{{ ansible_facts["distribution_version"] }}.yml'
        - '{{ ansible_facts["distribution"] }}{{ ansible_facts["distribution_major_version"] }}.yml'
        - '{{ ansible_facts["distribution"] }}.yml'
        - '{{ ansible_facts["os_family"] }}{{ ansible_facts["distribution_version"] }}.yml'
        - '{{ ansible_facts["os_family"] }}{{ ansible_facts["distribution_major_version"] }}.yml'
        - '{{ ansible_facts["os_family"] }}.yml'
      paths:
        - '{{ role_path }}/tasks'
      skip: true
  tags:
    - 'always'
```

Make sure to set the tags directly on the `include_tasks` task, and not on a surrounding block. Setting it on a block causes the tag to be inherited to all tasks in that block, therefore also to included tasks.


### Handling of GPG Keys under Debian (APT Keyring)

Adding a key to `/etc/apt/trusted.gpg.d` is insecure because it adds the key for all repositories. Therefore, `apt-key` (and the `ansible.builtin.apt_key` module) were deprecated.

The new and secure workflow is:

1. Store the GPG key in `/etc/apt/keyrings/`. The file extension **has** to match the file format. Use the `file` utility to determine the format:
    * `PGP public key block Public-Key (old)`: ASCII-armored key. Use `.asc` extension.
    * `OpenPGP Public Key`: Binary GPG key. Use `.gpg` extension.

2. Explicitly specify the path to the key in the `/etc/apt/sources.list.d/` file, for example: `deb [signed-by=/etc/apt/keyrings/icinga.asc] https://...`.

Have a look at the [repo_icinga/tasks/Debian.yml](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_icinga/tasks/Debian.yml) (ASCII armored key) or [repo_mariadb/tasks/Debian.yml](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb/tasks/Debian.yml) (binary GPG key) roles.


### Roles with Special Features

The following roles use techniques that are unusual within LFOps. Roles not in this list follow the standard install-config-service pattern documented in `roles/example`. Each subsection points to the role we consider the cleanest reference implementation of that pattern; if you need to add the same pattern to a new role, start by reading the listed role.


#### Build from source (autotools)

* [libmaxminddb](https://github.com/Linuxfabrik/lfops/tree/main/roles/libmaxminddb): Downloads a GitHub release tarball, then runs `./configure`, `make`, `make check`, `make install` instead of relying on a distro package.


#### Custom SELinux policy modules

* [selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux): Generic driver for inventory-defined `.te` source. Compiles via `checkmodule` + `semodule_package` + `semodule --install` in a temp directory, and applies modules → booleans / file contexts / ports → restorecon → setenforce in that order so types and booleans introduced by a new module are usable in the same run.


#### FACL with multi-user / inherited access

* [mirror](https://github.com/Linuxfabrik/lfops/tree/main/roles/mirror): Grants both the webserver user and the mirror service user RW access to the served files, plus `default:` ACLs so newly created files inherit the same permissions without a recursive `setfacl` run.


#### Multi-OS coverage (Linux + Windows)

* [monitoring_plugins](https://github.com/Linuxfabrik/lfops/tree/main/roles/monitoring_plugins): Splits its task tree into separate `linux-*.yml` and `windows-*.yml` files for install, package-vs-source flavour, archive download and uninstall paths.


#### Non-default Jinja2 delimiters

* [telegraf](https://github.com/Linuxfabrik/lfops/tree/main/roles/telegraf): Flips the variable delimiters via the `#jinja2:variable_start_string:'[%', variable_end_string:'%]'` header in `telegraf.conf.j2`, so TOML payloads containing `{{ ... }}` (Telegraf's own templating) survive Ansible's templating pass.


#### Permission management via `find -exec chmod`

* [grav](https://github.com/Linuxfabrik/lfops/tree/main/roles/grav): Four separate `chmod` passes (files `664`, `bin/` `775`, directories `775`, plus a setgid pass on directories), each registered with `changed_when` based on the `--changes` output for idempotency.


#### systemd socket activation with an on-demand backend

* [chromium_headless](https://github.com/Linuxfabrik/lfops/tree/main/roles/chromium_headless): Fronts a long-running daemon (Chromium, which does not implement the systemd socket-activation protocol) with a `systemd-socket-proxyd`. A `.socket` unit binds the public port, the proxy forwards to the backend on `127.0.0.1` and exits after an idle timeout, and `BindsTo=` ties the backend's lifecycle to the proxy so it starts on the first request and stops when idle.


#### Other

* [apache_solr](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_solr): Picks the matching OpenJDK package for the configured Solr major version (Solr 9 → OpenJDK 17, Solr 8 → OpenJDK 8) via a per-major-version lookup in `vars/main.yml`.

* [mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mongodb): Entries in `mongodb__databases` / `mongodb__users` accept `state: skip` to leave the entry untouched in this run (neither created nor removed) - useful when the database / user is managed elsewhere but should still appear in the inventory.

* [moodle](https://github.com/Linuxfabrik/lfops/tree/main/roles/moodle): Runtime version discovery via `api.github.com/repos/moodle/moodle/tags`, filtered on `^v<configured-version>` and using the first match as the patch tag to download.

* [nextcloud](https://github.com/Linuxfabrik/lfops/tree/main/roles/nextcloud): Writes a state file once initial installation succeeded and uses it to skip the install-only tasks on every subsequent run. The README has a concise but informative "Tags" section.

* [php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php): Builds the `ansible.builtin.package` lists by splitting `php__modules__combined_var` on `state: present` vs `state: absent`, so install and removal happen in two batched package calls instead of one task per module.

* [redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis): Reads the installed Redis version via `package_facts` and deploys the matching `<version>-redis.conf.j2`. systemd is configured via unit-file overrides instead of editing the upstream unit.


### Vendored Plugins

Some files under `plugins/modules/` and `plugins/module_utils/` are not authored by Linuxfabrik but vendored from upstream projects, either because we needed local patches, because the upstream version requires a newer ansible-core than LFOps supports, or because the dependency has to ship with the module to the managed node. They are kept in lockstep with their upstream and should be re-synced (or removed) when the listed condition is met.

* `plugins/modules/ipagroup.py`, `ipahbacrule.py`, `ipahostgroup.py`, `ipapwpolicy.py`, `ipasudocmd.py`, `ipasudocmdgroup.py`, `ipasudorule.py`, `ipauser.py`

    * Upstream: <https://github.com/freeipa/ansible-freeipa>
    * Reason: temporary copy with local `--diff` support from PR [#1415](https://github.com/freeipa/ansible-freeipa/pull/1415).
    * Drop when: PR #1415 is merged and an ansible-freeipa release containing it is available; switch to `freeipa.ansible_freeipa.<module>`.

* `plugins/modules/lvm_pv.py`

    * Upstream: <https://github.com/ansible-collections/community.general> (PR [#10070](https://github.com/ansible-collections/community.general/pull/10070), released in community.general 11.0.0).
    * Reason: community.general 11.0.0 requires ansible-core >= 2.18, which LFOps does not yet mandate (RHEL 8 / Python 3.6 still supported).
    * Drop when: LFOps raises its minimum ansible-core to >= 2.18; switch to `community.general.lvm_pv` and update `roles/lvm` accordingly.

* `plugins/module_utils/gnupg.py` (and its `gnupg.py_LICENSE.txt`)

    * Upstream: <https://github.com/vsajip/python-gnupg> (`python-gnupg`). The synced revision is recorded in the file's own `__version__`.
    * Reason: the `gpg_key` module runs on the managed node and drives the `gpg` binary through this library. Bundling it byte-identical with upstream avoids requiring a `python-gnupg` pip install on every target. The upstream BSD license is kept alongside it.
    * Drop when: not expected; re-sync with the upstream release when picking up bug fixes or newer-Python support, keeping the file unmodified.


### Plugins

In-house plugins live under `plugins/` following the standard Ansible collection layout: `filter/`, `lookup/`, `modules/` and `module_utils/`. The `## Tasks` rules above (FQCN, meta modules, idempotency) are about role tasks; the points below are specific to writing the plugins themselves.

* Every in-house plugin starts with the standard file header, followed by `from __future__ import absolute_import, division, print_function` and `__metaclass__ = type`:

    ```python
    #!/usr/bin/env python3
    # -*- coding: utf-8; py-indent-offset: 4 -*-
    #
    # Author:  Linuxfabrik GmbH, Zurich, Switzerland
    # Contact: info (at) linuxfabrik (dot) ch
    #          https://www.linuxfabrik.ch/
    # License: The Unlicense, see LICENSE file.
    ```

* Use single quotes and f-strings consistently (vendored plugins keep their upstream style, see below).
* Every plugin carries `DOCUMENTATION` (and `RETURN` / `EXAMPLES` where applicable). Keep it valid YAML: in a `description` list, a bullet containing a colon followed by a space is parsed as a mapping and makes `ansible-doc` fail, so rephrase or quote such bullets. Verify with `ansible-doc -t <filter|lookup|module> linuxfabrik.lfops.<name>`; `tests/unit/test_plugin_docs.py` guards against this class of error for all in-house plugins.
* Set `version_added` to the LFOps release the plugin first shipped in, and never change it afterwards.
* `module_utils` holds code shared between plugins. Do not import the external Linuxfabrik Python Libraries (`lib`) into a plugin; copy what you need and note the origin in a comment.


#### Plugin Tests

Unit tests are **mandatory** for every in-house plugin. Any pull request that adds or changes a plugin must add or update its test, and `git grep` should never find a plugin without one.

* **Where**: under `tests/unit/`, mirroring the plugin tree, named `test_<plugin>.py` (e.g. `tests/unit/plugins/filter/test_combine_lod.py`). A plugin with no collection-qualified imports (e.g. the `combine_lod` filter) can be loaded by file path. A plugin that imports `ansible_collections.linuxfabrik.lfops...` (modules, or lookups pulling in a module_util) is imported through that path; `tests/conftest.py` makes this checkout importable as the collection so the imports resolve under plain pytest/tox. Same-named test files in different plugin-type directories are fine (`--import-mode=importlib`). Assert behavior, not implementation details.
* **Two tiers**, because plugins run in different environments:

    * Controller plugins (`plugins/filter/`, `plugins/lookup/`) are evaluated on the Ansible controller and only ever see the controller's Python (>= 3.10). They run on the standard CI matrix.
    * Managed-node plugins (`plugins/modules/`, `plugins/module_utils/`) are executed on the target host and must keep working down to the oldest managed-node Python we maintain (Python 3.6 on RHEL 8). That tier runs inside a RHEL 8 / UBI 8 container; it is scaffolded in `tox.ini` (`[testenv:py36-target]`) and gets enabled once such tests exist.

* **How to run / verify** (the matrix of Python and ansible-core versions is driven by `tox`; see `tests/README.md` and `tox.ini`):

    ```bash
    tox                      # full controller matrix (every Python x ansible-core combination)
    tox -e py311-ansible216  # a single combination
    tox -f py311             # every ansible-core for one Python
    pytest tests/unit        # against the active interpreter (needs pytest, pyyaml, ansible-core)
    ```

* The `Linuxfabrik: Unit Tests` workflow runs the controller matrix on every push and pull request.


### Credits

* <https://github.com/whitecloud/ansible-styleguide>
* <https://redhat-cop.github.io/automation-good-practices>
* <https://docs.openstack.org/openstack-ansible/latest/contributor/code-rules.html>
