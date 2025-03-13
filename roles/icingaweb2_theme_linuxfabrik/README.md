# Ansible Role linuxfabrik.lfops.icingaweb2_theme_linuxfabrik

This role installs and enables [Linuxfabrik's IcingaWeb2 Theme](https://github.com/Linuxfabrik/icingaweb2-theme-linuxfabrik).

## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.


## Tags

| Tag                            | What it does                                           |
| ---                            | ------------                                           |
| `icingaweb2_theme_linuxfabrik` | Installs and configures Linuxfabrik's IcingaWeb2 Theme |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `icingaweb2_theme_linuxfabrik__version` | The module version to install. Possible options: https://github.com/Linuxfabrik/icingaweb2-theme-linuxfabrik/releases |

Example:
```yaml
# mandatory
icingaweb2_theme_linuxfabrik__version: 'v1.1.0'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
