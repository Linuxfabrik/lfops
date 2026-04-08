# Ansible Role linuxfabrik.lfops.freeipa_server

This role installs and configures [FreeIPA](https://www.freeipa.org/) as a server.

Ideally, the FreeIPA should be installed on a separate server. If that is not possible, you could group it with DNS and NTP on an infrastructure server. As a last resort you can install it on the central firewall / gateway server.


## Mandatory Requirements

* At least 2 GB RAM are required.
* The IPA installer is quite picky about the DNS configuration. The following checks are done by installer:

    * The hostname cannot be `localhost` or `localhost6`.
    * The hostname must be fully-qualified (`server.ipa.test`). Use two-level domain names. Otherwise you'll get error messages like `Invalid realm name: single label realms are not supported`.
    * The hostname must be resolvable.
    * The reverse lookup of the FreeIPA IP server address must match the hostname of the FreeIPA server. Otherwise you'll get error messages like `In unattended mode you need to provide at least -r, -p and -a options` or `The host name "ipa.example" does not match the value "myipa" obtained by reverse lookup on IP address 192.102.0.106`.
    * If neither the domain nor the realm being set, you'll get error messages like `In unattended mode you need to provide at least -r, -p and -a options`.

* Do not use an existing domain or hostname unless you own the domain. It's a common mistake to use `example.com`. We recommend to use a reserved top level domain from RFC2606 for private test installations, e.g. `ipa.test`.
* Install the [ansible-freeipa Ansible Collection](https://github.com/freeipa/ansible-freeipa) on the Ansible control node. This can be done by calling `ansible-galaxy collection install freeipa.ansible_freeipa`.


## Tags

`freeipa_server`

* Installs and configures FreeIPA as a server.
* Triggers: none.

`freeipa_server:configure`

* Manages all FreeIPA resources (everything except installation).
* Triggers: none.

`freeipa_server:group`

* Manages FreeIPA groups.
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

`freeipa_server:sudocmd`

* Manages FreeIPA sudo commands and sudo command groups.
* Triggers: none.

`freeipa_server:sudorule`

* Manages FreeIPA sudo rules.
* Triggers: none.

`freeipa_server:systemd_override`

* Deploys `/etc/systemd/system/pki-tomcatd@.service.d/override.conf`.
* Triggers: none.

`freeipa_server:user`

* Manages FreeIPA users and their group memberships.
* Triggers: none.


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

    * `cmds`:

        * Optional. List of sudo command names.
        * Type: List.

    * `cmdgroups`:

        * Optional. List of sudo command group names.
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

* The `TimeoutStartSec` value for the `pki-tomcatd@.service` systemd override.
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
freeipa_server__hostgroups__host_var:
  - name: 'webservers'
    description: 'Web server hosts'
    hosts:
      - 'web01.example.com'
      - 'web02.example.com'
freeipa_server__ipa_admin_principal: 'admin'
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
    cmdgroups:
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


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
