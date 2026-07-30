# Ansible Role linuxfabrik.lfops.dnf_versionlock

This role installs and configures the [dnf versionlock plugin](https://dnf-plugins-core.readthedocs.io/en/latest/versionlock.html) so that selected packages stay pinned across `dnf upgrade`.


*Available since LFOps `3.0.0`.*


## How the Role Behaves

* **Only the entries you declare are managed.** The role drives the lock list entry by entry through the `community.general.dnf_versionlock` module instead of writing the file as a whole. Locks set by something else, for example the package pin of the [monitoring_plugins](https://github.com/Linuxfabrik/lfops/tree/main/roles/monitoring_plugins) role, are therefore left in place. An entry that is no longer wanted has to be removed explicitly with `state: 'absent'`; dropping it from the inventory alone does not unlock the package.
* **A lock is resolved at deploy time.** By default an entry is resolved through `dnf repoquery` and pins the version that is installed on the host, so the target needs to be able to reach its repositories. Set `raw: true` on an entry to write the spec verbatim instead, which also allows pinning a version that does not exist yet.
* **dnf only.** The module drives the `dnf` binary, so the role does not run on yum-based releases. It also does not support dnf5 (Fedora 41 and newer), where the versionlock configuration moved to `/etc/dnf/versionlock.toml`.


## Tags

`dnf_versionlock`

* Installs the versionlock plugin and applies the declared lock list entries.
* Triggers: none.


## Optional Role Variables

`dnf_versionlock__versionlocks__host_var` / `dnf_versionlock__versionlocks__group_var`

* List of dictionaries describing the versionlock entries. Have a look at [dnf versionlock](https://dnf-plugins-core.readthedocs.io/en/latest/versionlock.html) for the accepted package name specs.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. The package name spec to lock, in the format expected by `dnf repoquery`.
        * Type: String.

    * `raw`:

        * Optional. Set to `true` to use the spec verbatim instead of resolving it to the installed version. Required to pin a version that is not available yet.
        * Type: Bool.
        * Default: `false`

    * `state`:

        * Optional. `present` locks the package, `excluded` excludes the spec from transactions, and `absent` removes matching entries from the lock list.
        * Type: String. One of `absent`, `excluded`, `present`.
        * Default: `'present'`

Example:
```yaml
# optional
dnf_versionlock__versionlocks__host_var:
  - name: 'nginx'
    state: 'present'
  - name: 'enterprise-search-0:8.7.*' # pin to 8.7.x, only allowing patch updates
    raw: true
    state: 'present'
  - name: 'bind-32:9.11*'
    state: 'excluded'
  - name: 'httpd'
    state: 'absent'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
