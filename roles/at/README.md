# Ansible Role linuxfabrik.lfops.at

This role installs at, a daemon that allows commands to be run at a specified time.

Tested on

* RHEL 8 (and compatible)
* Fedora Server 35


## Tags

| Tag        | What it does                          |
| ---        | ------------                          |
| `at`       | Installs and configures at/atd        |
| `at:state` | Controls the state of the atd service |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `at__service_enabled` | Enables or disables the atd service, analogous to `systemctl enable/disable --now`. | `true` |

Example:
```yaml
# optional
at__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
