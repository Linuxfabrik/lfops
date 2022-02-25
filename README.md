# Ansible Collection of Roles, Playbooks and Plugins for managing Linux-based data centers

## Installation

To install the latest **stable** release:
```bash
ansible-galaxy collection install linuxfabrik.lfops
```

To install the latest **development** version:
```bash
# via HTTPS
ansible-galaxy collection install git+https://github.com/Linuxfabrik/lfops.git

# via SSH
ansible-galaxy collection install git@github.com:Linuxfabrik/lfops.git
```

To develop directly in the git repository:
```bash
git clone git@github.com:Linuxfabrik/lfops.git
mkdir -p ~/.ansible/collections/ansible_collections/linuxfabrik/
ln -s /path/to/lfops ~/.ansible/collections/ansible_collections/linuxfabrik/
```

## Documentation

The documentation for all plugins is available through `ansible-doc`. For example: `ansible-doc linuxfabrik.lfops.gpg_key` shows the documentation for the GPG key managing module.
