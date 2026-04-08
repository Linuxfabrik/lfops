# Ansible Role linuxfabrik.lfops.shell

This role executes arbitrary shell commands on the host.

Note that this role is not idempotent by default, consider setting `creates`, `removes` or `run_once` (see below).


## Tags

`shell`

* Executes shell commands.
* Triggers: none.

Tipp:

* To deploy a single Shell Command only, supplement the extra variable `--extra-vars='shell__limit_cmds=["010-setup-step1"]'`. See [Optional Role Variables - Specific to this role](https://github.com/Linuxfabrik/lfops/tree/main/roles/shell#optional-role-variables).

## Optional Role Variables

`shell__commands__host_var` / `shell__commands__group_var`

* List of dictionaries containing the commands to execute.
* Subkeys:

    * `name`:

        * Mandatory. A user-defined name for the commands. Must be unique. The commands are sorted by name and executed in that order.
        * Type: String.

    * `commands`:

        * Mandatory. Shell commands to execute.
        * Type: String.

    * `state`:

        * Optional. Whether to execute the commands or not. One of `present` or `absent`.
        * Type: String.
        * Default: `'present'`

    * `chdir`:

        * Optional. Change into this directory before running the command.
        * Type: String.
        * Default: unset

    * `creates`:

        * Optional. A filename, when it already exists, the commands *not* be run. If `run_once: true` is set, this will be set to `/etc/ansible/facts.d/shell_{{ item["name"] }}.state`.
        * Type: String.
        * Default: unset

    * `removes`:

        * Optional. A filename, when it does not exist, the commands will *not* be run.
        * Type: String.
        * Default: unset

    * `run_once`:

        * Optional. Only run the commands once. This creates a state file (`/etc/ansible/facts.d/shell_{{ item["name"] }}.state`) and sets `creates` correspondingly.
        * Type: Bool.
        * Default: `false`

    * `stdin`:

        * Optional. Set the stdin of the command directly to the specified value.
        * Type: String.
        * Default: unset

    * `stdin_add_newline`:

        * Optional. Whether to append a newline to stdin data.
        * Type: Bool.
        * Default: `true`

    * `user`:

        * Optional. User to run the commands as.
        * Type: String.
        * Default: unset (most likely `root`)

    * `ignore_errors`:

        * Optional. Whether to ignore errors during command execution.
        * Type: Bool.
        * Default: `false`

* Type: List of dictionaries.
* Default: `[]`

`shell__limit_cmds`

* Checks if the `name` of the command is in the list and only runs those. Can be used on the CLI to speed up the deployment, e.g. `--extra-vars='shell__limit_cmds=["010-setup-step1"]'`.
* Type: List.
* Default: unset

Example:

```yaml
# optional
shell__commands__host_var:
  - name: '100-setup-step2'
    commands: |
      touch test2
      echo "test2 $(date)" >> /tmp/log
      sleep 3
    chdir: '/tmp'
    creates: '/tmp/test2'
  - name: '010-setup-step1'
    commands: |
      touch test1
      echo "test1 $(date)" >> /tmp/log
      sleep 3
    run_once: true
    chdir: '/tmp'
    user: 'linuxfabrik'
    ignore_errors: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
