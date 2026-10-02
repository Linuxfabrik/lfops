# Ansible Role linuxfabrik.lfops.chrony

This role installs and configures [chrony](https://chrony.tuxfamily.org/), a NTP daemon. This role configures Chrony

* to act like a client
* by specifying `chrony__allow` to act like a NTP-server providing time syncing to other clients


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* The configuration is fully templated: `/etc/chrony.conf` on the Red Hat family, `/etc/chrony/chrony.conf` on Debian and Ubuntu, each close to the file the distribution ships. Out-of-band edits are overwritten on the next run (a timestamped backup is kept).
* chronyd uses only the sources from `chrony__ntp_pools` and `chrony__ntp_servers`. If neither is set, the host has no time source. The distribution's default pools, time sources from DHCP and, on Debian and Ubuntu, `/etc/chrony/sources.d` are not used. Ubuntu 26.04 ships its default pools in `/etc/chrony/sources.d`, where chronyd would prefer them over every source from the inventory.
* On Debian and Ubuntu, drop-ins in `/etc/chrony/conf.d` are read at the beginning of the deployed `chrony.conf`, so the role's settings win over a drop-in that sets the same directive. Debian 13 and Ubuntu 26.04 read them at the end of their own `chrony.conf`, where a drop-in would win. Directives that add something instead of replacing it still take effect from a drop-in: a `pool`, `server` or `sourcedir` there adds time sources next to the ones from the inventory, and with the `prefer` option chronyd uses only those. Likewise, `allow` and `deny` add access rules.
* The deployed `chrony.conf` loads no key file, so NTP sources are not authenticated with symmetric keys. RHEL 10's own `chrony.conf` does the same, while RHEL 8 and 9, Debian and Ubuntu load a key file that holds no keys (`/etc/chrony.keys`, `/etc/chrony/chrony.keys`).


## Tags

`chrony`

* Installs and configures chrony.
* Triggers: chrony service restart (`chronyd.service` on the Red Hat family, `chrony.service` on Debian and Ubuntu).

`chrony:state`

* Manages the state of the chrony service.
* Triggers: none.


## Mandatory Role Variables

This role does not have any mandatory variables. However, either `chrony__ntp_pools` or `chrony__ntp_servers` has to be set, otherwise the host has no time source.


## Optional Role Variables

`chrony__allow`

* A list of subnets which are allowed to access the server as a NTP server. Setting this effectively turns this server into a NTP server.
* Type: List.
* Default: `[]`

`chrony__bindaddress`

* On which address chrony should listen. Can be used to restrict access to a certain address.
* Type: String.
* Default: unset

`chrony__binddevice`

* To which network interface chrony should bind. Can be used to restrict access to certain interfaces. Note that this does not work with enforcing SELinux. Try using `chrony__bindaddress`.
* Type: String.
* Default: unset

`chrony__ntp_pools`

* A list of NTP server pools. Same as `chrony__ntp_servers`, except that it is used to specify a pool of NTP servers rather than a single NTP server.
* Type: List.
* Default: `[]`

`chrony__ntp_servers`

* A list of NTP servers which should be used as a time source. The `iburst` option is always used, meaning chronyd will start with a burst of 4-8 requests in order to make the first update of the clock sooner.
* Type: List.
* Default: `[]`

`chrony__service_enabled`

* Enables or disables the chrony service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`chrony__service_state`

* Changes the state of the chrony service, analogous to `systemctl start/stop/restart/reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `chrony__service_enabled` is `true`, else `'stopped'`

Example:
```yaml
# optional
chrony__allow:
  - '192.0.2.0/24' # whole subnet
  - '198.51.100.8' # only this address
chrony__bindaddress: '192.0.2.1'
chrony__binddevice: 'eth0'
chrony__ntp_pools:
  - 'ch.pool.ntp.org'
chrony__ntp_servers:
  - '192.0.2.2'
chrony__service_enabled: true
chrony__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
