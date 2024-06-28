# Ansible Role linuxfabrik.lfops.openvpn_server

This role installs and configures [OpenVPN](https://openvpn.net/) as a server. Currently, the only supported configuration is a multi-client server. A corresponding client config will be generated to `/tmp/` on the ansible control node.

This role does not configure OpenVPN logging via `log-append /var/log/openvpn.log`. Instead it configures OpenVPN to use Journald, because there we get log entries including timestamps etc. To inspect the logs, use `journalctl --unit=openvpn-server@server -f` for example.


## Mandatory Requirements

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Install Python 3, and the python3-policycoreutils module (required for the SELinux Ansible tasks). This can be done using the [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils) role.


## Optional Requirements

* Create a certificate for the OpenVPN server and save it on the ansible control node as `{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc/openvpn/server/server.p12`.
* Generate a certificate revocation list and save it on the ansible control node as `{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc/openvpn/server/crl.pem`.


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

For details see `man openvpn`.

| Variable                          | Description                                                                                             | Default Value     |
| --------                          | -----------                                                                                             | -------------     |
| `openvpn_server__client_configs` | List of client configs. Can be used to limit a client to a certain IP, which then can be used during firewalling. Subkeys <ul><li>`name`: Mandatory, string. Name of hte client's X509 common name.</li><li>`raw`: Mandatory, string. Raw config for this client.</li><li>`state`: Optional, string. If the config should be `present` or `absent`. Defaults to `present`.</li></ul> | `[]`|
| `openvpn_server__client_netmask`  | The netmask that will be used with `openvpn_server__client_network` to allocate client addresses.       | `'255.255.255.0'` |
| `openvpn_server__crl_verify` | Check peer certificate against a Certificate Revocation List. If defined, it expects this file on the remote host in the specified location. If not defined, it expects a `crl.pem` in `host_vars/{{ inventory_hostname }}/etc/openvpn/server/server.p12` and will copy it to the remote host. | unset |
| `openvpn_server__pkcs12` | Specify a PKCS #12 file containing local private key, local certificate, and root CA certificate. This option can be used instead of `--ca`, `--cert`, and `--key`. Not available with mbed TLS. If defined, it expects this file on the remote host in the specified location. If not defined, it expects a `server.p12` in `host_vars/{{ inventory_hostname }}/etc/openvpn/server/server.p12` and will copy it to the remote host. | unset |
| `openvpn_server__port`            | Which port the OpenVPN server should use.                                                               | `1194`            |
| `openvpn_server__pushs`           | A list of options that will be pushed to the connected clients. Can be used to set routes.              | `[]`              |
| `openvpn_server__raw` | Raw (user-defined) OpenVPN Config. Will be placed at the end of the `/etc/openvpn/server/server.conf` file. | unset |
| `openvpn_server__service_enabled` | Enables or disables the `openvpn-server@server` service, analogous to `systemctl enable/disable --now`. | `true`            |

Example:
```yaml
# optional
openvpn_server__client_configs:
  - name: 'user1@example.com'
    raw: |-
      ifconfig-push 192.0.2.250 255.255.255.0
    state: 'present'
openvpn_server__client_netmask: '255.255.255.0'
openvpn_server__port: 1194
openvpn_server__pushs:
  - 'route 192.0.2.0 255.255.255.0'
openvpn_server__raw: |-
  plugin /usr/lib64/openvpn/plugins/openvpn-plugin-auth-pam.so "openvpn login USERNAME password PASSWORD pin OTP"
openvpn_server__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
