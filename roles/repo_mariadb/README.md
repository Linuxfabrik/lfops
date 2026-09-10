# Ansible Role linuxfabrik.lfops.repo_mariadb

This role deploys the [MariaDB Package Repository](https://mariadb.com/docs/server/server-management/install-and-upgrade-mariadb/mariadb-package-repository-setup-and-usage).


*Available since LFOps `2.0.0`.*


## Tags

`repo_mariadb`

* Deploys the MariaDB Package Repository.
* Triggers: none.


## Mandatory Role Variables

`repo_mariadb__version`

* The MariaDB repo version to install. [Have a look at the MariaDB Download Site for the list of available releases](https://mariadb.org/download/?t=mariadb&p=mariadb&os=Linux&cpu=x86_64). Also, have a look at the [MariaDB Server Releases page](https://mariadb.com/docs/release-notes/community-server) to check which version is a "long-term support MariaDB stable" or "short-term support MariaDB development" release.
* On RHEL 10 this has to be 10.11 or newer, since MariaDB publishes no RHEL 10 packages for older releases.
* Type: String.

Example:
```yaml
# mandatory
repo_mariadb__version: '10.6'
```


## Optional Role Variables

`repo_mariadb__basic_auth_login`

* Use HTTP basic auth to login to the repository. Only takes effect together with a custom mirror URL; the default public repositories do not use basic auth. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles.
* Type: String.
* Default: `'{{ lfops__repo_basic_auth_login | default("") }}'`

`repo_mariadb__mirror_url`

* Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used.
* Type: String.
* Default: `'{{ lfops__repo_mirror_url | default("") }}'`

Example:
```yaml
# optional
repo_mariadb__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_mariadb__mirror_url: 'https://mirror.example.com'
```


## Troubleshooting

**The run aborts with `MariaDB X.Y publishes no packages for RHEL 10`**

* MariaDB publishes RHEL 10 packages from 10.11 on. The role stops before writing the repository file, because a repository that answers 404 breaks every dnf transaction on the host, not only the MariaDB install. Set `repo_mariadb__version` to 10.11 or newer.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
