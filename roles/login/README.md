# Ansible Role login

This role creates users, adds them to additional groups, and sets their sshd authorized_keys to allow them to login to the system.
Aditionally, a group can be added to the sudoers for password-less `sudo` access.

FQCN: linuxfabrik.lfops.login

Tested on

* RHEL 8 (and compatible)
* Fedora Server 35


## Requirements

This role does not have any requirements.


## Tags

| Tag   | What it does                                        |
| ---   | ------------                                        |
| login | Manages users, their groups and ssh authorized_keys |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/login/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### login__passwordless_sudo_group

The group which should be added to the sudoers for password-less `sudo` access.

Default:
```yaml
login__passwordless_sudo_group: ''
```

#### login__users

A list of the users to be created or deleted.

Subkeys:

* `name`: Mandatory, string. The name of the user account.
* `state`: Optional, string. Defaults to `present`. The state of the user account. Possible options: `present`, `absent`.
* `additional_groups`: Optional, list. Defaults to `[]`. Additional groups the user account should be in.
* `sshd_authorized_keys`: Optional, list. Defaults to `[]`. List of sshd authorized_keys for the user account.
* `remove_other_sshd_authorized_keys`: Optional, boolean. Defaults to `true`. Whether to remove all other non-specified keys from the authorized_keys file.

Default:
```yaml
login__users: []
```

Example:
```yaml
login__users:
  - name: 'test'
    state: 'present'
    additional_groups:
      -  'wheel'
      -  'testgroup'
      -  '{{ login__passwordless_sudo_group }}'
    sshd_authorized_keys:
      - 'ssh-ed25519 M4wt6qfbtyAaBnhSJDzoQEAOwiQM7k9lTvhYhNHJ7i6ciWH9uXJlbpbDF4Wv5lSr8t1maY test@example.com'
    remove_other_sshd_authorized_keys: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
