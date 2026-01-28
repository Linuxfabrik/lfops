# Ansible Role linuxfabrik.lfops.logstash

This role installs and configures a Logstash server with support for multiple pipelines.

Note that this role does NOT let you specify a particular Logstash version. It simply installs the latest available Logstash version from the repos configured in the system. If you want or need to install a specific version, have a look at the [linuxfabrik.lfops.repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch) role (Logstash uses the Elasticsearch repository).


## Mandatory Requirements

* Enable the official elasticsearch repository. This can be done using the [linuxfabrik.lfops.repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch) role.

If you use the [logstash playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/logstash.yml), this is automatically done for you.


## Tags

| Tag                  | What it does                              | Reload / Restart          |
| ---                  | ------------                              | ----------------          |
| `logstash`           | Installs and configures Logstash          | Restarts logstash.service |
| `logstash:configure` | Deploys configuration files and TLS certs | Reloads logstash.service  |
| `logstash:pipelines` | Deploys pipeline configuration files      | Reloads logstash.service  |
| `logstash:state`     | Manages the state of the Logstash service | -                         |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `logstash__elasticsearch_ca_cert` | ASCII-armored PEM CA certificate for TLS connections to Elasticsearch. Should match the CA used by Elasticsearch. | unset |
| `logstash__java_opts` | Additional Java options passed to Logstash via `LS_JAVA_OPTS`. By default, sets the temp directory to `{{ logstash__path_data }}/tmp` because `/tmp` on CIS-hardened systems is mounted with noexec. | `'-Djava.io.tmpdir={{ logstash__path_data }}/tmp'` |
| `logstash__log_level` | The log level. Valid values are: `fatal`, `error`, `warn`, `info`, `debug`, `trace`. | `'info'` |
| `logstash__node_name` | A descriptive name for the node. | `'{{ ansible_facts["nodename"] }}'` |
| `logstash__path_data` | Path to the directory where Logstash stores its data. | `'/var/lib/logstash'` |
| `logstash__path_logs` | Path to the directory where Logstash stores its logs. | `'/var/log/logstash'` |
| `logstash__pipelines__host_var` / <br> `logstash__pipelines__group_var` | List of pipeline definitions. Subkeys: <ul><li>`pipeline_id`: Mandatory, string. Unique identifier for the pipeline. Used as filename (`<pipeline_id>.conf`).</li><li>`content`: Mandatory, multiline string. The pipeline configuration content (input/filter/output sections).</li><li>`state`: Optional, string. `present` or `absent`. Defaults to `present`.</li><li>`pipeline_workers`: Optional, integer. Number of worker threads for this pipeline.</li><li>`pipeline_batch_size`: Optional, integer. Maximum number of events per batch.</li><li>`pipeline_batch_delay`: Optional, integer. Maximum delay in milliseconds before dispatching an undersized batch.</li><li>`pipeline_ordered`: Optional, string. Event ordering mode: `auto`, `true`, or `false`.</li><li>`queue_type`: Optional, string. Queue type: `memory` or `persisted`.</li><li>`queue_max_bytes`: Optional, string. Maximum queue capacity (e.g., `'1024mb'`).</li><li>`queue_page_capacity`: Optional, string. Page data file size for persisted queues.</li><li>`queue_max_events`: Optional, integer. Maximum number of unread events in the queue.</li><li>`queue_checkpoint_acks`: Optional, integer. Maximum number of acked events before forcing a checkpoint.</li><li>`queue_checkpoint_writes`: Optional, integer. Maximum number of written events before forcing a checkpoint.</li><li>`dead_letter_queue_enable`: Optional, boolean. Enable dead letter queue for this pipeline.</li><li>`dead_letter_queue_max_bytes`: Optional, string. Maximum size of the dead letter queue.</li></ul> | `[]` |
| `logstash__raw` | Multiline string. Raw content which will be appended to the `logstash.yml` config file. | `''` |
| `logstash__service_enabled` | Enables or disables the logstash service, analogous to `systemctl enable/disable --now`. | `true` |
| `logstash__service_state` | Controls the state of the logstash service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |

Example:
```yaml
# optional
logstash__elasticsearch_ca_cert: '{{ lookup("ansible.builtin.file", "{{ inventory_dir }}/group_files/elasticsearch/ca.crt") }}'
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
