# LFOps - Ansible Collection of Roles, Playbooks and Plugins for managing Linux-based Cloud Infrastructures

## The Purpose of LFOps

LFOps is like [DebOps](https://docs.debops.org/) a collection of *Free and Open Source tools that allow users to bootstrap and manage an IT infrastructure based on* RHEL and other operating systems. *Ansible is used as the main configuration management platform.* LFOps *provides a collection of Ansible roles that manage various services, as well as a set of Ansible playbooks that tie them together in a highly integrated environment.*

LFOps is designed to be used within the Linuxfabrik. Nevertheless, we try to keep its general-purpose as much as possible.


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
ansible-playbook --inventory path/to/inventory linuxfabrik.lfops.php --limit myhost
```

For more details on group names, Ansible tags, etc., see the playbooks and README files for the roles.


## A typical Workflow Example

First, add `myhost` to the corresponding groups in your Ansible inventory.

```yaml
[lfops_hetzner_vm]
myhost

[lfops_setup_basic]
myhost

[lfops_monitoring_plugins]
myhost

[lfops_setup_nextcloud]
myhost
```

After that run the corresponding playbooks (optionally append parameters like `--diff` and/or `--check`):

```bash
ansible-playbook --inventory path/to/inventory linuxfabrik.lfops.hetzner_vm --limit myhost
```

Run the basic setup:

```bash
ansible-playbook --inventory path/to/inventory linuxfabrik.lfops.setup_basic --limit myhost
```

Deploy a component:

```bash
ansible-playbook --inventory path/to/inventory linuxfabrik.lfops.monitoring_plugins --limit myhost
```

Deploy a full-fledged application (playbooks for complex application setups are prefixed by `setup_`):

```bash
ansible-playbook --inventory path/to/inventory linuxfabrik.lfops.setup_nextcloud --limit myhost
```

Change some settings afterwards, for example in PHP:

```bash
ansible-playbook --inventory path/to/inventory linuxfabrik.lfops.setup_nextcloud --limit myhost --tags php
```


## Compatibility List

Which Ansible role is proven to run on which OS? See [COMPATIBILTY](https://github.com/Linuxfabrik/LFOps/blob/main/COMPATIBILITY.md)


## Bitwarden

Requires the [bw CLI](https://bitwarden.com/help/article/cli/) version v2022.9.0+.

If you want to use Bitwarden as your password manager backend, do a `lookup` in your inventory like this:

```yaml
grafana_grizzly__grafana_service_account_login:
  "{{ lookup('linuxfabrik.lfops.bitwarden_item',
    {
      'hostname': inventory_hostname,
      'purpose': 'Grafana Service Account Token',
      'username': 'grizzly',
      'collection_id': lfops__bitwarden_collection_id,
      'organization_id': lfops__bitwarden_organization_id,
    },
  ) }}"
```

Before running Ansible, unlock the access to your Bitwarden vault and start the Bitwarden RESTful API webserver as follows:

```bash
export BW_SESSION="$(bw unlock --raw)"
bw status | jq
bw serve --hostname 127.0.0.1 --port 8087 &
```

After that run your playbook as usual:

```bash
ansible-playbook ...
```

The LFOps Bitwarden module will fetch the item from the vault and create it if it does not exist. See `ansible-doc -t lookup linuxfabrik.lfops.bitwarden_item` for all the details.

The lookup normally returns multiple keys, including the `username` and `password` subkeys. If only the password is required, use the following lookup:

```yaml
freeipa_server__directory_manager_password:
  "{{ lookup('linuxfabrik.lfops.bitwarden_item',
    {
      'hostname': inventory_hostname,
      'purpose': 'FreeIPA',
      'username': 'cn=Directory Manager',
      'collection_id': lfops__bitwarden_collection_id,
      'organization_id': lfops__bitwarden_organization_id,
    },
  )['password'] }}"
