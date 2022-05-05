# Ansible Role system_update

This role configures the system to check for system updates, to schedule updates and reboots and to send notifications via email or Rocket.Chat.
The update check can be set to a specific weekday and daytime. The execution of available updates and necessary reboots can be scheduled relatively to the specific update check time e.g. "04:00 + 1 days".

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

| Tag   								| What it does                               		 	 				|
| ---   								| ------------                              		 	  			|
| system_uodate 				| Sets up automatic system update via systemd timer.	  	|
| system_update:state 	| Determines whether notify-and-schedule.timer is enabled |


## Role Variables

### Mandatory

#### system_update__notification_recipients

A list of recipients to notify about update schedules, the updates themselves and reboots.

Example:
```yaml
system_update__notification_recipients:
	- 'info@example.com'
	- 'support@example.com'
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

A list of recipients to notify if new versions config files have been found.

Example:
```yaml
system_update__new_configfile_notification_recipients:
	- 'info@example.com'
	- 'support@example.com'
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

The time when to actually execute the updates and to reboot, relative to the time which has been set in 'system_update__notify_time_wday', 'system_update__notify_time_hour' and 'system_update__notify_time_minute'.

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

The URL to a potential Rocket.Chat Server to send notifications about the updates to.

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

This codeblock will be executed after the updates have been installed and before a potentially scheduled reboot.

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
