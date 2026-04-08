# Ansible Role linuxfabrik.lfops.firewall

This role configures a firewall on the system. For the currently supported firewalls, see the options for the `firewall__firewall` variable below.


## Mandatory Requirements

* When using `firewall__firewall == fwbuilder`, you either need to manually deploy a Firewall Builder file to `/etc/fwb.sh` or use the ``firewall__fwbuilder_repo_url`` variable to clone the Firewall Builder files automatically.


## Optional Requirements

* When using `firewall__firewall == iptables`, you can place an iptables config file in your inventory, which will be deployed to the system. The file has to be placed into `{{ inventory_dir }}/host_files/{{ inventory_hostname }}/etc/sysconfig/iptables`.


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

* The name of the Firewall Builder file which will be created when compiling the firewall in Firewall Builder. Needed if ``firewall__fwbuilder_repo_url`` is used and if the Firewall name within Firewall Builder differs from ``{{ inventory_hostname }}``.
* Type: String.
* Default: `'{{ inventory_hostname }}'`

`firewall__fwbuilder_repo_url`

* The GIT repository URL to clone the compiled firewall files from.
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
firewall__fwbuilder_fw_file: 'example.fw'
firewall__fwbuilder_repo_url: 'git@git.example.com:fwbuilder/fwb.git'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
