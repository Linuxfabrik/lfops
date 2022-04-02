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
* This CHANGELOG.
* Role: at
* Role: cockpit
* Role: dnf_makecache
* Role: exoscale_vm
* Role: firewall
* Role: glances
* Role: kdump
* Role: login
* Role: network
* Role: sshd
* Role: timezone
* Role: yum_utils

### Changed
* Role duplicity: Implemented massive-parallel backups.


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
