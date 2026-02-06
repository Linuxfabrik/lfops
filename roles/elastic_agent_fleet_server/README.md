# Ansible Role linuxfabrik.lfops.elastic_agent_fleet_server

This role installs and configures [Elastic Agent](https://www.elastic.co/elastic-agent) as a Fleet Server. The Fleet Server acts as the control plane for managing Elastic Agents and connecting them to Elasticsearch and Kibana.


## Mandatory Requirements

* Enable the Elasticsearch Package Repository. This can be done using the [linuxfabrik.lfops.repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch) role.
* A running Elasticsearch cluster.
* A Fleet Server service token. Generate one using the Elasticsearch API or Kibana (Fleet -> Add Fleet Server).


## Optional Requirements

* TLS certificates for the Fleet Server. Generate them using the Elasticsearch `certutil` tool (see below).


## Tags

| Tag | Description |
| --- | ----------- |
| `elastic_agent_fleet_server` | Installs and configures elastic-agent as Fleet Server |
| `elastic_agent_fleet_server:certs` | Deploys TLS certificates |
| `elastic_agent_fleet_server:enroll` | Enrolls the agent as Fleet Server |
| `elastic_agent_fleet_server:state` | Manages the state of the elastic-agent service |


## Pre-Installation Steps

### Generate Service Token

Generate a service token for the Fleet Server using the Elasticsearch API:

```bash
elastic_host='localhost'
elastic_cacert='/etc/elasticsearch/certs/http_ca.crt'
fleet_server_name="$(hostname --fqdn)"

curl --cacert "$elastic_cacert" \
    --user "elastic:${ELASTIC_PASSWORD}" \
    --request POST "https://$elastic_host:9200/_security/service/elastic/fleet-server/credential/token/$fleet_server_name?pretty=true" \
    --header "Content-Type: application/json"
```

Store the `value` field from the response as `elastic_agent_fleet_server__service_token`.

Alternatively, the token can be taken from Kibana (Fleet -> Add Fleet Server).


### Generate TLS Certificates (Optional)

If you want TLS for the Fleet Server, generate certificates using the Elasticsearch `certutil` tool. On the node where Elasticsearch CA lives:

```bash
cat > /tmp/fleet-server-cert.yml <<EOF
instances:
  - name: 'fleet-server.example.com'
    ip:
      - '127.0.0.1'
      - '192.0.2.10'
    dns:
      - 'localhost'
      - 'fleet-server.example.com'
      - 'fleet-server'
EOF

/usr/share/elasticsearch/bin/elasticsearch-certutil cert \
  --ca-cert /etc/elasticsearch/ca/ca.crt \
  --ca-key /etc/elasticsearch/ca/ca.key \
  --in /tmp/fleet-server-cert.yml \
  --pem \
  --out /tmp/fleet-server-certs.zip
```

Copy the generated certificates to the Ansible inventory. The certificates are used for:
* `elastic_agent_fleet_server__elasticsearch_ca` - The CA certificate (same as Elasticsearch CA)
* `elastic_agent_fleet_server__ssl_cert` - The Fleet Server certificate
* `elastic_agent_fleet_server__ssl_key` - The Fleet Server private key


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `elastic_agent_fleet_server__elasticsearch_host` | Elasticsearch URL. Will only be used for the initial connection, so the node's role is irrelevant. Afterwards, the output defined in the policy will be used. |
| `elastic_agent_fleet_server__service_token` | The service token for authenticating the Fleet Server to Elasticsearch. Generate using the Elasticsearch API. |

Example:
```yaml
# mandatory
elastic_agent_fleet_server__elasticsearch_host: 'https://ingest1.example.com:9200'
elastic_agent_fleet_server__service_token: 'AAEAAWVsYXN0aWMvZmxlZXQtc2VydmVyL3Rva2VuMTpTTHVuZERNWlJJR...'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `elastic_agent_fleet_server__elasticsearch_ca` | ASCII-armored PEM CA certificate for verifying Elasticsearch TLS (Fleet Server -> Elasticsearch). | unset |
| `elastic_agent_fleet_server__insecure` | Skip TLS verification. Only use for testing with self-signed certificates. | `false` |
| `elastic_agent_fleet_server__policy_id` | The Fleet Server policy ID. Must exist in Kibana Fleet. | `'fleet-server-policy'` |
| `elastic_agent_fleet_server__service_enabled` | Enables or disables the elastic-agent service, analogous to `systemctl enable/disable`. | `true` |
| `elastic_agent_fleet_server__service_state` | The state of the elastic-agent service. Possible options: `started`, `stopped`, `restarted`. | `'started'` |
| `elastic_agent_fleet_server__ssl_cert` | ASCII-armored PEM TLS certificate for the Fleet Server (Fleet Agent -> Fleet Server). | unset |
| `elastic_agent_fleet_server__ssl_key` | ASCII-armored PEM TLS private key for the Fleet Server (Fleet Agent -> Fleet Server). | unset |
| `elastic_agent_fleet_server__url` | The URL of the Fleet Server. Used by agents to connect. | `'https://{{ ansible_facts["nodename"] }}:8220'` |

Example:
```yaml
# optional
elastic_agent_fleet_server__elasticsearch_ca: '{{ lookup("ansible.builtin.file", inventory_dir ~ "/group_files/elasticsearch/ca.crt") }}'
elastic_agent_fleet_server__insecure: false
elastic_agent_fleet_server__policy_id: 'fleet-server-policy'
elastic_agent_fleet_server__service_enabled: true
elastic_agent_fleet_server__service_state: 'started'
elastic_agent_fleet_server__ssl_cert: '{{ lookup("ansible.builtin.file", inventory_dir ~ "/host_files/" ~ inventory_hostname ~ "/fleet-server.crt") }}'
elastic_agent_fleet_server__ssl_key: '{{ lookup("ansible.builtin.file", inventory_dir ~ "/host_files/" ~ inventory_hostname ~ "/fleet-server.key") }}'
elastic_agent_fleet_server__url: 'https://fleet.example.com:8220'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
