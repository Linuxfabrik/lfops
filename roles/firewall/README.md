# Ansible Role linuxfabrik.lfops.firewall

This role configures a firewall on the system. For the currently supported firewalls, see the options for the `firewall__firewall` variable below.


## Mandatory Requirements

* When using `firewall__firewall == fwbuilder`, you either need to manually deploy a Firewall Builder file to `/etc/fwb.sh` or use the ``firewall__fwbuilder_repo_url`` variable to clone the Firewall Builder files automatically.


## Optional Requirements

* When using `firewall__firewall == iptables`, you can place an iptables config file in your inventory, which will be deployed to the system. The file has to be placed into `{{ inventory_dir }}/host_files/{{ inventory_hostname }}/etc/sysconfig/iptables`.


## Tags

| Tag        | What it does                        |
| ---        | ------------                        |
| `firewall` | Configures a firewall on the system |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `firewall__firewall`           | Which firewall should be activated and configured. All other firewalls will be disabled. Possible options:<br> * `'None'`<br> * `'firewalld'`<br> * `'fwbuilder'`<br> * `'iptables'`<br> * `'nftables'`<br> * `'ufw'` | `'fwbuilder'` |
| `firewall__firewalld_ports__group_var` / <br> `firewall__firewalld_ports__host_var` | List of dictionaries defining the FirewallD ports. Subkeys: <ul><li>`port`: Mandatory, string. Port or port range.</li><li>`state`: Optional, string. State of the port. Either `enabled` or `disabled`. Defaults to `enabled.</li></ul> | `[]` |
| `firewall__firewalld_services__group_var` / <br> `firewall__firewalld_services__host_var` | List of dictionaries defining the FirewallD services. Subkeys: <ul><li>`port`: Mandatory, string. Name of the service.</li><li>`state`: Optional, string. State of the service. Either `enabled` or `disabled`. Defaults to `enabled.</li></ul> | `[]` |
| `firewall__fwbuilder_fw_file`  | The name of the Firewall Builder file which will be created when compiling the firewall in Firewall Builder. Needed if ``firewall__fwbuilder_repo_url`` is used and if the Firewall name within Firewall Builder differs from ``{{ inventory_hostname }}`` | `{{ inventory_hostname }}` |
| `firewall__fwbuilder_repo_url` | The GIT repository URL to clone the compiled firewall files from. | `unset` |


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
