# Ansible Role linuxfabrik.lfops.github_project_createrepo

This role installs and configures [github_project_createrepo](https://github.com/Linuxfabrik/github-project-createrepo).


*Available since LFOps `3.0.0`.*


## How the Role Behaves

* The service runs as the unprivileged `github-project-createrepo` user and may only write to the repositories it maintains: every `relative_target_path` belongs to that user, while `github_project_createrepo__base_path` and the directories leading to the repositories belong to `root`. Nothing else served from `github_project_createrepo__base_path`, such as a repository signing key, can be changed by the service.
* The web server needs no special access, it reads the repositories through the permissions for all users.
* ACL entries that this role granted up to LFOps `v9.0.0` on `github_project_createrepo__base_path` for the service and the web server are removed. If no other ACL entries exist below it, the ACLs are removed entirely.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* Python 3 must be installed (role: [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python)).
* `createrepo` must be installed (role: [linuxfabrik.lfops.apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps)).
* `git` must be installed (role: [linuxfabrik.lfops.apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps)).


## Tags

`github_project_createrepo`

* Installs and configures github_project_createrepo.
* Triggers: none.

`github_project_createrepo:configure`

* Deploys `/etc/github-project-createrepo.yml`.
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

Example:
```yaml
# optional
github_project_createrepo__base_path: '/var/www/html/github-repos'
github_project_createrepo__timer_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
