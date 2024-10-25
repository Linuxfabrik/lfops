# Ansible Role linuxfabrik.lfops.repo_opensearch

This role deploys the [Opensearch Package Repository](https://opensearch.org/docs/latest/opensearch/install/rpm/).


## Tags

| Tag            | What it does                           |
| ---            | ------------                           |
| `repo_opensearch` | Deploys the Opensearch Package Repository |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `repo_opensearch__version__host_var` / <br> `repo_opensearch__version__group_var` | The version of the Opensearch repository which should be installed.  <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). |

Example:
```yaml
# mandatory
repo_opensearch__version__host_var: '2.x'  # or '1.x'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_baseos__basic_auth_login` | Use HTTP basic auth to login to the repository. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles. | `{{ lfops__repo_basic_auth_login \| default("") }}` |
| `repo_opensearch__mirror_url` | String. Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_opensearch__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_opensearch__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
