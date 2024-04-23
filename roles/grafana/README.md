# Ansible Role linuxfabrik.lfops.grafana

This role installs and configures [Grafana](https://grafana.com/).


## Mandatory Requirements

* Enable the official [Grafana OSS Repository](https://grafana.com/docs/grafana/latest/installation/rpm/). This can be done using the [linuxfabrik.lfops.repo_grafana](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_grafana) role.


## Tags

| Tag                        | What it does                                  |
| ---                        | ------------                                  |
| `grafana`                  | Installs and configures Grafana               |
| `grafana:configure`        | Deploys the Grafana config files              |
| `grafana:provisioning`     | Deploys the Grafana provisioning config files |
| `grafana:service_accounts` | Creates Service Accounts and their tokens     |


## Mandatory Role Variables

| Variable               | Description                                 |
| --------               | -----------                                 |
| `grafana__admin_login` | The Grafana admin account.                  |
| `grafana__root_url`    | The root url on which Grafana is reachable. |


Example:
```yaml
# mandatory
grafana__admin_login:
  username: 'grafana-admin-user'
  password: 'linuxfabrik'
grafana__root_url: 'https://monitoring.example.com/grafana'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `grafana__allow_embedding` | Whether to allow browsers to render Grafana in a `<frame>`, `<iframe>`, `<embed>` or `<object>`. | `true` |
| `grafana__api_url` | The url on which the Grafana API is reachable. This might differ from the `grafana__root_url` when running a Grafana cluster behind a loadbalancer. | `'{{ grafana__root_url }}'` |
| `grafana__auth_anonymous_enabled` | Whether to allow anonymous (passwordless) access or not. Possible options: `true` or `false` | `false` |
| `grafana__auth_anonymous_org_name` | The organization name that should be used for unauthenticated users. | `'Main Org.'` |
| `grafana__auth_anonymous_org_role` | The role for unauthenticated users. | `'Viewer'` |
| `grafana__bitwarden_collection_id` | Will be used to store the token of the created service accounts to this Bitwarden Collection. Can be obtained from the URL in Bitwarden WebGUI. | `'{{ lfops__bitwarden_collection_id | default() }}'` |
| `grafana__bitwarden_organization_id` | Will be used to store the token of the created service accounts to this Bitwarden Organization. Can be obtained from the URL in Bitwarden WebGUI. | `'{{ lfops__bitwarden_organization_id | default() }}'` |
| `grafana__cookie_samesite` | The [SameSite cookie attribute](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite). Possible options:<br> * disabled<br> * lax<br> * none<br> * strict | `'lax'` |
| `grafana__https_config` | Determines whether HTTPS is enabled or not. Subkeys: <ul><li>`cert_file`: Mandatory, string. The path of the certificate file used for SSL encryption.</li><li>`cert_key`: Mandatory, string. The path of the certificate key file used for SSL encryption.</li></ul> | unset |
| `grafana__ldap_config` | The configuration to use a LDAP user base for logging into Grafana. More information can be found [here](https://grafana.com/docs/grafana/latest/auth/ldap/). Subkeys: <ul><li>`host`: Optional, string. Defaults to `127.0.0.1`. The host on which the LDAP server is accessible. Specify multiple hosts space separated.</li><li>`port`: Optional, integer. Defaults to `389`. The port on which the LDAP server is accessible.</li><li>`use_ssl`: Optional, boolean. Defaults to `false`. If an encrypted TLS connection should be used.</li><li>`ssl_skip_verify`: Optional, boolean. Defaults to `false`. If the ssl cert validation should be skipped.</li><li>`bind_dn`: Mandatory, string. The distinguished name of the account which should be used to login to the LDAP server.</li><li>`bind_password`: Mandatory, string. The password of the account which should be used to login to the LDAP server.</li><li>`search_base_dns`: Mandatory, list. List of base dns to search through for users.</li><li>`search_filter`: Mandatory, string. A LDAP user filter expression.</li><li>`group_search_base_dns`: Optional, list. Defaults to unset. List of base dns to search through for groups.</li><li>`group_search_filter_user_attribute`: Optional, list. Defaults to unset. The `%s` in the search filter will be replaced by this.</li><li>`group_search_filter`: Optional, string. Defaults to unset. A LDAP filter, to retrieve the groups of which the user is a member (only set if memberOf attribute is not available).</li><li>`admin_group_dn`: Optional, string. Defaults to unset. The distinguished name of the LDAP group that should be Grafana admins.</li><li>`editor_group_dn`: Optional, string. Defaults to unset. The distinguished name of the LDAP group that should be Grafana editors.</li><li>`viewer_group_dn`: Optional, string. Defaults to unset. The distinguished name of the LDAP group that should be Grafana viewers.</li><li>`email`: Optional, string. Defaults to `email`. Email attribute in the LDAP directory.</li><li>`username`: Optional, string. Defaults to `cn`. Username attribute in the LDAP directory. | unset |</li></ul>
| `grafana__provisioning_dashboards__group_var`/<br> `grafana__provisioning_dashboards__host_var` | List of dictionaries containing the dashboards to deploy via provisioning. Subkeys: <ul><li>`state`: Optional, string. Either `present` or `absent`. Defaults to `present`.</li><li>Have a look at https://grafana.com/docs/grafana/latest/administration/provisioning/#dashboards for the subkeys. </li></ul><br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `grafana__provisioning_datasources__group_var` /<br> `grafana__provisioning_datasources__host_var` | List of dictionaries containing the datasources to deploy via provisioning. Subkeys: <ul><li>`state`: Optional, string. Either `present` or `absent`. Defaults to `present`.</li><li>Have a look at https://grafana.com/docs/grafana/latest/administration/provisioning/#data-sources for the subkeys.</li></ul><br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `grafana__provisioning_service_accounts__group_var` /<br> `grafana__provisioning_service_accounts__host_var` | List of dictionaries containing [service accounts](https://grafana.com/docs/grafana/latest/administration/service-accounts/) to create. It automatically creates a token for the service account, with the same role as the service account itself. Beware that the token is only displayed once during the Ansible run, or optionally saved to Bitwarden. Subkeys: <ul><li>name: Mandatory, string. Name of the service account.</li><li>role: Optional, string. Role of the service account. Possible options: `'Admin'`, `'Editor'` or `'Viewer'`. Defaults to `'Viewer'`</li><li>`state`: Optional, string. Either `present` or `absent`. Defaults to `present`.</li></ul><br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `grafana__serve_from_sub_path` | Bool. Whether Grafana itself should run on a subpath or not. Only effective if there is a subpath in `grafana__root_url` | `true` |
| `grafana__service_enabled` | Bool. Enables or disables the service, analogous to `systemctl enable/disable --now`. | `true` |
| `grafana__skip_token_to_bitwarden` | Skip the storing of the service account tokens to Bitwarden. | `false` |
| `grafana__smtp_config` | Email server settings. More information can be found here: https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/#smtp. Subkeys:<br> * `host`: Optional, string. Defaults to `localhost:25`. The host and port on which the SMTP server is accessible.<br> * `user`: Optional, string. Defaults to unset. The user, in case of SMTP auth.<br> * `password`: Optional, string. Defaults to unset. The password, in case of SMTP auth.<br> * `cert_file`: Optional, string. Defaults to unset. File path to a cert file.<br> * `key_file`: Optional, string. Defaults to unset. File path to a key file.<br> * `skip_verify`: Optional, string. Defaults to `false`.If the ssl cert validation should be skipped.<br> * `from_name`: Optional, string. Defaults to `Grafana`. Name to be used when sending out emails.<br> * `from_address`: Optional, string. Defaults to `admin@grafana.localhost`. Address used when sending out emails. | unset |
| `grafana__users_case_insensitive_login` | Have a look at https://grafana.com/blog/2022/12/12/guide-to-using-the-new-grafana-cli-user-identity-conflict-tool-in-grafana-9.3 | unset |

Example:
```yaml
# optional
grafana__allow_embedding: true
grafana__api_url: 'https://grafana01.example.com/grafana'
grafana__auth_anonymous_enabled: false
grafana__auth_anonymous_org_name: 'Main Org.'
grafana__auth_anonymous_org_role: 'Viewer'
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
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
