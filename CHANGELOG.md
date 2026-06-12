# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Maintainer note:** Add new entries to the top of the matching subsection in the Unreleased section, even if this results in multiple entries for the same role. This way users only need to read the new entries at the top. Rules for the subsections:
> * Each subsection appears **at most once** per section. Never create a second `### Added`, `### Fixed`, etc. - append to the existing one.
> * Order the subsections as: `Breaking Changes`, `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`. This is the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) order, with the LFOps-specific `Breaking Changes` first. Omit subsections that have no entries.
> * Within a subsection, sort entries newest first (newest on top).


## [Unreleased]

### Breaking Changes

* **role:mariadb_server**: The default for `skip_name_resolve` is now `OFF` instead of `ON`. Hosts that relied on the previous default and grant access by hostname keep working, but connections are now resolved via DNS again. Set `mariadb_server__cnf_skip_name_resolve__group_var: 'ON'` (or the `__host_var`) to restore the previous behaviour.

### Added

* **role:glances**: Add RHEL 10 / Rocky 10 / Alma 10 support by installing glances into a Python venv via the `python_venv` role, since the package is not available in EPEL 10. RHEL 10 is now marked proven (`x`) in COMPATIBILITY.
* **role:graylog_datanode**: Add `graylog_datanode__http_publish_uri` to set the REST API URI the DataNode advertises, needed when the bind address is not directly reachable (multiple interfaces, a NAT gateway, or a `0.0.0.0` bind address).

### Changed

* **role:icingadb, role:icingaweb2, role:icingaweb2_module_reporting, role:icingaweb2_module_x509, role:mariadb_server**: Move the MariaDB tasks from the deprecated `community.mysql` collection to its replacement `ansible.mysql`. Behaviour is unchanged, but the deprecation warnings printed on every run are gone and the roles keep working once `community.mysql` is removed upstream.
* **role:apache_httpd**: Update the Matomo log-analytics import script (`import_logs.py`) to the latest upstream version. The auth token can now be provided via a `--auth-config` file instead of the command line (passing `--token-auth`, `--login` or `--password` as options is deprecated, since they are visible in the process list and now log a deprecation warning). Also adds support for the Traefik access-log format and fixes a possible endless loop when reading a config file.

### Fixed

* **role:kvm_vm**: Use `kvm_vm__connect_url` for every libvirt operation. Disk resizes (`virsh blockresize`) and a few other steps previously ignored the configured connection URL and always talked to the local default, so they failed or acted on the wrong libvirt when `kvm_vm__connect_url` pointed at a non-default or remote host.


## [v7.0.0] - 2026-06-11

### Breaking Changes

