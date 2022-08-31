# Ansible Role linuxfabrik.lfops.repo_elasticsearch

This role [deploys the Elasticsearch Repository](https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html#rpm-repo) (both free and subscription features).

Tested on

* RHEL 8 (and compatible)


## Tags

| Tag           | What it does                     |
| ---           | ------------                     |
| `repo_elasticsearch` | Deploys the Elasticsearch Repository |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_elasticsearch__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles, or else to `''`. | `'{{ lfops__repo_mirror_url | default("") }}'` |
| `repo_elasticsearch__version` | The Elasticsearch repo version to install. One of `5.x`, `6.x`, `7.x` or `8.x`. [Have a look at the Elasticsearch repository for the list of available releases](https://www.elastic.co/downloads/past-releases#elasticsearch). | `'8.x'`

Example:
```yaml
# optional
repo_elasticsearch__mirror_url: 'https://mirror.example.com'
repo_elasticsearch__version: '8.x'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
