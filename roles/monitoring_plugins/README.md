# Ansible Role linuxfabrik.lfops.monitoring_plugins

This role deploys the [Linuxfabik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins), allowing them to be easily executed by a monitoring system.

Notes:

* Best practice is to put the affected hosts into downtime or disable them in Icinga before applying this role. This role can do that for you.
* This role allows you to deploy custom plugins which are placed under `{{ inventory_dir }}/host_files/{{ inventory_hostname }}/usr/lib64/nagios/plugins` on the Ansible control node.


*Available since LFOps `1.0.0`.*


## How the Role Behaves

* **Source install builds a virtual environment.** With `monitoring_plugins__install_method: 'source'`, the role deploys the plugins into a self-contained Python virtual environment under `/usr/lib64/linuxfabrik-monitoring-plugins/venv` and rewrites the plugin shebangs to that interpreter, mirroring the layout of the rpm/deb package.
* **The role provisions a suitable Python itself.** On RHEL 8 the system Python is 3.6, which is too old. The role installs Python 3.9 (package `python39`) and builds the virtual environment with it, so a source install works on RHEL 8 without any manual Python setup. Every other supported platform already ships Python 3.9 or newer and is used as-is.
* **Source tracks the newest code, the package tracks releases.** Unlike the rpm/deb package, which is frozen at each release, the source install pulls the newest third-party dependencies (unpinned) and deploys the newest Linuxfabrik library straight from its GitHub repository. The Linuxfabrik library is an independent project with its own version numbers, so it is always deployed from its `main` branch regardless of `monitoring_plugins__version`. Which plugin code is deployed follows `monitoring_plugins__version` (`dev` deploys the `main` branch, a version deploys that tag).
* **Legacy cleanup.** An earlier version of this role installed the source dependencies into the home directories of root and the icinga user via `pip --user`. On the next run the role removes those leftovers (only packages under the respective `~/.local`, never system packages), since the virtual environment supersedes them.


## Installation Methods

 Taken from the Linuxfabrik Monitoring Plugins [INSTALL](https://github.com/Linuxfabrik/monitoring-plugins/blob/main/INSTALL.rst) document:

| Platform | Install | Implemented by | Mandatory Requirements |
|----------|---------|----------------|--------------|
| Linux    | Binaries from rpm/deb package (**default**) | `monitoring_plugins__install_method: 'package'` | Deploy the [Repository for the Monitoring Plugins](https://repo.linuxfabrik.ch/monitoring-plugins/). This can be done using the [linuxfabrik.lfops.repo_monitoring_plugins](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_monitoring_plugins) role. If you use the [monitoring_plugins Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/monitoring_plugins.yml), this is automatically done for you.<br/><br/>By default, this role installs the latest available package from the repository. It enables version lock / version pinning for the installed package. This prevents automatic updates from causing inconsistencies between the installed plugins and the configuration of the monitoring system (e.g. outdated Icinga Director configuration). Updating plugins should be done in a controlled manner along with updating the monitoring server configuration. See `monitoring_plugins__skip_package_versionlock` for details. |
| Linux    | Binaries from zip | Currently not supported by this role | |
| Linux    | Source Code | `monitoring_plugins__install_method: 'source'` | None. The role provisions a suitable Python itself (it installs Python 3.9 on RHEL 8, where the system Python is 3.6) and deploys the plugins into a self-contained virtual environment. See "How the Role Behaves" above. |
| Windows  | Binaries from msi (**default**) | `monitoring_plugins__install_method: 'package'` | Icinga2 Agent is required. |
| Windows  | Binaries from zip | `monitoring_plugins__install_method: 'archive'` | Since you cannot change files that are currently used by a process in Windows, when running against a Windows host, this role first stops the Icinga2 service, deploys the plugins and starts the service again. Optionally, it sets a downtime for each host. Have a look at the optional role variables below for this. |
| Windows  | Source Code | Currently not supported by this role | |


## Requirements

* See table above (depends on the use case).


## Tags

`monitoring_plugins`

* Deploys the monitoring plugins, including the Linuxfabrik Plugin Library and custom plugins.
* Triggers: none.

`monitoring_plugins:custom`

* Only deploys the custom plugins.
* Triggers: none.

`monitoring_plugins:remove`

* Removes the Linuxfabrik Monitoring Plugins.
* Triggers: none.


## Mandatory Role Variables

`monitoring_plugins__version`

* Which version of the monitoring plugins should be deployed? Possible options:

    * A specific release, for example `2.2.1`. See the [Releases](https://github.com/Linuxfabrik/monitoring-plugins/releases).
    * `dev`: The development version (main branch). Use with care. Only works with `monitoring_plugins__install_method: 'source'`.

* Defaults to `lfops__monitoring_plugins_version` for convenience.
* Type: String.

Example:
```yaml
# mandatory
monitoring_plugins__version: '2.2.1'
```


## Optional Role Variables

`monitoring_plugins__icinga2_api_password`

* The password of the `monitoring_plugins__icinga2_api_user`. This is required to schedule a downtime for Windows hosts.
* Type: String.
* Default: unset

`monitoring_plugins__icinga2_api_url`

* The address of the Icinga2 master API. This is required to schedule a downtime for Windows hosts.
* Type: String.
* Default: unset

`monitoring_plugins__icinga2_api_user`

* The Icinga2 API user. This is required to schedule a downtime for Windows hosts. Therefore, it needs to have the following permissions: `permissions = [ "actions/schedule-downtime", "actions/remove-downtime" ]`
* Type: String.
* Default: unset

`monitoring_plugins__icinga2_cn`

* The common name / host name. Will be used to schedule a downtime for Windows hosts.
* Type: String.
* Default: `'{{ ansible_facts["nodename"] }}'`

`monitoring_plugins__icinga_user`

* The user that owns the deployed plugins, the Linuxfabrik library and the source virtual environment. Only relevant if `monitoring_plugins__install_method: 'source'`.
* Type: String.
* Default: `'icinga'` on RHEL, `'nagios'` on Debian

`monitoring_plugins__install_method`

* Which variant of the monitoring plugins should be deployed? Possible options:

    * `package`: Deploy the install package with the compiled checks. This does not require Python on the system.
    * `source`: Deploy the plugins as source code. This requires Python to be installed. Currently for Linux only.
    * `archive`: Deploy the compiled binaries from a zip file downloaded from [download.linuxfabrik.ch](https://download.linuxfabrik.ch). Currently for Windows only.

* Type: String.
* Default: `'package'`

`monitoring_plugins__skip_package_versionlock`

* By default, the version of the `linuxfabrik-monitoring-plugins` are locked after installation. Setting this to `true` skips this step (and never unlocks the version pinning again).
* Type: Bool.
* Default: `false`

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

**`No package linuxfabrik-monitoring-plugins-main available. msg: Failed to install some of the specified packages`**

* Appears when setting `monitoring_plugins__version: 'dev'` without also setting `monitoring_plugins__install_method: 'source'`. Set the install method to `'source'`.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
