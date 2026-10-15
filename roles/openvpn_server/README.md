# Ansible Role linuxfabrik.lfops.openvpn_server

This role installs and configures [OpenVPN](https://openvpn.net/) 2.7 as a server. Currently, the only supported configuration is a multi-client server. A corresponding client config will be generated to `/tmp/` on the ansible control node.

This role does not configure OpenVPN logging via `log-append /var/log/openvpn.log`. Instead it configures OpenVPN to use Journald, because there we get log entries including timestamps etc. To inspect the logs, use `journalctl --unit=openvpn-server@server --follow` for example.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* The role requires OpenVPN 2.7 or newer. It installs `openvpn >= 2.7`, which also upgrades an older OpenVPN, and aborts with a hint to [repo_openvpn](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_openvpn) if no repository offers it.
* The package is installed without weak dependencies. The OpenVPN 2.7 packages recommend `kmod-ovpn` for data channel offload, which pulls DKMS, a compiler and the kernel headers onto the server, while RHEL cannot use it: RHEL 10 ships a kernel older than 6.16, and on RHEL 8 and 9 the SELinux policy keeps OpenVPN from using the module. On RHEL 8 and 9 the role therefore switches data channel offload off (`disable-dco`), which also spares the SELinux denial OpenVPN would otherwise log at every start.
* An upgrade restarts `openvpn-server@server.service` from within the package, which drops every connected client. On RHEL 8 that restart still runs with the unit file of the old package. The role does not restart the service a second time in the run that upgrades OpenVPN, even if the configuration changed; it ends with a message to run `systemctl daemon-reload && systemctl restart openvpn-server@server.service` in a maintenance window.
* The TLS settings follow the OpenVPN 2.7 defaults, with two exceptions. Client certificates are checked against the OpenSSL security level 2 (`tls-cert-profile preferred`) instead of level 1, so certificates with RSA keys below 2048 bits or SHA-1 signatures are refused. And a client certificate must carry the TLS Web Client Authentication extended key usage (`remote-cert-tls client`). The data channel uses AES-256-GCM, AES-128-GCM or ChaCha20-Poly1305, whichever the client supports, and there are no Diffie-Hellman parameters to manage.
* A change to `/etc/openvpn/server/server.conf`, to the server certificate (`server.p12`) or to the Diffie-Hellman file restarts `openvpn-server@server.service`, because OpenVPN reads all three only at startup. The restart drops every connected client, which then reconnects on its own. Defer it with `lfops__skip_restart_handlers`, and note that the restart is skipped when the service was just started in the same run or when `openvpn_server__service_state` is `stopped`.
* A change to the certificate revocation list does **not** restart the service. OpenVPN reloads the file whenever it changed before each TLS negotiation, so a revoked certificate is refused from the next connection attempt onwards, without an outage for the other clients.
* A change to a client config (CCD) does **not** restart the service either. OpenVPN reads a client's file when that client connects, so the change applies the next time that client reconnects, while the other clients stay up.
* Configuration is fully templated. On every run `server.conf` and the CCD files are re-rendered from the role's templates (a timestamped backup is kept), so manual edits are overwritten. Manage all settings through the role variables below.
* On hosts where SELinux is enabled the role labels the configured port with `openvpn_port_t`. Where SELinux is disabled that step is skipped.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* The OpenVPN repository must be enabled (role: [linuxfabrik.lfops.repo_openvpn](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_openvpn)). It is the recommended source for OpenVPN 2.7 on RHEL 8 and 9, where EPEL ships outdated versions (2.4 and 2.5). On RHEL 10, EPEL ships 2.7 as well, but lags behind.
* The EPEL repository must be enabled (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)). OpenVPN needs `pkcs11-helper` from it on RHEL 8 and 10.
* Python 3 and the python3-policycoreutils module must be installed (required for the SELinux Ansible tasks) (role: [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils)).


## Requirements

Manual steps:

* The [kernel_modules](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_modules) role, which `setup_basic` runs, blocks the `tun` kernel module by default. OpenVPN needs it, so allow it in the inventory:
```yaml
kernel_modules__modules__host_var:
  - name: 'tun'
    enabled: true
```
* Issue client certificates with an RSA key of at least 2048 bits (or an EC key of at least 224 bits), a SHA-256 or stronger signature and the TLS Web Client Authentication extended key usage. The server refuses other certificates. RSA 2048 or ECDSA P-256 are enough; larger keys slow down every handshake without a security gain that matters here.
* Create a certificate for the OpenVPN server and save it on the ansible control node as `{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc/openvpn/server/server.p12`.
* Generate a certificate revocation list and save it on the ansible control node as `{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc/openvpn/server/crl.pem`.


## Tags

`openvpn_server`

* Installs and configures OpenVPN.
* Triggers: openvpn-server@server.service restart.

`openvpn_server:crl`

* Deploys the certificate revocation list.
* Triggers: none.

