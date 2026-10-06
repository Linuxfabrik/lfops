# Ansible Role linuxfabrik.lfops.apache_solr

This role installs [Apache Solr](https://solr.apache.org) from the full binary package. Parallel installation of multiple versions and switching between them is supported. We do not make use of Solr's `install_solr_service.sh` script due to idempotency reasons (we ported it to Ansible instead).

This Ansible role

* supports Basic authentication for users with the use of the `BasicAuthPlugin`,
* and supports Rule-based authorization with the `RuleBasedAuthorizationPlugin`,
* but currently does not create any cores or collections.

The role installs the Java that the Solr major version needs, from the distribution's repositories:

| Platform                          | Solr 8   | Solr 9  | Solr 10 |
| ---                               | ---      | ---     | ---     |
| Debian 12                         |          | Java 17 |         |
| Debian 13                         |          | Java 21 | Java 21 |
| RHEL 8, RHEL 9                    | Java 8   | Java 17 | Java 21 |
| RHEL 10                           |          | Java 21 | Java 21 |
| Ubuntu 22.04, 24.04, 26.04        |          | Java 17 | Java 21 |

Solr 8 is EOL and only covered where existing installations still run it. Solr 10 starts in SolrCloud mode by default and is not covered by the role's tests.


*Available since LFOps `3.0.0`.*


## How the Role Behaves

* The release tarball is downloaded on the Ansible controller and copied to the target, so the controller needs outbound access to `dlcdn.apache.org` and `archive.apache.org`, the target does not. The download comes from the Apache CDN, which only carries the current releases, and from the much slower Apache archive for every other version.
* As with Solr's own `install_solr_service.sh`, the installation under `apache_solr__install_dir` belongs to `root`, so Solr cannot modify its own program files, while `apache_solr__var_dir` belongs to the Solr user and is not readable for other users.
* Changing `apache_solr__version` installs the new version next to the old one, switches the `solr` symlink to it and restarts Solr. The old version is left in place.
* `security.json` is fully templated from `apache_solr__users__*_var` and `apache_solr__roles__*_var`, so users or permissions added through the Solr API or the Admin UI are overwritten on the next run. The file is only deployed if at least one user is configured.
* Solr applies only the first permission that matches a request. The role therefore writes one Solr permission per permission name, lists every role holding it, places `all` last and adds a role holding `all` to every permission, so such a role is never locked out by a more specific permission.
* Solr 9.11 and newer reject a login whose password equals the username. The role aborts the run for such a user instead of deploying it.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* The tools that Solr's start script and the role need, such as `lsof` and `tar`, must be installed (role: [linuxfabrik.lfops.apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps)).


## Tags

`apache_solr`

* Installs and configures the whole Apache Solr server and deploys `bin/solr.in.sh`, `log4j.xml.j2` and `security.json`.
* Triggers: solr.service restart.

`apache_solr:state`

* Manages the state of `solr.service`.
* Triggers: none.

`apache_solr:users`

* Generates hashed passwords and deploys `security.json`.
* Triggers: solr.service restart.


## Mandatory Role Variables

`apache_solr__checksum`

* The SHA512 checksum according to your version. See `solr-X.X.X.tgz.sha512` file at https://archive.apache.org/dist/solr/solr/ for Solr 9+, https://archive.apache.org/dist/lucene/solr/ for Solr 8-.
* Type: String.

`apache_solr__version`

* The version to install. See https://archive.apache.org/dist/solr/solr/ for Solr 9+, https://archive.apache.org/dist/lucene/solr/ for Solr 8-.
* Type: String.

Example:
```yaml
# mandatory
apache_solr__checksum: 'sha512:0cf320f15662b03844e2d3e983b2a50abab3e643d9aff53ed5a4481ef870776420c7bd8dfde377183d44304dcc589f6784ab020eb7c6675000f86fe32fff4057'
apache_solr__version: '9.11.0'
```


## Optional Role Variables

`apache_solr__data_dir`

* [SOLR_DATA_HOME](https://solr.apache.org/guide/solr/latest/configuration-guide/index-location-format.html).
* Type: String.
* Default: `'/var/solr/data'`

`apache_solr__group`

* Primary group of the Solr user, running the systemd service.
* Type: String.
* Default: `'solr'`

`apache_solr__heap`

* [SOLR_HEAP](https://solr.apache.org/guide/solr/latest/deployment-guide/taking-solr-to-production.html#memory-and-gc-settings), the maximum size of the Java heap.
* Type: String.
* Default: `'512m'`

`apache_solr__http_bind_address`

* [SOLR_JETTY_HOST](https://solr.apache.org/guide/solr/latest/deployment-guide/taking-solr-to-production.html#security-considerations), the address Solr listens on. Set it to `'0.0.0.0'` or to the address of an interface if Solr has to be reachable from other hosts.
* Type: String.
* Default: `'127.0.0.1'`

`apache_solr__http_bind_port`

* [SOLR_PORT](https://solr.apache.org/guide/solr/latest/deployment-guide/upgrading-a-solr-cluster.html#planning-your-upgrade).
* Type: Number.
* Default: `8983`

`apache_solr__install_dir`

* Where to install Apache Solr to.
* Type: String.
* Default: `'/opt'`

`apache_solr__log4j_props`

* [LOG4J_PROPS](https://solr.apache.org/guide/solr/latest/deployment-guide/taking-solr-to-production.html#log-settings).
* Type: String.
* Default: `'/var/solr/log4j2.xml'`

`apache_solr__log_level`

* [SOLR_LOG_LEVEL](https://solr.apache.org/guide/solr/latest/deployment-guide/configuring-logging.html).
* Type: String.
* Default: `'INFO'`

`apache_solr__logs_dir`

* [SOLR_LOGS_DIR](https://solr.apache.org/guide/solr/latest/deployment-guide/configuring-logging.html#permanent-logging-settings).
* Type: String.
* Default: `'/var/log/solr'`

`apache_solr__pid_dir`

* [SOLR_PID_DIR](https://solr.apache.org/guide/solr/latest/deployment-guide/taking-solr-to-production.html#environment-overrides-include-file).
* Type: String.
* Default: `'/var/solr'`

`apache_solr__roles__group_var` / `apache_solr__roles__host_var`

* Roles bridge the gap between users and permissions. The roles can be used with any of the authentication plugins or with a custom authentication plugin if you have created one. You will only need to ensure that logged-in users are mapped to the roles defined by the plugin. The role-to-user mappings must be defined explicitly for every possible authenticated user.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name for the role.
        * Type: String.

    * `permissions`:

        * Mandatory. [Predefined Solr permissions](https://solr.apache.org/guide/solr/latest/deployment-guide/rule-based-authorization-plugin.html#predefined-permissions) assigned to this role. Have a look at the example for all possible values. A role holding `all` is allowed everything.
        * Type: List of strings.

    * `state`:

        * Optional. Either `present` or `absent`.
        * Type: String.

`apache_solr__security_manager_enabled`

* `SOLR_SECURITY_MANAGER_ENABLED`. Enables the Java Security Manager, which confines Solr's file system access to its own directories. Set to `false` if Solr has to follow symlinks pointing outside of them.
* Type: Bool.
* Default: `true`

`apache_solr__service`

* Name of the systemd service.
* Type: String.
* Default: `'solr'`

`apache_solr__service_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`apache_solr__service_state`

* Changes the state of the Apache Solr service, analogous to `systemctl start/stop/restart/reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `apache_solr__service_enabled` is `true`, else `'stopped'`

`apache_solr__stop_wait`

* `SOLR_STOP_WAIT`, the number of seconds Solr gets to stop gracefully before it is killed. Also the number of seconds the start script waits for Solr to listen on its port.
* Type: Number.
* Default: `180`

`apache_solr__user`

* Username running the systemd service.
* Type: String.
* Default: `'solr'`

`apache_solr__users__group_var` / `apache_solr__users__host_var`

* This Ansible role supports Basic authentication for users with the use of the `BasicAuthPlugin`, which only provides user authentication. To control user permissions, you may need to configure `apache_solr__roles__group_var` / `apache_solr__roles__host_var`. At least one user has to remain present once users are configured.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `username`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Mandatory. Password. Must differ from the username on Solr 9.11 and newer.
        * Type: String.

    * `role`:

        * Mandatory. Name of the role the user belongs to.
        * Type: String.

    * `state`:

        * Optional. Either `present` or `absent`.
        * Type: String.

`apache_solr__var_dir`

* The absolute path to the Solr home directory for each Solr node.
* Type: String.
* Default: `'/var/solr'`

Example:
```yaml
# optional
apache_solr__data_dir: '/var/solr/data'
apache_solr__group: 'solr'
apache_solr__heap: '512m'
apache_solr__http_bind_address: '127.0.0.1'
apache_solr__http_bind_port: 8983
apache_solr__install_dir: '/opt'
apache_solr__log4j_props: '/var/solr/log4j2.xml'
apache_solr__log_level: 'INFO'
apache_solr__logs_dir: '/var/log/solr'
apache_solr__pid_dir: '/var/solr'
apache_solr__security_manager_enabled: true
apache_solr__service: 'solr'
apache_solr__service_enabled: true
apache_solr__service_state: 'started'
apache_solr__stop_wait: 180
apache_solr__user: 'solr'
apache_solr__var_dir: '/var/solr'

apache_solr__roles__host_var:
  - name: 'reader'
    permissions:
      - 'config-read'
      - 'filestore-read'
      - 'metrics-read'
      - 'read'
      - 'schema-read'
    state: 'present'
  - name: 'admin'
    permissions:
      # - collection-admin-edit
      # - collection-admin-read
      # - config-edit
      # - config-read
      # - core-admin-edit
      # - core-admin-read
      # - filestore-read
      # - filestore-write
      # - health
      # - metrics-read
      # - package-edit
      # - read
      # - schema-edit
      # - schema-read
      # - security-edit
      # - security-read
      # - update
      # - zk-read
      - 'all'
    state: 'present'

apache_solr__users__host_var:
  - username: 'solr-admin'
    password:
      "{{ lookup('linuxfabrik.lfops.bitwarden_item',
        {
          'hostname': inventory_hostname,
          'purpose': 'Apache Solr',
          'username': 'solr-admin',
          'collection_id': lfops__bitwarden_collection_id,
          'organization_id': lfops__bitwarden_organization_id,
        },
      )['password'] }}"
    role: 'admin'
    state: 'present'
```


## Troubleshooting

**The run aborts with `Solr X.Y.Z needs a Java that <platform> does not ship`**

* The distribution offers no Java that this Solr major version runs on, for example Java 21 for Solr 10 on Debian 12. Install a Solr version the message lists as supported on this platform, or move Solr to a platform from the table at the top.

**The run aborts with `Solr X.Y.Z rejects the login of a user whose password equals the username`**

* Set a password that differs from the username for the listed users. Solr 9.11 and newer refuse such logins.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
