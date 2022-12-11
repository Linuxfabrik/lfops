# Ansible Role linuxfabrik.lfops.libreoffice

This role installs LibreOffice on a server, so it is intended for headless operation and is mainly used for document conversion.

Runs on

* RHEL 8 (and compatible)


## Tags

| Tag           | What it does     |
| ---           | ------------     |
| `libreoffice` | Installs LibreOffice |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `libreoffice__client_apache`| Boolean. If set to `true`, LibreOffice is configured to run under the user "apache". | unset |

Example:
```yaml
# optional
libreoffice__client_apache: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
