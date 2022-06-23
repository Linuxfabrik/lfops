# Ansible Role firewall

This role configures a firewall on the system. For the currently supported firewalls, see the options for the `firewall__firewall` variable below.

FQCN: linuxfabrik.lfops.firewall

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

IMPORTANT:
* When using `firewall__firewall == fwbuilder`, you need to deploy a Firewall Builder file to `/etc/fwb.sh` **before** running this role.


### Optional

* When using `firewall__firewall == iptables`, you can place an iptables config file in your inventory, which will be deployed to the system. The file has to be placed into `{{ inventory_dir }}/host_files/{{ inventory_hostname }}/etc/sysconfig/iptables`.


## Tags

| Tag      | What it does                        |
| ---      | ------------                        |
| firewall | Configures a firewall on the system |


## Role Variables

This role does not have any variable defaults.


### Mandatory

#### firewall__firewall

Which firewall should be activated and optionally configured. All other firewalls will be disabled. Possible options:

* `None`
* `firewalld`
* `fwbuilder`
* `iptables`
* `nftables`
* `ufw`


### Optional

This role does not have any optional variables.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
