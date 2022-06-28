# Ansible Role chrony

This role installs and configures [chrony](https://chrony.tuxfamily.org/), a NTP daemon. It can either be configured as a client, or as a server, providing time syncing to other clients.

FQCN: linuxfabrik.lfops.chrony

Tested on

* RHEL 8 (and compatible)


## Requirements

This role does not have any requirements.


## Tags

| Tag          | What it does                            |
| ---          | ------------                            |
| chrony       | Installs and configures chrony          |
| chrony:state | Manages the state of the chrony service |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/chrony/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables. However, either `chrony__ntp_pools` or `chrony__ntp_servers` should be set to enable time synchronisation.


### Optional

#### chrony__ntp_servers

A list of NTP servers which should be used as a time source. The `ibust` option is always used, meaning chronyd will start with a burst of 4-8 requests in order to make the first update of the clock sooner.

Default:
```yaml
chrony__ntp_servers: []
```


#### chrony__ntp_pools

A list of NTP server pools. Same as `chrony__ntp_servers`, except that it is used to specify a pool of NTP servers rather than a single NTP server.

Default:
```yaml
chrony__ntp_pools: []
```


#### chrony__allow

A list of subnets which are allowed to access the server as a NTP server. Setting this effectively turns this server into a NTP server.

Default:
```yaml
chrony__allow: []
```

Example:
```yaml
chrony__allow:
  - '198.51.100.8' # only this address
  - '192.0.2.0/24' # whole subnet
```


#### chrony__bindaddress

On which address chrony should listen. Can be used to restrict access to a certain address.

Default: unset

Example:
```yaml
chrony__bindaddress: '192.0.2.1'
```


#### chrony__binddevice

To which network interface chrony should bind. Can be used to restrict access to certain interfaces. Note that this does not work with enforcing SELinux. Try using `chrony__bindaddress`.

Default: unset

Example:
```yaml
chrony__binddevice: 'eth0'
```


#### chrony__service_enabled

Enables or disables the chrony service, analogous to `systemctl enable/disable --now`. Possible options:

* true
* false

Default:
```yaml
chrony__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
