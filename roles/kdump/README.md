# Ansible Role linuxfabrik.lfops.kdump

[kdump](https://docs.kernel.org/admin-guide/kdump/kdump.html) is the Linux kernel crash-dump mechanism: when the running kernel panics, a pre-loaded "capture kernel" boots and writes a `vmcore` file to disk for post-mortem analysis. The capture kernel needs RAM permanently reserved at boot via the `crashkernel=` cmdline option, which is wasted on most production servers. By default this role stops and disables `kdump.service` so the daemon no longer runs; set `kdump__service_enabled: true` to turn kdump on instead. The `crashkernel=` reservation itself is not touched, see "How the Role Behaves".


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* When kdump is to run, meaning `kdump__service_enabled: true` or a `kdump__service_state` other than `stopped`, the role installs the package that ships `kdump.service`: `kdump-utils` on RHEL 10, `kexec-tools` on RHEL 8 and 9. With kdump off it installs nothing, and a host without the unit counts as having kdump off already.
* When kdump is to run and its service cannot be managed, the run fails.
* kdump only starts once memory is reserved for the capture kernel with `crashkernel=` on the kernel command line, and a reservation takes effect at the next boot. The role does not set it. Either run `kdumpctl reset-crashkernel --kernel=ALL` once, which writes the distribution's default, or set `crashkernel` through `bootloader__cmdline_options__host_var` / `bootloader__cmdline_options__group_var` of the [bootloader](https://github.com/Linuxfabrik/lfops/tree/main/roles/bootloader) role, then reboot. Until then, starting kdump fails.


## Tags

`kdump`

* Installs the kdump package when kdump is to run, and manages the state of `kdump.service`.
* Triggers: none.


## Optional Role Variables

`kdump__service_enabled`

* Enables or disables the kdump service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `false`

`kdump__service_state`

* Changes the state of the kdump service, analogous to `systemctl start/stop/restart/reload`. Possible options:

    * `started`
    * `stopped`
    * `restarted`
    * `reloaded`

* Type: String.
* Default: `'stopped'`

Example:
```yaml
# optional
kdump__service_enabled: false
kdump__service_state: 'stopped'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
