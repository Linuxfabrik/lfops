# Ansible Role linuxfabrik.lfops.keycloak

This role installs [Keycloak](https://www.keycloak.org/guides#getting-started).

This role is compatible with the following Keycloak versions:

* Keycloak 24
* Keycloak 25
* Keycloak 26


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* **The tarball is fetched on the Ansible controller** and copied to the target from there, so a target without internet access can still be provisioned. The controller needs to reach `github.com`.
* **Installation is keyed on `version.txt`.** Keycloak ships that file inside its tarball and it names the installed release. The role reads it and skips the download and the extraction when the wanted version is already in place.
* **An upgrade extracts over the existing installation.** Bump `keycloak__version` and re-run the role. Files that the new release no longer ships stay behind, and `providers/`, `themes/` and `data/` are kept. Wipe `/opt/keycloak` by hand first if you want a clean tree.
* **`kc.sh build` only runs when it has to**, that is when the installation or `keycloak.conf` changed. It also acts as the configuration check: an invalid value aborts the run naming the option and the accepted values, before the service is restarted with it. An unknown *option name* is not caught, Keycloak ignores it silently.
* **The bootstrap admin is provisioned once.** See `keycloak__admin_login` and "Post-Installation Steps"; the cleartext password does not stay on disk after the run.
* **The role does not manage TLS certificates.** It only points Keycloak at the paths given in `keycloak__https_certificate_file` and `keycloak__https_certificate_key_file`.
* **Leaving both certificate variables empty selects edge mode**, where a reverse proxy in front of Keycloak terminates TLS. The role then sets `http-enabled=true` and `proxy-headers` itself, so Keycloak builds its URLs from the proxy's forwarded headers instead of from the internal address. Setting the two variables switches to reencrypt/passthrough, where Keycloak terminates TLS itself. See the [Keycloak reverse proxy documentation](https://www.keycloak.org/server/reverseproxy).


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* A MariaDB database and user for Keycloak must be created (role: [linuxfabrik.lfops.mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server)).
* The MariaDB repository must be enabled (role: [linuxfabrik.lfops.repo_mariadb](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_mariadb)).
* The EPEL repository must be enabled (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)).
* The Python MySQL module required by the MariaDB role must be installed (role: [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python)).

The role installs the OpenJDK matching `keycloak__version` itself (OpenJDK 17 for Keycloak 24, OpenJDK 21 for Keycloak 25 and newer).


## Requirements

Keycloak supports one of the following database servers; create a database and a user for it. The "Setup Keycloak" playbook wires up MariaDB for you (see Dependent Roles), the others must be provided separately.

* mariadb
* mssql
* mysql
* oracle
* postgres

Manual steps:

