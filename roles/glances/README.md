# Ansible Role linuxfabrik.lfops.glances

This role installs [glances](https://nicolargo.github.io/glances/) and drops a snippet into `/etc/profile.d/glances.sh` that aliases `top` and `glances` to `glances -t 1`.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

On RHEL 8 / 9 (and clones) and on Debian / Ubuntu, glances is installed from the distribution package. On RHEL 10 and clones (Rocky / Alma 10), `glances` is not packaged in EPEL 10, so it is installed into a dedicated Python venv at `/opt/python-venv/glances` (the `glances` binary is exposed in `/usr/local/bin`).


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* On RHEL-compatible systems, the EPEL repository must be enabled (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)). On RHEL 8 / 9 it provides the `glances` package; on RHEL 10 it provides `python3-virtualenv` for the Python venv.
* On Rocky Linux 9 and 10, the CRB repository must be enabled (role: [linuxfabrik.lfops.repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos)). On Rocky 9 the `glances` package moved from EPEL into the base repository; on Rocky 10 it provides dependencies for `python3-virtualenv`.
* On RHEL 10 and clones, the Python venv that holds glances is created by [linuxfabrik.lfops.python_venv](https://github.com/Linuxfabrik/lfops/tree/main/roles/python_venv). Skip it with `glances__skip_python_venv`.


## Tags

`glances`

* Installs glances and configures the `top` / `glances` aliases.
* Triggers: none.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
