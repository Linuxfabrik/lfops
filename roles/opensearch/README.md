# Ansible Role linuxfabrik.lfops.opensearch

This role installs and configures a OpenSearch server.

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


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `opensearch__version__host_var` / <br> `opensearch__version__group_var` | The version of OpenSearch which should be installed.  <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). |

Example:
```yaml
# mandatory
opensearch__version__host_var: '2.5.0'
```

## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `opensearch__action_auto_create_index__host_var` / <br> `opensearch__action_auto_create_index__group_var` | Automatic index creation allows any index to be created automatically.  <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `true` |
| `opensearch__cluster_name__host_var` / <br> `opensearch__cluster_name__group_var` | A descriptive name for your cluster.  <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `'my-application'` |
| `opensearch__path_data__host_var` / <br> `opensearch__path_data__group_var` | Path to directory where to store the data. Directory will be created. | `'/var/lib/opensearch'` |
| `opensearch__plugins_security_disabled` | Enables or disables the opensearch [security plugin](https://opensearch.org/docs/1.3/security-plugin/index/), which offers `encryption`, `authentication`, `access control` and `audit logging and compliance`. <br/>Note: If you want to use this feature, there is more configuration needed, which is currently not supported by this role. You will need to do the additional configuration of the security plugin manually. | `true` |
| `opensearch__service_enabled` | Enables or disables the opensearch service, analogous to `systemctl enable/disable --now`. | `true` |

Example:
```yaml
# optional
opensearch__action_auto_create_index__host_var: false
opensearch__cluster_name__host_var: 'my-cluster'
opensearch__path_data__host_var: '/var/lib/opensearch'

opensearch__plugins_security_disabled: false
opensearch__service_enabled: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
