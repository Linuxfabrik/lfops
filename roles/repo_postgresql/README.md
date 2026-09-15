# Ansible Role linuxfabrik.lfops.repo_postgresql

This role deploys the official [PostgreSQL Repo](https://www.postgresql.org/download/linux/redhat/).


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* On RHEL 8 and 9, the role disables the distribution's `postgresql` module, so the PostgreSQL packages come from the PGDG repositories.
* The PostgreSQL version repositories (`pgdg14` to `pgdg18`) get `priority=90`, ahead of dnf's default of 99. This deviates from the upstream repository file, which sets no priority: RHEL 10 AppStream ships `postgresql18-*` under the same package names as PGDG but with the distribution's file layout (`/usr/bin`, `postgresql-setup`), so without the priority dnf would install or update to whichever build has the higher version, while the `postgresql_server` role relies on the PGDG layout below `/usr/pgsql-<version>`. The common repository (`pgdg-common`) keeps the default priority, so packages such as `pgbouncer`, `barman` or `python3-psycopg2` still come from whichever repository has the newer build.


## Tags

`repo_postgresql`

* Deploys the PostgreSQL Repository.
* Triggers: none.


## Optional Role Variables

`repo_postgresql__basic_auth_login`

* Use HTTP basic auth to login to the repository. Only takes effect together with a custom mirror URL; the default public repositories do not use basic auth. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles.
* Type: String.
* Default: `'{{ lfops__repo_basic_auth_login | default("") }}'`

`repo_postgresql__mirror_url`

* Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used.
* Type: String.
* Default: `'{{ lfops__repo_mirror_url | default("") }}'`

Example:
```yaml
# optional
repo_postgresql__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_postgresql__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
