# Ansible Role linuxfabrik.lfops.shared

This role bundles helper tasks reused across other LFOps roles and playbooks. It is not designed to be run as a whole; instead, callers import individual tasks via `import_role` / `include_role` with `tasks_from:`.


*Available since LFOps `2.0.1`.*


## Available Tasks

`log-start.yml` and `log-end.yml`

* Append a `START` / `END` line to `/var/log/linuxfabrik-lfops.log` on the target host. Includes the playbook name as well as run/skip tags. No-op in `--check` mode and on Windows. Used as `pre_tasks` / `post_tasks` in every LFOps playbook.
* Parameters: none.

`print-messages.yml`

* Prints the messages roles collected in `__shared__end_of_play_messages` as one block, so the operator sees every manual step in one place directly above the `PLAY RECAP` instead of scattered over a long run. Skipped when nothing was collected, and clears the list afterwards so the next play of a `playbooks/all.yml` run does not repeat it. Used as `post_tasks` in every LFOps playbook, next to `log-end.yml`.
* Parameters: none. Reads `__shared__end_of_play_messages`, see the "Reporting a Manual Step to the Operator" section of the [CONTRIBUTING.md](https://github.com/Linuxfabrik/lfops/blob/main/CONTRIBUTING.md).

`platform-variables.yml`

* Loads OS-family / distribution / version-specific `vars/<name>.yml` files of the *calling* role, in order from least to most specific (e.g. `RedHat.yml` -> `RedHat8.yml` -> `Rocky.yml` -> `Rocky8.yml` -> `Rocky8.10.yml`). Missing files are skipped silently.
* Parameters: none. Relies on `ansible_parent_role_paths[0]` (i.e. it must be imported from another role).

`global-variables.yml`

* Loads LFOps-wide platform variables from the shared role's *own* `vars/<name>.yml` files (`role_path`, not the calling role), using the same least-to-most-specific order as `platform-variables.yml`. Imported in every playbook's `pre_tasks` so the variables are available to all roles in the play.
* Parameters: none.

`assert-reboot-possible.yml` and `request-reboot.yml`

* The two halves of the reboot pattern, see the "Reboots" section of the [CONTRIBUTING.md](https://github.com/Linuxfabrik/lfops/blob/main/CONTRIBUTING.md). `assert-reboot-possible.yml` belongs in the calling role's validation block: it refuses `lfops__reboot_now` on a host without `/usr/local/sbin/schedule-reboot` before the role writes anything, and registers the stat result the other file reads. `request-reboot.yml` files the reboot request, performs the reboot right away when `lfops__reboot_now` is set, or reports the pending reboot to the operator when the mechanism is not deployed. Include it gated on the calling role's own "a reboot is needed" condition.
* Parameters of `assert-reboot-possible.yml`: none.
* Parameters of `request-reboot.yml`:

    * `shared__reboot_reason`: Mandatory. Spool file name, by convention the role name.
    * `shared__reboot_detail`: Mandatory. What changed, in lower case. Goes into the notification mail, followed by the name of the calling role, and into the message the operator sees.

`clone-lib-repo.yml`

* Clones the [Linuxfabrik Python Libraries](https://github.com/Linuxfabrik/lib) to `/tmp/ansible.lib-repo` on the Ansible controller (`delegate_to: localhost`, serialized with `throttle: 1`, `--check`-safe). Includes a rescue path that wipes the directory and retries on failure (e.g. when an existing checkout is on a different ref).
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
- name: 'Set LFOps-wide platform variables'
  ansible.builtin.import_role:
    name: 'shared'
    tasks_from: 'global-variables.yml'
  tags:
    - 'always'

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
