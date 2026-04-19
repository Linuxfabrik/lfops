# Ansible Role linuxfabrik.lfops.keepalived

This role installs and configures [keepalived](https://www.keepalived.org/).


## Scope

The role intentionally covers a minimal VRRP setup:

* Deploys exactly one `vrrp_instance` (`VI_{{ keepalived__instance_id }}`) with a single
  `virtual_ipaddress`.
* PASS authentication (`auth_type PASS`) between MASTER and BACKUP. Note that keepalived
  only evaluates the first eight characters of the password.
* Priorities: `255` for MASTER, `200` for BACKUP.
* `smtp_alert` for notifications; no `notify_*` hooks.
* No tracking (no `track_process`, `track_file`, `track_interface` or `track_script`).

It does **not**:

* Set the `net.ipv4.ip_nonlocal_bind = 1` sysctl that services binding to the VIP typically
  need. Use [linuxfabrik.lfops.kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings)
  or set it manually.
* Open the firewall for VRRP (IP protocol 112). Use [linuxfabrik.lfops.firewall](https://github.com/Linuxfabrik/lfops/tree/main/roles/firewall)
  or similar.

For advanced setups (multiple VIPs, tracking-based priority adjustments, `notify_*` hooks),
override the template in your own role or extend `/etc/keepalived/keepalived.conf`
manually.


## Tags

`keepalived`

* Installs and configures keepalived.
* Triggers: keepalived.service restart.

`keepalived:state`

* Manages the state of the keepalived service.
* Triggers: none.


## Mandatory Role Variables

`keepalived__notification_email_addresses`

* The email addresses for notifications.
* Type: List.
* Default: none

`keepalived__password`

* The password for the communication between the MASTER and BACKUP instances. Only the first eight (8) characters are used.
* Type: String.
* Default: none

`keepalived__state`

* Determines whether to be the MASTER or BACKUP.
* Type: String.
* Default: none

`keepalived__virtual_ipaddress`

* The IP address to be shared between the MASTER and BACKUP.
* Type: String.
* Default: none

Example:
```yaml
# mandatory
keepalived__notification_email_addresses:
  - 'root@example.com'
keepalived__password: 'linuxfabrik'
keepalived__state: 'MASTER'
keepalived__virtual_ipaddress: '192.0.2.1'
```


## Optional Role Variables

`keepalived__instance_id`

* The vrrp instance id keepalived should use.
* Type: Number.
* Default: `1`

`keepalived__interface`

* The network interface keepalived should use.
* Type: String.
* Default: `'{{ ansible_facts["default_ipv4"]["interface"] }}'`

`keepalived__notification_email_from`

* The email address keepalived should use as the sender address for email notifications.
* Type: String.
* Default: `'root@{{ ansible_facts["nodename"] }}'`

`keepalived__service_enabled`

* Enables or disables the keepalived service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`keepalived__smtp_server`

* The SMTP server keepalived should use in order to send email notifications.
* Type: String.
* Default: `'localhost'`

`keepalived__virtual_router_id`

* The virtual router id.
* Type: Number.
* Default: `'{{ keepalived__instance_id }}'`

Example:
```yaml
# optional
keepalived__instance_id: 1
keepalived__interface: 'eth'
keepalived__notification_email_from: 'root@server.loc'
keepalived__service_enabled: true
keepalived__smtp_server: 'smtp.example.com'
keepalived__virtual_router_id: 1
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
