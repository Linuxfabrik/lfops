# Ansible Role keycloak

This role installs [keycloak](https://www.keycloak.org/guides#getting-started).

FQCN: linuxfabrik.lfops.keycloak

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Fedora


## Requirements

One of the following database servers with `keycloak` database:

| Database  | Tested version |
| --------  | -------------- |
| mariadb 	| 10			 |
| mssql		| 2016			 |
| mysql		| 8				 |
| oracle	| 12c			 |
| postgres	| 10 			 |

Default:
```yaml
keycloak__dbserver: 'mariadb'
```

## Tags

| Tag   	| What it does      |
| ---   	| ------------      |
| keycloak 	| Installs keycloak |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/keycloak/defaults/main.yml) for the variable defaults.


### Mandatory

#### keycloak__mode

Specifies the mode keycloak is supposed to run in.

Possible options:

* production
* development


#### keycloak__admin_user

The Keycloak admin user.


#### keycloak__admin_pass

The Keycloak admin user's password.


#### keycloak__db_user

The database user for keycloak.


#### keycloak__db_password

The Keycloak database user's password.


### Optional

Default:
```yaml
keycloak__mode: 'production'
```

#### keycloak__dbserver

Specifies the database server keycloak is supposed to use.

Possible options:

* mariadb
* mssql
* mysql
* oracle
* postgres

Default:
```yaml
keycloak__dbserver: 'mariadb'
```

### keycloak__proxy_mode

The following proxy modes are available:

* edge: Enables communication through HTTP between the proxy and Keycloak. This mode is suitable for deployments with a highly secure internal network where the reverse proxy keeps a secure connection (HTTP over TLS) with clients while communicating with Keycloak using HTTP.

* reencrypt: Requires communication through HTTPS between the proxy and Keycloak. This mode is suitable for deployments where internal communication between the reverse proxy and Keycloak should also be protected. Different keys and certificates are used on the reverse proxy as well as on Keycloak.

* passthrough: Enables communication through HTTP or HTTPS between the proxy and Keycloak. This mode is suitable for deployments where the reverse proxy is not terminating TLS. The proxy instead is forwarding requests to the Keycloak server so that secure connections between the server and clients are based on the keys and certificates used by the Keycloak server.


Configure the reverse proxy:

Some Keycloak features rely on the assumption that the remote address of the HTTP request connecting to Keycloak is the real IP address of the clients machine.

When you have a reverse proxy or loadbalancer in front of Keycloak, this might not be the case, so please make sure your reverse proxy is configured correctly by performing these actions:

Set the `X-Forwarded-For`, `X-Forwarded-Proto`, and `X-Forwarded-Host` HTTP headers.

To set these headers, consult the documentation for your reverse proxy.

Take extra precautions to ensure that the X-Forwarded-For header is set by your reverse proxy. If this header is incorrectly configured, rogue clients can set this header and trick Keycloak into thinking the client is connected from a different IP address than the actual address. This precaution can more be critical if you do any deny or allow listing of IP addresses.

Exposed path recommendations
When using a reverse proxy, Keycloak only requires certain paths need to be exposed. The following table shows the recommended paths to expose.

| Keycloak Path | Reverse Proxy Path | Exposed				| Reason 																									|
| ------------- | ------------------ | -------				| ------ 																									|
| /			 	| -					 | No					| When exposing all paths, admin paths are exposed unnecessarily.											|
| /admin/		| -					 | No 					| Exposed admin paths lead to an unnecessary attack vector.													|
| /js/			| -					 | Yes (see note below) | Access to keycloak.js needed for "internal" clients, e.g. the account console. 							|
| /welcome/		| -					 | No 					| No need exists to expose the welcome page after initial installation.										|
| /realms/		| /realms/			 | Yes 					| This path is needed to work correctly, for example, for OIDC endpoints.									|
| /resources/	| /resources/		 | Yes 					| This path is needed to serve assets correctly. It may be served from a CDN instead of the Keycloak path.	|
| /robots.txt 	| /robots.txt 		 | Yes 					| Search engine rules.																						|
| /metrics		| -					 | No 					| Exposed metrics lead to an unnecessary attack vector.														|
| /health 		| - 				 | No 					| Exposed health checks lead to an unnecessary attack vector.												|


Note:

As it’s true that the js path is needed for internal clients like the account console, it’s good practice to use keycloak.js from a JavaScript package manager like npm or yarn for your external clients.


## On the webconsole

If you try to configure the administrative user via the web console on a remote machine you will encounter an error. This is prohibited because of potential security risks. Therefore, creating the administrative user via the web admin console is only allowed when running on localhost.
As a consequence, you have to set the following environment variables first before executing the start command:

1. export KEYCLOAK_ADMIN=admin
2. export KEYCLOAK_ADMIN_PASSWORD=secret


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
