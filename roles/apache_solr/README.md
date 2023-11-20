# Ansible Role linuxfabrik.lfops.apache_solr

This role installs [Apache Solr](https://solr.apache.org) (the full binary package, for all operating systems). Parallel installation of multiple versions and switching between them is supported. We do not make use of Solr's `install_solr_service.sh` script due to idempotency reasons (we ported it to Ansible instead).

This Ansible role

* supports Basic authentication for users with the use of the `BasicAuthPlugin`,
* and supports Rule-based authorization with the `RuleBasedAuthorizationPlugin`,
* but does not create any cores.

Runs on

* RHEL 8 (and compatible)
* RHEL 9 (and compatible)


## Mandatory Requirements

* Install Java 11+. This can be done using the [linuxfabrik.lfops.apps](https://github.com/Linuxfabrik/lfops/tree/main/roles/apps) role.

If you use the [Apache Solr Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/apache_solr.yml), this is automatically done for you.

## Tags

| Tag                      | What it does                                    |
| ---                      | ------------                                    |
| `apache_solr`            | <ul><li>Download and verify Apache Solr `{{ apache_solr__version }}` from Solr archive (the full binary package, for all operating systems)</li><li>Download and verify Apache Solr `{{ apache_solr__version }}` from Lucene archive (the full binary package, for all operating systems)</li><li>Ensure group "`{{ apache_solr__user }}`" exists</li><li>Add the user "`{{ apache_solr__user }}`" with primary group of "`{{ apache_solr__user }}`"</li><li>`mkdir -p {{ apache_solr__install_dir }}/solr-{{ apache_solr__version }}`</li><li>`mkdir -p {{ apache_solr__data_dir }}`</li><li>`mkdir -p {{ apache_solr__logs_dir }}`</li><li>`tar xvzf /tmp/solr-{{ apache_solr__version }}.tgz`</li><li>`ln -s {{ apache_solr__install_dir }}/solr-{{ apache_solr__version }} {{ apache_solr__install_dir }}/solr`</li><li>Deploy `{{ apache_solr__install_dir }}/solr/bin/solr.in.sh`</li><li>Deploy `{{ apache_solr__log4j_props }}`</li><li>`chown -R {{ apache_solr__user }}:{{ apache_solr__user }} {{ apache_solr__install_dir }}/solr`</li><li>`chown -R {{ apache_solr__user }}:{{ apache_solr__user }} {{ apache_solr__var_dir }}`</li><li>`find {{ apache_solr__install_dir }}/solr-{{ apache_solr__version }} -type d -exec chmod --changes 0755 {} \;`</li><li>`find {{ apache_solr__install_dir }}/solr-{{ apache_solr__version }} -type f -exec chmod --changes 0644 {} \;`</li><li>`chmod -R 0755 {{ apache_solr__install_dir }}/solr-{{ apache_solr__version }}/bin`</li><li>`find {{ apache_solr__var_dir }} -type d -exec chmod --changes 0750 {} \;`</li><li>`find {{ apache_solr__var_dir }} -type f -exec chmod --changes 0640 {} \;`</li><li>Deploy `/etc/systemd/system/solr.service`</li><li>`systemctl enable/disable solr.service --now`</li><li>Deploy `{{ apache_solr__var_dir }}/security.json`</li></ul> |
| `apache_solr:state`      | <ul><li>Deploy `/etc/systemd/system/solr.service`</li><li>`systemctl enable/disable solr.service --now`</li><li>Generate hashed passwords</li><li>Deploy `{{ apache_solr__var_dir }}/security.json`</li></ul> |
| `apache_solr:user`      | <ul><li>Generate hashed passwords</li><li>Deploy `{{ apache_solr__var_dir }}/security.json`</li></ul> |


## Mandatory Role Variables

| Variable                             | Description                                                                                                        |
| --------                             | -----------                                                                                                        |
| `apache_solr__checksum` | String. The SHA512 checksum according to your version. See https://archive.apache.org/dist/solr/solr/ for Solr 9+, https://archive.apache.org/dist/lucene/solr/ for Solr 8-. | `'sha512:7147caaec5290049b721f9a4e8b0c09b1775315fc4aa790fa7a88a783a45a61815b3532a938731fd583e91195492c4176f3c87d0438216dab26a07a4da51c1f5'` |
| `apache_solr__version` | The version to install. See https://archive.apache.org/dist/solr/solr/ for Solr 9+, https://archive.apache.org/dist/lucene/solr/ for Solr 8-. |

Example:
```yaml
# mandatory
# apache_solr__checksum: 'sha512:fcd1ca482744f4a72c21c59d1877f3aeeb4b8683cf89af70bb10d29fc07da1858628b2666e3c363227e4b2f7a8ef33c2b63065811ae1c2f2843fe9f09305cb59'
# apache_solr__version: '9.3.0'
apache_solr__checksum: 'sha512:7147caaec5290049b721f9a4e8b0c09b1775315fc4aa790fa7a88a783a45a61815b3532a938731fd583e91195492c4176f3c87d0438216dab26a07a4da51c1f5'
apache_solr__version: '9.4.0'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apache_solr__data_dir` | String. [SOLR_DATA_HOME](https://solr.apache.org/guide/solr/latest/configuration-guide/index-location-format.html) | `'/var/solr/data'` |
| `apache_solr__group` | String. Group running the systemd service. | `'solr'` |
| `apache_solr__http_bind_address` | String. [SOLR_JETTY_HOST](https://solr.apache.org/guide/solr/latest/deployment-guide/taking-solr-to-production.html#security-considerations) | `'0.0.0.0'` |
| `apache_solr__http_bind_port` | Number. [SOLR_PORT](https://solr.apache.org/guide/solr/latest/deployment-guide/upgrading-a-solr-cluster.html#planning-your-upgrade) | `8983` |
| `apache_solr__install_dir` | String. Where to install Apache Solr to. | `'/opt'` |
| `apache_solr__log4j_props` | String. [LOG4J_PROPS](https://solr.apache.org/guide/solr/latest/deployment-guide/taking-solr-to-production.html#log-settings) | `'/var/solr/log4j2.xml'` |
| `apache_solr__log_level` | String. [SOLR_LOG_LEVEL](https://solr.apache.org/guide/solr/latest/deployment-guide/configuring-logging.html) | `'INFO'` |
| `apache_solr__logs_dir` | String. [SOLR_LOGS_DIR](https://solr.apache.org/guide/solr/latest/deployment-guide/configuring-logging.html#permanent-logging-settings) | `'/var/log/solr'` |
| `apache_solr__pid_dir` | String. [SOLR_PID_DIR](https://solr.apache.org/guide/solr/latest/deployment-guide/taking-solr-to-production.html#environment-overrides-include-file) | `'/var/solr'` |
| `apache_solr__roles__group_var`/<br/>`apache_solr__roles__host_var` | List of dictionaries. Roles bridge the gap between users and permissions. The roles can be used with any of the authentication plugins or with a custom authentication plugin if you have created one. You will only need to ensure that logged-in users are mapped to the roles defined by the plugin. The role-to-user mappings must be defined explicitly for every possible authenticated user.<br/>Subkeys: <ul><li>`name`: Mandatory, string. Name for the role.</li><li>`permissions`: Mandatory, list of strings. Apache Solr permissions assigned to this role. Have a look at the example for all possible values.</li><li>`state`: Optional, string. Either `present` or `absent`.</li></ul> | unset (see example bewlow) |
| `apache_solr__service_enabled` | Bool. Enables or disables the service, analogous to `systemctl enable/disable --now`. | `true` |
| `apache_solr__service` | String. Name of the systemd service. | `'solr'` |
| `apache_solr__user` | String. Username running the systemd service. | `'solr'` |
| `apache_solr__users__group_var`/<br/>`apache_solr__users__host_var` | List of dictionaries. This Ansible role supports Basic authentication for users with the use of the `BasicAuthPlugin`, which only provides user authentication. To control user permissions, you may need to configure `apache_solr__roles__group_var` / `apache_solr__roles__host_var`.<br/>Note: The 'all' permission should always be the last permission in your config so that more specific permissions are applied first.<br/>Subkeys: <ul><li>`username`: Mandatory, string. Username.</li><li>`password`: Mandatory, string. Password.</li><li>`role`: Mandatory, string. Name of the role the user belongs to.</li><li>`state`: Optional, string. Either `present` or `absent`.</li></ul> | unset (see example bewlow) |
| `apache_solr__var_dir` | String. The absolute path to the Solr home directory for each Solr node. | `'/var/solr'` |

Example:
```yaml
# optional
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
