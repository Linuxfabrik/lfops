# Ansible Role linuxfabrik.lfops.freeipa_client

This role installs and configures [FreeIPA](https://www.freeipa.org/) as a client.


## Mandatory Requirements

* Install the [ansible-freeipa Ansible Collection](https://github.com/freeipa/ansible-freeipa) on the Ansible control node. This can be done by calling `ansible-galaxy collection install freeipa.ansible_freeipa`.


## Tags

| Tag              | What it does                                |
| ---              | ------------                                |
| `freeipa_client` | Installs and configures FreeIPA as a client |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `freeipa_client__create_home_dir` | Defines if PAM will be configured to create a users home directory if it does not exist. | `true` |
| `freeipa_client__ipa_admin_user` | The IPA admin user / Kerberos admin principal. | `{'username': 'admin', 'password': freeipa_server__ipa_admin_password}` |

Example:
```yaml
# optional
freeipa_client__create_home_dir: true
freeipa_client__ipa_admin_user:
  username: 'admin'
  password: 'linuxfabrik'
```

## Troubleshooting

`msg: Unable to discover domain, not provided on command line`: Check your DNS server configuration - `IN SOA` and `IN NS` options, as well as a correct `_ldap._tcp IN SRV 10 10 389 freeipa-server.example.com.` in your forward zone.

`Joining realm failed: JSON-RPC call failed: Couldn't connect to server`: Check firewall settings, perhaps a port like LDAP or HTTPS is blocked.

`msg: krb5.keytab missing! Retry with ipaclient_force_join=yes to generate a new one`, re-join an unprovisioned host: `ansible-playbook ... --extra-vars='ipaclient_force_join=true'`

`IPA client already installed with a conflicting domain`: Follow [Manually Unconfiguring Client Machines](https://access.redhat.com/documentation/de-de/red_hat_enterprise_linux/6/html/identity_management_guide/manually-unconfig-machines)


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