* **plugin:combine_lod, role:apache_httpd, role:mariadb_server, role:proxysql, role:selinux**: A composite `unique_key` (a list of keys) now requires every component to be set on each item, instead of letting one be filled by a downstream default. Set the previously optional component explicitly: `virtualhost_port` on every `apache_httpd` vHost, `host` on every `mariadb_server` user/role, `port` on every `proxysql` server, and `proto` on every `selinux` port. Otherwise the play fails with a clear error.
* **role:apache_httpd, role:apache_tomcat, role:mastodon, role:postgresql_server**: Rename tags to the project-wide naming scheme. `apache_httpd:config` becomes `apache_httpd:configure`, and `apache_tomcat:users`, `mastodon:users`, `postgresql_server:users` and `postgresql_server:databases` lose their trailing `s` (`...:user`, `...:database`). Adjust any `--tags` / `--skip-tags` invocations and automation that reference the old tag names.
* **role:sshd**: Ship hardened SSH defaults that change the behaviour of existing installations on the next run: X11 forwarding, agent forwarding and TCP keepalives are now off, `MaxAuthTries` is lowered to `3`, `ClientAliveCountMax` to `2`, and `LogLevel` is raised to `VERBOSE`. Sessions relying on X11 or agent forwarding stop working, and a client offering more than three keys from its SSH agent can be locked out. Restore the previous behaviour where needed via the new variables: `sshd__x11_forwarding: true`, `sshd__allow_agent_forwarding: true`, `sshd__tcp_keep_alive: true`, `sshd__max_auth_tries: 6`, `sshd__client_alive_count_max: 3`, `sshd__log_level: 'INFO'`. Additionally configurable are `sshd__allow_tcp_forwarding` and `sshd__max_sessions`.
* **role:apache_httpd, role:apache_solr, role:freeipa_server, role:grav, role:icingaweb2, role:influxdb, role:mariadb_server, role:mongodb, role:nextcloud, role:opensearch**: Align section tags to the controlled vocabulary, which uses plural names for sections that manage multiple objects. The `:user` tags become `:users`, the `:database` tags become `:databases`, and `apache_httpd:config` becomes `apache_httpd:configure`. Adjust any `--tags` / `--skip-tags` invocations and automation that reference the old tag names.
* **role:minio_client, role:objectstore_backup**: Both roles and their playbooks (`playbooks/minio_client.yml`, `playbooks/objectstore_backup.yml`) have been removed, along with the corresponding role blocks in `playbooks/setup_nextcloud.yml` and the `setup_nextcloud__skip_minio_client` / `setup_nextcloud__skip_objectstore_backup` variables. MinIO Server has been archived as no-longer-maintained since February 2026, and we are moving away from using object storage for critical data. Users relying on these roles must replace the MinIO-based object-store backup with their own solution (e.g. `rclone`); the `mc` binary, its config under `/etc/mc/`, the `objectstore-backup` systemd timer/service, and `/usr/local/bin/mc-mirror.sh` are no longer managed by lfops and will remain on existing hosts until removed manually ([#241](https://github.com/Linuxfabrik/lfops/issues/241)).
* **role:infomaniak_vm**: Always create a managed port for every entry in `infomaniak_vm__networks`, even when no `fixed_ip` is set. Previously only networks with a `fixed_ip` got a managed port; networks without one relied on OpenStack's auto-created port. To avoid creating unused (but billed) managed ports on VMs provisioned under the old behavior, make sure to manually rename the existing port in OpenStack to match the `port_name`. Note that this port will not survive VM deletion / detachment, since it was automatically created and therefore is owned by OpenStack, not the user.

### Added

* **testing**: Add a Molecule-based test framework that runs the playbooks (and through them the roles) against throwaway libvirt/KVM VMs or Podman containers. Scenarios live under `extensions/molecule`; see the Testing section in `CONTRIBUTING.md`.
* **role:icinga2_master, role:icingadb, role:icingaweb2, role:icingaweb2_module_reporting, role:icingaweb2_module_x509**: Add explicit Ubuntu variable files, making Ubuntu support visible alongside Debian. The Icinga repository, GPG key and package names were verified on Debian 13 and Ubuntu 24.04.
* **role:nextcloud**: Add `meta/argument_specs.yml` declaring the user-facing variables, so role-entry validation catches type mismatches and missing mandatory variables.
* **role:clamav**: Add `meta/argument_specs.yml` declaring the user-facing variables, so role-entry validation catches type mismatches and unknown variables.
* **role:core_dumps**: New role that disables core dumps (which can leak sensitive process memory to disk) following the CIS Benchmark recommendations. Runs as part of `setup_basic`.
* **role:login**: Sets a password-aging policy and a stricter default umask in `/etc/login.defs` (configurable). Applies to newly created accounts and password changes, not retroactively to existing accounts.
* **role:kernel_modules**: New role that hardens a host by blocking rarely used or risky kernel modules (FireWire, legacy filesystems, uncommon network protocols) following the CIS Benchmark recommendations. Runs as part of `setup_basic`. The defaults stay clear of modules that would break common workloads (containers, snap, USB storage); those can be blocked explicitly where wanted.
* **role:sshd**: Add Ubuntu 22.04 / 24.04 / 26.04 support and run on Fedora. On Debian and Ubuntu the role now manages the correct service unit (`ssh.service`) and disables OpenSSH socket activation (`ssh.socket`) so the daemon is managed consistently across distributions. Red Hat-family releases without a version-specific template (in particular Fedora) now fall back to a generic `RedHat` `sshd_config` template instead of failing.
* **role:hostname**: Maintains an `/etc/hosts` entry mapping the FQDN (and short name) to the host's primary IPv4 address for proper local name resolution. The IP is configurable via `hostname__etc_hosts_ip`, and the whole behaviour can be disabled with `hostname__manage_etc_hosts: false`.
* **role:tmux**: Installs tmux and deploys a system-wide `/etc/tmux.conf` with sensible defaults, such as a larger scrollback buffer and mouse support. Selections are copied to the local clipboard over SSH via OSC 52 (where the terminal emulator supports it), and `prefix + P` dumps a pane's whole scrollback buffer to a file.
* **role:graylog_server**: Make more HTTP, Elasticsearch, processing/output buffer and message journal settings configurable via `graylog_server__http_external_uri`, `graylog_server__http_enable_cors`, `graylog_server__elasticsearch_max_total_connections`, `graylog_server__elasticsearch_max_total_connections_per_route`, `graylog_server__output_batch_size`, `graylog_server__processbuffer_processors`, `graylog_server__outputbuffer_processors`, `graylog_server__ring_size`, `graylog_server__inputbuffer_ring_size`, `graylog_server__message_journal_max_age` and `graylog_server__message_journal_max_size`.
* **role:mariadb_server**: Make `aria_pagecache_buffer_size`, `key_buffer_size` and `sort_buffer_size` configurable via the corresponding `mariadb_server__cnf_*` variables.
* **plugin:platform_select**: New filter plugin for selecting a value from a platform-keyed dictionary by OS family / distribution / version.
* **role:alternatives**: Support managing `subcommands` (slaves/followers) and the Red Hat-only `family` grouping. The role now also ensures the alternatives tooling is installed (`chkconfig` on RHEL 8, `alternatives` on RHEL 9/10; bundled with `dpkg` on Debian/Ubuntu), and can be included without variables as a no-op.
* **role:redis**: Add template for version 8.8
* **role:system_update**: Add a security lane for Rocky Linux. A second timer (twice a day by default) installs only Rocky Linux security hot-fixes from the dedicated `security` repository (provided by `repo_baseos`) and reboots the host if needed. The reboot time is steered per host group (for example immediately on test hosts, deferred to the evening on production hosts). Enabled by default; a no-op where the `security` repository is not enabled, and can be turned off with `system_update__security_enabled: false`. This keeps critical security fixes flowing daily while the regular update lane stays on its weekly schedule.
* **role:mariadb_server**: Add `mariadb_server__cnf_innodb_snapshot_isolation` variable (MariaDB 10.6+), defaulting to `'ON'`.
* **role:repo_baseos**: Add the Rocky Linux `security` repository (critical CVE fixes), enabled by default. Opt out per host or group via `repo_baseos__security_repo_enabled__host_var` / `repo_baseos__security_repo_enabled__group_var`.
* **role:chromium_headless**: New role. Provides a hardened, socket-activated headless Chromium backend (started on the first request, stopped again after an idle timeout, so it uses no RAM while unused) for tools such as the Icinga Web 2 PDF Export Module. Installs `chromium-headless` from EPEL instead of Google's proprietary repository.
* **role:graylog_datanode, role:graylog_server**: Add template for Graylog 7.1.
* **role:sshd**: Add Debian 13 support.
* **role:mirror**: Document the new per-repository `newest_only` subkey on `mirror__reposync_repos` entries. Defaults to `true` (only the newest version of each package is mirrored). Set to `false` for repositories that publish multiple versions in parallel, such as Icinga, where older versions must remain available.
* **role:repo_remi**: Add RHEL 10 / Rocky 10 support (new GPG key, repo templates, and module-stream tasks for EL 10).
* **role:repo_remi**: Add `meta/argument_specs.yml` declaring the four user-facing variables (`repo_remi__basic_auth_login`, `repo_remi__enabled_php_version`, `repo_remi__enabled_redis_version`, `repo_remi__mirror_url`) so role-entry validation catches type mismatches and unknown variables. `repo_remi__basic_auth_login` is declared as `type: 'raw'` because its default in `defaults/main.yml` resolves to an empty string when no Bitwarden lookup is configured.
* **role:monitoring_plugins, role:repo_monitoring_plugins**: Add SLES 15 and SLES 16 support. The roles now install the Linuxfabrik Monitoring Plugins from the SUSE channel of `repo.linuxfabrik.ch` and apply the SUSE-specific package version lock ([#245](https://github.com/Linuxfabrik/lfops/issues/245)).
* **role:alternatives, role:elastic_agent, role:elastic_agent_fleet_server, role:icinga_kubernetes_web, role:lvm, role:mailto_root, role:motd, role:proxysql**: (Re-)introduce `meta/argument_specs.yml` so role-entry validation catches type mismatches and missing required variables. The originally proposed specs were correct for these roles (no strict-options login dicts, no `__dependent_var` injections from `setup_*` playbooks), so they are restored unchanged.
* **role:apps, role:example, role:kernel_settings**: (Re-)introduce `meta/argument_specs.yml`, with the `__dependent_var` slot declared so `setup_*` playbooks that inject these via `vars:` (e.g. `setup_icinga2_master`, `setup_moodle`, `setup_nextcloud`) pass validation.
* **role:freeipa_client, role:grafana_grizzly, role:icingaweb2_module_reporting, role:mastodon**: (Re-)introduce `meta/argument_specs.yml` for the login dicts, declared as plain `type: 'dict'` (no strict sub-options), so they can be fed directly from `linuxfabrik.lfops.bitwarden_item` (which returns the full Bitwarden item with extra keys like `id`, `notes`, `fields`).
* **role:repo_monitoring_plugins**: Add optional variable `repo_monitoring_plugins__testing` (default `false`) to switch from the `release` channel to the `testing` channel. On Red Hat-family systems, a single `/etc/yum.repos.d/linuxfabrik-monitoring-plugins.repo` is now deployed (replacing the previous `linuxfabrik-monitoring-plugins-release.repo`, which is removed on upgrade) containing both the `[linuxfabrik-monitoring-plugins-release]` and `[linuxfabrik-monitoring-plugins-testing]` sections, with `enabled=` toggled by the variable so DNF metadata for both channels can stay cached across switches. On Debian/Ubuntu, the `-release` suffix in the apt sources file is replaced with `-testing` accordingly.
* **playbooks/setup_basic**: Add `setup_basic__skip_policycoreutils` to skip the `policycoreutils` role, matching the pattern used by the other roles in the playbook.
* **role:uptimerobot, plugins/modules/uptimerobot_***: New role and a set of nine custom modules to manage UptimeRobot resources directly from a playbook. CRUD modules: `uptimerobot_monitor`, `uptimerobot_mwindow`, `uptimerobot_psp`, plus `uptimerobot_alert_contact` (delete only — UptimeRobot API v2 does not expose creating contacts). Read-only info modules for inspection and dynamic inventories: `uptimerobot_account_info`, `uptimerobot_monitor_info`, `uptimerobot_mwindow_info`, `uptimerobot_alert_contact_info`, `uptimerobot_psp_info`. All CRUD modules support `--check` and `--diff`, are idempotent on re-run, and translate API integer IDs to user-facing labels in both directions. Configuration is done via four inventory lists (`uptimerobot__monitors`, `uptimerobot__mwindows`, `uptimerobot__psps`, `uptimerobot__alert_contacts`). API key resolution: `api_key` parameter, `api_key_file` (default `~/.uptimerobot`), or `UPTIMEROBOT_API_KEY` environment variable.
* **role:at**: Add optional variable `at__service_state` (`reloaded` / `restarted` / `started` / `stopped`) to control the running state of `atd.service` independently from boot autostart. Default behaviour is unchanged: `at__service_enabled: true` keeps the service started, `false` stops it.
* **role:dnf_makecache**: Add optional variables `dnf_makecache__service_state` and `dnf_makecache__timer_state` to control the running state of `dnf-makecache.service` and `dnf-makecache.timer` independently from boot autostart. Default behaviour is unchanged.
* **role:open_vm_tools**: Add optional variables `open_vm_tools__service_enabled` and `open_vm_tools__service_state`. The role previously had no way to disable / stop `vmtoolsd.service`; now the service can be managed like in the other LFOps service-wrapper roles. Default behaviour is unchanged (service enabled and started).
* **role:qemu_guest_agent**: Add optional variable `qemu_guest_agent__service_state` (`reloaded` / `restarted` / `started` / `stopped`) to control the running state of `qemu-guest-agent.service` independently from boot autostart. Default behaviour is unchanged: `qemu_guest_agent__service_enabled: true` keeps the service started, `false` stops it.
* **role:libmaxminddb**: Now runs on Debian and Ubuntu in addition to Red Hat-family systems.
* **role:mod_maxminddb**: Now runs on Debian and Ubuntu in addition to Red Hat-family systems. The Apache module is enabled automatically on Debian/Ubuntu (no manual `a2enmod` needed).
* **role:logstash**: Add optional variables `logstash__monitoring_cluster_uuid`, `logstash__monitoring_enabled`.
* **role:elasticsearch**: Add optional variables `elasticsearch__cluster_routing_allocation_disk_watermark_flood_stage_frozen_max_headroom`, `elasticsearch__cluster_routing_allocation_disk_watermark_flood_stage_max_headroom`, `elasticsearch__cluster_routing_allocation_disk_watermark_high_max_headroom`, `elasticsearch__cluster_routing_allocation_disk_watermark_low_max_headroom`.
* **role:elasticsearch**: Add optional variable `elasticsearch__cluster_routing_allocation_disk_watermark_flood_stage_frozen`.
* **role:graylog_datanode**: Add optional variable `graylog_datanode__raw`.
* **role:graylog_datanode**: Add optional variables `graylog_datanode__path_repos`, `graylog_datanode__node_search_cache_size` to configure searchable snapshot locations and size of disk-based searchable snapshot cache.
* **role:infomaniak_vm**: Add `keep_port_on_absent` subkey on `infomaniak_vm__networks` entries to preserve the port (and its fixed IP) when the VM is set to `infomaniak_vm__state: 'absent'`, so the same IP can be re-used
* **role:infomaniak_vm**: Add `port_name` subkey on `infomaniak_vm__networks` entries to override the name of the managed port. Defaults to the previous `{{ infomaniak_vm__name }}--{{ item["name"] }}--port` pattern, so existing setups are unaffected
* **role:kibana**: Add `kibana__logging` variable to make the `logging:` block in `kibana.yml` fully user-configurable (appenders, loggers, root, rotation). The default preserves the previous hardcoded behavior: JSON logs at `/var/log/kibana/kibana.log`, rotated daily, 14 rotations kept
* **ci**: Add bandit (security) and vulture (dead code) to pre-commit hooks

### Changed

* **role:icinga2_master, role:icingadb**: Validate the Icinga 2 configuration before restarting the service. A faulty config now fails the playbook run loudly instead of bouncing the daemon into a broken state and leaving Icinga 2 down.
* **role:nextcloud**: Automatic app updates are now enabled by default (`nextcloud__timer_app_update_enabled`). The scheduled app update only switches Nextcloud into maintenance mode when an app update is actually pending, so an instance that is already up to date keeps serving requests without interruption. After updating, the recommended database migrations are applied automatically. A failed run no longer leaves the instance stuck in maintenance mode.
* **role:clamav**: Now runs on Debian and Ubuntu in addition to Red Hat-family systems, and works on RHEL 10. The role seeds the signature database on first install so the scanner starts reliably, and runs an EICAR self-test (also available on its own via the `clamav:test` tag) that confirms detection actually works.
* **role:acme_sh**: Issue ECDSA P-256 certificates by default instead of RSA-4096, for faster TLS handshakes at equivalent security. Certificates previously issued as RSA are reissued as ECDSA on the next run, and the superseded RSA certificate is dropped from renewal. Set `acme_sh__key_length` to an RSA value such as `4096` to keep RSA.
* **playbooks**: Enable the CRB repository on Rocky 10 too, not just Rocky 9. Previously Rocky 10 hosts silently skipped this step, which could leave dependencies such as `python3-virtualenv` uninstallable.
* **role:grafana**: Apply the systemd/chkconfig workaround on RHEL 10 as well, not just RHEL 9.
* **role:tools**: Install the German locale package (`glibc-langpack-de`) on RHEL 10 as well.
* **playbooks**: Roles that target the whole RHEL family now run on any enterprise distribution that is not Fedora, instead of an explicit list of major versions. This adds support for RHEL 10 and future releases without further changes, while Fedora stays excluded as before.
* **role:tools**: No longer installs tmux. Use the dedicated `tmux` role instead, which also ships a configuration with sensible defaults.
* **roles:mariadb_server, icingaweb2, icingaweb2_module_x509, duplicity, php, crypto_policy**: Internal refactor of OS-keyed default lookups. Behavior is unchanged on supported platforms. The internal package-selection dicts in `mariadb_server`, `icingaweb2`, `icingaweb2_module_x509` and `duplicity` are no longer overridable from inventory; they were never meant to be.
* **role:shared**: The Apache httpd user/group (`apache` on RedHat, `www-data` on Debian, `wwwrun`/`www` on Suse) is now defined once in the `shared` role as `__shared__apache_httpd_user` / `__shared__apache_httpd_group` and loaded into every playbook through a new `global-variables.yml` task in `pre_tasks`, instead of being repeated in the `vars/` of around 20 roles. The affected roles now expect this `pre_tasks` import to run, so running them ad-hoc outside the bundled playbooks requires importing `shared`'s `global-variables.yml` first. On Suse, the `monitoring_plugins` web files now use the correct apache group `www` instead of `wwwrun` (on RedHat and Debian the user and group are identical, so file ownership there is unchanged).
* **role:repo_baseos**: The Rocky 8 `security` repository now matches Rocky 9/10: it adds the `security-debuginfo` and `security-source` sub-repositories (disabled), a 6-hour metadata expiry so emergency hot-fixes are noticed quickly, and the `$rltype` mirrorlist variable.
* **plugin:gpg_key**: Refresh the bundled GPG helper library so the module keeps working on current Python and GnuPG releases. Existing playbooks are unaffected. The `gnupghome` parameter now expands `~` and resolves relative paths, matching its documentation.
* **docs**: All role READMEs now follow a consistent structure that separates the dependencies a playbook sets up for you from what you must provide yourself. Documentation only, no behavior changes.
* **role:keycloak**: The role no longer leaves the bootstrap admin credentials lying around in `/etc/sysconfig/keycloak` after the first run. It now writes the credentials, waits for Keycloak to consume them on startup (provisioning the bootstrap admin in the `master` realm), re-renders the sysconfig file with the credentials removed, and stores a state marker at `/etc/ansible/facts.d/keycloak__admin_login_bootstrapped.state` so subsequent runs skip the credential render entirely. After the first run, `keycloak__admin_login` can be removed from the inventory. Disaster recovery: delete the marker file, re-add the variable, re-run. Also recommend a `-temp` suffix for the initial admin username (example: `keycloak-admin-temp`) so it is visually obvious in the Keycloak UI which account must be deleted once a permanent admin exists.
* **role:redis**: Bump default for `net.core.somaxconn` from `1024` to `4096` to match the RHEL 9 / RHEL 10 kernel default and the current Redis upstream recommendation. Hosts on RHEL 9 or 10 see no effective change (the override was already below the kernel default); RHEL 8 hosts now get `4096` instead of `1024`.
* **role:monitoring_plugins**: `install_method: 'source'` now reads the per-Python-LTS lockfile under `lockfiles/pyXX/requirements.txt` (`py39` ... `py314`) from both the `monitoring-plugins` and `lib` repos, picking the directory that matches the target host's Python. The previous root-level `requirements.txt` no longer exists upstream. No variable changes; rsync sources updated.
* **CONTRIBUTING**: `meta/argument_specs.yml` must declare the `__dependent_var` slot for any variable that `setup_*` playbooks inject into the role via `vars:`. Dict variables fed by external lookups like `linuxfabrik.lfops.bitwarden_item` should use `type: 'dict'` without strict sub-options, since the lookup returns the full item with additional keys.
* **role:example**: Demonstrate the `delegate_to: 'localhost'` + `become: false` pattern (download on the controller, copy to the target) so role authors can copy it consistently.
* **role:apache_httpd**: bump Core Rule Set to 4.27.0
* **role:apache_httpd**: Update the two reverse-proxy snippets in `EXAMPLES.md` to use `ProxyPass` instead of `RewriteRule ^/(.*) ... [proxy,last]`. The RewriteRule variant `%`-decodes the URI pattern and forwards characters such as `?` unencoded to the backend, which breaks WebDAV apps (file-not-found on rename in Nextcloud). The examples now also carry a comment explaining the choice and link to the corresponding [blog post](https://www.linuxfabrik.ch/blog/nextcloud-rewriterules-vs-proxypass).
* **role:motd**: Updated default value of `motd__legal_notice`.
* **role:dnf_versionlock**: Rename internal OS-specific variables `dnf_versionlock__list_path` and `dnf_versionlock__packages` to `__dnf_versionlock__list_path` and `__dnf_versionlock__packages`. They are set in `vars/RedHat{7,8,9}.yml` and `vars/Fedora{40,41}.yml` and were never meant to be overridden from inventory; the `__` prefix makes that visible (LFOps convention). If you set either of these in your inventory, switch to the new names.
* **role:icingaweb2_module_businessprocess**: Rename internal variable `icingaweb2_module_businessprocess__icingaweb2_owner` (set in `vars/{Debian,RedHat}.yml`) to `__icingaweb2_module_businessprocess__icingaweb2_owner`. Inventory overrides need to be renamed; the value (`www-data` on Debian, `apache` on Red Hat) stays the same.
* **role:icingaweb2_module_company**: Rename internal variable `icingaweb2_module_company__icingaweb2_owner` (set in `vars/{Debian,RedHat}.yml`) to `__icingaweb2_module_company__icingaweb2_owner`. Inventory overrides need to be renamed; the value (`www-data` on Debian, `apache` on Red Hat) stays the same.
* **role:icingaweb2_module_cube**: Rename internal variable `icingaweb2_module_cube__icingaweb2_owner` to `__icingaweb2_module_cube__icingaweb2_owner`. See `roles/icingaweb2_module_businessprocess` above.
* **role:icingaweb2_module_fileshipper**: Rename internal variable `icingaweb2_module_fileshipper__icingaweb2_owner` to `__icingaweb2_module_fileshipper__icingaweb2_owner`. See `roles/icingaweb2_module_businessprocess` above.
* **role:icingaweb2_module_generictts**: Rename internal variable `icingaweb2_module_generictts__icingaweb2_owner` to `__icingaweb2_module_generictts__icingaweb2_owner`. See `roles/icingaweb2_module_businessprocess` above.
* **role:icingaweb2_module_incubator**: Rename internal variable `icingaweb2_module_incubator__icingaweb2_owner` to `__icingaweb2_module_incubator__icingaweb2_owner`. See `roles/icingaweb2_module_company` above.
* **role:icingaweb2_module_pdfexport**: Rename internal variable `icingaweb2_module_pdfexport__icingaweb2_owner` to `__icingaweb2_module_pdfexport__icingaweb2_owner`. See `roles/icingaweb2_module_company` above.
* **role:icingaweb2_theme_linuxfabrik**: Rename internal variable `icingaweb2_theme_linuxfabrik__icingaweb2_owner` to `__icingaweb2_theme_linuxfabrik__icingaweb2_owner`. See `roles/icingaweb2_module_company` above.
* **role:freeipa_client**: Add `meta/argument_specs.yml`. No behaviour change.
* **role:haveged, role:libmaxminddb, role:qemu_guest_agent**: README now also explains *what* the underlying tool actually does and when you'd want it (entropy daemon, MaxMind GeoIP reader library, hypervisor-to-guest communication channel) instead of just linking out.
* **roles**: README intros across 19 roles (`ansible_init`, `cockpit`, `collect_rpmnew_rpmsave`, `crypto_policy`, `hostname`, `kdump`, `repo_collabora`, `repo_docker`, `repo_gitlab_ce`, `repo_gitlab_runner`, `repo_grafana`, `repo_influxdb`, `repo_mongodb`, `repo_redis`, `selinux`, `snmp`, `sshd`, `timezone`, `unattended_upgrades`) now explain in one or two sentences what the underlying software actually is and when an admin would use it, instead of just naming it.
* **COMPATIBILITY**: Promote the RHEL 10 column from `(x)` (or empty) to `x` (proven) for the 23 roles exercised by `setup_basic` and validated on a RHEL 10 host: `at`, `cloud_init`, `cockpit`, `dnf_makecache`, `hostname`, `icinga2_agent`, `kdump`, `login`, `lvm`, `mailto_root`, `monitoring_plugins`, `motd`, `network`, `python`, `python_venv`, `repo_icinga`, `repo_monitoring_plugins`, `rsyslog`, `selinux`, `system_update`, `systemd_journald`, `timezone`, `tools`. `glances` stays at `(x)` because the package is missing in EPEL 10 (see the role README).
* **COMPATIBILITY**: `at`, `haveged`, `mod_maxminddb` and `qemu_guest_agent` are now expected to work on Debian 12 / 13 and Ubuntu 22.04 / 24.04 / 26.04 (marked `(x)`: code-reviewed, untested in production).
* **role:hostname, role:kdump, role:timezone**: Add `meta/argument_specs.yml` so Ansible validates the role variables (types, choices) at role entry. No behaviour change.
* **role:libmaxminddb, role:mod_maxminddb**: Add `meta/argument_specs.yml`. No behaviour change.
* **role:network**: Scope the `hc-utils` removal task to Red Hat-family hosts (`when: ansible_facts["os_family"] == "RedHat"`). Hetzner ships `hc-utils` as RPMs only, so on Debian / Ubuntu the call was a no-op caught by `ignore_errors: true`. No behaviour change on either family.
* **role:icingaweb2_module_businessprocess**: README now documents the install behaviour (controller-side download, every-run-overwrite, idempotent module enable). Add `meta/argument_specs.yml`.
* **role:icingaweb2_module_cube**: README now documents the install behaviour. Add `meta/argument_specs.yml`.
* **role:icingaweb2_module_fileshipper**: README now documents the install behaviour and the `php-xml`/`php-yaml`/`php-zip` runtime dependency. Add `meta/argument_specs.yml`.
* **role:icingaweb2_module_generictts**: README now documents the install behaviour. Add `meta/argument_specs.yml`.
* **role:apps**: Document that the role uses `ansible.builtin.package` internally, so `state: 'latest'` works on backends that support it.
* **role:cloud_init**: README now lists all cleanup actions (`cloud-init` package removal, `/etc/NetworkManager/conf.d/99-cloud-init.conf`, `/etc/cloud/cloud.cfg.rpmsave`).
* **role:dnf_versionlock**: README explains the RHEL 7 vs RHEL 8+ backend differences (`yum-plugin-versionlock` vs `dnf-command(versionlock)` and the corresponding lock-list paths).
* **role:glances**: Document the optional `glances__skip_repo_baseos` variable (skip the implicit `repo_baseos` invocation on Rocky 9) and the implicit `repo_epel` / `repo_baseos` dependencies. Note in the Mandatory Requirements section that the role currently fails on RHEL 10 / Rocky 10 / Alma 10 because `glances` is not packaged in EPEL 10.
* **role:icingaweb2_module_company**: Document the install-once idempotency (module is installed on first run only; subsequent runs do not overwrite local customizations) and the controller-side download mechanism.
* **role:icingaweb2_module_incubator**: Document the controller-side download mechanism and that the directory is overwritten on every run, so changing `icingaweb2_module_incubator__version` is the supported upgrade path.
* **role:icingaweb2_module_pdfexport**: Document the controller-side download mechanism and the upgrade-on-rerun behaviour. Add a pointer that runtime dependencies (e.g. a headless browser) have to be installed separately.
* **role:icingaweb2_theme_linuxfabrik**: README clarifies that the role is pulled in via `setup_icinga2_master` (there is no dedicated playbook) and documents the upgrade-on-rerun behaviour.
* **role:libreoffice**: Document the full effect of `libreoffice__client_apache: true` (directory layout, one-shot dummy conversion, two custom SELinux policy modules, plus SELinux booleans/fcontexts via the companion playbook). Note that this option is Red Hat-only.
* **role:maxmind_geoip**: Document the optional `maxmind_geoip__skip_systemd_unit` variable and how to override the `OnCalendar=weekly` schedule via `maxmind_geoip__systemd_unit__timers__dependent_var`. Mention that the timer is what triggers the first download (so initial population requires a manual `systemctl start update-maxmind.service` if you don't want to wait for the next weekly fire).
* **role:nodejs**: Document the `/bin/nodejs -> /bin/node` compatibility symlink, clarify that `nodejs__dnf_module_stream` is Red Hat-family only and accepts the stream as Number or String.
* **role:open_vm_tools**: Document that the role targets VMware-virtualized guests and that, unlike `qemu_guest_agent` / `haveged`, no `__service_enabled` variable is exposed.
* **role:repo_debian_base**: Document the supported Debian versions (10, 11, 12), the Debian-only scope, and the post-deploy `rpmnew` / `dpkg-dist` / `ucf-dist` cleanup.
* **role:shared**: Document all `tasks_from:` helpers (`log-start`, `log-end`, `platform-variables`, `clone-lib-repo`, `clone-monitoring-plugins-repo`, `remove-rpmnew-rpmsave`) with their required parameters and side effects.
* **role:system_update**: Change default of `system_update__update_time` from `'04:00 + 1 days'` to `'04:{{ 59 | random(seed=inventory_hostname) }} + 1 days'`, so updates are spread deterministically across 04:00–04:59 (minute derived from `inventory_hostname`) instead of all hosts firing at 04:00 sharp
* **role:firewall**: Install `nftables` together with `iptables` for `firewall__firewall == "fwbuilder"` on all distros (previously only installed via per-distro task files on Fedora and RHEL 8/9). The redundant `tasks/Fedora.yml`, `tasks/RedHat8.yml` and `tasks/RedHat9.yml` were removed.
* **role:graylog_server**: Update `server.conf` templates to include `telemetry_enabled = false`.
* **role:keepalived**: Document role scope in the README. The role intentionally covers only a minimal VRRP setup (single `vrrp_instance`, single `virtual_ipaddress`, PASS auth, `smtp_alert`). It does not set the `net.ipv4.ip_nonlocal_bind` sysctl and does not open the firewall for VRRP; pointers to the `kernel_settings` and `firewall` roles are included
* **all roles**: Rewrite all role READMEs to use the new standard format: replace markdown tables with bullet lists for tags and variables, convert HTML/blockquote subkeys to expanded indented format, standardize terminology (`Bool` not `Boolean`, `Mandatory` not `Required`)
* **role:opensearch**: Rewrite README with step-by-step cluster setup guide, single-node section, post-installation steps, and improved variable documentation
* **role:elasticsearch**: Improve README with single-node section and clearer explanation of the manual certificate approach for cluster setup
* **COMPATIBILITY**: Add Ubuntu 26.04 column
* **COMPATIBILITY**: Mark OSes a role is theoretically usable on (but untested) with `(x)`. Inferred from per-role static analysis (OS-specific task/vars files, modules used, hardcoded paths and services)
* **COMPATIBILITY**: Add missing `crypto_policy` RHEL 10 entry
* **COMPATIBILITY**: Remove Debian 11 and Ubuntu 20.04 columns (EOL)

### Removed

* **role:repo_remi**: Drop support for RHEL 7 and Fedora 35. Both are EOL (RHEL 7: June 2024, Fedora 35: December 2022). The per-platform `tasks/RedHat7.yml`, `vars/{RedHat7,Fedora}.yml` and `templates/{RedHat7,Fedora}/` trees are removed.
* **tool:particle**: Remove the `tools/particle` Vagrant-based role test runner, its leftover `particle/Vagrantfile`, its sample inventories under `tests/`, and the bundled `linuxfabrik/lib` git submodule (whose only consumer was `particle`). The runner and the submodule were tightly wired together, and Dependabot did not have a `gitsubmodule` config for this repo, so the bundled lib was silently drifting behind upstream. Since role testing is moving to Molecule anyway, dropping the whole stack is cleaner than keeping the wiring around. Older revisions remain accessible through git history.
* **role:freeipa_client**: Remove the dead-code defaults `freeipa_server__config_default_shell`, `freeipa_server__config_password_expiration_notification`, `freeipa_server__domain` and `freeipa_server__realm` from `defaults/main.yml`. They were never read by the role (these settings live in `freeipa_server` and are read from the `freeipa_server` role's defaults).

### Fixed

* **role:repo_elasticsearch, role:repo_grafana, role:repo_graylog, role:repo_icinga, role:repo_influxdb, role:repo_mariadb, role:repo_mongodb, role:repo_monitoring_plugins, role:repo_mydumper, role:repo_opensearch, role:repo_proxysql, role:repo_redis, role:repo_sury**: Refreshing the apt cache is no longer reported as a change on every run.
* **role:repo_remi**: Enabling the php, composer and Redis module streams is now idempotent. Repeated runs no longer report a change or briefly disable and re-enable the stream on every run.
* **role:proxysql**: `mysql_servers` entries are now deduplicated by their actual `address` field. The merge key referenced a non-existent `hostname` field, so multiple backends sharing a host group and port were silently collapsed into one.
* **role:repo_influxdb**: prevent the `influxdata-archive-keyring` package from being installed on both Enterprise Linux and Debian, as it would drop a second repo file pointing at upstream that is not managed by LFOps.
* **role:php**: php-fpm workers now run with a defined `PATH`. Previously the worker environment was cleared, leaving `getenv("PATH")` empty, which broke PHP code that shells out to system binaries and tripped Nextcloud's "PHP getenv" setup warning.
* **role:redis**: The Redis configuration file is no longer world-readable. It is now deployed as `root:redis` with mode `0640`, so its contents (e.g. a configured password) can no longer be read by other local users.
* **role:acme_sh**: No longer reinstalls every certificate and reloads the web server on every run. Certificates are only reinstalled when they were just (re)issued or when the installed file is missing, so repeated runs are idempotent.
* **role:keycloak**: Role now prints a clear instruction when a re-run can no longer obtain a token because the bootstrap admin was manually switched over to a permanent account (temporary `-temp` user deleted) and the bootstrap marker went missing.
* **roles**: Controller-side downloads and git clones (those delegated to localhost) are no longer skipped when the first targeted host happens not to need them. Running a role against multiple hosts previously risked leaving later hosts without the downloaded artifact. Such steps now also run safely when the playbook targets many hosts in parallel.
* **role:mongodb**: Managing MongoDB users (admin, regular or dump user) requires `mongodb__conf_security_authorization` to be enabled, since the role authenticates as the admin user, which only exists with authorization on. Previously, defining a dump user with authorization disabled caused a confusing authentication failure. The role now aborts early with a clear message when users are defined while authorization is disabled, and the dump config no longer writes login credentials in that case.
* **plugin:gpg_key**: Corrected the module documentation. The GPG helper library ships with the collection, so no separate `python-gnupg` install is required, and the returned key field is documented as `uids` (matching the actual output).
* **plugin:nextcloud_occ_app_config**: An `array` config value is now compared as JSON, so a key whose stored value already matches the desired one no longer reports a change (and re-runs `occ config:app:set`) on every run.
* **plugin:bitwarden_item**: The module no longer writes to the Bitwarden vault when run in check mode (`--check`); it reports the would-be change instead.
* **plugin:bitwarden_item**: A run without `password` (the default `None`) no longer overwrites an existing item's password; the current password is preserved, matching the documented behavior.
* **plugin:sqlite_query**: A failed query now fails the task instead of reporting success with the error text in `query_result`. Playbooks that relied on the previous silent success will now correctly fail.
* **plugin:sqlite_query**: A `REGEXP` query against a column that contains NULL values no longer fails; a NULL value simply does not match.
* **plugin:uptimerobot_\***: The modules no longer crash when the UptimeRobot API returns a non-list response for a list endpoint; the response is passed through instead.
* **plugin:nextcloud_occ_app_config, plugin:nextcloud_occ_system_config, plugin:uptimerobot_monitor, plugin:uptimerobot_psp**: Fixed their documentation so `ansible-doc` renders them again. A unit-test guard now catches this class of error for every in-house plugin.
* **plugin:bitwarden_item**: Fixed the lookup's documentation so `ansible-doc` renders it again.
* **plugin:combine_lod**: Fixed its documentation so `ansible-doc` renders it again.
* **role:kernel_settings**: The `systemd_cpu_affinity` setting is now actually applied. The value was computed and shown in the debug output but never passed to the underlying system role, so a configured CPU affinity had no effect.
* **role:inflxudb**: Always install `curl`, which is required to start influxdb but missing as a package dependency.
* **role:redis**: Added missing paths for running against Debian.
* **role:icingaweb2_module_pdfexport**: PDF export now works out of the box. The headless browser backend the module needs is installed and configured automatically via the new `chromium_headless` role (wired into the `icingaweb2_module_pdfexport` and `setup_icinga2_master` playbooks); previously it had to be set up by hand, so fresh deployments ended up without working PDF export.
* **role:graylog_datanode**: Fix the `Conditional result ... was of type 'str'` deprecation warning.
* **role:graylog_server**: Validate that each `graylog_server__system_inputs` entry sets `global: true` or assigns a `node`. Key was marked as mandatory but not enforced. The role now aborts the `graylog_server:configure_defaults` run with a clear message.
* **role:graylog_server**: Fix the `graylog_server:configure_defaults` run aborting on Graylog 7.0+ with `Status code was 400 and not [200]` / `Unable to map property can_be_default` while creating the default index set, by removing the property from the role. Graylog 7.x dropped it and 6.x ignored it.
* **role:keycloak**: Fix ownership under `/opt/keycloak/data/`. Previously the post-install build step ran as `root` and left `/opt/keycloak/data/` and `/opt/keycloak/data/tmp/` owned by `root:root`, which the `keycloak` service user could not write into (no `data/cache/` was ever created). The build now runs as the `keycloak` service user, and existing installations get the ownership corrected on the next role run.
* **role:nodejs**: Fix `@nodejs:<stream>` install failing with `broken groups or modules: nodejs:<stream>`. Two issues compounded: DNF refuses to silently switch an already-enabled module stream, and some modules ship without a `[d]efault` profile, so `@nodejs:<stream>` (no profile specified) cannot be resolved. The role now runs `dnf -y module reset nodejs` first when `nodejs__dnf_module_stream` is set, and installs the explicit `/common` profile.
* **role:blocky**: The handler `blocky: validate config & restart blocky.service` is now notified if the blocky binary is changed on the host to ensure that the blocky service is restarted after an update (as it was already documented for the `blocky` tag)
* **role:nextcloud**: The `nextcloud-update` script now owns the maintenance mode lifecycle itself instead of expecting callers to enable it beforehand. Previously, callers enabled maintenance mode before invoking the script (to protect the DB dump), which disables the LDAP user provider and causes the `before-update` export (`occ user:list`, `config:list`, `app:list`) to silently omit LDAP users. The script now assumes maintenance mode is **off** at start, runs the `before-update` export with apps loaded, lets `updater.phar` manage maintenance mode itself, and explicitly disables it again before `occ upgrade` and `occ app:update` (since `occ upgrade` does not turn it off on its own) — so all post-upgrade commands (`app:update`, `db:add-missing-*`, `db:convert-filecache-bigint`, the `after-update` export) also run with apps loaded. Callers must drop the manual `maintenance:mode --on` step from their pre-script workflow; the DB dump should rely on `--single-transaction` instead.
* **roles**: Set `become: false` on tasks delegated to localhost across the collection. Previously these tasks inherited `become: true` from the playbook level and tried to call `sudo` on the Ansible controller, which fails on controllers without a passwordless sudo setup with `sudo: a password is required`. Affected are all `repo_*` roles, the `*_vm` cloud roles (`exoscale_vm`, `hetzner_vm`, `infomaniak_vm`), all `icingaweb2_module_*` roles that download artefacts, `monitoring_plugins`, `shared`, plus several others. Existing playbooks that were working without playbook-level `become: true` are unaffected ([#242](https://github.com/Linuxfabrik/lfops/issues/242)).
* **role:repo_monitoring_plugins**: Add the missing `run_once: true` on the local repo-key download task on Red Hat platforms, matching the Debian variant. The key is now downloaded once per run instead of once per host.
* **role:network**: README still claimed the role disables zeroconf, but the corresponding `NOZEROCONF=yes` task was removed in 2024 (NetworkManager no longer adds the zeroconf route by default). Bring the README in line with what the role actually does and call out the Hetzner-specific `hc-utils` cleanup explicitly.
* **role:haveged**: Setting `haveged__service_state: 'stopped'` produced the invalid systemctl command `stopp` because of a `[:-2]` slice in the task name. The role now uses `ansible.builtin.service` directly with the configured state, so all four valid values (`reloaded` / `restarted` / `started` / `stopped`) work as expected.
* **role:unattended_upgrades**: Correct README description; the role deactivates Unattended Upgrades by setting both `APT::Periodic` flags to `0` in `/etc/apt/apt.conf.d/20auto-upgrades` (Debian/Ubuntu), it does not remove the `unattended-upgrades` package.
* **playbooks/clamav, playbooks/duplicity, playbooks/fangfrisch, playbooks/influxdb, playbooks/mongodb, playbooks/python_venv**: Enable `repo_baseos` (CRB) and `repo_epel` on Rocky 9+ before the `python_venv` role to fix `No match for argument: python3-virtualenv` / `nothing provides python3-wheel-wheel needed by python3-virtualenv`.
* **playbooks/setup_graylog_datanode, playbooks/setup_graylog_server, playbooks/setup_icinga2_master, playbooks/setup_rocketchat**: Extend existing `repo_baseos` `when` condition from `== "9"` to `| int >= 9` (Rocky 10+), and extend `repo_epel` version list to include RHEL/Rocky 10.
* **playbooks/freeipa_client, playbooks/freeipa_server**: Set `strategy: 'linear'` explicitly so the playbooks work even when the user's `ansible.cfg` defaults to a strategy that reuses the target Python interpreter (e.g. `mitogen_linear`). The ansible-freeipa modules rely on `ipalib`'s global API singleton and otherwise fail with `API.bootstrap() already called` on the second module call.
* **role:mariadb_server**: Stop writing the deprecated `innodb_buffer_pool_chunk_size` setting to the generated config for MariaDB 10.11, 11.4 and 11.8. MariaDB ignores the value from 10.11.12, 11.4.6 and 11.8.2 onwards and derives the chunk size automatically from `innodb_buffer_pool_size`. The user-facing role variables stay declared for backward compatibility but are now documented as deprecated. On MariaDB 10.6 the setting is unchanged. The role now also aborts at the start of the run with a clear error message if `innodb_buffer_pool_chunk_size` (on MariaDB 10.11+) or `innodb_file_per_table` (on MariaDB 11.0+) is still set in inventory, so that an upgrade from MariaDB 10.6 to 11.x does not silently keep a stale override around.
* **role:mariadb_server**: Fix MariaDB starting in the `unconfined_service_t` SELinux domain on RHEL 10, which leaves `/var/lib/mysql/mysql.sock` mislabeled and breaks `php-fpm`/`httpd_t` clients (e.g. Icinga Web 2 login: `SQLSTATE[HY000] [2002] Permission denied`). The unit drop-in's `ExecStartPre=-/bin/chcon -t mysqld_exec_t /usr/sbin/mariadbd` workaround for [MDEV-30520](https://jira.mariadb.org/browse/MDEV-30520) cannot relabel the binary on EL10+, where the packaged `mariadb.service` applies `ProtectSystem` that mounts `/usr` read-only inside the service sandbox. The role now sets the `mysqld_exec_t` file context for `/usr/sbin/mariadbd` persistently via `semanage fcontext` + `restorecon` (outside the systemd sandbox) and notifies a restart so the daemon comes up in `mysqld_t`.
* **role:icinga2_master**: Fix `selinux` role failing on RHEL 10 with `SELinux boolean icinga2_can_connect_all is not defined in persistent policy` (and `[Errno 11]` for the other Icinga/Nagios booleans). The `icinga2-selinux` policy module references `nagios_*_plugin_t` types that were moved out of the EL10 base policy into the separate `nagios-selinux` package (EPEL), so without it the `icinga2-selinux` `%post` silently fails and the booleans never appear. The role now installs `nagios-selinux` as a separate pre-install task on RHEL 10 so its `%post` registers the required types before `icinga2-selinux`'s `%post` runs.
* **role:infomaniak_vm**: Stop passing `security_groups` to `openstack.cloud.server`. Since the security group is already applied on the `ext-net1` port, setting it on the server made Neutron attempt the same on internal-network ports where `port_security_enabled` is `false`, failing with `Network requires port_security_enabled and subnet associated in order to apply security groups.`
* **role:redis**: Fix `No package redis available.` on RHEL 10. Red Hat replaced Redis with Valkey (BSD-licensed, API/protocol/config-file compatible) in AppStream and the Remi repos no longer ship Redis for EL10 either. The role now installs `valkey` on EL10 via a new OS-specific `vars/RedHat10.yml`. Hardcoded paths (package name, `package_facts` lookup, `/etc/redis/`, `/var/lib/redis`, `/var/run/redis`, `/etc/redis/modules`) in `tasks/main.yml` and the `<v>-redis.conf.j2` templates are now driven by internal `__redis__*` variables, so EL8/9 keep installing Redis unchanged. User-facing variables (`redis__conf_*`, `redis__service_name`) stay backwards-compatible.
* **role:redis**: Guard the four `loadmodule /usr/lib/redis/modules/{rejson,redisbloom,redistimeseries,redisearch}.so` directives in `8.0-redis.conf.j2` with an `{% if __redis__package == 'redis' %}` block. They reference Redis Stack bundle paths that don't exist on Valkey (the EL10 replacement), so loading them aborts the server. On RHEL 8/9 (Redis) the directives stay active.
* **role:openvpn_server**: Fix `invalid selinux context: [Errno 22] Invalid argument` on RHEL 10 when deploying `server.p12` / `crl.pem`. The SELinux type `openvpn_etc_t` no longer exists in the RHEL 10 core policy (only `openvpn_port_t` and the packet types remain). The role now uses `etc_t` on RHEL 10 via a new OS-specific internal variable `__openvpn_server__selinux_etc_type`; other platforms keep `openvpn_etc_t`
* **role:repo_epel**: Fix malformed RHEL 10 `epel.repo`: a missing newline in the `[epel-source]` section rendered `enabled=0username=<login>` when `repo_epel__basic_auth_login` was set, causing dnf to reject the file with `Invalid configuration value: enabled=0username=...`
* **role:repo_mariadb**: Fix `dnf -y module disable mariadb` failing on RHEL 10 with `missing groups or modules: mariadb`. Modularity was removed in EL10 (DNF5) and the `mariadb` module no longer exists, so the task and the corresponding `module_hotfixes = 1` directive in the generated `MariaDB.repo` are now scoped to RHEL 8 and 9 only
* **role:infomaniak_vm**: Apply the VM's security group on the `ext-net1` port instead of (only) on the server. When a VM boots against a pre-created port, Neutron enforces the port's security groups, not those passed to the server, so without this the configured rules were silently ignored on the public interface
* **role:logstash**: Default value of `logstash__java_opts` now caps JVM heap size at 8g.
* **role:logstash**: Default value of `logstash__java_opts` now sets JVM heap size to be 60% of total memory.
* **role:graylog_datanode**: Validate that `graylog_datanode__password_secret | length >= 16`
* **role:graylog_server**: Validate that `graylog_server__password_secret | length >= 16`
* **role:nextcloud**: Ensure that the Nextcloud OCC is executable.
* **execution-environment**: Add missing `sshpass` system package, required for SSH password-based connections (e.g. `--ask-pass`)
* **role:keycloak**: Fix transaction timeout silently dropping from 3600s to 300s on Keycloak 26.6.0+ due to new `transaction-default-timeout` CLI option overriding the Quarkus property
* **role:keycloak**: Fix MariaDB database encoding defaulting to deprecated `utf8` (`utf8mb3`) instead of `utf8mb4`, causing warnings in Keycloak 26.6.0+
* **role:mount**: Fix `when` condition for NFS/CIFS client package installation failing with multiple mounts and when `state` key is undefined

### Security

* **plugin:gpg_key**: The cleartext passphrase is no longer included in the module's failure output when key generation fails.
* **role:repo_\***: HTTP basic auth credentials are now only written to the repository config files when a custom mirror URL is set. Previously, setting `lfops__repo_basic_auth_login` without `lfops__repo_mirror_url` wrote the credentials into repo files that still pointed at the public vendor mirrors, causing the package manager to send them to servers that do not use basic auth. The Icinga repo is intentionally unchanged, since its subscription URL legitimately requires basic auth.
* **ci**: Scope `GITHUB_TOKEN` permissions in the dependabot-auto-merge workflow to the job level, with top-level now `read-all`. Matches the pattern used by the other LFOps workflows and addresses the OpenSSF Scorecard `Token-Permissions` finding.
* **ci**: Harden the CI supply chain: the `pre-commit` install in the pre-commit-autoupdate workflow is now hash-pinned via `.github/pre-commit/requirements.txt` (generated with `pip-compile --generate-hashes --strip-extras`), and `dependabot/fetch-metadata` is pinned to a commit SHA so all GitHub Actions used in `.github/workflows/` are now pinned by hash. The policy is documented in CONTRIBUTING.md under "CI Supply Chain"

## [v6.0.1] - 2026-04-07

### Fixed

* **ci**: Strip badges from README.md before publishing to Galaxy, as external images are not rendered


## [v6.0.0] - 2026-04-07

### Breaking Changes

* **role:nfs_server**: Rework `nfs_server__exports` from a list of strings to a list of dictionaries with new `path`, `clients`, `owner`, `group`, and `mode` subkeys
* **role:kvm_host**: Change NAT to be explicitly activated for virtual nets
* **role:apache_httpd**: Change the default to not install/enable mod_qos by default (it is no longer shipped in EPEL 10)

### Added

* Add MkDocs-based documentation site, deployed automatically to GitHub Pages via `tools/build-docs` and a GitHub Actions workflow
* **CONTRIBUTING**: Document semantic parameter ordering for Ansible modules
* **playbooks**: Add `example.yml` and `setup_example.yml` playbooks as development references
* **role:example**: Add complete example role with defaults, handlers, tasks, templates, and vars as a reference for consistent role development
* **role:icingaweb2_module_grafana**: Add JWT support
* **role:grafana**: Add JWT support
* Add `playbooks/README.md` documenting all playbooks with their roles in execution order and available skip variables
* **role:apache_httpd**: Add platform-specific behavior section, wsgi example, and document localhost endpoints in README
* **role:apache_httpd**: Add skip variables section to README linking to relevant playbooks
* **role:mailx**: Add skip variables section to README linking to relevant playbooks
* **role:policycoreutils**: Add skip variables section to README linking to relevant playbooks
* **role:yum_utils**: Add skip variables section to README linking to relevant playbooks
* **plugin:bitwarden_item**: Add file-based item cache to reduce `bw serve` API calls, preventing crashes under load. Cache is stored in `$XDG_RUNTIME_DIR` (RAM-backed tmpfs) with `/tmp` fallback. After create/edit operations, the cache is updated inline to avoid expensive full re-syncs, with a 1-second sleep as rate limit to prevent Bitwarden API errors. Convert `is_unlocked` to a property to fix it never being called.
* **role:freeipa_server**: Add `--diff` support for all FreeIPA modules and add `freeipa_server:configure` tag
* **role:mariadb_server**: Add `mariadb_server__cnf_wsrep_log_conflicts` and `mariadb_server__cnf_wsrep_retry_autocommit` variables
* **role:mariadb_server**: Add `mariadb_server__cnf_wsrep_gtid_mode` variable to configure `wsrep_gtid_mode` for Galera
* **role:openvpn_server**: Add `openvpn_server:crl` tag to allow deploying the certificate revocation list independently
* **role:nextcloud**: Add Icinga2 set / unset downtime functionality to `nextcloud-update.j2`
* **execution-environment**: Add mitogen
* **role:nfs_client**: Add optional `owner`, `group` and `mode` subkeys for mount point directories
* **role:logstash**: Add support for deploying custom grok pattern files to `/etc/logstash/patterns/`
* **role:mount**: Add optional `owner` and `group` subkeys for mount point directories
* **role:elasticsearch**: Add logrotate config for daily rotation
* **role:freeipa_server**: Add the ability to specify the systemd unit start timeout
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

* **ci**: Publish pre-releases directly to prod Ansible Galaxy instead of galaxy-dev, since it is unreliable and pulp-ansible excludes pre-release versions from "latest"
* Update pre-commit hooks to latest versions
* Unify CONTRIBUTING and convert from reStructuredText to Markdown
* **roles**: Add `backup: true` to all `ansible.builtin.template` tasks to ensure config file backups before overwriting
* **role:nextcloud**: Refactor `nextcloud-update.j2`
* **role:keycloak**: Rework `keycloak.conf` template to match Keycloak's default config structure
* **role:apache_httpd**: bump Core Rule Set to 4.24.1
* **role:repo_remi**: Install Composer from `remi-modular` repository
* **role:icingadb**: Enhance `config.yml` template
* **role:apache_httpd**: Improve output; bump Core Rule Set to 4.24.0

### Fixed

* **role:apache_httpd**: Fix `apache_httpd__mod_security_coreruleset_version` default value in README (4.4.0 -> 4.24.1), fix prefork variable names in README (`spare_threads` -> `spare_servers`), fix various typos ("best practise", "Tipp")
* **role:mailx**: Fix grammar in task name ("make" -> "makes"), sort template module parameters alphabetically
* **role:policycoreutils**: Fix grammar in task name ("are" -> "is")
* **plugin:bitwarden_item**: Fix missing `raise` in multipart error handling, `break` instead of `continue` in multi-term lookup, `folder_id` wrongly typed as `list` instead of `str` in module, notes default mismatch between documentation and code, and wrong "lookup plugin" wording in module documentation
* **role:mirror**: Fix missing `0440` permissions on sudoers file
* **role:login**: Rename sudoers file from `lfops_login` to `linuxfabrik` to match the kickstart configuration; remove the old file automatically
* **roles**: Fix Ansible 2.19 deprecation warning for conditional results of type `int` by using `| length > 0` instead of `| length`
* **role:firewall**: Fix fwbuilder repo clone being skipped when `run_once` picks a host without `firewall__fwbuilder_repo_url`
* **role:sshd**: Validate sshd config with `sshd -t` before reloading the service
* **role:nfs_client**: Fix systemd not being aware of new or removed NFS mount units
* **role:keycloak**: Fix issues preventing Keycloak from starting
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

* **role:nextcloud**: Add nextcloud_occ_*_config modules with diff and check mode support
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


[Unreleased]: https://github.com/Linuxfabrik/lfops/compare/v7.0.0...HEAD
[v7.0.0]: https://github.com/Linuxfabrik/lfops/compare/v6.0.1...v7.0.0
[v6.0.1]: https://github.com/Linuxfabrik/lfops/compare/v6.0.0...v6.0.1
[v6.0.0]: https://github.com/Linuxfabrik/lfops/compare/v5.1.0...v6.0.0
[v5.1.0]: https://github.com/Linuxfabrik/lfops/compare/v5.0.0...v5.1.0
[v5.0.0]: https://github.com/Linuxfabrik/lfops/compare/v4.0.0...v5.0.0
[v4.0.0]: https://github.com/Linuxfabrik/lfops/compare/v3.0.0...v4.0.0
[v3.0.0]: https://github.com/Linuxfabrik/lfops/compare/v2.0.1...v3.0.0
[v2.0.1]: https://github.com/Linuxfabrik/lfops/compare/v2.0.0...v2.0.1
[v2.0.0]: https://github.com/Linuxfabrik/lfops/compare/v1.0.1...v2.0.0
[v1.0.1]: https://github.com/Linuxfabrik/lfops/compare/v1.0.0...v1.0.1
[v1.0.0]: https://github.com/Linuxfabrik/lfops/releases/tag/v1.0.0
