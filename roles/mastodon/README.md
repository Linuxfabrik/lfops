# Ansible Role linuxfabrik.lfops.mastodon

This role installs and configures [Mastodon](https://joinmastodon.org/), a federated microblogging platform, as Podman containers.


## Mandatory Requirements

* Enable the PostgreSQL repository. This can be done using the [linuxfabrik.lfops.repo_postgresql](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_postgresql) role.
* Install the PostgreSQL server. This can be done using the [linuxfabrik.lfops.postgresql_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/postgresql_server) role.
* Create a PostgreSQL user for Mastodon. This can be done using the [linuxfabrik.lfops.postgresql_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/postgresql_server) role.
* Install Redis. This can be done using the [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) and [linuxfabrik.lfops.redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis) role.
* Enable the Elasticsearch repository (optional). This can be done using the [linuxfabrik.lfops.repo_elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_elasticsearch) role.
* Install Elasticsearch (optional). This can be done using the [linuxfabrik.lfops.elasticsearch](https://github.com/Linuxfabrik/lfops/tree/main/roles/elasticsearch) role.
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
elasticsearch__network_host: 'fqdn.example.com' # Allow access from container. Make sure the DNS entry (or /etc/hosts) points to the correct ip (not 127.)
```


## Optional Requirements

* It is recommended to set `Storage=presistent` in `/etc/systemd/journald.conf` to allow the user to use `journalctl --user`. This can be done using the [linuxfabrik.lfops.systemd_journald](https://github.com/Linuxfabrik/lfops/tree/main/roles/systemd_journald) role.
* If the host should act as a Postfix MTA, make sure it is listening on the IP address so that the container can reach it. This can be done using the [linuxfabrik.lfops.postfix](https://github.com/Linuxfabrik/lfops/tree/main/roles/postfix) role.


## Tags

`mastodon`

* Installs and configures Mastodon.
* Triggers: none.

`mastodon:configure`

* Deploys Mastodon configuration files.
* Triggers: none.

`mastodon:containers`

* Deploys Mastodon containers.
* Triggers: none.

`mastodon:deploy_search`

* Deploys the Elasticsearch indices.
* Triggers: none.

`mastodon:users`

* Creates Mastodon users.
* Triggers: none.


## Mandatory Role Variables

`mastodon__active_record_encryption_deterministic_key`

* Generate with `bundle exec rails db:encryption:init`. Changing this will result in data loss and other issues.
* Type: String.

`mastodon__active_record_encryption_key_derivation_salt`

* Generate with `bundle exec rails db:encryption:init`. Changing this will result in data loss and other issues.
* Type: String.

`mastodon__active_record_encryption_primary_key`

* Generate with `bundle exec rails db:encryption:init`. Changing this will result in data loss and other issues.
* Type: String.

`mastodon__domain`

* This is the unique identifier of your server in the network. This cannot be safely changed later. It has to be the public domain name the server is running under.
* Type: String.

`mastodon__otp_secret`

* Generate with `bundle exec rails secret`. Changing this will break two-factor authentication.
* Type: String.

`mastodon__postgresql_login`

* The user account for accessing the PostgreSQL database.
* Type: Dictionary.
* Subkeys:

    * `username`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Mandatory. Password.
        * Type: String.

    * `state`:

        * Mandatory. State of the user.
        * Type: String.

`mastodon__secret_key_base`

* Generate with `bundle exec rails secret`. Changing this will break all active browser sessions.
* Type: String.

`mastodon__vapid_private_key`

* Generate with `bundle exec rails mastodon:webpush:generate_vapid_key`. Changing this will break push notifications.
* Type: String.

`mastodon__vapid_public_key`

* Generate with `bundle exec rails mastodon:webpush:generate_vapid_key`. Changing this will break push notifications.
* Type: String.

Note: Secrets can be easily generated without installing Mastodon and Ruby locally by running the bundle commands in a temporary container, e.g. `podman run --rm mastodon/mastodon:latest bundle exec rails secret`.

Example:
```yaml
# mandatory
mastodon__active_record_encryption_deterministic_key: 'insecure_DO_NOT_USE_IN_PRODUCTION_Sml8YNpgR5KhSgbuDu2E2Ib2U3S4laEi'
mastodon__active_record_encryption_key_derivation_salt: 'insecure_DO_NOT_USE_IN_PRODUCTION_EnLFYG1GPMQq32Q3SD5ai0FkyxvKsq4h'
mastodon__active_record_encryption_primary_key: 'insecure_DO_NOT_USE_IN_PRODUCTION_NQtf5CQ0ttTfT7qCbxhrbVKqlNTgxIEW'
mastodon__domain: 'example.com'
mastodon__otp_secret: 'insecure_DO_NOT_USE_IN_PRODUCTION_b07d3de935e63a5caa30b687f876e042a6d9f93902aebcfb880fa3ae30449f27df5e8f2dfec6e8a21ad25166a2337b711fb964bdd2389ca4fd06c40bd0cac924'
mastodon__postgresql_login:
  username: 'mastodon'
  password: 'linuxfabrik'
  state: 'present'
mastodon__secret_key_base: 'insecure_DO_NOT_USE_IN_PRODUCTION_565c24702495cfa599cae4a31d843016f020a8548b169500a4eb64eeb8f29745fe02778dd5b7690c84f627f24da24bb3855cc56800a4a752831ce61970561a95'
mastodon__vapid_private_key: 'insecure_DO_NOT_USE_IN_PRODUCTION_06bsp_1VMSn6fsLC41qoV_Qobgk6ptrrpCQkrsxHOAk='
mastodon__vapid_public_key: 'insecure_DO_NOT_USE_IN_PRODUCTION_BIKa90fBBxJ_iXZDYI6lB6lvoIXN_NfZ44wyC-j_QKEPhq-LaPXc0x-E_PKVjsrv0iBhGMcaWbYYHrKLSbN_pHY='
```


## Optional Role Variables

`mastodon__container_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`mastodon__container_state`

* Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options: `started`, `stopped`, `restarted`, `reloaded`.
* Type: String.
* Default: `'started'`

`mastodon__elasticsearch_enabled`

* Whether Elasticsearch support is enabled.
* Type: Bool.
* Default: `true`

`mastodon__elasticsearch_host`

* The host on which Elasticsearch is reachable.
* Type: String.
* Default: `'host.containers.internal'`

`mastodon__elasticsearch_port`

* The port on which Elasticsearch is reachable.
* Type: Number.
* Default: `9200`

`mastodon__ip_retention_period`

* How long Mastodon should retain records of IPs (in seconds). Make sure to modify the scheduling of `ip_cleanup_scheduler` in `config/sidekiq.yml` to be less than daily if you lower this below two days (172800).
* Type: Number.
* Default: `31556952`

`mastodon__ldap_base`

* The base distinguised name for the LDAP search.
* Type: String.
* Default: `''`

`mastodon__ldap_bind_dn`

* The bind distinguished name to authenticate against the LDAP server.
* Type: String.
* Default: `''`

`mastodon__ldap_enabled`

* Whether to enable the LDAP integration.
* Type: Bool.
* Default: `false`

`mastodon__ldap_host`

* The host on which LDAP is reachable.
* Type: String.
* Default: `''`

`mastodon__ldap_mail`

* The LDAP attribute which Mastodon should use as the account e-mail address.
* Type: String.
* Default: `'mail'`

`mastodon__ldap_method`

* The method to connect to the LDAP server. Possible options: `'start_tls'`, `'simple_tls'`.
* Type: String.
* Default: `'start_tls'`

`mastodon__ldap_password`

* The password for the LDAP bind distinguished name.
* Type: String.
* Default: `''`

`mastodon__ldap_port`

* The port on which LDAP is reachable.
* Type: Number.
* Default: `389`

`mastodon__ldap_search_filter`

* LDAP search filter for mapping users. Mastodon `%<uid>s` with `mastodon__ldap_uid`, `%<mail>s` with `mastodon__ldap_mail` and `%s<email>s` with the e-mail address to look up.
* Type: String.
* Default: `'(|(%<uid>s=%<email>s)(%<mail>s=%<email>s))'`

`mastodon__ldap_tls_no_verify`

* Whether Mastodon should not verify SSL connections to the LDAP server (e.g. when using self-signed certificates).
* Type: Bool.
* Default: `true`

`mastodon__ldap_uid`

* The LDAP attribute which Mastodon should use as the account username.
* Type: String.
* Default: `'uid'`

`mastodon__ldap_uid_conversion_enabled`

* Mastodon does not allow certain characters in usernames. Enable automatic conversion of usernames that do not conform.
* Type: Bool.
* Default: `true`

`mastodon__postgresql_db_name`

* The name of the PostgreSQL database.
* Type: String.
* Default: `'mastodon_production'`

`mastodon__postgresql_host`

* The host on which PostgreSQL is reachable.
* Type: String.
* Default: `'host.containers.internal'`

`mastodon__postgresql_port`

* The port on which PostgreSQL is reachable.
* Type: Number.
* Default: `5432`

`mastodon__redis_host`

* The host on which Redis is reachable.
* Type: String.
* Default: `'host.containers.internal'`

`mastodon__redis_password`

* The password for the Redis instance, if authentication is enabled.
* Type: String.
* Default: `''`

`mastodon__redis_port`

* The port on which Redis is reachable.
* Type: Number.
* Default: `6379`

`mastodon__session_retention_period`

* How long Mastodon should retain records of sessions (in seconds).
* Type: Number.
* Default: `31556952`

`mastodon__smtp_auth_method`

* How Mastodon should authenticate against the SMTP server. Possible options: `'none'` no authentication, `'plain'` authentication with plaintext password, `'login'` authentication with base64 encoded password, `'cram_md5'`.
* Type: String.
* Default: `'none'`

`mastodon__smtp_from_address`

* The from address Mastodon should use when sending email notifications.
* Type: String.
* Default: `''`

`mastodon__smtp_login`

* The login for the SMTP server Mastodon should use in order to send email notifications.
* Type: String.
* Default: `''`

`mastodon__smtp_openssl_verify_mode`

* How Mastodon should verify/enforce SSL connections to the SMTP server. Possible options: `'none'`, `'peer'`, `'client_once'`, `'fail_if_no_peer_cert'`.
* Type: String.
* Default: `'none'`

`mastodon__smtp_password`

* The password for the SMTP server Mastodon should use in order to send email notifications.
* Type: String.
* Default: `''`

`mastodon__smtp_port`

* The port Mastodon should use in order to send email notifications.
* Type: Number.
* Default: `25`

`mastodon__smtp_server`

* The SMTP server Mastodon should use in order to send email notifications.
* Type: String.
* Default: `'host.containers.internal'`

`mastodon__streaming_port`

* The port on which the Mastodon streaming service will be available.
* Type: Number.
* Default: `4000`

`mastodon__user_home_directory`

* The home directory of the user running Mastodon.
* Type: String.
* Default: `'/opt/mastodon'`

`mastodon__users__host_var` / `mastodon__users__group_var`

* A list of dictionaries containing Mastodon users. For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `username`:

        * Mandatory. The username of the Mastodon user.
        * Type: String.

    * `email`:

        * Mandatory. The email of the Mastodon user.
        * Type: String.

    * `approve`:

        * Optional. Approve the user. Otherwise the user may need to be approved manually in the webgui before being able to log in.
        * Type: Bool.
        * Default: `false`

    * `confirm`:

        * Optional. Confirm the users email address. No email confirmation message will be sent to the user.
        * Type: Bool.
        * Default: `false`

    * `role`:

        * Optional. Role of the user.
        * Type: String.
        * Default: unset

`mastodon__version`

* Which Mastodon version to install. Have a look at the available [releases](https://github.com/mastodon/mastodon/releases).
* Type: String.
* Default: `'latest'`

`mastodon__web_domain`

* To install Mastodon on `mastodon.example.com` in such a way it can serve `@alice@example.com`, set `mastodon__local_domain` to `example.com` and `mastodon__web_domain` to `mastodon.example.com`. This also requires additional configuration on the server hosting `example.com` to redirect requests from `https://example.com/.well-known/webfinger` to `https://mastodon.example.com/.well-known/webfinger`.
* Type: String.
* Default: unset

`mastodon__web_port`

* The port on which the Mastodon web service will be available.
* Type: Number.
* Default: `3000`

Example:
```yaml
# optional
mastodon__container_enabled: true
mastodon__container_state: 'started'
mastodon__elasticsearch_enabled: true
mastodon__elasticsearch_host: 'elasticsearch.example.com'
mastodon__elasticsearch_port: 9200
mastodon__ip_retention_period: 172800
mastodon__ldap_base: 'dc=example,dc=com'
mastodon__ldap_bind_dn: 'uid=freeipa-reader,cn=sysaccounts,cn=etc,dc=example,dc=com'
mastodon__ldap_enabled: true
mastodon__ldap_host: 'id.example.com'
mastodon__ldap_mail: 'mail'
mastodon__ldap_method: 'simple_tls'
mastodon__ldap_password: 'linuxfabrik'
mastodon__ldap_port: 636
mastodon__ldap_search_filter: '(&(|(%<uid>s=%<email>s)(%<mail>s=%<email>s))(objectclass=inetorgperson)(memberof=cn=mastodon_user_group,cn=groups,cn=accounts,dc=example,dc=com))'
mastodon__ldap_tls_no_verify: true
mastodon__ldap_uid: 'uid'
mastodon__ldap_uid_conversion_enabled: false
mastodon__postgresql_db_name: 'mastodon-example'
mastodon__postgresql_host: 'db.example.com'
mastodon__postgresql_port: 5432
mastodon__redis_host: 'redis.example.com'
mastodon__redis_password: 'linuxfabrik'
mastodon__redis_port: 6379
mastodon__session_retention_period: 172800
mastodon__smtp_auth_method: 'login'
mastodon__smtp_from_address: 'noreply@example.com'
mastodon__smtp_login: 'mastodon'
mastodon__smtp_openssl_verify_mode: false
mastodon__smtp_password: 'linuxfabrik'
mastodon__smtp_port: 25
mastodon__smtp_server: 'mail.example.com'
mastodon__streaming_port: 8081
mastodon__user_home_directory: '/opt/Mastodon'
mastodon__users__host_var:
  - name: 'owner'
    email: 'owner@example.com'
    approve: true
    confirm: true
    role: 'Owner'
mastodon__version: 'v4.3.9'
mastodon__web_domain: 'social.example.com'
mastodon__web_port: 8080
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
