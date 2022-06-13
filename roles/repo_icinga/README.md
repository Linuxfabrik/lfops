# Ansible Role repo_icinga

This role deploys the [Icinga Package Repository](https://packages.icinga.com/).

FQCN: linuxfabrik.lfops.repo_icinga

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Requirements

This role does not have any requirements.


## Tags

| Tag         | What it does                          |
| ---         | ------------                          |
| repo_icinga | Deploys the Icinga Package Repository |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/repo_icinga/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### repo_icinga__mirror_url

Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles, or else to `''`.

Default:
```yaml
repo_icinga__mirror_url: '{{ lfops__repo_mirror_url | default("") }}'
```


#### repo_icinga__subscription_login

The [Icinga Repository Subscription](https://icinga.com/subscription/) account.

Default: unset

Example
```yaml
repo_icinga__subscription_login:
  username: 'my-username'
  password: 'my-secret-password'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
