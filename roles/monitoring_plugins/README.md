# Ansible Role linuxfabrik.lfops.monitoring_plugins

This role deploys the [Linuxfabik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins), allowing them to be easily executed by a monitoring system.

Notes:

* Best practice is to put the affected hosts into downtime or disable them in Icinga before applying this role. This role can do that for you.
* This role allows you to deploy custom plugins which are placed under `{{ inventory_dir }}/host_files/{{ inventory_hostname }}/usr/lib64/nagios/plugins` on the Ansible control node.


*Available since LFOps `1.0.0`.*


## How the Role Behaves

* **Source install builds a virtual environment.** With `monitoring_plugins__install_method: 'source'`, the role deploys the plugins into a self-contained Python virtual environment under `/usr/lib64/linuxfabrik-monitoring-plugins/venv` and rewrites the plugin shebangs to that interpreter, mirroring the layout of the rpm/deb package. Check, event and notification plugins all land flat in `/usr/lib64/nagios/plugins`, and their assets in `/usr/lib64/nagios/plugins/assets`, which is where the Icinga command definitions expect them. The OID lists and MIBs of the `snmp` plugin go into `device-oids/` and `device-mibs/` next to it. Device definitions of your own in these directories are left alone, by updates and by `monitoring_plugins:remove`.
* **The role provisions a suitable Python itself.** On RHEL 8 the system Python is 3.6, which is too old. The role installs Python 3.9 (package `python39`) and builds the virtual environment with it, so a source install works on RHEL 8 without any manual Python setup. Every other supported platform already ships Python 3.9 or newer and is used as-is. A virtual environment left behind by an earlier run with a different Python is rebuilt.
* **The source install needs no Internet access on the target.** The Ansible controller clones the monitoring-plugins and Linuxfabrik library repositories, downloads every Python dependency as a wheel for the interpreter, architecture and glibc of each target, and copies everything over. pip on the target installs from those files only, so air-gapped hosts are provisioned like any other.
* **Dependencies are pinned and verified.** The source install uses the lockfiles of the monitoring-plugins checkout, which pin every package to an exact version and to the checksums of its files, the same set CI tests the plugins against and the rpm/deb packages ship. pip refuses any file whose checksum does not match. A later run moves an existing venv to the versions of the current lockfile.
* **On Linux, the Icinga2 agent keeps running during a deployment.** Plugins and library files are replaced by renaming, so a check never runs a half-written plugin. The virtual environment of the source install is changed in place, though: while the role moves it to new dependency versions, or rebuilds it for another Python, a check that runs at that moment can fail. The next check passes again.
* **Which code is deployed follows `monitoring_plugins__version`.** A release deploys that tag of the plugins and the Linuxfabrik library release its lockfiles pin. `dev` deploys the `main` branch of both repositories, and the dependencies of the library's `main` branch take precedence over the ones the plugin lockfile resolved.
* **SELinux.** On RHEL with SELinux enabled, the source install loads the same policy module as the `linuxfabrik-monitoring-plugins-selinux` package and switches on `nagios_run_sudo`, which the plugins need to run through sudo. RHEL 10 carries no nagios policy and has no such boolean, so there only the module is loaded.
* **The sudoers drop-ins are validated.** They are only put in place once `visudo` accepts them, since a broken file in `/etc/sudoers.d` locks every user out of sudo, not just the monitoring user.
* **The source install records what it placed.** It writes `/usr/lib64/linuxfabrik-monitoring-plugins/install-manifest.txt` in the same format as the one-line installer, so either tool can remove what the other installed. A plugin that an earlier run deployed and that the checkout no longer carries is removed.
* **Plugins are owned by root, readable by the monitoring user.** The whitelisted plugins run as root through sudo, so the plugins, the bundled library and the virtual environment are owned by root and are only readable and executable for the monitoring user. Ownership and modes are set explicitly on every run and do not depend on the umask of the Ansible controller, so a re-run also repairs a host that was left in a broken state.
* **The psi-* plugins need `psi=1` on the RHEL family.** Their kernels keep no pressure stall information unless booted with `psi=1`, so the plugins report "no PSI" there. This role does not touch the kernel command line itself, it hands the option to the [bootloader](https://github.com/Linuxfabrik/lfops/tree/main/roles/bootloader) role, which the `setup_basic` playbook runs. Debian, Fedora and Ubuntu track pressure by default.
* **Bash completion for the plugins.** Both install methods place `/etc/bash_completion.d/linuxfabrik-monitoring-plugins`, which completes the command line options of every plugin in the plugin directory. The package ships it, the source install copies it from the checkout. It is only read on a host that has the `bash-completion` package, which this role does not install on your behalf.
* **Legacy cleanup.** An earlier version of this role installed the source dependencies into the home directories of root and the icinga user via `pip --user`. On the next run the role removes those leftovers (only packages under the respective `~/.local`, never system packages), since the virtual environment supersedes them.


## Installation Methods

 Taken from the Linuxfabrik Monitoring Plugins [INSTALL](https://github.com/Linuxfabrik/monitoring-plugins/blob/main/INSTALL.md) document:

| Platform | Install | Implemented by | Mandatory Requirements |
|----------|---------|----------------|--------------|
| Linux    | Binaries from rpm/deb package (**default**) | `monitoring_plugins__install_method: 'package'` | Deploy the [Repository for the Monitoring Plugins](https://repo.linuxfabrik.ch/monitoring-plugins/). This can be done using the [linuxfabrik.lfops.repo_monitoring_plugins](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_monitoring_plugins) role. If you use the [monitoring_plugins Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/monitoring_plugins.yml), this is automatically done for you.<br/><br/>By default, this role installs the latest available package from the repository. It enables version lock / version pinning for the installed package. This prevents automatic updates from causing inconsistencies between the installed plugins and the configuration of the monitoring system (e.g. outdated Icinga Director configuration). Updating plugins should be done in a controlled manner along with updating the monitoring server configuration. See `monitoring_plugins__skip_package_versionlock` for details. |
| Linux    | Binaries from zip | Currently not supported by this role | |
| Linux    | Source Code | `monitoring_plugins__install_method: 'source'` | See "Requirements" below. The role provisions a suitable Python on the target itself (it installs Python 3.9 on RHEL 8, where the system Python is 3.6) and deploys the plugins into a self-contained virtual environment. See "How the Role Behaves" above. |
| Windows  | Binaries from msi (**default**) | `monitoring_plugins__install_method: 'package'` | Icinga2 Agent is required. |
| Windows  | Binaries from zip | `monitoring_plugins__install_method: 'archive'` | Since you cannot change files that are currently used by a process in Windows, when running against a Windows host, this role first stops the Icinga2 service, deploys the plugins and starts the service again. Optionally, it sets a downtime for each host. Have a look at the optional role variables below for this. |
| Windows  | Source Code | Currently not supported by this role | |


## Requirements

* See table above (depends on the use case).
* Source install: outbound access from the controller to GitHub and PyPI. The targets need neither.
* Source install: glibc 2.17 or newer on the target, since the dependencies are installed from manylinux wheels.

Manual steps:

* Source install: install pip for the Python that runs Ansible on the controller. To download through a proxy or from a PyPI mirror, set the usual pip environment variables (`HTTPS_PROXY`, `PIP_INDEX_URL`) for `ansible-playbook`.


## Switching from the Package to the Source Install

1. Set `monitoring_plugins__install_method: 'source'` for the host.
2. Remove the package, its version lock, the package repository and its signing key:

    ```bash
    ansible-playbook --inventory=inventory linuxfabrik.lfops.monitoring_plugins \
        --tags=monitoring_plugins:remove,repo_monitoring_plugins:remove --limit=myhost
    ```

3. Deploy the source install:

    ```bash
    ansible-playbook --inventory=inventory linuxfabrik.lfops.monitoring_plugins --limit=myhost
    ```

The playbooks only register the package repository for `monitoring_plugins__install_method: 'package'`, so a later run of `setup_basic` or `icinga2_agent` does not bring it back.


## Tags

`monitoring_plugins`

* Deploys the monitoring plugins, including the Linuxfabrik Plugin Library and custom plugins.
* Triggers: none.

`monitoring_plugins:custom`

* Only deploys the custom plugins.
* Triggers: none.

`monitoring_plugins:remove`

* Removes the Linuxfabrik Monitoring Plugins, whether installed as a package, by this role from source, by the one-line installer or by hand: the packages including their version locks (purged on Debian and Ubuntu), everything listed in the install manifest, every file any release ever placed into `/usr/lib64/nagios/plugins` unless another package owns it, the virtual environment, the sudoers drop-ins, the bash completion and the SELinux policy module. `nagios_run_sudo` is left as it is. Custom plugins are kept unless they carry the name of a Linuxfabrik plugin.
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

* By default, the version of the `linuxfabrik-monitoring-plugins` are locked after installation. Setting this to `true` skips this step (and never unlocks the version pinning again). The role lifts the lock for the install and sets it again afterwards; if the install fails, a lock that existed before the run is set again, so the host does not stay unlocked.
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
