# Ansible Role linuxfabrik.lfops.kdump

[kdump](https://docs.kernel.org/admin-guide/kdump/kdump.html) is the Linux kernel crash-dump mechanism: when the running kernel panics, a pre-loaded "capture kernel" boots and writes a `vmcore` file to disk for post-mortem analysis. The capture kernel needs RAM permanently reserved at boot via the `crashkernel=` cmdline option, which is wasted on most production servers. This role stops and disables the `kdump.service` so the daemon no longer runs; the `crashkernel=` reservation itself is *not* touched (use the `kernel_settings` role for that).


## Tags

`kdump`

* Stops and disables the `kdump` service.
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
