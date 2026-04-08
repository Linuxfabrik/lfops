# Ansible Role linuxfabrik.lfops.qemu_guest_agent

This role installs the [QEMU Guest Agent](https://wiki.qemu.org/Features/GuestAgent/) for the generic and open source machine emulator and virtualizer.


## Tags

`qemu_guest_agent`

* Install qemu-guest-agent.
* `systemctl enable/disable --now qemu-guest-agent.service`.
* Triggers: none.

`qemu_guest_agent:state`

* `systemctl enable/disable --now qemu-guest-agent.service`.
* Triggers: none.


## Optional Role Variables

`qemu_guest_agent__service_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable --now`. Possible options: `true`, `false`.
* Type: Bool.
* Default: `true`

Example:

```yaml
# optional
qemu_guest_agent__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
