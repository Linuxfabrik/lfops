# Ansible Role linuxfabrik.lfops.podman_containers

This role installs [Podman](https://podman.io/) and deploys [Quadlets](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html) to configure containers, networks and volumes. The role supports running rootless containers.


*Available since LFOps `3.0.0`.*


## Requirements

Manual steps:

* Optional: when running rootless containers, create a user with lingering enabled by running the [login](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/login.yml) playbook (role: [linuxfabrik.lfops.login](https://github.com/Linuxfabrik/lfops/tree/main/roles/login)):
```yaml
login__users__host_var:
  - name: 'example'
    home: '/opt/example'
    state: 'present'
    linger: true
```
* Optional: when running rootless containers, note that the [kernel_modules](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_modules) role, which `setup_basic` runs, blocks the `tun` kernel module by default. Rootless container networking (pasta, slirp4netns) needs it, so allow it in the inventory:
```yaml
kernel_modules__modules__host_var:
  - name: 'tun'
    enabled: true
```

* Optional: when running rootful containers on a network of their own with a FirewallFabrik nftables script, disable "Flush entire ruleset" in the firewall settings. Otherwise every start of the firewall deletes the rules netavark set up, and the published ports of these containers stop answering until `podman network reload --all`. The policy also has to accept the forwarded traffic to and from the container networks, see [Coexistence with Docker, CrowdSec, fail2ban and Other Tools](https://linuxfabrik.github.io/firewallfabrik/user-guide/12%20-%20Integration%20with%20OS%20Running%20on%20the%20Firewall%20Machine/#coexistence-with-docker-crowdsec-fail2ban-and-other-tools) in the FirewallFabrik user guide. Rootless containers are not affected, their rules live in the network namespace of their user.


## Tags

`podman_containers`

* Installs Podman, deploys `/etc/containers/containers.conf.d/z00-linuxfabrik.conf`, deploys Quadlets and manages their state.
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

* Manages the state of the containers, networks and volumes. Restarts a running container whose unit changed in the same run.
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

`podman_containers__firewall_driver`

* Firewall driver netavark uses to set up the rules of Podman networks, for rootful and rootless containers. Set as `firewall_driver` in `/etc/containers/containers.conf.d/z00-linuxfabrik.conf`; a user's own `~/.config/containers/containers.conf.d/` takes precedence. Possible options: `'firewalld'` (experimental upstream), `'iptables'` (netavark 1 only, netavark 2 on RHEL 10 rejects it), `'nftables'`, `'none'` (no firewall rules, so no port forwarding), or `''` to leave it to netavark. With `'iptables'`, netavark calls whatever `iptables` points to. If that is iptables-legacy (as on RHEL 9 hosts that got the `iptables-legacy` package from EPEL), a rootless container on a network of its own only starts if something else loaded the `ip_tables` kernel module before, which a rootless user may not do. `'nftables'` does not depend on the iptables backend. Takes effect when a network is set up, so restart the containers (or reboot) after changing it. Has no effect with the CNI network backend (Podman 4 on RHEL 8).
* Type: String.
* Default: `'nftables'`
* Deviates from the upstream default `''`, with which netavark picks `'iptables'` on RHEL 9 and `'nftables'` on RHEL 10: with `'iptables'`, rootless containers fail to start where `iptables` is iptables-legacy.

`podman_containers__networks__host_var` / `podman_containers__networks__group_var`

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

`podman_containers__volumes__host_var` / `podman_containers__volumes__group_var`

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
podman_containers__firewall_driver: 'nftables'
podman_containers__networks__host_var:
  - name: 'rocketchat'
    user: 'rocketuser'
podman_containers__volumes__host_var:
  - name: 'rocketchat'
    user: 'rocketuser'
```


## Troubleshooting

**`Failed to enable unit: Unit ... is transient or generated.`**

* Since the units are generated, `systemctl enable/disable` has no effect. Autostarting is handled by the `podman-system-generator` based on the `WantedBy` setting in the quadlet. Have a look at `man podman-systemd.unit` for details.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
