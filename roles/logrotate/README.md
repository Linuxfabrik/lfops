# Ansible Role linuxfabrik.lfops.logrotate

This role ensures that logrotate is installed and configured for main classic system log files like `/var/log/cron`, `/var/log/maillog` or `/var/log/messages`.

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
| `logrotate__rotate`      | Number. Log files are rotated `count` days before being removed or mailed to the address specified in a `logrotate` mail directive. If count is `0`, old versions are removed rather than rotated. If count is `-1`, old logs are not removed at all (use with caution, may waste performance and disk space). | `14`          |

Example:
```yaml
# optional
logrotate__rotate: 7
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
