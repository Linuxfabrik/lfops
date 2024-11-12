# Ansible Role linuxfabrik.lfops.bind

This role installs and configures [bind](https://www.isc.org/bind/) as a DNS server, either as a primary or secondary.

## Tags

| Tag               | What it does                                   |
|-------------------|------------------------------------------------|
| `squid`           | Installs and configures squid                  |
| `squid:configure` | Manages the main squid config                  |
| `squid:state`     | Manages the state of the squid systemd service |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `bind__trusted_networks` | List of networks from which DNS queries are allowed. Results in the `trusted` ACL in the config. |
| `bind__zones` | List of dictionaries defining the zone files with the DNS records. Subkeys:<ul><li>`name`: Mandatory, string. The name of the zone. Suffix with `in-addr.arpa` (IPv4) / `ip6.arpa` (IPv6) for reverse zones.</li><li>`file`: Optional, string. The filename for the zone file under `/var/named/`. Defaults to `name` with `.zone` suffix.</li><li>`type`: Optional, string. [type](https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-type) of the zone. Defaults to `master`.</li><li>`forwarders`: Optional, list of strings. [forwarders](https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-forwarders) of the zone. Defaults to `[]`, as this is generally not useful for `type: 'master'`.</li><li>`allow_transfer`: Optional, list of strings. [allow-transfer](https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-allow-transfer) of the zone to a secondary. Defaults to `[]`.</li><li>`masters`: Optional, list of strings. [masters](https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-primaries) of from which to fetch the zone. Defaults to `[]`.</li><li>`raw`: Optional, multiline string. The raw content of the zone file.</li></ul> |

Example:
```yaml
# mandatory
bind__trusted_networks:
  - 'any'
bind__zones:
  - name: 'example.com'
    file: 'forward.zone'
    raw: |-
      $TTL 1H

      @ IN SOA dns-server.example.com. root@example.com. (
          2022042501 ; <SERNO>
          1H         ; <TIME-TO-REFRESH>
          1H         ; <TIME-TO-RETRY>
          1W         ; <TIME-TO-EXPIRE>
          1D )       ; <minimum-TTL>

      @ IN NS dns-server.example.com.
      _ldap._tcp    IN     SRV     10 10 389 dns-server.example.com.

      dns-server        IN A    192.0.2.2
  - name: '2.0.192.in-addr.arpa'
    file: 'reverse.zone'
    raw: |-
      $TTL 1H

      @ IN SOA dns-server.example.com. info@example.com. (
          2022042501 ; <SERNO>
          1H         ; <TIME-TO-REFRESH>
          1H         ; <TIME-TO-RETRY>
          1W         ; <TIME-TO-EXPIRE>
          1D )       ; <minimum-TTL>

      @ IN NS dns-server.example.com.

      2    IN PTR dns-server.example.com.
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `squid__conf_acl_localnet` | | `['0.0.0.1-0.255.255.255', '10.0.0.0/8', '100.64.0.0/10', '169.254.0.0/16', '172.16.0.0/12', '192.168.0.0/16', 'fc00::/7', 'fe80::/10']`
| `squid__conf_acl_SSL_ports` | | `['443']` |
| `squid__conf_acl_Safe_ports` | | `['80', '21', '443', '70', '210', '1025-65535', '280', '488', '591', '777']` |
| `squid__conf_acl_raw` | | unset |
| `squid__conf_coredump_dir` | String. Directory where Squid should leave coredumps. | `'/var/spool/squid'` |
| `squid__conf_http_access` | List of additional access control list rules. | `[]` |
| `squid__conf_http_port` | List of socket addresses where Squid will listen for HTTP client requests. | `['3128']` |
| `squid__conf_raw` | Multiline string. Raw content which will be appended to the end of `/etc/squid/squid.conf`. | unset |
| `squid__conf_refresh_pattern` | List of refresh patterns. | `['^ftp: 1440 20% 10080', '-i (/cgi-bin/\|\?) 0 0% 0', '. 0 20% 4320']` |
| `squid__service_enabled` | Boolean. Enables or disables the squid service, analogous to `systemctl enable/disable --now`. | `true` |

Example:
```yaml
# optional
bind__allow_new_zones: true
bind__allow_query_cache:
  - 'none'
bind__allow_recursion:
  - 'none'
bind__allow_transfer:
  - '192.0.2.0/24'
bind__forwarders:
  - '1.0.0.1'
  - '1.1.1.1'
bind__keys:
  - name: 'rndc-key-192.0.2.3'
    algorithm: 'hmac-sha256'
    secret: 'linuxfabrik'
bind__listen_on_addresses:
  - '192.0.2.2/32'
bind__named_conf_raw: |-
  include "/etc/rndc.key";
  controls {
      inet * port 953 allow { localhost; 192.0.2.3; 127.0.0.1; } keys { "rndc-key"; "rndc-key-192.0.2.3"; };
  };
bind__named_service_enabled: true
bind__recursion: false
bind__rpz_zone: 'rpz'
bind__zones:
  # make use of the bind__rpz_zone
  - name: '{{ bind__rpz_zone }}'
    file: '{{ bind__rpz_zone }}.zone'
    raw: |-
      $TTL 1H

      @ IN SOA 001-p-infra01.example.com. info@example.com. (
          2022101801 ; <SERNO>
          1H         ; <TIME-TO-REFRESH>
          1H         ; <TIME-TO-RETRY>
          1W         ; <TIME-TO-EXPIRE>
          1D )       ; <minimum-TTL>

      @ IN NS 001-p-infra01.example.com.

      internal-website.example.com     A     192.0.2.3
bind__listen_ipv6: true
```


## Primary-Secondary Example

With this configuration the primary actively notifies the secondary for any zone changes (i.e. changes to the serial).
The secondary actively checks the serial for changes every 1 hour (`TIME-TO-REFRESH`).
The secondary caches the zone file locally, and uses the cached version during startup.

Note: BIND 9.11 (RHEL8) does not yet support `primary` and `secondary`, use `master` and `slave` instead.

Primary:
```yaml
# either set `bind__allow_transfer` for all zones, or the `allow_transfer` subkey per zone to allow access
bind__allow_transfer:
  - '192.0.2.0/24'
bind__zones:
  - name: 'example.com'
    file: 'forward.zone'
    type: 'master'
    raw: |-
      $TTL 1H

      @ IN SOA primary.example.com. root@example.com. (
          2024082801 ; <SERNO>
          1H         ; <TIME-TO-REFRESH>
          1H         ; <TIME-TO-RETRY>
          1W         ; <TIME-TO-EXPIRE>
          1D )       ; <minimum-TTL>

      @ IN NS primary.example.com.
      @ IN NS secondary.example.com.

      primary        IN A    192.0.2.2
      secondary      IN A    192.0.2.3

  - name: '2.0.192.in-addr.arpa'
    file: 'reverse.zone'
    type: 'master'
    # more specific than `bind__allow_transfer`, takes priority
    allow_transfer:
      - '192.0.2.3/32'
    raw: |-
      $TTL 1H

      @ IN SOA primary.example.com. root@example.com. (
          2024082801 ; <SERNO>
          1H         ; <TIME-TO-REFRESH>
          1H         ; <TIME-TO-RETRY>
          1W         ; <TIME-TO-EXPIRE>
          1D )       ; <minimum-TTL>

      @ IN NS primary.example.com.
      @ IN NS secondary.example.com.

      2   IN PTR primary.example.com.
      3   IN PTR secondary.example.com.
```

Secondary:
```yaml
bind__zones:
  - name: 'example.com'
    file: 'forward.zone'
    type: 'master'
    masters:
      - '192.0.2.2'

  - name: '2.0.192.in-addr.arpa'
    file: 'reverse.zone'
    type: 'slave'
    masters:
      - '192.0.2.2'
```



## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
