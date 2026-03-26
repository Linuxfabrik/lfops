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

| Tag              | What it does                    | Reload / Restart |
| ---              | ------------                    | ---------------- |
| `freeipa_server` | Installs and configures FreeIPA as a server | - |
| `freeipa_server:configure` | Manages all FreeIPA resources (everything except installation) | - |
| `freeipa_server:group` | Manages FreeIPA groups | - |
| `freeipa_server:hbacrule` | Manages FreeIPA HBAC rules | - |
| `freeipa_server:hostgroup` | Manages FreeIPA host groups | - |
| `freeipa_server:pwpolicy` | Manages FreeIPA password policies | - |
| `freeipa_server:sudocmd` | Manages FreeIPA sudo commands and sudo command groups | - |
| `freeipa_server:sudorule` | Manages FreeIPA sudo rules | - |
| `freeipa_server:systemd_override` | Deploys `/etc/systemd/system/pki-tomcatd@.service.d/override.conf` | - |
| `freeipa_server:user` | Manages FreeIPA users and their group memberships | - |


## Mandatory Role Variables

| Variable                     | Description                                                                          |
| --------                     | -----------                                                                          |
| `freeipa_server__directory_manager_password` | The password for the Directory Manager. This is the superuser that needs to be used to perform rare low level tasks. |
| `freeipa_server__ipa_admin_password` | The password for the FreeIPA admin. This user is a regular system account used for IPA server administration. Set this in the `group_vars` so that the `linuxfabrik.lfops.freeipa_client` role can use it. |

