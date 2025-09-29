# Ansible Role linuxfabrik.lfops.repo_mongodb

This role deploys the MongoDB repository.


## Tags

| Tag            | What it does                   | Reload / Restart |
| ---            | ------------                   | ---------------- |
| `repo_mongodb` | Deploys the MongoDB repository | - |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `repo_mongodb__version` | The MongoDB repo version to install. [Have a look at the MongoDB repository for the list of available releases](https://repo.mongodb.org/yum/redhat/8/mongodb-org/). |

Example:
```yaml
# mandatory
repo_mongodb__version: '6.0'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_mongodb__basic_auth_login` | Use HTTP basic auth to login to the repository. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles. | `{{ lfops__repo_basic_auth_login \| default("") }}` |
| `repo_mongodb__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_mongodb__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_mongodb__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
