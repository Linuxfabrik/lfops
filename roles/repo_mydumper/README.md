# Ansible Role linuxfabrik.lfops.repo_mydumper

This role deploys a repository for the mydumper package.
Note that Linuxfabrik currently uses its [own repository server](https://repo.linuxfabrik.ch/) for RedHat-based Distros.


## Tags

| Tag             | What it does                    |
| ---             | ------------                    |
| `repo_mydumper` | Deploys the mydumper repository |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_mydumper__basic_auth_login` | Use HTTP basic auth to login to the repository. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles. | `{{ lfops__repo_basic_auth_login \| default("") }}` |
| `repo_mydumper__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_mydumper__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_mydumper__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
