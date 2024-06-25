# Ansible Role linuxfabrik.lfops.maxmind_geoip

This role installs the shell script `/usr/local/sbin/update-maxmind` together with a systemd-timer. The shell script downloads the free GeoIP databases GeoLite2-ASN, GeoLite2-City and GeoLite2-Country in `mmdb`-format from [Maxmind](https://www.maxmind.com/) to `/usr/share/GeoIP/`. The script is scheduled weekly.

For Maxmind, depending on your needs, you normally run three playbooks in this particular order:

1. libmaxminddb
2. mod_maxminddb
3. maxmind_geoip (this role)


## Mandatory Requirements

You need a (free) Maxmind license key.


## Tags

| Tag                   | What it does                                 |
| ---                   | ------------                                 |
| `maxmind_geoip`       | Deploy `/usr/local/sbin/update-maxmind`      |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `maxmind_geoip__lic` | String. The license key from Maxmind. |

Example:
```yaml
# mandatory
maxmind_geoip__lic: '1a1c5e4202784cec'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