`openvpn_server:state`

* Manages the state of the OpenVPN service.
* Triggers: none.


## Mandatory Role Variables

`openvpn_server__client_network`

* The network in which the OpenVPN server should allocate client addresses, where `openvpn_server__client_netmask` will be used as the netmask.
* Type: String.

Example:

```yaml
# mandatory
openvpn_server__client_network: '192.0.2.0'
```


## Optional Role Variables

For details see `man openvpn`.

`openvpn_server__client_configs`

* List of dictionaries (client configs, "CCD"). Can be used to limit a client to a certain IP, which then can be used during firewalling.
* Subkeys:

    * `name`:

        * Mandatory. Name of the client's X509 common name.
        * Type: String.

    * `raw`:

        * Mandatory. Raw config for this client.
        * Type: String.

    * `state`:

        * Optional. If the config should be `present` or `absent`.
        * Type: String.
        * Default: `'present'`

* Type: List of dictionaries.
* Default: `[]`

`openvpn_server__client_netmask`

* The netmask that will be used with `openvpn_server__client_network` to allocate client addresses.
* Type: String.
* Default: `'255.255.255.0'`

`openvpn_server__crl_verify`

* Check peer certificate against a Certificate Revocation List.
* Type: String.
* Default: `'/etc/openvpn/server/crl.pem'`

`openvpn_server__crl_verify_skip_deploy`

* If false (the default), it expects the file `{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc{{ openvpn_server__crl_verify }}` on the Ansible control node and will copy that file to the remote host. If true, it expects this file to already exist on the remote host in the specified location.
* Type: Bool.
* Default: `false`

`openvpn_server__duplicate_cn`

* Allow several clients with the same certificate to be connected at the same time. Leave it off when every client has its own certificate: a copied certificate would otherwise go unnoticed, and the per-client settings in `openvpn_server__client_configs` (for example a fixed IP address) collide when two clients share a common name.
* Type: Bool.
* Default: `false`

`openvpn_server__pkcs12`

* Specify a PKCS #12 file containing local private key, local certificate, and root CA certificate. This option can be used instead of `--ca`, `--cert`, and `--key`. Not available with mbed TLS.
* Type: String.
* Default: `'/etc/openvpn/server/server.p12'`

`openvpn_server__pkcs12_skip_deploy`

* If false (the default), it expects the file `{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files{{ openvpn_server__pkcs12 }}` on the Ansible control node and will copy that file to the remote host. If true, it expects this file to already exist on the remote host in the specified location.
* Type: Bool.
* Default: `false`

`openvpn_server__port`

* TCP/UDP port number or port name for both local and remote (sets both `--lport` and `--rport` options to given port). The current default of 1194 represents the official IANA port number assignment for OpenVPN and has been used since version 2.0-beta17. Previous versions used port 5000 as the default.
* Type: Number.
* Default: `1194`

`openvpn_server__pushs`

* A list of options that will be pushed to the connected clients. Can be used to set routes.
* Type: List.
* Default: `[]`

`openvpn_server__raw`

* Raw (user-defined) OpenVPN Config. Will be placed at the end of the `/etc/openvpn/server/server.conf` file.
* Type: String.
* Default: unset

`openvpn_server__service_enabled`

* Enables or disables the `openvpn-server@server` service at boot, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`openvpn_server__service_state`

* Changes the state of the OpenVPN service, analogous to `systemctl start/stop/restart/reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `openvpn_server__service_enabled` is `true`, else `'stopped'`

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
openvpn_server__duplicate_cn: false
openvpn_server__pkcs12: '/etc/openvpn/server/server.p12'
openvpn_server__pkcs12_skip_deploy: false
openvpn_server__port: 1194
openvpn_server__pushs:
  - 'route 192.0.2.0 255.255.255.0'
openvpn_server__raw: |-
  plugin /usr/lib64/openvpn/plugins/openvpn-plugin-auth-pam.so "openvpn login USERNAME password PASSWORD pin OTP"
openvpn_server__service_enabled: true
openvpn_server__service_state: 'started'
```


## Troubleshooting

**`openvpn_server: The role requires OpenVPN 2.7 or newer, but dnf cannot install it`**

No enabled repository offers OpenVPN 2.7. Run the role through the `openvpn_server` playbook, which enables the OpenVPN repository with [repo_openvpn](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_openvpn), or run that playbook first if you set `openvpn_server__skip_repo_openvpn`.

**A client cannot connect, the server logs `VERIFY ERROR`, `ee key too small` or `ca md too weak`**

The client certificate does not meet OpenSSL security level 2, see "Requirements". Issue a new certificate with an RSA key of at least 2048 bits and a SHA-256 signature.

**A client cannot connect, the server logs `Certificate does not have extended key usage extension` or `--remote-cert-tls client` fails**

The client certificate lacks the TLS Web Client Authentication extended key usage, see "Requirements". Issue a new client certificate from a client template.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
