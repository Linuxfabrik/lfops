# Ansible Role linuxfabrik.lfops.login

This role creates users, adds them to additional groups, and sets their sshd authorized_keys to allow them to login to the system.
Aditionally, a group can be added to the sudoers for password-less `sudo` access.

IMPORTANT:

* The default behavior of this role is that it distributes SSH keys that it knows from the host/group variables and deletes any other keys that already exist on the target system in `.ssh/authorized_keys`. This might break things. Set `remove_other_sshd_authorized_keys` accordingly.

Runs on

* Fedora Server 35+
* RHEL 8 (and compatible)
* RHEL 9 (and compatible)
* Ubuntu 16


## Tags

| Tag     | What it does                                        |
| ---     | ------------                                        |
| `login` | Manages users, their groups and ssh authorized_keys |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `login__users__host_var` /<br> `login__users__group_var` | A list of the users to be created or deleted. Subkeys: <ul><li>`additional_groups`: Optional, list. Defaults to `[]`. Additional groups the user account should be in.</li><li>`home`: Optional, string. Defaults to None. The home directory for the user. Will be created.</li><li>`name`: Mandatory, string. The name of the user account.</li><li>`primary_group`: Optional, string. The name of the primary group. If omitted, the primary group name will be the same as the username. If this primary group exists via a central authentication method e.g. FreeIPA, the primary group will default to `users`.</li><li>`remove_other_sshd_authorized_keys`: Optional, boolean. Defaults to `false`. Whether to remove all other non-specified keys from the authorized_keys file.</li><li>`shell`: Optional, string. Defaults to None. Shell for the user account.</li><li>`sshd_authorized_keys`: Optional, list. Defaults to `[]`. List of sshd authorized_keys for the user account.</li><li>`state`: Optional, string. Defaults to `present`. The state of the user account. Possible options: `present`, `absent`.</li><li>`system`: Optional, string. Defaults to `false`. If this is a system account or not. Usually system accounts are used for running applications.</li></ul><br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `login__passwordless_sudo_group` | The group which should be added to the sudoers for password-less `sudo` access. | `''` |

Example:
```yaml
# optional
login__users__host_var:
  - name: 'test'
    state: 'present'
    additional_groups:
      -  'wheel'
      -  '{{ login__passwordless_sudo_group }}'
    primary_group: 'testgroup'
    sshd_authorized_keys:
      - 'ssh-ed25519 M4wt6qfbtyAaBnhSJDzoQEAOwiQM7k9lTvhYhNHJ7i6ciWH9uXJlbpbDF4Wv5lSr8t1maY test@example.com'
    remove_other_sshd_authorized_keys: true
  - name: 'github-runner'
    home: '/opt/github-runner'
    state: 'present'
    system: 'true'
login__users__group_var: []
login__passwordless_sudo_group: ''
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
