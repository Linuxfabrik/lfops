# Ansible Role linuxfabrik.lfops.repo_baseos

This role deploys the BaseOS repositories, which can be used to set a custom mirror server.


## Tags

`repo_baseos`

* Deploys the BaseOS repositories.
* Triggers: none.


## Optional Role Variables

`repo_baseos__basic_auth_login`

* Use HTTP basic auth to login to the repository. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles.
* Type: String.
* Default: `'{{ lfops__repo_basic_auth_login | default("") }}'`

`repo_baseos__crb_repo_enabled__host_var` / `repo_baseos__crb_repo_enabled__group_var`

* Whether the CRB repository should be enabled or not.
* Type: Bool.
* Default: `false`

`repo_baseos__mirror_url`

* Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used.
* Type: String.
* Default: `'{{ lfops__repo_mirror_url | default("") }}'`

Example:
```yaml
# optional
repo_baseos__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_baseos__crb_repo_enabled__host_var: true
repo_baseos__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
