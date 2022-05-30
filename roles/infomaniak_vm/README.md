# Ansible Role infomaniak_vm

This role creates and manages instances (virtual machines) on [Infomaniak](https://www.infomaniak.com/). It also allows creating other compontents for the instance, such as networks and firewall rules.

FQCN: linuxfabrik.lfops.infomaniak_vm

Tested on

* Fedora 35


## Requirements

### Mandatory

* Install the [openstack command line tool](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html).
* Import your public SSH-key into Infomaniak ([here](https://portal.infomaniak.com/compute/keypairs)). Ideally, set the key name to your local username (replace `.` with ` `), then you can use the default value for `infomaniak_vm__key_name`.


### Optional

This role does not have optional requirements.


## Tags

| Tag           | What it does                     |
| ---           | ------------                     |
| infomaniak_vm | Creates and manages the instance |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/infomaniak_vm/defaults/main.yml) for the variable defaults.


### Mandatory

#### infomaniak_vm__flavor

The flavor for the instance. This defines the amount of CPU cores, RAM and disk space. The possible options can be obtained using `openstack flavor list`.

Example:
```yaml
infomaniak_vm__flavor: 'a1-ram2-disk50-perf1'
```


#### infomaniak_vm__image

The image to use for this instance. The possible options can be obtained using `openstack image list`.

Example:
```yaml
infomaniak_vm__image: 'Rocky 8 Generic Cloud' # openstack image list
```


#### infomaniak_vm__username

The username for the API. Can be obtained by downloading the OpenStack RC file.

Example:
```yaml
infomaniak_vm__username: 'PCU-123456'
```


#### infomaniak_vm__password

The password for the API. Can be obtained by downloading the OpenStack RC file.

Example:
```yaml
infomaniak_vm__password: 'my-secret-password'
```


#### infomaniak_vm__project_id

The project ID for the API. Can be obtained by downloading the OpenStack RC file.

Example:
```yaml
infomaniak_vm__project_id: 'oitexaeTeivaoRo7einuighRiegh4iexah'
```


### Optional


#### infomaniak_vm__security_group_rules

A list of dictionaries containing rules for the security group (basically OpenStack firewall rules).

Subkeys:

* `direction`: Required, string. For which direction the rule should apply. Possible options: `ingress`, `egress`.
* `protocol`: Required, string. To which IP protocol the rule is applied. Possible options: `any`, `tcp`, `udp`, `icmp`.
* `port_range_min`: Required, int. The starting port.
* `port_range_max`: Required, int. The ending port.

Example:
```yaml
infomaniak_vm__security_group_rules:
  - direction: 'ingress'
    protocol: 'tcp'
    port_range_min: 22
    port_range_max: 22
```



#### infomaniak_vm__networks

A list of dictionaries defining which networks should be attached to this instance. It also allows the creation of new internal networks, or setting a fixed IP for the instance.

Subkeys:

* `name`: Required, string. The name of an existing network, or the network which should be created.
* `cidr`: Optional, string. The CIDR of the network which should be created.
* `fixed_ip`: Optional, string. The fixed IP of this instance.

Default:
```yaml
infomaniak_vm__networks: # openstack network list
  - name: 'ext-net1'
  - name: 'test-network'
    cidr: '10.1.3.0/24'
    fixed_ip: '10.1.3.1'
```


#### infomaniak_vm__volume_size

The size of the root-volume in GB. This should only be used if the `infomaniak_vm__flavor` does not include a disk.

Default:
```yaml
infomaniak_vm__volume_size: 20
```


#### infomaniak_vm__name

The name of the instance. By default, it uses the Ansible inventory name.

Default:
```yaml
infomaniak_vm__name: '{{ inventory_hostname }}'
```


#### infomaniak_vm__key_name

The name of the depoited SSH-key. Defaults to using the local username of the Ansible control node, but replaces all `.` with ` `, since periods are not allowed in the key name.

Default:
```yaml
infomaniak_vm__key_name: '{{ lookup("env", "USER") | regex_replace(".", " ") }}'
```


#### infomaniak_vm__state

The state of the instance. Possible options:

* present
* absent

Note that setting the `infomaniak_vm__state` to absent also removes all other created compontents, except the networks, which are never deleted since other VMs could still be using them.

Default:
```yaml
infomaniak_vm__state: 'present'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
