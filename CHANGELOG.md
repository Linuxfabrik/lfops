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

### Added

New features:

* This CHANGELOG.

* Role network: Added functionality to configure network connections.

* Role: acme_sh
* Role: at
* Role: audit
* Role: bind
* Role: chrony
* Role: cloud_init
* Role: cockpit
* Role: crypto_policy
* Role: dnf_makecache
* Role: exoscale_vm
* Role: firewall
* Role: git
* Role: glances
* Role: hetzner_vm
* Role: hostname
* Role: icinga2_master
* Role: icingaweb2_module_vspheredb
* Role: influxdb
* Role: infomaniak_vm
* Role: java
* Role: kdump
* Role: kernel_settings
* Role: keycloak
* Role: libselinux_python
* Role: login
* Role: mailto_root
* Role: mariadb_server
* Role: network
* Role: openssl
* Role: openvpn_server
* Role: perl
* Role: php
* Role: repo_baseos
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

* Module: mariadb_user

### Changed

Changes in existing functionality:

* Role duplicity: Implemented massive-parallel backups.
* Role mariadb_server: Changed `mariadb_server__admin_host` to a list.


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
