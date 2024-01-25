# Ansible Role linuxfabrik.lfops.repo_monitoring_plugins

This role deploys the repository at repo.linuxfabrik.ch for the Linuxfabrik Monitoring Plugins.

Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Debian 10
* Debian 11
* Ubuntu 18.04
* Ubuntu 20.04
* Ubuntu 22.04


## Tags

| Tag                       | What it does                              |
| ---                       | ------------                              |
| `repo_monitoring_plugins` | Deploys the Monitoring Plugins repository |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_baseos__basic_auth_login` | Use HTTP basic auth to login to the repository. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles. | `{{ lfops__repo_basic_auth_login \| default("") }}` |
| `repo_monitoring_plugins__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_monitoring_plugins__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_monitoring_plugins__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
