# Ansible Role linuxfabrik.lfops.firewall

This role configures a firewall on the system. For the currently supported firewalls, see the options for the `firewall__firewall` variable below.

Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Ubuntu 16

## Mandatory Requirements

* When using `firewall__firewall == fwbuilder`, you need to manually deploy a Firewall Builder file to `/etc/fwb.sh`.


## Optional Requirements

* When using `firewall__firewall == iptables`, you can place an iptables config file in your inventory, which will be deployed to the system. The file has to be placed into `{{ inventory_dir }}/host_files/{{ inventory_hostname }}/etc/sysconfig/iptables`.


## Tags

| Tag        | What it does                        |
| ---        | ------------                        |
| `firewall` | Configures a firewall on the system |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `firewall__firewall` | Which firewall should be activated and configured. All other firewalls will be disabled. Possible options:<br> * `'None'`<br> * `'firewalld'`<br> * `'fwbuilder'`<br> * `'iptables'`<br> * `'nftables'`<br> * `'ufw'` | `'fwbuilder'` |

Example:
```yaml
# optional
firewall__firewall: 'fwbuilder'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
