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

`borg_local`

* Installs and configures borg.
* Triggers: none.

`borg_local:configure`

* Configures borg.
* Triggers: none.

`borg_local:state`

* Manages the state of the borg timer.
* Triggers: none.


## Mandatory Role Variables

`borg_local__passphrase`

* Passphrase for the Borg repositories.
* Type: String.

Example:
```yaml
# mandatory
borg_local__passphrase: 'linuxfabrik'
```

## Optional Role Variables

`borg_local__backup_dir`

* The directory where the backup repositories will be created.
* Type: String.
* Default: `'/backup'`

`borg_local__backup_opts__host_var` / `borg_local__backup_opts__group_var`

* The list of options used by borg.
* Type: List of dictionaries.
* Default:

    * `'--stats'`
    * `'--progress'`
    * `'--one-file-system'`
    * `'--compression lz4'`
    * `'--checkpoint-interval 86400'`

* Subkeys:

    * `option`:

        * Mandatory. The option to be used.
        * Type: String.

    * `state`:

        * Optional. Either `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`borg_local__exclude_files__host_var` / `borg_local__exclude_files__group_var`

* The list of files or directories which should be excluded from the backup. Excludes act as filters within the included paths.
* Type: List of dictionaries.
* Default:

    * `'/root/.cache'`
    * `'*.svn*'`
    * `'*.git*'`
    * `'*.tmp'`
    * `'*.temp'`
    * `'*/cache/*'`
    * `'*/log/*'`

* Subkeys:

    * `file`:

        * Mandatory. The file or directory to be excluded.
        * Type: String.

    * `state`:

        * Optional. Either `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`borg_local__icinga2_api_url`

* The URL of the Icinga2 API (usually on the Icinga2 Master). This will be used to set a downtime for the corresponding ClamAV service.
* Type: String.
* Default: `'https://{{ icinga2_agent__icinga2_master_host | d("") }}:{{ icinga2_agent__icinga2_master_port | d(5665) }}'`

`borg_local__icinga2_api_user_login`

* The Icinga2 API User to set the downtime for the corresponding ClamAV service.
* Type: Dictionary.
* Default: unset

`borg_local__icinga2_hostname`

* The hostname of the Icinga2 host on which the downtime should be set.
* Type: String.
* Default: `'{{ ansible_facts["nodename"] }}'`

`borg_local__include_files__host_var` / `borg_local__include_files__group_var`

* The list of files or directories which should be included in the backup. Only the listed paths are backed up, everything else is implicitly excluded.
* Type: List of dictionaries.
* Default:

    * `'/etc'`
    * `'/home'`
    * `'/opt'`
    * `'/root'`
    * `'/var/spool/cron'`

* Subkeys:

    * `file`:

        * Mandatory. The file or directory to be included.
        * Type: String.

    * `state`:

        * Optional. Either `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`borg_local__on_calendar_daily_hour`

* The hour of the daily backup.
* Type: Number.
* Default: `23`

`borg_local__on_calendar_daily`

* The time at which the daily backup will run. Once per day.
* Type: String.
* Default: `'*-*-* {{ borg_local__on_calendar_daily_hour }}:{{ 45 | random(seed=inventory_hostname) }}'`

`borg_local__on_calendar_hourly`

* The time at which the hourly backup will run. Once per hour.
* Type: String.
* Default: `'*-*-* *:{{ 59 | random(start=45, seed=inventory_hostname) }}'`

`borg_local__retention_daily`

* The number of daily backups to keep.
* Type: String.
* Default: `'14d'`

`borg_local__retention_hourly`

* The number of hourly backups to keep.
* Type: String.
* Default: `'99H'`

`borg_local__timer_daily_enabled`

* Whether the daily backup should be enabled.
* Type: Bool.
* Default: `true`

`borg_local__timer_hourly_enabled`

* Whether the hourly backup should be enabled.
* Type: Bool.
* Default: `false`

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
