# Ansible Role linuxfabrik.lfops.graylog_server

This role installs and configures a [Graylog](https://www.graylog.org) server. Optionally, it allows the creation of a cluster setup.

Additionally this role creates default "System Inputs" and a Linuxfabrik default "index set".

Note that this role does NOT let you specify a particular Graylog Server version. It simply installs the latest available Graylog Server version from the repos configured in the system. If you want or need to install a specific Graylog Server version, use the [linuxfabrik.lfops.repo_graylog_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_graylog_server) beforehand.


## Known Limitations

* This role only supports Graylog Data Nodes (not OpenSearch or Elasticsearch).


## Mandatory Requirements

Properly set hostnames and ensure that communication via DNS among all participating hosts works. This especially affects clustered systems, because the datanode instance registers itself to the mongodb database with its hostname.

Sizing of disks:

* `/`: at least 4 GB free disk space (create a 8+ GB partition).
* `/var`: at least 15 GB free disk space (create a 20+ GB partition).

If you use the ["Setup Graylog Server" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_graylog_server.yml), the following is automatically done for you:

* Install MongoDB. This can be done using the [linuxfabrik.lfops.mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mongodb) role.
* If you're not using a versioned MongoDB repository, don't forget to protect MongoDB from being updated with newer minor and major versions. This can be done using the [linuxfabrik.lfops.dnf_versionlock](https://github.com/Linuxfabrik/lfops/tree/main/roles/dnf_versionlock) role.
* Enable the official [Graylog repository](https://go2docs.graylog.org/current/downloading_and_installing_graylog/red_hat_installation.htm). This can be done using the [linuxfabrik.lfops.repo_graylog](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_graylog) role.


## Tags

| Tag                         | What it does                                    | Reload / Restart |
| ---                         | ------------                                    | ---------------- |
| `graylog_server`            | Installs and configures Graylog Server          | Restarts graylog-server.service |
| `graylog_server:configure`  | Deploys the config files, manages the CA keystore, creates the system inputs and a default index set | Restarts graylog-server.service |
| `graylog_server:configure_defaults`  | Only executed on demand. Configure Graylog Indices, Index Sets and Inputs. | - |
| `graylog_server:state`      | Manages the state of the Graylog Server service | - |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `graylog_server__root_user` | The main user account for the graylog administrator. Subkeys:<ul><li>`username`: Mandatory, string. Username</li><li>`password`: Mandatory, string. Password</li><li>`email`: Optional, string. Email. Defaults to `''`.</li></ul> |
| `graylog_server__password_secret` | This secret must be set the same value on all Graylog Server and Data Nodes. |

Example:
```yaml
# mandatory
graylog_server__root_user:
  username: 'graylog-admin'
  password: 'linuxfabrik'
  email: 'webmaster@example.com'
graylog_server__password_secret: 'Linuxfabrik_GmbH'
```

## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `graylog_server__elasticsearch_hosts` | List of Elasticsearch hosts URLs Graylog should connect to. Only set this when not using Graylog Data Nodes. | unset |
| `graylog_server__http_bind_address` | The network interface used by the Graylog HTTP interface. | `'127.0.0.1'` |
| `graylog_server__http_bind_port` | The port used by the Graylog HTTP interface. | `9000` |
| `graylog_server__is_leader` | This should be set to `true` for a single node in the cluster. The leader will perform some periodical tasks that non-leaders won't perform. | `true` |
| `graylog_server__mongodb_uri` | MongoDB connection string. See https://docs.mongodb.com/manual/reference/connection-string/ for details. | `'mongodb://127.0.0.1/graylog'` |
| `graylog_server__opts` | The Java options like heapsize used by Graylog. | `'-Xms1g -Xmx1g -server -XX:+UseG1GC -XX:-OmitStackTraceInFastThrow'` |
| `graylog_server__service_enabled` | Enables or disables the Systemd unit. | `true` |
| `graylog_server__stale_leader_timeout_ms` | Time in milliseconds after which a detected stale leader node is being rechecked on startup. Try increasing this if `NO_LEADER: There was no leader Graylog server node detected in the cluster` appear in the System Messages. | `2000` |
| `graylog_server__timezone` | The time zone setting of the root user. See [joda.org](http://www.joda.org/joda-time/timezones.html) for a list of valid time zones. | `'Europe/Zurich'` |

Example:
```yaml
# optional
graylog_server__elasticsearch_hosts: # TODO doesnt exist anymore
  - 'https://opensearch1.example.com:9200'
  - 'https://opensearch2.example.com:9200'
  - 'https://opensearch3.example.com:9200'
graylog_server__http_bind_address: '192.0.2.1'
graylog_server__http_bind_port: 9000
graylog_server__is_leader: true
graylog_server__mongodb_uri: 'mongodb://graylog01.example.com:27017,username:password@graylog02.example.com:27017,graylog03.example.com:27017/graylog?replicaSet=rs01'
graylog_server__opts: '-Xms2g -Xmx2g -server -XX:+UseG1GC -XX:-OmitStackTraceInFastThrow'
graylog_server__service_enabled: false
graylog_server__stale_leader_timeout_ms: 10000
graylog_server__timezone: 'Europe/Zurich'
```


## Configure Graylog Indices, Index Sets and Inputs

Use the tag `graylog_server:configure_defaults` to configure Graylog indices, index sets and inputs.

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `graylog_server__system_default_index_set` | Creates a default index set. Subkeys: <ul><li>`can_be_default`: Mandatory, boolean. Whether this index set can be default.</li><li>`creation_date`: Mandatory, date. Date in iso8601 format.</li><li>`description`: Mandatory, string. Description of index set.</li><li>`field_type_refresh_interval`: Mandatory, integer. Refresh interval in milliseconds.</li><li>`index_analyzer`: Mandatory, string. Elasticsearch/Opensearch analyzer for this index set.</li><li>`index_optimization_max_num_segments`: Mandatory, integer. Maximum number of segments per Elasticsearch/Opensearch index after optimization (force merge).</li><li>`index_optimization_disabled`: Mandatory, boolean. Whether Elasticsearch/Opensearch index optimization (force merge) after rotation is disabled.</li><li>`index_prefix`: Mandatory, string. A unique prefix used in Elasticsearch/Opensearch indices belonging to this index set. The prefix must start with a letter or number, and can only contain letters, numbers, `_`, `-` and `+`.</li><li>`replicas`: Mandatory, integer. Number of Elasticsearch/Opensearch replicas used per index in this index set.</li><li>`retention_strategy_class`: Mandatory, string. Retention strategy class to clean up old indices.</li><li>`retention_strategy`<ul><li>`max_number_of_indices`: Mandatory, integer. Maximum number of indices to keep before retention strategy gets triggered.</li><li>`type`: Mandatory, string. Retention strategy type to clean up old indices.</li></ul><li>`rotation_strategy_class`: Mandatory, string. Graylog uses multiple indices to store documents in. You can configure the strategy it uses to determine when to rotate the currently active write index.</li><li>`rotation_strategy`<ul><li>`rotation_period`: Mandatory, string. How long an index gets written to before it is rotated. (i.e. "P1D" for 1 day, "PT6H" for 6 hours).</li><li>`rotate_empty_index_set`: Mandatory, boolean. Apply the rotation strategy even when the index set is empty (not recommended).</li><li>`type`: Mandatory, string. The type of the Rotation Strategy.</li></ul><li>`shards`: Mandatory, integer. Number of Elasticsearch/Opensearch shards used per index in this index set. Attention: Never set this higher than the number of Elasticsearch/Opensearch nodes!</li><li>`title`: Mandatory, string. Descriptive name of the index set.</li><li>`writable`: Mandatory, boolean. Whether this Index Set is writable.</li></ul> | One index per day; 365 indices max |
| `graylog_server__system_inputs` | Creates system inputs. Subkeys: <ul><li>`configuration`: Mandatory, dictionay. Specific configuration of corresponding input. Please refer to the [API documentation](https://go2docs.graylog.org/current/setting_up_graylog/rest_api.html).</li><li>`global`: Mandatory, boolean. Whether this input should start on all nodes.</li><li>`title`: Mandatory, string. The title for this input.</li><li>`type`: Mandatory, string. The type of the input.</li></ul> | Gelf (12201/TCP), Gelf (12201/UDP), Syslog (1514/UDP) |

Example:
```yaml
# optional
graylog_server__system_default_index_set:
  can_be_default: true
  creation_date: '{{ ansible_date_time.iso8601 }}'
  description: 'One index per day; 365 indices max'
  field_type_refresh_interval: 5000
  index_analyzer: 'standard'
  index_optimization_disabled: false
  index_optimization_max_num_segments: 1
  index_prefix: 'lfops-default'
  replicas: 0
  retention_strategy:
    max_number_of_indices: 365
    type: 'org.graylog2.indexer.retention.strategies.DeletionRetentionStrategyConfig'
  retention_strategy_class: 'org.graylog2.indexer.retention.strategies.DeletionRetentionStrategy'
  rotation_strategy:
    rotation_period: 'P1D'
    rotate_empty_index_set: false
    type: 'org.graylog2.indexer.rotation.strategies.TimeBasedRotationStrategyConfig'
  rotation_strategy_class: 'org.graylog2.indexer.rotation.strategies.TimeBasedRotationStrategy'
  shards: 4
  title: 'Linuxfabrik Index Set (managed by Ansible - do not edit)'
  writable: true
graylog_server__system_inputs:
  - configuration:
      bind_address: '0.0.0.0'
      number_worker_threads: 4
      override_source: ''
      port: 5044
      recv_buffer_size: 1048576
      tcp_keepalive: false
      tls_cert_file: ''
      tls_client_auth: 'disabled'
      tls_client_auth_cert_file: ''
      tls_enable: false
      tls_key_file: ''
      tls_key_password: ''
    global: true
    title: 'Beats (5044/TCP - managed by Ansible - do not edit)'
    type: 'org.graylog.plugins.beats.Beats2Input'
  - configuration:
      bind_address: '0.0.0.0'
      decompress_size_limit: 8388608
      max_message_size: 2097152
      number_worker_threads: 4
      override_source: ''
      port: 12201
      recv_buffer_size: 1048576
      tcp_keepalive: false
      tls_cert_file: ''
      tls_client_auth: 'disabled'
      tls_client_auth_cert_file: ''
      tls_enable: false
      tls_key_file: ''
      tls_key_password: ''
      use_null_delimiter: true
    global: true
    title: 'Gelf (12201/TCP - managed by Ansible - do not edit)'
    type: 'org.graylog2.inputs.gelf.tcp.GELFTCPInput'
  - configuration:
      bind_address: '0.0.0.0'
      decompress_size_limit: 8388608
      number_worker_threads: 4
      override_source: ''
      port: 12201
      recv_buffer_size: 1048576
    global: true
    title: 'Gelf (12201/UDP - managed by Ansible - do not edit)'
    type: 'org.graylog2.inputs.gelf.udp.GELFUDPInput'
  - configuration:
      allow_override_date: true
      bind_address: '0.0.0.0'
      decompress_size_limit: 8388608
      expand_structured_data: false
      force_rdns: false
      number_worker_threads: 4
      override_source: ''
      port: 1514
      recv_buffer_size: 1048576
      store_full_message: false
    global: true
    title: 'Syslog (1514/UDP - managed by Ansible - do not edit)'
    type: 'org.graylog2.inputs.syslog.udp.SyslogUDPInput'
```


## Troubleshooting

Q: `/bin/sh: /opt/python-venv/pymongo/bin/python3: No such file or directory`

A: You either have to run the whole playbook, or python_venv directly: `ansible-playbook --inventory myinv linuxfabrik.lfops.setup_graylog_server --tags python_venv`


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
