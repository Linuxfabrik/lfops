# Ansible Role linuxfabrik.lfops.opensearch

This role installs and configures a OpenSearch server. Optionally, it allows the creation of a cluster setup.

Currently supported versions:
* 1.x
* 2.x

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Enable the official OpenSearch repository. This can be done using the [linuxfabrik.lfops.repo_opensearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_opensearch) role.

If you use the [opensearch playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/opensearch.yml), this is automatically done for you.

## Tags

| Tag             | What it does                            |
| ---             | ------------                            |
| `opensearch`       | <ul><li>Install opensearch-`{{ opensearch__version__combined_var }}`</li><li>Deploy `/etc/opensearch/opensearch.yml`</li><li>
Deploy `/etc/sysconfig/opensearch`</li><li>`systemctl {{ opensearch__service_enabled | bool | ternary("enable", "disable") }} --now opensearch.service`</li></ul> |
| `opensearch:state` | <ul><li>`systemctl {{ opensearch__service_enabled | bool | ternary("enable", "disable") }} --now opensearch.service`</li></ul> |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `opensearch__action_auto_create_index__host_var` / <br> `opensearch__action_auto_create_index__group_var` | Automatic index creation allows any index to be created automatically.  <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `true` |
| `opensearch__cluster_name__host_var` / <br> `opensearch__cluster_name__group_var` | A descriptive name for your cluster.  <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `'my-application'` |
| `opensearch__network_host` | Set the bind address to a specific IP. | `'127.0.0.1'` |
| `opensearch__node_name` | A descriptive name for the node | `'{{ ansible_facts["nodename"] }}'` |
| `opensearch__path_data__host_var` / <br> `opensearch__path_data__group_var` | Path to directory where to store the data. Directory will be created. | `'/var/lib/opensearch'` |
| `opensearch__plugins_security_disabled` | Enables or disables the opensearch [security plugin](https://opensearch.org/docs/1.3/security-plugin/index/), which offers `encryption`, `authentication`, `access control` and `audit logging and compliance`. <br/>Note: If you want to use this feature, there is more configuration needed, which is currently not supported by this role. You will need to do the additional configuration of the security plugin manually. | `true` |
| `opensearch__service_enabled` | Enables or disables the opensearch service, analogous to `systemctl enable/disable --now`. | `true` |
| `opensearch__version__host_var` / <br> `opensearch__version__group_var` | The version of OpenSearch which should be installed. If unset, latest will be installed.  <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | unset |

Example:
```yaml
# optional
opensearch__action_auto_create_index__host_var: false
opensearch__cluster_name__host_var: 'my-cluster'
opensearch__network_host: '127.0.0.1'
opensearch__node_name: 'my-node1'
opensearch__path_data__host_var: '/var/lib/opensearch'
opensearch__version__host_var: '2.5.0'

opensearch__plugins_security_disabled: false
opensearch__service_enabled: false
```


### Cluster Configuration

Use the following variables if you want to setup a OpenSearch cluster. Make sure that the cluster members can reach each other by setting `opensearch__network_host` accordingly.

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `opensearch__cluster_initial_cluster_manager_nodes` | A list of initial master-eligible nodes. You need to set this once when bootstrapping the cluster (aka the first start of the cluster). Make sure to remove this option after the first start, the nodes should not restart with this option active. Most of the time contains the same value as `opensearch__discovery_seed_hosts`. | unset |
| `opensearch__discovery_seed_hosts` | A list of IPs or hostnames that point to other master-eligible nodes of the cluster. The port defaults to 9300 but can be overwritten using `:9301`, for example. | unset |

Example:
```yaml
# cluster configuration
opensearch__cluster_initial_cluster_manager_nodes:
  - 'node1.example.com'
  - 'node2.example.com'
  - 'node3.example.com'
opensearch__discovery_seed_hosts:
  - 'node1.example.com'
  - 'node2.example.com'
  - 'node3.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
