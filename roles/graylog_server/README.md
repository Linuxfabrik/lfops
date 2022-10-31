# Ansible Role linuxfabrik.lfops.graylog_server

This role installs and configures a [Graylog](https://www.graylog.org) server. Currently supported versions: `4.0`, `4.1`, `4.2` and `4.3`.
You can choose between `opensearch` (default) and `elasticsearch` as the searchengine. If you choose to use `opensearch`, Graylog Server 4.3 is required!

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

| Tag                     | What it does                                    |
| ---                     | ------------                                    |
| `graylog_server`        | Installs and configures Graylog Server          |
| `graylog_server:state`  | Manages the state of the Graylog Server service |


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
| `graylog_server__plugins` | A list of available plugins which can be installed additionally. Possible options: </br> * `graylog-enterprise-plugins`<br/> * `graylog-integrations-plugins`<br/> *  `graylog-enterprise-integrations-plugins` | `[]` |
| `graylog_server__timezone` | The time zone setting of the root user. See [joda.org](http://www.joda.org/joda-time/timezones.html) for a list of valid time zones. | `'Europe/Zurich'` |
| `graylog_server__http_bind_address` | The network interface used by the Graylog HTTP interface. | `'127.0.0.1'` |
| `graylog_server__http_bind_port` | The port used by the Graylog HTTP interface. | `9000` |
| `graylog_server__service_enabled` | Enables or disables the Systemd unit. | `true` |


Example:
```yaml
# optional
graylog_server__plugins:
  - 'graylog-enterprise-plugins'
  - 'graylog-integrations-plugins'
  - 'graylog-enterprise-integrations-plugins'
graylog_server__timezone: 'Europe/Zurich'
graylog_server__http_bind_address: '192.0.2.1'
graylog_server__http_bind_port: 8080
graylog_server__service_enabled: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
