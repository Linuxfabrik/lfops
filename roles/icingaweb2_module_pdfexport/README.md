# Ansible Role linuxfabrik.lfops.icingaweb2_module_pdfexport

This role installs and enables the [IcingaWeb2 PDF Export Module](https://github.com/Icinga/icingaweb2-module-pdfexport), used by IcingaWeb2 reporting and notification flows to render PDFs.

This role is tested with the following IcingaWeb2 PDF Export Module versions:

* 0.11.0


## How the Role Behaves

* The Tarball for `icingaweb2_module_pdfexport__version` is downloaded on the Ansible controller (`delegate_to: 'localhost'`, `run_once: true`), then copied to the target. The controller therefore needs Internet access to GitHub; the target does not.
* On every role run the directory `/usr/share/icingaweb2/modules/pdfexport` is overwritten with the contents of the configured version. To upgrade or downgrade the module, change `icingaweb2_module_pdfexport__version` and re-run the role.
* `icingacli module enable pdfexport` is only invoked when `/etc/icingaweb2/enabledModules/pdfexport` does not yet exist (idempotent).
* This role only installs the IcingaWeb2 module itself. Any runtime dependencies of the module (see the [module documentation](https://github.com/Icinga/icingaweb2-module-pdfexport#requirements)) have to be installed and configured separately.


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.
* Internet access from the Ansible controller (downloads from `https://github.com/Icinga/icingaweb2-module-pdfexport/archive/`).
* The runtime dependencies listed in the [module documentation](https://github.com/Icinga/icingaweb2-module-pdfexport#requirements) (typically a headless browser binary). Install and configure them separately.


## Tags

`icingaweb2_module_pdfexport`

* Installs and enables the IcingaWeb2 PDF Export Module.
* Triggers: none.


## Mandatory Role Variables

`icingaweb2_module_pdfexport__version`

* The module version to install. Possible options: https://github.com/Icinga/icingaweb2-module-pdfexport/releases.
* Type: String.

Example:

```yaml
# mandatory
icingaweb2_module_pdfexport__version: 'v0.11.0'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
