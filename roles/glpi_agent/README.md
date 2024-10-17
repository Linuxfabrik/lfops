# Ansible Role linuxfabrik.lfops.glpi_agent

This role installs and configures the [GLPI Agent](https://glpi-agent.readthedocs.io).


## Mandatory Requirements

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.

If you use the ["GLPI Agent" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/glpi_agent.yml), this is automatically done for you.


## Tags

| Tag                    | What it does                              |
| ---                    | ------------                              |
| `glpi_agent`           | Installs and configure GLPI Agent.        |
| `glpi_agent:configure` | Deploys the configuration file.           |
| `glpi_agent:state`     | Manages the state of the systemd service. |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `glpi_agent__conf_server` | String. Specifies the server to use both as a controller for the agent, and as a recipient for task execution output. |

Example:
```yaml
# mandatory
glpi_agent__conf_server: 'https://glpi.example.com'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `glpi_agent__conf_local` | String. Write the results of the tasks execution locally. | `'/tmp'` |
| `glpi_agent__conf_no_ssl_check` | Bool. Ignore self-signed certificates of the server. | `false` |
| `glpi_agent__conf_ssl_fingerprint` | Specifies the fingerprint of the ssl server certificate to trust. The fingerprint to use can be retrieved in agent log by temporarily enabling `glpi_agent__conf_no_ssl_check` option. | unset |
| `glpi_agent__service_enabled` | Bool. Enables or disables the service, analogous to `systemctl enable/disable --now`.  | `true` |
| `glpi_agent__version` | String. The version of blocky to install. Possible options: `'latest'`, or any from https://github.com/glpi-project/glpi-agent/releases. | `'latest'` |

Example:
```yaml
# optional
glpi_agent__conf_local: '/tmp'
glpi_agent__conf_no_ssl_check: false
glpi_agent__conf_ssl_fingerprint: 'sha256$...'
glpi_agent__service_enabled: true
glpi_agent__version: 'latest'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
