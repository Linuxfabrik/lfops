# Ansible Role linuxfabrik.lfops.login

This role creates users, adds them to additional groups, and sets their SSH authorized_keys to allow them to login to the system.
Aditionally, a group can be added to the sudoers for password-less `sudo` access.

IMPORTANT:

* The default behavior of this role is that it distributes SSH keys that it knows from the host/group variables and deletes any other keys that already exist on the target system in `.ssh/authorized_keys`. This might break things. Set `remove_other_sshd_authorized_keys` accordingly.

## Mandatory Requirements

* Install the `passlib` Python module on the Ansible Controller (`dnf install python3-passlib` on Fedora).


## Tags

| Tag     | What it does                                        |
| ---     | ------------                                        |
| `login` | Manages users, their groups and SSH authorized_keys |
| `login:authorized_keys` | Manages SSH authorized_keys |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `login__passwordless_sudo_group` | The group which should be added to the sudoers for password-less `sudo` access. | `''` |
| `login__users__host_var` /<br> `login__users__group_var` | A list of the users to be created or deleted. Subkeys: <ul><li>`additional_groups`: Optional, list. Defaults to `[]`. Additional groups the user account should be in.</li> <li>`create_home`: Optional, boolean. Unless set to `false`, a home directory will be made for the user when the account is created or if the home directory does not exist. Defaults to `true`. <li>`home`: Optional, string. Defaults to None. The home directory for the user. Will be created.</li> <li>`linger`: Optional, boolean. Enable lingering of the account, analogous to `loginctl enable/disable-linger`. Defaults to `false`.</li> <li>`name`: Mandatory, string. The name of the user account.</li> <li>`password`: Optional, string. The password of the user.</li> <li>`primary_group`: Optional, string. The name of the primary group. If omitted, the primary group name will be the same as the username. If this primary group exists via a central authentication method e.g. FreeIPA, the primary group will default to `users`.</li> <li>`remove_other_sshd_authorized_keys`: Optional, boolean. Defaults to `false`. Whether to remove all other non-specified keys from the authorized_keys file.</li> <li>`shell`: Optional, string. Defaults to None. Shell for the user account.</li> <li>`sshd_authorized_keys`: Optional, list. Defaults to `[]`. List of sshd authorized_keys for the user account.</li> <li>`state`: Optional, string. Defaults to `present`. The state of the user account. Possible options: `present`, `absent`.</li> <li>`system`: Optional, string. Defaults to `false`. If this is a system account or not. Usually system accounts are used for running applications.</li></ul><br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |

Example:
```yaml
# optional
login__passwordless_sudo_group: 'linuxfabrik'
login__users__host_var:
  - name: 'test'
    password: 'linuxfabrik'
    home: '/home/linuxfabrik'
    create_home: true
    shell: '/bin/bash'
    linger: true
    primary_group: 'testgroup'
    additional_groups:
      - 'wheel'
      - '{{ login__passwordless_sudo_group }}'
    sshd_authorized_keys:
      - 'ssh-ed25519 M4wt6qfbtyAaBnhSJDzoQEAOwiQM7k9lTvhYhNHJ7i6ciWH9uXJlbpbDF4Wv5lSr8t1maY test@example.com'
    remove_other_sshd_authorized_keys: true
    state: 'present'
    system: false
  - name: 'github-runner'
    home: '/opt/github-runner'
    state: 'present'
    system: true
login__users__group_var: []
```


## Troubleshooting

`[DEPRECATION WARNING]: Encryption using the Python crypt module is deprecated. The Python crypt module is deprecated and will be removed from Python 3.13. Install the passlib library for continued encryption functionality. This feature will be removed in version 2.17.`: Make sure to install the `passlib` Python module on the Ansible Controller (`dnf install python3-passlib` on Fedora).


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
