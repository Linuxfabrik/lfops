# Ansible Role linuxfabrik.lfops.logrotate

This role ensures that logrotate is installed and configured.

Tested on

* Fedora
* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Tags

| Tag         | What it does                         |
| ---         | ------------                         |
| `logrotate` | Installs and configures log rotation |


## Optional Role Variables

| Variable                 | Description                                         | Default Value |
| --------                 | -----------                                         | ------------- |
| `logrotate__rotate_days` | For how many days the rotated files should be kept. | `14`          |

Example:
```yaml
# optional
logrotate__rotate_days: 14
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
