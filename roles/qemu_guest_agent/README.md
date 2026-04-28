# Ansible Role linuxfabrik.lfops.qemu_guest_agent

This role installs the [QEMU Guest Agent](https://wiki.qemu.org/Features/GuestAgent/) for the generic and open source machine emulator and virtualizer.


## Tags

`qemu_guest_agent`

* Installs `qemu-guest-agent` and manages `qemu-guest-agent.service`.
* Triggers: none.

`qemu_guest_agent:state`

* Manages the state of `qemu-guest-agent.service` (enable/disable at boot, plus start/stop/restart/reload).
* Triggers: none.


## Optional Role Variables

`qemu_guest_agent__service_enabled`

* Whether `qemu-guest-agent.service` is enabled at boot, analogous to `systemctl enable / disable`.
* Type: Bool.
* Default: `true`

`qemu_guest_agent__service_state`

* State of `qemu-guest-agent.service`, analogous to `systemctl start / stop / restart / reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `qemu_guest_agent__service_enabled` is `true`, otherwise `'stopped'`.

Example:
```yaml
# optional
qemu_guest_agent__service_enabled: true
qemu_guest_agent__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
