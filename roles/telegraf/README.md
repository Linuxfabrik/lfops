# Ansible Role linuxfabrik.lfops.telegraf

This role installs and configures [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/).


## Mandatory Requirements

* Enable the official [InfluxDB repository](https://docs.influxdata.com/influxdb/v1.8/introduction/install/?t=Red+Hat+%26amp%3B+CentOS). This can be done using the [linuxfabrik.lfops.repo_influxdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_influxdb) role.


## Tags

| Tag                  | What it does                           | Reload / Restart |
| ---                  | ------------                           | ---------------- |
| `telegraf`           | Installs and configures telegraf server | Restarts telegraf.service |
| `telegraf:state`     | Manages the state of the telegraf server    | - |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `telegraf__agent_interval` | Default data collection interval for all inputs | `'10s'` |
| `telegraf__conf__host_var` / <br> `telegraf__conf__group_var` | List of dictionaries. Configurations to deploy to `/etc/telegraf/telegraf.d/`. Subkeys:<ul><li>`filename`: Mandatory, string. Destination filename. Normally equal to the name of the source `template` used. Will be suffixed with `.conf`.</li><li>`raw`: Optional, string. Raw content that should be part of the config.</li><li>`state`: Optional, string. Either `present` or `absent`. Defaults to `present`.</li><li>`template`: Mandatory, string. Which template to use for the config. Possible options: `raw` or `graylog`.</li><li>`username`: Optional, string. Username. Set this to the Graylog access token when using `template: 'graylog'`.</li></ul> | [] |
| `telegraf__inputs_cpu_enable` | Read metrics about cpu usage | `true` |
| `telegraf__inputs_disk_enable` | Read metrics about disk usage by mount point | `true` |
| `telegraf__inputs_diskio_enable` | Read metrics about disk IO by device | `true` |
| `telegraf__inputs_kernel_enable` | Get kernel statistics from /proc/stat | `true` |
| `telegraf__inputs_mem_enable` | Read metrics about memory usage | `true` |
| `telegraf__inputs_net_enable` | Gather metrics about network interfaces | `false` |
| `telegraf__inputs_processes_enable` | Get the number of processes and group them by status | `true` |
| `telegraf__inputs_swap_enable` | Read metrics about swap memory usage | `true` |
| `telegraf__inputs_system_enable` | Read metrics about system load & uptime | `true` |
| `telegraf__inputs_vsphere_enable` | Read metrics from one or many vCenters | `false` |
| `telegraf__inputs_vsphere_password` |  | `''` |
| `telegraf__inputs_vsphere_username` |  | `''` |
| `telegraf__inputs_vsphere_vcenters` | List of vCenter URLs to be monitored. | `[]` |
| `telegraf__outputs_influxdb_database` | The target database for metrics; will be created as needed. For UDP url endpoint database needs to be configured on server side. | `''` |
| `telegraf__outputs_influxdb_password` | HTTP Basic Auth | `''` |
| `telegraf__outputs_influxdb_skip_database_creation` | We assume that the InfluxDB role creates the database. | `true` |
| `telegraf__outputs_influxdb_urls` | The full HTTP or UDP URL for your InfluxDB instance. Multiple URLs can be specified for a single cluster, only ONE of the urls will be written to each interval. | `['http://127.0.0.1:8086']` |
| `telegraf__outputs_influxdb_username` | HTTP Basic Auth | `''` |
| `telegraf__service_enabled` | Enables or disables the telegraf service, analogous to `systemctl enable/disable`. | `true` |
| `telegraf__service_state` | Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |

Example:
```yaml
# optional
telegraf__agent_interval: '10s'
telegraf__conf__host_var:
  - filename: 'graylog'
    state: 'present'
    template: 'graylog'
    username: 'linuxfabrik' # graylog access token (need to be sent as the username)
telegraf__inputs_cpu_enable: false
telegraf__inputs_disk_enable: false
telegraf__inputs_diskio_enable: false
telegraf__inputs_kernel_enable: false
telegraf__inputs_mem_enable: false
telegraf__inputs_net_enable: false
telegraf__inputs_processes_enable: false
telegraf__inputs_swap_enable: false
telegraf__inputs_system_enable: false
telegraf__inputs_vsphere_enable: true
telegraf__inputs_vsphere_password: 'password'
telegraf__inputs_vsphere_username: 'username'
telegraf__inputs_vsphere_vcenters:
  - 'https://vsphere/sdk'
telegraf__outputs_influxdb_database: 'telegraf'
telegraf__outputs_influxdb_password: 'password'
telegraf__outputs_influxdb_skip_database_creation: true
telegraf__outputs_influxdb_urls:
  - 'http://127.0.0.1:8086'
telegraf__outputs_influxdb_username: 'telegraf'
telegraf__service_enabled: true
telegraf__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
