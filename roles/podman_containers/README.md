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

| Tag                   | What it does                                 |
| ---                   | ------------                                 |
| `podman_containers`             | Installs Podman, deploys Quadlets and manages their state |
| `podman_containers:containers`   | Deploys and removes container Quadlets |
| `podman_containers:networks`   | Deploys and removes network Quadlets |
| `podman_containers:state`   | Manages the state of the containers, networks and volumes |
| `podman_containers:volumes`   | Deploys and removes volume Quadlets |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `podman_containers__containers__host_var` / <br> `podman_containers__containers__group_var` | List of dictionaries describing the Podman containers. Subkeys: <ul><li>`enabled`: Boolean, optional. Set `true` to start the container at boot. Defaults to `true`.</li><li>`name`: String, mandatory. Name of the quadlet file. Will be suffixed with `-container.service`.</li><li>`raw_container`: String, optional. Raw block in the `[Container]` section. Defaults to unset.</li><li>`raw_install`: String, optional. Raw block in the `[Install]` section. Defaults to unset.</li><li>`raw_service`: String, optional. Raw block in the `[Service]` section. Defaults to unset.</li><li>`raw_unit`: String, optional. Raw block in the `[Unit]` section. Defaults to unset.</li><li>`state`: String, optional. State of the container. Possible options: `present`, `absent`, `started` (implies `present`), `stopped` (implies `present`). Defaults to `started`.</li><li>`user`: String, optional. Set this to run the container as rootless. Defaults to unset Defaults to unset (rootful).</li><li>`wanted_by`: String, optional. Unit for the `WantedBy` directive. Only effective if `enabled: true` is set. Defaults to `default.target`.</li></ul> | `[]` |
| `podman_networks__networks__host_var` / <br> `podman_networks__networks__group_var` | List of dictionaries describing the Podman networks. Subkeys: <ul><li>`enabled`: Boolean, optional. Set `true` to start the network at boot. Defaults to `true`.</li><li>`name`: String, mandatory. Name of the quadlet file. Will be suffixed with `-network.service`.</li><li>`raw_network`: String, optional. Raw block in the `[Network]` section. Defaults to unset.</li><li>`raw_install`: String, optional. Raw block in the `[Install]` section. Defaults to unset.</li><li>`raw_service`: String, optional. Raw block in the `[Service]` section. Defaults to unset.</li><li>`raw_unit`: String, optional. Raw block in the `[Unit]` section. Defaults to unset.</li><li>`state`: String, optional. State of the network. Possible options: `present`, `absent`, `started` (implies `present`), `stopped` (implies `present`). Defaults to `started`.</li><li>`user`: String, optional. Set this to run the corresponding container as rootless. Defaults to unset (rootful).</li><li>`wanted_by`: String, optional. Unit for the `WantedBy` directive. Only effective if `enabled: true` is set. Defaults to `default.target`.</li></ul> | `[]` |
| `podman_volumes__volumes__host_var` / <br> `podman_volumes__volumes__group_var` | List of dictionaries describing the Podman volumes. Subkeys: <ul><li>`enabled`: Boolean, optional. Set `true` to start the volume at boot. Defaults to `true`.</li><li>`name`: String, mandatory. Name of the quadlet file. Will be suffixed with `-volume.service`.</li><li>`raw_volume`: String, optional. Raw block in the `[Volume]` section. Defaults to unset.</li><li>`raw_install`: String, optional. Raw block in the `[Install]` section. Defaults to unset.</li><li>`raw_service`: String, optional. Raw block in the `[Service]` section. Defaults to unset.</li><li>`raw_unit`: String, optional. Raw block in the `[Unit]` section. Defaults to unset.</li><li>`state`: String, optional. State of the volume. Possible options: `present`, `absent`, `started` (implies `present`), `stopped` (implies `present`). Defaults to `started`.</li><li>`user`: String, optional. Set this to run the corresponding container as rootless. Defaults to unset (rootful).</li><li>`wanted_by`: String, optional. Unit for the `WantedBy` directive. Only effective if `enabled: true` is set. Defaults to `default.target`.</li></ul> | `[]` |

Example:
```yaml
# optional
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
