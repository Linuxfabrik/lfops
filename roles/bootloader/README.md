# Ansible Role linuxfabrik.lfops.bootloader

This role manages the kernel command line of a host, for parameters that only take effect at boot time.

On the Red Hat family the boot entries are written with `grubby`. Debian and Ubuntu do not package `grubby`, so there the role deploys a GRUB drop-in of its own and regenerates the boot loader configuration.


*Available in the next LFOps release.*


## How the Role Behaves

* Red Hat family: options are applied to every boot entry of the host (`grubby --update-kernel=ALL`), so the running kernel and every kernel still installed alongside it carry the same command line. `grubby` keeps `GRUB_CMDLINE_LINUX` in `/etc/default/grub` in sync while doing so, appending only the managed options and leaving the rest of the file alone. Nothing else in `/etc/default/grub` and nothing in `grub.cfg` is touched.
* Debian family: the options are written to `/etc/default/grub.d/z00-lfops.cfg` and `update-grub` regenerates `/boot/grub/grub.cfg` from it. `grub-mkconfig` sources `/etc/default/grub` first and every `/etc/default/grub.d/*.cfg` after it, so the drop-in wins without the packaged configuration file ever being edited, and it appends to whatever `GRUB_CMDLINE_LINUX` already holds instead of replacing it (the sourcing order was read from the `grub-mkconfig` of grub-common 2.12-9+deb13u2 on Debian 13, 2.12-1ubuntu7.3 on Ubuntu 24.04 and 2.14-2ubuntu2.1 on Ubuntu 26.04). Once no option is left to set, the drop-in is removed instead of being left behind empty.
* A configured option counts as present only when **every** boot entry carries it, and it is compared as a whole word with the option escaped, so an option containing a dot matches a dot.
* A run against a host that already carries the configured command line changes nothing and reports no change, and it neither requests a reboot nor touches any file. Changing the value of an option that is already set replaces it rather than adding a second one.
* `--check` changes nothing. The dry run reads the current boot entries and reports what it would add or remove.
* The change only takes effect on the next boot. When the [schedule_reboot](https://github.com/Linuxfabrik/lfops/tree/main/roles/schedule_reboot) mechanism is deployed, a changed command line requests a reboot at the next maintenance window (spool entry `bootloader`). Without it, the role only prints a message and leaves the reboot to the operator.
* On the Red Hat family a kernel installed later inherits the command line from the running kernel. `kernel-install` builds the boot entry of a new kernel from `/etc/kernel/cmdline`, from `/usr/lib/kernel/cmdline`, or, when neither exists, from `/proc/cmdline` of the running kernel (verified against `/usr/lib/kernel/install.d/20-grub.install` on Rocky 9). A kernel installed between the change and the reboot therefore still comes up without the new options; run the role again afterwards. On the Debian family this cannot happen, because installing a kernel regenerates `/boot/grub/grub.cfg` from the drop-in.
* The role manages the kernel command line only. It does not add, remove or reorder boot entries, does not change the boot loader timeout, and does not manage the GRUB password.


## Known Limitations

* GRUB 2 only. Hosts booted by zipl or systemd-boot are not supported.
* Debian family: `state: 'absent'` only drops an option from the command line this role writes. An option that comes from `/etc/default/grub` or from another drop-in stays, because the role never edits files it does not own. On the Red Hat family the same option is removed with `grubby --remove-args`.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* Optional: the reboot mechanism should be in place (role: [linuxfabrik.lfops.schedule_reboot](https://github.com/Linuxfabrik/lfops/tree/main/roles/schedule_reboot)), so a changed kernel command line reboots the host at the maintenance window instead of waiting for a manual reboot.


## Requirements

* The host is booted by GRUB 2.
* Red Hat family: `grubby` is installed. It is part of every GRUB installation there, since `kernel-install` relies on it.
* Debian family: `grub2-common` is installed. It provides `update-grub`, which the role calls.


## Tags

`bootloader`

* Configures the kernel command line.
* Requests a reboot when the kernel command line changed.
* Triggers: none.


## Optional Role Variables

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

`bootloader__cmdline_options__host_var` / `bootloader__cmdline_options__group_var`

* Kernel command line options. An option that is already present with a different value is overwritten. On the Debian family the options end up in `GRUB_CMDLINE_LINUX`, so they apply to the recovery entries as well.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the option, for example `psi`.
        * Type: String.

    * `value`:

        * Optional. Value of the option. Omit it for options that stand on their own, for example `quiet`. Quote a value YAML reads as a boolean, `'on'` and `'off'` among them, otherwise it reaches the command line as `True` or `False`.
        * Type: String or Number.

    * `state`:

        * Optional. Whether the option is added to or removed from the kernel command line. One of `present` or `absent`. On the Debian family see "Known Limitations".
        * Type: String.
        * Default: `'present'`

Example:
```yaml
# optional
bootloader__cmdline_options__group_var:
  - name: 'psi'
    value: 1
  - name: 'quiet'
  - name: 'nosmt'
    state: 'absent'
```


## Troubleshooting

**The option is configured, but `/proc/cmdline` does not contain it**

* The host has not been rebooted since the change. Check the boot entries with `grubby --info=ALL` respectively `grep linux /boot/grub/grub.cfg`; they carry the new command line right away, `/proc/cmdline` only after the reboot.

**On a Red Hat-family host a newly installed kernel boots without the configured options**

* The kernel was installed while the change was still pending a reboot, so it inherited the command line of the running kernel. Run the role again to update the entry of the new kernel.

**On a Debian-family host an option is still on the command line although it is set to `state: 'absent'`**

* The option comes from `/etc/default/grub` or from another drop-in in `/etc/default/grub.d/`, which this role does not touch. Remove it there.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
