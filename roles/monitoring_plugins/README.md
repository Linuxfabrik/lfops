# Ansible Role linuxfabrik.lfops.monitoring_plugins

This role deploys the [Linuxfabik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins), allowing them to be easily executed by a monitoring system.

Notes:

* Best practice is to put the affected hosts into downtime or disable them in Icinga before applying this role. This role can do that for you.
* This role allows you to deploy custom plugins which are placed under `{{ inventory_dir }}/host_files/{{ inventory_hostname }}/usr/lib64/nagios/plugins` on the Ansible control node.


## Installation Methods

 Taken from the Linuxfabrik Monitoring Plugins [INSTALL](https://github.com/Linuxfabrik/monitoring-plugins/blob/main/INSTALL.rst) document:

| Platform | Install | Implemented by | Mandatory Requirements |
|----------|---------|----------------|--------------|
| Linux    | Binaries from rpm/deb package (**default**) | `monitoring_plugins__install_method: 'package'` | Deploy the [Repository for the Monitoring Plugins](https://repo.linuxfabrik.ch/monitoring-plugins/). This can be done using the [linuxfabrik.lfops.repo_monitoring_plugins](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_monitoring_plugins) role. If you use the [monitoring_plugins Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/monitoring_plugins.yml), this is automatically done for you.<br/><br/>By default, this role installs the latest available package from the repository. It enables version lock / version pinning for the installed package. This prevents automatic updates from causing inconsistencies between the installed plugins and the configuration of the monitoring system (e.g. outdated Icinga Director configuration). Updating plugins should be done in a controlled manner along with updating the monitoring server configuration. See `monitoring_plugins__skip_package_versionlock` for details. |
| Linux    | Binaries from zip | Currently not supported by this role | |
| Linux    | Source Code | `monitoring_plugins__install_method: 'source'` | Ensure that Python 3.9+ including associated pip is installed and activated by default. On Debian 12, a virtual environment is mandatory. |
| Windows  | Binaries from msi (**default**) | `monitoring_plugins__install_method: 'package'` | Icinga2 Agent is required. |
| Windows  | Binaries from zip | `monitoring_plugins__install_method: 'archive'` | Since you cannot change files that are currently used by a process in Windows, when running against a Windows host, this role first stops the Icinga2 service, deploys the plugins and starts the service again. Optionally, it sets a downtime for each host. Have a look at the optional role variables below for this. |
| Windows  | Source Code | Currently not supported by this role | |


## Mandatory Requirements

* See table above (depends on the use case).


## Tags

| Tag                                 | What it does                                                                                |
| ---                                 | ------------                                                                                |
| `monitoring_plugins`                | Deploys the monitoring plugins, including the Linuxfabrik Plugin Library and custom plugins |
| `monitoring_plugins:custom`         | Only deploys the custom plugins                                                             |
| `monitoring_plugins:remove`         | Removes the Linuxfabrik Monitoring Plugins                                                  |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `monitoring_plugins__version` | String. Which version of the monitoring plugins should be deployed? Possible options: <ul><li>A specific release, for example `1.2.0.11`. See the [Releases](https://github.com/Linuxfabrik/monitoring-plugins/releases).</li><li>`dev`: The development version (main branch). Use with care. Only works with `monitoring_plugins__install_method: 'source'`.</li></ul> Defaults to `lfops__monitoring_plugins_version` for convenience. |

Example:
```yaml
# mandatory
monitoring_plugins__version: '1.2.0.11'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `monitoring_plugins__icinga2_api_password` | String. The password of the `monitoring_plugins__icinga2_api_user`. This is required to schedule a downtime for Windows hosts. | unset |
| `monitoring_plugins__icinga2_api_url` | String. The address of the Icinga2 master API. This is required to schedule a downtime for Windows hosts. | unset |
| `monitoring_plugins__icinga2_api_user` | String. The Icinga2 API user. This is required to schedule a downtime for Windows hosts. Therefore, it needs to have the following permissions: `permissions = [ "actions/schedule-downtime", "actions/remove-downtime" ]` | unset |
| `monitoring_plugins__icinga2_cn` | String. The common name / host name. Will be used to schedule a downtime for Windows hosts. | `'{{ ansible_facts["nodename"] }}'` |
| `monitoring_plugins__icinga_user` | String. The user running the Monitoring Plugins. The role installs the pip packages from the requirements.yml for this user. Only relevant if `monitoring_plugins__install_method: 'source'`.  | `'icinga'` on RHEL, `'nagios'` on Debian |
| `monitoring_plugins__install_method` | String. Which variant of the monitoring plugins should be deployed? Possible options:<ul><li>`package`: Deploy the install package with the compiled checks. This does not require Python on the system.</li><li>`source`: Deploy the plugins as source code. This requires Python to be installed. Currently for Linux only.</li><li>`archive`: Deploy the compiled binaries from a zip file downloaded from [download.linuxfabrik.ch](https://download.linuxfabrik.ch). Currently for Windows only.</li></ul> | `'package'` |
| `monitoring_plugins__skip_package_versionlock` | By default, the version of the `linuxfabrik-monitoring-plugins` are locked after installation. Setting this to `true` skips this step (and never unlocks the version pinning again). | `false` |

Example:
```yaml
# optional
monitoring_plugins__icinga2_api_password: 'linuxfabrik'
monitoring_plugins__icinga2_api_url: 'https://192.0.2.3:5665/v1'
monitoring_plugins__icinga2_api_user: 'downtime-api-user'
monitoring_plugins__icinga2_cn: 'windows1.example.com'
monitoring_plugins__icinga_user: 'icinga'
monitoring_plugins__install_method: 'source'
monitoring_plugins__skip_package_versionlock: false
```


## Troubleshooting

If you get `No package linuxfabrik-monitoring-plugins-main available. msg: Failed to install some of the specified packages` while setting `monitoring_plugins__version: 'dev'`, you simply forgot to also set `monitoring_plugins__install_method: 'source'`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
