# Ansible Role linuxfabrik.lfops.repo_grafana

This role deploys the Grafana OSS Repository.


## Tags

| Tag            | What it does                       |
| ---            | ------------                       |
| `repo_grafana` | Deploys the Grafana OSS Repository |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_baseos__basic_auth_login` | Use HTTP basic auth to login to the repository. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles. | `{{ lfops__repo_basic_auth_login \| default("") }}` |
| `repo_grafana__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_grafana__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_grafana__mirror_url: 'https://mirror.example.com'
```


## Troubleshooting

`Status code: 403 for https://rpm.grafana.com/repodata/repomd.xml (IP: 151.101.194.217)`: Unset `repo_grafana__basic_auth_login`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
