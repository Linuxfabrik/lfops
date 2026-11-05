# Ansible Role linuxfabrik.lfops.nodejs

This role installs Node.js.

By default, the role installs the latest available `nodejs` package from the configured repositories. On Red Hat-family systems you can select a different Node.js major version using `nodejs__dnf_module_stream`. On RHEL 8 and 9 the role installs it from the DNF module stream of that number. RHEL 10 has no modules, so the role installs the `nodejs<version>` and `nodejs<version>-npm` packages (for example `nodejs24`) and links `/usr/bin/node`, `/usr/bin/npm` and `/usr/bin/npx` to the versioned binaries of these packages. On Debian / Ubuntu the variable has no effect; whichever Node.js version the distribution ships will be installed.

After installation the role creates a symlink `/bin/nodejs -> /bin/node`. This keeps scripts and tooling that hard-code `/bin/nodejs` working on distributions that only ship `/bin/node` (or vice versa).


*Available since LFOps `2.0.0`.*


## Tags

`nodejs`

* Installs Node.js and creates the `/bin/nodejs` symlink.
* Triggers: none.


## Optional Role Variables

`nodejs__dnf_module_stream`

* The Node.js major version to install (Red Hat family only). Possible options: `dnf module list nodejs` on RHEL 8 and 9, `dnf list 'nodejs[0-9]*'` on RHEL 10. On RHEL 10, the default version (Node.js 22, the `nodejs` package) has no versioned package, leave the variable unset for it. Remove an installed `nodejs` package before switching to another version there, since it owns `/usr/bin/node`; the role aborts otherwise. Accepts the stream as a number (`20`) or as a string (`'20'`); both work because the role coerces it via the `string` filter.
* Type: Number or String.
* Default: unset (uses the default `nodejs` package).

Example:
```yaml
# optional
nodejs__dnf_module_stream: 24
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
