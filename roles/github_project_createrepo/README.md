# Ansible Role linuxfabrik.lfops.github_project_createrepo

This role installs and configures [github_project_createrepo](https://github.com/Linuxfabrik/github-project-createrepo).


## Mandatory Requirements

* Install Python 3. This can be done using the [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python) role.
* Install `createrepo`. This can be done using the [linuxfabrik.lfops.apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps) role.
* Install `git`. This can be done using the [linuxfabrik.lfops.apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps) role.

If you use the [`github_project_createrepo` Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/github_project_createrepo.yml), this is automatically done for you.


## Tags

`github_project_createrepo`

* Installs and configures github_project_createrepo.
* Triggers: none.

`github_project_createrepo:configure`

* Deploys `/etc/github_project_createrepo.yml`.
* Triggers: none.


## Mandatory Role Variables

`github_project_createrepo__github_repos`

* A list of dictionaries containing GitHub Repository from which the RPM-assets will be downloaded. Subkeys: Have a look at the project's [README](https://github.com/Linuxfabrik/github-project-createrepo/blob/main/README.md#configuration).
* Type: List of dictionaries.
* Default: none

Example:
```yaml
# mandatory
github_project_createrepo__github_repos:
  - github_user: 'mydumper'
    github_repo: 'mydumper'
    relative_target_path: 'mydumper/el/8'
    rpm_regex: 'mydumper-{latest_version}-\d\+.el8.x86_64.rpm'
  - github_user: 'exoscale'
    github_repo: 'cli'
    relative_target_path: 'exoscale/cli'
    # cannot use latest_version, as exoscale prefixes that with a "v", but there is no "v" in the rpm filename
    rpm_regex: 'exoscale-cli_\d+\.\d+\.\d+_linux_amd64\.rpm'
```


## Optional Role Variables

`github_project_createrepo__base_path`

* Directory under which all the repos will be placed. This directory should be served by a webserver.
* Type: String.
* Default: `'/var/www/html/github-repos'`

`github_project_createrepo__timer_enabled`

* Enables or disables the github-project-createrepo timer, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`github_project_createrepo__webserver_user`

* The user under which the webserver runs. Will be used to set the correct FACL entries so that both users can access the files.
* Type: String.
* Default: `'apache'`

Example:
```yaml
# optional
github_project_createrepo__base_path: '/var/www/html/github-repos'
github_project_createrepo__timer_enabled: true
github_project_createrepo__webserver_user: 'nginx'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
