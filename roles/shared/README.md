# Ansible Role linuxfabrik.lfops.shared

This role bundles helper tasks reused across other LFOps roles and playbooks. It is not designed to be run as a whole; instead, callers import individual tasks via `import_role` / `include_role` with `tasks_from:`.


## Available Tasks

`log-start.yml` and `log-end.yml`

* Append a `START` / `END` line to `/var/log/linuxfabrik-lfops.log` on the target host. Includes the playbook name as well as run/skip tags. No-op in `--check` mode and on Windows. Used as `pre_tasks` / `post_tasks` in every LFOps playbook.
* Parameters: none.

`platform-variables.yml`

* Loads OS-family / distribution / version-specific `vars/<name>.yml` files of the *calling* role, in order from least to most specific (e.g. `RedHat.yml` -> `RedHat8.yml` -> `Rocky.yml` -> `Rocky8.yml` -> `Rocky8.10.yml`). Missing files are skipped silently.
* Parameters: none. Relies on `ansible_parent_role_paths[0]` (i.e. it must be imported from another role).

`clone-lib-repo.yml`

* Clones the [Linuxfabrik Python Libraries](https://github.com/Linuxfabrik/lib) to `/tmp/ansible.lib-repo` on the Ansible controller (`delegate_to: localhost`, `run_once`, `--check`-safe). Includes a rescue path that wipes the directory and retries on failure (e.g. when an existing checkout is on a different ref).
* Parameters:

    * `shared__lib_version`: Mandatory. The git ref to check out. Accepts `'dev'` (resolved to `main`), a tag like `'v1.2.3'`, or a bare version like `'1.2.3'` (auto-prefixed with `v`).

`clone-monitoring-plugins-repo.yml`

* Same as `clone-lib-repo.yml` but for the [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins). Target on the controller: `/tmp/ansible.monitoring-plugins-repo`.
* Parameters:

    * `shared__monitoring_plugins_version`: Mandatory. Same semantics as `shared__lib_version`.

`remove-rpmnew-rpmsave.yml`

* Removes `<file>.rpmnew`, `<file>.rpmsave`, `<file>.dpkg-dist` and `<file>.ucf-dist` for a single config file. Only runs when `lfops__remove_rpmnew_rpmsave` is `true` (LFOps-wide opt-in, see the main [README](https://github.com/Linuxfabrik/lfops/blob/main/README.md#lfops__remove_rpmnew_rpmsave)).
* Parameters:

    * `shared__remove_rpmnew_rpmsave_config_file`: Mandatory. Absolute path of the deployed config file (without the `.rpmnew` / `.rpmsave` suffix).


## Usage Example

```yaml
- name: 'Set platform/version specific variables'
  ansible.builtin.import_role:
    name: 'shared'
    tasks_from: 'platform-variables.yml'
  tags:
    - 'always'

- name: 'Remove rpmnew / rpmsave'
  ansible.builtin.include_role:
    name: 'shared'
    tasks_from: 'remove-rpmnew-rpmsave.yml'
  vars:
    shared__remove_rpmnew_rpmsave_config_file: '/etc/example/example.conf'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
