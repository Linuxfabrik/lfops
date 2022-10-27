# Ansible Role linuxfabrik.lfops.opensearch

This role installs and configures a OpenSearch server.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Enable the official OpenSearch repository. This can be done using the [linuxfabrik.lfops.repo_opensearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_opensearch) role.

If you use the [opensearch playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/opensearch.yml), this is automatically done for you.

## Tags

| Tag             | What it does                            |
| ---             | ------------                            |
| `opensearch`       | Installs and configures OpenSearch   |
| `opensearch:state` | Manages the state of the OpenSearch service |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `opensearch__version__host_var` / <br> `opensearch__version__group_var` | The version of OpenSearch which should be installed.  <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). |

Example:
```yaml
# mandatory
opensearch__version__host_var: '1.3.4'
```

## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `opensearch__action_auto_create_index__host_var` / <br> `opensearch__action_auto_create_index__group_var` | Automatic index creation allows any index to be created automatically.  <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `true` |
| `opensearch__cluster_name__host_var` / <br> `opensearch__cluster_name__group_var` | A descriptive name for your cluster.  <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `'my-application'` |
| `opensearch__service_enabled` | Enables or disables the opensearch service, analogous to `systemctl enable/disable --now`. | `true` |

Example:
```yaml
# optional
opensearch__action_auto_create_index_host_var: false
opensearch__cluster_name__host_var: 'my-cluster'
opensearch__service_enabled: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
