# Ansible Role linuxfabrik.lfops.apps

This role manages a list of applications using the OS's package manager.


## Tags

`apps`

* Remove apps using the package manager.
* Deploy apps using the package manager.
* Triggers: none.


## Optional Role Variables

`apps__apps__host_var` / `apps__apps__group_var`

* List of apps to remove or to deploy.
* Type: List of dictionaries.
* Default: `[]`

* Subkeys:

    * `name`:

        * Mandatory. Name of the application package.
        * Type: String.

    * `state`:

        * Optional. Possible options: `present` (default), `absent`. You can use other states like `latest` ONLY if they are supported by the underlying package module(s) executed.
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
