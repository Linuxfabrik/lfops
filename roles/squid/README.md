# Ansible Role linuxfabrik.lfops.squid

This role installs and configures [squid](https://www.squid-cache.org/) as a caching proxy for the web.


## Tags

`squid`

* Installs and configures squid.
* Triggers: squid.service restart (after `squid -k parse`).

`squid:configure`

* Manages the squid config.
* Triggers: squid.service restart (after `squid -k parse`).

`squid:state`

* Manages the state of the squid systemd service.
* Triggers: none.


## Optional Role Variables

`squid__conf_acl_localnet__host_var` / `squid__conf_acl_localnet__group_var`

* List of dictionaries containing hosts and subnets from where browsing should be allowed.
* Type: List of dictionaries.
* Default: `['0.0.0.1-0.255.255.255', '10.0.0.0/8', '100.64.0.0/10', '169.254.0.0/16', '172.16.0.0/12', '192.168.0.0/16', 'fc00::/7', 'fe80::/10']`
* Subkeys:

    * `src`:

        * Mandatory. Host or subnet.
        * Type: String.

    * `state`:

        * Optional. State of the src entry. Either `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`squid__conf_acl_raw`

* Raw content which will be appended next to the other ACLs at the top of the config.
* Type: String.
* Default: unset

`squid__conf_acl_safe_ports__host_var` / `squid__conf_acl_safe_ports__group_var`

* List of dictionaries containing ports to which access is allowed. All other ports are blocked.
* Type: List of dictionaries.
* Default: `['80', '21', '443', '70', '210', '1025-65535', '280', '488', '591', '777']`
* Subkeys:

    * `port`:

        * Mandatory. Port (or port range).
        * Type: String.

    * `state`:

        * Optional. State of the port entry. Either `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`squid__conf_acl_ssl_ports__host_var` / `squid__conf_acl_ssl_ports__group_var`

* List of dictionaries containing ports to which the HTTP CONNECT method is allowed.
* Type: List of dictionaries.
* Default: `['443']`
* Subkeys:

    * `port`:

        * Mandatory. Port.
        * Type: String.

    * `state`:

        * Optional. State of the port entry. Either `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`squid__conf_coredump_dir`

* Directory where Squid coredumps are stored.
* Type: String.
* Default: `'/var/spool/squid'`

`squid__conf_http_access`

* List of additional `http_access` rules. Will usually reference ACLs defined in `squid__conf_acl_raw`.
* Type: List.
* Default: `[]`

`squid__conf_http_port`

* List of socket addresses where Squid will listen for HTTP client requests.
* Type: List.
* Default: `['3128']`

`squid__conf_raw`

* Raw content which will be appended to the end of `/etc/squid/squid.conf`.
* Type: String.
* Default: unset

`squid__conf_refresh_pattern`

* List of refresh patterns.
* Type: List.
* Default: `['^ftp:    1440  20% 10080', '-i (/cgi-bin/|\?) 0  0%  0', '.    0 20% 4320']`

`squid__service_enabled`

* Enables or disables the squid service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

Example:
```yaml
# optional
squid__conf_acl_localnet__group_var: []
squid__conf_acl_localnet__host_var:
  - src: '192.0.2.0/24'
    state: 'present'
squid__conf_acl_raw: |-
  acl QUERY urlpath_regex cgi-bin \?
  acl block_port port 8905
squid__conf_acl_safe_ports__group_var: []
squid__conf_acl_safe_ports__host_var:
  - port: '563'
    state: 'present'
squid__conf_acl_ssl_ports__group_var: []
squid__conf_acl_ssl_ports__host_var:
  - port: '563'
    state: 'present'
squid__conf_coredump_dir: '/var/spool/squid'
squid__conf_http_access:
  - 'deny test'
  - 'deny block'
squid__conf_http_port:
  - '3128'
squid__conf_raw: |-
  access_log /var/log/squid/access.log
  icp_access deny lf_banned
  icp_access allow all
  cache deny QUERY
squid__conf_refresh_pattern:
  - '^ftp:    1440  20% 10080'
  - '-i (/cgi-bin/|\?) 0  0%  0'
  - '.    0 20% 4320'
squid__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
