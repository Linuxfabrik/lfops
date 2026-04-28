# Ansible Role linuxfabrik.lfops.apps

This role manages a list of applications using the OS's package manager. Internally it uses `ansible.builtin.package`, so the right backend (`apt`, `dnf`, `yum`, ...) is chosen automatically per host.

Items with `state: 'absent'` are removed first, then everything else is installed in a single `present` call.


## Tags

`apps`

* Removes apps using the package manager.
* Deploys apps using the package manager.
* Triggers: none.


## Optional Role Variables

`apps__apps__host_var` / `apps__apps__group_var`

* List of apps to remove or to deploy. Items can be set on multiple inventory levels (`host_var`, `group_var`); the role merges them via the standard LFOps "Combined Variables" pattern.
* Type: List of dictionaries.
* Default: `[]`

* Subkeys:

    * `name`:

        * Mandatory. Name of the application package, as understood by the host's package manager.
        * Type: String.

    * `state`:

        * Optional. Possible options: `'present'` (default), `'absent'`. You can use other states like `'latest'` ONLY if they are supported by the underlying package backend (`apt`, `dnf`, ...) on the target host.
        * Type: String.
        * Default: `'present'`

Example:
```yaml
# optional
apps__apps__host_var:
  - name: 'svn'
    state: 'absent'
  - name: 'git'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
