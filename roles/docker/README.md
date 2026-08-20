# Ansible Role linuxfabrik.lfops.docker

This role installs and configures [docker](https://www.docker.com/).


*Available since LFOps `2.0.0`.*


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* The official [docker repository](https://docs.docker.com/engine/install/centos/#install-using-the-repository) must be enabled (role: [linuxfabrik.lfops.repo_docker](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_docker)).


## Tags

`docker`

* Installs and configures docker.
* Triggers: docker.service restart.

`docker:configure`

* Deploys `/etc/docker/daemon.json`.
* Triggers: docker.service restart.

`docker:state`

* Manages the state of the docker service.
* Triggers: none.


## Optional Role Variables

`docker__daemon_json_default_address_pools`

* The address ranges docker allocates the subnets of its container networks from, including the default `bridge` network. Set this to keep docker off ranges that are already routed in your network. The pools replace docker's built-in ones (`172.17.0.0/16` up to `172.28.0.0/14`, and `192.168.0.0/16`), they do not extend them.
* Type: List of dictionaries.
* Default: unset
* Subkeys:

    * `base`:

        * Mandatory. The range the subnets are carved out of, in CIDR notation.
        * Type: String.

    * `size`:

        * Mandatory. The prefix length of each subnet carved out of `base`. A `base` of `172.18.0.0/16` with a `size` of `24` yields 256 container networks.
        * Type: Number.

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
docker__daemon_json_default_address_pools:
  - base: '172.18.0.0/16'
    size: 24
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
