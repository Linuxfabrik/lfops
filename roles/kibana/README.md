# Ansible Role linuxfabrik.lfops.kibana

This role installs and configures Kibana, a visualization and exploration tool for data stored in Elasticsearch.

Note that this role does NOT let you specify a particular Kibana version. It simply installs the latest available Kibana version from the repos configured in the system. If you want or need to install a specific version, have a look at the [linuxfabrik.lfops.repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch) role, which also provides Kibana packages.


## Mandatory Requirements

* Enable the official Elasticsearch repository (which also provides Kibana packages). This can be done using the [linuxfabrik.lfops.repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch) role.
* A running Elasticsearch installation. This can be done using the [linuxfabrik.lfops.elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/elasticsearch) role.

If you use the [kibana playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/kibana.yml), the repository setup is automatically done for you.


## Tags

| Tag                  | What it does                               | Reload / Restart            |
| ---                  | ------------                               | ----------------            |
| `kibana`             | Installs and configures Kibana             | Restarts kibana.service     |
| `kibana:configure`   | Deploys configuration files                | Restarts kibana.service     |
| `kibana:state`       | Manages the state of the Kibana service    | -                           |


## Post-Installation Steps

Create a service account token for Kibana on an Elasticsearch node:

```bash
elastic_host='localhost'
elastic_cacert='/etc/elasticsearch/certs/http_ca.crt'

curl --cacert "$elastic_cacert" \
    --user "elastic:${ELASTIC_PASSWORD}" \
    --request POST "https://$elastic_host:9200/_security/service/elastic/kibana/credential/token/kibana-token-01?pretty=true" \
    --header "Content-Type: application/json"
```


## Mandatory Role Variables

| Variable                                          | Description                                                                         |
| --------                                          | -----------                                                                         |
| `kibana__elasticsearch_service_account_token`     | Service account token for Kibana to authenticate to Elasticsearch. See Post-Installation Steps for how to create this token. |
| `kibana__xpack_encrypted_saved_objects_encryption_key` | Encryption key for encrypted saved objects (alerts, actions, connectors). Must be at least 32 characters. Generate with `openssl rand -base64 32`. Note: Use the same key across all Kibana instances when load-balancing. |
| `kibana__xpack_reporting_encryption_key`          | Encryption key for reporting features. Must be at least 32 characters. Generate with `openssl rand -base64 32`. Note: Use the same key across all Kibana instances when load-balancing. |
| `kibana__xpack_security_encryption_key`           | Encryption key for security features (session data, tokens). Must be at least 32 characters. Generate with `openssl rand -base64 32`. Note: Use the same key across all Kibana instances when load-balancing. |

Example:
```yaml
# mandatory
kibana__elasticsearch_service_account_token: 'AAEAAWVsYXN0aWMva2liYW5hL3Rva2VuMTpabGQ...'
kibana__xpack_encrypted_saved_objects_encryption_key: '...'
kibana__xpack_reporting_encryption_key: '...'
kibana__xpack_security_encryption_key: '...'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `kibana__csp_strict` | Boolean. Enables strict Content Security Policy (CSP) mode for additional protection against XSS attacks. Set to `false` if you have compatibility issues with certain browsers or plugins. | `true` |
| `kibana__elasticsearch_ca_cert` | ASCII-armored PEM CA certificate for TLS connections to Elasticsearch. Should match the CA used by Elasticsearch. | unset |
| `kibana__elasticsearch_hosts` | List of URLs of the Elasticsearch instances to use for all queries. Supports multiple hosts for high availability. | `['https://localhost:9200']` |
| `kibana__elasticsearch_ssl_verification_mode` | Controls the verification of certificates presented by Elasticsearch. One of: `full` (performs hostname verification), `certificate` (skips hostname verification) or `none` (skips verification entirely). | `'full'` |
| `kibana__server_host` | Specifies the address to which the Kibana server will bind. IP addresses and host names are both valid values. To allow connections from remote users, set this parameter to a non-loopback address. | `0.0.0.0` |
| `kibana__server_name` | A human-readable name for this Kibana instance. | `'{{ ansible_facts["nodename"] }}'` |
| `kibana__server_port` | The port on which the Kibana server will listen. | `5601` |
| `kibana__server_public_base_url` | The publicly available URL that end users will use to access Kibana. This is used for generating links in emails and other places. | unset |
| `kibana__server_security_response_headers_disable_embedding` | Prevents embedding Kibana in iframes to mitigate clickjacking attacks. Set to `false` if you need to embed Kibana in other applications. | `true` |
| `kibana__server_ssl_certificate` | Path to the PEM-format SSL certificate file for HTTPS connections from browsers to Kibana. Required when `kibana__server_ssl_enabled: true` is set. The role will set ownership to `kibana:root` and mode to `0644`. | unset |
| `kibana__server_ssl_enabled` | Boolean. Enables SSL/TLS for incoming connections from browsers to the Kibana server. When enabled, `kibana__server_ssl_certificate` and `kibana__server_ssl_key` must be provided. | `false` |
| `kibana__server_ssl_key` | Path to the PEM-format SSL private key file for HTTPS connections from browsers to Kibana. Required when `kibana__server_ssl_enabled: true` is set. The role will set ownership to `kibana:kibana` and mode to `0400` for security. | unset |
| `kibana__service_enabled` | Enables or disables the kibana service, analogous to `systemctl enable/disable --now`. | `true` |
| `kibana__service_state` | Controls the state of the kibana service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |

Example:
```yaml
# optional
kibana__csp_strict: true
kibana__elasticsearch_ca_cert: '{{ lookup("ansible.builtin.file", "{{ inventory_dir }}/group_files/elasticsearch_cluster/etc/elasticsearch/certs/ca.crt") }}'
kibana__elasticsearch_hosts:
  - 'https://elasticsearch01.example.com:9200'
  - 'https://elasticsearch02.example.com:9200'
  - 'https://elasticsearch03.example.com:9200'
kibana__elasticsearch_ssl_verification_mode: 'full'
kibana__server_host: '0.0.0.0'
kibana__server_name: 'kibana-prod-01'
kibana__server_port: 5601
kibana__server_public_base_url: 'https://kibana.example.com'
kibana__server_security_response_headers_disable_embedding: true
kibana__server_ssl_certificate: '/etc/pki/tls/certs/kibana-server.crt'
kibana__server_ssl_enabled: true
kibana__server_ssl_key: '/etc/pki/tls/private/kibana-server.key'
kibana__service_enabled: true
kibana__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
