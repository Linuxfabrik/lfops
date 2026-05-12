# Ansible Role linuxfabrik.lfops.repo_google_chrome

This role deploys the package repository for [Google Chrome](https://www.google.com/chrome/) on RHEL-based distributions.


*Available since LFOps `6.0.2`.*


## Tags

`repo_google_chrome`

* Deploys the Google Chrome Repository.
* Triggers: none.


## Optional Role Variables

`repo_google_chrome__basic_auth_login`

* Use HTTP basic auth to login to the repository. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles.
* Type: String.
* Default: `'{{ lfops__repo_basic_auth_login | default("") }}'`

`repo_google_chrome__mirror_url`

* Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used.
* Type: String.
* Default: `'{{ lfops__repo_mirror_url | default("") }}'`

Example:
```yaml
# optional
repo_google_chrome__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_google_chrome__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
