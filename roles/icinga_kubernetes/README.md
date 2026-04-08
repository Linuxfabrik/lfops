# Ansible Role linuxfabrik.lfops.icinga_kubernetes

[Icinga for Kubernetes](https://icinga.com/docs/icinga-for-kubernetes/latest/) consists of multiple components. This role only installs [Icinga for Kubernetes](https://icinga.com/docs/icinga-for-kubernetes/latest/). Generally, the [Icinga for Kubernetes Web](https://icinga.com/docs/icinga-for-kubernetes-web/latest/) is also required, use the [linuxfabrik.lfops.icinga_kubernetes_web](https://github.com/Linuxfabrik/lfops/tree/main/roles/icinga_kubernetes_web) role for that.

This role is tested with the following Icinga for Kubernetes versions:

* 0.3.0


## Mandatory Requirements

* A configured Icinga2 Master Setup. This can be done using the [linuxfabrik.lfops.setup_icinga2_master](https://github.com/linuxfabrik/lfops/tree/main/playbooks/setup_icinga2_master.yml) playbook.


## Tags

`icinga_kubernetes`

* Installs and configures Icinga for Kubernetes.
* Triggers: icinga-kubernetes.service restart.


## Mandatory Role Variables

`icinga_kubernetes__database_login`

* The user account for accessing the Icinga for Kubernetes SQL database. Currently, only MySQL is supported.
* Type: Dictionary.
* Default: none

Example:
```yaml
# mandatory
icinga_kubernetes__database_login:
  username: 'icinga_kubernetes'
  password: 'linuxfabrik'
```


## Optional Role Variables

`icinga_kubernetes__clusters__host_var` / `icinga_kubernetes__clusters__group_var`

* A list of kubernetes cluster configs. For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Subkeys:

    * `name`:

        * Mandatory. The name of the cluster.
        * Type: String.

    * `kubeconfig_path`:

        * Mandatory. Path to the cluster's kubeconfig. For permissions, have a look at https://icinga.com/docs/icinga-for-kubernetes/latest/doc/02-Installation/#kubernetes-access-control-requirements.
        * Type: String.

    * `state`:

        * Optional. State of the cluster config. Possible options: `present`, `absent`.
        * Type: String.
        * Default: `'present'`

* Type: List of dictionaries.
* Default:

```yaml
icinga_kubernetes__clusters__role_var:
  - name: 'default'
    kubeconfig_path: '/etc/icinga-kubernetes/kubeconfig'
    state: 'present'
```

`icinga_kubernetes__database_host`

* The host on which the Icinga for Kubernetes SQL database is reachable.
* Type: String.
* Default: `'127.0.0.1'`

`icinga_kubernetes__database_login_host`

* The Host-part of the SQL database user.
* Type: String.
* Default: `'127.0.0.1'`

`icinga_kubernetes__database_name`

* The name of the Icinga for Kubernetes SQL database.
* Type: String.
* Default: `'icinga_kubernetes'`

`icinga_kubernetes__service_enabled`

* Enables or disables the Icinga for Kubernetes service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

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
