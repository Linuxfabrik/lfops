# Ansible Role system_update

This role configures the server to do weekly system updates.
For this, the scripts first check for available updates during the day, and notify the system administrators (either via email or [Rocket.Chat](https://rocket.chat/)). The actual update will then be executed the next day, usually during the night (can be configured). If necessary, the server will be automatically rebooted after the updates.

FQCN: linuxfabrik.lfops.system_update

Tested on

* Debian
* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Fedora


## Requirements

### Roles

* linuxfabrik.lfops.at
* linuxfabrik.lfops.mailx


## Tags

| Tag                 | What it does                                            |
| ---                 | ------------                                            |
| system_update       | Sets up automatic system update via systemd timer       |
| system_update:state | Determines whether notify-and-schedule.timer is enabled |


## Role Variables

### Mandatory

#### system_update__notification_recipients

A list of email recipients to notify about the expected updates and the report of the installed updates.

Example:
```yaml
system_update__notification_recipients:
  - 'info@example.com'
  - 'support@example.com'
```


#### system_update__notification_sender

The email sender account. This will be used as the "from"-address for all notifications.

Example:
```yaml
system_update__notification_sender: 'noreply@example.com'
```


#### system_update__notification_hostname_prefix

This will set a prefix that will be showed in front of the hostname. Can be used to separate servers by environment or customer.

Example:
```yaml
system_update__notification_hostname_prefix: '1234-'
```


#### system_update__new_configfile_notification_recipients

A list of email recipients to notify if there is a new version of a config file (`rpmnew` / `rpmsave` / `dpkg-dist` / `ucf-dist`).

Example:
```yaml
system_update__new_configfile_notification_recipients:
  - 'info@example.com'
  - 'support@example.com'
```


#### system_update__update_on_calendar

When the notification for the expected updates should be sent. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format.

Example:
```yaml
system_update__update_on_calendar: 'mon 10:00'
```


#### system_update__update_time

The time when to actually execute the updates (and automatically reboot if necessary), relative to `system_update__update_on_calendar`.

Example:
```yaml
system_update__update_time: '04:00 + 1 days'
```


### Optional

#### system_update__update_enabled

Default:
```yaml
system_update__update_enabled: true
```


#### system_update__icinga2_api_user

The Icinga2 API User used to set the downtime for the corresponding host and all it's services.

Example:
```yaml
system_update__icinga2_api_user: 'username'
```


#### system_update__icinga2_api_password

The password for the Icinga2 API User used to set the downtime for the corresponding host and all it's services.

Example:
```yaml
system_update__icinga2_api_password: '1234abcd'
```


#### system_update__icinga2_master

The hostname or ip address of the Icinga2 master instance where to set the downtime for the corresponding host and all it's services.

Example:
```yaml
system_update__icinga2_master: 'icinga.example.com'
```


#### system_update__rocketchat_url

The URL to a potential Rocket.Chat server to send notifications about the updates to.

Example:
```yaml
system_update__rocketchat_url: 'rocketchat.example.com'
```


#### system_update__rocketchat_msg_suffix

A suffix to the Rocket.Chat notifications. This can be used to mention other users.

Example:
```yaml
system_update__rocketchat_msg_suffix: '@administrator'
```


#### system_update__post_update_code

This codeblock will be executed after the updates have been installed and before a potential reboot.

Example:
```yaml
system_update__post_update_code: |-
  VAR='hello world'
  echo $VAR
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
