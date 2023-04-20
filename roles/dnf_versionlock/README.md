# Ansible Role linuxfabrik.lfops.dnf_versionlock
This role installs and configures the [dnf versionlock plugin](https://dnf-plugins-core.readthedocs.io/en/latest/versionlock.html).

Runs on

* RHEL 7 (and compatible). Note that `yum versionlock` has less capabilites than the DNF variant.
* RHEL 8 (and compatible)


## Tags

| Tag               | What it does                            |
| ---               | ------------                            |
| `dnf_versionlock` | Installs and configures dnf versionlock |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `dnf_versionlock__versionlocks` | List of versionlock (<package-name-spec>) entries. Have a look at `man yum-versionlock` for RHEL7 or [dnf versionlock](https://dnf-plugins-core.readthedocs.io/en/latest/versionlock.html) for RHEL8. |

Example:
```yaml
# mandatory
dnf_versionlock__versionlocks:
  - 'enterprise-search-0:8.7.*' # pin to 8.7.x, only allowing patch updates. only works on RHEL8
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
