# Ansible Role linuxfabrik.lfops.nodejs

This role installs Node.js.

By default, the role just installs the latest available `nodejs` package. One can use `nodejs__dnf_module_stream` to install `nodejs` from a DNF module stream.


## Tags

`nodejs`

* Installs Node.js.
* Triggers: none.


## Optional Role Variables

`nodejs__dnf_module_stream`

* The DNF module stream from which Node.js should be installed. Possible options: `dnf module list nodejs`.
* Type: Number.
* Default: unset

Example:
```yaml
# optional
nodejs__dnf_module_stream: 16
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
