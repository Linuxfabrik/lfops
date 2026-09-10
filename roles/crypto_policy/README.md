# Ansible Role linuxfabrik.lfops.crypto_policy

On Red Hat-family systems, `update-crypto-policies` is a system-wide switch that picks the allowed TLS / SSH / IPsec / Kerberos algorithm sets for *all* crypto-aware services in one place (e.g. `DEFAULT`, `LEGACY`, `FUTURE`, `FIPS`). This role sets that policy and additionally ships custom sub-policies defined by Linuxfabrik, e.g. to support CIS hardening.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

`update-crypto-policies --set` rewrites the configuration the crypto libraries read, but every process that is already running keeps the algorithm set it started with. The host is therefore in a mixed state until it is restarted, which is what the command itself says: "System-wide crypto policies are applied on application start-up. It is recommended to restart the system for the change of policies to fully take place."

When the [schedule_reboot](https://github.com/Linuxfabrik/lfops/tree/main/roles/schedule_reboot) mechanism is deployed, a changed policy therefore requests a reboot at the next maintenance window (spool entry `crypto_policy`). Without it, the role only prints a message and leaves the reboot to the operator. A run against a host that already carries the configured policy changes nothing and requests nothing.

`lfops__reboot_now` makes the role reboot in the same run instead of waiting for the window. The reboot still goes through the same mechanism, so the notification mail, the Icinga downtime and the grace period all apply, and a reboot another role requested earlier in the run is carried out together with this one. The role then waits for the host to come back before the play continues. Have a look at the [README](https://github.com/Linuxfabrik/lfops/blob/main/README.md#lfops__reboot_now). With the variable set on a host where the `schedule_reboot` mechanism is missing, the run aborts rather than reporting a reboot it cannot perform.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* Optional: the reboot mechanism should be in place (role: [linuxfabrik.lfops.schedule_reboot](https://github.com/Linuxfabrik/lfops/tree/main/roles/schedule_reboot)), so a changed policy reboots the host at the maintenance window instead of waiting for a manual reboot.


## Tags

`crypto_policy`

* Sets the system crypto policy.
* Requests a reboot when the policy changed, or performs it in the same run when `lfops__reboot_now` is set.
* Triggers: none.


## Optional Role Variables

`crypto_policy__policy`

* The crypto policy to activate. See `roles/crypto_policy/templates/etc/crypto-policies/policies/modules/` for a list of available crypto policies. Example: `DEFAULT:LINUXFABRIK-NO-SHA1:LINUXFABRIK-SSH-NO-CBC`
* Type: String.
* Default:
    * RedHat8: `'DEFAULT:LINUXFABRIK-NO-SHA1:LINUXFABRIK-NO-WEAKMAC:LINUXFABRIK-SSH-NO-CBC:LINUXFABRIK-SSH-NO-CHACHA20'`
    * RedHat9: `'DEFAULT:LINUXFABRIK-NO-SHA1:LINUXFABRIK-NO-WEAKMAC:LINUXFABRIK-SSH-NO-CBC:LINUXFABRIK-SSH-NO-CHACHA20:LINUXFABRIK-SSH-NO-ETM'`
    * RedHat10: `'DEFAULT:LINUXFABRIK-NO-SHA1:LINUXFABRIK-NO-WEAKMAC:LINUXFABRIK-SSH-NO-CBC:LINUXFABRIK-SSH-NO-CHACHA20:LINUXFABRIK-SSH-NO-ETM'`

Example:
```yaml
# optional
crypto_policy__policy: 'DEFAULT:LINUXFABRIK-NO-SHA1:LINUXFABRIK-NO-WEAKMAC:LINUXFABRIK-SSH-NO-CBC:LINUXFABRIK-SSH-NO-CHACHA20:LINUXFABRIK-SSH-NO-ETM'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
