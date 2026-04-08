# Ansible Role linuxfabrik.lfops.telegraf

This role installs and configures [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/).


## Mandatory Requirements

* Enable the official [InfluxDB repository](https://docs.influxdata.com/influxdb/v1.8/introduction/install/?t=Red+Hat+%26amp%3B+CentOS). This can be done using the [linuxfabrik.lfops.repo_influxdb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_influxdb) role.

If you use the [telegraf playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/telegraf.yml), this is automatically done for you.


## Tags

`telegraf`

* Installs and configures telegraf server.
* Triggers: telegraf.service restart.

`telegraf:state`

* Manages the state of the telegraf server.
* Triggers: none.


## Optional Role Variables

`telegraf__agent_interval`

* Default data collection interval for all inputs.
* Type: String.
* Default: `'10s'`

`telegraf__conf__host_var` / `telegraf__conf__group_var`

* Configurations to deploy to `/etc/telegraf/telegraf.d/`.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `filename`:

        * Mandatory. Destination filename. Normally equal to the name of the source `template` used. Will be suffixed with `.conf`.
        * Type: String.

    * `raw`:

        * Optional. Raw content that should be part of the config. Only used when `template: 'raw'`.
        * Type: String.
        * Default: unset

    * `state`:

        * Optional. Either `present` or `absent`.
        * Type: String.
        * Default: `'present'`

    * `template`:

        * Mandatory. Which template to use for the config. Possible options: `raw` or `graylog`.
        * Type: String.

    * `username`:

        * Optional. Username. Set this to the Graylog access token when using `template: 'graylog'`.
        * Type: String.
        * Default: unset

    * `by_role`:

        * Optional. Name of the role that generated this config (for documentation purposes in the generated file).
        * Type: String.
        * Default: unset

`telegraf__inputs_cpu_enable`

* Read metrics about cpu usage.
* Type: Bool.
* Default: `true`

`telegraf__inputs_disk_enable`

* Read metrics about disk usage by mount point.
* Type: Bool.
* Default: `true`

`telegraf__inputs_diskio_enable`

* Read metrics about disk IO by device.
* Type: Bool.
* Default: `true`

`telegraf__inputs_kernel_enable`

* Get kernel statistics from `/proc/stat`.
* Type: Bool.
* Default: `true`

`telegraf__inputs_mem_enable`

* Read metrics about memory usage.
* Type: Bool.
* Default: `true`

`telegraf__inputs_net_enable`

* Gather metrics about network interfaces.
* Type: Bool.
* Default: `false`

`telegraf__inputs_processes_enable`

* Get the number of processes and group them by status.
* Type: Bool.
* Default: `true`

`telegraf__inputs_swap_enable`

* Read metrics about swap memory usage.
* Type: Bool.
* Default: `true`

`telegraf__inputs_system_enable`

* Read metrics about system load & uptime.
* Type: Bool.
* Default: `true`

`telegraf__inputs_vsphere_enable`

* Read metrics from one or many vCenters.
* Type: Bool.
* Default: `false`

`telegraf__inputs_vsphere_password`

* Password for vSphere authentication.
* Type: String.
* Default: `''`

`telegraf__inputs_vsphere_username`

* Username for vSphere authentication.
* Type: String.
* Default: `''`

`telegraf__inputs_vsphere_vcenters`

* vCenter URLs to be monitored.
* Type: List.
* Default: `[]`

`telegraf__outputs_influxdb_database`

* The target database for metrics; will be created as needed. For UDP url endpoint database needs to be configured on server side.
* Type: String.
* Default: `''`

`telegraf__outputs_influxdb_password`

* Password for HTTP Basic Auth to InfluxDB.
* Type: String.
* Default: `''`

`telegraf__outputs_influxdb_skip_database_creation`

* Skip database creation (we assume the InfluxDB role creates the database).
* Type: Bool.
* Default: `true`

`telegraf__outputs_influxdb_urls`

* The full HTTP or UDP URL for your InfluxDB instance. Multiple URLs can be specified for a single cluster, only ONE of the urls will be written to each interval.
* Type: List.
* Default: `['http://127.0.0.1:8086']`

`telegraf__outputs_influxdb_username`

* Username for HTTP Basic Auth to InfluxDB.
* Type: String.
* Default: `''`

`telegraf__service_enabled`

* Enables or disables the telegraf service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`telegraf__service_state`

* Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options: `started`, `stopped`, `restarted`, `reloaded`.
* Type: String.
* Default: `'started'`

Example:
```yaml
# optional
telegraf__agent_interval: '30s'
telegraf__conf__host_var:
  - filename: 'graylog'
    state: 'present'
    template: 'graylog'
    username: 'linuxfabrik' # graylog access token (needs to be sent as the username)
  - filename: 'custom-input'
    state: 'present'
    template: 'raw'
    raw: |
      [[inputs.exec]]
        commands = ["/usr/local/bin/my-custom-script.sh"]
        data_format = "influx"
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
