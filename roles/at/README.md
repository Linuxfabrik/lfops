# Ansible Role linuxfabrik.lfops.at

This role installs at, a daemon that allows commands to be run at a specified time.


## Tags

`at`

* Installs and configures at/atd.
* Triggers: none.

`at:state`

* Controls the state of the atd service.
* Triggers: none.


## Optional Role Variables

`at__service_enabled`

* Enables or disables the atd service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

Example:
```yaml
# optional
at__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
