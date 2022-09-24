# Ansible Role linuxfabrik.lfops.openvpn_server

This role installs and configures [OpenVPN](https://openvpn.net/) as a server. Currently, the only supported configuration is a multi-client server. A corresponding client config will be generated to `/tmp/` on the ansible control node.

This role does not configure OpenVPN logging via `log-append /var/log/openvpn.log`. Instead it configures OpenVPN to use Journald, because there we get log entries including timestamps etc. To inspect the logs, use `journalctl --unit=openvpn-server@server -f` for example.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Create a certificate for the OpenVPN server and save it on the ansible control node as `{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc/openvpn/server/server.p12`.
* Generate a certificate revocation list and save it on the ansible control node as `{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc/openvpn/server/crl.pem`.
* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Install Python 3, and the python3-policycoreutils module (required for the SELinux Ansible tasks). This can be done using the [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils) role.


## Tags

| Tag                    | What it does                             |
| ---                    | ------------                             |
| `openvpn_server`       | Installs and configures OpenVPN          |
| `openvpn_server:state` | Manages the state of the OpenVPN service |


## Mandatory Role Variables

| Variable                         | Description                                                                                                                                   |
| --------                         | -----------                                                                                                                                   |
| `openvpn_server__client_network` | The network in which the OpenVPN server should allocate client addresses, where `openvpn_server__client_netmask` will be used as the netmask. |

Example:
```yaml
# mandatory
openvpn_server__client_network: '192.0.2.0'
```


## Optional Role Variables

| Variable                          | Description                                                                                             | Default Value     |
| --------                          | -----------                                                                                             | -------------     |
| `openvpn_server__client_netmask`  | The netmask that will be used with `openvpn_server__client_network` to allocate client addresses.       | `'255.255.255.0'` |
| `openvpn_server__port`            | Which port the OpenVPN server should use.                                                               | `1194`            |
| `openvpn_server__pushs`           | A list of options that will be pushed to the connected clients. Can be used to set routes.              | `[]`              |
| `openvpn_server__service_enabled` | Enables or disables the `openvpn-server@server` service, analogous to `systemctl enable/disable --now`. | `true`            |

Example:
```yaml
# optional
openvpn_server__client_netmask: '255.255.255.0'
openvpn_server__port: 1194
openvpn_server__pushs:
  - 'route 192.0.2.0 255.255.255.0'
openvpn_server__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
