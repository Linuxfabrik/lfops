# Ansible Role python

This role installs Python on the system, optionally with additional modules.

FQCN: linuxfabrik.lfops.python

Tested on

* RHEL 8 (and compatible)


## Requirements

This role does not have any requirements.


## Tags

| Tag    | What it does                                                                 |
| ---    | ------------                                                                 |
| python | This role installs Python on the system, optionally with additional modules. |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/python/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### python__version

The python version to install. Possible options for Linux:

* 2
* 3

Windows requires the full version (check the possible options [here](https://www.python.org/ftp/python/)).

Default:
```yaml
python__version: 3
```

Example:
```yaml
python__version: '3.10.4'
```


#### python__host_modules / python__group_modules

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

List of additional python modules that should be installed via the standard package manager.

Default:
```yaml
python__group_modules: []
python__host_modules: []
```

Example:
```yaml
python__host_modules:
  - 'python3-psutil'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
