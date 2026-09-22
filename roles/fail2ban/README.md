# Ansible Role linuxfabrik.lfops.fail2ban

This role installs and configures [fail2ban](https://www.fail2ban.org).

Filters and jails are defined in the inventory (`fail2ban__filters__*_var` / `fail2ban__jails__*_var`). Each entry either references one of the templates shipped with the role, or uses the `raw` template to deploy an arbitrary filter or jail definition.

This role provides five additional filters:

* apache-404: Matches HTTP 404 responses in Apache access logs (combined, combinedio, common, fail2ban, linuxfabrikio, matomo, vhost_common). Can be used to ban IPs causing excessive 404 errors.
  **Important:** in order to capture the client ip for all formats, this filter requires the ServerName to be a domain instead of an ip address when using a LogFormat where the canonical ServerName `%v` precedes the client IP `%h` (matomo, vhost_common).
* apache-dos: Matches all incoming requests in Apache access logs (combined, combinedio, common, fail2ban, linuxfabrikio, matomo, vhost_common; other formats do not match). Can be used to limit the number of allowed requests per client. Like apache-404, it needs a ServerName that is a domain for matomo and vhost_common.
* nextcloud: Matches failed logins and failed two-factor challenges in the Nextcloud log (`nextcloud.log`), the filter from the [Nextcloud hardening guide](https://docs.nextcloud.com/server/stable/admin_manual/installation/harden_server.html#setup-fail2ban). The `z10-nextcloud` jail bans IPs that fail too often. Nextcloud logs the address of the client, also behind a reverse proxy listed in its `trusted_proxies`, so the jail runs on the Nextcloud host. There it only keeps out clients that connect to the host directly: traffic that comes through the proxy arrives from the proxy's address, which the ban does not cover.
* portscan: Instantly blocks an IP if it accesses a non-permitted port. Only packets that open a connection count: a TCP SYN without ACK, PSH, RST or FIN, or any UDP packet. Reply traffic of a TCP connection the firewall no longer tracks, such as the late FIN of a half-closed connection, an RST or a mid-connection ACK, is ignored, and so are ICMP error messages, so a server that a local proxy talks to is not banned. TCP scans that send no plain SYN, such as FIN, NULL, Xmas, ACK and SYN/FIN scans, are therefore not banned either; they find no open port on a stateful firewall. A late UDP reply, for example a DNS answer that arrives after the firewall has forgotten the query, is still banned, since the kernel log cannot tell it apart from a UDP scan.
* wordpress-login: Matches failed WordPress logins in Apache access logs (combined, common, linuxfabrikio, matomo, vhost_common), also for WordPress in a sub-path such as `/blog`, which WordPress answers with the login form again (HTTP 200) instead of a redirect. The `z10-wordpress-login` jail bans IPs that fail too often. It bans the address Apache logs as the client, so behind a reverse proxy it belongs on the proxy, where that is the visitor's address; on the WordPress host it would ban the proxy.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

The role deploys its `[DEFAULT]` section as `jail.d/z00-defaults.conf`. fail2ban reads `jail.d/` in alphabetical order, so this file is read after the `00-firewalld.conf` that the `fail2ban-firewalld` package ships on the Red Hat family, and `banaction` ends up as `fail2ban__jail_default_banaction` instead of the packaged firewalld action. `banaction_allports` is not touched and keeps the packaged value.

Jails are read from a `z10-<template>.conf.j2` source but written to `jail.d/<filename>.conf`, so the destination name, and with it the order in which fail2ban reads the jail, is chosen freely per entry. Filters have no such prefix and are written to `filter.d/<filename>.conf`.

The `apache-*` and `php-url-fopen` templates enable the jail of the same name that fail2ban ships in `jail.conf`, with its filter and its `port`, `maxretry`, `findtime` and `bantime`. They only set `logpath`, to the error or access logs below `/var/log/httpd/` in the naming of the [apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role (`<name>-error.log`, `<name>-access.log`), which the `*error_log` and `*access_log` of `jail.conf` do not match.

On a host with `/var/log/httpd`, the role enables these jails without further inventory:

* `apache-auth`: failed logins (`mod_auth_basic`, `mod_auth_digest`), requests denied by `Require`, and SNI mismatches.
* `apache-fakegooglebot`: clients that claim to be Googlebot, but whose address does not resolve to Google.
* `apache-modsecurity`: requests that ModSecurity denied.
* `apache-nohome`: probes for home directories (`/~root/`).
* `apache-noscript`: probes for scripts that do not exist (`.php`, `.asp`, `.pl`, `cgi-bin`).
* `apache-overflows`: path traversal attempts.
* `php-url-fopen`: attempts to pass a remote URL to a PHP script (remote file inclusion).

They belong on the host the clients connect to. Behind a reverse proxy, a ban on the client address does nothing, since the packets come from the proxy, and where Apache logs the proxy as the client, the jails would ban the proxy itself. The role therefore leaves them out where `apache_httpd__mod_remoteip_internal_proxy` lists a proxy; for a host behind a proxy without `mod_remoteip`, set `fail2ban__jails_apache_enabled` to `false`. Hosts without `/var/log/httpd`, or with the jails disabled, get them removed.

A ban of an HTTP jail (`apache-*`, `nextcloud`, `php-url-fopen`, `wordpress-login`) also closes the connections the client already holds on the ports of the jail, with `ss --kill` (`action.d/ss-kill.conf`). A firewall rule alone does not stop a client that keeps one HTTP/2 connection busy, and it leaves the server side of each open connection waiting until `Timeout`, holding an httpd worker. On the Red Hat family, SELinux only allows this with the `lfops_fail2ban_ss_kill` policy module, which the role installs unless SELinux is disabled. It grants fail2ban the `net_admin` capability, which also lets it reconfigure network interfaces. If `ss --kill` leaves a connection open, `/var/log/fail2ban.log` shows an `ERROR` for the `ss-kill` action. The other jails, such as `sshd`, leave established connections open.

The `apache-dos` template is not enabled by default. It bans a client that sends more than 600 requests within 10 seconds for 5 minutes, and doubles the duration with each further ban of the same address, up to one day. Its firewall rule only blocks new connections, so that a flood of connections does not keep the httpd workers waiting until `Timeout` even if `ss --kill` fails. The template sets its own `action`, so `fail2ban__jail_default_action` does not apply to it, and blocking only new connections needs an `nftables-*` or `iptables-*` banaction in `fail2ban__jail_default_banaction`. To change a single value, keep `z10-apache-dos` and add a jail file that is read after it with only that value (see the example below).

The `apache-badbots` and `apache-botsearch` templates are not enabled by default: they match against lists of user agents (2013) and paths (2017) that fail2ban no longer maintains.

The role deploys `skip_if_nologs = true`, so a jail whose `logpath` matches no file is skipped instead of keeping fail2ban from starting with all its other jails, for example on an Apache host before the first vHost is deployed. This needs fail2ban 1.1.1 or newer; older releases ignore the option, and there such a jail still keeps fail2ban from starting.

The sshd jail runs the filter in `aggressive` mode, which also bans clients that connect and leave without trying to log in, such as scanners and clients sending a broken protocol banner.

The bans go into the table `inet f2b-table` of nftables, next to the tables of the host's firewall, with one set of banned addresses per jail (`nft list set inet f2b-table addr-set-sshd`). A firewall reload that flushes the whole ruleset removes the table, and with it every ban: fail2ban rebuilds the table at its next ban, but bans an address it already lists as banned again only when that address shows up in the log once more. Restart fail2ban after such a reload.

The `iptables-*` banactions need the `xt_multiport` kernel module, which RHEL 10 ships in `kernel-modules-extra`. On a host whose running kernel lacks it, such as one installed from a cloud image, the role installs `kernel-modules-extra` for that kernel, so bans take effect without a reboot, and `kernel-modules-extra-matched`, so later kernels bring the module along. Without the module, iptables rejects every ban while fail2ban still lists the address as banned.

On the Red Hat family, the playbook deploys the Linuxfabrik repository, which serves fail2ban built from the latest upstream release. EPEL lags behind and does not recognize every attack its filters are meant for, for example the `invalid URI path` (`AH10244`) of a path traversal attempt in `apache-overflows`.


## Known Limitations

* The Apache jails are enabled when fail2ban is deployed after Apache. On a host that gets Apache later, run the fail2ban playbook again.
* `apache-badbots` only matches access log lines that end with the user agent, as in the `combined` format, not the `linuxfabrikio` format of the apache_httpd role.
* `apache-modsecurity` bans every client ModSecurity denies twice within 10 minutes, so a false positive of the Core Rule Set becomes a ban.
* `apache-overflows` only recognizes path traversal attempts. Apache 2.4 answers overlong request lines, invalid methods and invalid characters in the URI with a `400` without an error log line the filter could match.
* `php-url-fopen` only matches access logs that start with the client address (`combined`, `common`), not the `matomo` and `vhost_common` formats, which start with the server name.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* On Rocky 9 and newer, the CRB repository must be enabled, since EPEL builds against it (role: [linuxfabrik.lfops.repo_baseos](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_baseos)).
* The `python3-policycoreutils` module must be installed (required for the SELinux Ansible tasks) (role: [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils)).
* On RHEL-compatible systems, the EPEL repository must be enabled (role: [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel)).
* On RHEL-compatible systems, the Linuxfabrik repository serves fail2ban (role: [linuxfabrik.lfops.repo_linuxfabrik](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_linuxfabrik)).
* On RHEL-compatible systems, the `nis_enabled` SELinux boolean must be enabled (role: [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux)).
* sshd must log at `VERBOSE` level, otherwise the sshd jail does not see the failed logins (role: [linuxfabrik.lfops.sshd](https://github.com/Linuxfabrik/lfops/tree/main/roles/sshd)).
* The firewall must leave the nftables table of fail2ban alone (role: [linuxfabrik.lfops.firewall](https://github.com/Linuxfabrik/lfops/tree/main/roles/firewall)).


## Requirements

* Optional: The `apache-*` jails read the Apache logs below `/var/log/httpd/`.
* Optional: The `nextcloud` jail reads `fail2ban__jail_nextcloud_logpath`. On SELinux systems, fail2ban may only read files labeled as logs, which is why the `nextcloud` role writes the Nextcloud log to `/var/log/nextcloud/` instead of the data directory. fail2ban does not start while the log file is missing.
* Optional: The `portscan` filter matches the kernel log of an iptables firewall that logs denied packets, as fwbuilder generates it, read through the systemd journal. Without such a firewall the jail never bans.


## Tags

`fail2ban`

* Installs and configures fail2ban.
* Triggers: fail2ban.service restart.

`fail2ban:configure`

* Deploys the actions, filters, jails and the SELinux policy module without touching the packages.
* Triggers: fail2ban.service restart.

`fail2ban:state`

* Manages the state of the fail2ban service.
* Triggers: none.


## Optional Role Variables

`fail2ban__filter_apache_404_ignoreregex`

* A list of regular expressions. Log lines matching any of these patterns will be ignored by the `apache-404` filter, even if they match the `failregex`. Useful for excluding known missing resources like `/favicon.ico` or `/assets/style.css`, or requests from authenticated users, such as the clients of a package mirror that request packages from outdated repository metadata.
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

* The default action. This will be used in all jails which do not overwrite it. The HTTP jails run it followed by `ss-kill` (see "How the Role Behaves"); `apache-dos` sets its own action.
* Type: String.
* Default: `'%(banaction)s[name=%(__name__)s, bantime="%(bantime)s", port="%(port)s", protocol="%(protocol)s", chain="%(chain)s"]'`

`fail2ban__jail_default_banaction`

* The default banaction, which will be executed as defined in `fail2ban__jail_default_action` (assuming the jail does not overwrite it).
* Type: String.
* Default: `'nftables-multiport'`
* Deviates from the upstream default `iptables-multiport` (`firewallcmd-rich-rules` with the `fail2ban-firewalld` package on RHEL): LFOps deploys nftables firewalls, and the bans then live in nftables as well instead of going through the iptables compatibility layer or firewalld.

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

* Ports on which a connection attempt that the firewall denies does not lead to a ban in the portscan jail. The jail only sees packets the firewall denied, so a port that is open to everyone never triggers it, whether it is listed or not. List the ports that the firewall opens to some sources only, such as SSH restricted to an admin network, so that others trying them are blocked without being banned. The ports are matched exactly and apply to TCP and UDP alike, so `22` exempts port 22 and not 2222. An empty list exempts no port.
* Type: List of numbers.
* Default: `'{{ [sshd__port | d(22)] }}'`, the port the [sshd](https://github.com/Linuxfabrik/lfops/tree/main/roles/sshd) role configures

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

`fail2ban__jail_sshd_mode`

* The mode of the sshd filter. `normal` bans failed logins, `ddos` clients that connect and leave without trying to log in, `extra` further failures of the authentication, and `aggressive` all of them.
* Type: String. One of `aggressive`, `ddos`, `extra`, `normal`.
* Default: `'aggressive'`
* Deviates from the upstream default `normal`, which leaves scanners alone that only probe the protocol banner.

`fail2ban__jail_sshd_port`

* The port the sshd jail bans on, or several as a comma-separated list such as `'22,2222'`. Takes the port the [sshd](https://github.com/Linuxfabrik/lfops/tree/main/roles/sshd) role configures.
* Type: String.
* Default: `'{{ sshd__port | d(22) }}'`
* Deviates from the upstream default `ssh` (port 22): a ban only blocks the ports listed here, so on a host where sshd listens on another port it would have no effect.

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
* Default: `z10-portscan`, `z10-sshd`, and on Apache hosts `z10-apache-auth`, `z10-apache-fakegooglebot`, `z10-apache-modsecurity`, `z10-apache-nohome`, `z10-apache-noscript`, `z10-apache-overflows`, `z10-php-url-fopen` (see `fail2ban__jails_apache_enabled`)
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

`fail2ban__jails_apache_enabled`

* Enables the Apache jails (see "How the Role Behaves") on a host with `/var/log/httpd`. Set it to `false` on a host behind a reverse proxy that logs the proxy as the client, such as LibreNMS behind a proxy.
* Type: Bool.
* Default: `true`, unless `apache_httpd__mod_remoteip_internal_proxy` lists a proxy

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
  - '^[^\["]* (?!- )\S+ \[' # 404s from authenticated users (%u is not "-")
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
fail2ban__jail_default_banaction: 'nftables-multiport'
fail2ban__jail_default_ignoreip:
  - '192.0.2.1/32' # ansible deployment host
fail2ban__jail_default_rocketchat_hook: ''
fail2ban__jail_nextcloud_bantime: '8h'
fail2ban__jail_nextcloud_findtime: '10m'
fail2ban__jail_nextcloud_logpath: '/var/log/nextcloud/nextcloud.log'
fail2ban__jail_nextcloud_maxretry: 5
fail2ban__jail_portscan_allowed_ports:
  - 22532
fail2ban__jail_portscan_bantime: '8h'
fail2ban__jail_portscan_server_ips:
  - '192.0.2.5'
  - '198.51.100.100'
fail2ban__jail_sshd_bantime: '7d'
fail2ban__jail_sshd_mode: 'aggressive'
fail2ban__jail_sshd_port: '22532'
fail2ban__jail_wordpress_login_bantime: '8h'
fail2ban__jail_wordpress_login_findtime: '10m'
fail2ban__jail_wordpress_login_maxretry: 5
fail2ban__jails__host_var:
  - filename: 'z10-apache-dos'
    state: 'present'
    template: 'apache-dos'
  - filename: 'z10-wordpress-login'
    state: 'present'
    template: 'wordpress-login'
  - filename: 'z20-custom-apache-dos'
    state: 'present'
    template: 'raw'
    raw: |-
      [apache-dos]
      maxretry = 1200
fail2ban__jails_apache_enabled: true
fail2ban__service_enabled: true
fail2ban__service_state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
