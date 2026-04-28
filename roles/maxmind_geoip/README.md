# Ansible Role linuxfabrik.lfops.maxmind_geoip

This role installs the shell script `/usr/local/sbin/update-maxmind` together with a systemd timer. The shell script downloads the free GeoIP databases GeoLite2-ASN, GeoLite2-City and GeoLite2-Country in `mmdb`-format from [Maxmind](https://www.maxmind.com/) to `/usr/share/GeoIP/`. The script is scheduled weekly.

For Maxmind, depending on your needs, you normally run three playbooks in this particular order:

1. libmaxminddb
2. mod_maxminddb
3. maxmind_geoip (this role)


## How the Role Behaves

* The role itself only deploys the update script. The companion `linuxfabrik.lfops.systemd_unit` role (called by the playbook) creates the `update-maxmind.service` (oneshot) and `update-maxmind.timer` (`OnCalendar=weekly`). The service is *not* enabled directly; the timer is what fires it.
* The first GeoIP database refresh therefore happens at the next weekly timer trigger. To populate the databases immediately after the first run, trigger the service manually: `systemctl start update-maxmind.service`.
* The Maxmind license key is rendered into `/usr/local/sbin/update-maxmind` in cleartext (mode `0755`, owned by `root:root`).
* Outbound HTTPS access from the target host to `download.maxmind.com` is required for the script to work.


## Mandatory Requirements

* A free Maxmind license key.
* Outbound HTTPS access from each target host to `download.maxmind.com`.


## Tags

`maxmind_geoip`

* Deploys `/usr/local/sbin/update-maxmind`.
* Triggers: none.


## Mandatory Role Variables

`maxmind_geoip__lic`

* The license key from Maxmind.
* Type: String.

Example:
```yaml
# mandatory
maxmind_geoip__lic: '1a1c5e4202784cec'
```


## Optional Role Variables

`maxmind_geoip__skip_systemd_unit`

* If `true`, the playbook skips the `linuxfabrik.lfops.systemd_unit` role and therefore does not create the `update-maxmind` service / timer. Use this when you want to manage the schedule yourself (e.g. via cron).
* Type: Bool.
* Default: `false`

Example:
```yaml
# optional
maxmind_geoip__skip_systemd_unit: true
```


## Advanced: Changing the Schedule

The default `OnCalendar=weekly` schedule is set via `maxmind_geoip__systemd_unit__timers__dependent_var` in `defaults/main.yml`. To change it, override the whole list in your inventory:

```yaml
maxmind_geoip__systemd_unit__timers__dependent_var:
  - name: 'update-maxmind'
    raw_timer: |-
      OnCalendar=*-*-* 03:00:00
      RandomizedDelaySec=1h
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
