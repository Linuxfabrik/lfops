# Ansible Role linuxfabrik.lfops.example

This role configures something using [example](https://example.com/). Currently, this role ...

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Fedora 35
* Fedora 36


## Mandatory Requirements

* Enable the [example repository](https://example.com/). This can be done using the [linuxfabrik.lfops.repo_example](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_example) role.
* Install EXAMPLE. This can be done using the [linuxfabrik.lfops.example](https://github.com/Linuxfabrik/lfops/tree/main/roles/example) role.
* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.

**Attention**

> Make sure that this condition is met.


## Optional Requirements

* Step 1
* Step 2


## Tags

| Tag                   | What it does                                 |
| ---                   | ------------                                 |
| `example`             | * step 1<br> * step 2                        |
| `example:configure`   | * step 1<br> * step 2                        |
| `example:script`      | * step 1<br> * step 2                        |
| `example:state`       | * step 1<br> * step 2                        |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `example__var1` | descr |

Example:
```yaml
# mandatory
example__var1: 'value'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `example__var2` | descr | `'default'` |

Example:
```yaml
# optional
example__var2: 'value'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
