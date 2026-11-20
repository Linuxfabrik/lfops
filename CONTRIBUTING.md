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

Commit messages, pull request bodies and documentation never name a customer host, nor a Linuxfabrik-internal one. Describe the host generically instead, for example "a Rocky 8 host" or "a Nextcloud host with about 400 GB of data".


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
* Use `d()`, not its long form `default()`, for consistency.
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
* `roles/<role-name>/README.md`, following `roles/example/README.md` and [README](docs/developer-guide/roles.md#readme) below.
* `roles/<role-name>/meta/argument_specs.yml` declaring all user-facing variables.
* Updates to `playbooks/README.md`, `playbooks/all.yml`, `COMPATIBILITY.md` and `CHANGELOG.md`.
* For a role that stores data outside of the default backup sources: the directory in `duplicity__backup_sources__role_var` and in `roles/duplicity/README.md`, see [Playbooks](docs/developer-guide/playbooks.md#playbooks).
* An entry for `roles/<role-name>/defaults/main.yml` in `.ansible-lint-ignore` (`jinja[spacing]`), as the `__combined_var` expressions in the defaults span several lines.


### OS Coverage

A new or changed role covers the **full operating-system matrix** in [COMPATIBILITY.md](COMPATIBILITY.md) (currently Debian 12 and 13, RHEL 8, 9 and 10, Ubuntu 22.04, 24.04 and 26.04). COMPATIBILITY.md is authoritative; add a column there before supporting a new release.

* Abstract OS differences (package names, paths, unit names, users, ...) into per-OS vars files, see [OS-specific Variables](docs/developer-guide/variables.md#os-specific-variables). Reference roles: `sshd`, `clamav`.
* Validate empirically on each family before claiming support: one podman container per OS (e.g. `rockylinux/rockylinux:10`, `debian:13`, `ubuntu:24.04`), systemd-enabled when services are managed.
* Mark a cell `x` only once it is proven to run; `(x)` means "expected to work but not verified".


### Security by Default

A host deployed with LFOps and no further inventory should already be in the state a security review would ask for: where the safe value also works, it is the default, even if upstream ships the permissive one. Document the deviation per [Deviating from an Upstream Default](docs/developer-guide/variables.md#deviating-from-an-upstream-default).


### Changelog Sections

The "Changelog" rules above apply, except that entries are sorted newest first, because operators running playbooks need to see what changed most recently.

* Each subsection (`### Added`, ...) appears at most once per release section; append to the existing one.
* Order: `Breaking Changes`, `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`. Omit empty subsections.
* Add new entries at the top of a subsection, even if this results in multiple entries for the same role.


### Developer Guide

Before you change code, read the file in `docs/developer-guide/` that matches the task, completely:

| File | Read before |
|---|---|
| [playbooks.md](docs/developer-guide/playbooks.md) | writing or changing a playbook |
| [plugins.md](docs/developer-guide/plugins.md) | writing or changing an in-house module, filter, lookup or callback plugin, or its unit test |
| [roles.md](docs/developer-guide/roles.md) | writing or changing a role: principles, README structure, handlers, reboots, preflight checks, manual steps, tags, and the roles with special techniques |
| [systemd.md](docs/developer-guide/systemd.md) | deploying a systemd drop-in, a calendar timer or a secret for a systemd service |
| [tasks.md](docs/developer-guide/tasks.md) | writing tasks, controller-side caches, OS-specific task files or an APT keyring |
| [templates.md](docs/developer-guide/templates.md) | adding or changing a template |
| [testing.md](docs/developer-guide/testing.md) | writing or running a Molecule scenario |
| [upstream.md](docs/developer-guide/upstream.md) | following an upstream release, adding a workaround with a planned removal, or re-syncing a vendored plugin |
| [variables.md](docs/developer-guide/variables.md) | adding, renaming or validating a role variable, combined or OS-specific variables, or deviating from an upstream default |


### Credits

* <https://github.com/whitecloud/ansible-styleguide>
* <https://redhat-cop.github.io/automation-good-practices>
* <https://docs.openstack.org/openstack-ansible/latest/contributors/code-rules.html>
