# Ansible Role linuxfabrik.lfops.chromium_headless

This role installs the headless [Chromium](https://www.chromium.org/) shell together with the runtime libraries and fonts required for headless rendering, and sets up a socket-activated `chromium-headless` systemd service. Clients connect to a configurable TCP socket; Chromium is started on the first request via `systemd-socket-proxyd` and stopped again after a configurable idle timeout, so no RAM is wasted while the backend is unused.

The setup is used as a headless browser backend for tools such as the [Icinga Web 2 PDF Export Module](https://github.com/Icinga/icingaweb2-module-pdfexport).


*Available since LFOps `6.0.2`.*


## How the Role Behaves

* Three systemd units are deployed:
    * `chromium-headless-proxy.socket` listens on `listen_address:listen_port` (default `127.0.0.1:9222`).
    * `chromium-headless-proxy.service` runs `systemd-socket-proxyd`, which bridges the activated socket to Chromium (Chromium itself does not implement the systemd socket-activation protocol), forwarding traffic to `backend_port` (default `9223`). On `idle_timeout` seconds without traffic it exits. On EL8 (systemd 239) the underlying `--exit-idle-time` option does not exist, so the idle shutdown is skipped there and the backend stays resident once activated; on-demand start still works.
    * `chromium-headless.service` runs the actual Chromium process under the `chromium` system user. Its start job is held until Chromium's debugging port actually accepts connections, so the proxy (ordered after it) never races ahead and fails the first request. It is bound to the proxy via `BindsTo=`, so when the proxy exits on idle, Chromium stops too; the SIGTERM-triggered exit is treated as clean so this does not mark the unit failed. It is **not** enabled on boot and must not be started directly. The proxy triggers it via `Requires=`.
* On SELinux-enforcing hosts, two booleans are enabled: `systemd_socket_proxyd_bind_any` so the `chromium-headless-proxy.socket` unit may bind the listen port even when it carries an unexpected SELinux port type (on Rocky/RHEL 9 the default `9222` is registered as `hplip_port_t`), and `systemd_socket_proxyd_connect_any` so the proxy may connect to Chromium's non-standard backend port.
* The service-lifecycle variables (`chromium_headless__service_enabled`, `__service_state`) manage the `chromium-headless-proxy.socket` unit, not the Chromium service directly.


## Mandatory Requirements

* Enable the EPEL repository, which provides `chromium-headless`. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.

If you use the [Chromium Headless Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/chromium_headless.yml), this is automatically done for you.


## Tags

`chromium_headless`

* Creates the `chromium` system user and group.
* Installs Chromium along with the required runtime libraries and fonts.
* Sets the `systemd_socket_proxyd_bind_any` and `systemd_socket_proxyd_connect_any` SELinux booleans.
* Deploys all three systemd units (`chromium-headless-proxy.socket`, `chromium-headless-proxy.service`, `chromium-headless.service`).
* Ensures the `chromium-headless-proxy.socket` is in the desired state.
* Triggers: daemon-reload on any unit-file change; socket restart only on `chromium-headless-proxy.socket` changes. Changes to the proxy or Chromium service unit file take effect on the next socket-activation cycle.

`chromium_headless:configure`

* Deploys the three systemd units (`chromium-headless-proxy.socket`, `chromium-headless-proxy.service`, `chromium-headless.service`).
* Triggers: daemon-reload on any unit-file change; socket restart only on `chromium-headless-proxy.socket` changes. Changes to the proxy or Chromium service unit file take effect on the next socket-activation cycle.

`chromium_headless:state`

* Manages the `chromium-headless-proxy.socket` state (start, stop, enable, disable).
* Triggers: none.


## Optional Role Variables

`chromium_headless__backend_port`

* Internal port Chromium itself listens on. The proxy forwards traffic from `listen_port` to this port. Only meaningful to change if `listen_port` and `backend_port` would otherwise collide.
* Type: Number.
* Default: `9223`

`chromium_headless__extra_args__host_var` / `chromium_headless__extra_args__group_var`

* Additional Chromium CLI flags appended to the `ExecStart` line of `chromium-headless.service`, in the order listed. Useful for tuning behavior without overwriting the whole unit.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. The CLI flag, including any leading dashes and value (e.g. `--window-size=1920,1080`).
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`chromium_headless__idle_timeout`

* Seconds the `systemd-socket-proxyd` waits without active connections before exiting. When it exits, the bound `chromium-headless.service` stops automatically. The next inbound connection re-activates the whole chain, paying ~1-2 seconds of cold-start latency. Has no effect on EL8, whose systemd (239) lacks the `--exit-idle-time` option; the backend stays resident there.
* Type: Number.
* Default: `300`

`chromium_headless__listen_address`

* Address the `chromium-headless-proxy.socket` binds to. Chromium's own debugging port always stays on `127.0.0.1` regardless of this setting, so only the proxy is reachable here. Keep this on `127.0.0.1` unless you intentionally want to expose the proxy to other hosts; it enforces neither TLS nor authentication.
* Type: String.
* Default: `'127.0.0.1'`

`chromium_headless__listen_port`

* Port the proxy socket listens on. This is the endpoint clients connect to.
* Type: Number.
* Default: `9222`

`chromium_headless__service_enabled`

* Enables or disables the `chromium-headless-proxy.socket` at boot, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`chromium_headless__service_state`

* Changes the state of the `chromium-headless-proxy.socket`, analogous to `systemctl start/stop/restart/reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'`

`chromium_headless__user_data_dir`

* Home directory of the `chromium` system user and Chromium user data directory. Used both as the user's `home`, as the `--user-data-dir` value for Chromium, and as the writable path exposed via systemd `ReadWritePaths=`.
* Type: String.
* Default: `'/var/lib/chromium-headless'`

Example:
```yaml
# optional
chromium_headless__backend_port: 9223
chromium_headless__extra_args__host_var:
  - name: '--window-size=1920,1080'
  - name: '--lang=de-CH'
chromium_headless__idle_timeout: 600
chromium_headless__listen_address: '127.0.0.1'
chromium_headless__listen_port: 9222
chromium_headless__service_enabled: true
chromium_headless__service_state: 'started'
chromium_headless__user_data_dir: '/var/lib/chromium-headless'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