```

Beware that if you are using the lookup in `group_vars`, you probably do not want to use inventory_hostname. For example, the following would create a new login for each FreeIPA client:

```yaml
freeipa_server__ipa_admin_password:
  "{{ lookup('linuxfabrik.lfops.bitwarden_item',
    {
      'hostname': inventory_hostname,
      'purpose': 'FreeIPA',
      'username': 'admin',
      'collection_id': lfops__bitwarden_collection_id,
      'organization_id': lfops__bitwarden_organization_id,
    },
  )['password'] }}"
```

Instead, replace `inventory_hostname` with the correct FreeIPA server hostname:

```yaml
freeipa_server__ipa_admin_password:
  "{{ lookup('linuxfabrik.lfops.bitwarden_item',
    {
      'hostname': 'freeipa.example.com',
      'purpose': 'FreeIPA',
      'username': 'admin',
      'collection_id': lfops__bitwarden_collection_id,
      'organization_id': lfops__bitwarden_organization_id,
    },
  )['password'] }}"
```


## Documentation

* Ansible Roles: Each role has its own README file.
* Ansible Plugins: The documentation for all plugins is available through `ansible-doc`. For example, `ansible-doc linuxfabrik.lfops.gpg_key` shows the documentation for the GPG key managing module.


## The "all" Playbook

Imagine that you want to deploy an updated MariaDB dump script to all hosts that have a MariaDB server. This would mean that you would need to run not only the `linuxfabrik.lfops.mariadb_server` playbook, but also all playbooks that include MariaDB Server, e.g. `linuxfabrik.lfops.setup_wordpress`, etc. To simplify this, you can simply use the `linuxfabrik.lfops.all` playbook, which imports all other playbooks. Make sure you use it with `--tags` and `--limit` to get the desired effect.


## LFOps-wide Variables

There are a handful of variables that are used across roles. It is still possible to overwrite the LFOps-wide variable with the role-specific one.

### `lfops__monitoring_plugins_version`

This variable is used as the default whenever the version of the [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins) repo is required. Have a look at the [monitoring_plugins Role README](https://github.com/Linuxfabrik/lfops/blob/main/roles/monitoring_plugins/README.md) for details.

Example:
```yaml
lfops__monitoring_plugins_version: 'main'
```

### `lfops__repo_basic_auth_login`

This variable is used as the default across all `repo_*` roles if it is set. Can be used to authenticate against the repository server using HTTP basic auth. Have a look at the respective role's README for details.

Note: Currently this only works for RPM repositories.

Example:
```yaml
lfops__repo_basic_auth_login:
  username: 'mirror-user'
  password: 'linuxfabrik'
```

### `lfops__repo_mirror_url`

This variable is used as the default across all `repo_*` roles if it is set. Can be used to set the URL to a custom mirror server providing the repository. Have a look at the respective role's README for details.

Example:
```yaml
lfops__repo_mirror_url: 'https://mirror.example.com'
```

## Tips, Tricks & Troubleshooting

### ansible_become: true

Don't use `become: true` or `ansible_become: true` in role playbooks. Instead, set `ansible_become: true` in your group_vars or host_vars ONLY (not in `all.yml` - `localhost` must not be part of the group. Otherwise you'll get errors like `sudo: a password is required`).


### Finding all groups a host belongs to

When running playbooks against a host it might be useful to know all the group memberships.

```bash
ansible --inventory path/to/inventory myhost -m debug -a "var=group_names"
```

### Connecting as an unprivileged user, correct sudoers config

When connecting as an unprivileged user, you must make sure that the user is allowed to change to all other user accounts, not just root.
Otherwise it will be impossible to run tasks as other unprivileged users, for example `become_user: 'apache'`.
This means that the Runas_Spec in sudoers must be `(ALL)`, for example:

```
ansible-user ALL=(ALL) NOPASSWD: ALL
```
or
```
ansible-user ALL=(ALL) ALL
```
