# Ansible Role linuxfabrik.lfops.grafana

This role installs and configures [Grafana](https://grafana.com/).

Tested on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Enable the official [Grafana OSS Repository](https://grafana.com/docs/grafana/latest/installation/rpm/). This can be done using the [linuxfabrik.lfops.repo_grafana](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_grafana) role.


## Tags

| Tag       | What it does                    |
| ---       | ------------                    |
| `grafana` | Installs and configures Grafana |


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
  password: 'my-secret-password'
grafana__root_url: 'https://monitoring.example.com/grafana'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `grafana__allow_embedding` | Whether to allow browsers to render Grafana in a <frame>, <iframe>, <embed> or <object>. | `true` |
| `grafana__auth_anonymous_enabled` | Whether to allow anonymous (passwordless) access or not. Possible options: | `false` |
| `grafana__auth_anonymous_org_name` | The organization name that should be used for unauthenticated users. | `'Main Org.'` |
| `grafana__auth_anonymous_org_role` | The role for unauthenticated users. | `'Viewer'` |
| `grafana__cookie_samesite` | The [SameSite cookie attribute](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite). Possible options:<br> * disabled<br> * lax<br> * none<br> * strict | `'lax'` |
| `grafana__ldap_config` | The configuration to use a LDAP user base for logging into Grafana. More information can be found here: https://grafana.com/docs/grafana/latest/auth/ldap/. Subkeys:<br> * `host`: Optional, string. Defaults to `127.0.0.1`. The host on which the LDAP server is accessible.<br> * `port`: Optional, integer. Defaults to `389`. The port on which the LDAP server is accessible.<br> * `use_ssl`: Optional, boolean. Defaults to `false`. If an encrypted TLS connection should be used.<br> * `bind_dn`: Required, string. The distinguished name of the account which should be used to login to the LDAP server.<br> * `bind_password`: Required, string. The password of the account which should be used to login to the LDAP server.<br> * `search_base_dns`: Required, list. List of base dns to search through for users.<br> * `search_filter`: Required, string. A LDAP user filter expression.<br> * `group_search_base_dns`: Optional, list. Defaults to unset. List of base dns to search through for groups.<br> * `group_search_filter_user_attribute`: Optional, list. Defaults to unset. The `%s` in the search filter will be replaced by this.<br> * `group_search_filter`: Optional, string. Defaults to unset. A LDAP filter, to retrieve the groups of which the user is a member (only set if memberOf attribute is not available).<br> * `admin_group_dn`: Optional, string. Defaults to unset. The distinguished name of the LDAP group that should be Grafana admins.<br> * `editor_group_dn`: Optional, string. Defaults to unset. The distinguished name of the LDAP group that should be Grafana editors.<br> * `viewer_group_dn`: Optional, string. Defaults to unset. The distinguished name of the LDAP group that should be Grafana viewers.<br> * `email`: Optional, string. Defaults to `email`. Email attribute in the LDAP directory.<br> * `username`: Optional, string. Defaults to `cn`. Username attribute in the LDAP directory. | unset |
| `grafana__service_enabled` | Enables or disables the Grafana service, analogous to `systemctl enable/disable --now`. Possible options: | `true` |

Example:
```yaml
# optional
grafana__allow_embedding: true
grafana__auth_anonymous_enabled: false
grafana__auth_anonymous_org_name: 'Main Org.'
grafana__auth_anonymous_org_role: 'Viewer'
grafana__cookie_samesite: 'lax'
grafana__ldap_config:
  host: 'ldap.example.com'
  port: 389
  bind_dn: 'uid=freeipa-reader,cn=sysaccounts,cn=etc,dc=example,dc=com'
  bind_password: 'my-secret-password'
  search_filter: '(uid=%s)' # or for example: '(cn=%s)' or '(sAMAccountName=%s)'
  search_base_dns:
    - 'cn=users,cn=accounts,dc=example,dc=com'
  attribute_username: 'uid'
  editor_group_dn: 'cn=monitoring,cn=groups,cn=accounts,dc=example,dc=com'
  viewer_group_dn: '*'
grafana__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)