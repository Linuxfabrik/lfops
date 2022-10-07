# Ansible Role linuxfabrik.lfops.graylog_server

This role installs and configures a [Graylog](https://www.graylog.org) server. Currently supported versions: `4.0`, `4.1`, `4.2` and `4.3`.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Enable the official [Graylog repository](https://docs.graylog.org/docs/centos). This can be done using the [linuxfabrik.lfops.repo_graylog](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_graylog) role.


## Tags

| Tag                     | What it does                                    |
| ---                     | ------------                                    |
| `graylog_server`        | Installs and configures Graylog Server          |
| `graylog_server:state`  | Manages the state of the graylog Server service |


## Mandatory Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `graylog_server__root_password` | The password which sould be set for the admin user. | unset |
| `graylog_server__password_secret` | You MUST set a secret to secure/pepper the stored user passwords here. Use at least 64 characters. Generate one by using for example: `pwgen -N 1 -s 96`. ATTENTION: This value must be the same on all Graylog nodes in the cluster. Changing this value after installation will render all user sessions and encrypted values in the database invalid. (e.g. encrypted access tokens) | unset |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `graylog_server__search_engine` | The search engine which Graylog Server should use under the hood. Possibilities are `'opensearch'` or `'elasticsearch'`. ATTENTION: If you choose to use `opensearch`, Graylog Server 4.3 is required! | `'opensearch'` |
| `graylog_server__install_plugins` | Whether following plugins sould be installed additionally: `graylog-enterprise-plugins`, `graylog-integrations-plugins` and `graylog-enterprise-integrations-plugins`. | `false` |
| `graylog_server__root_username` | The admin username which should be used. | `'admin'` |
| `graylog_server__root_email` | The email address of the root user. | `''` |
| `graylog_server__timezone` | The time zone setting of the root user. See [joda.org](http://www.joda.org/joda-time/timezones.html) for a list of valid time zones. | `'UTC'` |
| `graylog_server__http_bind_address` | The network interface used by the Graylog HTTP interface. | `'127.0.0.1'` |
| `graylog_server__http_bind_port` | The port used by the Graylog HTTP interface. | `9000` |
| `graylog_server__service_enabled` | Enable or disable the Graylog Server Service | `true` |


Example:
```yaml
# mandatory
graylog_server__root_password: 'password'
graylog_server__password_secret: '9395pKmkuxSFU623AJpQNA3iyB7R82NuxZRzw19C3m3YXnE62Ky8me7eg9Z1TzwC'

# optional
graylog_server__search_engine: 'elasticsearch'
graylog_server__root_username: 'graylog-admin'
graylog_server__install_plugins: true
graylog_server__root_email: 'webmaster@example.com'
graylog_server__timezone: 'Europe/Zurich'
graylog_server__http_bind_address: '192.168.1.10'
graylog_server__http_bind_port: 8080
graylog_server__service_enabled: false
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
