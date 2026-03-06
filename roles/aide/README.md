# Ansible Role linuxfabrik.lfops.aide

This role ensures that AIDE is installed, configured, and scheduled for regular filesystem integrity checks.

* The initial AIDE database is created only if `/var/lib/aide/aide.db.gz` does not already exist.


## Tags

| Tag | What it does | Reload / Restart |
| --- | ------------ | ---------------- |
| `aide` | Runs all tasks of the role | - |
| `aide:configure` | Deploys the `/etc/aide.conf` configuration file | - |
| `aide:install` | Installs the AIDE package and initializes the AIDE database if it does not exist yet | - |
| `aide:update_db` | Rebuilds the AIDE database; Only runs if called explicitly | - |
| `aide:state` | Deploys and enables the `aide-check.service` and `aide-check.timer` systemd units | Reloads systemd daemon if unit files changed |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `aide__check_time_on_calendar` | Specifies at what time of the day the aide check runs. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format. | `'05:00:00'` |
| `aide__include_rules` | List of paths to monitor with their AIDE rule group. | `['/srv CONTENT_EX', '/opt/venv CONTENT']` |
| `aide__exclude_rules` | List of paths to exclude from monitoring. | `['/srv/app/tmp', '/srv/app/cache']` |

Example:
```yaml
# optional
aide__check_time_on_calendar: '03:00:00'
aide__include_rules:
  - '/etc CONTENT_EX'      # Extended content + file type + access
  - '/srv/app/node_modules CONTENT'    # Content + file type
aide__exclude_rules:
  - '/var/log'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
