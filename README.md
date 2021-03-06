# LFOps - Ansible Collection of Roles, Playbooks and Plugins for managing Linux-based Cloud Infrastructures


## Installation

To install the **stable** release of the collection:
```bash
ansible-galaxy collection install linuxfabrik.lfops
```

To install the **development** version of the collection (requires ansible >= 2.10):
```bash
# via HTTPS
ansible-galaxy collection install git+https://github.com/Linuxfabrik/lfops.git

# via SSH
ansible-galaxy collection install git@github.com:Linuxfabrik/lfops.git
```

To use the git repository directly (just for development purposes):
```bash
git clone git@github.com:Linuxfabrik/lfops.git
mkdir -p ~/.ansible/collections/ansible_collections/linuxfabrik/
ln -s /path/to/lfops ~/.ansible/collections/ansible_collections/linuxfabrik/
```

## How to use LFOps

Example: If you want to run `playbooks/php.yml`, place your host `myhost` in the `lfops_php` group. After that, run:

```bash
ansible-playbook --inventory path/to/environment linuxfabrik.lfops.php --limit myhost
```

For more details on group names, Ansible tags, etc., see the playbooks and README files for the roles.


## A typical Workflow Example

First, add `myhost` to the corresponding groups in your Ansible inventory.

```yaml
[lfops_hetzner_vm]
myhost

[lfops_basic_setup]
myhost

[lfops_monitoring_plugins]
myhost

[lfops_setup_nextcloud]
myhost
```

Deploy a VM:

```bash
ansible-playbook --inventory path/to/environment linuxfabrik.lfops.mcm_vm --limit myhost
```

Run the basic setup:

```bash
ansible-playbook --inventory path/to/environment linuxfabrik.lfops.setup_basic --limit myhost
```

Deploy a component:

```bash
ansible-playbook --inventory path/to/environment linuxfabrik.lfops.monitoring_plugins --limit myhost
```

Deploy a full-fledged application (Playbooks for application setups are prefixed by `setup_`):

```bash
ansible-playbook --inventory path/to/environment linuxfabrik.lfops.setup_nextcloud --limit myhost
```


## Documentation

* Roles: Each role has its own README file.
* Plugins: The documentation for all plugins is available through `ansible-doc`. For example, `ansible-doc linuxfabrik.lfops.gpg_key` shows the documentation for the GPG key managing module.


## Known Limitations

Combined lists and dictionaries (`rolename__combined_varname`) containing default values cannot be unset or overwritten, they can only be extended. If you need to overwrite to delete a pre-defined value, use `rolename__role_varname` or `rolename__combined_varname` and assign all needed values.


## Tips and Tricks

### ansible_become: true

Don't use `become: true` in role playbooks. Instead, set `ansible_become: true` in your group_vars or host_vars (not in `all.yml` - `localhost` must not be part of the group).


### Re-use values which are defined in `rolename__group_varname` in `rolename__host_varname` without duplicating them

Nice trick for variables that get combined. Imagine you just want to add a single setting on a host, and want to avoid repeating all other settings (because if you do not specify them, they will be considered as "unset" on the host level). This is a real life example for the `linuxfabrik.lfops.login` role:

group var:
```yaml
login__group_users:
  - name: 'linuxfabrikadmin'
    state: 'present'
    additional_groups:
      - 'sudo'
    sshd_authorized_keys:
      - 'ssh-rsa ...'
      - 'ssh-rsa ...'
      - 'ssh-ed25519 ...'
      - 'ssh-ed25519 ...'
      - 'ssh-ed25519 ...'
```

host_var - add some group definitions for the user, but get all ssh keys from group vars (which is the first entry in `login__group_users`, therefore get item `0` from the `login__group_users` list):
```yaml
login__host_users:
  - name: 'linuxfabrikadmin'
    state: 'present'
    additional_groups:
      - 'adm'
      - 'cdrom'
      - 'dip'
      - 'lxd'
      - 'plugdev'
      - 'sudo'
    sshd_authorized_keys: '{{ login__group_users.0.sshd_authorized_keys }}'
```
