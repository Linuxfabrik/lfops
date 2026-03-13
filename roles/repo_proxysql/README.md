# Ansible Role linuxfabrik.lfops.repo_proxysql

This role deploys the [ProxySQL Package Repository](https://proxysql.com/documentation/installing-proxysql/).


## Tags

| Tag            | What it does                           | Reload / Restart |
| ---            | ------------                           | ---------------- |
| `repo_proxysql` | Deploys the ProxySQL Package Repository | - |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `repo_proxysql__version__host_var` / <br> `repo_proxysql__version__group_var` | String. The version of the ProxySQL repository which should be installed.  <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). |

Example:
```yaml
# mandatory
repo_proxysql__version__host_var: '2.7'  # or '2.6', '2.5', '2.4', '2.3', '2.2'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_proxysql__basic_auth_login` | Dict. Use HTTP basic auth to login to the repository. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles. | `{{ lfops__repo_basic_auth_login \| default("") }}` |
| `repo_proxysql__mirror_url` | String. Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_proxysql__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_proxysql__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
