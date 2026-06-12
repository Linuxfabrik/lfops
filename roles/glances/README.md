# Ansible Role linuxfabrik.lfops.glances

This role installs [glances](https://nicolargo.github.io/glances/) and drops a snippet into `/etc/profile.d/glances.sh` that aliases `top` and `glances` to `glances -t 1`.


## Mandatory Requirements

* On RHEL-compatible systems, the EPEL repository (provides the `glances` package). The companion playbook (`playbooks/glances.yml`) takes care of this automatically by also running [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) on RHEL 7/8/9 hosts.
* On Rocky Linux 9, the CRB repository (moved from EPEL into the base repo on Rocky 9). The playbook also runs [linuxfabrik.lfops.repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos) for that distribution / version unless skipped (see below).


## Platform Support

`glances` is not packaged in EPEL 10. On RHEL 10 and clones (Rocky / Alma 10) the role installs glances into a dedicated Python venv at `/opt/python-venv/glances` via pip; on all other supported platforms glances is installed from the distribution package.


## Tags

`glances`

* Installs glances and configures the `top` / `glances` aliases.
* Triggers: none.


## Optional Playbook Variables

`glances__skip_repo_baseos`

* Skip the implicit `linuxfabrik.lfops.repo_baseos` invocation on Rocky Linux 9. Set this if you manage the CRB repository yourself or if the host has no Internet access to the Rocky mirrors.
* Type: Bool.
* Default: `false`

Example:
```yaml
# optional
glances__skip_repo_baseos: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
