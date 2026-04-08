# Ansible Role linuxfabrik.lfops.docker

This role installs and configures [docker](https://www.docker.com/).


## Mandatory Requirements

* Enable the official [docker repository](https://docs.docker.com/engine/install/centos/#install-using-the-repository). This can be done using the [linuxfabrik.lfops.repo_docker](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_docker) role.

If you use the ["docker" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/docker.yml), this is automatically done for you.


## Tags

`docker`

* Installs and configures docker.
* Triggers: docker.service restart.

`docker:state`

* Manages the state of the docker service.
* Triggers: none.


## Optional Role Variables

`docker__daemon_json_dns`

* A list of DNS server for all Docker containers.
* Type: List.
* Default: the server's nameserver (`['{{ ansible_facts["dns"]["nameservers"][0] }}']`)

`docker__daemon_json_insecure_registries`

* A list of insecure registries (without TLS) which should be accepted by the docker daemon.
* Type: List.
* Default: unset

`docker__daemon_json_log_driver`

* The default logging driver for all containers. Possible options: <https://docs.docker.com/config/containers/logging/configure/>.
* Type: String.
* Default: `'syslog'`

`docker__daemon_json_log_opts`

* A dictionary of logging options. Possible options: <https://docs.docker.com/config/containers/logging/configure/>.
* Type: Dictionary.
* Default: unset

`docker__service_enabled`

* Enables or disables the docker service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`docker__service_state`

* Changes the state of the docker service, analogous to `systemctl start/stop/restart/reload`. Possible options: `started`, `stopped`, `restarted`, `reloaded`.
* Type: String.
* Default: `'started'`

Example:
```yaml
# optional
docker__daemon_json_dns:
  - '{{ ansible_facts["dns"]["nameservers"][0] }}'
  - 'dns.example.com'
docker__daemon_json_insecure_registries:
  - 'registry.example.com:5000'
docker__daemon_json_log_driver: 'syslog'
docker__daemon_json_log_opts:
  env: 'os,customer'
  labels: 'somelabel'
  max-file: '5'
  max-size: '11m'
docker__service_enabled: true
docker__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
