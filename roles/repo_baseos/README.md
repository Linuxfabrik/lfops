# Ansible Role linuxfabrik.lfops.repo_baseos

This role deploys the BaseOS repositories, which can be used to set a custom mirror server.

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Tags

| Tag           | What it does                    |
| ---           | ------------                    |
| `repo_baseos` | Deploys the BaseOS repositories |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_baseos__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles, or else to `''`. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_baseos__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
