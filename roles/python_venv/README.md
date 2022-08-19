# Ansible Role linuxfabrik.lfops.python_venv

This role creates and manages various [Python 3 virtual environments (venv)](https://docs.python.org/3/library/venv.html). These are placed below `/opt/python-venv/` on the target system.

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Fedora 35


## Mandatory Requirements

* Install Python 3


## Tags

| Tag           | What it does                                 |
| ---           | ------------                                 |
| `python_venv` | Creates and manages the virtual environments |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `python_venv__host_venvs` /<br> `python_venv__group_venvs` | Dictionary containing definitions for the virtual environments. Subkeys:<br> * `exposed_binaries`: Optional, list. List of binaries which should be linked to `/usr/local/bin` for easier access on the command line. The binaries are expected to exist below `/opt/python-venv/name/bin/`.<br> * `name`: Mandatory, string. The name of the virtual environment. Will be used for the folder name below `/opt/python-venv`.<br> * `package_requirements`: Optional, list. These packages will be installed before installing the pip `packages` using the default package manager (e.g. `dnf`).<br> * `packages`: Mandatory, list. These packages will be installed in the virtual environment using `pip`.<br> * `system_site_packages`:  Optional, boolean. Defaults to `true`. Allows the virtual environment to access the system site-packages dir.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |

Example:
```yaml
# optional
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
python_venv__group_venvs: []
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
