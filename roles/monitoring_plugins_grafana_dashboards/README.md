# Ansible Role linuxfabrik.lfops.monitoring_plugins_grafana_dashboards

This role deploys the Monitoring Plugins Grafana Dashboards for a Grafana Server via provisioning.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Install and configure Grafana with the required provisioning config. This can be done using the [linuxfabrik.lfops.grafana](https://github.com/Linuxfabrik/lfops/tree/main/roles/grafana) role.

If you use the ["Monitoring Plugins Grafana Dashboards" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/monitoring_plugins_grafana_dashboards.yml) or ["Setup Icinga2 Master" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_icinga2_master.yml), this is automatically done for you.


## Tags

| Tag           | What it does                                 |
| ---           | ------------                                 |
| `monitoring_plugins_grafana_dashboards` | Deploys the Monitoring Plugins Grafana Dashboards. |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `monitoring_plugins_grafana_dashboard__director_database_login` | The login for the Director SQL database. Only needs to have read permissions. |
| `monitoring_plugins_grafana_dashboard__influxdb_login` | The login for the InfluxDB database. Only needs to have read permissions. |

Example:
```yaml
# mandatory
monitoring_plugins_grafana_dashboard__director_database_login:
  username: 'dashboard'
  password: 'linuxfabrik'
monitoring_plugins_grafana_dashboard__influxdb_login:
  username: 'dashboard'
  password: 'linuxfabrik'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `monitoring_plugins_grafana_dashboard__director_database_host` | The host of the Director SQL database. | `'127.0.0.1'` |
| `monitoring_plugins_grafana_dashboard__director_database_name` | The name of the Director SQL database. | `'{{ icingaweb2_module_director__database_name }}'` |
| `monitoring_plugins_grafana_dashboard__influxdb_database_name` | The name of the InfluxDB database. | `'{{ icinga2_master__influxdb_database_name }}'` |
| `monitoring_plugins_grafana_dashboard__influxdb_host` | The host of the InfluxDB database. | `'{{ icinga2_master__influxdb_host }}'` |
| `monitoring_plugins_grafana_dashboards__repo_version` | The version of the monitoring plugins that will be used for the grafana dashboards. Possible options: * `latest`: The **latest stable** release. See the [Releases](https://github.com/Linuxfabrik/monitoring-plugins/releases).<br> * `main`: The development version. Use with care.<br> * A specific release, for example `2022030201`. See the [Releases](https://github.com/Linuxfabrik/monitoring-plugins/releases). | `'{{ lfops__monitoring_plugins_version \| default("latest") }}'` |

Example:
```yaml
# optional
monitoring_plugins_grafana_dashboard__director_database_host: 'localhost'
monitoring_plugins_grafana_dashboard__director_database_name: 'my-db'
monitoring_plugins_grafana_dashboard__influxdb_database_name: 'my-director-db'
monitoring_plugins_grafana_dashboard__influxdb_host: '127.0.0.1'
monitoring_plugins_grafana_dashboards__repo_version: '2022072001'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
