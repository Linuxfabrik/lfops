# Ansible Role linuxfabrik.lfops.exoscale_vm

This role creates and manages instances (virtual machines) on [Exoscale](https://www.exoscale.com/). It also allows creating other compontents for the instance, such as networks and firewall rules.

Runs on

* Fedora 35
* Fedora 38


## Known Limitations

* Resizing / scaling of instances is currently not supported


## Mandatory Requirements

* Install the [exo command line tool](https://github.com/exoscale/cli/releases) and configure your Exoscale account using `exo config` on the Ansible control node.
* Install the `python3-cs` library on the Ansible control node.
* Import your public SSH-key into Exoscale ([here](https://portal.exoscale.com/compute/keypairs)). Ideally, set the key name to your local username, then you can use the default value for `exoscale_vm__ssh_key`.


## Tags

| Tag                     | What it does                               |
| ---                     | ------------                               |
| `exoscale_vm`           | Creates and manages the instance           |
| `exoscale_vm:firewalls` | Manage the provider firewalls of the host. |
| `exoscale_vm:networks`  | Manage the provider private networks.      |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `exoscale_vm__account` | The name of the Exoscale account name as configured during `exo config`. Can be found in `~/.config/exoscale/exoscale.toml` afterwards. |
| `exoscale_vm__api_key` | Set the Exoscale API key. API keys can be managed [here](https://portal.exoscale.com/iam/api-keys). We recommend creating a unrestricted key, because else some operations fail. |
| `exoscale_vm__api_secret` | Set the Exoscale secret corresponding to the API key. |
| `exoscale_vm__service_offering` | The Exoscale service offering. This defines the amount of CPU cores, RAM and disk space. The possible options can be obtained using `exo compute instance-type list --verbose`. Note that these changes will only be applied to stopped instances. |
| `exoscale_vm__template` | The Exoscale template for the instance. The possible options can be obtained using `exo compute instance-template list`. Note that you have to use the ID instead of the name when referencing custom templates. |
| `exoscale_vm__zone` | The Exoscale zone the instance should be in.  The possible options can be obtained using `exo zone list`. |

Example:
```yaml
# mandatory
exoscale_vm__account: 'example'
exoscale_vm__api_key: 'EXOtn4Rg5ooosUALc1uNTqVTyTd'
exoscale_vm__api_secret: '4Is7jmDfzCONfJtEfxqX1VePSK9p7iZLafJy9ItC'
exoscale_vm__service_offering: 'standard.tiny'
exoscale_vm__template: 'Rocky Linux 8 (Green Obsidian) 64-bit'
exoscale_vm__zone: 'ch-dk-2'
```


## Optional Role Variables

| Variable                 | Description | Default Value |
| --------                 | ----------- | ------------- |
| `exoscale_vm__disk_size` | The disk size in GBs. Has to be higher than 10. Note that adjusting the disk size currently is currently not supported. | `10` |
| `exoscale_vm__name` | The name of the instance. By default, the Ansible inventory name prefixed with `e` is used, as it has to start with a letter. | `'e{{ inventory_hostname }}'` |
| `exoscale_vm__private_instance` | Boolean to choose if the instance should be "private" without a public IP, or not. | `false` |
| `exoscale_vm__private_networks` | A list of dictionaries defining which networks should be attached to this instance. It also allows the creation of new internal networks, or setting a fixed IP for the instance. Subkeys: <ul><li>`name`: Mandatory, string. The name of an existing network, or the network which should be created.</li><li>`cidr`: Optional, string. If this is given, a new network with this cidr is created.</li><li>`fixed_ip`: Optional, string. The fixed IP of this instance. This can be used for attach to an existing network, or when creating a new one.</li></ul> | unset |
| `exoscale_vm__security_group_rules` | A list of dictionaries containing rules for the security group (basically Exoscale firewall rules). Subkeys: <ul><li>`cidr`: Optional, string. CIDR to be used for security group rule.</li><li>`protocol`: Mandatory, string. To which IP protocol the rule is applied. Possible options: `tcp`, `udp`, `icmp`.</li><li>`start_port`: Mandatory, int. The starting port.</li><li>`end_port`: Mandatory, int. The ending port.</li><li>`state`: Optional, string. State of the rule. Either `absent` or `present`. Defaults to `present`.</li><li>`type`: Mandatory, string. For which direction the rule should apply. Possible options: `ingress`, `egress`.</li></ul> | unset |
| `exoscale_vm__ssh_key` | The name of the SSH-key depoited in Exoscale [here](https://portal.exoscale.com/compute/keypairs). Defaults to using the local username of the Ansible control node. | `'{{ lookup("env", "USER") }}'` |
| `exoscale_vm__state` | The state of the instance. Possible options: <ul><li>deployed</li><li>started</li><li>stopped</li><li>restarted</li><li>restored</li><li>destroyed</li><li>expunged</li><li>present</li><li>absent</li></ul> | `'started'` |

Example:
```yaml
# optional
exoscale_vm__disk_size: 10
exoscale_vm__name: '{{ inventory_hostname }}'
exoscale_vm__private_instance: false
exoscale_vm__private_networks:
  - name: 'net-prod01'
    cidr: '192.0.2.0/24'
    fixed_ip: '192.0.2.1'
exoscale_vm__security_group_rules:
  - type: 'ingress'
    protocol: 'tcp'
    start_port: 22
    end_port: 22
exoscale_vm__ssh_key: '{{ lookup("env", "USER") }}'
exoscale_vm__state: 'started'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
