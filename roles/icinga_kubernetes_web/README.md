# Ansible Role linuxfabrik.lfops.icinga_kubernetes_web

[Icinga for Kubernetes](https://icinga.com/docs/icinga-for-kubernetes/latest/) consists of multiple components. This role only installs [Icinga for Kubernetes Web](https://icinga.com/docs/icinga-for-kubernetes-web/latest/). Generally, the [Icinga for Kubernetes](https://icinga.com/docs/icinga-for-kubernetes/latest/) is also required, use the [linuxfabrik.lfops.icinga_kubernetes](https://github.com/Linuxfabrik/lfops/tree/main/roles/icinga_kubernetes) role for that. Run the linuxfabrik.lfops.icinga_kubernetes role first to initialise the database.

This role is tested with the following Icinga for Kubernetes Web versions:

* 0.2.0


*Available since LFOps `3.0.0`.*


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* A configured IcingaWeb2 must be available (role: [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2)).


## Tags

`icinga_kubernetes_web`

* Installs and configures the Icinga for Kubernetes Web Module.
* Triggers: none.


## Mandatory Role Variables

`icinga_kubernetes_web__version`

* The module version to install. Possible options: https://github.com/Icinga/icinga-kubernetes-web/releases.
* Type: String.
* Default: none

Example:
```yaml
# mandatory
icinga_kubernetes_web__version: 'v0.2.0'
```


## Optional Role Variables

`icinga_kubernetes_web__database_host`

* The host on which the Icinga for Kubernetes SQL database is reachable. Set this when the module runs on a different host than the database.
* Type: String.
* Default: `'{{ icinga_kubernetes__database_host }}'` (the value used by the [icinga_kubernetes](https://github.com/Linuxfabrik/lfops/tree/main/roles/icinga_kubernetes) role)

`icinga_kubernetes_web__database_login`

* The user account the module uses to access the Icinga for Kubernetes SQL database. Expects the subkeys `username` and `password`.
* Type: Dictionary.
* Default: `'{{ icinga_kubernetes__database_login }}'` (the value used by the [icinga_kubernetes](https://github.com/Linuxfabrik/lfops/tree/main/roles/icinga_kubernetes) role)

`icinga_kubernetes_web__database_name`

* The name of the Icinga for Kubernetes SQL database.
* Type: String.
* Default: `'{{ icinga_kubernetes__database_name }}'` (the value used by the [icinga_kubernetes](https://github.com/Linuxfabrik/lfops/tree/main/roles/icinga_kubernetes) role)

`icinga_kubernetes_web__url`

* The URL from where to download the IcingaWeb2 Business Process Module.
* Type: String.
* Default: `'https://github.com/Icinga/icinga-kubernetes-web/archive/{{ icinga_kubernetes_web__version }}.tar.gz'`

Example:
```yaml
# optional
icinga_kubernetes_web__database_host: '192.0.2.10'
icinga_kubernetes_web__database_login:
  username: 'icinga_kubernetes'
  password: 'linuxfabrik'
icinga_kubernetes_web__database_name: 'icinga_kubernetes'
icinga_kubernetes_web__url: 'https://github.com/Linuxfabrik/icingaweb2-module-kubernetes-web/archive/{{ icinga_kubernetes_web__version }}.tar.gz'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
