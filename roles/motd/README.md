# Ansible Role linuxfabrik.lfops.motd

This role ensures that login warning banners are configured properly (according to CIS).


## Tags

| Tag   | What it does | Reload / Restart |
| ---   | ------------ | ---------------- |
| `motd` | Installs login warning banners. | - |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `motd__logo_pty` | Logo for PTY consoles like SSH and other pseudo-terminals (multi-line) | [Have a look](https://github.com/Linuxfabrik/lfops/blob/main/roles/motd/defaults/main.yml) |
| `motd__logo_tty` | Logo for TTY console (multi-line). Backslashes have to be escaped properly. | [Have a look](https://github.com/Linuxfabrik/lfops/blob/main/roles/motd/defaults/main.yml) |
| `motd__legal_notice` | Legal notice (multi-line). CIS states that *Warning messages inform users who are attempting to login to the system of their legal status regarding the system and must include the name of the organization that owns the system and any monitoring policies that are in place.* | [Have a look](https://github.com/Linuxfabrik/lfops/blob/main/roles/motd/defaults/main.yml) |

Example:
```yaml
# optional
motd__logo_pty: |+
  powered by
  .____    .__                       _____      ___.         .__ __
  |    |   |__| ____  __ _____  ____/ ____\____ \_ |_________|__|  | __
  |    |   |  |/    \|  |  \  \/  /\   __\\__  \ | __ \_  __ \  |  |/ /
  |    |___|  |   |  \  |  />    <  |  |   / __ \| \_\ \  | \/  |    <
  |_______ \__|___|  /____//__/\_ \ |__|  (____  /___  /__|  |__|__|_ \
          \/       \/            \/            \/    \/              \/

motd__logo_tty: |+
  powered by
  .____    .__                       _____      ___.         .__ __
  |    |   |__| ____  __ _____  ____/ ____\\____ \\_ |_________|__|  | __
  |    |   |  |/    \\|  |  \\  \\/  /\\   __\\\\__  \\ | __ \\_  __ \\  |  |/ /
  |    |___|  |   |  \\  |  />    <  |  |   / __ \\| \\_\\ \\  | \\/  |    <
  |_______ \\__|___|  /____//__/\\_ \\ |__|  (____  /___  /__|  |__|__|_ \\
          \\/       \\/            \\/            \\/    \\/              \\/

motd__legal_notice: |+
  ************************************************************************
  *                                                                      *
  * This system is for the use of authorized users only. Individuals     *
  * using this computer system without authority or in excess of their   *
  * authority are subject to having all their activities on this system  *
  * monitored and recorded by system personnel. Anyone using this        *
  * system expressly consents to such monitoring and is advised that     *
  * if such monitoring reveals possible evidence of criminal activity    *
  * system personal may provide the evidence of such monitoring to law   *
  * enforcement officials.                                               *
  *                                                                      *
  ************************************************************************
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
