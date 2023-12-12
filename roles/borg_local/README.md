# Ansible Role linuxfabrik.lfops.borg_local

This role installs and configures [borg](https://www.borgbackup.org/) and sets up the desired backup repositories in a local directory.

Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Tags

| Tag                    | What it does                            |
| ---                    | ------------                            |
| `borg_local`           | Installs and configures borg            |
| `borg_local:configure` | Configures borg                         |
| `borg_local:state`     | Manages the state of the borg timer     |


## Mandatory Role Variables

This role does not have any mandatory variables.


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `borg_local__backup_dir` | The directory where the backup repositories will be created. | `/backup` |
| `borg_local__backup_hourly_enabled` | Whether the hourly backup should be enabled. | `false` |
| `borg_local__exclude_files` | The list of files which should be excluded from the backup. | `'--exclude /root/.cache --exclude '*.svn*' --exclude '*.git*' --exclude '*.tmp' --exclude '*.temp' --exclude '*/cache/*' --exclude '*/log/*''` |
| `borg_local__include_files` | The list of directories which should be included in the backup.  | `'/etc /home /opt /root /var/spool/cron'` |
| `borg_local__on_calendar_daily` | The time the daily backup will happen. Once per day. | `'*-*-* {{ borg_local__on_calendar_daily_hour }}:{{ 45|random(seed=inventory_hostname) }}'` |
| `borg_local__on_calendar_daily_hour` | The hour of the daily backup  | `23` |
| `borg_local__on_calendar_hourly` | The time the daily backup will happen. Once per hour. | `'*-*-* *:{{ 59 |random(start=45) }}'` |
| `borg_local__relocated_repo_access_is_ok` | Depending on this value, borg may warn you that the repository has been moved, if you did so. You will be given a prompt to confirm you are OK with this. | `'yes'` |
| `borg_local__retention_daily` | The amount of daily backups into the past. | `'14d'` |
| `borg_local__retention_hourly` | The amount of hourly backups into the past. | `'99H'` |
| `borg_local__service_enabled` | Whether the borg service is enabled or not. | `true` |

Example:
```yaml
# optional
borg_local__backup_dir: '/backup'
borg_local__backup_hourly_enabled: false
borg_local__exclude_files: "--exclude /root/.cache --exclude '*.svn*' --exclude '*.git*' --exclude '*.tmp' --exclude '*.temp' --exclude '*/cache/*' --exclude '*/log/*'"
borg_local__include_files: '/etc /home /opt /root /var/spool/cron'
borg_local__on_calendar_daily: '*-*-* {{ borg_local__on_calendar_daily_hour }}:{{ 45|random(seed=inventory_hostname) }}'
borg_local__on_calendar_daily_hour: 23
borg_local__on_calendar_hourly: '*-*-* *:{{ 59 |random(start=45) }}'
borg_local__relocated_repo_access_is_ok: 'yes'
borg_local__retention_daily: '14d'
borg_local__retention_hourly: '99H'
borg_local__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
