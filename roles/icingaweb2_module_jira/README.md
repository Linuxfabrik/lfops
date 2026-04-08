# Ansible Role linuxfabrik.lfops.icingaweb2_module_jira

This role installs and configures the [IcingaWeb2 Jira Module](https://github.com/Icinga/icingaweb2-module-jira).

This role is tested with the following IcingaWeb2 Jira Module versions:

* 1.3.4


## Mandatory Requirements

* A configured IcingaWeb2. This can be done using the [linuxfabrik.lfops.icingaweb2](https://github.com/linuxfabrik/lfops/tree/main/roles/icingaweb2) role.
* The module requires you to create two custom fields in Jira that represent "icingaKey" and "icingaStatus". Have a look at `icingaweb2_module_jira__key_fields_icinga_key` and `icingaweb2_module_jira__key_fields_icinga_status`.


## Tags

`icingaweb2_module_jira`

* Installs and configures the IcingaWeb2 Jira Module.
* Triggers: none.


## Mandatory Role Variables

`icingaweb2_module_jira__api_host`

* Hostname or IP address of the Jira API.
* Type: String.

`icingaweb2_module_jira__api_password`

* Password of the Jira API.
* Type: String.

`icingaweb2_module_jira__api_username`

* Username of the Jira API.
* Type: String.

`icingaweb2_module_jira__version`

* The module version to install. Possible options: https://github.com/Icinga/icingaweb2-module-jira/releases.
* Type: String.

Example:

```yaml
# mandatory
icingaweb2_module_jira__api_host: 'jira.example.com'
icingaweb2_module_jira__api_password: 'icinga-user'
icingaweb2_module_jira__api_username: 'linuxfabrik'
icingaweb2_module_jira__version: 'v1.3.4'
```


## Optional Role Variables

`icingaweb2_module_jira__api_path`

* Path of the Jira API, relative to `icingaweb2_module_jira__api_host`.
* Type: String.
* Default: `''`

`icingaweb2_module_jira__api_port`

* Port of the Jira API.
* Type: String.
* Default: `''`

`icingaweb2_module_jira__api_scheme`

* Scheme of the Jira API. One of `'http'` or `'https'`.
* Type: String.
* Default: `''`

`icingaweb2_module_jira__deployment_legacy`

* If legacy compatibility should be enabled or not.
* Type: Bool.
* Default: `true`

`icingaweb2_module_jira__deployment_type`

* The deployment type of Jira. One of `'cloud'` or `'server'`.
* Type: String.
* Default: `'cloud'`

`icingaweb2_module_jira__icingaweb2_url`

* The IcingaWeb2 URL for links pointing back to IcingaWeb2 in the Jira issues.
* Type: String.
* Default: `''`

`icingaweb2_module_jira__key_fields_icinga_key`

* Custom field in Jira to figure out whether an issue for the given object already exists.
* Type: String.
* Default: `'icingaKey'`

`icingaweb2_module_jira__key_fields_icinga_status`

* Custom field in Jira that represents the status of icinga object.
* Type: String.
* Default: `'icingaStatus'`

`icingaweb2_module_jira__ui_issuetype`

* Default issue type to be used for creating Jira tickets. Please note that the project settings must represent project keys, not display names.
* Type: String.
* Default: `''`

`icingaweb2_module_jira__ui_project`

* Default project to be used for creating Jira tickets. Please note that the project settings must represent project keys, not display names.
* Type: String.
* Default: `''`

`icingaweb2_module_jira__url`

* The URL from where to download the IcingaWeb2 Jira Module.
* Type: String.
* Default: `'https://github.com/Icinga/icingaweb2-module-jira/archive/{{ icingaweb2_module_jira__version }}.tar.gz'`

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
