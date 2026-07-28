# Ansible Role linuxfabrik.lfops.system_update

This role configures the server to do system updates. A weekly regular lane applies all available updates, and on Rocky Linux a daily security lane applies only security hot-fixes from the dedicated `security` repository. Both run at one configurable maintenance window per host and reboot the host afterwards if an update requires it. A `notify-and-schedule` script informs the administrators (via email or [Rocket.Chat](https://rocket.chat/)) when and which updates are pending.

Reboots are not performed by the update scripts themselves. They are delegated to the [schedule_reboot](https://github.com/Linuxfabrik/lfops/tree/main/roles/schedule_reboot) role: an update that needs a reboot drops a request into that role's spool, and `schedule_reboot` reboots the host once, at the window.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* **Updates run at the reboot window.** The regular lane (weekly) and the Rocky security lane (daily) both run at the maintenance window defined by `schedule_reboot__reboot_time__*` (the [schedule_reboot](https://github.com/Linuxfabrik/lfops/tree/main/roles/schedule_reboot) role). When an update needs a reboot it drops a request into that role's spool; the update unit is ordered before the reboot actor, so the reboot waits for the update to finish before it runs.
* **The security lane is enabled by default, but a no-op without the `security` repository.** That repository is provided by the [repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos) role. On hosts where it is not present, the security lane installs nothing and requests no reboot. Turn the lane off entirely with `system_update__security_enabled: false`.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* Optional: the root mail aliases are configured (role: [linuxfabrik.lfops.mailto_root](https://github.com/Linuxfabrik/lfops/tree/main/roles/mailto_root)).
* Optional: postfix provides the `sendmail` interface and mail relay used for the notifications (role: [linuxfabrik.lfops.postfix](https://github.com/Linuxfabrik/lfops/tree/main/roles/postfix)).
* The reboot mechanism must be present (role: [linuxfabrik.lfops.schedule_reboot](https://github.com/Linuxfabrik/lfops/tree/main/roles/schedule_reboot)). It owns the reboot window (`schedule_reboot__reboot_time__*`) and performs the reboot an update requests.
* Optional: yum-utils is installed on RHEL (role: [linuxfabrik.lfops.yum_utils](https://github.com/Linuxfabrik/lfops/tree/main/roles/yum_utils)).


## Requirements

Manual steps:

* On Debian, install needrestart by running the [apps](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/apps.yml) playbook (role: [linuxfabrik.lfops.apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps)).


## Tags

`system_update`

* Deploys the notify-and-schedule and update-and-reboot scripts and their systemd timers/services. On Rocky Linux hosts it also deploys the security-update lane.
* Triggers: none.

`system_update:state`

* Determines whether the notify-and-schedule, update-and-reboot and (Rocky) security-update timers are enabled.
* Triggers: none.


## Optional Role Variables

`system_update__cache_only`

* Whether to install updates from cache only. This implies to have the cache built beforehand.
* Type: Bool.
* Default: `false`

`system_update__mail_from`

* The email sender account. This will be used as the "from"-address for all notifications.
* Type: String.
* Default: `'{{ mailto_root__from }}'`

`system_update__mail_recipients_new_configfiles`

* A list of email recipients to notify if there is a new version of a config file (`rpmnew` / `rpmsave` / `dpkg-dist` / `ucf-dist`).
* Type: String.
* Default: `'{{ mailto_root__to }}'`

`system_update__mail_recipients_updates`

* A list of email recipients to notify about the expected updates and the report of the installed updates.
* Type: String.
* Default: `'{{ mailto_root__to }}'`

`system_update__mail_subject_hostname`

* String which will be used as the hostname in the mail subject. You can use `$()` to call bash code.
* Type: String.
* Default: `'$(hostname --short)'`

`system_update__mail_subject_prefix`

* This will set a prefix that will be showed in front of the hostname. Can be used to separate servers by environment or customer.
* Type: String.
* Default: `''`

`system_update__notify_and_schedule_on_calendar`

* When the informational "updates pending" notification is sent. This is purely a heads-up; the update is applied later at the maintenance window. By default it is sent at 10:00 on the day before `system_update__update_day`, so it always arrives before the update runs. If you set a multi-day or date-based `system_update__update_day`, set this explicitly. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format.
* Type: String.
* Default: 10:00 on the day before `system_update__update_day` (for example `'Mon 10:00'` when the update day is `Tue`)

`system_update__post_update_code`

* This codeblock will be executed after the updates have been installed and before a potential reboot.
* Type: String.
* Default: unset

`system_update__pre_update_code`

* This codeblock will be executed before the update process is started. Can be used to check pre-conditions for updating, for example for checking cluster nodes.
* Type: String.
* Default: unset

`system_update__rocketchat_msg_suffix`

* A suffix to the Rocket.Chat notifications. This can be used to mention other users.
* Type: String.
* Default: `''`

`system_update__rocketchat_url`

* The URL to a potential Rocket.Chat server to send notifications about the updates to.
* Type: String.
* Default: unset

`system_update__security_enabled`

* Enables or disables the security lane (the `security-update` timer), analogous to `systemctl enable/disable --now`. Rocky Linux only. When enabled but the `security` repository is not enabled on the host, the lane is a no-op.
* Type: Bool.
* Default: `true`

`system_update__security_on_calendar`

* When the security lane checks for and installs security hot-fixes. Defaults to the reboot window (`schedule_reboot__reboot_time__*`) so the reboot follows right after. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format.
* Type: String.
* Default: `'*-*-* {{ schedule_reboot__reboot_time__combined_var | d("04:00") }}'`

`system_update__security_repos`

* The repositories the security lane installs from. All other repositories are disabled for the security transaction, keeping it separate from the regular update lane.
* Type: List.
* Default: `['security']`

`system_update__update_day`

* The weekday on which the regular (weekly) update lane runs. Combined with the maintenance window to build the timer schedule, for example `Tue 04:00`. Defaults to `Tue` so the Monday notification (`system_update__notify_and_schedule_on_calendar`) arrives before the update. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format.
* Type: String.
* Default: `'Tue'`

`system_update__update_enabled`

* Enables or disables the regular update lane (the notify-and-schedule and update-and-reboot timers), analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

Example:
```yaml
# optional
system_update__cache_only: true
system_update__mail_from: 'noreply@example.com'
system_update__mail_recipients_new_configfiles:
  - 'info@example.com'
  - 'support@example.com'
system_update__mail_recipients_updates:
  - 'info@example.com'
  - 'support@example.com'
system_update__mail_subject_hostname: '$(hostname --long)'
system_update__mail_subject_prefix: '001-'
system_update__notify_and_schedule_on_calendar: 'mon *-*-01..07 10:00' # first monday of the month
system_update__post_update_code: |-
  VAR='hello world'
  echo $VAR
system_update__pre_update_code: |-
  check_dns() {
    local DNS_SERVER=$1
    if ! dig @$DNS_SERVER linuxfabrik.ch +short > /dev/null; then
        SUBJECT="$SUBJECT_PREFIX - System update failed"
        MSGBODY="DNS Server $DNS_SERVER failed to respond. Aborting update."
        send_msg
        exit 1
    fi
  }
  check_dns 192.0.2.10
  check_dns 192.0.2.11
system_update__rocketchat_msg_suffix: '@administrator'
system_update__rocketchat_url: 'https://chat.example.com/hooks/abcd1234'
system_update__security_enabled: true
system_update__security_repos:
  - 'security'
system_update__update_day: 'Tue'
system_update__update_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
