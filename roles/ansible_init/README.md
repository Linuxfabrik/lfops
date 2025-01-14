# Ansible Role linuxfabrik.lfops.ansible_init

`ansible-init` helps installing a working Ansible environment including roles from LFOps and a list Ansible inventories from various Git repositories.

This role:

* Updates ansible_init (`ansinv`) itself
* Updates LFOps
* Loads the list of Git repositories containing Ansible inventories
* Clones the inventories
* Optionally clones the roles to `../roles/`
* Installs recommended Ansible collections


## Tags

| Tag            | What it does                                                                                                                                   |
| ---            | ------------                                                                                                                                   |
| `ansible_init` | * Update ansible_init (ansinv) itself<br> * Update ../lfops<br> * Load repo list<br> * Clone the inventories<br> * Install ansible collections |
| `ansible_init:collections` | Install ansible collections |
| `ansible_init:command` | Load repo list |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `ansible_init__url` | URL of the ansinv repo. |

Example:
```yaml
# mandatory
ansible_init__url: 'git@example.com:my-ansinv.git'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `ansible_init__ansible_collections` | List of dictionaries of Ansible collections to install. Subkeys: <br> * `name`: Mandatory, string. Name of the collection. <br> * `type`. Optional. Defaults to `collection`. One of `collection`, `role`, or `both`. | All collections required to use LFOps |
| `ansible_init__inventories` | List of dictionaries of inventories to clone. Subkeys: <br> * `name`: Mandatory, string. Name of the inventory. Will be used as the folder name. <br> * `url`: Mandatory, string. Git, SSH, or HTTP(S) protocol address of the repository. <br> * `version`: Optional, string. Defaults to `'main'`. Git version to checkout. | `[]` |
| `ansible_init__lfops_url` | URL of the LFOps repo. Either `'git@github.com:Linuxfabrik/lfops.git'` for development purposes, or `'https://github.com/Linuxfabrik/lfops.git'` for general access. | `'https://github.com/Linuxfabrik/lfops.git'` |
| `ansible_init__roles` | List of dictionaries of roles to clone. Subkeys: <br> * `name`: Mandatory, string. Name of the role. Will be used as the folder name. <br> * `url`: Mandatory, string. Git, SSH, or HTTP(S) protocol address of the repository. <br> * `version`: Optional, string. Defaults to `'main'`. Git version to checkout. | `[]` |
| `ansible_init__version` | Git version of the ansinv repo to checkout. | `'main'` |

Example:
```yaml
# optional
ansible_init__ansible_collections:
  - name: 'community.mysql'
  - name: 'ngine_io.cloudstack'
ansible_init__inventories: []
ansible_init__lfops_url: 'git@github.com:Linuxfabrik/lfops.git'
ansible_init__roles: []
ansible_init__version: 'main'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
