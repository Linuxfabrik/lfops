# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Breaking Changes

Role: duplicity
* Renamed `duplicity__public_master_long_keyid` variable to `duplicity__gpg_encrypt_master_key`.
* Renamed `duplicity__public_master_key` variable to `duplicity__gpg_encrypt_master_key_block`.
* Changed the format of `duplicity__host_backup_sources`.

Role: kernel_settings
* Make `kernel_settings__` variables injection-capable via `kernel_settings__host_*`, `kernel_settings__group_*` and `kernel_settings__dependent_*`.

Role: login
* Changed logic and renamed `login__users` to two combined variables `login__group_users` (define users in group vars) and `login__host_users` (define users in host vars).

Role: chrony
* Fixed wrong variable prefix: Adjusted `chrony_server__` to `chrony__`.



### Added

New features:

* This CHANGELOG.

* Module: mariadb_user
* Role network: Added functionality to configure network connections.

* Role: acme_sh
* Role: apache_httpd
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
* Role: exoscale_vm
* Role: fail2ban
* Role: firewall
* Role: git
* Role: glances
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
* Role: libselinux_python
* Role: login
* Role: mailto_root
* Role: mariadb_server
* Role: network
* Role: nextcloud
* Role: openssl
* Role: openvpn_server
* Role: perl
* Role: php
* Role: redis
* Role: repo_baseos
* Role: repo_collabora_code
* Role: repo_icinga
* Role: repo_influxdb
* Role: repo_mariadb
* Role: repo_mydumper
* Role: repo_remi
* Role: sshd
* Role: stig
* Role: system_update
* Role: tar
* Role: timezone
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
