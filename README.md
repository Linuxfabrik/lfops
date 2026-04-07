<h1 align="center">
  Linuxfabrik LFOps
</h1>
<p align="center">
  Ansible Collection of roles, playbooks & plugins for Linux-based cloud infrastructure. Covers OS hardening, MariaDB, Icinga2, Nextcloud, FreeIPA, KVM & more. Bitwarden & Cloud integration.
  <span>&#8226;</span>
  <b>made by <a href="https://linuxfabrik.ch/">Linuxfabrik</a></b>
</p>
<div align="center" id="badges"> <!-- Do not change this line. It is used by .github/workflows/lf-build.yml to strip badges before publishing to Galaxy. -->

![GitHub Stars](https://img.shields.io/github/stars/linuxfabrik/lfops)
![License](https://img.shields.io/github/license/linuxfabrik/lfops)
![Version](https://img.shields.io/github/v/release/linuxfabrik/lfops?sort=semver)
![Ansible](https://img.shields.io/badge/ansible--core-≥2.16-EE0000)
![Platforms](https://img.shields.io/badge/Platforms-RHEL%20%7C%20Debian%20%7C%20Ubuntu-informational)
![GitHub Issues](https://img.shields.io/github/issues/linuxfabrik/lfops)
[![Galaxy](https://img.shields.io/badge/Galaxy-linuxfabrik.lfops-blue)](https://galaxy.ansible.com/ui/repo/published/linuxfabrik/lfops/)
[![GitHubSponsors](https://img.shields.io/github/sponsors/Linuxfabrik?label=GitHub%20Sponsors)](https://github.com/sponsors/Linuxfabrik)
[![PayPal](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=7AW3VVX62TR4A&source=url)

</div>

<br />

# LFOps

LFOps is a comprehensive Ansible Collection providing 145+ playbooks and 160+ roles to bootstrap and manage Linux-based IT infrastructures. It covers the full server lifecycle -- from initial provisioning and hardening to application deployment, monitoring, and automated backups. LFOps supports RHEL 8/9/10, Debian, and Ubuntu.


## Table of Contents

* [Requirements](#requirements)
* [Installation](#installation)
    * [Using ansible-galaxy](#using-ansible-galaxy)
    * [Development Setup](#development-setup)
* [Mitogen](#mitogen)
    * [Mitogen with ansible-playbook](#mitogen-with-ansible-playbook)
    * [Mitogen with ansible-navigator](#mitogen-with-ansible-navigator)
    * [Mitogen Compatibility](#mitogen-compatibility)
* [Using ansible-navigator](#using-ansible-navigator)
* [Usage](#usage)
    * [Running a Playbook](#running-a-playbook)
    * [Typical Workflow Example](#typical-workflow-example)
    * [The "all" Playbook](#the-all-playbook)
    * [Skipping Roles in a Playbook](#skipping-roles-in-a-playbook)
* [Configuration](#configuration)
    * [Recommended ansible.cfg](#recommended-ansiblecfg)
    * [LFOps-wide Variables](#lfops-wide-variables)
    * [Bitwarden Integration](#bitwarden-integration)
* [Documentation](#documentation)
* [Compatibility](#compatibility)
* [Tips, Tricks & Troubleshooting](#tips-tricks--troubleshooting)
* [Contributing](#contributing)
* [License](#license)


## Requirements

* **Ansible**: ansible-core >= 2.16
* **Python on the controller**: >= 3.10 (ansible-core 2.16/2.17) or >= 3.11 (ansible-core 2.18)
* **Python on managed nodes**: >= 3.6
* **Dependencies**: The collection depends on several community collections (see [`requirements.yml`](requirements.yml)). These are installed automatically when using `ansible-galaxy`.

**Which ansible-core version should I use?**

| ansible-core | Controller Python | Managed Node Python | RHEL 8 (Python 3.6) |
|--------------|-------------------|---------------------|----------------------|
| 2.16         | 3.10 -- 3.12      | 3.6 -- 3.12        | works out of the box |
| 2.17         | 3.10 -- 3.12      | 3.7 -- 3.12        | needs Python >= 3.7  |
| 2.18         | 3.11 -- 3.14      | 3.8 -- 3.13        | needs Python >= 3.8  |

If you manage RHEL 8 hosts with the default system Python (3.6), use **ansible-core 2.16**. If all your managed nodes have Python >= 3.8 (e.g. RHEL 9+, Debian 12+, Ubuntu 22.04+), you can use **ansible-core 2.18** for the latest features.


## Installation

### Using ansible-galaxy

```bash
# Install the collection and its dependencies
ansible-galaxy collection install linuxfabrik.lfops

# Alternatively, install from Git directly
ansible-galaxy collection install git+https://github.com/Linuxfabrik/lfops.git
```

To install the dependencies separately:

```bash
ansible-galaxy collection install -r requirements.yml
```

### Development Setup

If you want to contribute or test local changes, clone the repository and symlink it into Ansible's collection path:

```bash
git clone git@github.com:Linuxfabrik/lfops.git /path/to/lfops

mkdir -p ~/.ansible/collections/ansible_collections/linuxfabrik
ln -s /path/to/lfops ~/.ansible/collections/ansible_collections/linuxfabrik/lfops
```

**Important**: The symlink target must be named `lfops` and point to the cloned repository root (which contains the `galaxy.yml`).

To verify the collection is detected:

```bash
ansible-galaxy collection list | grep linuxfabrik
```


## Mitogen

[Mitogen](https://mitogen.networkgenomics.com/ansible_detailed.html) is an optional but recommended performance optimization for Ansible. It replaces the default SSH-based task execution with a persistent Python-to-Python channel, significantly reducing connection overhead and speeding up playbook runs.

### Mitogen with ansible-playbook

Install Mitogen into your Ansible virtual environment:

```bash
pip install mitogen
```

Determine the strategy plugins path (this depends on the Python version in your venv):

```bash
python3 -c "import os, ansible_mitogen; print(os.path.join(ansible_mitogen.__path__[0], 'plugins', 'strategy'))"
```

Add the output to your `ansible.cfg`:

```ini
[defaults]
strategy_plugins = /path/to/venv/lib/pythonX.Y/site-packages/ansible_mitogen/plugins/strategy
strategy = mitogen_linear
```

Since the `strategy_plugins` path contains the Python version, it differs per venv. If you use multiple venvs (e.g. ansible-core 2.16 and 2.18), either use separate `ansible.cfg` files or install Mitogen to a shared location:

```bash
pip install --target=/opt/mitogen mitogen
```

```ini
[defaults]
strategy_plugins = /opt/mitogen/ansible_mitogen/plugins/strategy
strategy = mitogen_linear
```

**Important**: Do not set `ANSIBLE_STRATEGY=mitogen_linear` via shell aliases or environment variables. This is hard to debug and overrides the config file silently. Always configure Mitogen in `ansible.cfg`.

### Mitogen with ansible-navigator

The LFOps [Execution Environment](#using-ansible-navigator) container image already includes Mitogen with the strategy plugins available at `/opt/mitogen/ansible_mitogen/plugins/strategy`. To enable it, add the following to the `ansible.cfg` used by ansible-navigator:

```ini
[defaults]
strategy_plugins = /opt/mitogen/ansible_mitogen/plugins/strategy
strategy = mitogen_linear
```

### Mitogen Compatibility

| ansible-core | Mitogen  | Controller Python |
|--------------|----------|-------------------|
| 2.16         | >= 0.3.7 | 3.10 -- 3.14      |
| 2.17         | >= 0.3.7 | 3.10 -- 3.14      |
| 2.18         | >= 0.3.7 | 3.11 -- 3.14      |

Always keep Mitogen up to date (`pip install --upgrade mitogen`). If you encounter `SyntaxError: future feature annotations is not defined`, either the Mitogen version is outdated or the Python version on the remote host is too old (< 3.7).


## Using ansible-navigator

LFOps provides a pre-built Execution Environment (EE) container image that includes all dependencies:

```bash
pip install ansible-navigator
```

Configure `ansible-navigator.yml` in your project directory:

```yaml
ansible-navigator:
  execution-environment:
    container-engine: podman # or docker
    enabled: true
    image: ghcr.io/linuxfabrik/lfops_ee:latest
    pull:
      policy: missing
  mode: stdout
```

Then run playbooks using `ansible-navigator` instead of `ansible-playbook`:

```bash
ansible-navigator run linuxfabrik.lfops.setup_basic \
  --inventory path/to/inventory \
  --limit myhost
```

The EE is based on Rocky Linux 9 with ansible-core 2.16, Python 3.11, and includes Mitogen for accelerated execution. See [`execution-environment.yml`](execution-environment.yml) for the full build definition. Public container images are available on [GitHub Container Registry](https://github.com/Linuxfabrik/lfops/pkgs/container/lfops_ee).


## Usage

### Running a Playbook

Each playbook requires the target host to be in a specific inventory group named `lfops_<playbook_name>`. For example, to run the `php` playbook against `myhost`:

1. Add the host to the `lfops_php` group in your inventory.
2. Run the playbook:

```bash
ansible-playbook linuxfabrik.lfops.php \
  --inventory path/to/inventory \
  --limit myhost
```

Use `--diff` to see changes, `--check` for dry-run mode, and `--tags` to run specific parts of a playbook.

### Typical Workflow Example

Add your host to the required groups in the inventory:

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

Then run the playbooks in order:

```bash
# Provision the VM
ansible-playbook --inventory path/to/inventory linuxfabrik.lfops.hetzner_vm --limit myhost

# Basic setup (hardening, SSH, firewall, chrony, etc.)
ansible-playbook --inventory path/to/inventory linuxfabrik.lfops.setup_basic --limit myhost

# Deploy monitoring
ansible-playbook --inventory path/to/inventory linuxfabrik.lfops.monitoring_plugins --limit myhost

# Deploy a full application stack (playbooks prefixed by "setup_" include all dependencies)
ansible-playbook --inventory path/to/inventory linuxfabrik.lfops.setup_nextcloud --limit myhost

# Change specific settings afterwards, e.g. PHP
ansible-playbook --inventory path/to/inventory linuxfabrik.lfops.setup_nextcloud --limit myhost --tags php
```

### The "all" Playbook

The `linuxfabrik.lfops.all` playbook imports all other playbooks. This is useful when a change affects multiple playbooks. For example, to deploy an updated MariaDB dump script to all hosts that have MariaDB (whether installed directly or as part of WordPress, Nextcloud, etc.):

```bash
ansible-playbook --inventory path/to/inventory linuxfabrik.lfops.all --tags mariadb_server --limit myhost
```

**Always** use `--tags` and `--limit` with the `all` playbook.

### Skipping Roles in a Playbook

The playbooks support skipping individual roles using inventory variables. For example, to skip the firewall role in `setup_basic`:

```yaml
setup_basic__skip_firewall: true
```

In playbooks that support role injections (like `setup_icinga2_master`), there are two variables:

* `playbook_name__role_name__skip_role`: Skips the role and disables the role's injections. Have a look at the playbook for the default value.
* `playbook_name__role_name__skip_role_injections`: Disables or re-enables the role's injections. Takes priority over `playbook_name__role_name__skip_role`. Defaults to `playbook_name__role_name__skip_role` for ease of use. Have a look at the playbook for the affected injections.


## Configuration

### Recommended ansible.cfg

Place an `ansible.cfg` in your inventory/project directory:

```ini
[defaults]
forks = 30
gathering = smart
fact_caching = jsonfile
fact_caching_connection = ~/.ansible_cache
fact_caching_timeout = 86400
host_key_checking = False
inventory_ignore_extensions = ~, .orig, .bak, .ini, .cfg, .retry, .pyc, .pyo, .csv, .md
inventory_ignore_patterns = '(host|group)_files'
nocows = 1
retry_files_enabled = False
strategy_plugins = /path/to/ansible_mitogen/plugins/strategy  ; see "Mitogen" section
strategy = mitogen_linear
timeout = 15

[ssh_connection]
pipelining = True
ssh_args = -o ControlMaster=auto -o ControlPersist=60s
```

### LFOps-wide Variables

It would sometimes be convenient to allow the user to set a default for multiple roles. However, since we strictly prefix all our variables with the role name, this is not that straightforward. Instead, we provide a handful of variables prefixed with `lfops__` that act as the default for multiple roles. It is, of course, still possible to overwrite the LFOps-wide variable with the role-specific one (for example, the value of `icingaweb2_module_director__monitoring_plugins_version` takes precedence over that of `lfops__monitoring_plugins_version`).

#### `lfops__monitoring_plugins_version`

This variable is used as the default whenever the version of the [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins) is required. For example, it is used to deploy the correct version of the Director Basket and Grafana Dashboards in the `icingaweb2_module_director` and `icingaweb2_module_grafana` roles, respectively. For documentation of the value, have a look at the `monitoring_plugins__version` variable in the [monitoring_plugins role README](https://github.com/Linuxfabrik/lfops/blob/main/roles/monitoring_plugins/README.md).

```yaml
lfops__monitoring_plugins_version: 'dev'
```

#### `lfops__remove_rpmnew_rpmsave`

This variable aims to simplify the management of rpmnew and rpmsave files (and their Debian equivalents) by allowing the admin to remove them with LFOps. The workflow would be to adjust the template in LFOps according to the new config file, then deploy with `--extra-vars='lfops__remove_rpmnew_rpmsave=true'` to update the config and remove the rpmnew / rpmsave in one run.

#### `lfops__repo_basic_auth_login`

This variable is used as the default across all `repo_*` roles if it is set. Can be used to authenticate against the repository server using HTTP basic auth. Have a look at the respective role's README for details.

Note: Currently this only works for RPM repositories.

```yaml
lfops__repo_basic_auth_login:
  username: 'mirror-user'
  password: 'linuxfabrik'
```

#### `lfops__repo_mirror_url`

This variable is used as the default across all `repo_*` roles if it is set. Can be used to set the URL to a custom mirror server providing the repository. Have a look at the respective role's README for details.

```yaml
lfops__repo_mirror_url: 'https://mirror.example.com'
```

### Bitwarden Integration

LFOps includes a Bitwarden lookup plugin that fetches secrets from your vault (and creates items if they do not exist). Requires the [bw CLI](https://bitwarden.com/help/article/cli/) version v2022.9.0+.

Usage example in your inventory:

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

Before running Ansible, unlock your vault and start the Bitwarden API server:

```bash
export BW_SESSION="$(bw unlock --raw)"
bw status | jq
bw serve --hostname 127.0.0.1 --port 8087 &
```

The lookup returns multiple keys, including `username` and `password`. To get only the password:

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

**Note**: When using the lookup in `group_vars`, avoid `inventory_hostname` if you want a shared credential (e.g. one password for all FreeIPA clients). Instead, use the actual server hostname:

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

See `ansible-doc -t lookup linuxfabrik.lfops.bitwarden_item` for all options.


## Documentation

Full documentation is available at [linuxfabrik.github.io/lfops](https://linuxfabrik.github.io/lfops/). It is automatically built and deployed on every push to `main`.

* **Ansible Roles**: Each role has its own README file in [`roles/<role_name>/`](roles/).
* **Ansible Plugins**: Available through `ansible-doc`. For example: `ansible-doc linuxfabrik.lfops.gpg_key`.
* **Changelog**: [CHANGELOG.md](CHANGELOG.md)
* **Compatibility**: [COMPATIBILITY.md](COMPATIBILITY.md)
* **Contributing**: [CONTRIBUTING.rst](CONTRIBUTING.rst)
* **Issue Tracker**: [GitHub Issues](https://github.com/Linuxfabrik/lfops/issues)


## Compatibility

Which Ansible role is proven to run on which OS? See [COMPATIBILITY.md](https://github.com/Linuxfabrik/lfops/blob/main/COMPATIBILITY.md).


## Tips, Tricks & Troubleshooting

**Q: Where should I set `ansible_become: true`?**

Don't use `become: true` in role playbooks. Instead, set `ansible_become: true` in your group_vars or host_vars only (not in `all.yml` -- `localhost` must not be part of the group, otherwise you'll get errors like `sudo: a password is required`).


**Q: How do I find all groups a host belongs to?**

```bash
ansible --inventory path/to/inventory myhost -m debug -a "var=group_names"
```


**Q: How do I connect as an unprivileged user?**

Make sure the user is allowed to switch to all other accounts, not just root. Otherwise tasks using `become_user: 'apache'` etc. will fail. The sudoers entry must use `(ALL)`:

```
ansible-user ALL=(ALL) NOPASSWD: ALL
```


**Q: How do I find out which playbooks ran against a host?**

All playbooks log every run to `/var/log/linuxfabrik-lfops.log` on the target host:

```
2024-05-23 11:15:26.604794 - Playbook linuxfabrik.lfops.apps: START
2024-05-23 11:15:32.877064 - Playbook linuxfabrik.lfops.apps: END
```


**Q: Debian: `No package matching '...' is available`**

Run `apt update` before running the specific role.


**Q: `[WARNING]: Collection x.y does not support Ansible version 2.16.xx`**

Install a newer Ansible version and update all collections:

```bash
python3 -m venv ~/venvs/ansible-2.18
source ~/venvs/ansible-2.18/bin/activate
pip install --upgrade pip
pip install 'ansible-core~=2.18.0'

ansible-galaxy collection install -r requirements.yml --upgrade
```


**Q: `error creating bridge interface ...: Numerical result out of range`**

On Linux an interface name must not exceed 15 characters. Choose a shorter bridge name.


## Contributing

See [CONTRIBUTING.rst](CONTRIBUTING.rst) for guidelines.


## License

This project is licensed under the [Unlicense](https://unlicense.org/).
