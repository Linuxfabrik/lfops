# Ansible Role linuxfabrik.lfops.freeipa_server

This role installs and configures [FreeIPA](https://www.freeipa.org/) as a server.

Runs on

* RHEL 8 (and compatible)

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

After running this role (and for now until implemented), run this as root:

```
authselect current
authselect select sssd with-sudo with-mkhomedir
authselect current
```


## Tags

| Tag              | What it does                    |
| ---              | ------------                    |
| `freeipa_server` | Installs and configures FreeIPA as a server |


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
| `freeipa_server__realm` | The kerberos protocol requires a Realm name to be defined. This is typically the domain name converted to uppercase. | `'{{ ansible_facts["domain"] \| upper }}'` |

Example:
```yaml
# optional
freeipa_server__config_default_shell: '/bin/bash'
freeipa_server__config_password_expiration_notification: 10
freeipa_server__domain: 'example.com'
freeipa_server__realm: 'EXAMPLE.COM'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
