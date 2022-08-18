# Ansible Role linuxfabrik.lfops.bind

This role installs and configures [bind](https://www.isc.org/bind/) as a DNS server. Currently, it only supports standalone configurations, no primary-replica configuration.

Tested on

* RHEL 8 (and compatible)


## Tags

| Tag    | What it does                 |
| ---    | ------------                 |
| `bind` | Installs and configures bind |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `bind__trusted_networks` | List of networks from which DNS queries are allowed. |
| `bind__zones` | List of dictionaries defining the zone files with the DNS records. Subkeys:<br> * `name`: Mandatory, string. The name of the zone. Suffix with `in-addr.arpa` for reverse zones.<br> * `file`: Mandatory, string. The filename for the zone file under `/var/named/`.<br> * `raw`: Mandatory, string. The raw content of the zone file. |

Example:
```yaml
# mandatory
bind__trusted_networks:
  - '192.0.2.0/24'
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

      @ IN SOA dns-server.example.com. root@example.com. (
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
| `bind__forwarders` | List of DNS servers to which DNS queries to unknown domain names should be forwarded. | `['1.0.0.1', '1.1.1.1']` |
| `bind__listen_on_addresses` | List of addresses on which the server will listen. This indirectly sets the listening interface(s). | `['any']` |
| `bind__named_service_enabled` | Enables or disables the named service, analogous to `systemctl enable/disable --now`. Possible options: | `true` |

Example:
```yaml
# optional
bind__forwarders:
  - '1.0.0.1'
  - '1.1.1.1'
bind__listen_on_addresses:
  - '192.0.2.2/32'
bind__named_service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
