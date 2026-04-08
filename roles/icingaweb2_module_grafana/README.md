# Ansible Role linuxfabrik.lfops.icingaweb2_module_grafana

This role installs and configures the [IcingaWeb2 Grafana Module](https://github.com/NETWAYS/icingaweb2-module-grafana).
Additionally, it deploys the the graph configuration for the [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins). This can be disabled using `icingaweb2_module_grafana__skip_monitoring_plugins_graphs_config`.

This role is tested with the following IcingaWeb2 Grafana Module versions:

* 3.1.3


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.
* A configured Grafana. This can be done using the [linuxfabrik.lfops.grafana](https://github.com/linuxfabrik/lfops/tree/main/roles/grafana) role.

If you use the [Setup Icinga2 Master Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_icinga2_master.yml), this is automatically done for you.


## Tags

`icingaweb2_module_grafana`

* Installs and configures the IcingaWeb2 Grafana Module.
* Triggers: none.

`icingaweb2_module_grafana:configure`

* Configures the IcingaWeb2 Grafana Module, excluding the graph configs.
* Triggers: none.

`icingaweb2_module_grafana:monitoring_plugins_graphs`

* Deploys the configuration for the graphs for the [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins).
* Triggers: none.


## Mandatory Role Variables

`icingaweb2_module_grafana__monitoring_plugins_version`

* Which version of the monitoring plugins should be deployed? Possible options:

    * A specific release, for example `1.2.0.11`. See the [Releases](https://github.com/Linuxfabrik/monitoring-plugins/releases).
    * `dev`: The development version (main branch). Use with care. Only works with `monitoring_plugins__install_method: 'source'`.

* Type: String.
* Default: `'{{ lfops__monitoring_plugins_version | default() }}'`

`icingaweb2_module_grafana__version`

* The module version to install. Possible options: https://github.com/NETWAYS/icingaweb2-module-grafana/releases.
* Type: String.

Example:

```yaml
# mandatory
icingaweb2_module_grafana__monitoring_plugins_version: '1.2.0.11'
icingaweb2_module_grafana__version: 'v3.1.3'
```


## Optional Role Variables

`icingaweb2_module_grafana__auth_jwt`

* Enable JWT-based authentication for Grafana requests.
* Type: Bool.
* Default: `'{{ grafana__auth_jwt }}'`

`icingaweb2_module_grafana__auth_jwt__priv_key_file`

* Path to the private key file used for JWT-based Grafana authentication.
* Type: String.
* Default: `'{{ grafana__auth_jwt__priv_key_file }}'`

`icingaweb2_module_grafana__custom_graphs_config`

* Multiline string. Custom configuration for the Grafana Graphs, will be deployed to `/etc/icingweb2/modules/grafana/graphs.ini` along with the configuration for the [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins).
* Type: String.
* Default: `''`

`icingaweb2_module_grafana__default_dashboard`

* Name of the default Grafana dashboard.
* Type: String.
* Default: `'Default'`

`icingaweb2_module_grafana__skip_monitoring_plugins_graphs_config`

* Skip the deployment of the graph configuration for [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins).
* Type: Bool.
* Default: `false`

`icingaweb2_module_grafana__theme`

* The theme for the Grafana graphs. Possible options:

    * `dark`
    * `light`

* Type: String.
* Default: `'light'`

`icingaweb2_module_grafana__url`

* The Grafana URL. This should be reachable from both the IcingaWeb2 server and the client device.
* Type: String.
* Default: `'{{ grafana__root_url }}'`

Example:

```yaml
# optional
icingaweb2_module_grafana__auth_jwt: false
icingaweb2_module_grafana__auth_jwt__priv_key_file: '/etc/grafana/jwt.key.priv'
icingaweb2_module_grafana__custom_graphs_config: |-
  [icingacli-x509]
  dashboard = "Default"
  panelId = "1"
  orgId = ""
  repeatable = "no"
  dashboarduid = "default"
  timerange = "7d"
icingaweb2_module_grafana__default_dashboard: 'Default'
icingaweb2_module_grafana__skip_monitoring_plugins_graphs_config: true
icingaweb2_module_grafana__theme: 'light'
icingaweb2_module_grafana__url: 'https://monitoring.example.com/grafana'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
