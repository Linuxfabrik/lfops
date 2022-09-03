# Ansible Role linuxfabrik.lfops.ansible_init

`ansible-init` helps installing a working Ansible environment including roles from LFOps and a list Ansible inventories from various Git repositories.

This role:

* Updates ansible_init (`ansinv`) itself
* Updates LFOps
* Loads the list of Git repositories containing Ansible inventories
* Clones the inventories
* Installs recommended Ansible collections

Tested on

* Fedora 35
* Fedora 36



## Tags

| Tag           | What it does                                 |
| ---           | ------------                                 |
| `ansible_init` | * Update ansible_init (ansinv) itself<br>* Update ../lfops<br>* Load repo list<br>* Clone the inventories<br>* Install ansible collections |
| `ansible_init:command` | * Load repo list | 


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |

Example:
```yaml
# optional
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
