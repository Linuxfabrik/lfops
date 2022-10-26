# Ansible Role linuxfabrik.lfops.elasticsearch_oss

This role installs and configures a Elasticsearch OSS server.

Note that this role does NOT let you specify a particular Elasticsearch OSS server version. It simply installs the latest available Elasticsearch OSS server version from the repos configured in the system. If you want or need to install a specific Elasticsearch OSS server version, use the [linuxfabrik.lfops.repo_elasticsearch_oss](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch_oss) beforehand.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Enable the official elasticsearch oss repository. This can be done using the [linuxfabrik.lfops.repo_elasticsearch_oss](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch_oss) role.
* If you use the [elasticsearch playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/elasticsearch.yml), this is automatically done for you.


## Tags

| Tag             | What it does                            |
| ---             | ------------                            |
| `elasticsearch_oss`       | Installs and configures Elasticsearch OSS         |
| `elasticsearch_oss:state` | Manages the state of the Elasticsearch OSS service |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `elasticsearch_oss__action_auto_create_index__host_var` | Automatic index creation allows any index to be created automatically. | `true` |
| `elasticsearch_oss__cluster_name__host_var` | A descriptive name for your cluster. | `'my-application'` |
| `elasticsearch_oss__service_enabled` | Enables or disables the elasticsearch oss service, analogous to `systemctl enable/disable --now`. | `true` |

Example:
```yaml
# optional
elasticsearch_oss__action_auto_create_index__host_var: false
elasticsearch_oss__cluster_name__host_var: 'my-cluster'
elasticsearch_oss__service_enabled: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
