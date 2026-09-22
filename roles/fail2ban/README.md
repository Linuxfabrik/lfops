# Ansible Role linuxfabrik.lfops.fail2ban

This role installs and configures [fail2ban](https://www.fail2ban.org).

Filters and jails are defined in the inventory (`fail2ban__filters__*_var` / `fail2ban__jails__*_var`). Each entry either references one of the templates shipped with the role, or uses the `raw` template to deploy an arbitrary filter or jail definition.

This role provides five additional filters:

* apache-404: Matches HTTP 404 responses in Apache access logs (combined, combinedio, common, fail2ban, linuxfabrikio, matomo, vhost_common). Can be used to ban IPs causing excessive 404 errors.
  **Important:** in order to capture the client ip for all formats, this filter requires the ServerName to be a domain instead of an ip address when using a LogFormat where the canonical ServerName `%v` precedes the client IP `%h` (matomo, vhost_common).
* apache-dos: Matches all incoming requests to Apache. Can be used to limit the number of allowed requests per client.
* nextcloud: Matches failed logins and failed two-factor challenges in the Nextcloud log (`nextcloud.log`), the filter from the [Nextcloud hardening guide](https://docs.nextcloud.com/server/stable/admin_manual/installation/harden_server.html#setup-fail2ban). The `z10-nextcloud` jail bans IPs that fail too often. Nextcloud logs the address of the client, also behind a reverse proxy listed in its `trusted_proxies`, so the jail runs on the Nextcloud host. There it only keeps out clients that connect to the host directly: traffic that comes through the proxy arrives from the proxy's address, which the ban does not cover.
* portscan: Instantly blocks an IP if it accesses a non-permitted port.
* wordpress-login: Matches failed WordPress logins in Apache access logs (combined, common, linuxfabrikio, matomo, vhost_common), also for WordPress in a sub-path such as `/blog`, which WordPress answers with the login form again (HTTP 200) instead of a redirect. The `z10-wordpress-login` jail bans IPs that fail too often. It bans the address Apache logs as the client, so behind a reverse proxy it belongs on the proxy, where that is the visitor's address; on the WordPress host it would ban the proxy.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

The role deploys its `[DEFAULT]` section as `jail.d/z00-defaults.conf`. fail2ban reads `jail.d/` in alphabetical order, so this file is read after the `00-firewalld.conf` that the `fail2ban-firewalld` package ships on the Red Hat family, and `banaction` ends up as `fail2ban__jail_default_banaction` instead of the packaged firewalld action. `banaction_allports` is not touched and keeps the packaged value.

Jails are read from a `z10-<template>.conf.j2` source but written to `jail.d/<filename>.conf`, so the destination name, and with it the order in which fail2ban reads the jail, is chosen freely per entry. Filters have no such prefix and are written to `filter.d/<filename>.conf`.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* On Rocky 9 and newer, the CRB repository must be enabled, since EPEL builds against it (role: [linuxfabrik.lfops.repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos)).
* The `python3-policycoreutils` module must be installed (required for the SELinux Ansible tasks) (role: [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils)).
* On RHEL-compatible systems, the EPEL repository must be enabled (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)).
* On RHEL-compatible systems, the `nis_enabled` SELinux boolean must be enabled (role: [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux)).
* sshd must log at `VERBOSE` level, otherwise the sshd jail does not see the failed logins (role: [linuxfabrik.lfops.sshd](https://github.com/Linuxfabrik/lfops/tree/main/roles/sshd)).
* The firewall must be one the `iptables-multiport` banaction can insert its chains into (role: [linuxfabrik.lfops.firewall](https://github.com/Linuxfabrik/lfops/tree/main/roles/firewall)).


## Requirements

* Optional: The `apache-*` jails read the Apache logs below `/var/log/httpd/`.
* Optional: The `nextcloud` jail reads `fail2ban__jail_nextcloud_logpath`. On SELinux systems, fail2ban may only read files labeled as logs, which is why the `nextcloud` role writes the Nextcloud log to `/var/log/nextcloud/` instead of the data directory. fail2ban does not start while the log file is missing.
* Optional: The `portscan` filter matches the kernel log of an iptables firewall that logs denied packets, as fwbuilder generates it, read through the systemd journal. Without such a firewall the jail never bans.


## Tags

`fail2ban`

* Installs and configures fail2ban.
* Triggers: fail2ban.service restart.

`fail2ban:configure`

* Deploys the actions, filters and jails without touching the packages.
* Triggers: fail2ban.service restart.

`fail2ban:state`

* Manages the state of the fail2ban service.
* Triggers: none.


## Optional Role Variables

`fail2ban__filter_apache_404_ignoreregex`

* A list of regular expressions. Log lines matching any of these patterns will be ignored by the `apache-404` filter, even if they match the `failregex`. Useful for excluding known missing resources like `/favicon.ico` or `/assets/style.css`.
* Type: List of strings.
* Default: `[]`

`fail2ban__filters__group_var` / `fail2ban__filters__host_var`

* The fail2ban filter definition. For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `apache-404`, `apache-dos`, `nextcloud`, `portscan`, `wordpress-login`
* Subkeys:

    * `filename`:

        * Mandatory. Destination filename in `filter.d/`, and normally is equal to the name of the source `template` used. Will be suffixed with `.conf`.
        * Type: String.

    * `raw`:

        * Optional. Raw content for the filter. Only used if `template` is `raw`.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

    * `template`:

        * Mandatory. Name of the Jinja template source file to use. Have a look at the possible options [here](https://github.com/Linuxfabrik/lfops/tree/main/roles/fail2ban/templates/etc/fail2ban/filter.d), or `raw`.
        * Type: String.

`fail2ban__jail_apache_404_bantime`

* The ban duration for the apache-404 jail.
* Type: String.
* Default: `'8h'`

`fail2ban__jail_apache_404_findtime`

* The find time for the apache-404 jail. An IP is banned if it causes more than `fail2ban__jail_apache_404_maxretry` 404 errors within this duration.
* Type: String.
* Default: `'10s'`

`fail2ban__jail_apache_404_maxretry`

* The number of 404 errors within `fail2ban__jail_apache_404_findtime` before an IP is banned.
* Type: Integer.
* Default: `10`

`fail2ban__jail_default_action`

* The default action. This will be used in all jails which do not overwrite it.
* Type: String.
* Default: `'%(banaction)s[name=%(__name__)s, bantime="%(bantime)s", port="%(port)s", protocol="%(protocol)s", chain="%(chain)s"]'`

`fail2ban__jail_default_banaction`

* The default banaction, which will be executed as defined in `fail2ban__jail_default_action` (assuming the jail does not overwrite it).
* Type: String.
* Default: `'iptables-multiport'`

`fail2ban__jail_default_ignoreip`

* List of IP addresses (in CIDR notation) that will be ignored from all jails (assuming the jail does not overwrite it).
* Type: List of strings.
* Default: `[]`

`fail2ban__jail_default_rocketchat_hook`

* The incoming Rocket.Chat hook which will be used to send a notification on bans. For this to work `rocketchat` has to be in the action, have a look at `fail2ban__jail_default_action` (example below).
* Type: String.
* Default: `''`

`fail2ban__jail_nextcloud_bantime`

* The ban duration for the nextcloud jail.
* Type: String.
* Default: `'8h'`

`fail2ban__jail_nextcloud_findtime`

* The find time for the nextcloud jail. An IP is banned if it fails to log in `fail2ban__jail_nextcloud_maxretry` times within this duration.
* Type: String.
* Default: `'10m'`

`fail2ban__jail_nextcloud_logpath`

* The Nextcloud log file the nextcloud jail reads.
* Type: String.
* Default: `'/var/log/nextcloud/nextcloud.log'`

`fail2ban__jail_nextcloud_maxretry`

* The number of failed Nextcloud logins within `fail2ban__jail_nextcloud_findtime` before an IP is banned.
* Type: Integer.
* Default: `5`

`fail2ban__jail_portscan_allowed_ports`

* A list of ports which are allowed to be accessed. IPs accessing these ports will not be blocked. Note: This setting is for the portscan jail.
* Type: List of numbers.
* Default: `[22]`

`fail2ban__jail_portscan_bantime`

* The ban duration for the portscan jail.
* Type: String.
* Default: `'8h'`

`fail2ban__jail_portscan_server_ips`

* A list of IP addresses of the server. Only traffic destined for these IPs will be considered. This prevents accidental banning due to traffic which is passing by the server, but not destined for it. Note: This setting is for the portscan jail.
* Type: List of strings.
* Default: `'{{ ansible_facts["all_ipv4_addresses"] }}'`

`fail2ban__jail_sshd_bantime`

* The ban duration for the sshd jail.
* Type: String.
* Default: `'7d'`

`fail2ban__jail_wordpress_login_bantime`

* The ban duration for the wordpress-login jail.
* Type: String.
* Default: `'8h'`

`fail2ban__jail_wordpress_login_findtime`

* The find time for the wordpress-login jail. An IP is banned if it fails to log in `fail2ban__jail_wordpress_login_maxretry` times within this duration.
* Type: String.
* Default: `'10m'`

`fail2ban__jail_wordpress_login_maxretry`

* The number of failed WordPress logins within `fail2ban__jail_wordpress_login_findtime` before an IP is banned.
* Type: Integer.
* Default: `5`

`fail2ban__jails__group_var` / `fail2ban__jails__host_var`

* The fail2ban jail definition. For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `z10-portscan`, `z10-sshd`
* Subkeys:

    * `filename`:

        * Mandatory. Destination filename in `jail.d/`, and normally is equal to the name of the source `template` used. Will be suffixed with `.conf`.
        * Type: String.

    * `raw`:

        * Optional. Raw content for the jail. Only used if `template` is `raw`.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

    * `template`:

        * Mandatory. Name of the Jinja template source file to use. Have a look at the possible options [here](https://github.com/Linuxfabrik/lfops/tree/main/roles/fail2ban/templates/etc/fail2ban/jail.d), or `raw`.
        * Type: String.

`fail2ban__service_enabled`

* Enables or disables the fail2ban service, analogous to `systemctl enable/disable`.
* Type: Bool.
* Default: `true`

`fail2ban__service_state`

* Changes the state of the fail2ban service, analogous to `systemctl start/stop/restart/reload`.
* Type: String. One of `reloaded`, `restarted`, `started`, `stopped`.
* Default: `'started'` if `fail2ban__service_enabled` is `true`, else `'stopped'`

Example:
```yaml
# optional
fail2ban__filter_apache_404_ignoreregex:
  - '^<HOST> [^"]*"GET /favicon\.ico '
  - '^<HOST> [^"]*"GET /assets/style\.css '
fail2ban__filters__host_var:
  - filename: 'numishare-admin'
    state: 'present'
    template: 'raw'
    raw: |-
      [Definition]
      failregex = ^<HOST> .*"POST /admin/j_security_check HTTP/[\d.]+" (401|403)
      ignoreregex =
fail2ban__jail_apache_404_bantime: '8h'
fail2ban__jail_apache_404_findtime: '10s'
fail2ban__jail_apache_404_maxretry: 10
fail2ban__jail_default_action: |-
  %(banaction)s[name=%(__name__)s, bantime="%(bantime)s", port="%(port)s", protocol="%(protocol)s", chain="%(chain)s"]
  rocketchat[name=%(__name__)s, rocketchat-hook="%(rocketchat-hook)s"]
fail2ban__jail_default_banaction: 'iptables-multiport'
fail2ban__jail_default_ignoreip:
  - '192.0.2.1/32' # ansible deployment host
fail2ban__jail_default_rocketchat_hook: ''
fail2ban__jail_nextcloud_bantime: '8h'
fail2ban__jail_nextcloud_findtime: '10m'
fail2ban__jail_nextcloud_logpath: '/var/log/nextcloud/nextcloud.log'
fail2ban__jail_nextcloud_maxretry: 5
fail2ban__jail_portscan_allowed_ports:
  - 22
fail2ban__jail_portscan_bantime: '8h'
fail2ban__jail_portscan_server_ips:
  - '192.0.2.5'
  - '198.51.100.100'
fail2ban__jail_sshd_bantime: '7d'
fail2ban__jail_wordpress_login_bantime: '8h'
fail2ban__jail_wordpress_login_findtime: '10m'
fail2ban__jail_wordpress_login_maxretry: 5
fail2ban__jails__host_var:
  - filename: 'z10-apache-dos'
    state: 'absent'
    template: 'apache-dos'
  - filename: 'z10-wordpress-login'
    state: 'present'
    template: 'wordpress-login'
  - filename: 'z20-custom-apache-dos'
    state: 'present'
    template: 'raw'
    raw: |-
      [apache-dos]
      bantime  = 5m
      enabled  = true
      findtime = 10s
      logpath  = /var/log/httpd/*access?log
      maxretry = 600
      port     = http,https
fail2ban__service_enabled: true
fail2ban__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
