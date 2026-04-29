# Ansible Role linuxfabrik.lfops.icingaweb2_module_fileshipper

This role installs and enables the [IcingaWeb2 Fileshipper Module](https://github.com/Icinga/icingaweb2-module-fileshipper). The Fileshipper extends the Icinga Director with two things: an `Import Source` that reads CSV / JSON / YAML / XML files from disk, and the ability to ship hand-crafted Icinga 2 config files through the Director.

This role is tested with the following IcingaWeb2 Fileshipper Module versions:

* 1.2.0


*Available since LFOps `3.0.0`.*


## How the Role Behaves

* The Tarball for `icingaweb2_module_fileshipper__version` is downloaded on the Ansible controller (`delegate_to: 'localhost'`, `run_once: true`), then copied to the target. The controller therefore needs Internet access to GitHub; the target does not.
* On every role run the directory `/usr/share/icingaweb2/modules/fileshipper` is overwritten with the contents of the configured version. To upgrade or downgrade the module, change `icingaweb2_module_fileshipper__version` and re-run the role.
* `icingacli module enable fileshipper` is only invoked when `/etc/icingaweb2/enabledModules/fileshipper` does not yet exist (idempotent).
* PHP runtime dependencies (`php-xml`, `php-yaml`, `php-zip`) are not installed by this role directly; they are injected into the `php` role via the `icingaweb2_module_fileshipper__php__modules__dependent_var` default. Install them via the [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role (the bundled playbook does this for you).


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.
* PHP with the `php-xml`, `php-yaml` and `php-zip` modules installed (see above).
* Internet access from the Ansible controller (downloads from `https://github.com/Icinga/icingaweb2-module-fileshipper/archive/`).


## Tags

`icingaweb2_module_fileshipper`

* Installs and enables the IcingaWeb2 Fileshipper Module.
* Triggers: none.


## Mandatory Role Variables

`icingaweb2_module_fileshipper__version`

* The module version to install. Possible options: https://github.com/Icinga/icingaweb2-module-fileshipper/releases.
* Type: String.

Example:

```yaml
# mandatory
icingaweb2_module_fileshipper__version: 'v1.2.0'
```


## Optional Role Variables

`icingaweb2_module_fileshipper__url`

* The URL from which the module tarball is downloaded. Override only if you mirror the upstream GitHub release elsewhere.
* Type: String.
* Default: `'https://github.com/Icinga/icingaweb2-module-fileshipper/archive/{{ icingaweb2_module_fileshipper__version }}.tar.gz'`

Example:

```yaml
# optional
icingaweb2_module_fileshipper__url: 'https://github.com/Linuxfabrik/icingaweb2-module-fileshipper/archive/{{ icingaweb2_module_fileshipper__version }}.tar.gz'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
