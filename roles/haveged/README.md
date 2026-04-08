# Ansible Role linuxfabrik.lfops.haveged

This role installs [haveged](https://github.com/jirka-h/haveged).


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
