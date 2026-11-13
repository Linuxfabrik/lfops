# Ansible Role linuxfabrik.lfops.firewall

This role configures a firewall on the system. For the currently supported firewalls, see the options for the `firewall__firewall` variable below.


*Available since LFOps `2.0.0`.*


## Requirements

Manual steps:

* When using `firewall__firewall == fwbuilder`, either manually deploy a Firewall Builder file to `/etc/fwb.sh` or use the ``firewall__fwbuilder_repo_url`` variable to clone the Firewall Builder files automatically. Without either, or if the repository has no compiled file for the host, the run aborts before the role stops any firewall.
* When using `firewall__firewall == iptables` or `firewall__firewall == nftables`, set the ruleset in `firewall__iptables_ruleset` or `firewall__nftables_ruleset`. Without it, the run aborts before the role stops any firewall.


## Tags

`firewall`

* Configures a firewall on the system.
* Triggers: Stops and masks firewalld.service, fwb.service, iptables.service, nftables.service, ufw.service. Starts and unmasks the firewall which is defined in `firewall__firewall`.

`firewall:deploy_fwb_sh`

* Deploys the `/etc/fwb.sh` file for Firewall Builder.
* Triggers: fwb.service restart.

`firewall:firewalld`

* Manages firewalld.
* Triggers: firewalld.service reload.


## Optional Role Variables

`firewall__firewall`

* Which firewall should be activated and configured. All other firewalls will be disabled. Possible options: `'None'`, `'firewalld'`, `'fwbuilder'`, `'iptables'`, `'nftables'`, `'ufw'`.
* Type: String.
* Default: `'fwbuilder'`

`firewall__firewalld_ports__group_var` / `firewall__firewalld_ports__host_var`

* List of dictionaries defining the FirewallD ports.
* Type: List of dictionaries.
* Default: `[]`

* Subkeys:

    * `port`:

        * Mandatory. Port or port range.
        * Type: String.

    * `state`:

        * Optional. State of the port. Either `enabled` or `disabled`.
        * Type: String.
        * Default: `'enabled'`

`firewall__firewalld_services__group_var` / `firewall__firewalld_services__host_var`

* List of dictionaries defining the FirewallD services.
* Type: List of dictionaries.
* Default: `[]`

* Subkeys:

    * `service`:

        * Mandatory. Name of the service.
        * Type: String.

    * `state`:

        * Optional. State of the service. Either `enabled` or `disabled`.
        * Type: String.
        * Default: `'enabled'`

`firewall__fwbuilder_fw_file`

* The name of the Firewall Builder file which will be created when compiling the firewall in Firewall Builder, without the `.fw` extension. Needed if ``firewall__fwbuilder_repo_url`` is used and if the Firewall name within Firewall Builder differs from ``{{ inventory_hostname }}``.
* Type: String.
* Default: `'{{ inventory_hostname }}'`

`firewall__fwbuilder_repo_url`

* The GIT repository URL to clone the compiled firewall files from.
* Type: String.
* Default: unset

`firewall__iptables_ruleset`

* The iptables ruleset in `iptables-save` format, deployed to `/etc/sysconfig/iptables`. Mandatory if `firewall__firewall` is `'iptables'`. The role checks it with `iptables-restore --test` before it replaces the file, and restarts `iptables.service` after a change.
* Type: String.
* Default: unset

`firewall__nftables_ruleset`

* The nftables ruleset, deployed to the file `nftables.service` loads: `/etc/sysconfig/nftables.conf` on the Red Hat family, `/etc/nftables.conf` on Debian and Ubuntu. Mandatory if `firewall__firewall` is `'nftables'`. The role checks it with `nft --check` before it replaces the file, and restarts `nftables.service` after a change.
* Type: String.
* Default: unset

Example:
```yaml
# optional
firewall__firewall: 'fwbuilder'
firewall__firewalld_ports__group_var: []
firewall__firewalld_ports__host_var:
  - port: '1234/tcp'
    state: 'enabled'
firewall__firewalld_services__group_var: []
firewall__firewalld_services__host_var:
  - service: 'ssh'
    state: 'enabled'
firewall__fwbuilder_fw_file: 'example'
firewall__fwbuilder_repo_url: 'git@git.example.com:fwbuilder/fwb.git'
# from a file in the inventory
firewall__iptables_ruleset: '{{ lookup("ansible.builtin.file",
    inventory_dir ~ "/host_files/" ~ inventory_hostname ~ "/etc/sysconfig/iptables")
  }}'
firewall__nftables_ruleset: |-
  flush ruleset
  table inet filter {
      chain input {
          type filter hook input priority filter; policy drop;
          ct state established,related accept
          iif "lo" accept
          meta l4proto { icmp, ipv6-icmp } accept
          tcp dport 22 accept
      }
  }
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
