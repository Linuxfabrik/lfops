# Ansible Role linuxfabrik.lfops.python

This role installs Python 2 or Python 3 on the system, optionally with additional modules.

Runs on

* RHEL 8 (and compatible)
* RHEL 9 (and compatible)
* Ubuntu 16


## Tags

| Tag      | What it does                                                                 |
| ---      | ------------                                                                 |
| `python` | This role installs Python on the system, optionally with additional modules. |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `python__modules__host_var` / `python__modules__group_var` | List of dictionaries containing additional Python modules that should be installed via the OS package manager. Subkeys: <ul><li>* `name`: String, mandatory. Name of the packages.</li><li>`state`: Optional, string. Either `present` or `absent`. Defaults to `present`.</li></ul><br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `python__version` | The Python version to install. Possible options for Linux:<br> * 2<br> * 3<br> Windows requires the full version (check the possible options [here](https://www.python.org/ftp/python/)). | `3` |

Example:
```yaml
# optional
python__modules__host_var:
  - name: 'python3-psutil'
    state: 'absent'
  - name: 'python3-requests'
    state: 'present'
python__modules__group_var: []
python__version: 3
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
