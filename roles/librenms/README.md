# Ansible Role python_venv

This role creates and manages various [Python 3 virtual environments (venv)](https://docs.python.org/3/library/venv.html). These are placed below `/opt/python-venv/` on the target system.

FQCN: linuxfabrik.lfops.python_venv

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Fedora 35


## Requirements

### Mandatory

* Install Python 3


### Optional

This role does not have any optional requirements.


## Tags

| Tag         | What it does                                 |
| ---         | ------------                                 |
| python_venv | Creates and manages the virtual environments |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/python_venv/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### python_venv__host_venvs / python_venv__group_venvs

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

A list of dictionaries containing definitions for the virtual environments.

Subkeys:

* `exposed_binaries`: Optional, list. List of binaries which should be linked to `/usr/local/bin` for easier access on the command line. The binaries are expected to exist below `/opt/python-venv/name/bin/`.
* `name`: Mandatory, string. The name of the virtual environment. Will be used for the folder name below `/opt/python-venv`.
* `package_requirements`: Optional, list. These packages will be installed before installing the pip `packages` using the default package manager (e.g. `dnf`).
* `packages`: Mandatory, list. These packages will be installed in the virtual environment using `pip`.
* `system_site_packages`:  Optional, boolean. Defaults to `true`. Allows the virtual environment to access the system site-packages dir.

Default:
```yaml
python_venv__host_venvs: []
python_venv__group_venvs: []
```

Example:
```yaml
python_venv__host_venvs:
  - name: 'duplicity'
    packages:
      - 'duplicity'
      - 'python-swiftclient'
      - 'python-keystoneclient'
    package_requirements:
      - 'gcc'
      - 'librsync-devel'
    exposed_binaries:
      - 'duplicity'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
