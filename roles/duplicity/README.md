# Ansible Role duplicity

This role configures *daily file-based* backups using [duplicity](https://duplicity.gitlab.io/). Currently, this role is focused on using [OpenStack Object Storage ("Swift")](https://wiki.openstack.org/wiki/Swift) as the storage backend.

FQCN: linuxfabrik.lfops.duplicity

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Fedora 35


## duba (Duplicity Backup)

The role comes with the special Python wrapper script `duba` for duplicity, implemented by Linuxfabrik. The script currently does a massive parallel backup to a Swift storage backend with duplicity, where the number of duplicity processes is (processor count + 1). The script's configuration file is located at `/etc/duba/duba.json`.

To start a backup, simply call `duba` (or `duba --config=/etc/duba/duba.json --command=backup`). Have a look at `duba --help` for details.


## Requirements

### Mandatory

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Install `duplicity`, `python-swiftclient` and `python-keystoneclient` into a Python 3 virtual environment in `/opt/python-venv/duplicity`. This can be done using the [linuxfabrik.lfops.python_venv](https://github.com/Linuxfabrik/lfops/tree/main/roles/python_venv) role.

**Attention**

> Make sure the virtual environment is not writable by other users to prevent privilege escalation. This is also done by the [linuxfabrik.lfops.python_venv](https://github.com/Linuxfabrik/lfops/tree/main/roles/python_venv) role.


### Optional

* Create a symbolic link from `/opt/python-venv/duplicity/bin/duplicity` to `/usr/local/bin/duplicity` for easier usage on the command line.
* Either configure journald to persist your logs and do the rotating, or use logrotated.


## Tags

| Tag                 | What it does                                 |
| ---                 | ------------                                 |
| duplicity           | Installs and configures duplicity            |
| duplicity:configure | Deploys the configuration for duplicity      |
| duplicity:state     | Manages the state of the daily systemd timer |
| duplicity:script    | Just deploys the `duba` script               |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/duplicity/defaults/main.yml) for the variable defaults.


### Mandatory

#### duplicity__gpg_encrypt_master_key

The long key ID of the master GPG key. Obtain it using `gpg --list-secret-keys --keyid-format=long`.

Default: unset

Example:
```yaml
duplicity__gpg_encrypt_master_key: 'LLZGH2BITI2LRLJCLFWEAJQ93N6MWTKBARQDMYX5'
```


#### duplicity__gpg_encrypt_master_key_block

The ASCII-armored public master GPG key. Obtain it using `gpg --armor --export $GPG_KEY`. This key is imported on the server and is used in addition to the server's own local GPG key to encrypt the backups. This means that the backups can be restored using either the master or the server's local private key (which is pretty cool in case of a desaster recovery).

Be aware of the empty line between `-----BEGIN PGP PUBLIC KEY BLOCK-----` and your public key block.

Default: unset

Example:
```yaml
duplicity__gpg_encrypt_master_key_block: |-
  -----BEGIN PGP PUBLIC KEY BLOCK-----

  6ec3d2aed2a54122817ca02b43a7e340kgKEdlbmVyYXRlZCBieSBBbnNpYmxlLi
  ...
  -----END PGP PUBLIC KEY BLOCK-----
```


#### duplicity__swift_login

The Swift username and password. Usually, this is given by the provider of the Swift Storage.

Subkeys:

* `username`: Mandatory, string. The Swift username.
* `password`: Mandatory, string. The Swift password.

Default: unset

Example:
```yaml
duplicity__swift_login:
  username: 'SBI-MF827483'
  password: 'some-secret-password'
```


#### duplicity__swift_tenantname

The Swift Tenantname. Usually, this is given by the provider of the Swift Storage.

Default: unset

Example:
```yaml
duplicity__swift_tenantname: 'sb_project_SBI-MF827483'
```


### Optional

#### duplicity__backup_dest_container

The Swift container. This can be used to separate backups on the destination. By default, this will be used in `duplicity__backup_dest`.

Default:
```yaml
duplicity__backup_dest_container: '{{ ansible_nodename }}'
```


#### duplicity__backup_dest

The backup destination. This will be used in combination with the backup source path to create the target URL for `duplicity`.

Default:
```yaml
duplicity__backup_dest: 'swift://{{ duplicity__backup_dest_container | trim("/") }}'
```


#### duplicity__backup_retention_time

The retention time of the backups. Time Formats: `s`, `m`, `h`, `D`, `W`, `M`, or `Y`.

Default:
```yaml
duplicity__backup_retention_time: '30D' # days
```


#### duplicity__host_backup_sources / duplicity__group_backup_sources

By default, the following directories are always backed up:

* /backup
* /etc
* /home
* /opt
* /root
* /var/spool/cron

These variables allow you to add additional directories to the backup and are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

Subkeys:

* `path`: Mandatory, string. Path to the folder to be backed up.
* `divide`: Optional, boolean. Defaults to `false`. Whether to split a large directory at its first level to perform parallel backups. Imagine a computer with 4 processor cores and the folder `data` containing 100 files and folders. If `divide` is set to `true`, `duba` will start and control 5 duplicate processes at once to speed up the backup process by almost a factor of 5.
* `excludes`: Optional, list. Defaults to `[]`. List of patterns that should not be included in the backup for this `path`.

Default:
```yaml
duplicity__host_backup_sources: []
duplicity__group_backup_sources: []
```

Example:
```yaml
duplicity__host_backup_sources:
  - path: '/var/www/html'
    divide: false
    excludes:
      - '/var/www/html/nextcloud/data'
  - path: '/var/www/html/nextcloud/data'
    divide: true
```


#### duplicity__excludes

List of *global* exclude shell patterns for `duplicity`. Have a look at `man duplicity` for details.

Default:
```yaml
duplicity__excludes:
  - '**/*.git*'
  - '**/*.svn*'
  - '**/*.temp'
  - '**/*.tmp'
  - '**/.cache'
  - '**/cache'
  - '**/log'
```


#### duplicity__timer_enabled

The state of the daily systemd timer.

Default:
```yaml
duplicity__timer_enabled: true
```


#### duplicity__on_calendar_hour

A shorthand to set the hour of `duplicity__on_calendar`.

Default:
```yaml
duplicity__on_calendar_hour: '23'
```


#### duplicity__on_calendar

The `OnCalendar` definition for the daily systemd timer. Have a look at `man systemd.time(7)` for the format.

Default:
```yaml
duplicity__on_calendar: '*-*-* {{ duplicity__on_calendar_hour }}:{{ 45 | random(seed=inventory_hostname) }}'
```


#### duplicity__loglevel

Set the loglevel. Possible options:

* error
* warning
* notice
* info
* debug

Default:
```yaml
duplicity__loglevel: 'notice'
```


#### duplicity__logrotate

Log files are rotated `count` days before being removed or mailed to the address specified in a `logrotate` mail directive. If count is `0`, old versions are removed rather than rotated. If count is `-1`, old logs are not removed at all (use with caution, may waste performance and disk space).

Default:
```yaml
duplicity__logrotate: 14
```


#### duplicity__swift_authurl

The Authentication URL for Swift. Usually, this is given by the provider of the Swift Storage.

Default:
```yaml
duplicity__swift_authurl: 'https://swiss-backup02.infomaniak.com/identity/v3'
```


#### duplicity__swift_authversion

The Authentication Version for Swift. Usually, this is given by the provider of the Swift Storage.

Default:
```yaml
duplicity__swift_authversion: '3'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
