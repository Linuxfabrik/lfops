# Ansible Role linuxfabrik.lfops.system_update

This role configures the server to do (weekly) system updates by deploying two shell scripts: The first script `notify-and-schedule` checks for available updates (normally during the day), and notifies the system administrators either via email or [Rocket.Chat](https://rocket.chat/). On update time (usually the next morning at round about 4 AM), the second script `update-and-reboot`

* sets a downtime for the host and all its services in Icinga
* applies all updates
* and, if necessary, automatically reboots the host after the updates.


## Mandatory Requirements

* Install at. This can be done using the [linuxfabrik.lfops.at](https://github.com/Linuxfabrik/lfops/tree/main/roles/at) role.
* Install mailx. This can be done using the [linuxfabrik.lfops.mailx](https://github.com/Linuxfabrik/lfops/tree/main/roles/mailx) role.
* Install needrestart on Debian. This can be done using the [linuxfabrik.lfops.apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps) role.
* Install yum-utils on RHEL. This can be done using the [linuxfabrik.lfops.yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils) role.

If you use the [system_update Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/system_update.yml), this is automatically done for you.


## Tags

| Tag                   | What it does                                            |
| ---                   | ------------                                            |
| `system_update`       | Sets up automatic system update via systemd timer       |
| `system_update:state` | Determines whether notify-and-schedule.timer is enabled |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `system_update__icinga2_api_url` | The URL of the Icinga2 API (usually on the Icinga2 Master). This will be used to set a downtime for the corresponding host and all its services in the `reboot` alias. | `'https://{{ icinga2_agent__icinga2_master_host | d("") }}:{{ icinga2_agent__icinga2_master_port | d(5665) }}'` |
| `system_update__icinga2_api_user_login` | The Icinga2 API User to set the downtime for the corresponding host and all its services. | unset |
| `system_update__icinga2_hostname` | The hostname of the Icinga2 host on which the downtime should be set. |  `'{{ ansible_facts["nodename"] }}'` |
| `system_update__mail_from` | The email sender account. This will be used as the "from"-address for all notifications. | `'{{ mailto_root__from }}'` |
| `system_update__mail_recipients_new_configfiles` | A list of email recipients to notify if there is a new version of a config file (`rpmnew` / `rpmsave` / `dpkg-dist` / `ucf-dist`). | `'{{ mailto_root__to }}'` |
| `system_update__mail_recipients_updates` | A list of email recipients to notify about the expected updates and the report of the installed updates. | `'{{ mailto_root__to }}'` |
| `system_update__mail_subject_prefix` | This will set a prefix that will be showed in front of the hostname. Can be used to separate servers by environment or customer. | `''` |
| `system_update__notify_and_schedule_on_calendar` | When the notification for the expected updates should be sent. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format. | `'mon 10:00'` |
| `system_update__post_update_code` | This codeblock will be executed after the updates have been installed and before a potential reboot. | unset |
| `system_update__rocketchat_msg_suffix` | A suffix to the Rocket.Chat notifications. This can be used to mention other users. | unset |
| `system_update__rocketchat_url` | The URL to a potential Rocket.Chat server to send notifications about the updates to. | unset |
| `system_update__update_enabled` | Enables or disables the system-update timer, analogous to `systemctl enable/disable --now`.  | `true` |
| `system_update__update_time` | The time when to actually execute the updates (and automatically reboot if necessary), relative to `system_update__notify_and_schedule_on_calendar`. | `04:00 + 1 days'` |

Example:
```yaml
# optional
system_update__icinga2_api_url: 'https://icinga.example.com:5665'
system_update__icinga2_api_user_login:
  username: 'downtime-user'
  password: 'linuxfabrik'
system_update__icinga2_hostname: 'myhost.example.com'
system_update__mail_from: 'noreply@example.com'
system_update__mail_recipients_new_configfiles:
  - 'info@example.com'
  - 'support@example.com'
system_update__mail_recipients_updates:
  - 'info@example.com'
  - 'support@example.com'
system_update__mail_subject_prefix: '001-'
system_update__notify_and_schedule_on_calendar: 'mon 10:00'
system_update__post_update_code: |-
  VAR='hello world'
  echo $VAR
system_update__rocketchat_msg_suffix: '@administrator'
system_update__rocketchat_url: 'https://chat.example.com/hooks/abcd1234'
system_update__update_enabled: true
system_update__update_time: '04:00 + 1 days'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
