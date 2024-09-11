# Ansible Role linuxfabrik.lfops.bind

This role installs and configures [bind](https://www.isc.org/bind/) as a DNS server, either as a primary or secondary.

## Tags

| Tag              | What it does                                   |
| ---              | ------------                                   |
| `bind`           | Installs and configures bind                   |
| `bind:configure` | Manages the main named config and the zones    |
| `bind:state`     | Manages the state of the named systemd service |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `bind__trusted_networks` | List of networks from which DNS queries are allowed. |
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
| `bind__allow_new_zones` | Boolean. If `true`, then zones can be added at runtime via `rndc addzone`.  | `false` |
| `bind__allow_transfer` | List of strings. The global [`allow-transfer`](https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-allow-transfer) option. Can be overwritten per zone. | `['none']` |
| `bind__forwarders` | List of DNS servers to which DNS queries to unknown domain names should be forwarded. | `['1.0.0.1', '1.1.1.1']` |
| `bind__keys` | List of dictionaries. [`key`s](https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-key) for use with TSIG or the command channel (`rndc`). Subkeys: <ul><li>`name`: Mandatory, string. Name of the key.</li><li>`algorithm`: Mandatory, string. [`algorithm`](https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-algorithm) of the key.</li><li>`secret`: Mandatory, string. The key's [`secret`](https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-secret). Will be base64 encoded by the role.</li></ul> | `[]` |
| `bind__listen_on_addresses` | List of addresses on which the server will listen. This indirectly sets the listening interface(s). | `['any']` |
| `bind__named_conf_raw` | Multiline string. Raw content which will be appended to the end of `/etc/named.conf` | unset |
| `bind__named_service_enabled` | Boolean. Enables or disables the named service, analogous to `systemctl enable/disable --now`. Possible options: | `true` |
| `bind__recursion` | Boolean. Defines whether recursion and caching are allowed. Disabling recursion is recommended for authorative name servers. | `true` |
| `bind__rpz_zone` | String. Name of the RPZ zone. Setting this enables the usage of a reverse-policy zone (have a look at https://dnsrpz.info/, basically acts as a `/etc/hosts` file for all clients). To use this, also create a zone with `name: '{{ bind__rpz_zone }}'` in `bind__zones`. | unset |
| bind__listen_ipv6 | Boolean. Enables or disables listening on IPv6. | `false` |

Example:
```yaml
# optional
bind__allow_new_zones: true
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
  controls {
      inet * port 953 allow { 192.0.2.3; 127.0.0.1; } keys { "rndc-key-192.0.2.3"; };
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
