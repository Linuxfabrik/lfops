# Ansible Role linuxfabrik.lfops.elastic_agent

This role installs and configures [Elastic Agent](https://www.elastic.co/elastic-agent) in Fleet-managed mode. The agent connects to a Fleet Server for centralized management and configuration.


*Available since LFOps `6.0.0`.*


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* The Elasticsearch package repository must be enabled (role: [linuxfabrik.lfops.repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch)). The elastic-agent package is served from it.


## Requirements

* A Fleet Server must be running and reachable.

Manual steps:

* Deploy a Fleet Server by running the [elastic_agent_fleet_server](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/elastic_agent_fleet_server.yml) playbook (role: [linuxfabrik.lfops.elastic_agent_fleet_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/elastic_agent_fleet_server)).
* Get an enrollment token from Kibana and store it as `elastic_agent__enrollment_token`:

    1. In Kibana, go to Fleet → Enrollment tokens
    2. Click "Create enrollment token"
    3. Select the agent policy
    4. Copy the token


## Tags

`elastic_agent`

* Installs and configures elastic-agent.
* Triggers: none.

`elastic_agent:certs`

* Deploys CA certificate.
* Triggers: none.

`elastic_agent:enroll`

* Enrolls the agent to Fleet Server.
* Triggers: none.

`elastic_agent:state`

* Manages the state of the elastic-agent service.
* Triggers: none.


## Mandatory Role Variables

`elastic_agent__enrollment_token`

* The enrollment token for registering the agent with Fleet Server. Obtain from Kibana Fleet UI or API.
* Type: String.
* Default: none

`elastic_agent__fleet_url`

* URL of the Fleet Server. Will only be used for the initial connection, afterwards the fleet server defined in the policy will be used.
* Type: String.
* Default: none

Example:
```yaml
# mandatory
elastic_agent__enrollment_token: 'dGhpcyBpcyBhIHNhbXBsZSBlbnJvbGxtZW50IHRva2Vu...'
elastic_agent__fleet_url: 'https://fleet1.example.com:8220'
```


## Optional Role Variables

`elastic_agent__fleet_ca`

* ASCII-armored PEM CA certificate for verifying the Fleet Server TLS certificate, typically the same CA as Elasticsearch.
* Type: String.
* Default: unset

`elastic_agent__insecure`

* Skip TLS verification. Only use for testing with self-signed certificates.
* Type: Bool.
* Default: `false`

`elastic_agent__service_enabled`

* Enables or disables the elastic-agent service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`elastic_agent__service_state`

* The state of the elastic-agent service. Possible options: `started`, `stopped`, `restarted`.
* Type: String.
* Default: `'started'`

`elastic_agent__tags`

* List of tags to apply to the agent during enrollment. Useful for identifying agents in Fleet.
* Type: List.
* Default: `[]`

Example:
```yaml
# optional
elastic_agent__fleet_ca: '{{ lookup("ansible.builtin.file", inventory_dir ~ "/group_files/elasticsearch/ca.crt") }}'
elastic_agent__insecure: false
elastic_agent__service_enabled: true
elastic_agent__service_state: 'started'
elastic_agent__tags:
  - 'production'
  - 'webserver'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
