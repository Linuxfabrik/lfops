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

| Tag                    | What it does                             | Reload / Restart |
| ---                    | ------------                             | ---------------- |
| `openvpn_server`       | Installs and configures OpenVPN          | - |
| `openvpn_server:state` | Manages the state of the OpenVPN service | - |


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
| `openvpn_server__client_configs`  | List of Dictionaries (client configs, "CCD"). Can be used to limit a client to a certain IP, which then can be used during firewalling. Subkeys <ul><li>`name`: Mandatory, string. Name of hte client's X509 common name.</li><li>`raw`: Mandatory, string. Raw config for this client.</li><li>`state`: Optional, string. If the config should be `present` or `absent`. Defaults to `present`.</li></ul> | `[]`|
| `openvpn_server__client_netmask`  | String. The netmask that will be used with `openvpn_server__client_network` to allocate client addresses. | `'255.255.255.0'` |
| `openvpn_server__crl_verify`      | String. Check peer certificate against a Certificate Revocation List.                                   | `'/etc/openvpn/server/crl.pem'` |
| `openvpn_server__crl_verify_skip_deploy` | Boolean. If false (the default), it expects the file `{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc{{ openvpn_server__crl_verify }}` on the Ansible control node and will copy that file to the remote host. If true, it expects this file to already exist on the remote host in the specified location. | `false` |
| `openvpn_server__dh`              | String. File containing Diffie Hellman parameters in .pem format (required for `--tls-server` only). The file will be created automatically. | `'/etc/openvpn/dh2048.pem'` |
| `openvpn_server__dh_skip_deploy`  | Boolean. Skip the creation of the Diffie Hellman file.                                                  | `false` (file will be created) |
| `openvpn_server__pkcs12`          | String. Specify a PKCS #12 file containing local private key, local certificate, and root CA certificate. This option can be used instead of `--ca`, `--cert`, and `--key`. Not available with mbed TLS. |
| `openvpn_server__pkcs12_skip_deploy` | Boolean. If false (the default), it expects the file `{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files{{ openvpn_server__pkcs12 }}` on the Ansible control node and will copy that file to the remote host. If true, it expects this file to already exist on the remote host in the specified location. | `false` |
| `openvpn_server__port`            | Number. TCP/UDP port number or port name for both local and remote (sets both `--lport` and `--rport` options to given port). The current default of 1194 represents the official IANA port number assignment for OpenVPN and has been used since version 2.0-beta17. Previous versions used port 5000 as the default.  | `1194` |
| `openvpn_server__pushs`           | List. A list of options that will be pushed to the connected clients. Can be used to set routes.              | `[]`              |
| `openvpn_server__raw`             | Text. Raw (user-defined) OpenVPN Config. Will be placed at the end of the `/etc/openvpn/server/server.conf` file. | unset |
| `openvpn_server__service_enabled` | Boolean. Enables or disables the `openvpn-server@server` service, analogous to `systemctl enable/disable --now`. | `true`            |

Example:
```yaml
# optional
openvpn_server__client_configs:
  - name: 'user1@example.com'
    raw: |-
      ifconfig-push 192.0.2.250 255.255.255.0
    state: 'present'
openvpn_server__client_netmask: '255.255.255.0'
openvpn_server__crl_verify: '/etc/openvpn/server/crl.pem'
openvpn_server__crl_verify_skip_deploy: false
openvpn_server__dh: '/etc/openvpn/dh2048.pem'
openvpn_server__dh_skip_deploy: false
openvpn_server__pkcs12: '/etc/openvpn/server/server.p12'
openvpn_server__pkcs12_skip_deploy: false
openvpn_server__pkcs12: '/etc/openvpn/server/server.p12'  # file already exists on remote host
openvpn_server__port: 1194
openvpn_server__pushs:
  - 'route 192.0.2.0 255.255.255.0'
openvpn_server__raw: |-
  plugin /usr/lib64/openvpn/plugins/openvpn-plugin-auth-pam.so "openvpn login USERNAME password PASSWORD pin OTP"
openvpn_server__service_enabled: true
```


## Troubleshooting

```
TASK [linuxfabrik.lfops.openvpn_server : Generate DH Parameters with 2048 bits size]
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: SyntaxError: future feature annotations is not defined
fatal: [host1]: FAILED! => changed=false
  module_stderr: |-
    Traceback (most recent call last):
    ...
    SyntaxError: future feature annotations is not defined
```
This occurs when running against a host with Python <=3.6, which is not supported in community.crypto >=3.0.0 (see their [CHANGELOG](https://github.com/ansible-collections/community.crypto/blob/main/CHANGELOG.md#v300)).
As a workaround the collection can be downgraded: `ansible-galaxy collection install --force 'community.crypto:<3.0.0'`


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
