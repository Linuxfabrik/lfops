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


## Documentation

* Roles: Each role has its own README file.
* Plugins: The documentation for all plugins is available through `ansible-doc`. For example, `ansible-doc linuxfabrik.lfops.gpg_key` shows the documentation for the GPG key managing module.
