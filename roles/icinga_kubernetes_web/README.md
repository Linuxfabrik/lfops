# Ansible Role linuxfabrik.lfops.icinga_kubernetes_web

[Icinga for Kubernetes](https://icinga.com/docs/icinga-for-kubernetes/latest/) consists of multiple components. This role only installs [Icinga for Kubernetes Web](https://icinga.com/docs/icinga-for-kubernetes-web/latest/). Generally, the [Icinga for Kubernetes](https://icinga.com/docs/icinga-for-kubernetes/latest/) is also required, use the [linuxfabrik.lfops.icinga_kubernetes](https://github.com/Linuxfabrik/lfops/tree/main/roles/icinga_kubernetes) role for that. Run the linuxfabrik.lfops.icinga_kubernetes role first to initialise the database.

This role is tested with the following Icinga for Kubernetes Web versions:

* 0.2.0


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.


## Tags

| Tag                     | What it does                                                 |
| ---                     | ------------                                                 |
| `icinga_kubernetes_web` | Installs and configures the Icinga for Kubernetes Web Module |


## Mandatory Role Variables

| Variable                         | Description                                                                                               |
| --------                         | -----------                                                                                               |
| `icinga_kubernetes_web__version` | The module version to install. Possible options: https://github.com/Icinga/icinga-kubernetes-web/releases |

Example:
```yaml
# mandatory
icinga_kubernetes_web__version: 'v0.2.0'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icinga_kubernetes_web__url` | The URL from where to download the IcingaWeb2 Business Process Module. | `https://github.com/Icinga/icinga-kubernetes-web/archive/{{ icinga_kubernetes_web__version }}.tar.gz` |

Example:
```yaml
# optional
icinga_kubernetes_web__url: 'https://github.com/Linuxfabrik/icingaweb2-module-businessprocess/archive/{{ icinga_kubernetes_web__version }}.tar.gz'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
