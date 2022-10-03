# Ansible Role linuxfabrik.lfops.qemu_guest_agent

This role installs the [QEMU Guest Agent](https://wiki.qemu.org/Features/GuestAgent/) for the generic and open source machine emulator and virtualizer.

Runs on

* RHEL 8 (and compatible)
* Ubuntu 16


## Tags

| Tag       | What it does                    |
| ---       | ------------                    |
| `qemu_guest_agent` | * Install qemu-guest-agent<br> * `systemctl enable/disable --now qemu-guest-agent.service` |
| `qemu_guest_agent:state`       | * `systemctl enable/disable --now qemu-guest-agent.service` |



## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `qemu_guest_agent__service_enabled` | Enables or disables the service, analogous to `systemctl enable/disable --now`. Possible options: `true`, `false`. | `true` |

Example:
```yaml
# optional
qemu_guest_agent__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
