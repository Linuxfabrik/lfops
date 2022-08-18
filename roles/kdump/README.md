# Ansible Role linuxfabrik.lfops.kdump

This role stops and disables the `kdump` service. Since most of the time, kdump is not required, but permanently reserves space in the memory for the capture kernel, we usually disable it.

Tested on

* RHEL 8 (and compatible)


## Tags

| Tag     | What it does                           |
| ---     | ------------                           |
| `kdump` | Stops and disables the `kdump` service |


## Optional Role Variables

| Variable                 | Description                                                                                                                                                                  | Default Value |
| --------                 | -----------                                                                                                                                                                  | ------------- |
| `kdump__service_enabled` | Enables or disables the kdump service, analogous to `systemctl enable/disable`.                                                                                              | `false`       |
| `kdump__service_state`   | Changes the state of the kdump service, analogous to `systemctl start/stop/restart/reload`. Possible options: * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'stopped'`   |

Example:
```yaml
# optional
kdump__service_enabled: false
kdump__service_state: 'stopped'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
