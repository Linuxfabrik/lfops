# Ansible Role linuxfabrik.lfops.at

This role installs at, a daemon that allows commands to be run at a specified time.


*Available since LFOps `2.0.0`.*


## Tags

`at`

* Installs and configures at/atd.
* Triggers: none.

`at:state`

* Manages the state of `atd.service` (enable/disable at boot, plus start/stop/restart/reload).
* Triggers: none.


## Optional Role Variables

`at__service_enabled`

* Whether `atd.service` is enabled at boot, analogous to `systemctl enable / disable`.
* Type: Bool.
* Default: `true`

`at__service_state`

* State of `atd.service`, analogous to `systemctl start / stop / restart / reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `at__service_enabled` is `true`, otherwise `'stopped'`.

Example:
```yaml
# optional
at__service_enabled: true
at__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
