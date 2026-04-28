# Ansible Role linuxfabrik.lfops.logstash

This role installs and configures a Logstash server with support for multiple pipelines.

Note that this role does NOT let you specify a particular Logstash version. It simply installs the latest available Logstash version from the repos configured in the system. If you want or need to install a specific version, have a look at the [linuxfabrik.lfops.repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch) role (Logstash uses the Elasticsearch repository).


## Mandatory Requirements

* Enable the official elasticsearch repository. This can be done using the [linuxfabrik.lfops.repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch) role.

If you use the [logstash playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/logstash.yml), this is automatically done for you.


## Tags

`logstash`

* Installs and configures Logstash.
* Triggers: logstash.service restart.

`logstash:configure`

* Deploys configuration files and TLS certs.
* Triggers: logstash.service reload.

`logstash:grok_patterns`

* Deploys custom grok pattern files.
* Triggers: logstash.service reload.

`logstash:pipelines`

* Deploys pipeline configuration files.
* Triggers: logstash.service reload.

`logstash:state`

* Manages the state of the Logstash service.
* Triggers: none.


## Optional Role Variables

`logstash__elasticsearch_ca_cert`

* ASCII-armored PEM CA certificate for TLS connections to Elasticsearch. Should match the CA used by Elasticsearch.
* Type: String.
* Default: unset

`logstash__grok_patterns__host_var` / `logstash__grok_patterns__group_var`

* List of custom grok pattern file definitions.
* Subkeys:

    * `name`:

        * Mandatory. Filename in `/etc/logstash/patterns/`.
        * Type: String.

    * `content`:

        * Mandatory. Pattern definitions (format: `PATTERN_NAME regex`).
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

* Type: List of dictionaries.
* Default: `[]`

`logstash__java_opts`

* Additional Java options passed to Logstash via `LS_JAVA_OPTS`. By default, sets the temp directory to `{{ logstash__path_data }}/tmp` because `/tmp` on CIS-hardened systems is mounted with noexec.
* Type: String.
* Default: `'-Djava.io.tmpdir={{ logstash__path_data }}/tmp'`

`logstash__log_level`

* The log level. Valid values are: `fatal`, `error`, `warn`, `info`, `debug`, `trace`.
* Type: String.
* Default: `'info'`

`logstash__monitoring_cluster_uuid`

* Elasticsearch Cluster UUID. Binds the metrics of Logstash to this specific cluster.
* Type: String.
* Default: unset

`logstash__monitoring_enabled`

* Enables or disables default collection of Logstash monitoring data.
* Type: Bool.
* Default: `true`

`logstash__node_name`

* A descriptive name for the node.
* Type: String.
* Default: `'{{ ansible_facts["nodename"] }}'`

`logstash__path_data`

* Path to the directory where Logstash stores its data.
* Type: String.
* Default: `'/var/lib/logstash'`

`logstash__path_logs`

* Path to the directory where Logstash stores its logs.
* Type: String.
* Default: `'/var/log/logstash'`

`logstash__pipelines__host_var` / `logstash__pipelines__group_var`

