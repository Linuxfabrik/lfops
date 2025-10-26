# Ansible Role linuxfabrik.lfops.shell

This role executes arbitrary shell commands on the host.

Note that this role is not idempotent by default, consider setting `creates`, `removes` or `run_once` (see below).


## Tags

| Tag     | What it does             | Reload / Restart |
| ---     | ------------             | ---------------- |
| `shell` | Executes shell commands. | - |

Tipp:

* To deploy a single Shell Command only, supplement the extra variable `--extra-vars=shell__limit_cmd=100-setup-step2`. See [Optional Role Variables - Specific to this role](https://github.com/Linuxfabrik/lfops/tree/main/roles/shell#optional-role-variables).

## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `shell__commands__host_var` / <br> `shell__commands__group_var` | List of dictionaries containing the commands to execute. Subkeys:<ul><li>`name`: Mandatory, string. A user-defined name for the commands. Must be unique. The commands are sorted by name and executed in that order.</li><li>`commands`: Mandatory, string. Shell commands to execute.</li><li>`state`: Optional, string. Whether to execute the commands or not. One of `present` or `absent`. Defaults to `present`.</li><li>`chdir`: Optional, string. Change into this directory before running the command. Defaults to null.</li><li>`creates`: Optional, string. A filename, when it already exists, the commands *not* be run. If `run_once: true` is set, this will be set to `/etc/ansible/facts.d/shell_{{ item["name"] }}.state`. Defaults to null.</li><li>`removes`: Optional, string. A filename, when it does not exist, the commands will *not* be run. Defaults to null.</li><li>`run_once`: Optional, bool. Only run the commands once. This creates a state file (`/etc/ansible/facts.d/shell_{{ item["name"] }}.state`) and sets `creates` correspondingly. Defaults to `false`.</li><li>`stdin`: Optional, string. Set the stdin of the command directly to the specified value. Defaults to null.</li><li>`stdin_add_newline`: Optional, bool. Whether to append a newline to stdin data. Defaults to `true`.</li><li>`user`: Optional, string. User to run the commands as. Defaults to null (most likely `root`).</li><li>`ignore_errors`: Optional, bool. Whether to ignore errors during command execution. Defaults to `false`</li></ul> | `[]` |
| `shell__limit_cmd` | List. Checks if the name is in the list and only deploys those. Can be used on the CLI to speed up the deployment, e.g. --extra-vars='shell__limit_cmd=["010-setup-step1"]'. | unset |

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
