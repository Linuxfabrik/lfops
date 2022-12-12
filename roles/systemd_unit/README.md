# Ansible Role linuxfabrik.lfops.systemd_unit

This role creates and manages various [Python 3 virtual environments (venv)](https://docs.python.org/3/library/venv.html). These are placed below `/opt/python-venv/` on the target system.

Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Fedora 35


## Mandatory Requirements

* Install Python 3


## Tags

| Tag           | What it does                                 |
| ---           | ------------                                 |
| `systemd_unit` | Creates and manages the virtual environments |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `systemd_unit__service_host_var` /<br> `systemd_unit__service_group_var` | List of Systemd Units. Subkeys:<ul><li>`name`: Mandatory, string. Name of the systemd service. Will be used as the filename.</li><li>`description`: Mandatory, string. The description for the unit.</li><li>`wanted_by`: Optional, string. Value for `WantedBy`. Defaults to `'default.target'`.</li><li>`unit_raw`: Optional, string. Raw block in the `[Unit]` section. Defaults to unset.</li><li>`service_raw`: Optional, string. Raw block in the `[Service]` section. Defaults to unset.</li><li>`install_raw`: Optional, string. Raw block in the `[Install]` section. Defaults to unset.</li><li>`state`: Optinal, string. State of the unit. Possible options: `present`, `absent`, `started`, `stopped`, `restarted`, `reloaded`. Defaults to `started`.</li><li>`enabled`: Optional, boolean. If the unit should start at boot or not. Defaults to `true`.</li></ul> <br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `systemd_unit__timer_host_var` /<br> `systemd_unit__timer_group_var` | List of Systemd Timers. Subkeys:<ul> <li>`name`: Mandatory, string. Name of the systemd timer. Will be used as the filename.</li> <li>`description`: Mandatory, string. The description for the unit.</li> <li>`wanted_by`: Optional, string. Value for `WantedBy`. Defaults to `'default.target'`.</li> <li>`unit_raw`: Optional, string. Raw block in the `[Unit]` section. Defaults to unset.</li> <li>`timer_raw`: Optional, string. Raw block in the `[Service]` section. Defaults to unset.</li> <li>`install_raw`: Optional, string. Raw block in the `[Install]` section. Defaults to unset.</li> <li>`state`: Optinal, string. State of the unit. Possible options: `present`, `absent`, `started`, `stopped`, `restarted`, `reloaded`. Defaults to `started`.</li> <li>`enabled`: Optional, boolean. If the unit should start at boot or not. Defaults to `true`.</li></ul><br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |

Example:
```yaml
# optional
systemd_unit__services__host_var:
  - name: 'mirror-update'
    description: 'Update the mirror'
    raw_service: |-
      ExecStart=/opt/mirror/mirror-update
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
