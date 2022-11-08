# Ansible Role linuxfabrik.lfops.graylog_server

This role installs and configures a [Graylog](https://www.graylog.org) server. Currently supported versions: `4.0`, `4.1`, `4.2` and `4.3`.
You can choose between `opensearch` (default) and `elasticsearch` as the searchengine. If you choose to use `opensearch`, Graylog Server 4.3 is required!
Additionally this role creates default `system inputs` and a Linuxfabrik default `index set`. Please check [Graylog API Reference](https://docs.graylog.org/docs/rest-api).

Note that this role does NOT let you specify a particular Graylog Server version. It simply installs the latest available Graylog Server version from the repos configured in the system. If you want or need to install a specific Graylog Server version, use the [linuxfabrik.lfops.repo_graylog_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_graylog_server) beforehand.


Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Install Java. This can be done using the [linuxfabrik.lfops.mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/java) role.
* Install MongoDB. This can be done using the [linuxfabrik.lfops.mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mongodb) role.
* Install Opensearch (preferred) or Elasticsearch as a search engine. This can be done using the [linuxfabrik.lfops.opensearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/opensearch) or [linuxfabrik.lfops.elasticsearch_oss](https://github.com/Linuxfabrik/lfops/tree/main/roles/elasticsearch_oss) role.
* Enable the official [Graylog repository](https://docs.graylog.org/docs/centos). This can be done using the [linuxfabrik.lfops.repo_graylog](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_graylog) role.

If you use the ["Setup Graylog Server" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_graylog_server.yml), this is automatically done for you.

## Tags

| Tag                         | What it does                                    |
| ---                         | ------------                                    |
| `graylog_server`            | Installs and configures Graylog Server          |
| `graylog_server:configure`  | Creates system inputs and a default index set   |
| `graylog_server:state`      | Manages the state of the Graylog Server service |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `graylog_server__admin_user` | The main user account for the graylog administrator. Subkeys:<br> * `username`: Username<br> * `password`: Password<br> * `email`: Optional, string. Email. Defaults to `''`. |
| `graylog_server__password_secret` | You MUST set a secret to secure/pepper the stored user passwords here. Use at least 64 characters. Generate one by using for example: `pwgen -N 1 -s 96`. ATTENTION: This value must be the same on all Graylog nodes in the cluster. Changing this value after installation will render all user sessions and encrypted values in the database invalid. (e.g. encrypted access tokens) |

Example:
```yaml
# mandatory
graylog_server__admin_user:
  username: 'graylog-admin'
  password: 'linuxfabrik'
  email: 'webmaster@example.com'
graylog_server__password_secret: '9395pKmkuxSFU623AJpQNA3iyB7R82NuxZRzw19C3m3YXnE62Ky8me7eg9Z1TzwC'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `graylog_server__http_bind_address` | The network interface used by the Graylog HTTP interface. | `'127.0.0.1'` |
| `graylog_server__http_bind_port` | The port used by the Graylog HTTP interface. | `9000` |
| `graylog_server__plugins` | A list of available plugins which can be installed additionally. Possible options: </br> * `graylog-enterprise-plugins`<br/> * `graylog-integrations-plugins`<br/> *  `graylog-enterprise-integrations-plugins` | `[]` |
| `graylog_server__service_enabled` | Enables or disables the Systemd unit. | `true` |
| `graylog_server__system_default_index_set` | Creates a default index set. ATTENTION: The `index_prefix` must be `role-default`, because the role is looking for this exact value. | One index per day; 365 indices max |
| `graylog_server__system_inputs` | Creates system inputs. | Gelf (12201/TCP), Gelf (12201/UDP) |
| `graylog_server__timezone` | The time zone setting of the root user. See [joda.org](http://www.joda.org/joda-time/timezones.html) for a list of valid time zones. | `'Europe/Zurich'` |

Example:
```yaml
# optional
graylog_server__http_bind_address: '192.0.2.1'
graylog_server__http_bind_port: 8080
graylog_server__plugins:
  - 'graylog-enterprise-plugins'
  - 'graylog-integrations-plugins'
  - 'graylog-enterprise-integrations-plugins'
graylog_server__service_enabled: false
graylog_server__system_inputs:
  - title: 'Gelf (12201/TCP)'
    global: true
    type: 'org.graylog2.inputs.gelf.tcp.GELFTCPInput'
    configuration:
        bind_address: '0.0.0.0'
        port: 12201
        decompress_size_limit: 8388608
        max_message_size: 2097152
        number_worker_threads: 2
        override_source: ''
        recv_buffer_size: 1048576
        tcp_keepalive: true
        tls_cert_file: ''
        tls_client_auth: 'disabled'
        tls_client_auth_cert_file: ''
        tls_enable: false
        tls_key_file: ''
        tls_key_password: ''
        use_null_delimiter: true
  - title: 'Gelf (12201/UDP)'
    global: true
    type: 'org.graylog2.inputs.gelf.udp.GELFUDPInput'
    configuration:
        bind_address: '0.0.0.0'
        port: 12201
        decompress_size_limit: 8388608
        number_worker_threads: 2
        override_source: ''
        recv_buffer_size: 1048576
graylog_server__system_default_index_set:
    title: 'Linuxfabrik Index Set'
    description: 'One index per day; 365 indices max'
    default: true
    can_be_default: true
    creation_date: '{{ ansible_date_time.iso8601 }}'
    shards: 4
    replicas: 0
    index_optimization_max_num_segments: 1
    index_optimization_disabled: false
    field_type_refresh_interval: 5000
    retention_strategy_class: 'org.graylog2.indexer.retention.strategies.DeletionRetentionStrategy'
    retention_strategy:
        max_number_of_indices: 365
        type: 'org.graylog2.indexer.retention.strategies.DeletionRetentionStrategyConfig'
    rotation_strategy_class: 'org.graylog2.indexer.rotation.strategies.TimeBasedRotationStrategy'
    rotation_strategy:
        rotation_period: 'P1D'
        rotate_empty_index_set: false
        type: 'org.graylog2.indexer.rotation.strategies.TimeBasedRotationStrategyConfig'
    writable: true
    index_analyzer: 'standard'
    index_prefix: 'role-default'
graylog_server__timezone: 'Europe/Zurich'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
