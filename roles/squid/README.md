# Ansible Role linuxfabrik.lfops.squid

This role installs and configures [squid](https://www.squid-cache.org/) as a caching proxy for the web.


## Tags

| Tag                 | What it does                                     | Reload / Restart |
| ------------------- | ------------------------------------------------ | ---------------- |
| `squid`             | Installs and configures squid                    | Restarts squid.service |
| `squid:configure`   | Manages the squid config                         | Restarts squid.service |
| `squid:state`       | Manages the state of the squid systemd service   | - |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `squid__conf_acl_localnet__host_var` / <br> `squid__conf_acl_localnet__group_var` | List of dictionaries containing hosts and subnets from where browsing should be allowed. Subkeys: <ul><li>`src`: String, mandatory. Host or subnet.</li><li>`state`: String, optional. State of the src entry. Either `present` or `absent`. Defaults to `present`</li></ul> | `['0.0.0.1-0.255.255.255', '10.0.0.0/8', '100.64.0.0/10', '169.254.0.0/16', '172.16.0.0/12', '192.168.0.0/16', 'fc00::/7', 'fe80::/10']`
| `squid__conf_acl_raw` | Multiline string. Raw content which will be appended next to the other ACLs at the top of the config. | unset |
| `squid__conf_acl_safe_ports__host_var` / <br> `squid__conf_acl_safe_ports__group_var` | List of dictionaries containing ports to which access is allowed. All other ports are blocked. Subkeys: <ul><li>`port`: String, mandatory. Port (or port range).</li><li>`state`: String, optional. State of the port entry. Either `present` or `absent`. Defaults to `present`</li></ul> | `['80', '21', '443', '70', '210', '1025-65535', '280', '488', '591', '777']` |
| `squid__conf_acl_ssl_ports__host_var` / <br> `squid__conf_acl_ssl_ports__group_var` | List of dictionaries containing ports to which the HTTP CONNECT method is allowed. Subkeys: <ul><li>`src`: String, mandatory. Host or subnet.</li><li>`state`: String, optional. State of the src entry. Either `present` or `absent`. Defaults to `present`</li></ul> | `['443']` |
| `squid__conf_coredump_dir` | String. Directory where Squid coredumps are stored. | `'/var/spool/squid'` |
| `squid__conf_http_access` | List of additional `http_access` rules. Will usually reference ACLs defined in `squid__conf_acl_raw`. | `[]` |
| `squid__conf_http_port` | List of socket addresses where Squid will listen for HTTP client requests. | `['3128']` |
| `squid__conf_raw` | Multiline string. Raw content which will be appended to the end of `/etc/squid/squid.conf`. | unset |
| `squid__conf_refresh_pattern` | List of refresh patterns. | `['^ftp: 1440 20% 10080', '-i (/cgi-bin/\|\?) 0 0% 0', '. 0 20% 4320']` |
| `squid__service_enabled` | Boolean. Enables or disables the squid service, analogous to `systemctl enable/disable --now`. | `true` |

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
