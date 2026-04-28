# Ansible Role linuxfabrik.lfops.icingaweb2_module_company

This role installs and enables the [IcingaWeb2 Company Module](https://github.com/Icinga/icingaweb2-theme-company), a starting point that ships placeholder logos and CSS overrides intended to be customized in place.

This role is tested with the following IcingaWeb2 Company Module versions:

* 1.0.0


## How the Role Behaves

* The version is hard-coded to `v1.0.0` in `tasks/main.yml`. No version variable is exposed.
* The Tarball is downloaded on the Ansible controller (`delegate_to: 'localhost'`, `run_once: true`), then copied to the target. The controller therefore needs Internet access to GitHub; the target does not.
* The download and extraction step only run on the *first* role execution (when `mkdir /usr/share/icingaweb2/modules/company` reports `changed`). On subsequent runs the role does not overwrite the directory, so any local customizations to logos or CSS are preserved.
* `icingacli module enable company` is only invoked when `/etc/icingaweb2/enabledModules/company` does not yet exist (idempotent).


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.
* Internet access from the Ansible controller (downloads `https://github.com/Icinga/icingaweb2-theme-company/archive/v1.0.0.tar.gz`).


## Tags

`icingaweb2_module_company`

* Installs and configures the IcingaWeb2 Company Module.
* Triggers: none.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
