# Ansible Role linuxfabrik.lfops.repo_collabora

This role deploys the official Collabora Enterprise Repository.

Supported Versions:

* 23.05
* 24.04


## Tags

| Tag                   | What it does                          |
| ---                   | ------------                          |
| `repo_collabora` | Deploys the Collabora Enterprise Repository |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `repo_collabora__customer_token` | The Customer Token to the Collabora Enterprise subscription. |
| `repo_collabora__version` | The version of Collabora Enterprise to be installed. |

Example:
```yaml
# mandatory
repo_collabora__customer_token: 'Example-Company-eragf35eb18692b7c0ufd3f03199a39i2233h5k8'
repo_collabora__version: '24.04'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_collabora__basic_auth_login` | Use HTTP basic auth to login to the repository. Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles. | `{{ lfops__repo_basic_auth_login \| default("") }}` |
| `repo_collabora__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url \| default("") }}'` |


Example:
```yaml
# optional
repo_collabora__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_collabora__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
