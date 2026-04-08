# Ansible Role linuxfabrik.lfops.keycloak

This role installs [Keycloak](https://www.keycloak.org/guides#getting-started).


## Mandatory Requirements

Minimum supported Keycloak version:

* Keycloak 24.0.0

Make sure you have OpenJDK installed.

* Keycloak 25+: OpenJDK 21
* Keycloak 24+: OpenJDK 17

Install one of the following database servers and create a database and a user for said database. For MariaDB, this can be done using the [linuxfabrik.lfops.mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server) role.

* mariadb
* mssql
* mysql
* oracle
* postgres

If Keycloak itself should terminate TLS (e.g. when not running behind a reverse proxy, or when using a reverse proxy in reencrypt/passthrough mode), you need to provide SSL/TLS certificates via `keycloak__https_certificate_file` and `keycloak__https_certificate_key_file`. This can be done using the [linuxfabrik.lfops.acme_sh](https://github.com/Linuxfabrik/lfops/tree/main/roles/acme_sh) role. When running behind a reverse proxy that terminates TLS (edge mode), no certificates are needed, and you can leave the certificate variables empty (the default).

If you use the ["Setup Keycloak" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_keycloak.yml), this installation is automatically done for you (you still have to take care of providing the required versions).

All Keycloak config settings are described here: https://www.keycloak.org/server/all-config


## Tags

`keycloak`

* Installs Keycloak.
* Triggers: keycloak.service restart.

`keycloak:configure`

* Deploy Keycloak config and sysconfig file, and create keycloak service.
* Triggers: keycloak.service restart.

`keycloak:state`

* Manages the state of the systemd service.
* Triggers: none.


## Mandatory Role Variables

`keycloak__admin_login`

* The *temporary* Keycloak Admin login credentials. To harden security, create a permanent admin account after logging in as a temporary admin user, and delete the temporary one.
* Type: Dictionary.
* Subkeys:

    * `username`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Mandatory. Password.
        * Type: String.

`keycloak__db_login`

* The database login credentials for keycloak.
* Type: Dictionary.
* Subkeys:

    * `username`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Mandatory. Password.
        * Type: String.

`keycloak__hostname`

* The hostname where keycloak is reachable.
* Type: String.

`keycloak__version`

* The version of Keycloak that should be installed.
* Type: String.

Example:
```yaml
# mandatory
keycloak__admin_login:
  password: 'password'
  username: 'keycloak-admin'
keycloak__db_login:
  password: 'password'
  username: 'keycloak'
keycloak__hostname: 'keycloak.local'
keycloak__version: '26.1.2'
```


## Optional Role Variables

`keycloak__db_url`

* The full database JDBC URL. If not provided, a default URL is set based on the selected database vendor.
* Type: String.
* Default: unset

`keycloak__db_url_database`

* The database name for Keycloak. If the db-url option is set, this option is ignored.
* Type: String.
* Default: `'keycloak'`

`keycloak__db_url_host`

* The host where the database for Keycloak is running. If the db-url option is set, this option is ignored.
* Type: String.
* Default: `'localhost'`

`keycloak__db_vendor`

* Specifies the database server Keycloak is supposed to use. Changing this requires a full run with the `keycloak` tag, as `kc.sh build` needs to be re-executed. Possible options: `mariadb`, `mssql`, `mysql`, `oracle`, `postgres`.
* Type: String.
* Default: `'mariadb'`

`keycloak__expose_healthcheck_endpoints`

* If the server should expose healthcheck endpoints.
* Type: Bool.
* Default: `true`

`keycloak__expose_metrics_endpoints`

* If the server should expose metrics endpoints.
* Type: Bool.
* Default: `true`

`keycloak__hostname_backchannel_dynamic`

* Enables dynamic resolving of backchannel URLs, including hostname, scheme, port and context path. Set to `true` if your application accesses Keycloak via a private network. If set to `true`, `keycloak__hostname` needs to be specified as a full URL.
* Type: Bool.
* Default: `false`

`keycloak__https_certificate_file`

* The file path to a server certificate or certificate chain in PEM format. Only needed when Keycloak itself terminates TLS (reencrypt/passthrough). Leave empty for edge proxy setups where the reverse proxy handles TLS.
* Type: String.
* Default: `''`

`keycloak__https_certificate_key_file`

* The file path to a private key in PEM format. Only needed when Keycloak itself terminates TLS (reencrypt/passthrough). Leave empty for edge proxy setups where the reverse proxy handles TLS.
* Type: String.
* Default: `''`

`keycloak__https_cipher_suites`

* The cipher suites to use. If none is given, a reasonable default is selected.
* Type: String.
* Default: unset

`keycloak__https_protocols`

* The TLS protocol versions Keycloak should use. Only applies when HTTPS certificate files are provided.
* Type: String.
* Default: `'TLSv1.3,TLSv1.2'`

`keycloak__log`

* Enable one or more log handlers in a comma-separated list.
* Type: String.
* Default: `'file'`

`keycloak__log_file`

* Set the log file path and filename.
* Type: String.
* Default: `'/var/log/keycloak/keycloak.log'`

`keycloak__mode`

* The mode to start Keycloak in. The development mode is targeted for people trying out Keycloak the first time and get it up and running quickly. It also offers convenient defaults for developers, for example to develop a new Keycloak theme. Possible options: `production`, `development`.
* Type: String.
* Default: `'production'`

`keycloak__proxy_headers`

* The proxy headers that should be accepted by the server. Only applies in production mode without HTTPS certificates (edge proxy mode).
* Type: String.
* Default: `'xforwarded'`

`keycloak__proxy_trusted_addresses`

* A comma separated list of trusted proxy addresses. Only applies in production mode without HTTPS certificates (edge proxy mode).
* Type: String.
* Default: unset

`keycloak__service_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`keycloak__spi_sticky_session_encoder_infinispan_should_attach_route`

* https://www.keycloak.org/server/reverseproxy#_enable_sticky_sessions
* Type: Bool.
* Default: `false`

`keycloak__state`

* Controls the Systemd service. One of `started`, `stopped`, `reloaded`.
* Type: String.
* Default: `'started'`

Example:
```yaml
# optional
keycloak__db_url: 'jdbc:mariadb://localhost/keycloak/'
keycloak__db_url_database: 'keycloak'
keycloak__db_url_host: 'localhost'
keycloak__db_vendor: 'mariadb'
keycloak__expose_healthcheck_endpoints: true
keycloak__expose_metrics_endpoints: true
keycloak__hostname_backchannel_dynamic: false
keycloak__https_certificate_file: '/etc/pki/tls/certs/www.example.com-chain.crt'
keycloak__https_certificate_key_file: '/etc/pki/tls/private/www.example.com.key'
keycloak__https_cipher_suites: 'TLS_RSA_WITH_AES_128_GCM_SHA256'
keycloak__https_protocols: 'TLSv1.3,TLSv1.2'
keycloak__log: 'file'
keycloak__log_file: '/var/log/keycloak/keycloak.log'
keycloak__mode: 'production'
keycloak__proxy_headers: 'xforwarded'
keycloak__proxy_trusted_addresses: '10.0.0.2'
keycloak__service_enabled: true
keycloak__spi_sticky_session_encoder_infinispan_should_attach_route: false
keycloak__state: 'started'
```


## Using a reverse proxy

See the [Keycloak reverse proxy documentation](https://www.keycloak.org/server/reverseproxy) for details. When running behind a reverse proxy that terminates TLS (edge mode), leave the HTTPS certificate variables empty. The role will automatically set `http-enabled=true` and `proxy-headers` (default: `xforwarded`). Optionally set `keycloak__proxy_trusted_addresses` to restrict which proxy addresses are trusted. When the reverse proxy does not terminate TLS (reencrypt/passthrough), provide certificate paths via `keycloak__https_certificate_file` and `keycloak__https_certificate_key_file`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
