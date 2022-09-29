# Ansible Role linuxfabrik.lfops.repo_graylog

This role [deploys the Graylog Repository](https://docs.graylog.org/docs/operating-system-packages). Although the Graylog project doesn't recommend to do that, LFOps prefers to install the repository configuration manually, because it's the only way to handle custom mirror servers.

Runs on

* RHEL 8 (and compatible)


## Tags

| Tag           | What it does                     |
| ---           | ------------                     |
| `repo_graylog` | Deploys the Graylog Repository |


## Mandatory Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_graylog__version` | The Graylog repo version to install. One of `'2.0'`, `'2.1'`, `'2.2'`, `'2.3'`, `'2.4'`, `'3.0'`, `'3.1'`, `'3.2'`, `'3.3'`, `'4.0'`, `'4.1'`, `'4.2'` or `'4.3'`. [Have a look at the graylog repository for the list of available releases](https://www.graylog.org/releases). |

Example:
```yaml
# mandatory
repo_graylog__version: '4.3'
```

## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_graylog__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_graylog__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
