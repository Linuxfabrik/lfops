# Ansible Role linuxfabrik.lfops.repo_monitoring_plugins

This role removes the former repository of the Linuxfabrik Monitoring Plugins at repo.linuxfabrik.ch/monitoring-plugins/ from a host. The Monitoring Plugins are served by the Linuxfabrik package repository, which the [linuxfabrik.lfops.repo_linuxfabrik](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_linuxfabrik) role deploys.

The role is deprecated and will be removed in a future LFOps release. The playbooks that deploy the Monitoring Plugins (`monitoring_plugins`, `icinga2_agent`, `setup_basic`, `setup_icinga2_master`) run it before `repo_linuxfabrik`, so hosts are cleaned up on their next run.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* The role removes every `linuxfabrik-monitoring-plugins*` file from `/etc/yum.repos.d` (Red Hat family), `/etc/zypp/repos.d` (SUSE) or `/etc/apt/sources.list.d` (Debian and Ubuntu), which also covers the timestamped backups of the repository file and the files that `tools/install-monitoring-plugins` of the Monitoring Plugins wrote.
* On Debian and Ubuntu, it also removes `/etc/apt/keyrings/linuxfabrik.asc`, which only the former repository file referenced.
* The Linuxfabrik signing key stays in the rpm database, since the Linuxfabrik repository is signed with the same key.
* The run aborts as long as one of the former variables `repo_monitoring_plugins__basic_auth_login`, `repo_monitoring_plugins__mirror_url` or `repo_monitoring_plugins__testing` is set. Use `repo_linuxfabrik__basic_auth_login`, `repo_linuxfabrik__mirror_url` and `repo_linuxfabrik__testing_repo_enabled` instead. A mirror has to serve the Linuxfabrik repository below `<mirror URL>/linuxfabrik/`, see the README of `repo_linuxfabrik`.


## Tags

`repo_monitoring_plugins`, `repo_monitoring_plugins:remove`

* Removes the former Monitoring Plugins repository.
* Triggers: none.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
