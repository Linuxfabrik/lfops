# Ansible Role linuxfabrik.lfops.ad_integration

This role joins a host to an Active Directory domain. It is a thin wrapper around the [`fedora.linux_system_roles.ad_integration` role](https://github.com/linux-system-roles/ad_integration), the upstream Linux System Role that runs `realm join` and configures SSSD (or Winbind) for direct AD integration. Once joined, AD users can log in and AD groups can be used for access control and `sudo` rules.


*Available in the next LFOps release.*


## How the Role Behaves

* The role calls `fedora.linux_system_roles.ad_integration`, which by default joins the realm with `realm join` using `adcli` and configures `sssd` as the client software. The join credentials are read from `ad_integration__login`.
* Joining is not fully idempotent: on an already-joined host `realm` reports that the host is a member and the role makes no changes, but set `ad_integration__force_rejoin__host_var` to `true` to leave and re-join.
* The join credentials are passed in cleartext to `realm join`. Store them in Bitwarden and inject them via the `linuxfabrik.lfops.bitwarden_item` lookup rather than committing them to the inventory.
* This role only performs the domain join and SSSD configuration. It does NOT manage time synchronization, crypto policies, DNS, or networking. The upstream role's `manage_timesync`, `manage_crypto_policies`, and `manage_dns` features are intentionally not exposed; cover these prerequisites with the dedicated LFOps roles (see Requirements).


## Requirements

* An Active Directory account that is allowed to join computers to the domain.
* Time must be in sync with the Active Directory domain controllers (Kerberos tolerates only a small clock skew).
* DNS must resolve the AD domain and its `_ldap._tcp` / `_kerberos._tcp` SRV records.
* Red Hat 8 and newer disable RC4 out of the box. Enable AES encryption in Active Directory, or relax the crypto policy on the host.

Manual steps:

* Install the [Linux System Roles](https://linux-system-roles.github.io/) on the Ansible control node, for example by calling `ansible-galaxy collection install fedora.linux_system_roles`.
* Synchronize the clock by running the [linuxfabrik.lfops.chrony](https://github.com/Linuxfabrik/lfops/tree/main/roles/chrony) role.
* Point DNS at the AD domain controllers by running the [linuxfabrik.lfops.network](https://github.com/Linuxfabrik/lfops/tree/main/roles/network) role (or a local resolver such as [linuxfabrik.lfops.blocky](https://github.com/Linuxfabrik/lfops/tree/main/roles/blocky) / [linuxfabrik.lfops.bind](https://github.com/Linuxfabrik/lfops/tree/main/roles/bind)).
* Optional: relax the crypto policy by running the [linuxfabrik.lfops.crypto_policy](https://github.com/Linuxfabrik/lfops/tree/main/roles/crypto_policy) role when the domain still requires RC4.


## Tags

`ad_integration`

* Joins the host to the Active Directory domain and configures SSSD.
* Triggers: none.


## Mandatory Role Variables

`ad_integration__realm`

* The Active Directory realm (domain) name to join, for example `EXAMPLE.COM`.
* Type: String.

`ad_integration__login`

* Credentials of the Active Directory user used to join the domain. Integrates with the `linuxfabrik.lfops.bitwarden_item` lookup.
* Type: Dictionary.
* Subkeys:

    * `username`:

        * Mandatory. The Active Directory user used to join the domain.
        * Type: String.

    * `password`:

        * Mandatory. The password of that user.
        * Type: String.

Example:
```yaml
# mandatory
ad_integration__realm: 'EXAMPLE.COM'
ad_integration__login:
  username: 'Administrator'
  password: 'linuxfabrik'
```


## Optional Role Variables

`ad_integration__auto_id_mapping__host_var` / `ad_integration__auto_id_mapping__group_var`

* Generate UID/GID numbers automatically instead of reading them from the directory (RFC 2307).
* Type: Bool.
* Default: `true`

`ad_integration__client_software__host_var` / `ad_integration__client_software__group_var`

* Client software to use with Active Directory.
* Type: String. One of `sssd`, `winbind`.
* Default: `'sssd'`

`ad_integration__computer_ou__host_var` / `ad_integration__computer_ou__group_var`

* Distinguished name of the organizational unit in which to create the computer account. Relative to the Root DSE or a complete LDAP DN.
* Type: String.
* Default: `''`

`ad_integration__force_rejoin__host_var` / `ad_integration__force_rejoin__group_var`

* Leave the existing domain before performing the join.
* Type: Bool.
* Default: `false`

`ad_integration__join_parameters__host_var` / `ad_integration__join_parameters__group_var`

* Additional parameters appended to the `realm join` command, for example `--user-principal`.
* Type: String.
* Default: `''`

`ad_integration__join_to_dc__host_var` / `ad_integration__join_to_dc__group_var`

* Host name or IP address of the domain controller to join via directly.
* Type: String.
* Default: `''`

`ad_integration__membership_software__host_var` / `ad_integration__membership_software__group_var`

* Software used to join the realm.
* Type: String. One of `adcli`, `samba`.
* Default: `'adcli'`

`ad_integration__sssd_settings__host_var` / `ad_integration__sssd_settings__group_var`

* Settings to include in the `[sssd]` section of `sssd.conf`.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `key`:

        * Mandatory. The configuration name.
        * Type: String.

    * `value`:

        * Mandatory. The configuration value.
        * Type: String.

`ad_integration__sssd_custom_settings__host_var` / `ad_integration__sssd_custom_settings__group_var`

* Settings to include in the `[domain/<REALM>]` section of `sssd.conf`.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `key`:

        * Mandatory. The configuration name.
        * Type: String.

    * `value`:

        * Mandatory. The configuration value.
        * Type: String.

Example:
```yaml
# optional
ad_integration__auto_id_mapping__host_var: false
ad_integration__client_software__host_var: 'sssd'
ad_integration__computer_ou__host_var: 'OU=Linux,OU=Servers,DC=example,DC=com'
ad_integration__force_rejoin__host_var: false
ad_integration__join_parameters__host_var: '--user-principal=host/client.example.com@EXAMPLE.COM'
ad_integration__join_to_dc__host_var: 'dc01.example.com'
ad_integration__membership_software__host_var: 'adcli'
ad_integration__sssd_settings__host_var:
  - key: 'default_domain_suffix'
    value: 'example.com'
ad_integration__sssd_custom_settings__host_var:
  - key: 'ad_gpo_access_control'
    value: 'enforcing'
  - key: 'use_fully_qualified_names'
    value: 'false'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
