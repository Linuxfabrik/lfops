# Ansible Role linuxfabrik.lfops.repo_proxysql

This role deploys the [ProxySQL Package Repository](https://proxysql.com/documentation/installing-proxysql/).


*Available since LFOps `3.0.0`.*


## Tags

`repo_proxysql`

* Deploys the ProxySQL Package Repository.
* Triggers: none.


## Mandatory Role Variables

`repo_proxysql__version__host_var` / `repo_proxysql__version__group_var`

* The version of the ProxySQL repository which should be installed. For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* ProxySQL does not build every version for every OS. On the Red Hat family:

    * RHEL 8: `2.2` to `2.7`, and `3.0`. ProxySQL 3.0 on RHEL 8 comes from the AlmaLinux 8 builds, which may lag behind the RHEL 9 and 10 builds, and needs `openssl3-libs` from EPEL (the `proxysql` playbook deploys it).
    * RHEL 9: `2.4` to `2.7`, and `3.0`.
    * RHEL 10: `3.0` only.

* Type: String.

Example:
```yaml
# mandatory
repo_proxysql__version__host_var: '3.0'  # or '2.7', '2.6', '2.5', '2.4', '2.3', '2.2'
```


## Optional Role Variables

`repo_proxysql__basic_auth_login`

* Use HTTP basic auth to login to the repository. Only takes effect together with a custom mirror URL; the default public repositories do not use basic auth. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles.
* Type: Dictionary.
* Default: `'{{ lfops__repo_basic_auth_login | default("") }}'`

`repo_proxysql__mirror_url`

* Set the URL to a custom mirror server providing the repository below the same path as repo.proxysql.com, for example `<mirror>/ProxySQL/proxysql-3.0.x/centos/9/`. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used.
* Type: String.
* Default: `'{{ lfops__repo_mirror_url | default("") }}'`

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
