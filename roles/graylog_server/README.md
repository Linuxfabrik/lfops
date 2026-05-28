# Ansible Role linuxfabrik.lfops.graylog_server

This role installs and configures a [Graylog](https://www.graylog.org) server. Optionally, it allows the creation of a cluster setup. On-demand, the role can also create or remove Graylog system inputs and index sets via the Graylog API; see [Post-Installation Steps](#post-installation-steps).


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* The role does not pin the Graylog Server version: it installs whatever the configured repository currently offers. To install a specific version, configure the repository accordingly beforehand (e.g. via [linuxfabrik.lfops.repo_graylog](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_graylog)).
* `/etc/graylog/server/server.conf` and the sysconfig opts file are fully templated and re-rendered on every run, with a timestamped backup kept next to each file, so out-of-band manual edits are overwritten. Manage all settings through the role variables.
* The role asserts that `graylog_server__password_secret` is at least 16 characters before running any other task.
* System inputs and index sets are managed only on demand, only on the leader node, and only when the corresponding tag (`graylog_server:configure_system_inputs` / `graylog_server:configure_system_index_sets`) is selected. See [Post-Installation Steps](#post-installation-steps).
* The role ships default system inputs (Beats, GELF TCP, GELF UDP, Syslog UDP) in `__role_var` but **no default index sets** - a single catch-all set is unsuitable for any non-trivial deployment. The operator must define at least one index set in the inventory and mark exactly one as `default: true`.
* The role does not manage the firewall or TLS certificates. Open the listener ports and provide certificates separately.


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


## Post-Installation Steps

Configure the CA for the Data Nodes in the "Graylog Initial Setup" wizard then wait for Graylog to start.

System inputs and index sets are managed on demand via the Graylog API. The role ships with default system inputs in `graylog_server__system_inputs__role_var` but **no default index sets**: rotation, retention, shards and replicas are configured per index set, so a single catch-all set is unsuitable as soon as you have mixed log sources, compliance retention requirements or wildly different volumes. You must define one or more index sets in the inventory, split by use case (typical split: an audit set with long retention, an application set with medium retention, an access/syslog set with short retention). The example in [Optional Role Variables](#optional-role-variables) below uses **data tiering** (Graylog's current model since 6.0); the legacy `rotation_strategy` / `retention_strategy` fields are still supported via `use_legacy_rotation: true` but Graylog has announced they will be deprecated.

To apply, run:

* `--tags graylog_server:configure_system_inputs` to create, update or delete the configured system inputs.
* `--tags graylog_server:configure_system_index_sets` to create, update or delete the configured index sets.

Both tasks only run on the leader node (`graylog_server__is_leader: true`) to avoid duplicates. Entries are matched by `title` (inputs) and `index_prefix` (index sets); changing other fields on an existing entry updates it in place. To remove an entry, override it in your inventory with `state: 'absent'`. Note that the input `port` and `index_prefix` can not be changed after creation; modifying them in the inventory will create a new entry instead of updating the existing one.

`--check` and `--diff` are supported: a dry-run with both flags prints the per-field delta (only the changed keys) and writes nothing.


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

`graylog_server:configure_system_index_sets`

* Only executed on demand.
* Creates, updates and deletes Graylog index sets via the API.
* Sets the index set marked with `default: true` as the default in Graylog.
* Triggers: none.

`graylog_server:configure_system_inputs`

* Only executed on demand.
* Creates, updates and deletes Graylog system inputs via the API.
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

`graylog_server__http_bind_address`

* The network interface used by the Graylog HTTP interface.
* Type: String.
* Default: `'127.0.0.1'`

`graylog_server__http_bind_port`

* The port used by the Graylog HTTP interface.
* Type: Number.
* Default: `9000`

`graylog_server__http_publish_uri`

* The absolute HTTP URI of this Graylog node which is used to communicate with the other Graylog nodes in the cluster and by users to access the Graylog web interface.
* Type: String.
* Default: `''`

`graylog_server__is_leader`

* This should be set to `true` for a single node in the cluster. The leader will perform some periodical tasks that non-leaders won't perform.
* Type: Bool.
* Default: `true`

`graylog_server__message_journal_dir`

* The directory which will be used to store the message journal. The directory must be exclusively used by Graylog and must not contain any other files than the ones created by Graylog itself. The role will create the folder with the required permissions.
* Type: String.
* Default: `'/var/lib/graylog-server/journal'`

`graylog_server__mongodb_uri`

* MongoDB connection string. See https://docs.mongodb.com/manual/reference/connection-string/ for details.
* Type: String.
* Default: `'mongodb://127.0.0.1/graylog'`

`graylog_server__opts`

* The Java options like heapsize used by Graylog.
* Type: String.
* Default: `'-Xms1g -Xmx1g -server -XX:+UseG1GC -XX:-OmitStackTraceInFastThrow'`

`graylog_server__service_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`graylog_server__stale_leader_timeout_ms`

* Time in milliseconds after which a detected stale leader node is being rechecked on startup. Try increasing this if `NO_LEADER: There was no leader Graylog server node detected in the cluster` appear in the System Messages.
* Type: Number.
* Default: `2000`

`graylog_server__system_index_sets__host_var` / `graylog_server__system_index_sets__group_var`

* Index sets to create, update or delete via the Graylog API. Used with the `graylog_server:configure_system_index_sets` tag.
* The role intentionally ships no defaults; the sysadmin must define at least one index set in the inventory and mark exactly one as `default: true`. See [Post-Installation Steps](#post-installation-steps) for the rationale.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `data_tiering`:

        * Mandatory when `use_legacy_rotation` is `false` (recommended). Data tiering is Graylog's current rotation/retention model and replaces the legacy `rotation_strategy` / `retention_strategy` configuration. The legacy strategies still work but Graylog has announced they will be deprecated.
        * Type: Dictionary.
        * Subkeys:

            * `type`:

                * Mandatory. `'hot_only'` for Graylog Open. `'hot_warm'` requires Graylog Enterprise and additional `warm_tier_*` settings.
                * Type: String.

            * `index_lifetime_min`:

                * Mandatory. Minimum time data must stay in the hot tier before becoming eligible for the next lifecycle action. ISO 8601 duration, e.g. `'P7D'` for 7 days.
                * Type: String.

            * `index_lifetime_max`:

                * Mandatory. Maximum time data may stay in the hot tier; once reached the next lifecycle action (rotation, deletion or migration to warm) is enforced. ISO 8601 duration, e.g. `'P30D'` for 30 days.
                * Type: String.

    * `default`:

        * Optional. If `true`, this index set is set as the Graylog default after create/update. Only one entry should set this.
        * Type: Bool.
        * Default: `false`

    * `description`:

        * Mandatory. Description of the index set.
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

        * Mandatory. A unique prefix used in indices belonging to this index set. The prefix must start with a letter or number, and can only contain letters, numbers, `_`, `-` and `+`. Used as the identity key for create/update/delete; cannot be changed after creation (changing it creates a new index set). It must not start with the same word as another index_prefix, e.g. `lfops` and `lfops02` would conflict.
        * Type: String.

    * `replicas`:

        * Mandatory. Number of replicas used per index in this index set.
        * Type: Number.

    * `retention_strategy`:

        * Legacy. Mandatory only when `use_legacy_rotation` is `true`; ignored otherwise. Prefer `data_tiering`.
        * Type: Dictionary.
        * Subkeys:

            * `max_number_of_indices`:

                * Mandatory. Maximum number of indices to keep before retention strategy gets triggered.
                * Type: Number.

            * `type`:

                * Mandatory. Retention strategy type to clean up old indices.
                * Type: String.

    * `retention_strategy_class`:

        * Legacy. Mandatory only when `use_legacy_rotation` is `true`; ignored otherwise. Prefer `data_tiering`.
        * Type: String.

    * `rotation_strategy`:

        * Legacy. Mandatory only when `use_legacy_rotation` is `true`; ignored otherwise. Prefer `data_tiering`.
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

        * Legacy. Mandatory only when `use_legacy_rotation` is `true`; ignored otherwise. Prefer `data_tiering`.
        * Type: String.

    * `shards`:

        * Mandatory. Number of shards used per index in this index set. Never set this higher than the number of data nodes.
        * Type: Number.

    * `state`:

        * Optional. State of the index set, one of `present`, `absent`.
        * Type: String.
        * Default: `'present'`

    * `title`:

        * Mandatory. Descriptive name of the index set.
        * Type: String.

    * `use_legacy_rotation`:

        * Optional. `false` (recommended) activates `data_tiering`; `true` falls back to the legacy `rotation_strategy` / `retention_strategy` configuration, which Graylog has announced will be deprecated.
        * Type: Bool.
        * Default: `false`

    * `writable`:

        * Mandatory. Whether this index set is writable.
        * Type: Bool.

`graylog_server__system_inputs__host_var` / `graylog_server__system_inputs__group_var`

* System inputs to create, update or delete via the Graylog API. Used with the `graylog_server:configure_system_inputs` tag.
* Type: List of dictionaries.
* Default: `Beats (5044/TCP)`, `Gelf (12201/TCP)`, `Gelf (12201/UDP)` and `Syslog (1514/UDP)`. See [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/graylog_server/defaults/main.yml) for the full content.
* Subkeys:

    * `configuration`:

        * Mandatory. Input-specific configuration; see the [API documentation](https://go2docs.graylog.org/current/setting_up_graylog/rest_api.html). The `port` cannot be changed after creation (changing it creates a new input).
        * Type: Dictionary.

    * `global`:

        * Mandatory. Whether this input should start on all nodes. Each entry must either set `global: true` or assign a `node`, otherwise Graylog creates the input but never starts it; the role asserts this.
        * Type: Bool.

    * `state`:

        * Optional. State of the input, one of `present`, `absent`.
        * Type: String.
        * Default: `'present'`

    * `title`:

        * Mandatory. The title for this input. Used as the identity key for create/update/delete.
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
graylog_server__http_bind_address: '192.0.2.1'
graylog_server__http_bind_port: 9000
graylog_server__http_publish_uri: 'http://graylog.example.com:9000/'
graylog_server__is_leader: true
graylog_server__message_journal_dir: '/data/graylog/journal'
graylog_server__mongodb_uri: 'mongodb://graylog01.example.com:27017,username:password@graylog02.example.com:27017,graylog03.example.com:27017/graylog?replicaSet=rs01'
graylog_server__opts: '-Xms2g -Xmx2g -server -XX:+UseG1GC -XX:-OmitStackTraceInFastThrow'
graylog_server__service_enabled: false
graylog_server__stale_leader_timeout_ms: 10000
graylog_server__system_index_sets__host_var:
  # catch-all set, marked as the Graylog default; everything that no stream rule
  # routes elsewhere lands here. Data tiering keeps data for 25-30 days.
  - title: 'Default'
    description: 'Default catch-all index set; 25-30 days - managed by Ansible - do not edit'
    default: true
    use_legacy_rotation: false
    data_tiering:
      type: 'hot_only'
      index_lifetime_min: 'P25D'
      index_lifetime_max: 'P30D'
    field_type_refresh_interval: 5000
    index_analyzer: 'standard'
    index_optimization_disabled: false
    index_optimization_max_num_segments: 1
    index_prefix: 'default'
    replicas: 0
    shards: 1
    state: 'present'
    writable: true
  # audit logs, long retention
  - title: 'Audit'
    description: 'Audit logs; 360-365 days - managed by Ansible - do not edit'
    use_legacy_rotation: false
    data_tiering:
      type: 'hot_only'
      index_lifetime_min: 'P360D'
      index_lifetime_max: 'P365D'
    field_type_refresh_interval: 5000
    index_analyzer: 'standard'
    index_optimization_disabled: false
    index_optimization_max_num_segments: 1
    index_prefix: 'audit'
    replicas: 0
    shards: 1
    state: 'present'
    writable: true
  # high-volume access/syslog logs, short retention
  - title: 'Access'
    description: 'Access/syslog logs; 10-14 days - managed by Ansible - do not edit'
    use_legacy_rotation: false
    data_tiering:
      type: 'hot_only'
      index_lifetime_min: 'P10D'
      index_lifetime_max: 'P14D'
    field_type_refresh_interval: 5000
    index_analyzer: 'standard'
    index_optimization_disabled: false
    index_optimization_max_num_segments: 1
    index_prefix: 'access'
    replicas: 0
    shards: 1
    state: 'present'
    writable: true
graylog_server__system_inputs__host_var:
  # add an additional input alongside the role defaults
  - title: 'Gelf Audit (12202/UDP - managed by Ansible - do not edit)'
    configuration:
      bind_address: '0.0.0.0'
      port: 12202
      decompress_size_limit: 8388608
      number_worker_threads: 4
      override_source: ''
      recv_buffer_size: 1048576
    global: true
    state: 'present'
    type: 'org.graylog2.inputs.gelf.udp.GELFUDPInput'
  # opt out of one of the role defaults:
  - title: 'Syslog (1514/UDP - managed by Ansible - do not edit)'
    state: 'absent'
graylog_server__timezone: 'Europe/Zurich'
graylog_server__trusted_proxies:
  - '127.0.0.1/32'
  - '0:0:0:0:0:0:0:1/128'
  - '10.0.0.0/8'
```


## Troubleshooting

**`/bin/sh: /opt/python-venv/pymongo/bin/python3: No such file or directory`**

* The `pymongo` virtualenv that the role's MongoDB-touching tasks rely on is missing. Run the full playbook, or just the `python_venv` role: `ansible-playbook --inventory myinv linuxfabrik.lfops.setup_graylog_server --tags python_venv`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
