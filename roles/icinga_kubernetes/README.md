# Ansible Role linuxfabrik.lfops.icinga_kubernetes

[Icinga for Kubernetes](https://icinga.com/docs/icinga-for-kubernetes/latest/) consists of multiple components. This role only installs [Icinga for Kubernetes](https://icinga.com/docs/icinga-for-kubernetes/latest/). Generally, the [Icinga for Kubernetes Web](https://icinga.com/docs/icinga-for-kubernetes-web/latest/) is also required, use the [linuxfabrik.lfops.icinga_kubernetes_web](https://github.com/Linuxfabrik/lfops/tree/main/roles/icinga_kubernetes_web) role for that.

This role is tested with the following Icinga for Kubernetes versions:

* 0.3.0


## Mandatory Requirements

* A configured Icinga2 Master Setup. This can be done using the [linuxfabrik.lfops.setup_icinga2_master](https://github.com/linuxfabrik/lfops/tree/main/playbooks/setup_icinga2_master.yml) playbook.


## Tags

| Tag        | What it does                                 |
| ---        | ------------                                 |
| `icinga_kubernetes` | Installs and configures Icinga for Kubernetes. |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `icinga_kubernetes__database_login` | The user account for accessing the Icinga for Kubernetes SQL database. Currently, only MySQL is supported. |

Example:
```yaml
# mandatory
icinga_kubernetes__database_login:
  username: 'icinga_kubernetes'
  password: 'linuxfabrik'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icinga_kubernetes__clusters__host_var` /<br> `icinga_kubernetes__clusters__group_var` | A list of kubernetes cluster configs. Subkeys: <ul><li>`name`: Mandatory, string. The name of the cluster.</li> <li>`kubeconfig_path`: Mandatory, string. Path to the cluster's kubeconfig. For permissions, have a look at https://icinga.com/docs/icinga-for-kubernetes/latest/doc/02-Installation/#kubernetes-access-control-requirements.</li> <li>`state`: Optional, string. State of the cluster config. Defaults to `present`. Possible options: `present`, `absent`.</li></ul> | [Have a look](https://github.com/Linuxfabrik/lfops/blob/main/roles/icinga_kubernetes/defaults/main.yml) |
| `icinga_kubernetes__database_host` | The host on which the Icinga for Kubernetes SQL database is reachable. | `127.0.0.1` |
| `icinga_kubernetes__database_login_host` | The Host-part of the SQL database user. | `127.0.0.1` |
| `icinga_kubernetes__database_name` | The name of the Icinga for Kubernetes SQL database. | `'icinga_kubernetes'` |
| `icinga_kubernetes__service_enabled` | Enables or disables the Icinga for Kubernetes service, analogous to `systemctl enable/disable --now`. | `true` |

Example:
```yaml
# optional
icinga_kubernetes__clusters__host_var:
  - name: 'default'
    state: 'absent'
  - name: 'other_cluster'
    kubeconfig_path: '/etc/icinga-kubernetes/kubeconfig-other_cluster'
    state: 'present'
icinga_kubernetes__database_host: '127.0.0.1'
icinga_kubernetes__database_login_host: 'localhost'
icinga_kubernetes__database_name: 'icinga_kubernetes'
icinga_kubernetes__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
