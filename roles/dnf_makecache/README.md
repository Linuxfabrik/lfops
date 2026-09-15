# Ansible Role linuxfabrik.lfops.dnf_makecache

This role manages `dnf-makecache.timer`, which periodically refreshes the DNF metadata cache. By default the timer is disabled and stopped, which is what most servers want: DNF refreshes its caches on demand, and the periodic refresh is rarely needed.

This role is Red Hat-family only (DNF / YUM). It does not run on Debian / Ubuntu.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* The role does not manage `dnf-makecache.service`. The service cannot be enabled at boot: it has no `[Install]` section (`systemctl is-enabled` reports `static`), runs `dnf makecache` once and only when `dnf-makecache.timer` triggers it. Disabling the timer therefore also stops the periodic refresh.


## Tags

`dnf_makecache`

* Manages the dnf-makecache timer.
* Triggers: none.


## Optional Role Variables

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
dnf_makecache__timer_enabled: false
dnf_makecache__timer_state: 'stopped'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
