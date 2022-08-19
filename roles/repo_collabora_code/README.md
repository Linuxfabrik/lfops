# Ansible Role linuxfabrik.lfops.repo_collabora_code

This role deploys the official [Collabora CODE Repository](https://docs.fedoraproject.org/en-US/collabora_code/).

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Tags

| Tag                   | What it does                          |
| ---                   | ------------                          |
| `repo_collabora_code` | Deploys the Collabora CODE Repository |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_collabora_code__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles, or else to `''`. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_collabora_code__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
