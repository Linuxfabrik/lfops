# Ansible Role linuxfabrik.lfops.ansible_init

`ansible-init` helps installing a working Ansible environment including roles from LFOps and a list Ansible inventories from various Git repositories.

This role:

* Updates ansible_init (`ansinv`) itself
* Updates LFOps
* Loads the list of Git repositories containing Ansible inventories
* Clones the inventories
* Optionally clones the roles to `../roles/`
* Installs recommended Ansible collections (from LFOps `requirements.txt`)


## Tags

`ansible_init`

* Update ansible_init (ansinv) itself.
* Update ../lfops.
* Load repo list.
* Clone the inventories.
* Install ansible collections.
* Triggers: none.

`ansible_init:collections`

* Install ansible collections.
* Triggers: none.

`ansible_init:command`

* Load repo list.
* Triggers: none.


## Mandatory Role Variables

`ansible_init__url`

* URL of the ansinv repo.
* Type: String.
* Default: none

Example:

```yaml
# mandatory
ansible_init__url: 'git@example.com:my-ansinv.git'
```


## Optional Role Variables

`ansible_init__ansible_collections`

* List of dictionaries of Ansible collections to install.
* Subkeys:

    * `name`:

        * Mandatory. Name of the collection.
        * Type: String.

    * `type`:

        * Optional. One of `collection`, `role`, or `both`.
        * Type: String.
        * Default: `'collection'`

* Type: List of dictionaries.
* Default: `[]`

`ansible_init__inventories`

* List of dictionaries of inventories to clone.
* Subkeys:

    * `name`:

        * Mandatory. Name of the inventory. Will be used as the folder name.
        * Type: String.

    * `url`:

        * Mandatory. Git, SSH, or HTTP(S) protocol address of the repository.
        * Type: String.

    * `version`:

        * Optional. Git version to checkout.
        * Type: String.
        * Default: `'main'`

* Type: List of dictionaries.
* Default: `[]`

`ansible_init__lfops_url`

* URL of the LFOps repo. Either `'git@github.com:Linuxfabrik/lfops.git'` for development purposes, or `'https://github.com/Linuxfabrik/lfops.git'` for general access.
* Type: String.
* Default: `'https://github.com/Linuxfabrik/lfops.git'`

`ansible_init__roles`

* List of dictionaries of roles to clone.
* Subkeys:

    * `name`:

        * Mandatory. Name of the role. Will be used as the folder name.
        * Type: String.

    * `url`:

        * Mandatory. Git, SSH, or HTTP(S) protocol address of the repository.
        * Type: String.

    * `version`:

        * Optional. Git version to checkout.
        * Type: String.
        * Default: `'main'`

* Type: List of dictionaries.
* Default: `[]`

`ansible_init__version`

* Git version of the ansinv repo to checkout.
* Type: String.
* Default: `'main'`

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
