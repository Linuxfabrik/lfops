# Ansible Role linuxfabrik.lfops.icinga2_agent

This role installs [Icinga2](https://icinga.com/), configures it to act as an agent, and tries to registers the host in the Icinga Director.

Currently, this role only works if the host can reach the Icinga2 master API.


## Mandatory Requirements

* Enable the [Icinga Package Repository](https://packages.icinga.com/). This can be done using the [linuxfabrik.lfops.repo_icinga](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_icinga) role.
* A configured Icinga2 Master.  This can be done using the [linuxfabrik.lfops.icinga2_master](https://github.com/Linuxfabrik/lfops/tree/main/roles/icinga2_master) role.

| Tag                   | What it does                               |
| ---                   | ------------                               |
| `icinga2_agent`       | Installs and configures icinga2 as an agent |
| `icinga2_agent:state` | Manages the state of the Icinga2 service   |


## Mandatory Role Variables

| Variable                                | Description                                                                                                                                                                              |
| --------                                | -----------                                                                                                                                                                              |
| `icinga2_agent__icinga2_api_user_login` | The account for generating a ticket for this agent using the Icinga2 API (API of Icinga Core). The account needs to have the `actions/generate-ticket` permission on the Icinga2 Master. |
| `icinga2_agent__icinga2_master_cn`      | The common name of the Icinga2 Master.                                                                                                                                                   |
| `icinga2_agent__windows_version`        | Mandatory for Windows. The version of the Icinga2 Agent to install. Possible options: https://packages.icinga.com/windows/.                                                              |

Example:
```yaml
icinga2_agent__icinga2_api_user_login:
  password: 'password'
  username: 'enrolment-user'
icinga2_agent__icinga2_master_cn: 'master.example.com'
icinga2_agent__windows_version: 'v2.12.8'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `icinga2_agent__additional_icinga2_master_endpoints` | A list of dictionaries with additional Icinga2 master endpoints. Subkeys: <br> * `host`: Mandatory, string. Host of the master endpoint. <br> * `port`: Optional, string. Defaults to 5665. The Icinga2 port of the endpoint. | `[]` |
| `icinga2_agent__bind_host` | The bind host. This allows restricting on which IP addresses the Agent is listening. | unset |
| `icinga2_agent__cn` | The common name of the Icinga2 Agent. Tries to default to the FQDN of the server. | `'{{ ansible_facts["nodename"] }}'` |
| `icinga2_agent__director_host_object_address` | The host address of the Icinga Director host object. Tries to default to the IPv4 address of the server. | `'{{ ansible_facts["ip_addresses"][0] }}'` for Windows, else `{{ ansible_facts["default_ipv4"]["address"] }}` |
| `icinga2_agent__director_host_object_display_name` | The host display name of the Icinga Director host object. Tries to default to the hostname. | `'{{ ansible_facts["hostname"] }}'` |
| `icinga2_agent__director_host_object_import` | A list of Icinga Director host templates which should be imported for this server. | `['tpl-host-windows']` for Windows, else `['tpl-host-linux']` |
| `icinga2_agent__icinga2_api_url` | The URL to the Icinga2 API. Will be used to generate the ticket for the agent certificate. | `'https://{{ icinga2_agent__icinga2_master_host }}:{{ icinga2_agent__icinga2_master_port }}'` |
| `icinga2_agent__icinga2_master_host`    | The host where the Icinga2 Master is running. Has to be reachable from the Agent. | `'{{ icinga2_agent__icinga2_master_cn }}'` |
| `icinga2_agent__icinga2_master_port` | The port on which the Icinga2 master is reachable. | `5665` |
| `icinga2_agent__icingaweb2_url` | The URL where the IcingaWeb2 (the API) is reachable. This will be used to register the host in the Icinga Director (otherwise the host is registered in Icinga Core, but not visible in Icinga Director). | `'https://{{ icinga2_agent__icinga2_master_host }}/icingaweb2'` |
| `icinga2_agent__icingaweb2_user_login` | A IcingaWeb2 user with `module/director,director/api,director/hosts` permissions. This will be used to register the host in the Icinga Director. | unset |
| `icinga2_agent__parent_zone` | The Icinga2 parent zone of the host. | `'master'` |
| `icinga2_agent__service_enabled` | Enables or disables the Icinga2 service, analogous to `systemctl enable/disable --now`. | `true` |
| `icinga2_agent__validate_certs` | If false, TLS certificates offered by the Icinga Master will not be validated. This should only set to false used on personally controlled sites using self-signed certificates. | `false` |
| `icinga2_agent__windows_download_path` | The path where the Icinga2.exe will be downloaded to. Certain Windows versions disallow the creation of files in `C:` which requires one to adjust this setting. Note that the path has to exist. | `C:` |
| `icinga2_agent__windows_service_user` | The Windows user account under which the Icinga2 service will be run. | `'NT AUTHORITY\SYSTEM'` |

Example:
```yaml
# optional
icinga2_agent__additional_icinga2_master_endpoints:
  - host: 'master2.example.com'
    port: 5665
  - host: 'master3.example.com'
icinga2_agent__bind_host: '0.0.0.0'
icinga2_agent__cn: '{{ ansible_facts["nodename"] }}'
icinga2_agent__director_host_object_address: '{{ ansible_facts["default_ipv4"]["address"] }}'
icinga2_agent__director_host_object_display_name: '{{ ansible_facts["hostname"] }}'
icinga2_agent__director_host_object_import:
  - 'tpl-host-linux'
icinga2_agent__icinga2_api_url: 'https://master3.example.com:{{ icinga2_agent__icinga2_master_port }}'
icinga2_agent__icinga2_master_host: '192.0.2.10'
icinga2_agent__icinga2_master_port: 5665
icinga2_agent__icingaweb2_url: 'https://monitoring.example.com/icingaweb2'
icinga2_agent__icingaweb2_user_login:
  password: 'password'
  username: 'enrolment-user'
icinga2_agent__parent_zone: 'satellite01'
icinga2_agent__service_enabled: true
icinga2_agent__validate_certs: true
icinga2_agent__windows_download_path: 'D:\Downloads'
icinga2_agent__windows_service_user: 'Icinga Service User'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
