# Ansible Role linuxfabrik.lfops.haveged

This role installs [haveged](https://github.com/jirka-h/haveged).


## Tags

| Tag       | What it does     | Reload / Restart |
| ---       | ------------     | ---------------- |
| `haveged` | Installs haveged | - |
| `haveged:state` | Manages the state of the systemd service | - |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `haveged__service_enabled`| Enables or disables the service, analogous to `systemctl enable/disable`. | `true` |
| `haveged__service_state` | Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options: <ul><li>`started`</li><li>`stopped`</li><li>`restarted`</li><li>`reloaded`</li></ul> | `'started'` |

Example:
```yaml
# optional
haveged__service_enabled: true
haveged__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
