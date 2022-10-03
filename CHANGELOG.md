# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Breaking Changes

Role: hostname

* Renamed `hostname__domain_name` to `hostname__domain_part`
* Renamed `hostname__hostname` to `hostname__full_hostname`

Role: infomaniak_vm

* Renamed `infomaniak_vm__password` to `infomaniak_vm__api_password`
* Renamed `infomaniak_vm__project_id` to `infomaniak_vm__api_project_id`
* Renamed `infomaniak_vm__username` to `infomaniak_vm__api_username`
* Renamed `infomaniak_vm__volume_size` to `infomaniak_vm__separate_boot_volume_size`

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
* Role: at
* Role: audit
* Role: bind
* Role: chrony
* Role: cloud_init
* Role: cockpit
* Role: collabora_code
* Role: coturn
* Role: crypto_policy
* Role: dnf_makecache
* Role: docker
* Role: exoscale_vm
* Role: fail2ban
* Role: firewall
* Role: freeipa_client
* Role: freeipa_server
* Role: git
* Role: glances
* Role: grafana
* Role: grav
* Role: graylog_server
* Role: hetzner_vm
* Role: hostname
* Role: icinga2_agent
* Role: icinga2_master
* Role: icingaweb2
* Role: icingaweb2_module_company
* Role: icingaweb2_module_director
* Role: icingaweb2_module_doc
* Role: icingaweb2_module_incubator
* Role: icingaweb2_module_monitoring
* Role: icingaweb2_module_vspheredb
* Role: influxdb
* Role: infomaniak_vm
* Role: java
* Role: kdump
* Role: kernel_settings
* Role: keycloak
* Role: kvm_host
* Role: kvm_vm
* Role: librenms
* Role: login
* Role: mailto_root
* Role: mariadb_client
* Role: mariadb_server
* Role: mongodb
* Role: motd
* Role: network
* Role: nextcloud
* Role: nfs_server
* Role: nodejs
* Role: open_vm_tools
* Role: openssl
* Role: openvpn_server
* Role: perl
* Role: php
* Role: policycoreutils
* Role: qemu_guest_agent
* Role: redis
* Role: repo_baseos
* Role: repo_collabora_code
* Role: repo_docker
* Role: repo_gitlab_ce
* Role: repo_grafana
* Role: repo_icinga
* Role: repo_influxdb
* Role: repo_mariadb
* Role: repo_mongodb
* Role: repo_mydumper
* Role: repo_remi
* Role: rocketchat
* Role: sshd
* Role: stig
* Role: system_update
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
