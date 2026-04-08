# Ansible Role linuxfabrik.lfops.login

This role creates users, adds them to additional groups, and sets their SSH authorized_keys to allow them to login to the system.
Aditionally, a group can be added to the sudoers for password-less `sudo` access.

IMPORTANT:

* The default behavior of this role is that it distributes SSH keys that it knows from the host/group variables and deletes any other keys that already exist on the target system in `.ssh/authorized_keys`. This might break things. Set `remove_other_sshd_authorized_keys` accordingly.

## Mandatory Requirements

* Install the `passlib` Python module on the Ansible Controller (`dnf install python3-passlib` on Fedora). If you use the [LFOps Execution Environment](https://github.com/Linuxfabrik/lfops/pkgs/container/lfops_ee), this is already done for you.


## Tags

`login`

* Manages users, their groups and SSH authorized_keys.
* Triggers: none.

`login:authorized_keys`

* Manages SSH authorized_keys.
* Triggers: none.


## Optional Role Variables

`login__passwordless_sudo_group`

* The group which should be added to the sudoers for password-less `sudo` access.
* Type: String.
* Default: `''`

`login__users__host_var` / `login__users__group_var`

* A list of the users to be created or deleted.
* Subkeys:

    * `additional_groups`:

        * Optional. Additional groups the user account should be in.
        * Type: List.
        * Default: `[]`

    * `create_home`:

        * Optional. Unless set to `false`, a home directory will be made for the user when the account is created or if the home directory does not exist.
        * Type: Bool.
        * Default: `true`

    * `home`:

        * Optional. The home directory for the user.
        * Type: String.
        * Default: the OS default

    * `linger`:

        * Optional. Enable lingering of the account, analogous to `loginctl enable/disable-linger`.
        * Type: Bool.
        * Default: `false`

    * `name`:

        * Mandatory. The name of the user account.
        * Type: String.

    * `password`:

        * Optional. The password of the user.
        * Type: String.

    * `primary_group`:

        * Optional. The name of the primary group. If omitted, the primary group name will be the same as the username. If this primary group exists via a central authentication method e.g. FreeIPA, the primary group will default to `users`.
        * Type: String.

    * `remove_other_sshd_authorized_keys`:

        * Optional. Whether to remove all other non-specified keys from the authorized_keys file.
        * Type: Bool.
        * Default: `false`

    * `shell`:

        * Optional. Shell for the user account.
        * Type: String.
        * Default: `'/bin/bash'`

    * `sshd_authorized_keys`:

        * Optional. List of sshd authorized_keys for the user account.
        * Type: List.
        * Default: `[]`

    * `state`:

        * Optional. The state of the user account. Possible options: `present`, `absent`.
        * Type: String.
        * Default: `'present'`

    * `system`:

        * Optional. If this is a system account or not. Usually system accounts are used for running applications.
        * Type: Bool.
        * Default: `false`

* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`

Example:

```yaml
# optional
login__passwordless_sudo_group: 'linuxfabrik'
login__users__host_var:
  - name: 'test'
    password: 'linuxfabrik'
    home: '/home/test'
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
