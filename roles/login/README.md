# Ansible Role linuxfabrik.lfops.login

This role creates users, adds them to additional groups, and sets their sshd authorized_keys to allow them to login to the system.
Aditionally, a group can be added to the sudoers for password-less `sudo` access.

IMPORTANT:

* The default behavior of this role is that it distributes SSH keys that it knows from the host/group variables and deletes any other keys that already exist on the target system in `.authorized_keys`. This might break things. Set `remove_other_sshd_authorized_keys` accordingly.

Runs on

* Fedora Server 35+
* RHEL 8 (and compatible)
* Ubuntu 16


## Tags

| Tag     | What it does                                        |
| ---     | ------------                                        |
| `login` | Manages users, their groups and ssh authorized_keys |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `login__users__host_var` /<br> `login__users__group_var` | A list of the users to be created or deleted. Subkeys:<br> * `name`: Mandatory, string. The name of the user account.<br> * `state`: Optional, string. Defaults to `present`. The state of the user account. Possible options: `present`, `absent`.<br> * `additional_groups`: Optional, list. Defaults to `[]`. Additional groups the user account should be in.<br> * `sshd_authorized_keys`: Optional, list. Defaults to `[]`. List of sshd authorized_keys for the user account.<br> * `remove_other_sshd_authorized_keys`: Optional, boolean. Defaults to `true`. Whether to remove all other non-specified keys from the authorized_keys file.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `login__passwordless_sudo_group` | The group which should be added to the sudoers for password-less `sudo` access. | `''` |

Example:
```yaml
# optional
login__users__host_var:
  - name: 'test'
    state: 'present'
    additional_groups:
      -  'wheel'
      -  'testgroup'
      -  '{{ login__passwordless_sudo_group }}'
    sshd_authorized_keys:
      - 'ssh-ed25519 M4wt6qfbtyAaBnhSJDzoQEAOwiQM7k9lTvhYhNHJ7i6ciWH9uXJlbpbDF4Wv5lSr8t1maY test@example.com'
    remove_other_sshd_authorized_keys: true
login__users__group_var: []
login__passwordless_sudo_group: ''
```


## Combining Group and Host Vars

Assume you have 'alice' defined like so:

group vars:
```yaml
login__users__group_var:
  - name: 'alice'
    additional_groups:
      -  'common'
      -  'groupgroup'
    sshd_authorized_keys:
      - 'ssh-rsa GROUPKEY'
```

host vars:
```yaml
login__users__host_var:
  - name: 'alice'
    additional_groups:
      -  'common'
      -  'hostgroup'
    sshd_authorized_keys:
      - 'ssh-rsa HOSTKEY'
```

The role will fully combine the account. First, 'alice' will be configured with all settings from group vars. After that, the host vars for 'alice' will apply. In the end 'alice' gets these settings:
```
{
    "name": "alice",
    "additional_groups": [
        "common",
        "groupgroup",
        "hostgroup"
    ],
    "sshd_authorized_keys": [
        "ssh-rsa GROUPKEY"
        "ssh-rsa HOSTKEY"
    ],
},
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
