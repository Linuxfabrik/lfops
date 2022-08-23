# Ansible Role linuxfabrik.lfops.system_update

This role configures the server to do (weekly) system updates by deploying two shell scripts: The first script `notify-and-schedule` checks for available updates (normally during the day), and notifies the system administrators either via email or [Rocket.Chat](https://rocket.chat/). On update time (usually the next morning at round about 4 AM), the second script `update-and-reboot`

* sets a downtime for the host and all it's services in Icinga
* applies all updates
* and, if necessary, automatically reboots the host after the updates.

Tested on

* Debian
* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Fedora


## Mandatory Requirements

* Install at. This can be done using the [linuxfabrik.lfops.at](https://github.com/Linuxfabrik/lfops/tree/main/roles/at) role.
* Install mailx. This can be done using the [linuxfabrik.lfops.mailx](https://github.com/Linuxfabrik/lfops/tree/main/roles/mailx) role.


## Tags

| Tag                   | What it does                                            |
| ---                   | ------------                                            |
| `system_update`       | Sets up automatic system update via systemd timer       |
| `system_update:state` | Determines whether notify-and-schedule.timer is enabled |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `system_update__new_configfile_notification_recipients` | A list of email recipients to notify if there is a new version of a config file (`rpmnew` / `rpmsave` / `dpkg-dist` / `ucf-dist`). |
| `system_update__notification_recipients` | A list of email recipients to notify about the expected updates and the report of the installed updates. |
| `system_update__notification_sender` | The email sender account. This will be used as the "from"-address for all notifications. |

Example:
```yaml
# mandatory
system_update__new_configfile_notification_recipients:
  - 'info@example.com'
  - 'support@example.com'
system_update__notification_recipients:
  - 'info@example.com'
  - 'support@example.com'
system_update__notification_sender: 'noreply@example.com'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `system_update__icinga2_api_user_login` | The Icinga2 API User to set the downtime for the corresponding host and all it's services. | unset |
| `system_update__icinga2_master` | The hostname or ip address of the Icinga2 master instance where to set the downtime for the corresponding host and all it's services. | unset |
| `system_update__notification_hostname_prefix` | This will set a prefix that will be showed in front of the hostname. Can be used to separate servers by environment or customer. | `true` |
| `system_update__post_update_code` | This codeblock will be executed after the updates have been installed and before a potential reboot. | unset |
| `system_update__rocketchat_msg_suffix` | A suffix to the Rocket.Chat notifications. This can be used to mention other users. | unset |
| `system_update__rocketchat_url` | The URL to a potential Rocket.Chat server to send notifications about the updates to. | unset |
| `system_update__update_enabled` | Enables or disables the system-update service, analogous to `systemctl enable/disable --now`.  | `true` |
| `system_update__update_on_calendar` | When the notification for the expected updates should be sent. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format. | `00'` |
| `system_update__update_time` | The time when to actually execute the updates (and automatically reboot if necessary), relative to `system_update__update_on_calendar`. | `00 + 1 days'` |

Example:
```yaml
# optional
system_update__icinga2_api_user_login:
  username: 'downtime-user'
  password: 'my-secret-password'
system_update__icinga2_master: 'icinga.example.com'
system_update__notification_hostname_prefix: '001-'
system_update__post_update_code: |-
  VAR='hello world'
  echo $VAR
system_update__rocketchat_msg_suffix: '@administrator'
system_update__rocketchat_url: 'https://chat.example.com/hooks/abcd1234'
system_update__update_enabled: true
system_update__update_on_calendar: 'mon 10:00'
system_update__update_time: '04:00 + 1 days'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
