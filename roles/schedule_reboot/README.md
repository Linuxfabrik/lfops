# Ansible Role linuxfabrik.lfops.schedule_reboot

This role provides a single, windowed reboot mechanism for a host. A reboot is requested by dropping a file into a spool directory (`/run/schedule-reboot/`), and one `do-reboot` actor, triggered by a systemd timer at a configurable maintenance window, performs a single reboot for all pending requests. An ad-hoc `schedule-reboot` command is available to request a reboot after a manual change.

Other roles reuse this mechanism instead of rebooting themselves: they drop a request file and let this role reboot the host once, at the window. The [system_update](https://github.com/Linuxfabrik/lfops/tree/main/roles/system_update) role works this way.


*Available in the next LFOps release.*


## How the Role Behaves

* **One reboot window.** `schedule_reboot__reboot_time__*` sets a single time of day at which the actor runs. Steer it per inventory group, for example an earlier window for infrastructure hosts so they reboot before the rest.
* **Reboots are modelled as state.** A pending reboot is a file in `/run/schedule-reboot/`; the file name is a category and its content is included in the notification mail. Several pending reasons coalesce into a single reboot. The spool lives on tmpfs, so it clears on the reboot itself.
* **Producers order themselves before the actor.** A role that runs work at the same window (such as a system update) declares its unit `Before=schedule-reboot.service` (order-only, no `Wants=`/`Requires=`). systemd then runs the reboot only after that work finishes; on a window where no producer runs, the actor runs alone and reboots only if a request is pending.
* **An Icinga downtime is set around the reboot.** When `schedule_reboot__icinga2_api_user_login` is set, the actor schedules a short host downtime before rebooting, so the reboot does not raise alerts. Without it, the reboot happens without a downtime.

To request a reboot from a script or by hand:

```bash
schedule-reboot <reason> [detail ...]         # request a reboot at the next window
schedule-reboot --now <reason> [detail ...]   # reboot as soon as any running producer finishes
```

To request a reboot from another role's deployed script, write a file directly:

```bash
printf '%s\n' "kernel updated" > /run/schedule-reboot/my_role
```


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* Optional: the root mail aliases are configured (role: [linuxfabrik.lfops.mailto_root](https://github.com/Linuxfabrik/lfops/tree/main/roles/mailto_root)).
* Optional: postfix provides the `sendmail` interface and mail relay used for the reboot notification (role: [linuxfabrik.lfops.postfix](https://github.com/Linuxfabrik/lfops/tree/main/roles/postfix)).


## Tags

`schedule_reboot`

* Deploys the `schedule-reboot` CLI, the `do-reboot` actor, the systemd timer/service, and the `/run/schedule-reboot` spool directory.
* Triggers: none.

`schedule_reboot:state`

* Determines whether the schedule-reboot timer is enabled.
* Triggers: none.


## Optional Role Variables

`schedule_reboot__enabled`

* Whether the schedule-reboot timer is enabled at boot, analogous to `systemctl enable / disable --now`. Disabling it stops scheduled reboots; `schedule-reboot --now` still works.
* Type: Bool.
* Default: `true`

`schedule_reboot__icinga2_api_url`

* The URL of the Icinga2 API (usually on the Icinga2 Master). Used to set a downtime for the host and all its services around the reboot.
* Type: String.
* Default: `'https://{{ icinga2_agent__icinga2_master_host | d("") }}:{{ icinga2_agent__icinga2_master_port | d(5665) }}'`

`schedule_reboot__icinga2_api_user_login`

* The Icinga2 API user used to set the downtime around the reboot. When unset, no downtime is scheduled.
* Type: Dictionary.
* Default: unset
* Subkeys:

    * `username`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Mandatory. Password.
        * Type: String.

`schedule_reboot__icinga2_hostname`

* The hostname of the Icinga2 host on which the downtime should be set.
* Type: String.
* Default: `'{{ ansible_facts["nodename"] }}'`

`schedule_reboot__mail_from`

* The email sender account, used as the "from" address for the reboot notification.
* Type: String.
* Default: `'{{ mailto_root__from }}'`

`schedule_reboot__mail_recipients`

* A list of email recipients for the reboot notification.
* Type: List of strings.
* Default: `'{{ mailto_root__to }}'`

`schedule_reboot__mail_subject_hostname`

* String used as the hostname in the mail subject. You can use `$()` to call bash code.
* Type: String.
* Default: `'$(hostname --short)'`

`schedule_reboot__mail_subject_prefix`

* A prefix shown in front of the hostname in the mail subject. Can be used to separate servers by environment or customer.
* Type: String.
* Default: `''`

`schedule_reboot__on_calendar`

* When the reboot actor runs. It reboots only if a request is pending in `/run/schedule-reboot/`. Defaults to daily at the reboot window. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format.
* Type: String.
* Default: `'*-*-* {{ schedule_reboot__reboot_time__combined_var }}'`

`schedule_reboot__reboot_grace_period`

* The number of seconds to wait after sending the reboot notification before the host actually reboots. This gives the notification mail time to leave the local mail queue (which is persistent, so the mail is never lost, but otherwise the heads-up can arrive after the host is already back). The host keeps serving during the wait. Set to `0` to reboot immediately.
* Type: Integer.
* Default: `60`

`schedule_reboot__reboot_time__host_var` / `schedule_reboot__reboot_time__group_var`

* The reboot window: the time of day at which the actor (and the producers ordered before it) run. Steer it per inventory group. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format.
* Type: String.
* Default: `'04:00'`

`schedule_reboot__rocketchat_msg_suffix`

* A suffix to the Rocket.Chat notification. This can be used to mention other users.
* Type: String.
* Default: `''`

`schedule_reboot__rocketchat_url`

* The URL to a Rocket.Chat server to send the reboot notification to.
* Type: String.
* Default: unset

Example:
```yaml
# optional
schedule_reboot__enabled: true
schedule_reboot__icinga2_api_url: 'https://icinga.example.com:5665'
schedule_reboot__icinga2_api_user_login:
  username: 'downtime-user'
  password: 'linuxfabrik'
schedule_reboot__icinga2_hostname: 'myhost.example.com'
schedule_reboot__mail_from: 'noreply@example.com'
schedule_reboot__mail_recipients:
  - 'info@example.com'
  - 'support@example.com'
schedule_reboot__mail_subject_prefix: '001-'
schedule_reboot__reboot_grace_period: 60
schedule_reboot__reboot_time__group_var: '19:00'
schedule_reboot__rocketchat_msg_suffix: '@administrator'
schedule_reboot__rocketchat_url: 'https://chat.example.com/hooks/abcd1234'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
