# Ansible Role linuxfabrik.lfops.glances

This role installs [glances](https://nicolargo.github.io/glances/) and drops a snippet into `/etc/profile.d/glances.sh` that aliases `top` and `glances` to `glances -t 1`. On RHEL 7 the aliases additionally pass `--disable-docker` to avoid the slow Docker probe.


*Available since LFOps `2.0.0`.*


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* On RHEL-compatible systems, the EPEL repository must be enabled (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)). It provides the `glances` package.
* On Rocky Linux 9, the CRB repository must be enabled (role: [linuxfabrik.lfops.repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos)). The `glances` package moved from EPEL into the base repository on Rocky 9.


## Requirements

Manual steps:

* On RHEL 10 and clones (Rocky / Alma 10), `glances` is not packaged in EPEL 10, so this role fails with `No package glances available.`. Install glances manually there (for example via `pip install glances` in a venv, or from a third-party repo) and skip this role.


## Tags

`glances`

* Installs glances and configures the `top` / `glances` aliases.
* Triggers: none.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
