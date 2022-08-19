# Ansible Role linuxfabrik.lfops.python

This role installs Python on the system, optionally with additional modules.

Tested on

* RHEL 8 (and compatible)


## Tags

| Tag      | What it does                                                                 |
| ---      | ------------                                                                 |
| `python` | This role installs Python on the system, optionally with additional modules. |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `python__host_modules` /<br> `python__group_modules` | List of additional Python modules that should be installed via the standard package manager.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `python__version` | The Python version to install. Possible options for Linux:<br> * 2<br> * 3<br> Windows requires the full version (check the possible options [here](https://www.python.org/ftp/python/)). | `3` |

Example:
```yaml
# optional
python__host_modules:
  - 'python3-psutil'
python__group_modules: []
python__version: 3
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
