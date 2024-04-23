# Ansible Role linuxfabrik.lfops.keycloak

This role installs [keycloak](https://www.keycloak.org/guides#getting-started).


## Mandatory Requirements

* Make sure you have OpenJDK installed.

  * Keycloak < 20: OpenJDK 11
  * Keycloak >= 20: OpenJDK 17

* Install one of the following database servers and create a database and a user for said database. For MariaDB, this can be done using the [linuxfabrik.lfops.mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server) role.

  * mariadb
  * mssql
  * mysql
  * oracle
  * postgres

If you use the ["Setup Keycloak" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_keycloak.yml), this installation is automatically done for you (you still have to take care of providing the required versions).


## Tags

| Tag        | What it does      |
| ---        | ------------      |
| `keycloak` | Installs keycloak |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `keycloak__apps__apps__host_var` / `keycloak__apps__apps__group_var` | The version of Keycloak that should be installed. |
| `keycloak__admin_login` | The Keycloak Admin login credentials. Subkeys:<br> * `username`: Mandatory, string. Username.<br> * `password`: Mandatory, string. Password. |
| `keycloak__db_login` | The database login credentials for keycloak. Subkeys:<br> * `username`: Mandatory, string. Username.<br> * `password`: Mandatory, string. Password. |
| `keycloak__hostname` | The hostname where keycloak is reachable. |
| `keycloak__java_package_name` | The Java package to be installed. |
| `keycloak__version` | The version of Keycloak that should be installed. |

Example:
```yaml
# mandatory
keycloak__apps__apps__host_var:
  - name: 'java-17-openjdk'
    state: 'present'
keycloak__admin_login:
  password: 'password'
  username: 'keycloak-admin'
keycloak__db_login:
  password: 'password'
  username: 'keycloak'
keycloak__hostname: 'keycloak.local'
keycloak__version: '18.0.0'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `keycloak__db_url` | The full database JDBC URL. If not provided, a default URL is set based on the selected database vendor. | `unset` |
| `keycloak__db_url_database` | The database name for keycloak. If the db-url option is set, this option is ignored. | `keycloak` |
| `keycloak__db_url_host` | The host where the database for keycloak is running. If the db-url option is set, this option is ignored. | `localhost` |
| `keycloak__db_vendor` | Specifies the database server keycloak is supposed to use. Possible options:<br> * mariadb<br> * mssql<br> * mysql<br> * oracle<br> * postgres | `mariadb` |
| `keycloak__expose_healthcheck_endpoints` | If the server should expose healthcheck endpoints. | `true` |
| `keycloak__expose_metrics_endpoints` | If the server should expose metrics endpoints. | `true` |
| `keycloak__https_protocols` | The cipher suites Keycloak is supposed to be using. | `TLSv1.3,TLSv1.2` |
| `keycloak__https_cipher_suites` | The cipher suites to use. If none is given, a reasonable default is selected. | `unset` |
| `keycloak__log` | Enable one or more log handlers in a comma-separated list. | `file` |
| `keycloak__log_file` | Set the log file path and filename. | `/var/log/keycloak/keycloak.log` |
| `keycloak__mode` | The mode to start Keycloak in. The development mode is targeted for people trying out Keycloak the first time and get it up and running quickly. It also offers convenient defaults for developers, for example to develop a new Keycloak theme.<br>Possible options:<br> * `production`<br> * `development` | `production` |
| `keycloak__proxy_mode` | The proxy address forwarding mode if the server is behind a reverse proxy.<br>* edge: Enables communication through HTTP between the proxy and Keycloak. This mode is suitable for deployments with a highly secure internal network where the reverse proxy keeps a secure connection (HTTP over TLS) with clients while communicating with Keycloak using HTTP.<br>* reencrypt: Requires communication through HTTPS between the proxy and Keycloak. This mode is suitable for deployments where internal communication between the reverse proxy and Keycloak should also be protected. Different keys and certificates are used on the reverse proxy as well as on Keycloak.<br>* passthrough: Enables communication through HTTP or HTTPS between the proxy and Keycloak. This mode is suitable for deployments where the reverse proxy is not terminating TLS. The proxy instead is forwarding requests to the Keycloak server so that secure connections between the server and clients are based on the keys and certificates used by the Keycloak server. | `unset` |

Example:
```yaml
# optional
keycloak__db_url_host: 'localhost'
keycloak__db_url_database: 'keycloak'
keycloak__db_url: 'jdbc:mariadb://localhost/keycloak/'
keycloak__db_vendor: 'mariadb'
keycloak__expose_healthcheck_endpoints: 'true'
keycloak__expose_metrics_endpoints: 'true'
keycloak__https_protocols: 'TLSv1.3,TLSv1.2'
keycloak__https_cipher_suites: 'TLS_RSA_WITH_AES_128_GCM_SHA256'
keycloak__log: 'file'
keycloak__log_file: '/var/log/keycloak/keycloak.log'
keycloak__mode: 'production'
keycloak__proxy_mode: 'edge'
```

## keycloak__proxy_mode

Configure the reverse proxy:

Some Keycloak features rely on the assumption that the remote address of the HTTP request connecting to Keycloak is the real IP address of the clients machine.

When you have a reverse proxy or loadbalancer in front of Keycloak, this might not be the case, so please make sure your reverse proxy is configured correctly by performing these actions:

Set the `X-Forwarded-For`, `X-Forwarded-Proto`, and `X-Forwarded-Host` HTTP headers.

To set these headers, consult the documentation for your reverse proxy.

Take extra precautions to ensure that the X-Forwarded-For header is set by your reverse proxy. If this header is incorrectly configured, rogue clients can set this header and trick Keycloak into thinking the client is connected from a different IP address than the actual address. This precaution can more be critical if you do any deny or allow listing of IP addresses.

Exposed path recommendations
When using a reverse proxy, Keycloak only requires certain paths need to be exposed. The following table shows the recommended paths to expose.

| Keycloak Path | Reverse Proxy Path | Exposed        | Reason                                                  |
| ------------- | ------------------ | -------        | ------                                                  |
| /       | -          | No         | When exposing all paths, admin paths are exposed unnecessarily.                     |
| /admin/   | -          | No           | Exposed admin paths lead to an unnecessary attack vector.                         |
| /js/      | -          | Yes (see note below) | Access to keycloak.js needed for "internal" clients, e.g. the account console.              |
| /welcome/   | -          | No           | No need exists to expose the welcome page after initial installation.                   |
| /realms/    | /realms/       | Yes          | This path is needed to work correctly, for example, for OIDC endpoints.                 |
| /resources/ | /resources/    | Yes          | This path is needed to serve assets correctly. It may be served from a CDN instead of the Keycloak path.  |
| /robots.txt   | /robots.txt      | Yes          | Search engine rules.                                            |
| /metrics    | -          | No           | Exposed metrics lead to an unnecessary attack vector.                           |
| /health     | -          | No           | Exposed health checks lead to an unnecessary attack vector.                       |


Note:

As it’s true that the js path is needed for internal clients like the account console, it’s good practice to use keycloak.js from a JavaScript package manager like npm or yarn for your external clients.


## On the webconsole

If you try to configure the administrative user via the web console on a remote machine you will encounter an error. This is prohibited because of potential security risks. Therefore, creating the administrative user via the web admin console is only allowed when running on localhost.
As a consequence, you have to set the following environment variables first before executing the start command:

1. export KEYCLOAK_ADMIN=admin
2. export KEYCLOAK_ADMIN_PASSWORD=linuxfabrik


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
