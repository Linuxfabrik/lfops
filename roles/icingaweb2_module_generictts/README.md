# Ansible Role linuxfabrik.lfops.icingaweb2_module_generictts

This role installs and enables the [IcingaWeb2 GenericTTS Module](https://github.com/Icinga/icingaweb2-module-generictts). The module rewrites ticket patterns (configurable regular expressions) found in Icinga acknowledgements, downtimes and comments into clickable links pointing at the configured trouble-ticket system.

This role is tested with the following IcingaWeb2 GenericTTS Module versions:

* 2.1.0


*Available since LFOps `3.0.0`.*


## How the Role Behaves

* The Tarball for `icingaweb2_module_generictts__version` is downloaded on the Ansible controller (`delegate_to: 'localhost'`, `run_once: true`), then copied to the target. The controller therefore needs Internet access to GitHub; the target does not.
* On every role run the directory `/usr/share/icingaweb2/modules/generictts` is overwritten with the contents of the configured version. To upgrade or downgrade the module, change `icingaweb2_module_generictts__version` and re-run the role.
* `icingacli module enable generictts` is only invoked when `/etc/icingaweb2/enabledModules/generictts` does not yet exist (idempotent).


## Requirements

* The Ansible controller must have Internet access (downloads from `https://github.com/Icinga/icingaweb2-module-generictts/archive/`).

Manual steps:

* Deploy a configured IcingaWeb2 by running the [icingaweb2](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/icingaweb2.yml) playbook (role: [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2)).


## Tags

`icingaweb2_module_generictts`

* Installs and enables the IcingaWeb2 GenericTTS Module.
* Triggers: none.


## Mandatory Role Variables

`icingaweb2_module_generictts__version`

* The module version to install. Possible options: https://github.com/Icinga/icingaweb2-module-generictts/releases.
* Type: String.

Example:

```yaml
# mandatory
icingaweb2_module_generictts__version: 'v2.1.0'
```


## Optional Role Variables

`icingaweb2_module_generictts__url`

* The URL from which the module tarball is downloaded. Override only if you mirror the upstream GitHub release elsewhere.
* Type: String.
* Default: `'https://github.com/Icinga/icingaweb2-module-generictts/archive/{{ icingaweb2_module_generictts__version }}.tar.gz'`

Example:

```yaml
# optional
icingaweb2_module_generictts__url: 'https://github.com/Linuxfabrik/icingaweb2-module-generictts/archive/{{ icingaweb2_module_generictts__version }}.tar.gz'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
