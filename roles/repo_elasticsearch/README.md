# Ansible Role linuxfabrik.lfops.repo_elasticsearch

This role [deploys the Elasticsearch Repository](https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html#rpm-repo) (both free and subscription features).

**Warning**: Regarding **Graylog** we caution you not to install or upgrade Elasticsearch to 7.11 and later! It is not supported. If you do so, it will break your instance! Use Elasticsearch 6.x or 7.10.2-1 max.

Tested on

* RHEL 8 (and compatible)


## Tags

| Tag                  | What it does                         |
| ---                  | ------------                         |
| `repo_elasticsearch` | Deploys the Elasticsearch Repository |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `repo_elasticsearch__version` | The Elasticsearch repo version to install. One of `5.x`, `6.x`, `7.x` or `8.x`. [Have a look at the Elasticsearch repository for the list of available releases](https://www.elastic.co/downloads/past-releases#elasticsearch). |

Example:
```yaml
# mandatory
repo_elasticsearch__version: '8.x'
```

## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_elasticsearch__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles, or else to `''`. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_elasticsearch__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
