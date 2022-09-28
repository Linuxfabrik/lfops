# Ansible Role linuxfabrik.lfops.infomaniak_vm

This role creates and manages instances (virtual machines) on [Infomaniak](https://www.infomaniak.com/). It also allows creating other compontents for the instance, such as networks and firewall rules.

Runs on

* Fedora 35


## Mandatory Requirements

* Install the [openstack command line tool](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html).
* Import your public SSH-key into Infomaniak ([here](https://api.pub1.infomaniak.cloud/horizon/project/key_pairs)). Ideally, set the key name to your local username (replace `.` with ` `), then you can use the default value for `infomaniak_vm__key_name`.


## Tags

| Tag             | What it does                     |
| ---             | ------------                     |
| `infomaniak_vm` | Creates and manages the instance |


## Mandatory Role Variables

| Variable                        | Description                                                                                                                                                |
| --------                        | -----------                                                                                                                                                |
| `infomaniak_vm__flavor`         | The flavor for the instance. This defines the amount of CPU cores, RAM and disk space. The possible options can be obtained using `openstack flavor list`. |
| `infomaniak_vm__image`          | The image to use for this instance. The possible options can be obtained using `openstack image list`.                                                     |
| `infomaniak_vm__api_password`   | The password for the OpenStack API. Normally this is the same as your admin user login.                                                                    |
| `infomaniak_vm__api_project_id` | The project ID for the OpenStack API. Can be obtained by running `openstack project list` after downloading and sourcing the OpenStack RC file.            |
| `infomaniak_vm__api_username`   | The username for the OpenStack API. Normally this is the same as your admin user login.                                                                    |

Example:
```yaml
# mandatory
infomaniak_vm__flavor: 'a1-ram2-disk50-perf1'
infomaniak_vm__image: 'Rocky 8 Generic Cloud'
infomaniak_vm__api_password: 'linuxfabrik'
infomaniak_vm__api_project_id: 'oitexaeTeivaoRo7einuighRiegh4iexah'
infomaniak_vm__api_username: 'PCU-123456'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `infomaniak_vm__key_name` | The name of the deposited SSH-key. Defaults to using the local username of the Ansible control node, but replaces all `.` with ` `, since periods are not allowed in the key name. | `'{{ lookup("env", "USER") \| regex_replace(".", " ") }}'` |
| `infomaniak_vm__name` | The name of the instance. By default, it uses the Ansible inventory name. | `'{{ inventory_hostname }}'` |
| `infomaniak_vm__networks` | A list of dictionaries defining which networks should be attached to this instance. It also allows the creation of new internal networks, or setting a fixed IP for the instance. Subkeys:<br> * `name`: Mandatory, string. The name of an existing network, or the network which should be created.<br> * `cidr`: Optional, string. If this is given, a new network with this cidr is created.<br> * `fixed_ip`: Optional, string. The fixed IP of this instance. This can be used for attach to an existing network, or when creating a new one. | unset |
| `infomaniak_vm__security_group_rules` | A list of dictionaries containing rules for the security group (basically OpenStack firewall rules). Subkeys:<br> * `direction`: Mandatory, string. For which direction the rule should apply. Possible options: `ingress`, `egress`.<br> * `protocol`: Mandatory, string. To which IP protocol the rule is applied. Possible options: `any`, `tcp`, `udp`, `icmp`.<br> * `port_range_min`: Mandatory, int. The starting port.<br> * `port_range_max`: Mandatory, int. The ending port. | unset |
| `infomaniak_vm__separate_boot_volume_size` | The size of the bootable root-volume in GB. This should only be used if the `infomaniak_vm__flavor` does not include a disk. | unset |
| `infomaniak_vm__separate_boot_volume_type` | The type of the bootable root-volume. This only has an effect if `infomaniak_vm__separate_boot_volume_size` is set. Possible Options:<br> * `'perf1'`<br> * `'perf2'`| `'perf2'` |
| `infomaniak_vm__state` | The state of the instance. Note that setting this to absent also removes all other created compontents, except the networks, which are never deleted since other VMs could still be using them. Possible options:<br> * `present`<br> * `absent` | `'present'` |

Example:
```yaml
# optional
infomaniak_vm__key_name: '{{ lookup("env", "USER") | regex_replace(".", " ") }}'
infomaniak_vm__name: '{{ inventory_hostname }}'
infomaniak_vm__networks:
  - name: 'ext-net1'
  - name: 'test-network'
    cidr: '10.1.3.0/24'
    fixed_ip: '10.1.3.1'
infomaniak_vm__security_group_rules:
  - direction: 'ingress'
    protocol: 'tcp'
    port_range_min: 22
    port_range_max: 22
infomaniak_vm__separate_boot_volume_size: 20
infomaniak_vm__separate_boot_volume_type: 'perf2'
infomaniak_vm__state: 'present'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
