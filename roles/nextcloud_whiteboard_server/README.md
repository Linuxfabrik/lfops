# Ansible Role linuxfabrik.lfops.nextcloud_whiteboard_server

This role runs the collaboration server of the [Nextcloud Whiteboard](https://github.com/nextcloud/whiteboard) app as a rootless Podman container. Users of a whiteboard see each other's changes and cursors in real time only through this server, and it records whiteboard sessions with a headless Chromium. Without it, the Whiteboard app works for one user at a time and Nextcloud reports "WebSocket server URL is not configured".


*Available in the next LFOps release.*


## How the Role Behaves

* The container runs the upstream image `ghcr.io/nextcloud-releases/whiteboard` as the user `nextcloud-whiteboard`, without capabilities and without the right to gain privileges. It listens on `127.0.0.1:3002` only; a reverse proxy publishes it.
* `podman-auto-update.timer` of the user pulls a new image of the configured tag once a day and restarts the container with it. Keep the Whiteboard app in Nextcloud up to date as well, since app and server are released together.
* The JWT secret is stored as a user-scoped systemd credential in `/opt/nextcloud-whiteboard-server/.config/credstore.encrypted/jwt-secret-key`, encrypted with the host key in `/var/lib/systemd/`. When the container starts, systemd decrypts it into `/run/user/<uid>/nextcloud-whiteboard-server/` (tmpfs, removed when the container stops), and the server reads it from there. The secret is therefore never in plain text on disk, not even in Podman's container storage, and not in a backup. With a TPM2 chip, the credential is bound to the Secure Boot state: after a firmware or Secure Boot change, the container does not start until the role runs again. The server refuses to start without the secret.
* Collaboration sessions are kept in memory. A restart of the container ends them; the whiteboards themselves are saved in Nextcloud.
* Recordings: the server records a whiteboard with Chromium and ffmpeg, both part of the image, uploads the video to Nextcloud into the folder `Whiteboard Recordings` of the recording user, and deletes its temporary copy. Nothing stays on this host, but the host needs HTTPS access to `nextcloud_whiteboard_server__nextcloud_url`.
* A change to the container settings restarts the container.


## Known Limitations

* Needs systemd 256 or newer (RHEL 10, Debian 13, Ubuntu 26.04) for the user-scoped credential. The role aborts on older systems before it changes anything.
* One server per Nextcloud. Several servers behind a load balancer would need Redis, which the role does not configure.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* The user `nextcloud-whiteboard` must exist with lingering enabled, so that its containers run without a login (role: [linuxfabrik.lfops.login](https://github.com/Linuxfabrik/lfops/tree/main/roles/login)).
* Podman must be installed and the container deployed as a Quadlet, together with the auto-update timer (role: [linuxfabrik.lfops.podman_containers](https://github.com/Linuxfabrik/lfops/tree/main/roles/podman_containers)).


## Requirements

* Outbound HTTPS access from the host to `ghcr.io` for the image, and to the Nextcloud instance for recordings.
* The kernel module `tun`, which rootless container networking needs. The [kernel_modules](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_modules) role, which `setup_basic` runs, blocks it by default, so allow it in the inventory:
```yaml
kernel_modules__modules__host_var:
  - name: 'tun'
    enabled: true
```

Manual steps:

* Publish the server through a TLS reverse proxy, for example below `/whiteboard/` on a vHost of the [apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role. The browsers of the Nextcloud users connect to it with Socket.IO (WebSocket, falling back to HTTP long polling):
```yaml
apache_httpd__vhosts__host_var:
  - template: 'proxy'
    conf_server_name: 'comm.example.com'
    virtualhost_port: 443
    raw: |-
      ProxyPass /whiteboard/ http://127.0.0.1:3002/ upgrade=websocket
      ProxyPassReverse /whiteboard/ http://127.0.0.1:3002/
```
* Point the Whiteboard app in Nextcloud to the server and give it the same secret, for example on the Nextcloud host with the [nextcloud](https://github.com/Linuxfabrik/lfops/tree/main/roles/nextcloud) role:
```yaml
nextcloud__app_configs__host_var:
  - key: 'whiteboard collabBackendUrl'
    value: 'https://comm.example.com/whiteboard'
  - key: 'whiteboard jwt_secret_key'
    value: 'linuxfabrik'
```


## Tags

`nextcloud_whiteboard_server`

* Checks the systemd version.
* Stores the JWT secret as a user-scoped systemd credential.
* Triggers: `systemctl --user restart nextcloud-whiteboard-server-container.service`.

`nextcloud_whiteboard_server:configure`

* Stores the JWT secret as a user-scoped systemd credential.
* Triggers: `systemctl --user restart nextcloud-whiteboard-server-container.service`.


## Mandatory Role Variables

`nextcloud_whiteboard_server__jwt_secret_key`

* The secret the server and the Whiteboard app in Nextcloud sign and verify their tokens with. Has to match `jwt_secret_key` of the app.
* Type: String.

`nextcloud_whiteboard_server__nextcloud_url`

* The URL under which the users reach Nextcloud. The server only accepts browsers coming from it (CORS) and uploads recordings to it.
* Type: String.

`nextcloud_whiteboard_server__version`

* The tag of the image `ghcr.io/nextcloud-releases/whiteboard`. `'stable'` follows the Whiteboard releases, so that the daily auto-update keeps the server in step with the app; a release tag such as `'v2.1.2'` pins it.
* Type: String.

Example:
```yaml
# mandatory
nextcloud_whiteboard_server__jwt_secret_key: 'linuxfabrik'
nextcloud_whiteboard_server__nextcloud_url: 'https://cloud.example.com'
nextcloud_whiteboard_server__version: 'stable'
```


## Optional Role Variables

`nextcloud_whiteboard_server__container_enabled`

* Whether the container starts at boot.
* Type: Bool.
* Default: `true`

`nextcloud_whiteboard_server__container_state`

* The state of the container. One of `absent`, `present`, `started` or `stopped`.
* Type: String.
* Default: `'started'`

`nextcloud_whiteboard_server__port`

* The port on `127.0.0.1` the server listens on.
* Type: Number.
* Default: `3002`

`nextcloud_whiteboard_server__user_home_directory`

* Home directory of the user `nextcloud-whiteboard`, which holds the credential and the container storage.
* Type: String.
* Default: `'/opt/nextcloud-whiteboard-server'`

Example:
```yaml
# optional
nextcloud_whiteboard_server__container_enabled: true
nextcloud_whiteboard_server__container_state: 'started'
nextcloud_whiteboard_server__port: 3002
nextcloud_whiteboard_server__user_home_directory: '/opt/nextcloud-whiteboard-server'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