Example:
```yaml
# mandatory
freeipa_server__directory_manager_password: 'linuxfabrik'
freeipa_server__ipa_admin_password: 'linuxfabrik'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `freeipa_server__config_default_shell` | The default shell for the users in FreeIPA. | `'/bin/bash'` |
| `freeipa_server__config_password_expiration_notification` | When the password expiration notification for FreeIPA users should be sent, in days. | `10` |
| `freeipa_server__domain` | The primary DNS domain. Typically this should be the domain part of FQDN of the server. | `'{{ ansible_facts["domain"] \| lower }}'` |
| `freeipa_server__groups__host_var` / `freeipa_server__groups__group_var` | List of dictionaries of FreeIPA groups to manage. Subkeys: <ul><li>`name`: Mandatory, string. Name of the group.</li><li>`description`: Optional, string. Group description.</li><li>`gidnumber`: Optional, integer. GID number.</li><li>`nonposix`: Optional, boolean. Create as a non-POSIX group.</li><li>`external`: Optional, boolean. Allow external non-IPA members.</li><li>`state`: Optional, string. `present` or `absent`. Defaults to `present`.</li></ul> | `[]` |
| `freeipa_server__hbacrules__host_var` / `freeipa_server__hbacrules__group_var` | List of dictionaries of FreeIPA HBAC rules to manage. Subkeys: <ul><li>`name`: Mandatory, string. Name of the HBAC rule.</li><li>`description`: Optional, string. Rule description.</li><li>`usercategory`: Optional, string. User category (`all`).</li><li>`hostcategory`: Optional, string. Host category (`all`).</li><li>`servicecategory`: Optional, string. Service category (`all`).</li><li>`users`: Optional, list. List of user names.</li><li>`groups`: Optional, list. List of group names.</li><li>`hosts`: Optional, list. List of host names.</li><li>`hostgroups`: Optional, list. List of host group names.</li><li>`hbacsvcs`: Optional, list. List of HBAC service names.</li><li>`hbacsvcgroups`: Optional, list. List of HBAC service group names.</li><li>`state`: Optional, string. `enabled`, `disabled` or `absent`. Defaults to `enabled`.</li></ul> | `[]` |
| `freeipa_server__hostgroups__host_var` / `freeipa_server__hostgroups__group_var` | List of dictionaries of FreeIPA host groups to manage. Subkeys: <ul><li>`name`: Mandatory, string. Name of the host group.</li><li>`description`: Optional, string. Host group description.</li><li>`hosts`: Optional, list. List of host names to add as members.</li><li>`hostgroups`: Optional, list. List of host group names to add as members.</li><li>`state`: Optional, string. `present` or `absent`. Defaults to `present`.</li></ul> | `[]` |
| `freeipa_server__ipa_admin_principal` | The Kerberos principal used for IPA admin authentication. | `'admin'` |
| `freeipa_server__pwpolicies__host_var` / `freeipa_server__pwpolicies__group_var` | List of dictionaries of FreeIPA password policies to manage. Subkeys: <ul><li>`name`: Mandatory, string. Name of the group the policy applies to.</li><li>`maxlife`: Optional, integer. Maximum password lifetime in days.</li><li>`minlife`: Optional, integer. Minimum password lifetime in hours.</li><li>`history`: Optional, integer. Password history size.</li><li>`minclasses`: Optional, integer. Minimum number of character classes.</li><li>`minlength`: Optional, integer. Minimum password length.</li><li>`maxfail`: Optional, integer. Maximum number of consecutive failures before lockout.</li><li>`failinterval`: Optional, integer. Period (in seconds) after which failure count is reset.</li><li>`lockouttime`: Optional, integer. Period (in seconds) for which account is locked.</li><li>`priority`: Optional, integer. Policy priority (lower value = higher priority).</li><li>`state`: Optional, string. `present` or `absent`. Defaults to `present`.</li></ul> | `[]` |
| `freeipa_server__realm` | The kerberos protocol requires a Realm name to be defined. This is typically the domain name converted to uppercase. | `'{{ ansible_facts["domain"] \| upper }}'` |
| `freeipa_server__sudocmdgroups__host_var` / `freeipa_server__sudocmdgroups__group_var` | List of dictionaries of FreeIPA sudo command groups to manage. Subkeys: <ul><li>`name`: Mandatory, string. Name of the sudo command group.</li><li>`description`: Optional, string. Command group description.</li><li>`sudocmds`: Optional, list. List of sudo command names to add as members.</li><li>`state`: Optional, string. `present` or `absent`. Defaults to `present`.</li></ul> | `[]` |
| `freeipa_server__sudocmds__host_var` / `freeipa_server__sudocmds__group_var` | List of dictionaries of FreeIPA sudo commands to manage. Subkeys: <ul><li>`name`: Mandatory, string. Command (e.g. `/usr/bin/less`).</li><li>`description`: Optional, string. Command description.</li><li>`state`: Optional, string. `present` or `absent`. Defaults to `present`.</li></ul> | `[]` |
| `freeipa_server__sudorules__host_var` / `freeipa_server__sudorules__group_var` | List of dictionaries of FreeIPA sudo rules to manage. Subkeys: <ul><li>`name`: Mandatory, string. Name of the sudo rule.</li><li>`description`: Optional, string. Rule description.</li><li>`usercategory`: Optional, string. User category (`all`).</li><li>`hostcategory`: Optional, string. Host category (`all`).</li><li>`cmdcategory`: Optional, string. Command category (`all`).</li><li>`runasusercategory`: Optional, string. RunAs user category (`all`).</li><li>`runasgroupcategory`: Optional, string. RunAs group category (`all`).</li><li>`users`: Optional, list. List of user names.</li><li>`groups`: Optional, list. List of group names.</li><li>`hosts`: Optional, list. List of host names.</li><li>`hostgroups`: Optional, list. List of host group names.</li><li>`cmds`: Optional, list. List of sudo command names.</li><li>`cmdgroups`: Optional, list. List of sudo command group names.</li><li>`runasusers`: Optional, list. List of RunAs user names.</li><li>`runasgroups`: Optional, list. List of RunAs group names.</li><li>`options`: Optional, list. List of sudo options (e.g. `!authenticate`).</li><li>`order`: Optional, integer. Sudo rule order.</li><li>`state`: Optional, string. `enabled`, `disabled` or `absent`. Defaults to `enabled`.</li></ul> | `[]` |
| `freeipa_server__users__host_var` / `freeipa_server__users__group_var` | List of dictionaries of FreeIPA users to manage. Subkeys: <ul><li>`name`: Mandatory, string. Login name.</li><li>`first`: Mandatory (for creation), string. First name.</li><li>`last`: Mandatory (for creation), string. Last name.</li><li>`password`: Optional, string. User password.</li><li>`email`: Optional, list. List of email addresses.</li><li>`shell`: Optional, string. Login shell.</li><li>`sshpubkey`: Optional, list. List of SSH public keys.</li><li>`groups`: Optional, list. List of group names the user should be a member of.</li><li>`update_password`: Optional, string. `on_create` or `always`. Defaults to `on_create`.</li><li>`state`: Optional, string. `present` or `absent`. Defaults to `present`.</li></ul> | `[]` |

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
