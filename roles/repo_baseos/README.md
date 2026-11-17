# Ansible Role linuxfabrik.lfops.repo_baseos

This role deploys the BaseOS repositories, which can be used to set a custom mirror server.


*Available since LFOps `2.0.0`.*


## Tags

`repo_baseos`

* Deploys the BaseOS repositories.
* Triggers: none.


## Optional Role Variables

`repo_baseos__basic_auth_login`

* Use HTTP basic auth to login to the repository. Only takes effect together with a custom mirror URL; the default public repositories do not use basic auth. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles.
* Type: Dictionary.
* Default: `'{{ lfops__repo_basic_auth_login | d("") }}'`
* Subkeys:

    * `password`:

        * Mandatory. Password.
        * Type: String.

    * `username`:

        * Mandatory. Username.
        * Type: String.

`repo_baseos__crb_repo_enabled__host_var` / `repo_baseos__crb_repo_enabled__group_var`

* Whether the CRB repository should be enabled or not.
* Type: Bool.
* Default: `false`

`repo_baseos__mirror_url`

* Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used.
* Type: String.
* Default: `'{{ lfops__repo_mirror_url | d("") }}'`

`repo_baseos__security_repo_enabled__host_var` / `repo_baseos__security_repo_enabled__group_var`

* Whether the Rocky Linux `security` repository should be enabled. This repository delivers critical CVE fixes. Set to `false` to opt out on a specific host or group.
* Type: Bool.
* Default: `true`
* Deviates from the upstream default `false`: critical CVE fixes should reach a host without the operator having to opt in first.

`repo_baseos__security_repo_use_upstream`

* Whether the Rocky Linux `security` repository always points at upstream, even when `repo_baseos__mirror_url` is set. Upstream is `dl.rockylinux.org` itself, not the mirrorlist: the mirrors sync with a delay and every host is handed its own, so a hot-fix would reach part of the hosts hours later than the rest. This keeps critical CVE fixes coming straight from upstream instead of a potentially lagging mirror. Hosts need outbound HTTPS access to `dl.rockylinux.org`. Set to `false` to make the `security` repository follow `repo_baseos__mirror_url` like the other repositories; without a `repo_baseos__mirror_url`, it stays on `dl.rockylinux.org`.
* Type: Bool.
* Default: `true`

Example:
```yaml
# optional
repo_baseos__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_baseos__crb_repo_enabled__host_var: true
repo_baseos__mirror_url: 'https://mirror.example.com'
repo_baseos__security_repo_enabled__host_var: false
repo_baseos__security_repo_use_upstream: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
