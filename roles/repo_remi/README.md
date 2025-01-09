# Ansible Role linuxfabrik.lfops.repo_remi

This role deploys the [Remi's RPM repository](https://rpms.remirepo.net/).


## Mandatory Requirements

* For RHEL7, install `yum-utils`. This can be done using the [linuxfabrik.lfops.yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils) role.


## Tags

| Tag         | What it does                |
| ---         | ------------                |
| `repo_remi` | Deploys the Remi Repository |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_remi__basic_auth_login` | Use HTTP basic auth to login to the repository. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles. | `{{ lfops__repo_basic_auth_login \| default("") }}` |
| `repo_remi__enabled_php_version` | The major version of php for which the repository should be enabled. If variable is unset, none of the remi-repo versions will be activated. | unset |
| `repo_remi__enabled_redis_version` | The major version of redis for which the repository should be enabled. If variable is unset, none of the remi-repo versions will be activated. | unset |
| `repo_remi__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_remi__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_remi__enabled_php_version: '8.1'
repo_remi__enabled_redis_version: '7.2'
repo_remi__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
