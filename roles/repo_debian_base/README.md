# Ansible Role linuxfabrik.lfops.repo_debian_base

This role deploys the basic Debian repositories, which can be used to set a custom mirror server.

Runs on

* Debian 11 (and compatible)


## Tags

| Tag           | What it does                    |
| ---           | ------------                    |
| `repo_debian_base` | Deploys the basic Debian repositories |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_debian_base__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_debian_base__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
