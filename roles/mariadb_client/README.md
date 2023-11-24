# Ansible Role linuxfabrik.lfops.mariadb_client

This role simply installs the command line client for MariaDB `mysql`.

Note that this role does NOT let you specify a particular MariaDB client version. It simply installs the latest available MariaDB client version from the repos configured in the system. If you want or need to install a specific MariaDB client version, use the [linuxfabrik.lfops.repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb) beforehand.

Runs on

* RHEL 8 (and compatible)


## Optional Requirements

* Enable the official [MariaDB Package Repository](https://mariadb.com/kb/en/mariadb-package-repository-setup-and-usage/). This can be done using the [linuxfabrik.lfops.repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb) role.


## Tags

| Tag              | What it does                |
| ---              | ------------                |
| `mariadb_client` | Installs the MariaDB client |


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
