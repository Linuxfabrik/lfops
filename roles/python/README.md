# Ansible Role linuxfabrik.lfops.python

This role installs Python 2 or Python 3 on the system, optionally with additional modules.


## Tags

`python`

* This role installs Python on the system, optionally with additional modules.
* Triggers: none.


## Optional Role Variables

`python__modules__host_var` / `python__modules__group_var`

* List of dictionaries containing additional Python modules that should be installed via the OS package manager on Linux, or via pip on Windows. For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the packages.
        * Type: String.

    * `state`:

        * Optional. Either `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`python__version`

* The Python version to install. Possible options for Linux: `2`, `3`. Windows requires the full version (check the possible options [here](https://www.python.org/ftp/python/)).
* Type: Number.
* Default: `3`

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
