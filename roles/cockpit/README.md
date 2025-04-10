# Ansible Role linuxfabrik.lfops.cockpit

This role can either install or remove all cockpit packages from the system (for security reasons).


## Tags

| Tag       | What it does                         |
| ---       | ------------                         |
| `cockpit` | Installs or removes cockpit packages |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `cockpit__additional_packages` | List of strings. Additional cockpit packages to install, to extend the functionality of the web console | unset |
| `cockpit__socket_enabled` | Bool. Enables or disables the `cockpit.socket`, analogous to `systemctl enable/disable --now`. | `true` |
| `cockpit__state` | String. State of the cockpit packages. Possible Options: `'absent'`, `'present'`. | `'absent'` |

Example:
```yaml
# optional
cockpit__additional_packages:
- 'cockpit-machines' # for KVM administration
cockpit__socket_enabled: true
cockpit__state: 'present'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
