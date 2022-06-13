# Ansible Role openvpn_server

This role installs and configures [OpenVPN](https://openvpn.net/) as a server. Currently, the only supported configuration is a multi-client server. A corresponding client config will be generated to `/tmp/` on the ansible control node.

FQCN: linuxfabrik.lfops.openvpn_server

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* Create a certificate for the OpenVPN server and save it on the ansible control node as `{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc/openvpn/server/server.p12`.
* Generate a certificate revocation list and save it on the ansible control node as `{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/etc/openvpn/server/crl.pem`.
* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Install Python 3, and the python3-policycoreutils module (required for the SELinux Ansible tasks).


### Optional

This role does not have any optional requirements.


## Tags

| Tag                  | What it does                             |
| ---                  | ------------                             |
| openvpn_server       | Installs and configures OpenVPN          |
| openvpn_server:state | Manages the state of the OpenVPN service |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/openvpn_server/defaults/main.yml) for the variable defaults.


### Mandatory

#### openvpn_server__client_network

The network in which the OpenVPN server should allocate client addresses, where `openvpn_server__client_netmask` will be used as the netmask.

Example:
```bash
openvpn_server__client_network: '192.0.2.0'
```


### Optional

#### openvpn_server__client_netmask

The netmask that will be used with `openvpn_server__client_network` to allocate client addresses.

Default:
```yaml
openvpn_server__client_netmask: '255.255.255.0'
```


#### openvpn_server__port

Which port the OpenVPN server should use.

Default:
```yaml
openvpn_server__port: 1194
```


#### openvpn_server__pushs

A list of options that will be pushed to the connected clients. Can be used to set routes.

Default:
```yaml
openvpn_server__pushs: []
```

Example:
```yaml
openvpn_server__pushs:
  - 'route 192.0.2.0 255.255.255.0'
```


#### openvpn_server__service_enabled

Enables or disables the `openvpn-server@server` service, analogous to `systemctl enable/disable --now`. Possible options:

* true
* false

Default:
```yaml
openvpn_server__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
