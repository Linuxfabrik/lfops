# Ansible Role linuxfabrik.lfops.icingaweb2_module_incubator

This role installs and enables the [IcingaWeb2 Incubator Module](https://github.com/Icinga/icingaweb2-module-incubator), a shared library required by several other IcingaWeb2 modules.

This role is tested with the following IcingaWeb2 Incubator Module versions:

* 0.17.0
* 0.20.0


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* The Tarball for `icingaweb2_module_incubator__version` is downloaded on the Ansible controller (`delegate_to: 'localhost'`, `run_once: true`), then copied to the target. The controller therefore needs Internet access to GitHub; the target does not.
* On every role run the directory `/usr/share/icingaweb2/modules/incubator` is overwritten with the contents of the configured version. To upgrade or downgrade the module, change `icingaweb2_module_incubator__version` and re-run the role.
* `icingacli module enable incubator` is only invoked when `/etc/icingaweb2/enabledModules/incubator` does not yet exist (idempotent).


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.
* Internet access from the Ansible controller (downloads from `https://github.com/Icinga/icingaweb2-module-incubator/archive/`).


## Tags

`icingaweb2_module_incubator`

* Installs and enables the IcingaWeb2 Incubator Module.
* Triggers: none.


## Mandatory Role Variables

`icingaweb2_module_incubator__version`

* The module version to install. Possible options: https://github.com/Icinga/icingaweb2-module-incubator/releases.
* Type: String.

Example:

```yaml
# mandatory
icingaweb2_module_incubator__version: 'v0.20.0'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
