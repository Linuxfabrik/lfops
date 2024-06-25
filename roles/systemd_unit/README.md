# Ansible Role linuxfabrik.lfops.systemd_unit

This role installs and manages systemd unit files. A unit file is a plain text ini-style file that encodes information about a service, a socket, a device, a mount point, an automount point, a swap file or partition, a start-up target, a watched file system path, a timer controlled and supervised by systemd, a resource management slice or a group of externally created processes. See `systemd.unit` for unit configuration, `systemd.syntax(7)` for a general description of the syntax, and [load-fragment-gperf.gperf.in](https://github.com/systemd/systemd/blob/main/src/core/load-fragment-gperf.gperf.in) for a list of all directives and their context.


## Tags

| Tag           | What it does                                 |
| ---           | ------------                                 |
| `systemd_unit` | <ul><li>Remove service units from `/etc/systemd/system`</li><li>Deploy the service units to `/etc/systemd/system`</li><li>Remove timer units from `/etc/systemd/system`</li><li>Deploy the timer units to `/etc/systemd/system`</li></ul> |
| `systemd_unit:mounts` | Manages systemd mount units. |
| `systemd_unit:services` | <ul><li>Remove service units from `/etc/systemd/system`</li><li>Deploy the service units to `/etc/systemd/system`</li></ul> |
| `systemd_unit:state` | Manages the state of the unit file |
| `systemd_unit:timers` | <ul><li>Remove timer units from `/etc/systemd/system`</li><li>Deploy the timer units to `/etc/systemd/system`</li></ul> |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `systemd_unit__mounts__host_var` /<br> `systemd_unit__mounts__group_var` | List of Systemd Mount Units. Subkeys:<ul><li>`name`: Mandatory, string. Name of the systemd mount. Will be used as the filename. Note mount units must be named after the mount point directories they control. Use `systemd-escape --path /mnt/my-folder`.</li><li>`description`: Optional, string. The description for the unit. If ommitted, the name will be used, suffixed by `Mount`.</li><li>`wanted_by`: Optional, string. Value for `WantedBy`. Defaults to `'default.target'`.</li><li>`raw_unit`: Optional, string. Raw block in the `[Unit]` section. Defaults to unset.</li><li>`raw_mount`: Optional, string. Raw block in the `[Mount]` section. Defaults to unset.</li><li>`raw_install`: Optional, string. Raw block in the `[Install]` section. Defaults to unset.</li><li>`state`: Optional, string. State of the unit. Possible options: `present`, `absent`, `started`, `stopped`, `restarted`, `reloaded`. Defaults to `started`.</li><li>`enabled`: Optional, boolean. If the unit should start at boot or not. Defaults to `true`.</li></ul> | `[]` |
| `systemd_unit__services__host_var` /<br> `systemd_unit__services__group_var` | List of Systemd Service Units. Subkeys:<ul><li>`name`: Mandatory, string. Name of the systemd service. Will be used as the filename.</li><li>`description`: Optional, string. The description for the unit. If ommitted, the name will be used, suffixed by `Service`.</li><li>`wanted_by`: Optional, string. Value for `WantedBy`. Defaults to `'default.target'`.</li><li>`raw_unit`: Optional, string. Raw block in the `[Unit]` section. Defaults to unset.</li><li>`raw_service`: Optional, string. Raw block in the `[Service]` section. Defaults to unset.</li><li>`raw_install`: Optional, string. Raw block in the `[Install]` section. Defaults to unset.</li><li>`state`: Optional, string. State of the unit. Possible options: `present`, `absent`, `started`, `stopped`, `restarted`, `reloaded`. Defaults to `started`.</li><li>`enabled`: Optional, boolean. If the unit should start at boot or not. Defaults to `true`.</li></ul> | `[]` |
| `systemd_unit__timers__host_var` /<br> `systemd_unit__timers__group_var` | List of Systemd Timer Units. Subkeys:<ul> <li>`name`: Mandatory, string. Name of the systemd timer. Will be used as the filename.</li> <li>`description`: Optional, string. The description for the unit. If ommitted, the name will be used, suffixed by `Timer`.</li> <li>`wanted_by`: Optional, string. Value for `WantedBy`. Defaults to `'default.target'`.</li> <li>`raw_unit`: Optional, string. Raw block in the `[Unit]` section. Defaults to unset.</li> <li>`raw_timer`: Optional, string. Raw block in the `[Service]` section. Defaults to unset.</li> <li>`raw_install`: Optional, string. Raw block in the `[Install]` section. Defaults to unset.</li> <li>`state`: Optional, string. State of the unit. Possible options: `present`, `absent`, `started`, `stopped`, `restarted`, `reloaded`. Defaults to `started`.</li> <li>`enabled`: Optional, boolean. If the unit should start at boot or not. Defaults to `true`.</li></ul> | `[]` |

Example:
```yaml
# optional
systemd_unit__mounts__host_var:
  - name: 'mnt-my\x2dfolder'
    raw_mount: |-
      What=//srv1/my-share
      Where=/mnt/my-folder
      Type=cifs
      Options=credentials=/root/.smbcreds,domain=example.com,vers=default
    enabled: true
    state: 'present'

# two services, one with more options, one minimal
systemd_unit__services__host_var:
  - name: 'fwb'
    description: 'Firewall Builder'
    raw_unit: |-
      After=default.target openvpn-server@server.service fail2ban.service
    raw_service: |-
      ExecReload=/etc/fwb.sh start
      ExecStart=/etc/fwb.sh start
      ExecStop=/etc/fwb.sh stop
      RemainAfterExit=yes
      Type=oneshot
    wanted_by: 'basic.target'
    state: 'present'
    enabled: true
  - name: 'duba'
    raw_service: |-
      ExecStart=/usr/local/bin/duba
      Type=oneshot

# two timers, one with more options, one minimal
systemd_unit__timers__host_var:
  - name: 'python-venv-update@'
    description: 'python-venv update timer for /opt/python-venv/%i'
    raw_timer: |-
      OnCalendar=daily
      Unit=python-venv@%i.service
    wanted_by: 'timers.target'
    state: 'present'
    enabled: true
  - name: 'duba'
    raw_timer: |-
      OnCalendar=daily
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
