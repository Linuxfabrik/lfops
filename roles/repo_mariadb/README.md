# Ansible Role linuxfabrik.lfops.repo_mariadb

This role deploys the [MariaDB Package Repository](https://mariadb.com/kb/en/mariadb-package-repository-setup-and-usage/).

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Tags

| Tag            | What it does                           |
| ---            | ------------                           |
| `repo_mariadb` | Deploys the MariaDB Package Repository |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `repo_mariadb__version` | The MariaDB repo version to install. [Have a look at the MariaDB Download Site for the list of available releases](https://mariadb.org/download/?t=mariadb&p=mariadb&os=Linux&cpu=x86_64). Also, have a look at the [MariaDB Server Releases page](https://mariadb.com/kb/en/mariadb-server-release-dates/) to check which version is a "long-term support MariaDB stable" or "short-term support MariaDB development" release. |

Example:
```yaml
# mandatory
repo_mariadb__version: '10.6'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_mariadb__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles, or else to `''`. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_mariadb__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
