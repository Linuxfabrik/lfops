# Ansible Role linuxfabrik.lfops.chrony

This role installs and configures [chrony](https://chrony.tuxfamily.org/), a NTP daemon. This role configures Chrony

* to act like a client
* by specifying `chrony__allow` to act like a NTP-server providing time syncing to other clients


## Tags

`chrony`

* Installs and configures chrony.
* Triggers: chronyd.service restart.

`chrony:state`

* Manages the state of the chrony service.
* Triggers: none.


## Mandatory Role Variables

This role does not have any mandatory variables. However, either `chrony__ntp_pools` or `chrony__ntp_servers` should be set to enable time synchronisation.


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

* A list of NTP servers which should be used as a time source. The `ibust` option is always used, meaning chronyd will start with a burst of 4-8 requests in order to make the first update of the clock sooner.
* Type: List.
* Default: `[]`

`chrony__service_enabled`

* Enables or disables the chrony service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

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
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
