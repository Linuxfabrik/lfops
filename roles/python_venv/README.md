# Ansible Role linuxfabrik.lfops.python_venv

This role creates and manages various [Python 3 virtual environments (venv)](https://docs.python.org/3/library/venv.html). These are placed below `/opt/python-venv/` on the target system.

Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* RHEL 9 (and compatible)
* Fedora 35
* Debian 11


## Mandatory Requirements

* Install Python 3
* On Rocky 9, the CRB Repo ("Code Ready Builder") needs to be enabled to be able to deploy `python3-virtualenv` - otherwise you'll get `nothing provides python3-wheel-wheel needed by python3-virtualenv-20.21.1-1.el9.noarch from epel`.


## Tags

| Tag           | What it does                                 |
| ---           | ------------                                 |
| `python_venv` | Creates and manages the virtual environments |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `python_venv__pip_cert` | Path to PEM-encoded CA certificate bundle. Set this to use the system CA store instead of pip's built-in certficates. See 'SSL Certificate Verification' in pip documentation for more information. | unset |
| `python_venv__venvs__host_var` / <br> `python_venv__venvs__group_var` | Dictionary containing definitions for the virtual environments. Subkeys: <ul><li>`exposed_binaries`: Optional, list. List of binaries which should be linked to `/usr/local/bin` for easier access on the command line. The binaries are expected to exist below `/opt/python-venv/name/bin/`.</li><li>`name`: Mandatory, string. The name of the virtual environment. Will be used for the folder name below `/opt/python-venv`.</li><li>`package_requirements`: Optional, list. These packages will be installed before installing the pip `packages` using the default package manager (e.g. `dnf`).</li><li>`packages`: Mandatory, list. These packages will be installed in the virtual environment using `pip`.</li><li>`system_site_packages`:  Optional, boolean. Defaults to `true`. Allows the virtual environment to access the system site-packages dir.</li><li>`python_executable`: Optional, string. The Python executable to use for the virtual environment. Defaults to `'python3'`.</li></ul><br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |

Example:
```yaml
# optional
python_venv__pip_cert: '/etc/pki/tls/certs/ca-bundle.crt' # system CA bundle on RHEL 8
python_venv__venvs__host_var:
  - name: 'clamav-fangfrisch'
    packages:
      - 'fangfrisch'
    exposed_binaries:
      - 'fangfrisch'
    package_requirements:
      - 'python39'
      - 'python39-devel'
    python_executable: 'python3.9'
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
python_venv__venvs__group_var: []
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
