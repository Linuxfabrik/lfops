# Ansible Role linuxfabrik.lfops.icingaweb2_module_cube

This role installs and enables the [IcingaWeb2 Cube Module](https://github.com/Icinga/icingaweb2-module-cube), which provides multi-dimensional pivot views (cubes) of host and service data in IcingaWeb2.

This role is tested with the following IcingaWeb2 Cube Module versions:

* 1.3.3


*Available since LFOps `3.0.0`.*


## How the Role Behaves

* The Tarball for `icingaweb2_module_cube__version` is downloaded on the Ansible controller (`delegate_to: 'localhost'`, `run_once: true`), then copied to the target. The controller therefore needs Internet access to GitHub; the target does not.
* On every role run the directory `/usr/share/icingaweb2/modules/cube` is overwritten with the contents of the configured version. To upgrade or downgrade the module, change `icingaweb2_module_cube__version` and re-run the role.
* `icingacli module enable cube` is only invoked when `/etc/icingaweb2/enabledModules/cube` does not yet exist (idempotent).


## Requirements

* The Ansible controller must have Internet access (downloads from `https://github.com/Icinga/icingaweb2-module-cube/archive/`).

Manual steps:

* Deploy a configured IcingaWeb2 by running the [icingaweb2](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/icingaweb2.yml) playbook (role: [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2)).


## Tags

`icingaweb2_module_cube`

* Installs and enables the IcingaWeb2 Cube Module.
* Triggers: none.


## Mandatory Role Variables

`icingaweb2_module_cube__version`

* The module version to install. Possible options: https://github.com/Icinga/icingaweb2-module-cube/releases.
* Type: String.

Example:

```yaml
# mandatory
icingaweb2_module_cube__version: 'v1.3.3'
```


## Optional Role Variables

`icingaweb2_module_cube__url`

* The URL from which the module tarball is downloaded. Override only if you mirror the upstream GitHub release elsewhere.
* Type: String.
* Default: `'https://github.com/Icinga/icingaweb2-module-cube/archive/{{ icingaweb2_module_cube__version }}.tar.gz'`

Example:

```yaml
# optional
icingaweb2_module_cube__url: 'https://github.com/Linuxfabrik/icingaweb2-module-cube/archive/{{ icingaweb2_module_cube__version }}.tar.gz'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
