# Ansible Role linuxfabrik.lfops.nodejs

This role installs Node.js.

By default, the role installs the latest available `nodejs` package from the configured repositories. On Red Hat-family systems you can pin to a specific DNF module stream using `nodejs__dnf_module_stream`. On Debian / Ubuntu the variable has no effect; whichever Node.js version the distribution ships will be installed.

After installation the role creates a symlink `/bin/nodejs -> /bin/node`. This keeps scripts and tooling that hard-code `/bin/nodejs` working on distributions that only ship `/bin/node` (or vice versa).


## Tags

`nodejs`

* Installs Node.js and creates the `/bin/nodejs` symlink.
* Triggers: none.


## Optional Role Variables

`nodejs__dnf_module_stream`

* The DNF module stream from which Node.js should be installed (Red Hat-family only). Possible options: `dnf module list nodejs`. Accepts the stream as a number (`20`) or as a string (`'20'`); both work because the role coerces it via the `string` filter.
* Type: Number or String.
* Default: unset (uses the default `nodejs` package).

Example:
```yaml
# optional
nodejs__dnf_module_stream: 20
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
