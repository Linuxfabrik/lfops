# Ansible Role linuxfabrik.lfops.repo_gitlab_runner

This role deploys the GitLab Runner Repository.


## Tags

`repo_gitlab_runner`

* Deploys the GitLab Runner Repository.
* Triggers: none.


## Optional Role Variables

`repo_gitlab_runner__basic_auth_login`

* Use HTTP basic auth to login to the repository. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles.
* Type: String.
* Default: `'{{ lfops__repo_basic_auth_login | default("") }}'`

`repo_gitlab_runner__mirror_url`

* Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used.
* Type: String.
* Default: `'{{ lfops__repo_mirror_url | default("") }}'`

Example:
```yaml
# optional
repo_gitlab_runner__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_gitlab_runner__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
