# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Maintainer note:** Always add new entries to the top of the Unreleased section (newest first), even if this results in multiple entries for the same role. This way users only need to read the new entries at the top.


## [Unreleased]

### Breaking Changes

* **role:kvm_host**: Change NAT to be explicitly activated for virtual nets
* **role:apache_httpd**: Change the default to not install/enable mod_qos by default (it is no longer shipped in EPEL 10)

### Added

* **role:postfix**: Add RHEL 10 support
* **role:kvm_vm**: Add the ability to resize disks
* **role:infomaniak_vm**: Add the ability to choose the deployment region/datacenter
* **role:crypto_policy**: Add RHEL 10 support
* **role:elastic_agent**: Add new role
* **role:elastic_agent_fleet_server**: Add new role
* **role:fail2ban**: Make `bantime` configurable for the sshd and portscan jails
* **role:duplicity**: Add support for RHEL 10
* **role:php**: Make `request_slowlog_timeout` and `request_terminate_timeout` configurable
* **role:graylog_server**: Make `http_publish_uri` configurable; make `trusted_proxies` configurable
* **role:graylog_datanode**: Add template for 7.0
* **role:graylog_server**: Add template for 7.0
* **role:lvm**: Add new role
* **role:logrotate**: Add support for RHEL 10
* **role:sshd**: Add support for RHEL 10
* **role:yum_utils**: Add support for RHEL 10
* **role:repo_epel**: Add support for RHEL 10
* **role:repo_baseos**: Add support for RHEL 10
* **role:policycoreutils**: Add support for RHEL 10
* **role:mailx**: Add support for RHEL 10
* **role:graylog_server**: Make `message_journal_dir` configurable
* **playbook:setup_basic**: Add lvm role

### Changed

* **role:repo_remi**: Install Composer from `remi-modular` repository
* **role:icingadb**: Enhance `config.yml` template
* **role:apache_httpd**: Improve output; bump Core Rule Set to 4.21.0

### Fixed

* **role:systemd_unit**: Correct the removal of units
* **role:bind**: Fix incorrect distribution version comparison in named.conf
* **role:python_venv**: Fix venv path in remove venv task
* **role:apache_httpd**: Prevent deployment of mods that should be disabled
* **role:repo_postgresql**: Remove EOL versions, adjust for RHEL 9 & 10
* **role:mariadb_server**: Fix the root cause of `/run/mariadb/wsrep-start-position: No such file or directory` after update of MariaDB (10.11.14 -> 10.11.15 or 11.4.8 -> 11.4.9)
* **role:ansible_init**: Install Ansible Collections from requirements.txt since that file contains the correct versions for running against RHEL 8
* **role:kibana**: Enable log rotation
* **role:kibana**: Fix `when` statement
* **playbook:setup_icinga2_master**: Fix syntax; add missing `kernel_settings` for MariaDB
* **lookup_plugin:bitwarden**: Make it more robust
* **role:monitoring_plugins**: Fix installation of package against non-RHEL hosts
* **role:rocketchat**: Fix typo and order of calls in playbook


## [v5.1.0] - 2026-01-06

### Added

* **role:kibana**: Add `kibana__raw` variable
* **role:elasticsearch**: Add `elasticsearch__raw` variable
* **role:apache_httpd**: Add nice ErrorDocuments
* **role:kibana**: Make SSL settings configurable


## [v5.0.0] - 2025-11-14

### Breaking Changes

* **role:elasticsearch_oss**: Rename to `elasticsearch`, as both the free and subscription versions are now in the same package
* **role:repo_elasticsearch_oss**: Remove, as both the free and subscription versions are now in the same package

### Added

* **role:acme_sh**: Add `acme_sh__reload_cmd` to allow setting the local reload command globally for all certificates
* **role:collabora**: Add new template versions
* **role:elasticsearch**:
  * Make `node.roles` configurable
  * Add variables for allocation awareness
  * Add `elasticsearch__path_data` variable to configure custom data directory
  * Improve handling of TLS certificates
  * Allow creation of clusters
* **role:gitlab_ce**: Make the `gitlab.rb` options for default project features, email reply-to address, LDAP integration and the upload path configurable
* **role:graylog_server**: Re-add `graylog_server__elasticsearch_hosts` to allow setups without Graylog Data Node
* **role:kibana**: Add new role
* **role:mariadb_server**:
  * Add support for version 11.8 (LTS)
  * Make `log_slave_updates` configurable
  * Add `mariadb_server__cnf_server_raw` variable
* **role:podman_containers**: Add option to enable the `podman-auto-update.timer`
* **role:postfix**: Add `postfix__lookup_tables__*_var` to allow easy deployment of lookup tables
* **role:redis**: Add template for version 8.2
* **role:selinux**:
  * Add handling of SELinux modules
  * Add capability to run `restorecon`
  * Add `selinux__policy` variable
* **role:shell**: Add `shell__limit_cmds` to limit executed shell commands
* **playbook:selinux**: Add `selinux__skip_policycoreutils` variable

