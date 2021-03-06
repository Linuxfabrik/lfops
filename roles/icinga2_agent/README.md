# Ansible Role icinga2_agent

This role installs [Icinga2](https://icinga.com/), configues it to act as an agent, and tries to registers the host in the Icinga Director.

Currently, this role only works if the host can reach the Icinga2 master API.


FQCN: linuxfabrik.lfops.icinga2_agent

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Fedora 35


## Requirements

### Mandatory

* Enable the [Icinga Package Repository](https://packages.icinga.com/). This can be done using the [linuxfabrik.lfops.repo_icinga](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_icinga) role.
* A configured Icinga2 Master.  This can be done using the [linuxfabrik.lfops.icinga2_master](https://github.com/Linuxfabrik/lfops/tree/main/roles/icinga2_master) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag                 | What it does                               |
| ---                 | ------------                               |
| icinga2_agent       | Installs and configues icinga2 as an agent |
| icinga2_agent:state | Manages the state of the Icinga2 service   |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/icinga2_agent/defaults/main.yml) for the variable defaults.


### Mandatory


#### icinga2_agent__icinga2_api_user_login

The account for generating a ticket for this agent using the Icinga2 API. The account needs to have the `actions/generate-ticket` permission on the Icinga2 Master.

Example:
```yaml
icinga2_agent__icinga2_api_user_login:
  username: 'enrolment-user'
  password: 'password'
```


#### icinga2_agent__icinga2_master_host

The host where the Icinga2 Master is running. Has to be reachable from the Agent.

Example:
```yaml
icinga2_agent__icinga2_master_host: 'master.example.com'
```


#### icinga2_agent__windows_version

Mandatory for Windows. The version of the Icinga2 Agent to install. Possible options: https://packages.icinga.com/windows/.

Example:
```yaml
icinga2_agent__windows_version: 'v2.12.8'
```


### Optional

#### icinga2_agent__icingaweb2_url

The URL where the IcingaWeb2 is reachable. This will be used to register the host in the Icinga Director.

Example:
```yaml
icinga2_agent__icingaweb2_url: 'https://monitoring.example.com/icingaweb2'
```


#### icinga2_agent__icingaweb2_user_login

A IcingaWeb2 user with `module/director,director/api,director/hosts` permissions. This will be used to register the host in the Icinga Director.

Example:
```yaml
icinga2_agent__icingaweb2_user_login:
  username: 'enrolment-user'
  password: 'password'
```

#### icinga2_agent__cn

The common name of the Icinga2 Agent. Tries to default to the FQDN of the server.

Default:
```yaml
icinga2_agent__cn: '{{ ansible_facts["nodename"] }}'
```


#### icinga2_agent__director_host_object_address

The host address of the Icinga Director host object. Tries to default to the IPv4 address of the server.
One can try setting this to `{{ ansible_facts["ip_addresses"][0] }}` for Windows servers.

Default:
```yaml
icinga2_agent__director_host_object_address: '{{ ansible_facts["default_ipv4"]["address"] }}'
```


#### icinga2_agent__director_host_object_display_name

The host display name of the Icinga Director host object. Tries to default to the hostname.

Default:
```yaml
icinga2_agent__director_host_object_display_name: '{{ ansible_facts["hostname"] }}'
```


#### icinga2_agent__director_host_object_import

A list of Icinga Director host templates which should be imported for this server.

Default:
```yaml
icinga2_agent__director_host_object_import:
  - 'tpl-host-linux'
```


#### icinga2_agent__icinga2_master_port

The port on which the Icinga2 master is reachable.

Default:
```yaml
icinga2_agent__icinga2_master_port: 5665
```


#### icinga2_agent__bind_host

The bind host. This allows restricting on which IP addresses the Agent is listening.

Default: unset

Example:
```yaml
icinga2_agent__bind_host:
```


#### icinga2_agent__service_enabled

Enables or disables the Icinga2 service, analogous to `systemctl enable/disable --now`. Possible options:

* true
* false

Default:
```yaml
icinga2_agent__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
