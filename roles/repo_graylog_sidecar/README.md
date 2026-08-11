# Ansible Role linuxfabrik.lfops.repo_graylog_sidecar

This role deploys the [Graylog Sidecar Repository](https://go2docs.graylog.org/current/getting_in_log_data/install_sidecar_on_linux.htm). The Graylog Sidecar is served from a dedicated repository, separate from the main Graylog repository deployed by [linuxfabrik.lfops.repo_graylog](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_graylog). Although the Graylog project ships a repository package for this, LFOps prefers to install the repository configuration manually, because it's the only way to handle custom mirror servers.


*Available in the next LFOps release.*


## Tags

`repo_graylog_sidecar`

* Deploys the Graylog Sidecar Repository.
* Triggers: none.


## Mandatory Role Variables

`repo_graylog_sidecar__version`

* The Graylog Sidecar repo version to install, in `'major.minor'` format. The Sidecar repository is versioned independently of the Graylog server. One of `'1.0'` through `'1.5'` as of 2026-06. [See the Graylog Sidecar releases for a current list](https://github.com/Graylog2/collector-sidecar/releases).
* Type: String.

Example:
```yaml
# mandatory
repo_graylog_sidecar__version: '1.5'
```


## Optional Role Variables

`repo_graylog_sidecar__basic_auth_login`

* Use HTTP basic auth to login to the repository. Only takes effect together with a custom mirror URL; the default public repositories do not use basic auth. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles.
* Type: String.
* Default: `'{{ lfops__repo_basic_auth_login | default("") }}'`

`repo_graylog_sidecar__mirror_url`

* Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used.
* Type: String.
* Default: `'{{ lfops__repo_mirror_url | default("") }}'`

Example:
```yaml
# optional
repo_graylog_sidecar__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_graylog_sidecar__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
