# Ansible Role system_update

This role configures automatic system updates.

FQCN: linuxfabrik.lfops.system_update

Tested on

* Debian
* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Fedora


## Requirements

### Roles:

* at
* mailx


## Tags

| Tag   				| What it does                               		 	  |
| ---   				| ------------                              		 	  |
| system_uodate 		| Sets up automatic system update via systemd timer.	  |
| system_update__state 	| Determines whether notify-and-schedule.timer is enabled |


## Role Variables

### Mandatory

#### system_update__notification_recipients

The recipients of update and reboot notifications. This can consist of multiple addresses separated by whitespaces.

Example:
```yaml
system_update__notification_recipients: 'info@example.com support@example.com'
```


#### system_update__notification_sender

The sender of email notifications.

Example:
```yaml
system_update__notification_sender: 'noreply@example.com'
```


#### system_update__notification_hostname_prefix

This will set a prefix to the hostname. E.g. a customer number.

Example:
```yaml
system_update__notification_hostname_prefix: '1234'
```


#### system_update__new_configfile_notification_recipients

The recipients of new config file notifications. This can consist of multiple addresses separated by whitespaces.

Example:
```yaml
system_update__new_configfile_notification_recipients: 'info@example.com support@example.com'
```


#### system_update__notify_time_wday

The weekday when to check for updates and to notify about them.

Example:
```yaml
system_update__notify_time_wday: 'mon'
```


#### system_update__notify_time_hour

The hour when to check for updates and to notify about them.

Example:
```yaml
system_update__notify_time_hour: '09'
```


#### system_update__notify_time_minute

The minute when to check for updates and to notify about them.

Example:
```yaml
system_update__notify_time_minute: '30'
```


#### system_update__update_time

The time when to actually execute the updates and to reboot.

Example:
```yaml
system_update__update_time: '04:04 + 1 days'
```


### Optional

#### system_update__update_enabled

Default:
```yaml
system_update__update_enabled: true
```


#### system_update__update_on_calendar

Allow setting via legacy variables, but it also allows setting update_on_calendar directly.

Default:
```yaml
system_update__update_on_calendar: '{{ system_update__notify_time_wday }} {{ system_update__notify_time_hour }}:{{ system_update__notify_time_minute }}'
```

Example:
```yaml
system_update__update_on_calendar: 'mon 09:30'
```


#### icinga2_api_user

The Icinga2 API User used to set downtimes.

Default:
```yaml
icinga2_api_user: ''
```


#### icinga2_api_password

The password for the Icinga2 API User used to set downtimes.

Default:
```yaml
icinga2_api_password: ''
```


#### icinga2_master

The hostname or ip address of the Icinga2 master instance.

Default:
```yaml
icinga2_master: ''
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
