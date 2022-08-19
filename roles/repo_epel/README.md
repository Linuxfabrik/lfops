# Ansible Role linuxfabrik.lfops.repo_epel

This role deploys the [Extra Packages for Enterprise Linux (EPEL) Repository](https://docs.fedoraproject.org/en-US/epel/).

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Mandatory Requirements

* Install `dnf-utils`. This can be done using the [linuxfabrik.lfops.yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils) role.


## Tags

| Tag         | What it does                |
| ---         | ------------                |
| `repo_epel` | Deploys the EPEL Repository |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_epel__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles, or else to `''`. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_epel__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
