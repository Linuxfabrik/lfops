# Ansible Role linuxfabrik.lfops.repo_sury

This role deploys the [Sury repository](https://deb.sury.org/).

Runs on

* Debian11 (and compatible)


## Tags

| Tag         | What it does                |
| ---         | ------------                |
| `repo_sury` | Deploys the Sury Repository |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_sury__enabled_repos` | The package repos which should be enabled. If variable is unset, none of the Sury package repos will be activated. | unset |
| `repo_sury__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_sury__enabled_repos:
  - 'bind'
  - 'nginx'
  - 'php'
repo_sury__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