* Optional: If Keycloak itself should terminate TLS (when it does not run behind a reverse proxy, or behind one in reencrypt/passthrough mode), provide the certificate and the private key and point `keycloak__https_certificate_file` and `keycloak__https_certificate_key_file` at them. Run the [linuxfabrik.lfops.acme_sh](https://github.com/Linuxfabrik/lfops/tree/main/roles/acme_sh) playbook to obtain them. Behind a reverse proxy that terminates TLS (edge mode) no certificates are needed and both variables stay empty.

All Keycloak config settings are described here: https://www.keycloak.org/server/all-config


## Post-Installation Steps

The first role run provisions a *temporary* bootstrap admin (`keycloak__admin_login`, by convention suffixed `-temp`) in the `master` realm. Replace it with a permanent admin and remove the bootstrap account afterwards. The order matters: verify that the permanent admin works *before* deleting the bootstrap one, otherwise you risk locking yourself out of the `master` realm.

1. Log in to the Keycloak admin console (`master` realm) as the bootstrap admin (`keycloak__admin_login["username"]`).
2. Create the permanent admin via *Users > Add user*: set a username (e.g. `linuxfabrik-admin`), turn *Email verified* on, then *Create*.
3. *Role mapping > Assign role > Filter by realm roles*: assign the `admin` role.
4. *Credentials > Set password*: set the password with *Temporary* off (otherwise the user must change it on first login), and store it in your password manager.
5. Verify the permanent admin: log out, then log in as the permanent admin in a fresh (incognito) session and confirm the admin console is fully accessible (Realms, Clients and Users are visible).
6. Delete the bootstrap admin: as the permanent admin, go to *Users > `keycloak__admin_login["username"]` > Delete*.
7. The role already removed the `KC_BOOTSTRAP_ADMIN_*` credentials from `/etc/sysconfig/keycloak` and wrote the marker `/etc/ansible/facts.d/keycloak__admin_login_bootstrapped.state` after the first run. Verify this:

    ```bash
    grep --quiet '^KC_BOOTSTRAP_ADMIN_' /etc/sysconfig/keycloak && echo FAIL || echo OK
    test -f /etc/ansible/facts.d/keycloak__admin_login_bootstrapped.state && echo OK || echo FAIL
    ```


## Tags

`keycloak`

* Installs Keycloak, including the bootstrap of the temporary admin account.
* Triggers: keycloak.service restart.

`keycloak:configure`

* Deploys `keycloak.conf`, the sysconfig file and the systemd unit, and rebuilds the server when a build-time option changed.
* Triggers: keycloak.service restart.

`keycloak:logrotate`

* Deploys the logrotate configuration.
* Triggers: none.

`keycloak:state`

* Manages the state of the systemd service.
* Triggers: none.


## Mandatory Role Variables

`keycloak__admin_login`

* The *temporary* Keycloak bootstrap admin login credentials. Keycloak only honors `KC_BOOTSTRAP_ADMIN_USERNAME` / `KC_BOOTSTRAP_ADMIN_PASSWORD` on the very first start, when no admin user exists in the `master` realm yet. Subsequent restarts ignore these variables.
* Mandatory only on the first role run. The role writes the credentials to `/etc/sysconfig/keycloak`, restarts Keycloak so it consumes them and provisions the bootstrap admin in the `master` realm, then immediately re-renders the sysconfig file with the credentials removed and marks the bootstrap as done via `/etc/ansible/facts.d/keycloak__admin_login_bootstrapped.state`. The cleartext password no longer lingers on disk after the role finishes.
* On subsequent runs the role detects the marker file and renders the sysconfig file without credentials right away. `keycloak__admin_login` can be removed from the inventory at that point.
* Use a username that visibly marks the account as throwaway (suffix `-temp`), so it is obvious in the Keycloak UI which account must be deleted once a permanent admin has been created. See "Post-Installation Steps" for the handover to a permanent admin.
* For disaster recovery (e.g. lost database, need to re-bootstrap an admin): remove `/etc/ansible/facts.d/keycloak__admin_login_bootstrapped.state`, re-add `keycloak__admin_login` to the inventory, and re-run the role.
* Type: Dictionary.
* Subkeys:

    * `username`:

        * Mandatory. Username. By convention, end with `-temp` (e.g. `keycloak-admin-temp`) to flag the account as the bootstrap user that must be deleted after the permanent admin is in place.
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

* The version of Keycloak that should be installed. Keycloak 24, 25 and 26 are supported; another major version aborts the run naming the supported ones.
* Possible options: <https://github.com/keycloak/keycloak/releases>.
* Type: String.

Example:
```yaml
# mandatory
keycloak__admin_login:
  username: 'keycloak-admin-temp'
  password: 'linuxfabrik'
keycloak__db_login:
  username: 'keycloak'
  password: 'linuxfabrik'
keycloak__hostname: 'keycloak.example.com'
keycloak__version: '26.1.2'
```


## Optional Role Variables

`keycloak__db_url`

* The full database JDBC URL. If empty, a default URL is set based on the selected database vendor.
* Type: String.
* Default: `''`

`keycloak__db_url_database`

* The database name for Keycloak. If `keycloak__db_url` is set, this option is ignored.
* Type: String.
* Default: `'keycloak'`

`keycloak__db_url_host`

* The host where the database for Keycloak is running. If `keycloak__db_url` is set, this option is ignored.
* Type: String.
* Default: `'localhost'`

`keycloak__db_vendor`

* Specifies the database server Keycloak is supposed to use. Changing this requires a run with the `keycloak:configure` tag, as `kc.sh build` needs to be re-executed. Possible options: `dev-file`, `dev-mem`, `mariadb`, `mssql`, `mysql`, `oracle`, `postgres`, `tidb`. `dev-file` and `dev-mem` are meant for development only.
* Type: String.
* Default: `'mariadb'`

`keycloak__expose_healthcheck_endpoints`

* If the server should expose healthcheck endpoints.
* Type: Bool.
* Default: `true`
* Deviates from the upstream default `false`: a reverse proxy or load balancer in front of Keycloak needs `/health/ready` to tell whether the server is ready for traffic, and Keycloak refers to that endpoint itself while it is still bootstrapping and answering every other request with `503`. The endpoints are served on the management port, not next to the realms.

`keycloak__expose_metrics_endpoints`

* If the server should expose metrics endpoints.
* Type: Bool.
* Default: `true`
* Deviates from the upstream default `false`: it lets a host be scraped without having to reconfigure and restart Keycloak first, and the endpoint is served on the same management port as the health endpoints, not next to the realms.

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

* The cipher suites to enable. An empty list lets Keycloak select a reasonable default.
* Type: List of strings.
* Default: `[]`

`keycloak__https_protocols`

* The TLS protocol versions Keycloak should use. Only applies when HTTPS certificate files are provided.
* Type: List of strings.
* Default: `['TLSv1.3', 'TLSv1.2']`

`keycloak__limit_nofile`

* The open file descriptor limit of the systemd service (`LimitNOFILE`).
* Type: Number.
* Default: `131072`

`keycloak__log`

* The log handlers to enable. Possible options: `console`, `file`, `syslog`.
* Type: List of strings.
* Default: `['file']`
* Deviates from the upstream default `console`: a service logging to the journal only competes with the rest of the host for the journal's rate limit, and a Keycloak instance under load loses messages that way. With `file` in the list the role also deploys a logrotate configuration.

`keycloak__log_file`

* Set the log file path and filename. Only used when `file` is one of `keycloak__log`.
* Type: String.
* Default: `'/var/log/keycloak/keycloak.log'`
* Deviates from the upstream default `data/log/keycloak.log`: that path sits inside the installation directory, which the role overwrites on an upgrade.

`keycloak__logrotate`

* Number of rotated log files to keep. Falls back to `logrotate__rotate` when that is set.
* Type: Number.
* Default: `14`

`keycloak__mode`

* The mode to start Keycloak in. The development mode is targeted for people trying out Keycloak the first time and get it up and running quickly. It also offers convenient defaults for developers, for example to develop a new Keycloak theme. Possible options: `production`, `development`.
* Type: String.
* Default: `'production'`

`keycloak__proxy_headers`

* The proxy headers that should be accepted by the server. Only applies in production mode without HTTPS certificates (edge proxy mode). Possible options: `forwarded`, `xforwarded`.
* Type: String.
* Default: `'xforwarded'`
* Deviates from the upstream default of accepting no proxy headers at all: in edge mode Keycloak sits behind a reverse proxy by definition, and without this it builds its redirect URLs from the internal address.

`keycloak__proxy_trusted_addresses`

* Trusted proxy addresses, as IP addresses or CIDRs. Only applies in production mode without HTTPS certificates (edge proxy mode). An empty list trusts every proxy.
* Type: List of strings.
* Default: `[]`

`keycloak__service_enabled`

* Enables or disables the service at boot, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`keycloak__service_state`

* Controls the systemd service. One of `restarted`, `started`, `stopped`. `reloaded` is not available, Keycloak's unit has no `ExecReload`.
* Type: String.
* Default: `'started'`

`keycloak__spi_sticky_session_encoder_infinispan_should_attach_route`

* Whether the cluster route is attached to cookies, instead of relying on the session affinity of the reverse proxy. See <https://www.keycloak.org/server/reverseproxy#_enable_sticky_sessions>.
* Type: Bool.
* Default: `false`
* Deviates from the upstream default `true`: the route only helps when Keycloak runs clustered behind a proxy that balances on it, and it is the reverse proxy that keeps the session affinity in the setups this role deploys. Upstream moves the same way and marks the enabled state as deprecated.

`keycloak__transaction_default_timeout`

* The default transaction timeout, in seconds. On Keycloak below 26.6.0 it is passed to the server as the Quarkus transaction manager property, from 26.6.0 on as `transaction-default-timeout`.
* Type: Number.
* Default: `3600`
* Deviates from the upstream default `5m`: a realm import and the first start against a large database run well past five minutes and are rolled back at that mark.

`keycloak__transaction_setup_timeout`

* The transaction timeout for database migration, import and export transactions, in seconds. Only applies to Keycloak 26.6.0 and newer.
* Type: Number.
* Default: `3600`
* Deviates from the upstream default `30m`: a schema migration on a large realm can exceed half an hour, and being cut off halfway leaves the migration to be repeated.

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
keycloak__https_cipher_suites:
  - 'TLS_RSA_WITH_AES_128_GCM_SHA256'
keycloak__https_protocols:
  - 'TLSv1.3'
  - 'TLSv1.2'
keycloak__limit_nofile: 131072
keycloak__log:
  - 'file'
keycloak__log_file: '/var/log/keycloak/keycloak.log'
keycloak__logrotate: 14
keycloak__mode: 'production'
keycloak__proxy_headers: 'xforwarded'
keycloak__proxy_trusted_addresses:
  - '192.0.2.30'
keycloak__service_enabled: true
keycloak__service_state: 'started'
keycloak__spi_sticky_session_encoder_infinispan_should_attach_route: false
keycloak__transaction_default_timeout: 3600
keycloak__transaction_setup_timeout: 3600
keycloak__version: '26.1.2'
```


## Troubleshooting

**Role aborts with `Keycloak <version> is not supported by this role`**

* `keycloak__version` names a major version the role ships no Java mapping for. Pin the host to one of the versions listed at the top of this README, or add the mapping to the role's `vars/main.yml`.

**Role fails with `Could not obtain an admin-cli token`**

* On a run where the bootstrap is not yet marked as done (the marker `/etc/ansible/facts.d/keycloak__admin_login_bootstrapped.state` is missing), the role verifies that the bootstrap admin can obtain a token before writing the marker. It waits up to five minutes for this, because Keycloak keeps answering `503` while it creates its database schema and the admin account on the first start, which takes a minute or two on a fresh database. This fails when the bootstrap admin no longer exists, which is the expected end state after the permanent-admin handover (see "Post-Installation Steps") once the `-temp` account has been deleted, combined with a missing marker file (e.g. a fresh Ansible controller, or a lost `/etc/ansible/facts.d`).
* If the handover is already complete, recreate the marker on the target and re-run the role:

    ```bash
    mkdir --parents /etc/ansible/facts.d
    touch /etc/ansible/facts.d/keycloak__admin_login_bootstrapped.state
    ```

* Otherwise, check that `keycloak.service` is running and that `keycloak__admin_login` matches the actual bootstrap admin, then re-run.

**Keycloak logs nothing to `journalctl -u keycloak`**

* By default the role enables the `file` log handler only, so the log goes to `keycloak__log_file`. Add `console` to `keycloak__log` to get the log into the journal as well.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
