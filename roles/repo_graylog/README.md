# Ansible Role linuxfabrik.lfops.repo_graylog

This role deploys the [Graylog Repository](https://docs.graylog.org/docs/operating-system-packages). Although the Graylog project doesn't recommend to do that, LFOps prefers to install the repository configuration manually, because it's the only way to handle custom mirror servers.


## Tags

| Tag           | What it does                     |
| ---           | ------------                     |
| `repo_graylog` | Deploys the Graylog Repository |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `repo_graylog__version` | String. The Graylog repo version to install, in `'major.minor'` format. One of `'2.0'` through `'5.2'` as of 2024-03. [See the Graylog repository for a current list of available releases](https://www.graylog.org/releases). |

Example:
```yaml
# mandatory
repo_graylog__version: '5.2'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_baseos__basic_auth_login` | Use HTTP basic auth to login to the repository. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles. | `{{ lfops__repo_basic_auth_login \| default("") }}` |
| `repo_graylog__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url \| default("") }}'` |

Example:
```yaml
# optional
repo_graylog__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_graylog__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
