# Ansible Role linuxfabrik.lfops.icingaweb2_module_businessprocess

This role installs and enables the [IcingaWeb2 Business Process Module](https://github.com/Icinga/icingaweb2-module-businessprocess), which lets you compose and visualize business-level service hierarchies on top of Icinga monitoring data.

This role is tested with the following IcingaWeb2 Business Process Module versions:

* 2.4.0


*Available since LFOps `3.0.0`.*


## How the Role Behaves

* The Tarball for `icingaweb2_module_businessprocess__version` is downloaded on the Ansible controller (`delegate_to: 'localhost'`, `run_once: true`), then copied to the target. The controller therefore needs Internet access to GitHub; the target does not.
* On every role run the directory `/usr/share/icingaweb2/modules/businessprocess` is overwritten with the contents of the configured version. To upgrade or downgrade the module, change `icingaweb2_module_businessprocess__version` and re-run the role.
* `icingacli module enable businessprocess` is only invoked when `/etc/icingaweb2/enabledModules/businessprocess` does not yet exist (idempotent).


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.
* Internet access from the Ansible controller (downloads from `https://github.com/Icinga/icingaweb2-module-businessprocess/archive/`).


## Tags

`icingaweb2_module_businessprocess`

* Installs and enables the IcingaWeb2 Business Process Module.
* Triggers: none.


## Mandatory Role Variables

`icingaweb2_module_businessprocess__version`

* The module version to install. Possible options: https://github.com/Icinga/icingaweb2-module-businessprocess/releases.
* Type: String.

Example:

```yaml
# mandatory
icingaweb2_module_businessprocess__version: 'v2.5.1'
```


## Optional Role Variables

`icingaweb2_module_businessprocess__url`

* The URL from which the module tarball is downloaded. Override only if you mirror the upstream GitHub release elsewhere.
* Type: String.
* Default: `'https://github.com/Icinga/icingaweb2-module-businessprocess/archive/{{ icingaweb2_module_businessprocess__version }}.tar.gz'`

Example:

```yaml
# optional
icingaweb2_module_businessprocess__url: 'https://github.com/Linuxfabrik/icingaweb2-module-businessprocess/archive/{{ icingaweb2_module_businessprocess__version }}.tar.gz'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
