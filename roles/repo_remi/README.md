# Ansible Role repo_remi

This role deploys the [Remi's RPM repository](https://rpms.remirepo.net/).

FQCN: linuxfabrik.lfops.repo_remi

Tested on

* RHEL 8 (and compatible)
* Fedora 35


## Requirements

This role does not have any requirements.


## Tags

| Tag       | What it does                |
| ---       | ------------                |
| repo_remi | Deploys the Remi Repository |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/repo_remi/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### repo_remi__mirror_url

Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles, or else to `''`.

Default:
```yaml
repo_remi__mirror_url: '{{ lfops__repo_mirror_url | default("") }}'
```


#### repo_remi__enabled_php_version

The major version of php for which the repository should be enabled.

Default: unset

Example:
```yaml
repo_remi__enabled_php_version: 7.4
```


#### repo_remi__enabled_redis_version

The major version of redis for which the repository should be enabled.

Default: unset

Example:
```yaml
repo_remi__enabled_redis_version: 6.0
```




## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
