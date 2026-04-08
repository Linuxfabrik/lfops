# Ansible Role linuxfabrik.lfops.apache_solr

This role installs [Apache Solr 8+](https://solr.apache.org) (the full binary package, for all operating systems). Parallel installation of multiple versions and switching between them is supported. We do not make use of Solr's `install_solr_service.sh` script due to idempotency reasons (we ported it to Ansible instead).

This Ansible role

* supports Basic authentication for users with the use of the `BasicAuthPlugin`,
* and supports Rule-based authorization with the `RuleBasedAuthorizationPlugin`,
* but currently does not create any cores or collections.


## Mandatory Requirements

* Install Java 11+. This can be done using the [linuxfabrik.lfops.apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps) role. Java OpenJDK latest is recommended.

If you use the [Apache Solr Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/apache_solr.yml), this is automatically done for you.


## Tags

`apache_solr`

* Installs and configures the whole Apache Solr server and deploys `bin/solr.in.sh`, `log4j.xml.j2` and `security.json`.
* Triggers: solr.service restart.

`apache_solr:state`

* Manages the state of `solr.service`.
* Triggers: none.

`apache_solr:user`

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
# apache_solr__checksum: 'sha512:fcd1ca482744f4a72c21c59d1877f3aeeb4b8683cf89af70bb10d29fc07da1858628b2666e3c363227e4b2f7a8ef33c2b63065811ae1c2f2843fe9f09305cb59'
# apache_solr__version: '9.3.0'
apache_solr__checksum: 'sha512:7147caaec5290049b721f9a4e8b0c09b1775315fc4aa790fa7a88a783a45a61815b3532a938731fd583e91195492c4176f3c87d0438216dab26a07a4da51c1f5'
apache_solr__version: '9.4.0'
```


## Optional Role Variables

`apache_solr__data_dir`

* [SOLR_DATA_HOME](https://solr.apache.org/guide/solr/latest/configuration-guide/index-location-format.html).
* Type: String.
* Default: `'/var/solr/data'`

`apache_solr__group`

* Group running the systemd service.
* Type: String.
* Default: `'solr'`

`apache_solr__http_bind_address`

* [SOLR_JETTY_HOST](https://solr.apache.org/guide/solr/latest/deployment-guide/taking-solr-to-production.html#security-considerations).
* Type: String.
* Default: `'0.0.0.0'`

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

        * Mandatory. Apache Solr permissions assigned to this role. Have a look at the example for all possible values.
        * Type: List of strings.

    * `state`:

        * Optional. Either `present` or `absent`.
        * Type: String.

`apache_solr__service`

* Name of the systemd service.
* Type: String.
* Default: `'solr'`

`apache_solr__service_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`apache_solr__stop_wait`

* Waiting up to $SOLR_STOP_WAIT seconds to see Solr running on port $SOLR_PORT.
* Type: Number.
* Default: `15`

`apache_solr__user`

* Username running the systemd service.
* Type: String.
* Default: `'solr'`

`apache_solr__users__group_var` / `apache_solr__users__host_var`

* This Ansible role supports Basic authentication for users with the use of the `BasicAuthPlugin`, which only provides user authentication. To control user permissions, you may need to configure `apache_solr__roles__group_var` / `apache_solr__roles__host_var`. Note: The 'all' permission should always be the last permission in your config so that more specific permissions are applied first.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `username`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Mandatory. Password.
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
apache_solr__http_bind_address: '0.0.0.0'
apache_solr__http_bind_port: 8983
apache_solr__install_dir: '/opt'
apache_solr__log4j_props: '/var/solr/log4j2.xml'
apache_solr__log_level: 'INFO'
apache_solr__logs_dir: '/var/log/solr'
apache_solr__pid_dir: '/var/solr'
apache_solr__service: 'solr'
apache_solr__service_enabled: true
apache_solr__stop_wait: 15
apache_solr__user: 'solr'
apache_solr__var_dir: '/var/solr'

apache_solr__roles__host_var:
  - name: 'reader'
    permissions:
      - 'config-read'
      - 'filestore-read'
      - 'metrics-read'
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


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
