# Ansible Role linuxfabrik.lfops.freeipa_server

This role installs and configures [FreeIPA](https://www.freeipa.org/) as a server.

Ideally, the FreeIPA should be installed on a separate server. If that is not possible, you could group it with DNS and NTP on an infrastructure server. As a last resort you can install it on the central firewall / gateway server.


*Available since LFOps `2.0.0`.*


## Known Limitations

* The role must be run with Ansible's `linear` strategy (the default). It is incompatible with strategies that reuse the target Python interpreter, such as Mitogen's `mitogen_linear`, because the underlying ansible-freeipa modules use `ipalib`'s global API singleton and fail with `API.bootstrap() already called` on the second module call. The bundled `playbooks/freeipa_server.yml` sets `strategy: 'linear'` explicitly.


## Requirements

* At least 2 GB RAM are required.
* The IPA installer is quite picky about the DNS configuration. The following checks are done by the installer:

    * The hostname cannot be `localhost` or `localhost6`.
    * The hostname must be fully-qualified (`server.ipa.test`). Use two-level domain names. Otherwise you'll get error messages like `Invalid realm name: single label realms are not supported`.
    * The hostname must be resolvable.
    * The reverse lookup of the FreeIPA IP server address must match the hostname of the FreeIPA server. Otherwise you'll get error messages like `In unattended mode you need to provide at least -r, -p and -a options` or `The host name "ipa.example" does not match the value "myipa" obtained by reverse lookup on IP address 192.102.0.106`.
    * If neither the domain nor the realm being set, you'll get error messages like `In unattended mode you need to provide at least -r, -p and -a options`.

* The role does not set up the DNS integrated into FreeIPA (`ipa-server-dns`). The DNS server of the domain therefore needs the records FreeIPA would otherwise maintain itself, for every FreeIPA server (`ipaserver/dns_data_management.py` in FreeIPA):

    * The Kerberos SRV and URI records, which clients use to find a KDC and to fail over to another one (`ipa-client-install` sets `dns_lookup_kdc = true`), and the `_kerberos` TXT record with the realm.
    * `_ldap._tcp`, for clients and replicas that look up the LDAP servers.
    * `ipa-ca` with the address of every server with the CA role. Every certificate FreeIPA issues names `http://ipa-ca.<domain>/` for OCSP and the CRL, so without it, clients cannot check whether a certificate was revoked.

    For a server `ipa01.example.com` in the realm `EXAMPLE.COM`, e.g. with the `bind` role:

    ```text
    _kerberos              IN TXT  "EXAMPLE.COM"
    _kerberos              IN URI  0 100 "krb5srv:m:tcp:ipa01.example.com."
    _kerberos              IN URI  0 100 "krb5srv:m:udp:ipa01.example.com."
    _kerberos-master._tcp  IN SRV  0 100 88  ipa01.example.com.
    _kerberos-master._udp  IN SRV  0 100 88  ipa01.example.com.
    _kerberos._tcp         IN SRV  0 100 88  ipa01.example.com.
    _kerberos._udp         IN SRV  0 100 88  ipa01.example.com.
    _kpasswd               IN URI  0 100 "krb5srv:m:tcp:ipa01.example.com."
    _kpasswd               IN URI  0 100 "krb5srv:m:udp:ipa01.example.com."
    _kpasswd._tcp          IN SRV  0 100 464 ipa01.example.com.
    _kpasswd._udp          IN SRV  0 100 464 ipa01.example.com.
    _ldap._tcp             IN SRV  0 100 389 ipa01.example.com.
    ipa-ca                 IN A    192.0.2.10
    ipa01                  IN A    192.0.2.10
    ```

    `ipa dns-update-system-records --dry-run` (after `kinit admin`) lists the records for the actual servers, and `ipa-healthcheck` reports every missing one (`IPADNSSystemRecordsCheck`).

* Clients and replicas reach the FreeIPA server on TCP 80 and 443 (HTTP/HTTPS), 389 and 636 (LDAP/LDAPS), 88 and 464 (Kerberos) and UDP 88 and 464 (Kerberos), as `ipa-server-install` lists them. TCP 80 is easily overlooked: `ipa-client-install` fetches the CA certificate over HTTP, and every certificate FreeIPA issues points to OCSP (`http://ipa-ca.<domain>/ca/ocsp`) and the CRL (`http://ipa-ca.<domain>/ipa/crl/MasterCRL.bin`) over HTTP. Port 53 is only needed with the DNS integrated into FreeIPA, and UDP 123 only for NTP, which the role does not set up in FreeIPA (`ipaclient_no_ntp`).

* Do not use an existing domain or hostname unless you own the domain. It's a common mistake to use `example.com`. We recommend to use a reserved top level domain from RFC2606 for private test installations, e.g. `ipa.test`.

Manual steps:

* Install the [ansible-freeipa Ansible Collection](https://github.com/freeipa/ansible-freeipa) on the Ansible control node by calling `ansible-galaxy collection install freeipa.ansible_freeipa`.


## Tags

`freeipa_server`

* Installs and configures FreeIPA as a server.
* Installs and configures `ipa-healthcheck` and runs it daily through `ipa-healthcheck.timer`, and once right away while there is no report yet.
* Triggers: none.

`freeipa_server:configure`

* Manages all FreeIPA resources (everything except installation).
* Triggers: none.

`freeipa_server:group`

* Manages FreeIPA groups.
* Triggers: none.

`freeipa_server:healthcheck`

* Installs `ipa-healthcheck`, deploys `/etc/ipahealthcheck/ipahealthcheck.conf` and `/etc/systemd/system/ipa-healthcheck.timer.d/z00-linuxfabrik.conf`, and ensures `ipa-healthcheck.timer` is in the desired state.
* Runs the healthcheck once if `/var/log/ipa/healthcheck/healthcheck.log` does not exist yet, so the monitoring has a report before the timer first runs.
* Triggers: none.

`freeipa_server:hbacrule`

* Manages FreeIPA HBAC rules.
* Triggers: none.

`freeipa_server:hostgroup`

* Manages FreeIPA host groups.
* Triggers: none.

`freeipa_server:pwpolicy`

* Manages FreeIPA password policies.
* Triggers: none.

`freeipa_server:state`

* Manages the state of `ipa-healthcheck.timer` (start, stop, enable, disable).
* Triggers: none.

`freeipa_server:sudocmd`

* Manages FreeIPA sudo commands and sudo command groups.
* Triggers: none.

`freeipa_server:sudorule`

* Manages FreeIPA sudo rules.
* Triggers: none.

`freeipa_server:systemd_override`

* Deploys `/etc/systemd/system/pki-tomcatd@.service.d/override.conf` and sets the matching `startup_timeout` in `/etc/ipa/default.conf`.
* Triggers: `systemctl daemon-reload`.

`freeipa_server:users`

* Manages FreeIPA users and their group memberships.
* Triggers: none.

Tip:

To manage a single resource (or a few) instead of all of them, supplement the matching tag with the corresponding `freeipa_server__limit_*` extra variable, e.g. `--tags freeipa_server:users --extra-vars='freeipa_server__limit_users=["jdoe"]'`. See [Optional Role Variables](https://github.com/Linuxfabrik/lfops/tree/main/roles/freeipa_server#optional-role-variables).


## Mandatory Role Variables

`freeipa_server__directory_manager_password`

* The password for the Directory Manager. This is the superuser that needs to be used to perform rare low level tasks.
* Type: String.

`freeipa_server__ipa_admin_password`

* The password for the FreeIPA admin. This user is a regular system account used for IPA server administration. Set this in the `group_vars` so that the `linuxfabrik.lfops.freeipa_client` role can use it.
* Type: String.

Example:
```yaml
# mandatory
freeipa_server__directory_manager_password: 'linuxfabrik'
freeipa_server__ipa_admin_password: 'linuxfabrik'
```


## Optional Role Variables

`freeipa_server__config_default_shell`

* The default shell for the users in FreeIPA.
* Type: String.
* Default: `'/bin/bash'`

`freeipa_server__config_password_expiration_notification`

* When the password expiration notification for FreeIPA users should be sent, in days.
* Type: Number.
* Default: `10`

`freeipa_server__domain`

* The primary DNS domain. Typically this should be the domain part of FQDN of the server.
* Type: String.
* Default: `'{{ ansible_facts["domain"] | lower }}'`

`freeipa_server__groups__host_var` / `freeipa_server__groups__group_var`

* FreeIPA groups to manage.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the group.
        * Type: String.

    * `description`:

        * Optional. Group description.
        * Type: String.

    * `gidnumber`:

        * Optional. GID number.
        * Type: Number.

    * `nonposix`:

        * Optional. Create as a non-POSIX group.
        * Type: Bool.

    * `external`:

        * Optional. Allow external non-IPA members.
        * Type: Bool.

    * `state`:

        * Optional. `present` or `absent`. Defaults to `present`.
        * Type: String.

`freeipa_server__hbacrules__host_var` / `freeipa_server__hbacrules__group_var`

* FreeIPA HBAC rules to manage.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the HBAC rule.
        * Type: String.

    * `description`:

        * Optional. Rule description.
        * Type: String.

    * `usercategory`:

        * Optional. User category (`all`).
        * Type: String.

    * `hostcategory`:

        * Optional. Host category (`all`).
        * Type: String.

    * `servicecategory`:

        * Optional. Service category (`all`).
        * Type: String.

    * `users`:

        * Optional. List of user names.
        * Type: List.

    * `groups`:

        * Optional. List of group names.
        * Type: List.

    * `hosts`:

        * Optional. List of host names.
        * Type: List.

    * `hostgroups`:

        * Optional. List of host group names.
        * Type: List.

    * `hbacsvcs`:

        * Optional. List of HBAC service names.
        * Type: List.

    * `hbacsvcgroups`:

        * Optional. List of HBAC service group names.
        * Type: List.

    * `state`:

        * Optional. `enabled`, `disabled` or `absent`. Defaults to `enabled`.
        * Type: String.

`freeipa_server__healthcheck_cert_expiration_days`

* How many days before a certificate expires `ipa-healthcheck` starts to warn about it.
* Type: Number.
* Default: `28`

`freeipa_server__healthcheck_excludes__host_var` / `freeipa_server__healthcheck_excludes__group_var`

* Results that `ipa-healthcheck` leaves out of its report, written to the `[excludes]` section of `/etc/ipahealthcheck/ipahealthcheck.conf`. Excluding a source or a check keeps it from running at all, excluding a key only filters that result from the report. `ipa-healthcheck` does not flag a source, check or key that does not exist.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `type`:

        * Mandatory. What to exclude. One of `source` (e.g. `ipahealthcheck.ipa.certs`), `check` (e.g. `IPADNSSystemRecordsCheck`) or `key` (a result key from the report, e.g. a certmonger tracking ID).
        * Type: String.

    * `value`:

        * Mandatory. The name of the source or check, or the result key. Together with `type`, it identifies the entry.
        * Type: String.

    * `comment`:

        * Optional. Why the result is excluded, written as a comment above the entry.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`. Defaults to `present`.
        * Type: String.

`freeipa_server__healthcheck_on_calendar`

* When `ipa-healthcheck.timer` runs the healthcheck, in the calendar event format of `systemd.time(7)`. The report goes to `/var/log/ipa/healthcheck/healthcheck.log` (JSON, overwritten on each run, rotated daily by logrotate). The timer is persistent: a run missed while the host was down takes place right after the next boot, so the report does not grow older than a day plus the downtime.
* Type: String.
* Default: `'*-*-* 06:{{ 59 | random(seed=inventory_hostname ~ "ipa-healthcheck") }}'`
* Deviates from the upstream default `*-*-* 04:00:00`: the healthcheck runs at a fixed minute per host after the reboot window of the `schedule_reboot` role (04:xx), so the report reflects the server after a reboot, and the servers of a replicated FreeIPA domain do not all check at the same time. The seed differs from the one of `lynis__on_calendar`, so the two start in different minutes on most hosts.

`freeipa_server__healthcheck_timeout`

* How many seconds each check of `ipa-healthcheck` may take before it counts as an error.
* Type: Number.
* Default: `30`
* Deviates from the upstream default `10`: on a FreeIPA server with 2 vCPUs, `CASystemCertTrustFlagCheck` took longer than 10 seconds in a full run and was reported as an error, although it reports no problem when given the time (its source takes 11 to 12 seconds on its own).

`freeipa_server__healthcheck_timer_enabled`

* Enables or disables `ipa-healthcheck.timer`, analogous to `systemctl enable/disable`. With `false`, the role does not run the healthcheck once after the installation either.
* Type: Bool.
* Default: `true`
* Deviates from the package, which leaves the timer disabled: without a regular healthcheck, problems such as expiring certificates or broken replication go unnoticed until a service fails.

`freeipa_server__healthcheck_timer_state`

* Changes the state of `ipa-healthcheck.timer`, analogous to `systemctl start/stop/restart`.
* Type: String. One of `restarted`, `started`, `stopped`.
* Default: `'started'`

`freeipa_server__hostgroups__host_var` / `freeipa_server__hostgroups__group_var`

* FreeIPA host groups to manage.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the host group.
        * Type: String.

    * `description`:

        * Optional. Host group description.
        * Type: String.

    * `hosts`:

        * Optional. List of host names to add as members.
        * Type: List.

    * `hostgroups`:

        * Optional. List of host group names to add as members.
        * Type: List.

    * `state`:

        * Optional. `present` or `absent`. Defaults to `present`.
        * Type: String.

`freeipa_server__ipa_admin_principal`

* The Kerberos principal used for IPA admin authentication.
* Type: String.
* Default: `'admin'`

`freeipa_server__limit_groups` / `freeipa_server__limit_hbacrules` / `freeipa_server__limit_hostgroups` / `freeipa_server__limit_pwpolicies` / `freeipa_server__limit_sudocmdgroups` / `freeipa_server__limit_sudocmds` / `freeipa_server__limit_sudorules` / `freeipa_server__limit_users`

* Each checks if the `name` of a resource is in the list and only manages those. Can be used on the CLI to speed up the deployment by managing a single resource (or a few) instead of all of them, e.g. `--extra-vars='freeipa_server__limit_users=["jdoe"]'`. Combine with the matching tag, e.g. `--tags freeipa_server:users`.
* Type: List.
* Default: unset

`freeipa_server__pwpolicies__host_var` / `freeipa_server__pwpolicies__group_var`

* FreeIPA password policies to manage.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the group the policy applies to.
        * Type: String.

    * `maxlife`:

        * Optional. Maximum password lifetime in days.
        * Type: Number.

    * `minlife`:

        * Optional. Minimum password lifetime in hours.
        * Type: Number.

    * `history`:

        * Optional. Password history size.
        * Type: Number.

    * `minclasses`:

        * Optional. Minimum number of character classes.
        * Type: Number.

    * `minlength`:

        * Optional. Minimum password length.
        * Type: Number.

    * `maxfail`:

        * Optional. Maximum number of consecutive failures before lockout.
        * Type: Number.

    * `failinterval`:

        * Optional. Period (in seconds) after which failure count is reset.
        * Type: Number.

    * `lockouttime`:

        * Optional. Period (in seconds) for which account is locked.
        * Type: Number.

    * `priority`:

        * Optional. Policy priority (lower value = higher priority).
        * Type: Number.

    * `state`:

        * Optional. `present` or `absent`. Defaults to `present`.
        * Type: String.

`freeipa_server__realm`

* The kerberos protocol requires a Realm name to be defined. This is typically the domain name converted to uppercase.
* Type: String.
* Default: `'{{ ansible_facts["domain"] | upper }}'`

`freeipa_server__sudocmdgroups__host_var` / `freeipa_server__sudocmdgroups__group_var`

* FreeIPA sudo command groups to manage.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the sudo command group.
        * Type: String.

    * `description`:

        * Optional. Command group description.
        * Type: String.

    * `sudocmds`:

        * Optional. List of sudo command names to add as members.
        * Type: List.

    * `state`:

        * Optional. `present` or `absent`. Defaults to `present`.
        * Type: String.

`freeipa_server__sudocmds__host_var` / `freeipa_server__sudocmds__group_var`

* FreeIPA sudo commands to manage.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Command (e.g. `/usr/bin/less`).
        * Type: String.

    * `description`:

        * Optional. Command description.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`. Defaults to `present`.
        * Type: String.

`freeipa_server__sudorules__host_var` / `freeipa_server__sudorules__group_var`

* FreeIPA sudo rules to manage.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the sudo rule.
        * Type: String.

    * `description`:

        * Optional. Rule description.
        * Type: String.

    * `usercategory`:

        * Optional. User category (`all`).
        * Type: String.

    * `hostcategory`:

        * Optional. Host category (`all`).
        * Type: String.

    * `cmdcategory`:

        * Optional. Command category (`all`).
        * Type: String.

    * `runasusercategory`:

        * Optional. RunAs user category (`all`).
        * Type: String.

    * `runasgroupcategory`:

        * Optional. RunAs group category (`all`).
        * Type: String.

    * `users`:

        * Optional. List of user names.
        * Type: List.

    * `groups`:

        * Optional. List of group names.
        * Type: List.

    * `hosts`:

        * Optional. List of host names.
        * Type: List.

    * `hostgroups`:

        * Optional. List of host group names.
        * Type: List.

    * `allow_sudocmds`:

        * Optional. List of sudo command names the rule allows.
        * Type: List.

    * `allow_sudocmdgroups`:

        * Optional. List of sudo command group names the rule allows.
        * Type: List.

    * `runasusers`:

        * Optional. List of RunAs user names.
        * Type: List.

    * `runasgroups`:

        * Optional. List of RunAs group names.
        * Type: List.

    * `options`:

        * Optional. List of sudo options (e.g. `!authenticate`).
        * Type: List.

    * `order`:

        * Optional. Sudo rule order.
        * Type: Number.

    * `state`:

        * Optional. `enabled`, `disabled` or `absent`. Defaults to `enabled`.
        * Type: String.

`freeipa_server__systemd_timeoutstartsec`

* The start-up timeout for `pki-tomcatd`, in seconds. Sets both `TimeoutStartSec` in the `pki-tomcatd@.service` systemd override and `startup_timeout` in `/etc/ipa/default.conf`, so that systemd and FreeIPA wait equally long for Dogtag to come up. Raise it on slow machines, where the FreeIPA built-in default of 90 seconds is not enough and `ipactl start` reports that the CA did not start.
* Type: Number.
* Default: `300`

`freeipa_server__users__host_var` / `freeipa_server__users__group_var`

* FreeIPA users to manage.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Login name.
        * Type: String.

    * `first`:

        * Mandatory (for creation). First name.
        * Type: String.

    * `last`:

        * Mandatory (for creation). Last name.
        * Type: String.

    * `password`:

        * Optional. User password.
        * Type: String.

    * `email`:

        * Optional. List of email addresses.
        * Type: List.

    * `shell`:

        * Optional. Login shell.
        * Type: String.

    * `sshpubkey`:

        * Optional. List of SSH public keys.
        * Type: List.

    * `groups`:

        * Optional. List of group names the user should be a member of.
        * Type: List.

    * `update_password`:

        * Optional. `on_create` or `always`. Defaults to `on_create`.
        * Type: String.

    * `state`:

        * Optional. `present` or `absent`. Defaults to `present`.
        * Type: String.

Example:
```yaml
# optional
freeipa_server__config_default_shell: '/bin/bash'
freeipa_server__config_password_expiration_notification: 10
freeipa_server__domain: 'example.com'
freeipa_server__groups__host_var:
  - name: 'developers'
    description: 'Development team'
  - name: 'old-group'
    state: 'absent'
freeipa_server__hbacrules__host_var:
  - name: 'allow_developers_webservers'
    users:
      - 'developer1'
    hostgroups:
      - 'webservers'
    hbacsvcs:
      - 'sshd'
    state: 'enabled'
freeipa_server__healthcheck_cert_expiration_days: 28
freeipa_server__healthcheck_excludes__host_var:
  - type: 'source'
    value: 'ipahealthcheck.ipa.dna'
    comment: 'no DNA ranges on this server'
  - type: 'key'
    value: '20210910141452'
    comment: 'customer certificate tracked by certmonger, unknown to IPA'
freeipa_server__healthcheck_on_calendar: '*-*-* 06:15'
freeipa_server__healthcheck_timeout: 30
freeipa_server__healthcheck_timer_enabled: true
freeipa_server__healthcheck_timer_state: 'started'
freeipa_server__hostgroups__host_var:
  - name: 'webservers'
    description: 'Web server hosts'
    hosts:
      - 'web01.example.com'
      - 'web02.example.com'
freeipa_server__ipa_admin_principal: 'admin'
freeipa_server__limit_users:
  - 'jdoe'
freeipa_server__pwpolicies__host_var:
  - name: 'developers'
    maxlife: 90
    minlife: 1
    minlength: 12
    minclasses: 3
    priority: 10
freeipa_server__realm: 'EXAMPLE.COM'
freeipa_server__sudocmdgroups__host_var:
  - name: 'network_cmds'
    description: 'Network commands'
    sudocmds:
      - '/usr/bin/ip'
      - '/usr/sbin/ss'
freeipa_server__sudocmds__host_var:
  - name: '/usr/bin/ip'
    description: 'IP command'
  - name: '/usr/sbin/ss'
    description: 'Socket statistics'
freeipa_server__sudorules__host_var:
  - name: 'allow_developers_network'
    groups:
      - 'developers'
    hostcategory: 'all'
    allow_sudocmdgroups:
      - 'network_cmds'
    options:
      - '!authenticate'
    state: 'enabled'
freeipa_server__systemd_timeoutstartsec: 300
freeipa_server__users__host_var:
  - name: 'jdoe'
    first: 'John'
    last: 'Doe'
    email:
      - 'jdoe@example.com'
    shell: '/bin/bash'
    sshpubkey:
      - 'ssh-ed25519 AAAAC3...'
    groups:
      - 'developers'
    update_password: 'on_create'
```


## Troubleshooting

**`Kerberos authentication failed: kinit: Cannot read password while getting initial credentials`**

* Raised by the `ipa*` resource management tasks (groups, users, HBAC rules, etc.) when the password of `freeipa_server__ipa_admin_principal` has expired, which the default FreeIPA password policy does after 90 days. The KDC rejects the authentication as expired, `kinit` switches to its password change dialog and asks for a new password, and the ansible-freeipa modules only hand it the old one, so the login aborts before a ticket is issued. Confirm it on the FreeIPA server with `kinit admin`, which reports `Password expired.  You must change it now.` before prompting. To fix it, log in to the FreeIPA Web UI with that principal, which asks for a new password right at login, or complete the `kinit` prompts on the server. Then set `freeipa_server__ipa_admin_password` to the new password and re-run the playbook.

**`Kerberos authentication failed: kinit: Configuration file does not specify default realm when parsing name admin`**

* Raised by the `ipa*` resource management tasks (groups, users, HBAC rules, etc.) after a previous run aborted partway through `ipaserver_setup_*`. The aborted run did not write `/etc/krb5.conf` and `/etc/ipa/default.conf` with a `default_realm`, and the next run's `ipaserver_setup_*` steps consider the install "already done" and skip. Verify on the target with `cat /etc/ipa/default.conf` and `grep default_realm /etc/krb5.conf`. Reset the partial install with `ipa-server-install --uninstall --unattended` and re-run the playbook. **Caution:** this wipes the LDAP backend; only run it on a host that has no production IPA data.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
