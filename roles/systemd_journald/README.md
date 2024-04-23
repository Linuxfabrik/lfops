# Ansible Role linuxfabrik.lfops.systemd_journald

This role configures Systemd's logging service "journald".


## Tags

| Tag                      | What it does                              |
| ---                      | ------------                              |
| `systemd_journald`       | Manages the journald config               |
| `systemd_journald:state` | Manages the state of the journald service |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `systemd_journald__conf_storage` | Controls where to store journal data. Have a look at `man 5 journald.conf`. Possible options: <br> * `volatile` <br> * `persistent` <br> * `auto` <br> * `none` | `'persistent'` |
| `systemd_journald__conf_system_max_use` | Percentage of the filesystem under `/var/log/journal` which may be used by journald. | `40` |
| `systemd_journald__service_enabled`| Enables or disables the service, analogous to `systemctl enable/disable`. | `true` |
| `systemd_journald__service_state` | Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |

Example:
```yaml
# optional
systemd_journald__conf_storage: 'persistent'
systemd_journald__conf_system_max_use: 10
systemd_journald__service_enabled: true
systemd_journald__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
