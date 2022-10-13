# Ansible Role linuxfabrik.lfops.elasticsearch_oss

This role installs and configures a Elasticsearch OSS server.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Enable the official Elasticsearch OSS repository. This can be done using the [linuxfabrik.lfops.repo_elasticsearch_oss](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch_oss) role.


## Tags

| Tag             | What it does                            |
| ---             | ------------                            |
| `elasticsearch_oss`       | Installs and configures Elasticsearch OSS         |
| `elasticsearch_oss:state` | Manages the state of the Elasticsearch OSS service |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `elasticsearch_oss__cluster_name` | A descriptive name for your cluster. | `'my-application'` |
| `elasicsearch_oss__action_auto_create_index` | Automatic index creation allows any index to be created automatically. | `true` |

Example:
```yaml
# optional
elasticsearch_oss__cluster_name: 'my-cluster'
elasicsearch_oss__action_auto_create_index: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
