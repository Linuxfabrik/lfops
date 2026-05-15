# Ansible Role linuxfabrik.lfops.google_chrome

This role installs [Google Chrome](https://www.google.com/chrome/) together with the runtime libraries and fonts required for headless rendering, and sets up a socket-activated `chrome-headless` systemd service. Clients connect to a configurable TCP socket; Chrome is started on the first request via `systemd-socket-proxyd` and stopped again after a configurable idle timeout, so no RAM is wasted while the backend is unused.

The setup is used as a headless browser backend for tools such as the [Icinga Web 2 PDF Export Module](https://github.com/Icinga/icingaweb2-module-pdfexport).


*Available since LFOps `6.0.2`.*


## How the Role Behaves

* Three systemd units are deployed:
    * `chrome-headless-proxy.socket` listens on `listen_address:listen_port` (default `127.0.0.1:9222`).
    * `chrome-headless-proxy.service` runs `systemd-socket-proxyd`, which bridges the activated socket to Chrome (Chrome itself does not implement the systemd socket-activation protocol), forwarding traffic to `backend_port` (default `9223`). On `idle_timeout` seconds without traffic it exits.
    * `chrome-headless.service` runs the actual Chrome process under the `chrome` system user. It is bound to the proxy via `BindsTo=`, so when the proxy exits on idle, Chrome stops too. It is **not** enabled on boot and must not be started directly — the proxy triggers it via `Requires=`.
* On SELinux-enforcing hosts, two booleans are enabled: `systemd_socket_proxyd_bind_any` so the `chrome-headless-proxy.socket` unit may bind the listen port even when it carries an unexpected SELinux port type (on Rocky/RHEL 9 the default `9222` is registered as `hplip_port_t`), and `systemd_socket_proxyd_connect_any` so the proxy may connect to Chrome's non-standard backend port.
* The service-lifecycle variables (`google_chrome__service_enabled`, `__service_state`) manage the `chrome-headless-proxy.socket` unit, not the Chrome service directly.


## Mandatory Requirements

* Enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Enable the Google Chrome repository. This can be done using the [linuxfabrik.lfops.repo_google_chrome](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_google_chrome) role.

If you use the [Google Chrome Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/google_chrome.yml), this is automatically done for you.


## Tags

`google_chrome`

* Creates the `chrome` system user and group.
* Installs Google Chrome along with the required runtime libraries and fonts.
* Sets the `systemd_socket_proxyd_bind_any` and `systemd_socket_proxyd_connect_any` SELinux booleans.
* Deploys all three systemd units (`chrome-headless-proxy.socket`, `chrome-headless-proxy.service`, `chrome-headless.service`).
* Ensures the `chrome-headless-proxy.socket` is in the desired state.
* Triggers: daemon-reload on any unit-file change; socket restart only on `chrome-headless-proxy.socket` changes. Changes to the proxy or Chrome service unit file take effect on the next socket-activation cycle.

`google_chrome:configure`

* Deploys the three systemd units (`chrome-headless-proxy.socket`, `chrome-headless-proxy.service`, `chrome-headless.service`).
* Triggers: daemon-reload on any unit-file change; socket restart only on `chrome-headless-proxy.socket` changes. Changes to the proxy or Chrome service unit file take effect on the next socket-activation cycle.

`google_chrome:state`

* Manages the `chrome-headless-proxy.socket` state (start, stop, enable, disable).
* Triggers: none.


## Optional Role Variables

`google_chrome__backend_port`

* Internal port Chrome itself listens on. The proxy forwards traffic from `listen_port` to this port. Only meaningful to change if `listen_port` and `backend_port` would otherwise collide.
* Type: Number.
* Default: `9223`

`google_chrome__extra_args__host_var` / `google_chrome__extra_args__group_var`

* Additional Chrome CLI flags appended to the `ExecStart` line of `chrome-headless.service`, in the order listed. Useful for tuning behavior without overwriting the whole unit.
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

`google_chrome__idle_timeout`

* Seconds the `systemd-socket-proxyd` waits without active connections before exiting. When it exits, the bound `chrome-headless.service` stops automatically. The next inbound connection re-activates the whole chain, paying ~1–2 seconds of cold-start latency.
* Type: Number.
* Default: `300`

`google_chrome__listen_address`

* Address the proxy socket binds to. Keep this on `127.0.0.1` unless you intentionally want to expose it to other hosts; neither the proxy nor Chrome enforces TLS or authentication.
* Type: String.
* Default: `'127.0.0.1'`

`google_chrome__listen_port`

* Port the proxy socket listens on. This is the endpoint clients connect to.
* Type: Number.
* Default: `9222`

`google_chrome__service_enabled`

* Enables or disables the `chrome-headless-proxy.socket` at boot, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`google_chrome__service_state`

* Changes the state of the `chrome-headless-proxy.socket`, analogous to `systemctl start/stop/restart/reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'`

`google_chrome__user_data_dir`

* Home directory of the `chrome` system user and Chrome user data directory. Used both as the user's `home`, as the `--user-data-dir` value for Chrome, and as the writable path exposed via systemd `ReadWritePaths=`.
* Type: String.
* Default: `'/var/lib/chrome-headless'`

Example:
```yaml
# optional
google_chrome__backend_port: 9223
google_chrome__extra_args__host_var:
  - name: '--window-size=1920,1080'
  - name: '--lang=de-CH'
google_chrome__idle_timeout: 600
google_chrome__listen_address: '127.0.0.1'
google_chrome__listen_port: 9222
google_chrome__service_enabled: true
google_chrome__service_state: 'started'
google_chrome__user_data_dir: '/var/lib/chrome-headless'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
