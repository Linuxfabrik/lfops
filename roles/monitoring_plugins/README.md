# Ansible Role linuxfabrik.lfops.monitoring_plugins

This role deploys the [Linuxfabik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins) `/usr/lib64/nagios/plugins/`, allowing them to be easily executed by a monitoring system.

There are three possible installation methods:

1. Linux only: Using the package manager (`monitoring_plugins__linux_variant == 'package'`):
* This is the preferred variant for Linux, as the packages provide the plugins compiled, with batteries (libraries) included.
* This means that Python does not have to be installed on the host.
* Requires the repository to be set up on the server (see [Mandatory Requirements](#mandatory-requirements) below).
* The role always installs the latest available package from the repository.
* And (by default) enables a version lock / version pin for the installed package. This prevents automatic updates from causing inconsistencies between the installed plugins and the configuration of the monitoring system (e.g. outdated Icinga Director configuration). Updating the plugins should be done manually along with updating the monitoring system configuration. Set `monitoring_plugins__skip_package_versionlock: true` to disable this behaviour.

2. Windows only: Deployment of the Nuitka-compiled plugins (`monitoring_plugins__windows_variant == 'nuitka'`):
* This is the preferred variant for Windows, as the packages provide the plugins compiled, with batteries (libraries) included.
* This means that Python does not have to be installed on the host.

3. By deploying the python source code from GitHub (`monitoring_plugins__linux_variant == 'python'` / `monitoring_plugins__windows_variant == 'python'`):
* This method should only be used if there is no package available, or for development / troubleshooting purposes.
* Deploys the version given in `monitoring_plugins__repo_version`.
* Also deploys the [Linuxfabrik Plugin Library](https://github.com/Linuxfabrik/monitoring-plugins) as python source code.

Additionally, this role allows you to deploy custom plugins which are placed under `{{ inventory_dir }}/host_files/{{ inventory_hostname }}/usr/lib64/nagios/plugins` on the Ansible control node.

Windows only: Since you cannot change files that are currently used by a process in Windows, when running against a Windows host, this role first stops the Icinga2 service, deploys the plugins and starts the service again. Optionally, it sets a downtime for each host. Have a look at the optional role variables below for this.

Runs on

* Debian 9
* Debian 10
* Fedora
* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Suse
* Ubuntu 16
* Windows


## Mandatory Requirements

Either:
* Deploy the [Repository for the Monitoring Plugins](https://repo.linuxfabrik.ch/monitoring-plugins/). This can be done using the [linuxfabrik.lfops.repo_monitoring_plugins](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_monitoring_plugins) role.

or:
* Install Python 3 and any further requirements from [INSTALL](https://github.com/Linuxfabrik/monitoring-plugins/blob/main/INSTALL.rst#python-run-from-source-code).


## Optional Requirements

* Round about 20 check plugins require the 3rd party [psutil](https://psutil.readthedocs.io/en/latest/) library. On RHEL-compatible systems, enable the EPEL repository (for example by using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role), then install `python3-psutil`.
* Look at the individual requirements of each check in its README file on [GitHub](https://github.com/Linuxfabrik/monitoring-plugins) or on [docs.linuxfabrik.ch](https://docs.linuxfabrik.ch/monitoring-plugins/000-check-plugins.html) to identify any dependencies on additional third-party libraries.


## Tags

| Tag                                 | What it does                                                                                |
| ---                                 | ------------                                                                                |
| `monitoring_plugins`                | Deploys the monitoring plugins, including the Linuxfabrik Plugin Library and custom plugins |
| `monitoring_plugins:custom`         | Only deploys the custom plugins                                                             |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `monitoring_plugins__icinga2_api_password` | The password of the `monitoring_plugins__icinga2_api_user`. This is required to schedule a downtime for Windows hosts. | unset |
| `monitoring_plugins__icinga2_api_url` | The address of the Icinga2 master API. This is required to schedule a downtime for Windows hosts. | unset |
| `monitoring_plugins__icinga2_api_user` | The Icinga2 API user. This is required to schedule a downtime for Windows hosts. Therefore, it needs to have the following permissions: `permissions = [ "actions/schedule-downtime", "actions/remove-downtime" ]` | unset |
| `monitoring_plugins__linux_variant` | String. Linux only. Which variant of the monitoring plugins should be deployed? Possible options:<ul><li>`package`: Deploy the packages with the checks compiled by pyinstaller. This does not require Python on the system.</li><li>`python`: Deploy the plugins as source code. This requires Python to be installed.</li></ul> | `'package'` |
| `monitoring_plugins__plugin_list` | Overwrite the automatically generated list of monitoring plugins that should be deployed. Note: This does not work for the compiled Nuitka plugins, (as they are all packaged in a single zip-file), nor with the RPM / DEB packages. | unset |
| `monitoring_plugins__repo_version` | String. Linux only: Which version of the monitoring plugins should be deployed? Possible options: <ul><li>`latest`: The **latest stable** release. See the [Releases](https://github.com/Linuxfabrik/monitoring-plugins/releases).</li><li>`main`: The development version. Use with care.</li><li>A specific release, for example `2022030201`. See the [Releases](https://github.com/Linuxfabrik/monitoring-plugins/releases).</li></ul> | `'{{ lfops__monitoring_plugins_version \| default("latest") }}'` |
| `monitoring_plugins__skip_notification_plugins__host_var` / `monitoring_plugins__skip_notification_plugins__group_var` | Skips the deployment of the notification-plugins (in addition to the check-plugins). For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `true` |
| `monitoring_plugins__skip_package_versionlock` | By default, the version of the `linuxfabrik-monitoring-plugins` (and `linuxfabrik-notification-plugins`) is locked after installation. Setting this to true skips this step. | `false` |
| `monitoring_plugins__windows_variant` | Windows only. Which variant of the monitoring plugins should be deployed? Possible options:<br> * `nuitka`: Deploy the nuitka-compiled checks (EXE files). This does not require Python on the system.<br> * `python`: Deploy the plain Python plugins. This requires Python to be installed on Windows. | `'nuitka'` |

Example:
```yaml
# optional
monitoring_plugins__icinga2_api_password: 'linuxfabrik'
monitoring_plugins__icinga2_api_url: 'https://192.0.2.3:5665/v1'
monitoring_plugins__icinga2_api_user: 'downtime-api-user'
monitoring_plugins__linux_variant: 'python'
monitoring_plugins__plugin_list:
  - 'about-me'
  - 'cpu-usage'
monitoring_plugins__repo_version: 'latest'
monitoring_plugins__skip_notification_plugins__host_var: true
monitoring_plugins__windows_variant: 'nuitka'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
