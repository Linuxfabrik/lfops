# Ansible Role linuxfabrik.lfops.repo_mydumper

This role deploys a repository for the mydumper package. Note that no official repository exists - Linuxfabrik currently uses its own (non-public) server.

Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Tags

| Tag             | What it does                    |
| ---             | ------------                    |
| `repo_mydumper` | Deploys the mydumper repository |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_baseos__basic_auth_login` | Use HTTP basic auth to login to the repository. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles. | `{{ lfops__repo_basic_auth_login \| default("") }}` |
| `repo_mydumper__baseurl` | Set the URL to a custom mirror server providing the repository. | `https://repo.linuxfabrik.ch/mydumper/el/{{ ansible_facts["distribution_major_version"] }}` |

Example:
```yaml
# optional
repo_mydumper__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_mydumper__baseurl: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
