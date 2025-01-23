# Ansible Role linuxfabrik.lfops.repo_icinga

This role deploys the [Icinga Package Repository](https://packages.icinga.com/).


## Mandatory Requirements

* For RHEL (and compatible) hosts an [Icinga Repo Subscription](https://www.linuxfabrik.ch/en/products/icinga-subscriptions) is required.


## Tags

| Tag           | What it does                          |
| ---           | ------------                          |
| `repo_icinga` | Deploys the Icinga Package Repository |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_icinga__basic_auth_login` | Use HTTP basic auth to login to the repository. Use this if you have an [Icinga Subscription](https://icinga.com/subscription/). Defaults to `lfops__repo_basic_auth_login`, making it easy to set this for all `repo_*` roles. | `{{ lfops__repo_basic_auth_login \| default("") }}` |
| `repo_icinga__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url \| default("") }}'` |
| `repo_icinga__use_subscription_url` | Boolean. Only relevant for OpenSUSE & SLES. Set this to `true` if you are using an [Icinga Subscription](https://icinga.com/subscription/). Changes the repository URLs to point to `/subscription/sles`. Also works in conjunction with `repo_icinga__mirror_url`. | `false` |

Example:
```yaml
# optional
repo_icinga__basic_auth_login:
  username: 'my-username'
  password: 'linuxfabrik'
repo_icinga__mirror_url: 'https://mirror.example.com'
repo_icinga__use_subscription_url: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
