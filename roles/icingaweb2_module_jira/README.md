# Ansible Role linuxfabrik.lfops.icingaweb2_module_jira

This role installs and configures the [IcingaWeb2 Jira Module](https://github.com/Icinga/icingaweb2-module-jira).

This role is tested with the following IcingaWeb2 Jira Module versions:

* 1.3.4


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.
* The module requires you to create two custom fields in Jira that represent "icingaKey" and "icingaStatus". Have a look at `icingaweb2_module_jira__key_fields_icinga_key` and `icingaweb2_module_jira__key_fields_icinga_status`.


## Tags

| Tag                      | What it does                                       | Reload / Restart |
| ---                      | ------------                                       | ---------------- |
| `icingaweb2_module_jira` | Installs and configures the IcingaWeb2 Jira Module | - |


## Mandatory Role Variables

| Variable                               | Description                                                                                                 |
| --------                               | -----------                                                                                                 |
| `icingaweb2_module_jira__api_host`     | String. Hostname or IP address of the Jira API.                                                                     |
| `icingaweb2_module_jira__api_password` | String. Password of the Jira API.                                                                                   |
| `icingaweb2_module_jira__api_username` | String. Username of the Jira API.                                                                                   |
| `icingaweb2_module_jira__version`      | String. The module version to install. Possible options: https://github.com/Icinga/icingaweb2-module-jira/releases. |

Example:
```yaml
# mandatory
icingaweb2_module_jira__api_host: 'jira.example.com'
icingaweb2_module_jira__api_password: 'icinga-user'
icingaweb2_module_jira__api_username: 'linuxfabrik'
icingaweb2_module_jira__version: 'v1.3.4'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icingaweb2_module_jira__api_path` | String. Path of the Jira API, relative to `icingaweb2_module_jira__api_host`. | `''` |
| `icingaweb2_module_jira__api_port` | Integer. Port of the Jira API. | `''` |
| `icingaweb2_module_jira__api_scheme` | String. Scheme of the Jira API. One of `'http'` or `'https'`. | `''` |
| `icingaweb2_module_jira__deployment_legacy` | Boolean. If legacy compatibility should be enabled or not. | `true` |
| `icingaweb2_module_jira__deployment_type` | String. The deployment type of Jira. One of `'cloud'` or `'server'`. | `'cloud'` |
| `icingaweb2_module_jira__icingaweb2_url` | String. The IcingaWeb2 URL for links pointing back to IcingaWeb2 in the Jira issues. | `''` |
| `icingaweb2_module_jira__key_fields_icinga_key` | String. Custom field in Jira to figure out whether an issue for the given object already exists. | `'icingaKey'` |
| `icingaweb2_module_jira__key_fields_icinga_status` | String. Custom field in Jira that represents the status of icinga object. | `'icingaStatus'` |
| `icingaweb2_module_jira__ui_issuetype` | Default issue type to be used for creating Jira tickets. Please note that the project settings must represent project keys, not display names. | `''` |
| `icingaweb2_module_jira__ui_project` | Default project to be used for creating Jira tickets. Please note that the project settings must represent project keys, not display names. | `''` |
| `icingaweb2_module_jira__url` | The URL from where to download the IcingaWeb2 Jira Module. | `https://github.com/Icinga/icingaweb2-module-jira/archive/{{ icingaweb2_module_jira__version }}.tar.gz` |

Example:
```yaml
# optional
icingaweb2_module_jira__api_path: ''
icingaweb2_module_jira__api_port: ''
icingaweb2_module_jira__api_scheme: ''
icingaweb2_module_jira__deployment_legacy: true
icingaweb2_module_jira__deployment_type: 'cloud'
icingaweb2_module_jira__icingaweb2_url: ''
icingaweb2_module_jira__key_fields_icinga_key: 'icingaKey'
icingaweb2_module_jira__key_fields_icinga_status: 'icingaStatus'
icingaweb2_module_jira__ui_issuetype: ''
icingaweb2_module_jira__ui_project: ''
icingaweb2_module_jira__url: 'https://github.com/Icinga/icingaweb2-module-jira/archive/{{ icingaweb2_module_jira__version }}.tar.gz'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
