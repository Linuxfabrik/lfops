# Ansible Role linuxfabrik.lfops.repo_sury

This role deploys the [Sury repository](https://deb.sury.org/).


## Tags

`repo_sury`

* Deploys the Sury Repository.
* Triggers: none.


## Mandatory Role Variables

`repo_sury__enabled_repos`

* A list of package repos which should be enabled. If the list is empty, none of the Sury package repos will be activated. For a full list of possible repos, please check [Sury Packages](https://packages.sury.org).
* Type: List.

Example:
```yaml
# mandatory
repo_sury__enabled_repos:
  - 'bind'
  - 'nginx'
  - 'php'
```


## Optional Role Variables

`repo_sury__mirror_url`

* Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used.
* Type: String.
* Default: `'{{ lfops__repo_mirror_url | default("") }}'`

Example:
```yaml
# optional
repo_sury__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
