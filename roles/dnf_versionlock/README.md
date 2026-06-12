# Ansible Role linuxfabrik.lfops.dnf_versionlock

This role installs and configures the [dnf versionlock plugin](https://dnf-plugins-core.readthedocs.io/en/latest/versionlock.html) so that selected packages stay pinned across `dnf upgrade`.

The role auto-selects the right backend per OS:

* RHEL 7 / CentOS 7: installs `yum-plugin-versionlock` and writes the lock list to `/etc/yum/pluginconf.d/versionlock.list`. Note that `yum versionlock` has fewer capabilities than the DNF variant; some lock specs (e.g. patch-only pins like `enterprise-search-0:8.7.*`) only work on RHEL 8+.
* RHEL 8 / 9 and Fedora 40 / 41: installs `dnf-command(versionlock)` and writes the lock list to `/etc/dnf/plugins/versionlock.list`.

The lock list is rendered as a template, so every run replaces the file with the current `dnf_versionlock__versionlocks` content. Manual edits to `versionlock.list` are overwritten.


*Available since LFOps `3.0.0`.*


## Tags

`dnf_versionlock`

* Installs and configures dnf versionlock.
* Triggers: none.


## Mandatory Role Variables

`dnf_versionlock__versionlocks`

* List of versionlock (`<package-name-spec>`) entries. Have a look at `man yum-versionlock` for RHEL 7 or [dnf versionlock](https://dnf-plugins-core.readthedocs.io/en/latest/versionlock.html) for RHEL 8+.
* Type: List of strings.

Example:
```yaml
# mandatory
dnf_versionlock__versionlocks:
  - 'enterprise-search-0:8.7.*' # pin to 8.7.x, only allowing patch updates; only works on RHEL 8+
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
