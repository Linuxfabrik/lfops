# Ansible Role linuxfabrik.lfops.opensearch

This role installs and configures a OpenSearch server.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Enable the official OpenSearch repository. This can be done using the [linuxfabrik.lfops.repo_opensearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_opensearch) role.


## Tags

| Tag             | What it does                            |
| ---             | ------------                            |
| `opensearch`       | Installs and configures OpenSearch   |
| `opensearch:state` | Manages the state of the OpenSearch service |


## Mandatory Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `opensearch__version` | The version of OpenSearch which should be installed. | unset |

## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `opensearch__cluster_name` | A descriptive name for your cluster. | `'my-application'` |
| `opensearch__action_auto_create_index` | Automatic index creation allows any index to be created automatically. | `true` |

Example:
```yaml
# mandatory
opensearch__version: '1.3.4'
# optional
opensearch__cluster_name: 'my-cluster'
opensearch_oss__action_auto_create_index: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
