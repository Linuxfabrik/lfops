# Ansible Role linuxfabrik.lfops.rsyslog

This role installs and configures [rsyslog](https://www.rsyslog.com/). Useful for configuring log forwarding, for example to a Graylog server.

Runs on

* RHEL 8 (and compatible)


## Tags

| Tag                 | What it does                                     |
| ---                 | ------------                                     |
| `rsyslog`           | Installs and configures rsyslog                  |
| `rsyslog:configure` | Deploys the configuration                        |
| `rsyslog:state`     | Manages the state of the rsyslog systemd service |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `rsyslog__conf__group_var` /<br> `rsyslog__conf__host_`var` | A list of rsyslog configs that should be deployed to `/etc/rsyslog.d/`. Subkeys:<ul><li>`template`: Mandatory, string. Name of the Jinja template source file to use. Have a look at the possible options [here](https://github.com/Linuxfabrik/lfops/tree/main/roles/rsyslog/templates/etc/rsyslog.d/).</li> <li>`filename`: Mandatory, string. Destination filename in `/etc/rsyslog.d/`, and normally is equal to the name of the source `template` used. Will be suffixed with `.conf`.</li> <li>`state`: Optional, string. State of the config. Possible options: `absent`, `present`. Defaults to `present`.</li> <li>`raw`: Optional, string: Raw content for the config.</li></ul> For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `rsyslog__service_enabled` | Enables or disables the rsyslog service, analogous to `systemctl enable/disable`. | `true` |
| `rsyslog__service_state` | Changes the state of the rsyslog service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |

Example:
```yaml
# optional
rsyslog__conf__group_var: []
rsyslog__conf__host_var:
  - filename: 'my-old-config'
    state: 'absent'
  - filename: 'graylog'
    comment: |-
      Relay logs to Graylog
    state: 'present'
    template: 'raw'
    raw: |-
      # rsyslog v7 filter conditions:
      # contains isequal startswith regex ereregex
      # http://www.rsyslog.com/doc/v7-stable/configuration/filters.html
      if (
          $msg startswith "GSSAPI client step " or
          $msg startswith "GSSAPI server step " or
          ($programname == "kernel" and $msg startswith "RULE ") or
          ($programname == "systemd" and ($msg startswith "Created slice " or $msg startswith "Removed slice ")) or
          ($programname == "systemd" and ($msg startswith "Starting user-" or $msg startswith "Stopping user-")) or
          ($programname == "systemd" and ($msg startswith "Starting Session " or $msg startswith "Started Session ")) or
          ($programname == "systemd-logind" and ($msg startswith "New Session " or $msg startswith "Removed Session "))
      )
      then
          # ignore, do not foward
          continue
      else
          *.* @graylog.example.com:1514;RSYSLOG_SyslogProtocol23Format
rsyslog__service_enabled: true
rsyslog__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
