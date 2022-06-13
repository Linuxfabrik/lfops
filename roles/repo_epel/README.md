# Ansible Role repo_epel

This role deploys the [Extra Packages for Enterprise Linux (EPEL) Repository](https://docs.fedoraproject.org/en-US/epel/).

FQCN: linuxfabrik.lfops.repo_epel

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Requirements

### Mandatory

* Install `dnf-utils`. This can be done using the [linuxfabrik.lfops.yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag       | What it does                |
| ---       | ------------                |
| repo_epel | Deploys the EPEL Repository |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/repo_epel/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### repo_epel__mirror_url

Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles, or else to `''`.

Default:
```yaml
repo_epel__mirror_url: '{{ lfops__repo_mirror_url | default("") }}'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
