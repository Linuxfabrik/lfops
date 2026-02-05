# Ansible Role linuxfabrik.lfops.elastic_agent

This role installs and configures [Elastic Agent](https://www.elastic.co/elastic-agent) in Fleet-managed mode. The agent connects to a Fleet Server for centralized management and configuration.


## Mandatory Requirements

* Enable the Elasticsearch Package Repository. This can be done using the [linuxfabrik.lfops.repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch) role.
* A running Fleet Server. This can be set up using the [linuxfabrik.lfops.elastic_agent_fleet_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/elastic_agent_fleet_server) role.
* An enrollment token from Kibana Fleet.


## Optional Requirements

* CA certificate for verifying the Fleet Server TLS certificate. This is the CA used for Fleet Server, typically the same as Elasticsearch.


## Tags

| Tag | Description |
| --- | ----------- |
| `elastic_agent` | Installs and configures elastic-agent |
| `elastic_agent:certs` | Deploys CA certificate |
| `elastic_agent:enroll` | Enrolls the agent to Fleet Server |
| `elastic_agent:state` | Manages the state of the elastic-agent service |


## Pre-Installation Steps

### Get Enrollment Token

Get an enrollment token from Kibana:

1. In Kibana, go to Fleet → Enrollment tokens
2. Click "Create enrollment token"
3. Select the agent policy
4. Copy the token


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `elastic_agent__enrollment_token` | The enrollment token for registering the agent with Fleet Server. Obtain from Kibana Fleet UI or API. |
| `elastic_agent__fleet_urls` | List of Fleet Server URLs. Multiple URLs provide failover. |

Example:
```yaml
# mandatory
elastic_agent__enrollment_token: 'dGhpcyBpcyBhIHNhbXBsZSBlbnJvbGxtZW50IHRva2Vu...'
elastic_agent__fleet_urls:
  - 'https://fleet1.example.com:8220'
  - 'https://fleet2.example.com:8220'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `elastic_agent__fleet_ca` | ASCII-armored PEM CA certificate for verifying the Fleet Server TLS certificate. | unset |
| `elastic_agent__insecure` | Skip TLS verification. Only use for testing with self-signed certificates. | `false` |
| `elastic_agent__service_enabled` | Enables or disables the elastic-agent service, analogous to `systemctl enable/disable`. | `true` |
| `elastic_agent__service_state` | The state of the elastic-agent service. Possible options: `started`, `stopped`, `restarted`. | `'started'` |
| `elastic_agent__tags` | List of tags to apply to the agent during enrollment. Useful for identifying agents in Fleet. | `[]` |

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
