# Ansible Role linuxfabrik.lfops.podman_containers

This role installs [Podman](https://podman.io/) and deploys [Quadlets](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html) to configure containers, networks and volumes. The role supports running rootless containers.


## Mandatory Requirements

* When running rootless containers, make sure to create a user with lingering enabled. This can be done using the [linuxfabrik.lfops.login](https://github.com/Linuxfabrik/lfops/tree/main/roles/login) role:
```yaml
login__users__host_var:
  - name: 'example'
    home: '/opt/example'
    state: 'present'
    linger: true
```


## Tags

`podman_containers`

* Installs Podman, deploys Quadlets and manages their state.
* Triggers: none.

`podman_containers:auto_update`

* Manages podman-auto-update.timer for system and users.
* Triggers: none.

`podman_containers:containers`

* Deploys and removes container Quadlets.
* Triggers: none.

`podman_containers:networks`

* Deploys and removes network Quadlets.
* Triggers: none.

`podman_containers:state`

* Manages the state of the containers, networks and volumes.
* Triggers: none.

`podman_containers:volumes`

* Deploys and removes volume Quadlets.
* Triggers: none.


## Optional Role Variables

`podman_containers__auto_update__host_var` / `podman_containers__auto_update__group_var`

* List of dictionaries controlling `podman-auto-update.timer`.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `on_calendar`:

        * Optional. Custom schedule for the timer in systemd calendar format (e.g., `daily`, `weekly`, `*-*-* 04:00:00`). When specified, creates an override file to customize the schedule. Uses systemd default `daily` when unset.
        * Type: String.
        * Default: unset

    * `state`:

        * Optional. State of the timer. Possible options: `present` (enable and start), `absent` (disable and stop).
        * Type: String.
        * Default: `'present'`

    * `user`:

        * Mandatory. Username for which to manage the timer. Use `root` for the system-wide timer.
        * Type: String.

`podman_containers__containers__host_var` / `podman_containers__containers__group_var`

* List of dictionaries describing the Podman containers.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `enabled`:

        * Optional. Set `true` to start the container at boot.
        * Type: Bool.
        * Default: `true`

    * `name`:

        * Mandatory. Name of the quadlet file. Will be suffixed with `-container.service`.
        * Type: String.

    * `raw_container`:

        * Optional. Raw block in the `[Container]` section.
        * Type: String.
        * Default: unset

    * `raw_install`:

        * Optional. Raw block in the `[Install]` section.
        * Type: String.
        * Default: unset

    * `raw_service`:

        * Optional. Raw block in the `[Service]` section.
        * Type: String.
        * Default: unset

    * `raw_unit`:

        * Optional. Raw block in the `[Unit]` section.
        * Type: String.
        * Default: unset

    * `state`:

        * Optional. State of the container. Possible options: `present`, `absent`, `started` (implies `present`), `stopped` (implies `present`).
        * Type: String.
        * Default: `'started'`

    * `user`:

        * Optional. Set this to run the container as rootless.
        * Type: String.
        * Default: unset (rootful)

    * `wanted_by`:

        * Optional. Unit for the `WantedBy` directive. Only effective if `enabled: true` is set.
        * Type: String.
        * Default: `'default.target'`

`podman_networks__networks__host_var` / `podman_networks__networks__group_var`

* List of dictionaries describing the Podman networks.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `enabled`:

        * Optional. Set `true` to start the network at boot.
        * Type: Bool.
        * Default: `true`

    * `name`:

        * Mandatory. Name of the quadlet file. Will be suffixed with `-network.service`.
        * Type: String.

    * `raw_network`:

        * Optional. Raw block in the `[Network]` section.
        * Type: String.
        * Default: unset

    * `raw_install`:

        * Optional. Raw block in the `[Install]` section.
        * Type: String.
        * Default: unset

    * `raw_service`:

        * Optional. Raw block in the `[Service]` section.
        * Type: String.
        * Default: unset

    * `raw_unit`:

        * Optional. Raw block in the `[Unit]` section.
        * Type: String.
        * Default: unset

    * `state`:

        * Optional. State of the network. Possible options: `present`, `absent`, `started` (implies `present`), `stopped` (implies `present`).
        * Type: String.
        * Default: `'started'`

    * `user`:

        * Optional. Set this to run the corresponding container as rootless.
        * Type: String.
        * Default: unset (rootful)

    * `wanted_by`:

        * Optional. Unit for the `WantedBy` directive. Only effective if `enabled: true` is set.
        * Type: String.
        * Default: `'default.target'`

`podman_volumes__volumes__host_var` / `podman_volumes__volumes__group_var`

* List of dictionaries describing the Podman volumes.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `enabled`:

        * Optional. Set `true` to start the volume at boot.
        * Type: Bool.
        * Default: `true`

    * `name`:

        * Mandatory. Name of the quadlet file. Will be suffixed with `-volume.service`.
        * Type: String.

    * `raw_volume`:

        * Optional. Raw block in the `[Volume]` section.
        * Type: String.
        * Default: unset

    * `raw_install`:

        * Optional. Raw block in the `[Install]` section.
        * Type: String.
        * Default: unset

    * `raw_service`:

        * Optional. Raw block in the `[Service]` section.
        * Type: String.
        * Default: unset

    * `raw_unit`:

        * Optional. Raw block in the `[Unit]` section.
        * Type: String.
        * Default: unset

    * `state`:

        * Optional. State of the volume. Possible options: `present`, `absent`, `started` (implies `present`), `stopped` (implies `present`).
        * Type: String.
        * Default: `'started'`

    * `user`:

        * Optional. Set this to run the corresponding container as rootless.
        * Type: String.
        * Default: unset (rootful)

    * `wanted_by`:

        * Optional. Unit for the `WantedBy` directive. Only effective if `enabled: true` is set.
        * Type: String.
        * Default: `'default.target'`

Example:
```yaml
# optional
podman_containers__auto_update__host_var:
  - user: 'root'
    state: 'present'
    on_calendar: '*-*-* 04:00:00' # run at 4 AM every day
  - user: 'rocketuser'
    state: 'present'
    on_calendar: 'weekly'
podman_containers__containers__host_var:
  - name: 'rocketchat'
    raw_container: |
      AutoUpdate=registry
      ContainerName=rocketchat
      EnvironmentFile=/opt/rocketchat/rocketchat.env
      HealthCmd=curl --fail --show-error --silent --max-time 2 http://localhost:3000
      HealthInterval=30s
      HealthOnFailure=kill
      HealthRetries=5
      HealthStartPeriod=5s
      HealthTimeout=10s
      Image=registry.rocket.chat/rocketchat/rocket.chat:latest
      LogDriver=journald
      Network=rocketchat.network
      PublishPort=3000:3000/tcp
      User=rocketchat
      UserNS=keep-id:uid=1000,gid=1000
    raw_service: |
      Restart=always
    user: 'rocketuser'
podman_containers__networks__host_var:
  - name: 'rocketchat'
    user: 'rocketuser'
podman_containers__volumes__host_var:
  - name: 'rocketchat'
    user: 'rocketuser'
```


## Troubleshooting

`Failed to enable unit: Unit ... is transient or generated.`: Since the units are generated, `systemctl enable/disable` has no effect. Autostarting is handled by the `podman-system-generator` based on the `WantedBy` setting in the quadlet. Have a look at `man podman-systemd.unit` for details.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
