# Ansible Role linuxfabrik.lfops.bind

This role installs and configures [bind](https://www.isc.org/bind/) as a DNS server. Currently, it only supports standalone configurations, no primary-replica configuration.

If you define a zone with `name`, `file` and `raw`, the role 

* creates the zone file in `/var/named/{{ item.file }}`
* creates the corresponding entry in `/etc/named.conf` like so:

    zone "{{ item.name }}" IN {
        type master;
        file "{{ item.file }}";
        # do normal iterative resolution (do not forward)
        forwarders { };
        allow-query { trusted; };
        allow-transfer { none; };
        allow-update { none; };
    };


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
| `bind__forwarders` | List of DNS servers to which DNS queries to unknown domain names should be forwarded. | `['1.0.0.1', '1.1.1.1']` |
| `bind__listen_on_addresses` | List of addresses on which the server will listen. This indirectly sets the listening interface(s). | `['any']` |
| `bind__named_conf_raw` | Optional, string. Raw content which will be appended to the end of `/etc/named.conf` | unset |
| `bind__named_service_enabled` | Enables or disables the named service, analogous to `systemctl enable/disable --now`. Possible options: | `true` |
| `bind__rpz_zone` | This enables the usage of a reverse-policy zone (have a look at https://dnsrpz.info/, basically acts as a `/etc/hosts` file for all clients). To use this, also create a zone with `name: '{{ bind__rpz_zone }}'` in `bind__zones`. | unset |

Example:
```yaml
# optional
bind__forwarders:
  - '1.0.0.1'
  - '1.1.1.1'
bind__listen_on_addresses:
  - '192.0.2.2/32'
bind__named_conf_raw: |-
  zone "example.com" {
      type forward;
      forwarders { my-dns.loc; };
  };
bind__named_service_enabled: true
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
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
