# Ansible Role linuxfabrik.lfops.repo_monitoring_plugins

This role deploys the repository at repo.linuxfabrik.ch for the Linuxfabrik Monitoring Plugins.


*Available since LFOps `2.0.0`.*


## Tags

`repo_monitoring_plugins`

* Deploys the Monitoring Plugins repository.
* Triggers: none.


## Optional Role Variables

`repo_monitoring_plugins__basic_auth_login`

* Use HTTP basic auth to login to the repository. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles.
* Type: String.
* Default: `'{{ lfops__repo_basic_auth_login | default("") }}'`

`repo_monitoring_plugins__mirror_url`

* Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used.
* Type: String.
* Default: `'{{ lfops__repo_mirror_url | default("") }}'`

`repo_monitoring_plugins__testing`

* If `true`, switch to the `testing` channel: the `release` repository is disabled and the `testing` repository is enabled. On Debian/Ubuntu, the `-release` suffix in the apt sources file is replaced with `-testing`. By default, the `release` channel is used.
* Type: Boolean.
* Default: `false`

Example:
```yaml
# optional
repo_monitoring_plugins__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_monitoring_plugins__mirror_url: 'https://mirror.example.com'
repo_monitoring_plugins__testing: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
