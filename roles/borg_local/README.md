# Ansible Role linuxfabrik.lfops.borg_local

This role installs and configures [borg](https://www.borgbackup.org/) and sets up the desired backup repositories in a local directory.

Note that if ClamAV (`clamd@scan.service`) is found on the host, it will be temporarily disabled during the backup.

To restore from a backup:
```bash
mkdir -p /mnt/borg

source /etc/borg/borg.conf
BORG_REPO="$BACKUP_DIR/daily" # or hourly or on-demand
borg mount "$BORG_REPO" /mnt/borg

cd /mnt/borg/20240101/backup/mariadb-dump
ll -h
cp -a /mnt/borg/20240101/backup/mariadb-dump /restore

# clean up (else the next backup fails)
umount /mnt/borg
```


## Tags

| Tag                    | What it does                            |
| ---                    | ------------                            |
| `borg_local`           | Installs and configures borg            |
| `borg_local:configure` | Configures borg                         |
| `borg_local:state`     | Manages the state of the borg timer     |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `borg_local__passphrase` | Passphrase for the Borg repositories. |

Example:
```yaml
# mandatory
borg_local__passphrase: 'linuxfabrik'
```

## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `borg_local__backup_dir` | The directory where the backup repositories will be created. | `/backup` |
| `borg_local__backup_opts__host_vars` / <br> `borg_local__backup_opts__group_vars` | The list of options used by borg. Subkeys: <ul><li>`option`: Mandatory, string. The option to be used.</li><li>`state`: Optional, string. Either `present` or `absent`. Defaults to `present`.</li></ul> | <ul><li>`'--stats'`</li><li>`'--progress'`</li><li>`'--one-file-system'`</li><li>`'--compression lz4'`</li><li>`'--checkpoint-interval 86400'`</li></ul> |
| `borg_local__exclude_files__host_vars` / <br> `borg_local__exclude_files__group_vars` | The list of files or direcotries which should be excluded from the backup. Subkeys: <ul><li>`file`: Mandatory, string. The file or directory to be excluded.</li><li>`state`: Optional, string. Either `present` or `absent`. Defaults to `present`.</li></ul> | <ul><li>`'/root/.cache'`</li><li>`'*.svn*'`</li><li>`'*.git*'`</li><li>`'*.tmp'`</li><li>`'*.temp'`</li><li>`'*/cache/*'`</li><li>`'*/log/*'`</li></ul> |
| `borg_local__icinga2_api_url` | The URL of the Icinga2 API (usually on the Icinga2 Master). This will be used to set a downtime for the corresponding ClamAV service. | `'https://{{ icinga2_agent__icinga2_master_host \| d("") }}:{{ icinga2_agent__icinga2_master_port \| d(5665) }}'` |
| `borg_local__icinga2_api_user_login` | The Icinga2 API User to set the downtime for the corresponding ClamAV service. | unset |
| `borg_local__icinga2_hostname` | The hostname of the Icinga2 host on which the downtime should be set. | `'{{ ansible_facts["nodename"] }}'` |
| `borg_local__include_files__host_vars` / <br> `borg_local__include_files__group_vars` | The list of files or directories which should be included in the backup. Subkeys: <ul><li>`file`: Mandatory, string. The file or directory to be included.</li><li>`state`: Optional, string. Either `present` or `absent`. Defaults to `present`.</li></ul> | <ul><li>`'/etc'`</li><li>`'/home'`</li><li>`'/opt'`</li><li>`'/root'`</li><li>`'/var/spool/cron'`</li></ul> |
| `borg_local__on_calendar_daily_hour` | The hour of the daily backup  | `23` |
| `borg_local__on_calendar_daily` | The time at which the daily backup will run. Once per day. | `'*-*-* {{ borg_local__on_calendar_daily_hour }}:{{ 45\|random(seed=inventory_hostname) }}'` |
| `borg_local__on_calendar_hourly` | The time at which the hourly backup will run. Once per hour. | `'*-*-* *:{{ 59 \|random(start=45) }}'` |
| `borg_local__retention_daily` | The number of daily backups to keep. | `'14d'` |
| `borg_local__retention_hourly` | The number of hourly backups to keep. | `'99H'` |
| `borg_local__timer_daily_enabled` | Whether the daily backup should be enabled. | `true` |
| `borg_local__timer_hourly_enabled` | Whether the hourly backup should be enabled. | `false` |

Example:
```yaml
# optional
borg_local__backup_dir: '/backup'
borg_local__backup_opts__host_var:
  - option: '--stats'
  - option: '--progress'
  - option: '--one-file-system'
  - option: '--compression lz4'
  - option: '--checkpoint-interval 86400'
borg_local__exclude_files__host_var:
  - file: '/root/.cache'
  - file: '*.svn*'
  - file: '*.git*'
  - file: '*.tmp'
  - file: '*.temp'
  - file: '*/cache/*'
  - file: '*/log/*'
borg_local__icinga2_api_url: 'https://icinga.example.com:5665'
borg_local__icinga2_api_user_login:
  username: 'downtime-user'
  password: 'linuxfabrik'
borg_local__icinga2_hostname: 'myhost.example.com'
borg_local__include_files__host_var:
  - file: '/etc'
  - file: '/home'
  - file: '/opt'
  - file: '/root'
  - file: '/var/spool/cron'
borg_local__on_calendar_daily: '*-*-* {{ borg_local__on_calendar_daily_hour }}:{{ 45 | random(seed=inventory_hostname) }}'
borg_local__on_calendar_daily_hour: 23
borg_local__on_calendar_hourly: '*-*-* *:{{ 59 | random(start=45) }}'
borg_local__retention_daily: '14d'
borg_local__retention_hourly: '99H'
borg_local__timer_daily_enabled: true
borg_local__timer_hourly_enabled: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