* List of pipeline definitions.
* Subkeys:

    * `pipeline_id`:

        * Mandatory. Unique identifier for the pipeline. Used as filename (`<pipeline_id>.conf`).
        * Type: String.

    * `content`:

        * Mandatory. The pipeline configuration content (input/filter/output sections).
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

    * `pipeline_workers`:

        * Optional. Number of worker threads for this pipeline.
        * Type: Number.

    * `pipeline_batch_size`:

        * Optional. Maximum number of events per batch.
        * Type: Number.

    * `pipeline_batch_delay`:

        * Optional. Maximum delay in milliseconds before dispatching an undersized batch.
        * Type: Number.

    * `pipeline_ordered`:

        * Optional. Event ordering mode: `auto`, `true`, or `false`.
        * Type: String.

    * `queue_type`:

        * Optional. Queue type: `memory` or `persisted`.
        * Type: String.

    * `queue_max_bytes`:

        * Optional. Maximum queue capacity (e.g., `'1024mb'`).
        * Type: String.

    * `queue_page_capacity`:

        * Optional. Page data file size for persisted queues.
        * Type: String.

    * `queue_max_events`:

        * Optional. Maximum number of unread events in the queue.
        * Type: Number.

    * `queue_checkpoint_acks`:

        * Optional. Maximum number of acked events before forcing a checkpoint.
        * Type: Number.

    * `queue_checkpoint_writes`:

        * Optional. Maximum number of written events before forcing a checkpoint.
        * Type: Number.

    * `dead_letter_queue_enable`:

        * Optional. Enable dead letter queue for this pipeline.
        * Type: Bool.

    * `dead_letter_queue_max_bytes`:

        * Optional. Maximum size of the dead letter queue.
        * Type: String.

* Type: List of dictionaries.
* Default: `[]`

`logstash__raw`

* Raw content which will be appended to the `logstash.yml` config file.
* Type: String.
* Default: `''`

`logstash__service_enabled`

* Enables or disables the logstash service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`logstash__service_state`

* Controls the state of the logstash service, analogous to `systemctl start/stop/restart/reload`. Possible options: `started`, `stopped`, `restarted`, `reloaded`.
* Type: String.
* Default: `'started'`

Example:
```yaml
# optional
logstash__elasticsearch_ca_cert: '{{ lookup("ansible.builtin.file", "{{ inventory_dir }}/group_files/elasticsearch/ca.crt") }}'
logstash__grok_patterns__host_var:
  - name: 'custom_app'
    content: |
      CUSTOM_TIMESTAMP %{YEAR}-%{MONTHNUM}-%{MONTHDAY}T%{HOUR}:%{MINUTE}:%{SECOND}
      CUSTOM_LOGLEVEL (DEBUG|INFO|WARN|ERROR|FATAL)
      CUSTOM_APPLOG %{CUSTOM_TIMESTAMP:timestamp} %{CUSTOM_LOGLEVEL:level} %{GREEDYDATA:message}
  - name: 'old_patterns'
    state: 'absent'
logstash__java_opts: '-Djava.io.tmpdir={{ logstash__path_data }}/tmp'
logstash__log_level: 'info'
logstash__node_name: '{{ ansible_facts["nodename"] }}'
logstash__path_data: '/var/lib/logstash'
logstash__path_logs: '/var/log/logstash'
logstash__pipelines__host_var:
  - pipeline_id: 'beats'
    pipeline_workers: 4
    content: |
      input {
        beats {
          port => 5044
        }
      }
      filter {
        if [fields][type] == "syslog" {
          grok {
            patterns_dir => ["/etc/logstash/patterns"]
            match => { "message" => "%{SYSLOGLINE}" }
          }
        }
      }
      output {
        elasticsearch {
          hosts => ["https://elasticsearch.example.com:9200"]
          ssl_certificate_authorities => ["/etc/logstash/certs/ca.crt"]
          user => "logstash_writer"
          password => "${LOGSTASH_ES_PASSWORD}"
          index => "beats-%{+YYYY.MM.dd}"
        }
      }
  - pipeline_id: 'syslog'
    queue_type: 'persisted'
    queue_max_bytes: '2048mb'
    content: |
      input {
        syslog {
          port => 514
        }
      }
      output {
        elasticsearch {
          hosts => ["https://elasticsearch.example.com:9200"]
          ssl_certificate_authorities => ["/etc/logstash/certs/ca.crt"]
          index => "syslog-%{+YYYY.MM.dd}"
        }
      }
  - pipeline_id: 'old-pipeline'
    state: 'absent'
logstash__raw: |-
  config.reload.automatic: true
  config.reload.interval: 3s
logstash__service_enabled: true
logstash__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
