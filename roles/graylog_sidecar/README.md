# Ansible Role linuxfabrik.lfops.graylog_sidecar

This role installs and configures the [Graylog Sidecar](https://go2docs.graylog.org/current/getting_in_log_data/install_sidecar_on_linux.htm). The Sidecar is a lightweight agent that runs on log-producing hosts, fetches collector configurations from a Graylog server and supervises the log collector backends (Filebeat etc.) that ship the logs.


*Available in the next LFOps release.*


## How the Role Behaves

* The configuration file `/etc/graylog/sidecar/sidecar.yml` is fully templated. On every run it is re-rendered from the role's template (a timestamped backup is kept), so out-of-band manual edits are overwritten. Manage all settings through the role variables below.
* A configuration change notifies a handler that restarts `graylog-sidecar.service`. The restart is skipped when the service was just started in the same run (redundant), when `graylog_sidecar__service_state` is `stopped`, or when restarts are deferred LFOps-wide via `lfops__skip_restart_handlers`.
* The systemd unit is registered once via `graylog-sidecar -service install`. The package ships no unit file, the binary generates `/etc/systemd/system/graylog-sidecar.service` and enables it. The task is guarded so it runs only when the unit file is missing, because a second call fails instead of doing nothing. As a side effect of the generator enabling the unit, a run limited to `--tags graylog_sidecar:configure` leaves the service enabled even when `graylog_sidecar__service_enabled` is `false`; a full run corrects this afterwards.
* This role does not install or configure collector backends and does not assign collector configurations. Manage those in the Graylog web UI under *System/Sidecars*, matching them to the sidecar via `graylog_sidecar__tags`. What a host actually ships is therefore decided on the server, not in this role's variables.
* The sidecar runs as `root` and executes the collector binaries the server tells it to. `graylog_sidecar__collector_binaries_accesslist` is the boundary for that trust: only listed paths may be executed. Keep it as tight as your collectors allow.
* `/etc/graylog/sidecar/sidecar.yml` contains `graylog_sidecar__server_api_token` and is deployed `0600 root:root`. The timestamped backups the role keeps next to it inherit those permissions.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* The Graylog Sidecar repository must be enabled (role: [linuxfabrik.lfops.repo_graylog_sidecar](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_graylog_sidecar)). The `graylog-sidecar` package is served from it.


## Requirements

* A reachable Graylog server.

Manual steps:

* Create an API token for the sidecar in the Graylog web UI under *System/Sidecars* and store it in your inventory as `graylog_sidecar__server_api_token`.


## Tags

`graylog_sidecar`

* Installs the `graylog-sidecar` package, deploys the configuration and ensures the service is in the desired state.
* Triggers: graylog-sidecar.service restart.

`graylog_sidecar:configure`

* Deploys the configuration file and registers the systemd unit.
* Triggers: graylog-sidecar.service restart.

`graylog_sidecar:state`

* Manages the service state (start, stop, enable, disable).
* Triggers: none.


## Mandatory Role Variables

`graylog_sidecar__server_api_token`

* The API token to authenticate against the Graylog server API. Create one in the Graylog web UI under *System/Sidecars*.
* Type: String.

`graylog_sidecar__server_url`

* The URL to the Graylog server API.
* Type: String.

Example:
```yaml
# mandatory
graylog_sidecar__server_api_token: 'linuxfabrik'
graylog_sidecar__server_url: 'http://graylog.example.com:9000/api/'
```


## Optional Role Variables

`graylog_sidecar__collector_binaries_accesslist`

* Absolute paths of the binaries the Graylog server is allowed to make this sidecar execute. Wildcards follow [Go's `filepath.Match`](https://pkg.go.dev/path/filepath#Match). The default mirrors the sidecar's own platform default for Linux, so the role changes nothing about which collectors may run; it only makes the list visible and configurable. Narrow it to the collectors you actually use. An empty list disables the check altogether, which lets anyone able to edit a collector configuration in the Graylog web UI execute an arbitrary binary as `root` on every host running this sidecar.
* Type: List of strings.
* Default:

    ```yaml
    - '/usr/bin/auditbeat'
    - '/usr/bin/filebeat'
    - '/usr/bin/heartbeat'
    - '/usr/bin/journalbeat'
    - '/usr/bin/metricbeat'
    - '/usr/bin/nxlog'
    - '/usr/bin/packetbeat'
    - '/usr/lib/graylog-sidecar/auditbeat'
    - '/usr/lib/graylog-sidecar/filebeat'
    - '/usr/share/auditbeat/bin/auditbeat'
    - '/usr/share/filebeat/bin/filebeat'
    - '/usr/share/heartbeat/bin/heartbeat'
    - '/usr/share/journalbeat/bin/journalbeat'
    - '/usr/share/metricbeat/bin/metricbeat'
    - '/usr/share/packetbeat/bin/packetbeat'
    - '/opt/nxlog/bin/nxlog'
    ```

`graylog_sidecar__node_name`

* The node name of the sidecar. If empty, the sidecar uses the hostname of the host it runs on.
* Type: String.
* Default: `''`

`graylog_sidecar__send_status`

* Transmit detailed sidecar information like collector statuses, metrics and log file lists. Disabling it reduces load on the Graylog server but disables some features in the server UI.
* Type: Bool.
* Default: `true`

`graylog_sidecar__service_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`graylog_sidecar__service_state`

* Changes the state of the service, analogous to `systemctl start/stop/restart/reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'`

`graylog_sidecar__tags`

* Tags to assign to this sidecar. Collector configurations matching any of these tags are automatically applied to the sidecar. Defaults to `default`, the tag of the collector configuration Graylog ships out of the box, so a freshly deployed sidecar starts collecting without further setup. Set to an empty list to register the sidecar without applying any configuration.
* Type: List of strings.
* Default: `['default']`

`graylog_sidecar__tls_skip_verify`

* Skip the verification of TLS connections to the Graylog server.
* Type: Bool.
* Default: `false`

`graylog_sidecar__update_interval`

* How often, in seconds, the sidecar contacts the Graylog server for keep-alive and configuration update requests.
* Type: Number.
* Default: `10`

Example:
```yaml
# optional
graylog_sidecar__collector_binaries_accesslist:
  - '/usr/lib/graylog-sidecar/filebeat'
graylog_sidecar__node_name: 'web01'
graylog_sidecar__send_status: true
graylog_sidecar__service_enabled: true
graylog_sidecar__service_state: 'started'
graylog_sidecar__tags:
  - 'linux'
  - 'webserver'
graylog_sidecar__tls_skip_verify: false
graylog_sidecar__update_interval: 10
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
