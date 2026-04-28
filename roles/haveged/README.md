# Ansible Role linuxfabrik.lfops.haveged

This role installs [haveged](https://github.com/jirka-h/haveged), a userspace entropy daemon. It feeds the kernel's random pool from CPU timing jitter (the HAVEGE algorithm), which is mostly useful on headless VMs and older systems where `/dev/random` would otherwise block during early boot or under heavy crypto load. Modern Linux kernels (5.x+) usually have enough entropy from `getrandom()` plus virtio-rng, so `haveged` is more of a safety net than a hard requirement.


## Tags

`haveged`

* Installs haveged.
* Triggers: none.

`haveged:state`

* Manages the state of the systemd service.
* Triggers: none.


## Optional Role Variables

`haveged__service_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`haveged__service_state`

* Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options:

    * `started`
    * `stopped`
    * `restarted`
    * `reloaded`

* Type: String.
* Default: `'started'`

Example:
```yaml
# optional
haveged__service_enabled: true
haveged__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
