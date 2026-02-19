# Ansible Role linuxfabrik.lfops.systemd_journald

This role configures Systemd's logging service "journald".

From `man journald.conf`:

* `SystemKeepFree=` control how much disk space systemd-journald shall leave free for other uses.
* `SystemMaxUse=` control how much disk space the journal may use up at most.
* `systemd-journald` will respect both limits and use the smaller of the two values.

Example with numbers on a 100G disk:

* `SystemKeepFree=10G` means that journald may use at most `100G - 10G = 90G`
* `SystemMaxUse=20G`

Whenever journald needs to free space, it computes `min(90G, 20G)`, and then deletes archived journal files until usage <= that value. Here, journald will grow the journal up to about 20G, then start deleting archived files to stay under that cap.


## Tags

| Tag                      | What it does                              | Reload / Restart |
| ---                      | ------------                              | ---------------- |
| `systemd_journald`       | Manages the journald config               | Restarts systemd-journald.service |
| `systemd_journald:state` | Manages the state of the journald service | - |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `systemd_journald__conf_storage` | Controls where to store journal data. Have a look at `man 5 journald.conf`. Possible options: <br> * `volatile` <br> * `persistent` <br> * `auto` <br> * `none` | `'persistent'` |
| `systemd_journald__conf_system_keep_free` | Controls how much disk space systemd-journald shall leave free for other uses. Unlike in `journald.conf`, you may also specify a percentage value, which will be automatically converted to bytes based on the partition size. | `'70%'` |
| `systemd_journald__conf_system_max_use` | Controls how much disk space the journal may use up at most. Unlike in `journald.conf`, you may also specify a percentage value, which will be automatically converted to bytes based on the partition size. | `30%` |
| `systemd_journald__service_enabled`| Enables or disables the service, analogous to `systemctl enable/disable`. | `true` |
| `systemd_journald__service_state` | Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |

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
