# Ansible Role linuxfabrik.lfops.keycloak

This role installs [Keycloak](https://www.keycloak.org/guides#getting-started).


## Mandatory Requirements

Make sure you have OpenJDK installed.

* Keycloak 25+: OpenJDK 21
* Keycloak 20+: OpenJDK 17

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

| Tag        | What it does      | Reload / Restart |
| ---        | ------------      | ---------------- |
| `keycloak` | Installs Keycloak | Restarts keycloak.service |
| `keycloak:configure` | Deploy Keycloak config and sysconfig file, and create keycloak service | Restarts keycloak.service |
| `keycloak:state` | Manages the state of the systemd service | - |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `keycloak__admin_login` | Dict. The *temporary* Keycloak Admin login credentials. To harden security, create a permanent admin account after logging in as a temporary admin user, and delete the temporary one. Subkeys:<br> * `username`: Mandatory, string. Username.<br> * `password`: Mandatory, string. Password. |
| `keycloak__db_login` | Dict. The database login credentials for keycloak. Subkeys:<br> * `username`: Mandatory, string. Username.<br> * `password`: Mandatory, string. Password. |
| `keycloak__hostname` | String. The hostname where keycloak is reachable. |
| `keycloak__version` | String. The version of Keycloak that should be installed. |

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

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `keycloak__db_url` | String. The full database JDBC URL. If not provided, a default URL is set based on the selected database vendor. | `unset` |
| `keycloak__db_url_database` | String. The database name for Keycloak. If the db-url option is set, this option is ignored. | `keycloak` |
| `keycloak__db_url_host` | String. The host where the database for Keycloak is running. If the db-url option is set, this option is ignored. | `localhost` |
| `keycloak__db_vendor` | String. Specifies the database server Keycloak is supposed to use. Possible options:<br> * mariadb<br> * mssql<br> * mysql<br> * oracle<br> * postgres | `mariadb` |
| `keycloak__expose_healthcheck_endpoints` | Bool. If the server should expose healthcheck endpoints. | `true` |
| `keycloak__expose_metrics_endpoints` | Bool. If the server should expose metrics endpoints. | `true` |
| `keycloak__hostname_strict_backchannel` | Bool. By default backchannel URLs are dynamically resolved from request headers to allow internal and external applications. | `false` |
| `keycloak__https_certificate_file` | String. The file path to a server certificate or certificate chain in PEM format. Only needed when Keycloak itself terminates TLS (reencrypt/passthrough). Leave empty for edge proxy setups where the reverse proxy handles TLS. | `''` |
| `keycloak__https_certificate_key_file` | String. The file path to a private key in PEM format. Only needed when Keycloak itself terminates TLS (reencrypt/passthrough). Leave empty for edge proxy setups where the reverse proxy handles TLS. | `''` |
| `keycloak__https_cipher_suites` | String. The cipher suites to use. If none is given, a reasonable default is selected. | `unset` |
| `keycloak__https_protocols` | String. The TLS protocol versions Keycloak should use. Only applies when HTTPS certificate files are provided. | `TLSv1.3,TLSv1.2` |
| `keycloak__log` | String. Enable one or more log handlers in a comma-separated list. | `file` |
| `keycloak__log_file` | String. Set the log file path and filename. | `/var/log/keycloak/keycloak.log` |
| `keycloak__mode` | String. The mode to start Keycloak in. The development mode is targeted for people trying out Keycloak the first time and get it up and running quickly. It also offers convenient defaults for developers, for example to develop a new Keycloak theme.<br>Possible options:<br> * `production`<br> * `development` | `production` |
| `keycloak__proxy_headers` | String. The proxy headers that should be accepted by the server. | `'xforwarded'` |
| `keycloak__proxy_trusted_addresses` | String. A comma separated list of trusted proxy addresses. | `'127.0.0.1'` |
| `keycloak__service_enabled` | Bool. Enables or disables the service, analogous to `systemctl enable/disable --now`. | `true` |
| `keycloak__spi_sticky_session_encoder_infinispan_should_attach_route` | Bool. https://www.keycloak.org/server/reverseproxy#_enable_sticky_sessions | `false` |
| `keycloak__state`| String. Controls the Systemd service. One of<br> * `started`<br> * `stopped`<br> * `reloaded` | `'started'` |

Example:
```yaml
# optional
keycloak__db_url: 'jdbc:mariadb://localhost/keycloak/'
keycloak__db_url_database: 'keycloak'
keycloak__db_url_host: 'localhost'
keycloak__db_vendor: 'mariadb'
keycloak__expose_healthcheck_endpoints: true
keycloak__expose_metrics_endpoints: true
keycloak__hostname_strict_backchannel: false
keycloak__https_certificate_file: '/etc/pki/tls/certs/www.example.com-chain.crt'
keycloak__https_certificate_key_file: '/etc/pki/tls/private/www.example.com.key'
keycloak__https_cipher_suites: 'TLS_RSA_WITH_AES_128_GCM_SHA256'
keycloak__https_protocols: 'TLSv1.3,TLSv1.2'
keycloak__log: 'file'
keycloak__log_file: '/var/log/keycloak/keycloak.log'
keycloak__mode: 'production'
keycloak__service_enabled: true
keycloak__spi_sticky_session_encoder_infinispan_should_attach_route: false
keycloak__state: 'started'
```


## Using a reverse proxy

See the [Keycloak reverse proxy documentation](https://www.keycloak.org/server/reverseproxy) for details. The `proxy-headers` option (default: `xforwarded`) controls which reverse proxy headers Keycloak accepts. When running behind a reverse proxy that terminates TLS (edge mode), leave the HTTPS certificate variables empty, as the role will set `http-enabled=true` automatically. When the reverse proxy does not terminate TLS (reencrypt/passthrough), provide certificate paths via `keycloak__https_certificate_file` and `keycloak__https_certificate_key_file`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
