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
| `systemd_journald__conf_system_keep_free` | Controls how much disk space systemd-journald shall leave free for other uses. Unlike in `journald.conf`, you may also specify a percentage value, which will be automatically converted to bytes based on the partition size. | `'15%'` |
| `systemd_journald__conf_system_max_use` | Controls how much disk space the journal may use up at most. Unlike in `journald.conf`, you may also specify a percentage value, which will be automatically converted to bytes based on the partition size. | `5G` |
| `systemd_journald__service_enabled`| Enables or disables the service, analogous to `systemctl enable/disable`. | `true` |
| `systemd_journald__service_state` | Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |

systemd-journald will respect both limits `systemd_journald__conf_system_keep_free` and `systemd_journald__conf_system_max_use` and use the smaller of the two values.

Example:
```yaml
# optional
systemd_journald__conf_storage: 'persistent'
systemd_journald__conf_system_keep_free: '20%'
systemd_journald__conf_system_max_use: '5G'
systemd_journald__service_enabled: true
systemd_journald__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
