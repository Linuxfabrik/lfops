# Ansible Role linuxfabrik.lfops.wireguard_server

This role installs and configures [wireguard](https://www.wireguard.com/install/) as server.

Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Tags

| Tag                          | What it does                                |
| ---                          | ------------                                |
| `wireguard_server`           | Installs and configures wireguard as server |
| `wireguard_server:configure` | Configures wireguard as server              |
| `wireguard_server:rekey`     | Deletes keys and generates new ones         |
| `wireguard_server:state`     | Manages the state of the wireguard service  |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `wireguard_server__ipaddress` | The client's ip address within the VPN. |

Example:
```yaml
# mandatory
wireguard_server__ipaddress: '10.8.0.2/24'
```

## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `wireguard_server__interface` | The name of the tunnel interface. | `'wg0'` |
| `wireguard_server__service_enabled` | Enables or disables the wireguard service, analogous to `systemctl enable/disable`. | `true` |
| `wireguard_server__service_state` | Changes the state of the wireguard service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded`. | `'started'` |

Example:
```yaml
# optional
wireguard_server__interface: 'wg0'
wireguard_server__service_enabled: true
wireguard_server__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
