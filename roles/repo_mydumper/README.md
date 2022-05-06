# Ansible Role repo_mydumper

This role deploys a repository for the mydumper package. Note that no official repository exists - Linuxfabrik currently uses its own (non-public) server.

FQCN: linuxfabrik.lfops.repo_mydumper

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Requirements

This role does not have any requirements.


## Tags

| Tag           | What it does                    |
| ---           | ------------                    |
| repo_mydumper | Deploys the mydumper repository |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/repo_mydumper/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### repo_mydumper__baseurl

Set the URL to a custom mirror server providing the repository.

Default:
```yaml
repo_mydumper__baseurl: 'http://mirror.linuxfabrik.ch/mydumper/el/{{ ansible_facts["distribution_major_version"] }}'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
