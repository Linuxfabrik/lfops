# Tasks

* Always use the FQCN of the module.
* Use meta modules: `ansible.builtin.package` instead of `yum` / `dnf` / `apt`, `ansible.builtin.service` instead of `systemd`.
* Prefer `ansible.builtin.command` (or `ansible.windows.win_command`) over `shell` over `raw`, and `ansible.builtin.template` over `copy`, `lineinfile` or `blockinfile`. Exception: see [Setting options in a packaged file instead of templating it](roles.md#setting-options-in-a-packaged-file-instead-of-templating-it).
* Pin `ansible.builtin.shell` to `executable: '/bin/bash'` (in `args:` or next to `cmd:`): Debian's `/bin/sh` is `dash`, which rejects `set -o pipefail`, `[[ ... ]]` and `source`. `/bin/bash` resolves with or without usrmerge, `/usr/bin/bash` does not.
* Never `state: 'latest'` with `ansible.builtin.package`, use `state: 'present'`.
* Use `delegate_to: 'localhost'`, never `local_action`.
* Set both `become: false` and `vars: ansible_become: false # noqa var-naming[pattern]` on every task or block delegated to localhost. Play-level `become: true` propagates to delegated tasks, and `ansible_become: true` in the inventory overrides the `become: false` keyword; only the task variable overrides the inventory. Otherwise the task fails with `sudo: a password is required`, or runs as root on the controller. Verified with ansible-core 2.16 and 2.18.
* Avoid `run_once: true`: it evaluates `when` (also that of an enclosing block or include) against the first host only, and if that host skips, every host skips. Let controller-side tasks run per host:
    * `ansible.builtin.get_url` writing a single file is race-safe (temp file plus atomic rename); with a version-pinned `dest` only the first host downloads.
    * Tasks mutating a shared controller path in place (`ansible.builtin.git` into a shared working dir, `command` / `shell` building files under `/tmp`) get `throttle: 1` with a comment `# serialize: ...`.
    * Where hosts write to different directories depending on their facts (interpreter, architecture), a `flock` per directory instead of `throttle: 1` lets the directories be built in parallel, while the hosts sharing one wait for the first. Reference: the dependency download in `roles/monitoring_plugins`.
    * `run_once` stays only for a single read-only lookup shared to all hosts, e.g. a GitHub release API query stored with `set_fact`.
* Set `vars: mitogen_task_isolation: 'fork' # noqa var-naming[pattern]` on controller-side tasks that take time per host: `ansible.posix.synchronize` (which runs `rsync` on the controller), downloads, `git ls-remote`. Under the Mitogen strategy, all tasks that run on the controller go to the one Mitogen context of the controller, which runs one call at a time, so these tasks run one host after the other: ten hosts delegating a two-second command to localhost take 20.9 s, 3.4 s with `fork` (Mitogen 0.3.44, ansible-core 2.16.19). Other strategies ignore the variable. Tasks with `throttle: 1` and quick ones (`stat`, `set_fact`) gain nothing.
* Download on the controller (`delegate_to: 'localhost'`) and copy to the target: release artifacts, Git checkouts, language packages. Only the controller needs outbound access; say who needs what in "How the Role Behaves". See `roles/example` and [Python dependencies for air-gapped targets](roles.md#python-dependencies-for-air-gapped-targets).
* Retry every download with `retries: 3` and `delay: 10`: `get_url`, `git`, `rpm_key` with a URL, `uri` lookups such as the GitHub release API, and every `package`, `apt`, `dnf` and `pip` task that installs or updates (not `state: 'absent'`). Since ansible-core 2.16 `retries` without `until` repeats until success. Never retry calls that change something, such as an API `POST`.
* Always give `command` and `shell` tasks `changed_when`, `creates` or `removes`; `changed_when: false` when read-only, and `changed_when: true # <reason>` when a command always runs and its effect cannot be detected.
* A read-only `command` with `check_mode: false` that calls a binary the role installs itself (package, unpacked archive) fails under `--check` on a host without it, since nothing is installed in check mode. Register the task that provides the binary, skip the command with `when: 'not (ansible_check_mode and <result> is changed)'`, and let the tasks using its result cope with a skipped one (`<result>["stdout_lines"] is defined`). Add `<result> is defined and` when a tag can skip the providing task. References: `roles/example`, `roles/lvm` (`growpart`).
* Prefer `chown -R --changes` over `ansible.builtin.file` with `recurse: true` (slow on large trees), with `changed_when: '<result>["stdout"] | length > 0'`.
* With `ansible.builtin.template`, always set `backup`, `src`, `dest`, `owner`, `group` and `mode`.
* The web server user (or any other service user) owns only what the application writes at runtime, such as uploads, caches or a configuration the web UI edits. Code, and configuration it only reads, belong to `root`; grant read access through the group (`owner: 'root'`, `group: '{{ __shared__apache_httpd_group }}'`, `mode: 0o640`). Otherwise a compromised web application can change the code or its own configuration. See `roles/example`.
* Prefer `ansible.builtin.assert` over `ansible.builtin.fail` with `when`, for consistency.
* Optionally add `ansible.builtin.debug` tasks for `__combined_var` variables.
* Split service `enabled` and `state` into separate tasks, see [Handlers](roles.md#handlers).
* Check `ansible_facts["selinux"]["status"] != "disabled"` before managing SELinux ports, file contexts or booleans.


## Controller-side Caches

What a role prepares on the controller for every host (Git checkouts, staging trees, downloaded packages) is cached, so that the first host prepares it and every further host and later run finds it done. Reference: `roles/monitoring_plugins`.

* Keep the cache below `/var/tmp/lfops/<role>/`, which outlives a reboot. `/var/tmp/lfops` is the one directory the [README](../../README.md#using-ansible-navigator) asks ansible-navigator users to mount into the EE, whose own `/var/tmp` starts empty with every run.
* Create both directories with `mode: 0o700`. The cache holds what is deployed to every host as root; below the world-writable `/var/tmp`, another user could create the directory first, and setting the mode then fails, so the run aborts instead of deploying that user's content.
* Name each entry after the state it holds, a release tag or a resolved commit (`git ls-remote`), never after a branch, so that an entry found there is final and needs no update. Hosts with different versions in one play then never share an entry.
* Build an entry in a temporary directory next to it and move it into place, or mark it complete with a file inside it as the last step, so that a run that aborts halfway leaves nothing a later host takes for complete.
* Remove entries older than 7 days at the start of the role (`find <cache> -mindepth 1 -maxdepth 1 -mtime +7 -exec rm -rf -- {} +`). systemd-tmpfiles ages out files below `/var/tmp` after 30 days one by one, which could leave an entry that looks complete with files missing; this also takes away versions no longer in use.


## OS-specific Tasks

Platform-specific tasks go into `tasks/<platform>.yml`; only the most specific match runs, then `main.yml` (a CentOS 7.9 host with `CentOS7.4.yml`, `CentOS7.yml`, `RedHat.yml` runs `CentOS7.yml`). Include them with the `include_tasks` + `first_found` task (`skip: true`) from `roles/example/tasks/main.yml`, which tries `distribution` + `distribution_version`, `distribution` + `distribution_major_version`, `distribution`, then the same for `os_family`. Tag `always` on the `include_tasks` task itself, not on a surrounding block, which would pass the tag on to all included tasks.


## Handling of GPG Keys under Debian (APT Keyring)

`/etc/apt/trusted.gpg.d` trusts a key for all repositories, so `apt-key` and `ansible.builtin.apt_key` are deprecated. Instead:

1. Store the key in `/etc/apt/keyrings/` with the extension matching `file`: `PGP public key block Public-Key (old)` is `.asc`, `OpenPGP Public Key` is `.gpg`.
2. Reference it in `/etc/apt/sources.list.d/`: `deb [signed-by=/etc/apt/keyrings/icinga.asc] https://...`.

References: `roles/repo_icinga/tasks/Debian.yml` (ASCII-armored), `roles/repo_mariadb/tasks/Debian.yml` (binary).
