# Ansible Role linuxfabrik.lfops.icingaweb2_module_pdfexport

This role installs and enables the [IcingaWeb2 PDF Export Module](https://github.com/Icinga/icingaweb2-module-pdfexport), used by IcingaWeb2 reporting and notification flows to render PDFs.

This role is tested with the following IcingaWeb2 PDF Export Module versions:

* 0.11.0


*Available since LFOps `4.0.0`.*


## How the Role Behaves

* The Tarball for `icingaweb2_module_pdfexport__version` is downloaded on the Ansible controller (`delegate_to: 'localhost'`, `run_once: true`), then copied to the target. The controller therefore needs Internet access to GitHub; the target does not.
* On every role run the directory `/usr/share/icingaweb2/modules/pdfexport` is overwritten with the contents of the configured version. To upgrade or downgrade the module, change `icingaweb2_module_pdfexport__version` and re-run the role.
* `icingacli module enable pdfexport` is only invoked when `/etc/icingaweb2/enabledModules/pdfexport` does not yet exist (idempotent).
* `/etc/icingaweb2/modules/pdfexport/config.ini` is deployed on every run. By default the module is wired to a running headless Chromium over the Chrome DevTools Protocol (CDP); set `icingaweb2_module_pdfexport__chrome_binary` to fall back to spawning Chromium locally on every export.
* This role only installs and configures the IcingaWeb2 module itself. The headless browser backend it talks to (see the [module documentation](https://github.com/Icinga/icingaweb2-module-pdfexport#requirements)) is provided separately by the [linuxfabrik.lfops.chromium_headless](https://github.com/Linuxfabrik/lfops/tree/main/roles/chromium_headless) role.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* A headless Chromium backend must provide the remote debugging interface this module connects to (role: [linuxfabrik.lfops.chromium_headless](https://github.com/Linuxfabrik/lfops/tree/main/roles/chromium_headless)).


## Requirements

* The Ansible controller must have Internet access (downloads from `https://github.com/Icinga/icingaweb2-module-pdfexport/archive/`).

Manual steps:

* Deploy a configured IcingaWeb2 by running the [icingaweb2](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/icingaweb2.yml) playbook (role: [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2)).


## Tags

`icingaweb2_module_pdfexport`

* Installs and enables the IcingaWeb2 PDF Export Module.
* Deploys `/etc/icingaweb2/modules/pdfexport/config.ini`.
* Triggers: none.

`icingaweb2_module_pdfexport:configure`

* Deploys `/etc/icingaweb2/modules/pdfexport/config.ini`.
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


## Optional Role Variables

`icingaweb2_module_pdfexport__chrome_binary`

* Path to a local Chrome / Chromium binary. If set, the module spawns Chrome locally on every PDF export and the `chrome_host` / `chrome_port` settings are ignored. Leave empty (the default) to use the remote CDP mode.
* Type: String.
* Default: `''`

`icingaweb2_module_pdfexport__chrome_host`

* Address of the headless Chromium instance the module connects to via the Chrome DevTools Protocol.
* Type: String.
* Default: `'{{ chromium_headless__listen_address | d("127.0.0.1") }}'`

`icingaweb2_module_pdfexport__chrome_port`

* Port of the headless Chromium instance the module connects to via the Chrome DevTools Protocol.
* Type: Number.
* Default: `'{{ chromium_headless__listen_port | d(9222) }}'`

`icingaweb2_module_pdfexport__force_temp_storage`

* When `true`, the module renders every PDF to a temporary file on disk before sending it to the browser instead of streaming it directly. Useful as a workaround on memory-constrained hosts.
* Type: Bool.
* Default: `false`

Example:

```yaml
# optional
icingaweb2_module_pdfexport__chrome_binary: '/usr/lib64/chromium-browser/headless_shell'
icingaweb2_module_pdfexport__chrome_host: '127.0.0.1'
icingaweb2_module_pdfexport__chrome_port: 9222
icingaweb2_module_pdfexport__force_temp_storage: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
