# Ansible Role linuxfabrik.lfops.dnf_makecache

This role manages the `dnf-makecache.service` and `dnf-makecache.timer` units. By default both are disabled and stopped, which is what most servers want — DNF caches are refreshed on demand and the periodic refresh is rarely needed.

This role is Red Hat-family only (DNF / YUM). It does not run on Debian / Ubuntu.


*Available since LFOps `2.0.0`.*


## Tags

`dnf_makecache`

* Manages the dnf-makecache service and timer.
* Triggers: none.


## Optional Role Variables

`dnf_makecache__service_enabled`

* Whether `dnf-makecache.service` is enabled at boot, analogous to `systemctl enable / disable`.
* Type: Bool.
* Default: `false`

`dnf_makecache__service_state`

* State of `dnf-makecache.service`, analogous to `systemctl start / stop / restart / reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `dnf_makecache__service_enabled` is `true`, otherwise `'stopped'`.

`dnf_makecache__timer_enabled`

* Whether `dnf-makecache.timer` is enabled at boot.
* Type: Bool.
* Default: `false`

`dnf_makecache__timer_state`

* State of `dnf-makecache.timer`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `dnf_makecache__timer_enabled` is `true`, otherwise `'stopped'`.

Example:
```yaml
# optional
dnf_makecache__service_enabled: false
dnf_makecache__timer_enabled: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
