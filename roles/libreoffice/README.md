# Ansible Role linuxfabrik.lfops.libreoffice

This role installs LibreOffice on a server, so it is intended for headless operation and is mainly used for document conversion.


## Tags

`libreoffice`

* Installs LibreOffice.
* Triggers: none.


## Optional Role Variables

`libreoffice__client_apache`

* If set to `true`, LibreOffice is configured to run under the user "apache".
* Type: Bool.
* Default: `false`

Example:
```yaml
# optional
libreoffice__client_apache: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
