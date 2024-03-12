# Ansible Role linuxfabrik.lfops.wireguard_client

This role installs and configures [wireguard](https://www.wireguard.com/install/) as client.

Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Tags

| Tag                          | What it does                                |
| ---                          | ------------                                |
| `wireguard_client`           | Installs and configures wireguard as client |
| `wireguard_client:configure` | Configures wireguard as client              |
| `wireguard_client:rekey`     | Deletes keys and generates new ones         |
| `wireguard_client:state`     | Manages the state of the wireguard service  |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `wireguard_client__ipaddress` | The client's ip address within the VPN. |
| `wireguard_client__wireguard_server` | The server where the wireguard server is running. Has to be reachable only from the ansible deployment host, not the wireguard client itself. |
| `wireguard_client__server_endpoint_ipaddress` | The physical IP address of the wireguard server. Has to be reachable from the wireguard client. |

Example:
```yaml
# mandatory
wireguard_client__ipaddress: '10.8.0.2/24'
wireguard_client__wireguard_server: 'wireguard-server@example.com'
wireguard_client__server_endpoint_ipaddress: '192.0.2.1'
```

## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `wireguard_client__interface` | The name of the tunnel interface. | `'wg0'` |
| `wireguard_client__persistent_keepalive` | Because NAT and stateful firewalls keep track of "connections", if a peer behind NAT or a firewall wishes to receive incoming packets, he must keep the NAT/firewall mapping valid, by periodically sending keepalive packets. When this option is enabled, a keepalive packet is sent to the server endpoint once every interval seconds. A sensible interval that works with a wide variety of firewalls is 25 seconds. Setting it to 0 turns the feature off. | `0` |
| `wireguard_client__server_endpoint_port` | The port of the wireguard server. Has to be reachable from the wireguard client. | `51820` |
| `wireguard_client__service_enabled` | Enables or disables the wireguard service, analogous to `systemctl enable/disable`. | `true` |
| `wireguard_client__service_state` | Changes the state of the wireguard service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded`. | `'started'` |

Example:
```yaml
# optional
wireguard_client__interface: 'wg0'
wireguard_client__persistent_keepalive: 25
wireguard_client__server_endpoint_port: 51820
wireguard_client__service_enabled: true
wireguard_client__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
