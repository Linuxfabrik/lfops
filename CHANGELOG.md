# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Breaking Changes

Role: apache_httpd
* Changed `conf_server_alias` from a string to a list

Role: graylog_server
* Remove support for Graylog < 5.0

Playbook: Setup Icinga2 Master
* Changed default of `setup_icinga2_master__skip_icingaweb2_module_monitoring` from `false` to `true`

Role: monitoring_plugins
* Remove the tasks for Nuitka compilation, as the compilation is done by the [Monitoring Plugins GitHub Action](https://github.com/Linuxfabrik/monitoring-plugins/actions/workflows/nuitka-compile.yml) now.
* Locks the version of the `monitoring-plugins` package after installing it. Updating the plugins should be done manually along with updating the monitoring system configuration.

Role: monitoring_plugins_grafana_dashboards
* Change from provisioning to grizzly for the deployment of the dashboards

Role: grafana
* Changed default value for `grafana__serve_from_sub_path` from `true` to `false`

Role: system_update
* Remove `system_update__icinga2_master` variable. Use `system_update__icinga2_api_url` instead


### Added

* Role: clamav
* Role: dnf_versionlock
* Role: fangfrisch
* Role: grafana_grizzly
* Role: icingadb
* Role: icingaweb2_module_businessprocess
* Role: repo_gitlab_runner
* Role: repo_rpmfusion

Role:python_venv
* allow specifying different certificate store
* allow specifying the python executable to be used in the venv

Role:kvm_vm
* add the option to boot the VM with UEFI

Role:selinux
* add support for SELinux ports

Role:systemd_unit
* add support for mount units

Role:bind
* add `bind__named_conf_raw` variable

Role: grafana
* creation of service accounts and their tokens

Playbook: setup_basic
* Add support for AlmaLinux 8

Role: duplicity:
* Add `duplicity__backup_full_if_older_than` variable

Role: cloud_init
* Add task to remove `/etc/cloud/cloud.cfg.rpmsave`

Role: graylog_server
* Add variables and documentation for multi-node setup
* Add Debian support

Role: logrotate
* Add compression

Role: mongodb
* Add Debian support
* Add keyfile handling
* Adjust for replica set across members
* Implement user management (fix #89)

Role: opensearch
* Add Debian support
* Add variables for cluster configuration

Role: php
* Add tag `php:fpm`

Role: python_venv
* Add Debian support

Role: repo_baseos
* Add AlmaLinux 8 support

Role: repo_graylog
* Add Debian support

Role: repo_mongodb
* Add Debian support

Role: repo_opensearch
* Add Debian support

Role: systemd_journald
* Make SystemMaxUse configurable

Role: systemd_update
* Add option `-y` to `yum check-update`


### Fixed

Role: influxdb
* Fix wrong systemd service name, which was preventing influxdb dumps from being scheduled


### Changed

Role: opensearch
* Make `opensearch__version*` optional

Role: graylog_server
* Remove version defaults from the role


## [2.0.1] - 2023-02-28

### Changed

* Adjustments for the [Ansible Galaxy Release](https://galaxy.ansible.com/linuxfabrik/lfops).


## [2.0.0] - 2023-02-28

All roles:
* Renamed all injectable variables:
    * `rolename__combined_varname` to `rolename__varname__combined_var`
    * `rolename__dependent_varname` to `rolename__varname__dependent_var`
    * `rolename__group_varname` to `rolename__varname__group_var`
    * `rolename__host_varname` to `rolename__varname__host_var`
    * `rolename__role_varname` to `rolename__varname__role_var`

Playbook: basic_setup
* Renamed to setup_basic to be consitent with the other setup playbooks
* Removed `audit` and `crypto_policy` roles for now

Role: acme_sh
* Added `name` subkey to `acme_sh__certificates`
* Moved `acme_sh__reload_cmd` to a subkey of `acme_sh__certificates`

Role: chrony
* Fixed wrong variable prefix: Adjusted `chrony_server__` to `chrony__`.

Role: collabora_code
* Renamed rolename and vars from `collabora_code` to `collabora`

Role: duplicity
* Renamed `duplicity__public_master_long_keyid` variable to `duplicity__gpg_encrypt_master_key`.
* Renamed `duplicity__public_master_key` variable to `duplicity__gpg_encrypt_master_key_block`.
* Changed the format of `duplicity__backup_sources__host_var`.

Role: fail2ban
* Adjusted subkeys of `fail2ban__jails__group_var` / `fail2ban__jails__host_var`

Role: git
* Added ...
* ... and later removed in favor of a more general `app` role

Role: hostname
* Renamed `hostname__domain_name` to `hostname__domain_part`
* Renamed `hostname__hostname` to `hostname__full_hostname`

Role: icinga2_agent
* Added new mandatory variable `icinga2_agent__icinga2_master_cn`
* Made `icinga2_agent__icinga2_master_host` optional
* Most users can replace all instances of `icinga2_agent__icinga2_master_host` to `icinga2_agent__icinga2_master_cn`

Role: infomaniak_vm
* Renamed `infomaniak_vm__password` to `infomaniak_vm__api_password`
* Renamed `infomaniak_vm__project_id` to `infomaniak_vm__api_project_id`
* Renamed `infomaniak_vm__username` to `infomaniak_vm__api_username`
* Renamed `infomaniak_vm__volume_size` to `infomaniak_vm__separate_boot_volume_size`

Role: java
* Removed, better substituted by `apps` role.

Role: kernel_settings
* Make `kernel_settings__` variables injection-capable via `kernel_settings__host_*`, `kernel_settings__group_*` and `kernel_settings__dependent_*`.

Role: libselinux_python:
* Renamed the role to policycoreutils.

Role: login
* Changed logic and renamed `login__users` to two combined variables `login__users__group_var` (define users in group vars) and `login__users__host_var` (define users in host vars).

Role: mariadb_server
* Renamed `mariadb_server__admin_login` to `mariadb_server__admin_user`
* Moved `mariadb_server__admin_host` to `mariadb_server__admin_user["host"]`
* Renamed `mariadb_server__dump_login` to `mariadb_server__dump_user`
* Moved `mariadb_server__dump_user_*` to subkeys in `mariadb_server__dump_user`

Role: monitoring_plugins
* Renamed `monitoring_plugins__deploy_notification_plugins` to `monitoring_plugins__skip_notification_plugins` and flipped the logic.

Role php:
* Made more variables injectable, therefore the variables have a new name.

Role: stig
* Moved to a new GitHub repo (temporarily)

Role: system_update
* Renamed variables:
    * system_update__mail_recipients_new_configfiles => system_update__mail_recipients_new_configfiles
    * system_update__mail_recipients_updates => system_update__mail_recipients_updates
    * system_update__mail_from => system_update__mail_from
    * system_update__mail_subject_prefix => system_update__mail_subject_prefix
    * system_update__notify_and_schedule_on_calendar => system_update__notify_and_schedule_on_calendar


### Added

New features:

* This CHANGELOG.

* Role network: Added functionality to configure network connections.

* Role: acme_sh
* Role: ansible_init
* Role: apache_httpd
* Role: apache_tomcat
* Role: apps
* Role: at
* Role: audit
* Role: bind
* Role: chrony
* Role: cloud_init
* Role: cockpit
* Role: collabora
* Role: coturn
* Role: crypto_policy
* Role: dnf_makecache
* Role: docker
* Role: elasticsearch_oss
* Role: exoscale_vm
* Role: fail2ban
* Role: firewall
* Role: freeipa_client
* Role: freeipa_server
* Role: glances
* Role: grafana
* Role: grav
* Role: graylog_server
* Role: haveged
* Role: hetzner_vm
* Role: hostname
* Role: icinga2_agent
* Role: icinga2_master
* Role: icingaweb2
* Role: icingaweb2_module_company
* Role: icingaweb2_module_director
* Role: icingaweb2_module_doc
* Role: icingaweb2_module_grafana
* Role: icingaweb2_module_incubator
* Role: icingaweb2_module_monitoring
* Role: icingaweb2_module_vspheredb
* Role: influxdb
* Role: infomaniak_vm
* Role: kdump
* Role: keepalived
* Role: kernel_settings
* Role: keycloak
* Role: kvm_host
* Role: kvm_vm
* Role: libmaxminddb
* Role: librenms
* Role: libreoffice
* Role: login
* Role: mailto_root
* Role: mariadb_client
* Role: mariadb_server
* Role: maxmind_geoip
* Role: minio_client
* Role: mod_maxminddb
* Role: mongodb
* Role: motd
* Role: network
* Role: nextcloud
* Role: nfs_client
* Role: nfs_server
* Role: nodejs
* Role: objectstore_backup
* Role: open_vm_tools
* Role: openssl
* Role: openvpn_server
* Role: perl
* Role: php
* Role: policycoreutils
* Role: postgresql_server
* Role: qemu_guest_agent
* Role: redis
* Role: repo_baseos
* Role: repo_collabora
* Role: repo_collabora_code
* Role: repo_debian_base
* Role: repo_docker
* Role: repo_elasticsearch_oss
* Role: repo_gitlab_ce
* Role: repo_grafana
* Role: repo_icinga
* Role: repo_influxdb
* Role: repo_mariadb
* Role: repo_mongodb
* Role: repo_monitoring_plugins
* Role: repo_mydumper
* Role: repo_postgresql
* Role: repo_remi
* Role: repo_sury
* Role: rocketchat
* Role: rsyslog
* Role: snmp
* Role: sshd
* Role: stig
* Role: system_update
* Role: systemd_journald
* Role: systemd_unit
* Role: tar
* Role: telegraf
* Role: timezone
* Role: unattended_upgrades
* Role: wordpress
* Role: yum_utils


### Changed

Changes in existing functionality:

* Module Util bitwarden: Switched to the bitwarden client API, as it is more reliable than using the command line tool directly

* Role duplicity: Implemented massive-parallel backups.
* role:acme_sh: is acme.sh automatically updated? ([fix #74](https://github.com/Linuxfabrik/lfops/issues/74))
* role:apache_tomcat: Use the correct Java version depending on Tomcat version ([fix #82](https://github.com/Linuxfabrik/lfops/issues/82))
* role:hetzner_vm: improve handling of ip addresses (new hetzner features) ([fix #72](https://github.com/Linuxfabrik/lfops/issues/72))
* role:hetzner_vm: should be able to manage the provider firewall ([fix #71](https://github.com/Linuxfabrik/lfops/issues/71))
* role:login: Needs a switch to be aggressive or not ([fix #65](https://github.com/Linuxfabrik/lfops/issues/65))
* role:mariadb_server: mydumper has to be implemented / adapted to the LFOps standards ([fix #56](https://github.com/Linuxfabrik/lfops/issues/56))
* role:mongodb: implement dumping / user management? ([fix #78](https://github.com/Linuxfabrik/lfops/issues/78))
* role:python: On RHEL 8+, don't install `python3`. Instead install `python38` or `python39` explicitly ([fix #62](https://github.com/Linuxfabrik/lfops/issues/62))
* role:tools: prompt.sh - We should see the Distro ([fix #47](https://github.com/Linuxfabrik/lfops/issues/47))


### Fixed

Bug fixes:

* Role icinga2_master: Missing option name in icinga2_master/tasks/main.yml ([fix #105](https://github.com/Linuxfabrik/lfops/issues/105))
* Role sshd: ModuleNotFoundError: No module named 'seobject' ([fix #53](https://github.com/Linuxfabrik/lfops/issues/53))
* basic_setup: Failed to set locale, defaulting to C.UTF-8 ([fix #55](https://github.com/Linuxfabrik/lfops/issues/55))
* do not use become: true in all playbooks ([fix #66](https://github.com/Linuxfabrik/lfops/issues/66))
* nft has to be deployed in basic-setup or the fwbuilder role ([fix #61](https://github.com/Linuxfabrik/lfops/issues/61))
* role: freeipa_server: msg: In unattended mode you need to provide at least -r, -p and -a options ([fix #83](https://github.com/Linuxfabrik/lfops/issues/83))
* role:audit wrong README ([fix #51](https://github.com/Linuxfabrik/lfops/issues/51))
* role:audit: wrong readme ([fix #58](https://github.com/Linuxfabrik/lfops/issues/58))
* role:crypto_policy wrong README ([fix #52](https://github.com/Linuxfabrik/lfops/issues/52))
* role:crypto_policy: Wrong README ([fix #76](https://github.com/Linuxfabrik/lfops/issues/76))
* role:icinga2_agent: On Debian User nagios does not exist when certs folder is created ([fix #77](https://github.com/Linuxfabrik/lfops/issues/77))
* role:monitoring_plugins: "deploy" vs "skip" ([fix #103](https://github.com/Linuxfabrik/lfops/issues/103))
* role:repo_graylog: `repo_graylog__mirror_url` is never actually used ([fix #94](https://github.com/Linuxfabrik/lfops/issues/94))
* role:sshd: ModuleNotFoundError: No module named 'seobject' ([fix #53](https://github.com/Linuxfabrik/lfops/issues/53))


## [1.0.1] - 2022-03-17

### Changed

* Adjust tags for Ansible Galaxy.


## [1.0.0] - 2022-03-17

### Added

* Role: duplicity
* Role: monitoring_plugins
* Role: python_venv
* Role: repo_epel

* Module: bitwarden_item
* Module: gpg_key

* Lookup Plugin: bitwarden

* Module Util: bitwarden
* Module Util: gnupg


[Unreleased]: https://github.com/Linuxfabrik/lfops/compare/v2.0.1...HEAD
[2.0.1]: https://github.com/Linuxfabrik/lfops/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/Linuxfabrik/lfops/compare/v1.0.1...v2.0.0
[1.0.1]: https://github.com/Linuxfabrik/lfops/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/Linuxfabrik/lfops/releases/tag/v1.0.0
