# Ansible Role linuxfabrik.lfops.mastodon

This role installs and configures [Mastodon](https://joinmastodon.org/), a federated microblogging platform, as Podman containers.


## Mandatory Requirements

* Enable the PostgreSQL repository. This can be done using the [linuxfabrik.lfops.repo_postgresql](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_postgresql) role.
* Install the PostgreSQL server. This can be done using the [linuxfabrik.lfops.postgresql_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/postgresql_server) role.
* Create a PostgreSQL user for Mastodon. This can be done using the [linuxfabrik.lfops.postgresql_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/postgresql_server) role.
* Install Redis. This can be done using the [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) and [linuxfabrik.lfops.redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis) role.
* Enable the Elasticsearch repository (optional). This can be done using the [linuxfabrik.lfops.repo_elasticsearch_oss](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch_oss) role.
* Install Elasticsearch (optional). This can be done using the [linuxfabrik.lfops.elasticsearch_oss](https://github.com/Linuxfabrik/lfops/tree/main/roles/elasticsearch_oss) role.
* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Install Apache HTTPd. This can be done using the [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role.

If you use the ["Setup Mastodon" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_mastodon.yml), this is automatically done for you (you still have to take care of providing the required versions).

* Make sure the container can access the databases:
```yaml
# PostgreSQL
postgresql_server__conf_listen_addresses:
  - 'localhost'
  - 'fqdn.example.com' # Allow access from container. Make sure the DNS entry (or /etc/hosts) points to the correct ip (not 127.)

# Redis
redis__conf_bind: 'fqdn.example.com' # Allow access from container. Make sure the DNS entry (or /etc/hosts) points to the correct ip (not 127.)

# Elasticsearch (if needed)
elasticsearch_oss__network_host: 'fqdn.example.com' # Allow access from container. Make sure the DNS entry (or /etc/hosts) points to the correct ip (not 127.)
```


## Optional Requirements

* It is recommended to set `Storage=presistent` in `/etc/systemd/journald.conf` to allow the user to use `journalctl --user`. This can be done using the [linuxfabrik.lfops.systemd_journald](https://github.com/Linuxfabrik/lfops/tree/main/roles/systemd_journald) role.
* If the host should act as a Postfix MTA, make sure it is listening on the IP address so that the container can reach it. This can be done using the [linuxfabrik.lfops.postfix](https://github.com/Linuxfabrik/lfops/tree/main/roles/postfix) role.


## Tags

| Tag        | What it does                     |
| ---        | ------------                     |
| `mastodon` | Installs and configures Mastodon |
| `mastodon:users` | Creates Mastodon users |


## Mandatory Role Variables
| Variable                  | Description                  |
| --------                  | -----------                  |
| `mastodon__active_record_encryption_deterministic_key` | Generate with `bundle exec rails db:encryption:init`. Changing this will result in data loss and other issues. |
| `mastodon__active_record_encryption_key_derivation_salt` | Generate with `bundle exec rails db:encryption:init`. Changing this will result in data loss and other issues. |
| `mastodon__active_record_encryption_primary_key` | Generate with `bundle exec rails db:encryption:init`. Changing this will result in data loss and other issues. |
| `mastodon__domain` | This is the unique identifier of your server in the network. This cannot be safely changed later. It has to be the public domain name the server is running under. |
| `mastodon__otp_secret` | Generate with `bundle exec rails secret`. Changing this will break two-factor authentication. |
| `mastodon__postgresql_login` | The user account for accessing the PostgreSQL database. |
| `mastodon__secret_key_base` | Generate with `bundle exec rails secret`. Changing this will break all active browser sessions. |
| `mastodon__vapid_private_key` | Generate with `bundle exec rails mastodon:webpush:generate_vapid_key`. Changing this will break push notifications. |
| `mastodon__vapid_public_key` | Generate with `bundle exec rails mastodon:webpush:generate_vapid_key`. Changing this will break push notifications. |

Note: Secrets can be easily generated without installing Mastodon and Ruby locally by running the bundle commands in a temporary container, e.g. `podman run --interactive --rm --tty mastodon/mastodon:latest bundle exec rails secret`.

Example:
```yaml
# mandatory
mastodon__domain: 'example.com'
mastodon__postgresql_login:
  username: 'mastodon'
  password: 'linuxfabrik'
  state: 'present'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `mastodon__container_enabled`| Enables or disables the service, analogous to `systemctl enable/disable`. | `true` |
| `mastodon__container_state` | Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |
| `mastodon__elasticsearch_enabled` | Whether Elasticsearch support is enabled. | `true` |
| `mastodon__elasticsearch_host` | The host on which Elasticsearch is reachable. | `'host.containers.internal'` |
| `mastodon__elasticsearch_port` | The port on which Elasticsearch is reachable. | `9200` |
| `mastodon__ip_retention_period` | How long Mastodon should retain records of IPs. Make sure to modify the scheduling of ip_cleanup_scheduler in config/sidekiq.yml to be less than daily if you lower this below two days (172800). | `31556952` |
| `mastodon__postgresql_db_name` | The name of the PostgreSQL database. | `'mastodon_production'` |
| `mastodon__postgresql_host` | The host on which PostgreSQL is reachable. | `'host.containers.internal'` |
| `mastodon__postgresql_port` | The port on which PostgreSQL is reachable. | `5432` |
| `mastodon__redis_host` | The host on which Redis is reachable. | `'host.containers.internal'` |
| `mastodon__redis_password` | The password for the Redis instance, if authentication is enabled. | `unset` |
| `mastodon__redis_port` | The port on which Redis is reachable. | `6379` |
| `mastodon__session_retention_period` | How long Mastodon should retain records of sessions. | `31556952` |
| `mastodon__smtp_from_address` | The from address Mastodon should use when sending email notifications. | `''` |
| `mastodon__smtp_login` | The login for the SMTP server Mastodon should use in order to send email notifications. | `''` |
| `mastodon__smtp_password` | The password for the SMTP server Mastodon should use in order to send email notifications. | `''` |
| `mastodon__smtp_port` | The port Mastodon should use in order to send email notifications. | `25` |
| `mastodon__smtp_server` | The SMTP server Mastodon should use in order to send email notifications. | `'host.containers.internal'` |
| `mastodon__streaming_port` | The port on which the Mastodon streaming service will be available. | `4000` |
| `mastodon__user_home_directory`| The home directory of the user running Mastodon. | `/opt/mastodon` |
| `mastodon__users__host_var` <br/> / <br/> `mastodon__users__group_var` | A list of dictionaries containing Mastodon users. Subkeys: <ul><li>`username`: Mandatory, string. The username of the Mastodon user.</li><li>`email`: Mandatory, string. The email of the Mastodon user.</li><li>`approve`: Optional, bool. Approve the user. Otherwise the user may need to be approved manually in the webgui before being able to log in. Defaults to `false`.</li><li>`confirm`: Optional, bool. Confirm the users email address. No email confirmation message will be sent to the user. Defaults to `false`.</li><li>`role`: Optional, string. Role of the user. Defaults to `unset`.</li></ul> For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `mastodon__version`| Which Mastodon version to install. Have a look at the available [releases](https://github.com/mastodon/mastodon/releases). | `'latest'` |
| `mastodon__web_domain` | To install Mastodon on `mastodon.example.com` in such a way it can serve `@alice@example.com`, set `mastodon__local_domain` to `example.com` and `mastodon__web_domain` to `mastodon.example.com`. This also requires additional configuration on the server hosting `example.com` to redirect requests from `https://example.com/.well-known/webfinger` to `https://mastodon.example.com/.well-known/webfinger`. | `unset` |
| `mastodon__web_port` | The port on which the Mastodon web service will be available. | `3000` |

Example:
```yaml
# optional
mastodon__container_enabled: true
mastodon__container_state: 'started'
mastodon__elasticsearch_enabled: false
mastodon__postgresql_host: 'db.example.com'
mastodon__postgresql_db_name: 'mastodon-example'
mastodon__smtp_from_address: 'noreply@example.com'
mastodon__smtp_server: 'mail.example.com'
mastodon__user_home_directory: '/opt/Mastodon'
mastodon__users__host_var:
  - name: 'owner'
    email: 'owner@example.com'
    approve: true
    confirm: true
    role: 'Owner'
mastodon__web_domain: 'social.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
