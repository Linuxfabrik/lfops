# Ansible Role linuxfabrik.lfops.dnf_makecache

This role ensures that the DNF-makecache Systemd service and timer are disabled.


## Tags

`dnf_makecache`

* Manages the dnf-makecache service and timer.
* Triggers: none.


## Optional Role Variables

`dnf_makecache__service_enabled`

* Enables or disables the DNF-makecache service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `false`

`dnf_makecache__timer_enabled`

* Enables or disables the DNF-makecache timer, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `false`

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
