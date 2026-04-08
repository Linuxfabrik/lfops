# Ansible Role linuxfabrik.lfops.grafana

This role installs and configures [Grafana](https://grafana.com/).


## Mandatory Requirements

* Enable the official [Grafana OSS Repository](https://grafana.com/docs/grafana/latest/installation/rpm/). This can be done using the [linuxfabrik.lfops.repo_grafana](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_grafana) role.


## Tags

`grafana`

* Installs and configures Grafana.
* Triggers: grafana-server.service restart.

`grafana:configure`

* Deploys the Grafana config files.
* Triggers: grafana-server.service restart.

`grafana:plugins`

* Manages Grafana Plugins.
* Triggers: grafana-server.service restart.

`grafana:provisioning`

* Deploys the Grafana provisioning config files.
* Triggers: grafana-server.service restart.

`grafana:service_accounts`

* Creates Service Accounts and their tokens.
* Triggers: none.

`grafana:state`

* Manages the state of the systemd service.
* Triggers: none.


## Mandatory Role Variables

`grafana__admin_login`

* The Grafana admin account.
* Type: Dictionary.

`grafana__root_url`

* The root url on which Grafana is reachable.
* Type: String.

Example:
```yaml
# mandatory
grafana__admin_login:
  username: 'grafana-admin-user'
  password: 'linuxfabrik'
grafana__root_url: 'https://monitoring.example.com/grafana'
```


## Optional Role Variables

`grafana__allow_embedding`

* Whether to allow browsers to render Grafana in a `<frame>`, `<iframe>`, `<embed>` or `<object>`.
* Type: Bool.
* Default: `true`

`grafana__api_url`

* The url on which the Grafana API is reachable. This might differ from the `grafana__root_url` when running a Grafana cluster behind a loadbalancer.
* Type: String.
* Default: `'{{ grafana__root_url }}'`

`grafana__auth_anonymous_enabled`

* Whether to allow anonymous (passwordless) access or not. Possible options: `true` or `false`.
* Type: Bool.
* Default: `false`

`grafana__auth_anonymous_org_name`

* The organization name that should be used for unauthenticated users.
* Type: String.
* Default: `'Main Org.'`

`grafana__auth_anonymous_org_role`

* The role for unauthenticated users.
* Type: String.
* Default: `'Viewer'`

`grafana__auth_jwt`

* Enable JWT-based authentication for Grafana requests.
* Type: Bool.
* Default: `false`

`grafana__auth_jwt__priv_key_file`

* Path to the private key file used to verify JWT signatures for Grafana authentication.
* Type: String.
* Default: `'/etc/grafana/jwt.key.priv'`

`grafana__auth_jwt__pub_key_file`

* Path to the public key file used to verify JWT signatures for Grafana authentication.
* Type: String.
* Default: `'/etc/grafana/jwt.key.pub'`

`grafana__bitwarden_collection_id`

* Will be used to store the token of the created service accounts to this Bitwarden Collection. Can be obtained from the URL in Bitwarden WebGUI.
* Type: String.
* Default: `'{{ lfops__bitwarden_collection_id | default() }}'`

`grafana__bitwarden_organization_id`

* Will be used to store the token of the created service accounts to this Bitwarden Organization. Can be obtained from the URL in Bitwarden WebGUI.
* Type: String.
* Default: `'{{ lfops__bitwarden_organization_id | default() }}'`

`grafana__cookie_samesite`

* The [SameSite cookie attribute](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite). Possible options: `disabled`, `lax`, `none`, `strict`.
* Type: String.
* Default: `'lax'`

`grafana__https_config`

* Determines whether HTTPS is enabled or not.
* Type: Dictionary.
* Default: unset
* Subkeys:

    * `cert_file`:

        * Mandatory. The path of the certificate file used for SSL encryption.
        * Type: String.

    * `cert_key`:

        * Mandatory. The path of the certificate key file used for SSL encryption.
        * Type: String.

`grafana__ldap_config`

* The configuration to use a LDAP user base for logging into Grafana. More information can be found [here](https://grafana.com/docs/grafana/latest/auth/ldap/).
* Type: Dictionary.
* Default: unset
* Subkeys:

    * `host`:

        * Optional. The host on which the LDAP server is accessible. Specify multiple hosts space separated.
        * Type: String.
        * Default: `'127.0.0.1'`

    * `port`:

        * Optional. The port on which the LDAP server is accessible.
        * Type: Number.
        * Default: `389`

    * `use_ssl`:

        * Optional. If an encrypted TLS connection should be used.
        * Type: Bool.
        * Default: `false`

    * `ssl_skip_verify`:

        * Optional. If the ssl cert validation should be skipped.
        * Type: Bool.
        * Default: `false`

    * `bind_dn`:

        * Mandatory. The distinguished name of the account which should be used to login to the LDAP server.
        * Type: String.

    * `bind_password`:

        * Mandatory. The password of the account which should be used to login to the LDAP server.
        * Type: String.

    * `search_base_dns`:

        * Mandatory. List of base dns to search through for users.
        * Type: List.

    * `search_filter`:

        * Mandatory. A LDAP user filter expression.
        * Type: String.

    * `group_search_base_dns`:

        * Optional. List of base dns to search through for groups.
        * Type: List.

    * `group_search_filter_user_attribute`:

        * Optional. The `%s` in the search filter will be replaced by this.
        * Type: List.

    * `group_search_filter`:

        * Optional. A LDAP filter, to retrieve the groups of which the user is a member (only set if memberOf attribute is not available).
        * Type: String.

    * `admin_group_dn`:

        * Optional. The distinguished name of the LDAP group that should be Grafana admins.
        * Type: String.

    * `editor_group_dn`:

        * Optional. The distinguished name of the LDAP group that should be Grafana editors.
        * Type: String.

    * `viewer_group_dn`:

        * Optional. The distinguished name of the LDAP group that should be Grafana viewers.
        * Type: String.

    * `email`:

        * Optional. Email attribute in the LDAP directory.
        * Type: String.
        * Default: `'email'`

    * `username`:

        * Optional. Username attribute in the LDAP directory.
        * Type: String.
        * Default: `'cn'`

`grafana__plugins__group_var` / `grafana__plugins__host_var`

* Grafana plugins.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the plugin. Can be found using `grafana-cli plugins list-remote`.
        * Type: String.

    * `state`:

        * Optional. Either `present` or `absent`. Defaults to `present`.
        * Type: String.

`grafana__provisioning_dashboards__group_var` / `grafana__provisioning_dashboards__host_var`

* The dashboards to deploy via provisioning. Have a look at https://grafana.com/docs/grafana/latest/administration/provisioning/#dashboards for the subkeys.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `state`:

        * Optional. Either `present` or `absent`. Defaults to `present`.
        * Type: String.

`grafana__provisioning_datasources__group_var` / `grafana__provisioning_datasources__host_var`

* The datasources to deploy via provisioning. Have a look at https://grafana.com/docs/grafana/latest/administration/provisioning/#data-sources for the subkeys.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `state`:

        * Optional. Either `present` or `absent`. Defaults to `present`.
        * Type: String.

`grafana__provisioning_service_accounts__group_var` / `grafana__provisioning_service_accounts__host_var`

* [Service accounts](https://grafana.com/docs/grafana/latest/administration/service-accounts/) to create. It automatically creates a token for the service account, with the same role as the service account itself. Beware that the token is only displayed once during the Ansible run, or optionally saved to Bitwarden.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the service account.
        * Type: String.

    * `role`:

        * Optional. Role of the service account. Possible options: `'Admin'`, `'Editor'` or `'Viewer'`. Defaults to `'Viewer'`.
        * Type: String.

    * `state`:

        * Optional. Either `present` or `absent`. Defaults to `present`.
        * Type: String.

`grafana__serve_from_sub_path`

* Whether Grafana itself should run on a subpath or not. Only effective if there is a subpath in `grafana__root_url`.
* Type: Bool.
* Default: `false`

`grafana__service_enabled`

* Enables or disables the service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

`grafana__skip_token_to_bitwarden`

* Skip the storing of the service account tokens to Bitwarden.
* Type: Bool.
* Default: `false`

`grafana__smtp_config`

* Email server settings. More information can be found here: https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/#smtp.
* Type: Dictionary.
* Default: unset
* Subkeys:

    * `host`:

        * Optional. The host and port on which the SMTP server is accessible.
        * Type: String.
        * Default: `'localhost:25'`

    * `user`:

        * Optional. The user, in case of SMTP auth.
        * Type: String.

    * `password`:

        * Optional. The password, in case of SMTP auth.
        * Type: String.

    * `cert_file`:

        * Optional. File path to a cert file.
        * Type: String.

    * `key_file`:

        * Optional. File path to a key file.
        * Type: String.

    * `skip_verify`:

        * Optional. If the ssl cert validation should be skipped.
        * Type: Bool.
        * Default: `false`

    * `from_name`:

        * Optional. Name to be used when sending out emails.
        * Type: String.
        * Default: `'Grafana'`

    * `from_address`:

        * Optional. Address used when sending out emails.
        * Type: String.
        * Default: `'admin@grafana.localhost'`

`grafana__users_case_insensitive_login`

* Have a look at https://grafana.com/blog/2022/12/12/guide-to-using-the-new-grafana-cli-user-identity-conflict-tool-in-grafana-9.3
* Type: Bool.
* Default: unset

`grafana__validate_certs`

* If set to `false`, the role will not validate SSL certificates when connecting to Grafana via `grafana__root_url`. This is useful when using self-signed certificates.
* Type: Bool.
* Default: `true`

Example:
```yaml
# optional
grafana__allow_embedding: true
grafana__api_url: 'https://grafana01.example.com/grafana'
grafana__auth_anonymous_enabled: false
grafana__auth_anonymous_org_name: 'Main Org.'
grafana__auth_anonymous_org_role: 'Viewer'
grafana__auth_jwt: false
grafana__auth_jwt__priv_key_file: '/etc/grafana/jwt.key.priv'
grafana__auth_jwt__pub_key_file: '/etc/grafana/jwt.key.pub'
grafana__cookie_samesite: 'lax'
grafana__https_config:
  cert_file: '/etc/ssl/ssl-certificate.crt'
  cert_key: '/etc/ssl/ssl-certificate.key'
grafana__ldap_config:
  username: 'uid'
  bind_dn: 'uid=freeipa-reader,cn=sysaccounts,cn=etc,dc=example,dc=com'
  bind_password: 'linuxfabrik'
  editor_group_dn: 'cn=monitoring,cn=groups,cn=accounts,dc=example,dc=com'
  host: 'ldap.example.com'
  port: 389
  search_base_dns:
    - 'cn=users,cn=accounts,dc=example,dc=com'
  search_filter: '(uid=%s)' # or for example: '(cn=%s)' or '(sAMAccountName=%s)'
  viewer_group_dn: '*'
grafana__plugins__group_var: []
grafana__plugins__host_var:
  - name: 'yesoreyeram-infinity-datasource'
grafana__provisioning_dashboards__group_var: []
grafana__provisioning_dashboards__host_var:
  - name: 'linuxfabrik-monitoring-plugins'
    orgId: 1
    folder: 'Linuxfabrik Monitoring Plugins'
    folderUid: 'linuxfabrik-monitoring-plugins'
    type: 'file'
    disableDeletion: false
    editable: false
    updateIntervalSeconds: 60
    options:
      path: '/var/lib/grafana/dashboards/linuxfabrik-monitoring-plugins'
grafana__provisioning_datasources__group_var: []
grafana__provisioning_datasources__host_var:
  - name: 'InfluxDB'
    type: 'influxdb'
    access: 'proxy'
    orgId: 1
    url: 'http://{{ icinga2_master__influxdb_host }}:8086'
    user: '{{ icinga2_master__influxdb_login["username"] }}'
    database: '{{ icinga2_master__influxdb_database_name }}'
    isDefault: true
    jsonData:
       timeInterval: '1m'
       tlsAuth: false
       tlsAuthWithCACert: false
    secureJsonData:
      password: '{{ icinga2_master__influxdb_login["password"] }}'
    version: 1
    editable: false
  - name: 'icinga_director'
    type: 'mysql'
    access: 'proxy'
    orgId: 1
    url: '{{ icingaweb2_module_director__database_host }}:3306'
    user: '{{ icingaweb2_module_director__database_login["username"] }}'
    database: '{{ icingaweb2_module_director__database_name }}'
    isDefault: false
    secureJsonData:
      password: '{{ icingaweb2_module_director__database_login["password"] }}'
    version: 1
    editable: false
grafana__provisioning_service_accounts__group_var: []
grafana__provisioning_service_accounts__host_var:
  - name: 'grizzly'
    role: 'Admin'
grafana__serve_from_sub_path: false
grafana__service_enabled: true
grafana__skip_token_to_bitwarden: true
grafana__smtp_config:
  host: 'mail.example.com:25'
  user: 'smtp-user'
  password: 'linuxfabrik'
  from_address: 'grafana@example.com'
grafana__users_case_insensitive_login: false
grafana__validate_certs: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