### Fixed

* **role:acme_sh**: Fix certificate paths for Ubuntu and Debian
* **role:apache_solr**: Automatically install the correct Java version
* **role:elasticsearch**:
  * Prevent undefined variable error
  * Fix default of `elasticsearch__path_data`
  * Set `vm.swappiness` to 1
* **role:firewall**: Ensure `firewalld` is installed if chosen
* **role:icinga2_agent**: Deploy logrotate config as hotfix for upstream issue ([#188](https://github.com/Linuxfabrik/lfops/issues/188))
* **role:icinga2_master**: Deploy logrotate config as hotfix for upstream issue ([#189](https://github.com/Linuxfabrik/lfops/issues/189))
* **role:icingaweb2**: Fix Icinga username for Debian
* **role:keycloak**: Install correct Java version, removing the `keycloak__java_package_name` variable
* **role:kvm_vm**: Fix path
* **role:mariadb_server**: Fix `/run/mariadb/wsrep-start-position: No such file or directory` after update
* **role:mastodon**: Adjust to breaking changes in `elasticsearch` role
* **role:monitoring_plugins**:
  * Also install `lib` via source if `monitoring_plugins__install_method: 'source'` is set
  * Add workaround for pip on Debian & Ubuntu
* **role:openvpn_server**: Actually remove CCD with `state: 'absent'`
* **role:repo_mariadb**: Fix handling of GPG key for Debian & Ubuntu
* **role:repo_opensearch**: Deploy correct GPG key for selected OpenSearch version
* **role:rocketchat**: Fix syntax of HealthCmd
* **playbook:opensearch**: Prevent the whole cluster from restarting at once
* **playbook:setup_icinga2_master**:
  * Fix order
  * Add missing injection for MariaDB Python modules


## [v4.0.0] - 2025-10-03

### Breaking Changes

* **role:icinga2_master**: Remove support for IDO, as it is deprecated in favor of IcingaDB. The following variables can be removed from the inventory:
  * `icinga2_master__database_enable_ha`
  * `icinga2_master__database_host`
  * `icinga2_master__database_login`
  * `icinga2_master__database_name`
* **role:icingaweb2_module_monitoring**: Remove, as it is deprecated in favor of IcingaDB. All variables starting with `icingaweb2_module_monitoring__` can be removed from the inventory.
* **role:mariadb_server**:
  * Remove support for EOL version 10.5
  * Remove `mariadb_server__cnf_expire_logs_days__group_var` / `mariadb_server__cnf_expire_logs_days__host_var`, use `mariadb_server__cnf_binlog_expire_logs_seconds__group_var` / `mariadb_server__cnf_binlog_expire_logs_seconds__host_var` instead

### Added

* **role:acme_sh**: Add support for Debian/Ubuntu
* **role:apache_httpd**: Add support for Debian/Ubuntu
* **role:elasticsearch_oss**: Add `elasticsearch_oss__discovery_type`, `elasticsearch_oss__network_host` variables; reset JVM tmp directory
* **role:icingaweb2_module_pdfexport**: Add new role
* **role:kvm_host**: Add support for Ubuntu 24.04
* **role:mastodon**: Add new role
* **role:mongodb**: Add RedHat config template for v8.0
* **role:moodle**: Add `moodle__version` variable to select the major and minor version
* **role:postgresql_server**: Add `postgresql_server__login_password` variable
* **role:repo_mydumper**: Add official repos for Debian-based systems
* **role:system_update**: Add `metadata_timer_sync` option for cache-only installations
* **tool:particle**: Add new tool

### Changed

* **role:gitlab_ce**: Update template to v18.4.0
* **role:mariadb_server**:
  * Create a backup file of the most important config files before applying new versions
  * Make ownership of SSL certificate CIS-conform
* **role:monitoring_plugins**: Remove `monitoring_plugins__skip_notification_plugins__*_var` variables as they are now always installed
* **role:systemd_journald**: Move config file to `/etc/systemd/journald.conf.d/z00-linuxfabrik.conf`, improve calculations and default values

### Fixed

* **role:apache_httpd**:
  * Use platform-specific group for htpasswd files
  * Allow unsetting the `CustomLog` directive
* **role:apache_tomcat**: Adjust logrotate config for multiple Tomcat instances
* **role:bind**:
  * Do not run `named-checkzone` against forward zones
  * Remove obsolete options for RHEL 9
* **role:duplicity**: Use python3.11 to prevent errors when installing latest duplicity
* **role:elasticsearch_oss**: Move tmpdir to a location with exec permissions specified by CIS hardening
* **role:keycloak**: Set `keycloak__proxy_trusted_addresses` to `'127.0.0.1'` due to FD leak if using `'127.0.0.1,::1'`
* **role:mariadb_server**:
  * Correct mydumper dependency packages for Debian-based systems
  * Fix failing dumps after mydumper update to v0.20.1
  * Adjust SELinux settings after upgrades
  * Grant `binlog monitor` privilege for `mariadb-backup` user
* **role:monitoring_plugins**:
  * Fix path to old sudoers file
  * Fix script execution in CIS-hardened `/tmp`
  * Improve versionlock and install SELinux package on RHEL
* **role:nextcloud**: Add missing `env` module
* **role:repo_opensearch**: Fix GPG key


## [v3.0.0] - 2025-06-13

### Breaking Changes

* **role:apache_httpd**:
  * Change `conf_server_alias` from a string to a list
  * Change default of the `authz_document_root` vHost variable from `Require local` to `Require all granted`. This is a more sensible default, as `allowed_file_extensions` is used to restrict the access.
  * Remove the `authz_file_extensions` vHost variable. Access to listed file extensions is now always allowed.
  * Fix a bug that allowed access to dotfiles which had extensions listed in `allowed_file_extensions`. Make sure this does not break your application, or set `allow_accessing_dotfiles: true`.
  * Change default of `apache_httpd__skip_mod_security_coreruleset` from `false` to `true`
* **role:apache_tomcat**:
  * Rename `apache_tomcat__skip_manager` to `apache_tomcat__skip_admin_webapps`
  * Change `apache_tomcat__users__*_var` from a simple list to a list of dictionaries
* **role:borg_local**: Add new mandatory variable `borg_local__passphrase`
* **role:collabora**:
  * Change `collabora__coolwsd_storage_wopi__*_var` to a list of dictionaries from a list of strings
  * Change `collabora__language_packages__*_var` to a list of dictionaries from a list of strings
  * Rename `collabora__coolwsd_allowed_languages` to `collabora__coolwsd_allowed_languages__*_var` and change it to a list of dictionaries from a list of strings
* **role:fangfrisch**: Remove malwarepatrol as it is discontinued (see https://malwareblocklist.org/)
* **role:grafana**: Change default value for `grafana__serve_from_sub_path` from `true` to `false`
* **role:graylog_server**:
  * Remove support for Graylog < 5.0
  * Only support Graylog 6.1+ (Graylog Data Node based installations). Currently no more support for dedicated OpenSearch or Elasticsearch.
  * Rename `graylog_server__admin_user` to `graylog_server__root_user`
* **role:icinga_kubernetes**: Switch config to v0.3.0 multi-cluster format, remove `icinga_kubernetes__kubeconfig_path`
* **role:icingadb**: Split into two roles, one for the IcingaDB daemon and one for IcingaDB Web. Have a look at the variables in the READMEs. Generally it is enough to rename `icingadb__api_user_login` to `icingadb_web__api_user_login`.
* **role:icingaweb2_module_director**: The `icingaweb2_module_director:basket` tag only runs if explicitly called to prevent accidental config overwrites
* **role:icingaweb2_module_vspheredb**: Remove the `v` prefix from the `icingaweb2_module_vspheredb__version` variable to be consistent with the other `icingaweb2_module_*` roles
* **role:kvm_vm**: Change `kvm_vm__boot_uefi` (bool) to `kvm_vm__boot` (string)
* **role:login**: Change default of `remove_other_sshd_authorized_keys` from `true` to `false`
* **role:mailto_root**:
  * Move most functionality to `role:postfix`, remove the `mailto_root:configure` and `mailto_root:testmail` tags
  * Change `mailto_root__from` from optional to mandatory
  * Testmail to external addresses now uses sender address (`mailto_root__from`)
* **role:mariadb_client**: Remove (use the `apps` role instead)
* **role:mariadb_server**:
  * Remove support for EOL versions 10.3 and 10.4
  * Remove support for non-LTS versions
  * Change default of `mariadb_server__cnf_client_ssl_verify_server_cert__*_var` for versions lower than 10.11 from `true` to `false` to prevent errors when SSL is disabled
* **module:bitwarden_item**, **lookup_plugin:bitwarden**:
  * Remove parameters `password_uppercase`, `password_lowercase`, `password_numeric`, `password_special`
  * Add parameter `password_choice`
* **role:mongodb**: Change `mongodb__conf_net_bind_ip` from a string to a list of strings. For example:
  ```yaml
  # old
  mongodb__conf_net_bind_ip: '0.0.0.0'

  # new
  mongodb__conf_net_bind_ip:
    - '0.0.0.0'
  ```
* **role:monitoring_plugins**:
  * Remove variables:
    * `monitoring_plugins__pip_executable`
    * `monitoring_plugins__pip_package`
    * `monitoring_plugins__python__modules`
    * `monitoring_plugins__windows_variant`
  * The `lfops__monitoring_plugins_version` variable (and all the `*.monitoring_plugin.*_version` variables) now only accepts a specific release or the value `dev`. `stable` or `latest` are no longer supported.
  * The `lfops__monitoring_plugins_version` variable is now mandatory.
  * Rename `monitoring_plugins__linux_variant` to `monitoring_plugins__install_method`:
    * `monitoring_plugins__linux_variant: 'python'` becomes `monitoring_plugins__install_method: 'source'`
  * Rename `monitoring_plugins__repo_version` to `monitoring_plugins__version`:
    * `monitoring_plugins__repo_version: 'latest'` becomes `monitoring_plugins__version: 'dev'`
  * Remove the tasks for Nuitka compilation, as the compilation is done by the [Monitoring Plugins GitHub Action](https://github.com/Linuxfabrik/monitoring-plugins/actions/workflows/nuitka-compile.yml) now
  * Lock the version of the `monitoring-plugins` package after installing it. Updating the plugins should be done manually along with updating the monitoring system configuration.
* **role:monitoring_plugins_grafana_dashboards**: Change from provisioning to grizzly for the deployment of the dashboards
* **role:mount**: Change `mount__mounts` to `mount__mounts__host_var` / `mount__mounts__group_var`
* **role:nextcloud**:
  * Rename `nextcloud__apps_config` to `nextcloud__app_configs__*_var`, add `state` subkey, make more use of the `value` subkey. `--value` is no longer required:
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
  * Rename `nextcloud__apps` to `nextcloud__apps__*_var`, add `state` subkey
  * Rename `nextcloud__sysconfig` to `nextcloud__sysconfig__*_var`, add `state` subkey, make more use of the `value` subkey (same as `nextcloud__app_configs__*_var`)
  * Remove `nextcloud__proxyconfig`. Use `nextcloud__sysconfig__*_var` instead.
  * Implement [notify_push](https://github.com/nextcloud/notify_push). Add the following to your Apache HTTPd config:
    ```apacheconf
    RewriteRule ^\/push\/ws(.*) ws://nextcloud-server:7867/ws$1 [proxy,last]
    RewriteRule ^\/push\/(.*)   http://nextcloud-server:7867/$1 [proxy,last]
    ProxyPassReverse /push/     http://nextcloud-server:7867/
    ```
  * Change default of `nextcloud__timer_app_update_enabled` from `true` to `false`, as this can sometimes lead to Nextcloud ending up in maintenance mode
  * Rename `nextcloud__apache_httpd__vhosts_virtualhost_ip` to `nextcloud__vhost_virtualhost_ip`
  * Rename `nextcloud__apache_httpd__vhosts_virtualhost_port` to `nextcloud__vhost_virtualhost_port`
* **role:opensearch**:
  * Change default of `opensearch__plugins_security_disabled` from `true` to `false`
  * For new installations of OpenSearch 2.12 and later, you must define a custom admin password in `opensearch__opensearch_initial_admin_password`
* **role:openssl**: Remove (use the `apps` role instead)
* **role:perl**: Remove (use the `apps` role instead)
* **role:postfix**: Now completely templates the whole config file. Beware when running against existing hosts.
* **role:postgresql_server**: Rename the `name` subkey of `postgresql_server__users__*_var` to `username` for consistency and easier integration of the Bitwarden lookup plugin
* **role:python**: Change `python__modules__*_var` to a list of dictionaries from a list of strings
* **role:redis**:
  * Drop support for Redis v5 (end of life)
  * Drop support for Redis v6
  * Change default of `redis__service_timeout_start_sec` and `redis__service_timeout_stop_sec` from `5s` to `90s`
* **role:repo_icinga**:
  * Remove `repo_icinga__use_subscription_url` for RHEL (and compatibles) as the packages without a subscription are outdated. The variable is now only effective for openSUSE and SLES.
  * Rename `repo_icinga__subscription_login` to `repo_icinga__basic_auth_login` and add a variable to explicitly use the Icinga Repo Subscription URL (`repo_icinga__use_subscription_url`). If you have `repo_icinga__subscription_login` set in your inventory, rename it to `repo_icinga__basic_auth_login` and set `repo_icinga__use_subscription_url: true` for the same effect.
* **role:repo_mydumper**: Adjust to use https://repo.linuxfabrik.ch/mydumper/ by default. Remove `repo_mydumper__baseurl`, add `repo_mydumper__mirror_url` instead.
* **role:rocketchat**:
  * Switch deployment method from native installation to Podman container
  * Remove `rocketchat__npm_version` variable
  * Rename and alter:
    * `rocketchat__application_path` to `rocketchat__user_home_directory` (new default: `'/opt/rocketchat'`)
    * `rocketchat__service_enabled` to `rocketchat__container_enabled`
    * `rocketchat__service_state` to `rocketchat__container_state`
  * Change default of `rocketchat__mongodb_host` to `'host.containers.internal'`
  * Remove Rocket.Chat notifications from the default banaction
* **role:selinux**: Change `ports` subkey of `selinux__ports__*_var` to `port`, accepting only a single port or port range, not a list
* **role:sshd**:
  * Remove `sshd__ciphers`, `sshd__kex` and `sshd__macs` variables, as these settings are managed by `crypto-policy` on RHEL
  * Now deploy the complete `/etc/ssh/sshd_config` as a template
  * Remove support for RHEL 7
* **role:system_update**: Remove `system_update__icinga2_master` variable. Use `system_update__icinga2_api_url` instead.
* **role:systemd_journald**: The value for `systemd_journald__conf_system_max_use` is now interpreted as a size in bytes. It supports the size specifications possible in `journald.conf` (e.g. `4G`). If you want to specify a percentage, use `'40%'`.
* **role:tar**: Remove (use the `apps` role instead)
* **playbook:icinga2_agent**: Change to also include the installation of the [Linuxfabrik Monitoring Plugins](https://github.com/Linuxfabrik/monitoring-plugins). This can be skipped by setting `icinga2_agent__skip_monitoring_plugins: true`.
* **playbook:setup_icinga2_master**:
  * Change default of `setup_icinga2_master__icingaweb2_module_company__skip_role` from `false` to `true`
  * Change the format of the role skip-variables from `playbook_name_skip_role_name` to `playbook_name__role_name__skip_role` for clarity and consistency. Have a look at the [README.md](./README.md#skipping-roles-in-a-playbook).
  * Add `playbook_name__role_name__skip_role_injections` variables to disable or re-enable the role's injections
  * Change default of `setup_icinga2_master__skip_icingaweb2_module_monitoring` from `false` to `true`

### Added

* **role:alternatives**: Add new role
* **role:apache_httpd**:
  * Add some mods
  * Add `skip_allowed_file_extensions` vHost variable
  * Add `skip_allowed_http_methods` vHost variable
* **role:apache_solr**: Add new role
* **role:audit**: Add more config variables
* **role:bind**:
  * Add multiple new variables, now allowing a primary-secondary setup
  * Add `bind__named_conf_raw` variable
* **role:blocky**: Add new role
* **role:borg_local**: Add new role
* **role:clamav**: Add new role
* **role:cloud_init**: Add task to remove `/etc/cloud/cloud.cfg.rpmsave`
* **role:collect_rpmnew_rpmsave**: Add new role
* **role:dnf_versionlock**: Add new role
* **role:duplicity**: Add `duplicity__backup_full_if_older_than` variable
* **role:fangfrisch**: Add new role
* **role:firewall**: Add `firewall__firewalld_ports__*_var` and `firewall__firewalld_services__*_var` variables
* **role:github_project_createrepo**: Add new role
* **role:glpi_agent**: Add new role
* **role:grafana**: Add creation of service accounts and their tokens
* **role:grafana_grizzly**: Add new role
* **role:graylog_datanode**: Add new role
* **role:graylog_server**: Add variables and documentation for multi-node setup; add Debian support
* **role:icinga2_agent**: Add `icinga2_agent:update` tag; add `icinga2_agent__validate_certs` variable
* **role:icinga2_master**: Add `icinga2_master__bind_host` variable
* **role:icinga_kubernetes**: Add new role
* **role:icinga_kubernetes_web**: Add new role
* **role:icingadb**: Add new role
* **role:icingaweb2_module_businessprocess**: Add new role
* **role:icingaweb2_module_cube**: Add new role
* **role:icingaweb2_module_fileshipper**: Add new role
* **role:icingaweb2_module_generictts**: Add new role
* **role:icingaweb2_module_jira**: Add new role
* **role:icingaweb2_module_reporting**: Add new role
* **role:icingaweb2_module_x509**: Add `icingaweb2_module_x509__url` variable
* **role:kvm_vm**: Add the option to boot the VM with UEFI
* **role:logrotate**: Add compression
* **role:mariadb_server**:
  * Add `mariadb_server__cnf_wsrep_sst_auth` and `mariadb_server__cnf_wsrep_sst_method` variables
  * Add `mariadb_server__cnf_extra_max_connections__*_var` and `mariadb_server__cnf_extra_port__*_var` variables
  * Add support for client and server TLS
  * Add Galera cluster installation
  * Make datadir configurable, including copy of old data to the new location
  * Make socket configurable
* **role:mirror**: Add new role
* **role:mongodb**:
  * Add Debian support
  * Add keyfile handling
  * Adjust for replica set across members
  * Implement user management ([fix #89](https://github.com/Linuxfabrik/lfops/issues/89))
* **role:moodle**: Add new role
* **role:mount**: Add new role
* **role:opensearch**: Add Debian support; add variables for cluster configuration
* **role:php**: Add tag `php:fpm`
* **role:podman_containers**: Add new role
* **role:proxysql**: Add new role
* **role:python_venv**:
  * Allow specifying different certificate store
  * Allow specifying the Python executable to be used in the venv
  * Add Debian support
* **role:repo_baseos**: Add AlmaLinux 8 support
* **role:repo_epel**: Add `repo_epel__epel_cisco_openh264_enabled` variable
* **role:repo_gitlab_runner**: Add new role
* **role:repo_graylog**: Add Debian support
* **role:repo_mongodb**: Add Debian support
* **role:repo_opensearch**: Add Debian support
* **role:repo_proxysql**: Add new role
* **role:repo_redis**: Add new role
* **role:repo_rpmfusion**: Add new role
* **role:selinux**: Add support for SELinux ports
* **role:shell**: Add new role; add option to ignore errors during command execution
* **role:system_update**: Add option `-y` to `yum check-update`
* **role:systemd_journald**: Add variable `systemd_journald__conf_system_keep_free`; make `SystemMaxUse` configurable
* **role:systemd_unit**: Add support for mount units
* **role:tools**: Add `tools__prompt_use_fqdn` variable
* **playbook:setup_basic**: Add support for AlmaLinux 8

### Changed

* **role:apache_httpd**: Change default of the `conf_custom_log` vHost variable from unset to `'logs/{{ conf_server_name }}-access.log linuxfabrikio'`
* **role:graylog_server**: Remove version defaults from the role
* **role:icingaweb2_module_grafana**: Change GitHub repo from Mikesch-mp to NETWAYS
* **role:mariadb_server**: mariadb-dump checks for the mydumper version and sets parameters accordingly
* **role:open_vm_tools**: Start and enable `vmtoolsd`
* **role:opensearch**: Make `opensearch__version*` optional

### Fixed

* **role:influxdb**: Fix wrong systemd service name, which was preventing InfluxDB dumps from being scheduled
* **role:mariadb_server**:
  * Fix handler when `bind_address` is not localhost
  * Add installation of missing package for mariabackup Galera SST
  * Fix clone-datadir against new Galera cluster
* **role:redis**: Fix various messages from log, fix v7 template settings, fix various comments and README


## [v2.0.1] - 2023-02-28

### Changed

* Adjustments for the [Ansible Galaxy Release](https://galaxy.ansible.com/linuxfabrik/lfops)


## [v2.0.0] - 2023-02-28

### Breaking Changes

* **All roles**: Rename all injectable variables:
  * `rolename__combined_varname` to `rolename__varname__combined_var`
  * `rolename__dependent_varname` to `rolename__varname__dependent_var`
  * `rolename__group_varname` to `rolename__varname__group_var`
  * `rolename__host_varname` to `rolename__varname__host_var`
  * `rolename__role_varname` to `rolename__varname__role_var`
* **role:acme_sh**:
  * Add `name` subkey to `acme_sh__certificates`
  * Move `acme_sh__reload_cmd` to a subkey of `acme_sh__certificates`
* **role:chrony**: Fix wrong variable prefix: adjust `chrony_server__` to `chrony__`
* **role:collabora**: Rename rolename and vars from `collabora_code` to `collabora`
* **role:duplicity**:
  * Rename `duplicity__public_master_long_keyid` to `duplicity__gpg_encrypt_master_key`
  * Rename `duplicity__public_master_key` to `duplicity__gpg_encrypt_master_key_block`
  * Change the format of `duplicity__backup_sources__host_var`
* **role:fail2ban**: Adjust subkeys of `fail2ban__jails__group_var` / `fail2ban__jails__host_var`
* **role:git**: Add and later remove in favor of a more general `apps` role
* **role:hostname**:
  * Rename `hostname__domain_name` to `hostname__domain_part`
  * Rename `hostname__hostname` to `hostname__full_hostname`
* **role:icinga2_agent**:
  * Add new mandatory variable `icinga2_agent__icinga2_master_cn`
  * Make `icinga2_agent__icinga2_master_host` optional
  * Most users can replace all instances of `icinga2_agent__icinga2_master_host` with `icinga2_agent__icinga2_master_cn`
* **role:infomaniak_vm**:
  * Rename `infomaniak_vm__password` to `infomaniak_vm__api_password`
  * Rename `infomaniak_vm__project_id` to `infomaniak_vm__api_project_id`
  * Rename `infomaniak_vm__username` to `infomaniak_vm__api_username`
  * Rename `infomaniak_vm__volume_size` to `infomaniak_vm__separate_boot_volume_size`
* **role:java**: Remove, better substituted by the `apps` role
* **role:kernel_settings**: Make `kernel_settings__` variables injection-capable via `kernel_settings__host_*`, `kernel_settings__group_*` and `kernel_settings__dependent_*`
* **role:libselinux_python**: Rename the role to `policycoreutils`
* **role:login**: Change logic and rename `login__users` to two combined variables `login__users__group_var` (define users in group vars) and `login__users__host_var` (define users in host vars)
* **role:mariadb_server**:
  * Rename `mariadb_server__admin_login` to `mariadb_server__admin_user`
  * Move `mariadb_server__admin_host` to `mariadb_server__admin_user["host"]`
  * Rename `mariadb_server__dump_login` to `mariadb_server__dump_user`
  * Move `mariadb_server__dump_user_*` to subkeys in `mariadb_server__dump_user`
* **role:monitoring_plugins**: Rename `monitoring_plugins__deploy_notification_plugins` to `monitoring_plugins__skip_notification_plugins` and flip the logic
* **role:php**: Make more variables injectable, therefore the variables have a new name
* **role:stig**: Move to a new GitHub repo (temporarily)
* **role:system_update**: Rename variables (note: old and new names appear identical in the original CHANGELOG, likely a documentation error):
  * `system_update__mail_recipients_new_configfiles` => `system_update__mail_recipients_new_configfiles`
  * `system_update__mail_recipients_updates` => `system_update__mail_recipients_updates`
  * `system_update__mail_from` => `system_update__mail_from`
  * `system_update__mail_subject_prefix` => `system_update__mail_subject_prefix`
  * `system_update__notify_and_schedule_on_calendar` => `system_update__notify_and_schedule_on_calendar`
* **playbook:basic_setup**: Rename to `setup_basic` to be consistent with the other setup playbooks. Remove `audit` and `crypto_policy` roles for now.

### Added

* This CHANGELOG
* **role:acme_sh**: Add new role
* **role:ansible_init**: Add new role
* **role:apache_httpd**: Add new role
* **role:apache_tomcat**: Add new role
* **role:apps**: Add new role
* **role:at**: Add new role
* **role:audit**: Add new role
* **role:bind**: Add new role
* **role:chrony**: Add new role
* **role:cloud_init**: Add new role
* **role:cockpit**: Add new role
* **role:collabora**: Add new role
* **role:coturn**: Add new role
* **role:crypto_policy**: Add new role
* **role:dnf_makecache**: Add new role
* **role:docker**: Add new role
* **role:elasticsearch_oss**: Add new role
* **role:exoscale_vm**: Add new role
* **role:fail2ban**: Add new role
* **role:firewall**: Add new role
* **role:freeipa_client**: Add new role
* **role:freeipa_server**: Add new role
* **role:glances**: Add new role
* **role:grafana**: Add new role
* **role:grav**: Add new role
* **role:graylog_server**: Add new role
* **role:haveged**: Add new role
* **role:hetzner_vm**: Add new role
* **role:hostname**: Add new role
* **role:icinga2_agent**: Add new role
* **role:icinga2_master**: Add new role
* **role:icingaweb2**: Add new role
* **role:icingaweb2_module_company**: Add new role
* **role:icingaweb2_module_director**: Add new role
* **role:icingaweb2_module_doc**: Add new role
* **role:icingaweb2_module_grafana**: Add new role
* **role:icingaweb2_module_incubator**: Add new role
* **role:icingaweb2_module_monitoring**: Add new role
* **role:icingaweb2_module_vspheredb**: Add new role
* **role:influxdb**: Add new role
* **role:infomaniak_vm**: Add new role
* **role:kdump**: Add new role
* **role:keepalived**: Add new role
* **role:kernel_settings**: Add new role
* **role:keycloak**: Add new role
* **role:kvm_host**: Add new role
* **role:kvm_vm**: Add new role
* **role:libmaxminddb**: Add new role
* **role:librenms**: Add new role
* **role:libreoffice**: Add new role
* **role:login**: Add new role
* **role:mailto_root**: Add new role
* **role:mariadb_client**: Add new role
* **role:mariadb_server**: Add new role
* **role:maxmind_geoip**: Add new role
* **role:minio_client**: Add new role
* **role:mod_maxminddb**: Add new role
* **role:mongodb**: Add new role
* **role:motd**: Add new role
* **role:network**: Add new role; add functionality to configure network connections
* **role:nextcloud**: Add new role
* **role:nfs_client**: Add new role
* **role:nfs_server**: Add new role
* **role:nodejs**: Add new role
* **role:objectstore_backup**: Add new role
* **role:open_vm_tools**: Add new role
* **role:openssl**: Add new role
* **role:openvpn_server**: Add new role
* **role:perl**: Add new role
* **role:php**: Add new role
* **role:policycoreutils**: Add new role
* **role:postgresql_server**: Add new role
* **role:qemu_guest_agent**: Add new role
* **role:redis**: Add new role
* **role:repo_baseos**: Add new role
* **role:repo_collabora**: Add new role
* **role:repo_collabora_code**: Add new role
* **role:repo_debian_base**: Add new role
* **role:repo_docker**: Add new role
* **role:repo_elasticsearch_oss**: Add new role
* **role:repo_gitlab_ce**: Add new role
* **role:repo_grafana**: Add new role
* **role:repo_icinga**: Add new role
* **role:repo_influxdb**: Add new role
* **role:repo_mariadb**: Add new role
* **role:repo_mongodb**: Add new role
* **role:repo_monitoring_plugins**: Add new role
* **role:repo_mydumper**: Add new role
* **role:repo_postgresql**: Add new role
* **role:repo_remi**: Add new role
* **role:repo_sury**: Add new role
* **role:rocketchat**: Add new role
* **role:rsyslog**: Add new role
* **role:snmp**: Add new role
* **role:sshd**: Add new role
* **role:stig**: Add new role
* **role:system_update**: Add new role
* **role:systemd_journald**: Add new role
* **role:systemd_unit**: Add new role
* **role:tar**: Add new role
* **role:telegraf**: Add new role
* **role:timezone**: Add new role
* **role:unattended_upgrades**: Add new role
* **role:wordpress**: Add new role
* **role:yum_utils**: Add new role

### Changed

* **module_util:bitwarden**: Switch to the Bitwarden client API, as it is more reliable than using the command line tool directly
* **role:acme_sh**: Automatically update acme.sh ([fix #74](https://github.com/Linuxfabrik/lfops/issues/74))
* **role:apache_tomcat**: Use the correct Java version depending on Tomcat version ([fix #82](https://github.com/Linuxfabrik/lfops/issues/82))
* **role:duplicity**: Implement massive-parallel backups
* **role:hetzner_vm**: Improve handling of IP addresses (new Hetzner features) ([fix #72](https://github.com/Linuxfabrik/lfops/issues/72)); manage the provider firewall ([fix #71](https://github.com/Linuxfabrik/lfops/issues/71))
* **role:login**: Add a switch to be aggressive or not ([fix #65](https://github.com/Linuxfabrik/lfops/issues/65))
* **role:mariadb_server**: Implement mydumper / adapt to the LFOps standards ([fix #56](https://github.com/Linuxfabrik/lfops/issues/56))
* **role:mongodb**: Implement dumping / user management ([fix #78](https://github.com/Linuxfabrik/lfops/issues/78))
* **role:python**: On RHEL 8+, don't install `python3`. Instead install `python38` or `python39` explicitly ([fix #62](https://github.com/Linuxfabrik/lfops/issues/62))
* **role:tools**: Show distro in prompt ([fix #47](https://github.com/Linuxfabrik/lfops/issues/47))

### Fixed

* **role:audit**: Fix wrong README ([fix #51](https://github.com/Linuxfabrik/lfops/issues/51), [fix #58](https://github.com/Linuxfabrik/lfops/issues/58))
* **role:crypto_policy**: Fix wrong README ([fix #52](https://github.com/Linuxfabrik/lfops/issues/52), [fix #76](https://github.com/Linuxfabrik/lfops/issues/76))
* **role:icinga2_agent**: On Debian, user `nagios` does not exist when certs folder is created ([fix #77](https://github.com/Linuxfabrik/lfops/issues/77))
* **role:icinga2_master**: Fix missing option name in `icinga2_master/tasks/main.yml` ([fix #105](https://github.com/Linuxfabrik/lfops/issues/105))
* **role:monitoring_plugins**: Fix "deploy" vs "skip" logic ([fix #103](https://github.com/Linuxfabrik/lfops/issues/103))
* **role:repo_graylog**: Fix `repo_graylog__mirror_url` never actually being used ([fix #94](https://github.com/Linuxfabrik/lfops/issues/94))
* **role:sshd**: Fix `ModuleNotFoundError: No module named 'seobject'` ([fix #53](https://github.com/Linuxfabrik/lfops/issues/53))
* **playbook:basic_setup**: Fix `Failed to set locale, defaulting to C.UTF-8` ([fix #55](https://github.com/Linuxfabrik/lfops/issues/55))
* Do not use `become: true` in all playbooks ([fix #66](https://github.com/Linuxfabrik/lfops/issues/66))
* Deploy nft in basic-setup or the fwbuilder role ([fix #61](https://github.com/Linuxfabrik/lfops/issues/61))
* **role:freeipa_server**: Fix `In unattended mode you need to provide at least -r, -p and -a options` ([fix #83](https://github.com/Linuxfabrik/lfops/issues/83))


## [v1.0.1] - 2022-03-17

### Changed

* Adjust tags for Ansible Galaxy


## [v1.0.0] - 2022-03-17

### Added

* **role:duplicity**: Add new role
* **role:monitoring_plugins**: Add new role
* **role:python_venv**: Add new role
* **role:repo_epel**: Add new role
* **module:bitwarden_item**: Add new module
* **module:gpg_key**: Add new module
* **lookup_plugin:bitwarden**: Add new lookup plugin
* **module_util:bitwarden**: Add new module util
* **module_util:gnupg**: Add new module util


[Unreleased]: https://github.com/Linuxfabrik/lfops/compare/v5.1.0...HEAD
[v5.1.0]: https://github.com/Linuxfabrik/lfops/compare/v5.0.0...v5.1.0
[v5.0.0]: https://github.com/Linuxfabrik/lfops/compare/v4.0.0...v5.0.0
[v4.0.0]: https://github.com/Linuxfabrik/lfops/compare/v3.0.0...v4.0.0
[v3.0.0]: https://github.com/Linuxfabrik/lfops/compare/v2.0.1...v3.0.0
[v2.0.1]: https://github.com/Linuxfabrik/lfops/compare/v2.0.0...v2.0.1
[v2.0.0]: https://github.com/Linuxfabrik/lfops/compare/v1.0.1...v2.0.0
[v1.0.1]: https://github.com/Linuxfabrik/lfops/compare/v1.0.0...v1.0.1
[v1.0.0]: https://github.com/Linuxfabrik/lfops/releases/tag/v1.0.0
