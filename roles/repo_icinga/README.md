# Ansible Role linuxfabrik.lfops.repo_icinga

This role deploys the [Icinga Package Repository](https://packages.icinga.com/).

Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Tags

| Tag           | What it does                          |
| ---           | ------------                          |
| `repo_icinga` | Deploys the Icinga Package Repository |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_icinga__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url | default("") }}'` |
| `repo_icinga__subscription_login` | The [Icinga Repository Subscription](https://icinga.com/subscription/) account. | unset |

Example:
```yaml
# optional
repo_icinga__mirror_url: 'https://mirror.example.com'
repo_icinga__subscription_login:
  username: 'my-username'
  password: 'linuxfabrik'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
