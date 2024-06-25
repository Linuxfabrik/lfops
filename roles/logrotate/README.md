# Ansible Role linuxfabrik.lfops.logrotate

This role ensures that logrotate is installed and configured for main classic system log files like `/var/log/cron`, `/var/log/maillog` or `/var/log/messages`.

Additionally, this role allows you to deploy custom logrotate configs which are placed under `{{ inventory_dir }}/host_files/{{ inventory_hostname }}/etc/logrotate.d` on the Ansible control node. Keep in mind that later config files may override the options given in earlier files, so the order in which the logrotate config files are listed is important.


## Tags

| Tag         | What it does                         |
| ---         | ------------                         |
| `logrotate` | <ul><li>Set platform/version specific variables</li><li>Install logrotate</li><li>Copy logrotate.conf template to /etc</li><li>Copy system logrotate templates to /etc/logrotate.d</li><li>Check if custom logrotate configs for {{ inventory_hostname }} exist</li><li>Copy the custom logrotate configs to /etc/logrotate.d</li></ul> |


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
