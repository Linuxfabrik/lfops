# Ansible Role linuxfabrik.lfops.repo_elasticsearch_oss

This role deploys the [Elasticsearch OSS Repository](https://www.elastic.co/guide/en/beats/filebeat/current/setup-repositories.html#_yum).
OSS is an alternative package which contains only features that are available under the Apache 2.0 license.

**Warning**: Regarding **Graylog** we caution you not to install or upgrade Elasticsearch to 7.11 and later! It is not supported. If you do so, it will break your instance! Use Elasticsearch 6.x or 7.10.2-1 max.

Runs on

* RHEL 8 (and compatible)


## Tags

| Tag                 		| What it does                         		|
| ---                 		| ------------                         		|
| `repo_elasticsearch_oss` 	| Deploys the Elasticsearch OSS Repository 	|


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `repo_elasticsearch_oss__version__host_var` / <br> `repo_elasticsearch_oss__version__group_var` | The Elasticsearch OSS repo version to install. One of `6.x` or `7.x`. [Have a look at the Elasticsearch OSS repository for the list of available releases](https://www.elastic.co/downloads/past-releases#elasticsearch-oss).  <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). |

Example:
```yaml
# mandatory
repo_elasticsearch_oss__version__host_var: '7.x'
```

## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_elasticsearch_oss__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_elasticsearch_oss__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
