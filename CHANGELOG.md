# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Breaking Changes

Role: acme_sh

* Added `name` subkey to `acme_sh__certificates`
* Moved `acme_sh__reload_cmd` to a subkey of `acme_sh__certificates`

Role: collabora_code

* Renamed rolename and vars from `collabora_code` to `collabora`

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

Role: mariadb_server
* Renamed `mariadb_server__admin_login` to `mariadb_server__admin_user`
* Moved `mariadb_server__admin_host` to `mariadb_server__admin_user["host"]`
* Renamed `mariadb_server__dump_login` to `mariadb_server__dump_user`
* Moved `mariadb_server__dump_user_*` to subkeys in `mariadb_server__dump_user`

Role php:
* Made more variables injectable, therefore the variables have a new name.

Playbook: basic_setup
* Renamed to setup_basic to be consitent with the other setup playbooks
* Removed `audit` and `crypto_policy` roles for now

All roles:
* Renamed all injectable variables:
    * `rolename__combined_varname` to `rolename__varname__combined_var`
    * `rolename__dependent_varname` to `rolename__varname__dependent_var`
    * `rolename__group_varname` to `rolename__varname__group_var`
    * `rolename__host_varname` to `rolename__varname__host_var`
    * `rolename__role_varname` to `rolename__varname__role_var`

Role: chrony
* Fixed wrong variable prefix: Adjusted `chrony_server__` to `chrony__`.

Role: duplicity
* Renamed `duplicity__public_master_long_keyid` variable to `duplicity__gpg_encrypt_master_key`.
* Renamed `duplicity__public_master_key` variable to `duplicity__gpg_encrypt_master_key_block`.
* Changed the format of `duplicity__backup_sources__host_var`.

Role: kernel_settings
* Make `kernel_settings__` variables injection-capable via `kernel_settings__host_*`, `kernel_settings__group_*` and `kernel_settings__dependent_*`.

Role: libselinux_python:
* Renamed the role to policycoreutils.

Role: login
* Changed logic and renamed `login__users` to two combined variables `login__users__group_var` (define users in group vars) and `login__users__host_var` (define users in host vars).

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
* Role: mod_maxminddb
* Role: mongodb
* Role: motd
* Role: network
* Role: nextcloud
* Role: nfs_client
* Role: nfs_server
* Role: nodejs
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
* Role: rocketchat
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

* Role duplicity: Implemented massive-parallel backups.
* Role mariadb_server: Changed `mariadb_server__admin_host` to a list.

### Fixed

Bug fixes:

*  role:sshd: ModuleNotFoundError: No module named 'seobject' ([fix #53](https://github.com/Linuxfabrik/lfops/issues/53))


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


[Unreleased]: https://github.com/Linuxfabrik/lfops/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/Linuxfabrik/lfops/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/Linuxfabrik/lfops/releases/tag/v1.0.0
