# Ansible Role linuxfabrik.lfops.repo_collabora_code

This role deploys the official [Collabora CODE Repository](https://docs.fedoraproject.org/en-US/collabora_code/).

Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Tags

| Tag                   | What it does                          |
| ---                   | ------------                          |
| `repo_collabora_code` | Deploys the Collabora CODE Repository |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_baseos__basic_auth_login` | Use HTTP basic auth to login to the repository. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles. | `{{ lfops__repo_basic_auth_login \| default("") }}` |
| `repo_collabora_code__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_collabora_code__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_collabora_code__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
