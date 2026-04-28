# Ansible Role linuxfabrik.lfops.unattended_upgrades

This role deactivates Unattended Upgrades on Debian-based systems by setting both `APT::Periodic::Update-Package-Lists` and `APT::Periodic::Unattended-Upgrade` to `0` in `/etc/apt/apt.conf.d/20auto-upgrades`. The `unattended-upgrades` package itself is left installed.

This role only supports Debian and Ubuntu. Running it against a Red Hat-family host fails because the target file does not exist there.


## Tags

`unattended_upgrades`

* Deactivates Unattended Upgrades.
* Triggers: none.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
