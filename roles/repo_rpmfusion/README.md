# Ansible Role linuxfabrik.lfops.repo_rpmfusion

This role deploys the [RPM Fusion](https://rpmfusion.org/RPM%20Fusion) free and nonfree Repositories.


## Mandatory Requirements

* Enable the EPEL Repository. This can be done using the [linuxfabrik.lfops.epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/epel) role.

If you use the ["Repo RPM Fusion" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/repo_rpmfusion.yml), this is automatically done for you.


## Tags

| Tag                  | What it does                         | Reload / Restart |
| ---                  | ------------                         | ---------------- |
| `repo_rpmfusion`     | Deploys the RPM Fusion Repository    | - |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_rpmfusion__basic_auth_login` | Use HTTP basic auth to login to the repository. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles. | `{{ lfops__repo_basic_auth_login \| default("") }}` |
| `repo_rpmfusion__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_rpmfusion__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_rpmfusion__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
