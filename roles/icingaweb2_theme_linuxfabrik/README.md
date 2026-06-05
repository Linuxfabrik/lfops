# Ansible Role linuxfabrik.lfops.icingaweb2_theme_linuxfabrik

This role installs and enables [Linuxfabrik's IcingaWeb2 Theme](https://github.com/Linuxfabrik/icingaweb2-theme-linuxfabrik).

The role does not have a dedicated playbook. It is normally pulled in via the [`setup_icinga2_master`](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_icinga2_master.yml) playbook and can be skipped there with `setup_icinga2_master__icingaweb2_theme_linuxfabrik__skip_role: true`.


*Available since LFOps `3.0.0`.*


## How the Role Behaves

* The Tarball for `icingaweb2_theme_linuxfabrik__version` is downloaded on the Ansible controller (`delegate_to: 'localhost'`), then copied to the target. The controller therefore needs Internet access to GitHub; the target does not.
* On every role run the directory `/usr/share/icingaweb2/modules/linuxfabrik` is overwritten with the contents of the configured version. To upgrade or downgrade the theme, change `icingaweb2_theme_linuxfabrik__version` and re-run the role.
* `icingacli module enable linuxfabrik` is only invoked when `/etc/icingaweb2/enabledModules/linuxfabrik` does not yet exist (idempotent). The theme has to be selected per user in IcingaWeb2 (or set as the default theme via the `theme` setting in `/etc/icingaweb2/config.ini`).


## Requirements

* The Ansible controller must have Internet access (downloads from `https://github.com/Linuxfabrik/icingaweb2-theme-linuxfabrik/archive/`).

Manual steps:

* Deploy a configured IcingaWeb2 by running the [icingaweb2](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/icingaweb2.yml) playbook (role: [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2)).


## Tags

`icingaweb2_theme_linuxfabrik`

* Installs and configures Linuxfabrik's IcingaWeb2 Theme.
* Triggers: none.


## Mandatory Role Variables

`icingaweb2_theme_linuxfabrik__version`

* The theme version to install. Possible options: https://github.com/Linuxfabrik/icingaweb2-theme-linuxfabrik/releases.
* Type: String.

Example:

```yaml
# mandatory
icingaweb2_theme_linuxfabrik__version: 'v1.1.0'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
