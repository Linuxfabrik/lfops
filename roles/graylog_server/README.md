# Ansible Role linuxfabrik.lfops.graylog_server

This role installs and configures a [Graylog](https://www.graylog.org) server. Optionally, it allows the creation of a cluster setup.

Additionally this role creates default "System Inputs" and a Linuxfabrik default "index set".

Note that this role does NOT let you specify a particular Graylog Server version. It simply installs the latest available Graylog Server version from the repos configured in the system. If you want or need to install a specific Graylog Server version, use the [linuxfabrik.lfops.repo_graylog](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_graylog) beforehand.


*Available since LFOps `2.0.0`.*


## Known Limitations

* This role only supports Graylog Data Nodes (not OpenSearch or Elasticsearch).


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* MongoDB must be installed (role: [linuxfabrik.lfops.mongodb](https://github.com/Linuxfabrik/lfops/tree/main/roles/mongodb)).
* The official [Graylog repository](https://go2docs.graylog.org/current/downloading_and_installing_graylog/red_hat_installation.htm) must be enabled (role: [linuxfabrik.lfops.repo_graylog](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_graylog)).


## Requirements

* Size the disks before running the role:

    * `/`: at least 4 GB free disk space (create a 8+ GB partition).
    * `/var`: at least 15 GB free disk space (create a 20+ GB partition).

Manual steps:

* Set hostnames properly and ensure that communication via DNS among all participating hosts works. This especially affects clustered systems, because the datanode instance registers itself to the mongodb database with its hostname.
* If you're not using a versioned MongoDB repository, protect MongoDB from being updated with newer minor and major versions by running the [dnf_versionlock](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/dnf_versionlock.yml) playbook (role: [linuxfabrik.lfops.dnf_versionlock](https://github.com/Linuxfabrik/lfops/tree/main/roles/dnf_versionlock)).


## Tags

`graylog_server`

* Installs the graylog-server package.
* Deploys the configuration files.
* Creates the message journal directory.
* Ensures the graylog-server service is in the desired state.
* Waits for the service to become available.
* Triggers: graylog-server.service restart.

`graylog_server:configure`

* Deploys the configuration files.
* Removes rpmnew/rpmsave files.
* Creates the message journal directory.
* Triggers: graylog-server.service restart.

`graylog_server:configure_defaults`

* Only executed on demand.
* Configures Graylog system inputs via the API.
* Creates and sets the default index set.
* Triggers: none.

`graylog_server:state`

* Manages the state of the graylog-server service.
* Triggers: none.


## Mandatory Role Variables

`graylog_server__password_secret`

* This secret must be set to the same value on all Graylog Server and Data Nodes.
* Type: String.

`graylog_server__root_user`

* The main user account for the Graylog administrator.
* Type: Dictionary.
* Subkeys:

    * `username`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Mandatory. Password.
        * Type: String.

    * `email`:

        * Optional. Email.
        * Type: String.
        * Default: `''`

Example:
```yaml
# mandatory
graylog_server__password_secret: 'Linuxfabrik_GmbH'
graylog_server__root_user:
  username: 'graylog-admin'
  password: 'linuxfabrik'
  email: 'webmaster@example.com'
```


## Optional Role Variables

`graylog_server__elasticsearch_hosts`

* List of Elasticsearch host URLs Graylog should connect to. Only set this when not using Graylog Data Nodes.
* Type: List of strings.
* Default: unset

`graylog_server__elasticsearch_max_total_connections`

* Maximum number of total connections to Elasticsearch/OpenSearch.
* Type: Number.
* Default: `200`

`graylog_server__elasticsearch_max_total_connections_per_route`

* Maximum number of total connections per Elasticsearch/OpenSearch route (normally this means per server).
* Type: Number.
* Default: `20`

`graylog_server__http_bind_address`

* The network interface used by the Graylog HTTP interface.
* Type: String.
* Default: `'127.0.0.1'`

`graylog_server__http_bind_port`

* The port used by the Graylog HTTP interface.
* Type: Number.
* Default: `9000`

`graylog_server__http_enable_cors`

* Whether to send CORS headers from the HTTP interface, allowing browsers to make Cross-Origin requests from any origin. Typically only needed when running Graylog with a separate frontend development server.
* Type: Bool.
* Default: `false`

`graylog_server__http_external_uri`

* The public URI of Graylog used by the web interface to communicate with the Graylog REST API. Usually required when Graylog runs behind a reverse proxy or load balancer. When left empty, `graylog_server__http_publish_uri` is used.
* Type: String.
* Default: `''`

`graylog_server__http_publish_uri`

* The absolute HTTP URI of this Graylog node which is used to communicate with the other Graylog nodes in the cluster and by users to access the Graylog web interface.
* Type: String.
* Default: `''`

`graylog_server__inputbuffer_ring_size`

* Size of the internal input ring buffer. Must be a power of 2 (512, 1024, 2048, ...).
* Type: Number.
* Default: `65536`

`graylog_server__is_leader`

* This should be set to `true` for a single node in the cluster. The leader will perform some periodical tasks that non-leaders won't perform.
* Type: Bool.
* Default: `true`

`graylog_server__message_journal_dir`

* The directory which will be used to store the message journal. The directory must be exclusively used by Graylog and must not contain any other files than the ones created by Graylog itself. The role will create the folder with the required permissions.
* Type: String.
* Default: `'/var/lib/graylog-server/journal'`

`graylog_server__message_journal_max_age`

* Maximum age messages are held in the journal before they are written to Elasticsearch/OpenSearch (whichever of maximum age or maximum size is reached first).
* Type: String.
* Default: `'12h'`

`graylog_server__message_journal_max_size`

* Maximum size of the message journal before messages are written to Elasticsearch/OpenSearch (whichever of maximum age or maximum size is reached first).
* Type: String.
* Default: `'5gb'`

`graylog_server__mongodb_uri`

* MongoDB connection string. See https://docs.mongodb.com/manual/reference/connection-string/ for details.
* Type: String.
* Default: `'mongodb://127.0.0.1/graylog'`

`graylog_server__opts`

* The Java options like heapsize used by Graylog.
* Type: String.
* Default: `'-Xms1g -Xmx1g -server -XX:+UseG1GC -XX:-OmitStackTraceInFastThrow'`

`graylog_server__output_batch_size`

* Batch size for the Elasticsearch/OpenSearch output, i.e. the maximum accumulated size of messages written in a single batch call. Can be an absolute number of messages or a data unit (e.g. `'10mb'`).
* Type: Number or String.
* Default: `500`

`graylog_server__outputbuffer_processors`

* Number of output buffer processors running in parallel. When unset, Graylog determines the value automatically based on the number of available CPU cores. Raise this if your buffers are filling up.
* Type: Number.
* Default: unset

`graylog_server__processbuffer_processors`

* Number of process buffer processors running in parallel. When unset, Graylog determines the value automatically based on the number of available CPU cores. Raise this if your buffers are filling up.
* Type: Number.
* Default: unset

`graylog_server__ring_size`

* Size of the internal output ring buffer. Raise this if raising `graylog_server__outputbuffer_processors` does not help anymore. Must be a power of 2 (512, 1024, 2048, ...).
* Type: Number.
* Default: `65536`

`graylog_server__service_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`graylog_server__stale_leader_timeout_ms`

* Time in milliseconds after which a detected stale leader node is being rechecked on startup. Try increasing this if `NO_LEADER: There was no leader Graylog server node detected in the cluster` appear in the System Messages.
* Type: Number.
* Default: `2000`

`graylog_server__system_default_index_set`

* Creates a default index set. Used with the `graylog_server:configure_defaults` tag.
* Type: Dictionary.
* Default: See [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/graylog_server/defaults/main.yml)
* Subkeys:

    * `creation_date`:

        * Mandatory. Date in ISO 8601 format.
        * Type: String.

    * `description`:

        * Mandatory. Description of index set.
        * Type: String.

    * `field_type_refresh_interval`:

        * Mandatory. Refresh interval in milliseconds.
        * Type: Number.

    * `index_analyzer`:

        * Mandatory. Elasticsearch/OpenSearch analyzer for this index set.
        * Type: String.

    * `index_optimization_disabled`:

        * Mandatory. Whether index optimization (force merge) after rotation is disabled.
        * Type: Bool.

    * `index_optimization_max_num_segments`:

        * Mandatory. Maximum number of segments per index after optimization (force merge).
        * Type: Number.

    * `index_prefix`:

        * Mandatory. A unique prefix used in indices belonging to this index set. The prefix must start with a letter or number, and can only contain letters, numbers, `_`, `-` and `+`.
        * Type: String.

    * `replicas`:

        * Mandatory. Number of replicas used per index in this index set.
        * Type: Number.

    * `retention_strategy`:

        * Mandatory. Retention strategy configuration.
        * Type: Dictionary.
        * Subkeys:

            * `max_number_of_indices`:

                * Mandatory. Maximum number of indices to keep before retention strategy gets triggered.
                * Type: Number.

            * `type`:

                * Mandatory. Retention strategy type to clean up old indices.
                * Type: String.

    * `retention_strategy_class`:

        * Mandatory. Retention strategy class to clean up old indices.
        * Type: String.

    * `rotation_strategy`:

        * Mandatory. Rotation strategy configuration.
        * Type: Dictionary.
        * Subkeys:

            * `rotation_period`:

                * Mandatory. How long an index gets written to before it is rotated (e.g. `'P1D'` for 1 day, `'PT6H'` for 6 hours).
                * Type: String.

            * `rotate_empty_index_set`:

                * Mandatory. Apply the rotation strategy even when the index set is empty (not recommended).
                * Type: Bool.

            * `type`:

                * Mandatory. The type of the rotation strategy.
                * Type: String.

    * `rotation_strategy_class`:

        * Mandatory. Graylog uses multiple indices to store documents in. You can configure the strategy it uses to determine when to rotate the currently active write index.
        * Type: String.

    * `shards`:

        * Mandatory. Number of shards used per index in this index set. Never set this higher than the number of data nodes.
        * Type: Number.

    * `title`:

        * Mandatory. Descriptive name of the index set.
        * Type: String.

    * `writable`:

        * Mandatory. Whether this index set is writable.
        * Type: Bool.

`graylog_server__system_inputs`

* Creates system inputs. Used with the `graylog_server:configure_defaults` tag.
* Type: List of dictionaries.
* Default: See [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/graylog_server/defaults/main.yml)
* Subkeys:

    * `configuration`:

        * Mandatory. Specific configuration of corresponding input. Please refer to the [API documentation](https://go2docs.graylog.org/current/setting_up_graylog/rest_api.html).
        * Type: Dictionary.

    * `global`:

        * Mandatory. Whether this input should start on all nodes.
        * Type: Bool.

    * `title`:

        * Mandatory. The title for this input.
        * Type: String.

    * `type`:

        * Mandatory. The type of the input.
        * Type: String.
        * To list the input types available on your Graylog node, append `/api-browser#?route=get-/system/inputs/types` to your Graylog web interface URL (for example `https://graylog.example.com/api-browser#?route=get-/system/inputs/types`) and click `Execute`. The `/system/inputs/types/all` route additionally returns each type's available `configuration` fields.

`graylog_server__timezone`

* The time zone setting of the root user. See [joda.org](http://www.joda.org/joda-time/timezones.html) for a list of valid time zones.
* Type: String.
* Default: `'Europe/Zurich'`

`graylog_server__trusted_proxies`

* List of trusted proxies that are allowed to set the client address with `X-Forwarded-For` header. May be subnets or hosts.
* Type: List of strings.
* Default: `[]`

Example:
```yaml
# optional
graylog_server__elasticsearch_hosts:
  - 'https://opensearch1.example.com:9200'
  - 'https://opensearch2.example.com:9200'
  - 'https://opensearch3.example.com:9200'
graylog_server__elasticsearch_max_total_connections: 200
graylog_server__elasticsearch_max_total_connections_per_route: 20
graylog_server__http_bind_address: '192.0.2.1'
graylog_server__http_bind_port: 9000
graylog_server__http_enable_cors: false
graylog_server__http_external_uri: 'https://graylog.example.com/'
graylog_server__http_publish_uri: 'http://graylog.example.com:9000/'
graylog_server__inputbuffer_ring_size: 65536
graylog_server__is_leader: true
graylog_server__message_journal_dir: '/data/graylog/journal'
graylog_server__message_journal_max_age: '12h'
graylog_server__message_journal_max_size: '5gb'
graylog_server__mongodb_uri: 'mongodb://graylog01.example.com:27017,username:password@graylog02.example.com:27017,graylog03.example.com:27017/graylog?replicaSet=rs01'
graylog_server__opts: '-Xms2g -Xmx2g -server -XX:+UseG1GC -XX:-OmitStackTraceInFastThrow'
graylog_server__output_batch_size: 500
graylog_server__outputbuffer_processors: 3
graylog_server__processbuffer_processors: 5
graylog_server__ring_size: 65536
graylog_server__service_enabled: false
graylog_server__stale_leader_timeout_ms: 10000
graylog_server__system_default_index_set:
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
  shards: 3
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
graylog_server__timezone: 'Europe/Zurich'
graylog_server__trusted_proxies:
  - '127.0.0.1/32'
  - '0:0:0:0:0:0:0:1/128'
  - '10.0.0.0/8'
```


## Troubleshooting

Q: `/bin/sh: /opt/python-venv/pymongo/bin/python3: No such file or directory`

A: You either have to run the whole playbook, or python_venv directly: `ansible-playbook --inventory myinv linuxfabrik.lfops.setup_graylog_server --tags python_venv`


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
