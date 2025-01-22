# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Note: Always add new entries to the top of the section, even if this results in multiple paragraphs for the same role. Otherwise the user will have to read through all the breaking changes every time they update LFOps. This way they can just read the new entries at the top, making it much easier for users to follow the CHANGELOG.


## [Unreleased] (in chronological order)

### Breaking Changes

Role:fangfrisch:
* Remove malwarepatrol as it is discontinued (see https://malwareblocklist.org/)

Role:graylog_server
* Only supports Graylog 6.1+ (Graylog Data Node based installations). Currently no more suppport für dedicated OpenSearch or Elasticsearch. Renamed `graylog_server__admin_user` to `graylog_server__root_user`.

Role:opensearch
* For new installations of OpenSearch 2.12 and later, you must define a custom admin password in `opensearch__opensearch_initial_admin_password` in order to set up an OpenSearch instance.

Role:postfix:
* now completely templates the whole config file. beware when running against existing hosts

Role:mailto_root:
* moved most functionality to role:postfix, and therefore removed the `mailto_root:configure` and `mailto_root:testmail` tags

Role:rocketchat:
* Switched deployment method from native installation to Podman container
* Removed `rocketchat__npm_version` variable
* Renamed and slightly altered:
    * `rocketchat__application_path` to `rocketchat__user_home_directory`, and changed default to `'/opt/rocketchat'`.
    * `rocketchat__service_enabled` to `rocketchat__container_enabled`
    * `rocketchat__service_state` to `rocketchat__container_state`
* Changed default of `rocketchat__mongodb_host` to `'host.containers.internal'`

Role:kvm_vm:
* `kvm_vm__boot_uefi` (bool) changed into `kvm_vm__boot` (string).

Module:bitwarden_item / Lookup Plugin:bitwarden:
* Removed parameters `password_uppercase`, `password_lowercase`, `password_numeric`, `password_special`
* Added parameter `password_choice`

Role:borg_local:
* Added new mandatory variable `borg_local__passphrase`

Role:apache_tomcat:
* Renamed `apache_tomcat__skip_manager` to `apache_tomcat__skip_admin_webapps`

Role:redis:
* Dropped support for Redis v6

Playbook:setup_icinga2_master:
* changed default of `setup_icinga2_master__icingaweb2_module_company__skip_role` from false to true.

Role:apache_httpd:
* changed default of `apache_httpd__skip_mod_security_coreruleset` from false to true.

Role:icingadb
* split into two roles, one for the IcingaDB daemon and one for IcingaDB Web. Have a look at the variables in the READMEs. Generally it is enough to rename `icingadb__api_user_login` to `icingadb_web__api_user_login`.

Playbook:setup_icinga2_master:
* changed the format of the role skip-variables from `playbook_name_skip_role_name` to `playbook_name__role_name__skip_role` for clarity and consistency. Have a look at the [README.md](./README.md#skipping-roles-in-a-playbook).
* also added `playbook_name__role_name__skip_role_injections` variables to disable or re-enabled the role's injections.

Role:systemd_journald
* The value for the variable `systemd_journald__conf_system_max_use` is now interpreted as a size in bytes. It supports the size specifications possible in `journald.conf` (e.g. `4G`). If you want to specify a percentage, use `'40%'`.

Role:redis
* removed support for Redis v5 (end of life)

Playbook:icinga2_agent
* Changed to also include the installation of the [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins). This can be skipped by setting `icinga2_agent__skip_monitoring_plugins: true`.

Playbook:setup_icinga2_master
* Changed default of `setup_icinga2_master__skip_icingaweb2_module_monitoring` from `false` to `true`

Role:apache_httpd
* Changed `conf_server_alias` from a string to a list
* the default of the `authz_document_root` vHost variable changed from `Require local` to `Require all granted`. This is a more sensible default, as `allowed_file_extensions` is used to restrict the access.
* removed the `authz_file_extensions` vHost variable. This was required to allow access to file extensions listed in `allowed_file_extensions'. From now on, the access to listed file extensions is always allowed.
* fixed a bug that allowed access to dotfiles which had extensions listed in `allowed_file_extensions`. Make sure this does not break your application, or set `allow_accessing_dotfiles: true`.

Role:apache_tomcat
* Changed `apache_tomcat__users__*_var` from a simple list to a list of dictionaries.

Role:collabora
* Changed `collabora__coolwsd_storage_wopi__*_var` to a list of dictionaries from a list of strings.
* Changed `collabora__language_packages__*_var` to a list of dictionaries from a list of strings.
* Renamed `collabora__coolwsd_allowed_languages` to `collabora__coolwsd_allowed_languages__*_var` and changed it to a list of dictionaries from a list of strings.

Role:grafana
* Changed default value for `grafana__serve_from_sub_path` from `true` to `false`

Role:graylog_server
* Remove support for Graylog < 5.0

Role:icingaweb2_module_vspheredb
* Removed the `v` prefix from the `icingaweb2_module_vspheredb__version` variable to be consistent with the other `icingaweb2_module_*` roles.

Role:login
* Changed default of `remove_other_sshd_authorized_keys` from `true` to `false`.

Role:mailto_root
* Changed `mailto_root__from` from optional to mandatory.
* Testmail to external addresses is now using sender address (`mailto_root__from`).

Role:mariadb_client
* Too trivial, removed (use the apps role instead)

Role:mongodb
* `mongodb__conf_net_bind_ip`: Changed from a string to a list of strings. For example:
```yaml
# old
mongodb__conf_net_bind_ip: '0.0.0.0'

# new
mongodb__conf_net_bind_ip:
  - '0.0.0.0'
```

Role:monitoring_plugins
* Remove the tasks for Nuitka compilation, as the compilation is done by the [Monitoring Plugins GitHub Action](https://github.com/Linuxfabrik/monitoring-plugins/actions/workflows/nuitka-compile.yml) now.
* Locks the version of the `monitoring-plugins` package after installing it. Updating the plugins should be done manually along with updating the monitoring system configuration.

Role:monitoring_plugins_grafana_dashboards
* Change from provisioning to grizzly for the deployment of the dashboards

Role:mount
* changed `mount__mounts` to `mount__mounts__host_var` / `mount__mounts__group_var`.

Role:nextcloud
* `nextcloud__apps_config`:
    * Renamed the variable to `nextcloud__app_configs__*_var`.
    * Added a `state` subkey that properly manages the state of the config options.
    * Made more use of the `value` subkey. `--value` is no longer required. See the example below.
```yaml
# old
nextcloud__apps_config:
  - { key: 'core',              value: 'shareapi_default_expire_date --value=yes' }
# new
nextcloud__app_configs__host_var:
  - key: 'core shareapi_default_expire_date'
    value: 'yes'
    state: 'present'
```
* `nextcloud__apps`:
    * Renamed the variable to `nextcloud__apps__*_var`.
    * Added a `state` subkey that properly manages the state of apps.
* `nextcloud__sysconfig`:
    * Renamed the variable to `nextcloud__sysconfig__*_var`.
    * Added a `state` subkey that properly manages the state of the config options.
    * Made more use of the `value` subkey. `--value` is no longer required, same as `nextcloud__app_configs__*_var`. See the example above.
* Removed `nextcloud__proxyconfig`. Use `nextcloud__sysconfig__*_var` instead.
* Implemented [notify_push](https://github.com/nextcloud/notify_push). Add the following to your Apache HTTPd config:
```apacheconf
RewriteRule ^\/push\/ws(.*) ws://nextcloud-server:7867/ws$1 [proxy,last]
RewriteRule ^\/push\/(.*)   http://nextcloud-server:7867/$1 [proxy,last]
ProxyPassReverse /push/     http://nextcloud-server:7867/
```
* Changed default of `nextcloud__timer_app_update_enabled` from `true` to `false`, as this can sometimes lead to Nextcloud ending up in maintenance mode
* Renamed `nextcloud__apache_httpd__vhosts_virtualhost_ip` to `nextcloud__vhost_virtualhost_ip`
* Renamed `nextcloud__apache_httpd__vhosts_virtualhost_port` to `nextcloud__vhost_virtualhost_port`

Role:opensearch
* Changed default of `opensearch__plugins_security_disabled` from `true` to `false`.

Role:openssl
* Too trivial, removed (use the apps role instead)

Role:perl
* Too trivial, removed (use the apps role instead)

Role:postgresql_server
* Renamed the `name` subkey of `postgresql_server__users__*_var` to `username` for consistency and easier integration of the Bitwarden lookup plugin.

Role:python
* Changed `python__modules__*_var` to a list of dictionaries from a list of strings.

Role:redis
* Changed default of `redis__service_timeout_start_sec` and `redis__service_timeout_stop_sec` from `5s` to `90s`.

Role:repo_icinga
* Renamed `repo_icinga__subscription_login` to `repo_icinga__basic_auth_login` and instead added a variable to explicitly use the Icinga Repo Subscription URL (`repo_icinga__use_subscription_url`). If you have `repo_icinga__subscription_login` set in your inventory, rename it to `repo_icinga__basic_auth_login` and set `repo_icinga__use_subscription_url: true` for the same effect as before.

Role:repo_mydumper
* adjusted to use https://repo.linuxfabrik.ch/mydumper/ by default
* removed `repo_mydumper__baseurl`, instead added `repo_mydumper__mirror_url`

Role:rocketchat
* Removed Rocket.Chat notifications from the default banaction

Role:selinux
* Changed `ports` subkey of `selinux__ports__*_var` to `port`, accepting only a single port or port range, not a list of ports / port ranges.

Role:sshd
* removed `sshd__ciphers`, `sshd__kex` and `sshd__macs` variables, as these settings are managed by `crypto-policy` on RHEL.
* now deploys the complete `/etc/ssh/sshd_config` as a template
* removed support for RHEL7

Role:system_update
* Remove `system_update__icinga2_master` variable. Use `system_update__icinga2_api_url` instead

Role:tar
* Too trivial, removed (use the apps role instead)


### Added

Role:repo_proxysql
* Added

Role:icinga2_master:
* Added `icinga2_master__bind_host` variable

Role:firewall:
* Added `firewall__firewalld_ports__*_var` and `firewall__firewalld_services__*_var` variables

Role:icingaweb2_module_x509
* Added `icingaweb2_module_x509__url` variable

Role:icinga2_agent
* Added `icinga2_agent:update` tag

Role:tools
* Added `tools__prompt_use_fqdn` variable

Role:graylog_datanode
* Added

Role:icingaweb2_module_reporting
* Added

Role:mariadb_server:
* Added Galera cluster installation
* Make datadir configurable, including copy of old one to the new location
* Make socket configurable

Role:glpi_agent
* Added

Role:icingaweb2_module_jira
* Added

Role:podman_containers
* Added

Role:blocky
* Added

Role:bind
* Added multiple new variables, now allowing a primary-secondary setup

Role:moodle
* Added

Role:icingaweb2_module_generictts
* Added

Role:icingaweb2_module_fileshipper
* Added

Role:icingaweb2_module_cube
* Added

Role:repo_redis:
* Added

Role:shell:
* Added

Role:collect_rpmnew_rpmsave:
* Added

Role:systemd_journald
* Add variable `systemd_journald__conf_system_keep_free`

Playbook:setup_basic
* Add support for AlmaLinux 8

Role:apache_httpd:
* added the `skip_allowed_file_extensions` vHost variable
* added the `skip_allowed_http_methods` vHost variable

Role:apache_solr
* Added

Role:bind
* add `bind__named_conf_raw` variable

Role:borg_local
* Added

Role:clamav
* Added

Role:cloud_init
* Add task to remove `/etc/cloud/cloud.cfg.rpmsave`

Role:dnf_versionlock
* Added

Role:duplicity:
* Add `duplicity__backup_full_if_older_than` variable

Role:fangfrisch
* Added

Role:github_project_createrepo
* Added

Role:grafana
* creation of service accounts and their tokens

Role:grafana_grizzly
* Added

Role:graylog_server
* Add variables and documentation for multi-node setup
* Add Debian support

Role:icingadb
* Added

Role:icingaweb2_module_businessprocess
* Added

Role:kvm_vm
* add the option to boot the VM with UEFI

Role:mirror
* Added

Role:mount
* Added

Role:python_venv
* allow specifying different certificate store
* allow specifying the python executable to be used in the venv

Role:repo_gitlab_runner
* Added

Role:repo_rpmfusion
* Added

Role:selinux
* add support for SELinux ports

Role:systemd_unit
* add support for mount units

Role:logrotate
* Add compression

Role:mongodb
* Add Debian support
* Add keyfile handling
* Adjust for replica set across members
* Implement user management (fix #89)

Role:opensearch
* Add Debian support
* Add variables for cluster configuration

Role:php
* Add tag `php:fpm`

Role:python_venv
* Add Debian support

Role:repo_baseos
* Add AlmaLinux 8 support

Role:repo_graylog
* Add Debian support

Role:repo_mongodb
* Add Debian support

Role:repo_opensearch
* Add Debian support

Role:systemd_journald
* Make SystemMaxUse configurable

Role:systemd_update
* Add option `-y` to `yum check-update`


### Fixed

Role:influxdb
* Fix wrong systemd service name, which was preventing influxdb dumps from being scheduled

Role:redis
* Fix various messages from log, fix v7 template settings, fix various comments and README


### Changed

Role:shell:
* add option to ignore errors during command execution

Role:mariadb_server:
* role:mariadb_server: mariadb-dump checks for the mydumper version and sets parameters accordingly

Role:apache_httpd:
* the default of the `conf_custom_log` vHost variable changed from unset to `'logs/{{ conf_server_name }}-access.log linuxfabrikio`

Role:audit:
* Add more config variables

Role:graylog_server
* Remove version defaults from the role

Role:icinga2_agent:
* New variable `icinga2_agent__validate_certs`

Role:open_vm_tools
* Starts and enables `vmtoolsd`

Role:opensearch
* Make `opensearch__version*` optional



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

Playbook:basic_setup
* Renamed to setup_basic to be consitent with the other setup playbooks
* Removed `audit` and `crypto_policy` roles for now

Role:acme_sh
* Added `name` subkey to `acme_sh__certificates`
* Moved `acme_sh__reload_cmd` to a subkey of `acme_sh__certificates`

Role:chrony
* Fixed wrong variable prefix: Adjusted `chrony_server__` to `chrony__`.

Role:collabora_code
* Renamed rolename and vars from `collabora_code` to `collabora`

Role:duplicity
* Renamed `duplicity__public_master_long_keyid` variable to `duplicity__gpg_encrypt_master_key`.
* Renamed `duplicity__public_master_key` variable to `duplicity__gpg_encrypt_master_key_block`.
* Changed the format of `duplicity__backup_sources__host_var`.

Role:fail2ban
* Adjusted subkeys of `fail2ban__jails__group_var` / `fail2ban__jails__host_var`

Role:git
* Added ...
* ... and later removed in favor of a more general `app` role

Role:hostname
* Renamed `hostname__domain_name` to `hostname__domain_part`
* Renamed `hostname__hostname` to `hostname__full_hostname`

Role:icinga2_agent
* Added new mandatory variable `icinga2_agent__icinga2_master_cn`
* Made `icinga2_agent__icinga2_master_host` optional
* Most users can replace all instances of `icinga2_agent__icinga2_master_host` to `icinga2_agent__icinga2_master_cn`

Role:infomaniak_vm
* Renamed `infomaniak_vm__password` to `infomaniak_vm__api_password`
* Renamed `infomaniak_vm__project_id` to `infomaniak_vm__api_project_id`
* Renamed `infomaniak_vm__username` to `infomaniak_vm__api_username`
* Renamed `infomaniak_vm__volume_size` to `infomaniak_vm__separate_boot_volume_size`

Role:java
* Removed, better substituted by `apps` role.

Role:kernel_settings
* Make `kernel_settings__` variables injection-capable via `kernel_settings__host_*`, `kernel_settings__group_*` and `kernel_settings__dependent_*`.

Role:libselinux_python:
* Renamed the role to policycoreutils.

Role:login
* Changed logic and renamed `login__users` to two combined variables `login__users__group_var` (define users in group vars) and `login__users__host_var` (define users in host vars).

Role:mariadb_server
* Renamed `mariadb_server__admin_login` to `mariadb_server__admin_user`
* Moved `mariadb_server__admin_host` to `mariadb_server__admin_user["host"]`
* Renamed `mariadb_server__dump_login` to `mariadb_server__dump_user`
* Moved `mariadb_server__dump_user_*` to subkeys in `mariadb_server__dump_user`

Role:monitoring_plugins
* Renamed `monitoring_plugins__deploy_notification_plugins` to `monitoring_plugins__skip_notification_plugins` and flipped the logic.

Role php:
* Made more variables injectable, therefore the variables have a new name.

Role:stig
* Moved to a new GitHub repo (temporarily)

Role:system_update
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
