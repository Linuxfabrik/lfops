# Ansible Role repo_collabora_code

This role deploys the official [Collabora CODE Repository](https://docs.fedoraproject.org/en-US/collabora_code/).

FQCN: linuxfabrik.lfops.repo_collabora_code

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Requirements

This role does not have any requirements.

## Tags

| Tag                 | What it does                          |
| ---                 | ------------                          |
| repo_collabora_code | Deploys the Collabora CODE Repository |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/repo_collabora_code/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### repo_collabora_code__mirror_url

Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles, or else to `''`.

Default:
```yaml
repo_collabora_code__mirror_url: '{{ lfops__repo_mirror_url | default("") }}'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
