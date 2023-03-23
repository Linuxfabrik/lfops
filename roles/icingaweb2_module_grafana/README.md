# Ansible Role linuxfabrik.lfops.icingaweb2_module_grafana

This role installs and configures the [IcingaWeb2 Grafana Module](https://github.com/Mikesch-mp/icingaweb2-module-grafana).
Additionally, it deploys the the graph configuration for the [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins). This can be disabled using `icingaweb2_module_grafana__skip_monitoring_plugins_graphs_config`.

Tested on

* RHEL 8 (and compatible)


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.
* A configured Grafana. This can be done using the [linuxfabrik.lfops.grafana](https://github.com/linuxfabrik/lfops/tree/main/roles/grafana) role.

If you use the [Setup Icinga2 Master Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_icinga2_master.yml), this is automatically done for you.


## Tags

| Tag                                                       | What it does                                                                                                                         |
| ---                                                       | ------------                                                                                                                         |
| `icingaweb2_module_grafana`                               | Installs and configures the IcingaWeb2 Grafana Module                                                                                |
| `icingaweb2_module_grafana:monitoring_plugins_graphs`     | Deploys the configuration for the graphs for the [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins) |


## Mandatory Role Variables

| Variable                             | Description                                                                                                        |
| --------                             | -----------                                                                                                        |
| `icingaweb2_module_grafana__version` | The module version to install. Possible options: https://github.com/Mikesch-mp/icingaweb2-module-grafana/releases. |

Example:
```yaml
# mandatory
icingaweb2_module_grafana__version: 'v1.4.2'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icingaweb2_module_grafana__monitoring_plugins_version` | The version of the monitoring plugins that will be used for generating the grafana graph configuration. Possible options: * `latest`: The **latest stable** release. See the [Releases](https://github.com/Linuxfabrik/monitoring-plugins/releases).<br> * `main`: The development version. Use with care.<br> * A specific release, for example `2022030201`. See the [Releases](https://github.com/Linuxfabrik/monitoring-plugins/releases). | `'{{ lfops__monitoring_plugins_version \| default("latest") }}'` |
| `icingaweb2_module_grafana__skip_monitoring_plugins_graphs_config` | Skip the deployment of the graph configuration for [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins). | `false` |
| `icingaweb2_module_grafana__theme` | The theme for the Grafana graphs. Possible options:<br> * `dark`<br> * `light` | `'light'` |
| `icingaweb2_module_grafana__url` | The Grafana URL. This should be reachable from both the IcingaWeb2 server and the client device. | `{{ grafana__root_url }}` |

Example:
```yaml
# optional
icingaweb2_module_grafana__monitoring_plugins_version: 'latest'
icingaweb2_module_grafana__skip_monitoring_plugins_graphs_config: true
icingaweb2_module_grafana__theme: 'light'
icingaweb2_module_grafana__url: 'https://monitoring.example.com/grafana'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
