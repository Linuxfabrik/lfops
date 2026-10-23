# Ansible Role linuxfabrik.lfops.exoscale_vm

This role creates and manages instances (virtual machines) on [Exoscale](https://www.exoscale.com/). It also allows creating other components for the instance, such as networks and firewall rules.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* The role runs on the Ansible controller and talks to the Exoscale API, using the `linuxfabrik.lfops.exoscale_instance`, `exoscale_private_network` and `exoscale_security_group` modules of this collection. The controller needs outbound HTTPS access to `api-<zone>.exoscale.com`.
* On an existing instance, the role scales it to `exoscale_vm__service_offering`, grows its disk to `exoscale_vm__disk_size`, attaches it to its security groups and attaches, detaches or re-addresses the `exoscale_vm__private_networks`. Scaling and growing the disk need a stopped instance; the role only stops a running instance for it with `exoscale_vm__force: true`, and fails otherwise.
* `exoscale_vm__template`, `exoscale_vm__ssh_key` and `exoscale_vm__private_instance` only take effect when the instance is created.
* Security group rules and private networks that exist at Exoscale but are not listed in the inventory are left alone. Remove them by listing them with `state: 'absent'`.
* Private networks are created, but never deleted, as other instances may use them as well. An existing private network is never changed.
* `--check` and `--diff` show what would change at Exoscale.


## Known Limitations

* `exoscale_vm__service_offering` can only be changed within the same instance type family (for example from `standard.tiny` to `standard.large`, but not to `memory.large`).
* The disk can only grow, never shrink.


## Requirements

* An Exoscale API key with its secret. Keys can be managed [here](https://portal.exoscale.com/iam/api-keys).

Manual steps:

* Import your public SSH-key into Exoscale ([here](https://portal.exoscale.com/compute/keypairs)). Ideally, set the key name to your local username, then you can use the default value for `exoscale_vm__ssh_key`.


## Tags

`exoscale_vm`

* Creates and manages the instance.
* Triggers: none.

`exoscale_vm:firewalls`

* Manages the security group of the instance and attaches the instance to it.
* Triggers: none.

`exoscale_vm:networks`

* Creates the private networks and attaches the instance to them.
* Triggers: none.

All three tags also apply the other changes to the instance (power state, scaling, disk size), since the attachments are managed together with the instance.


## Mandatory Role Variables

`exoscale_vm__api_key`

* The Exoscale API key.
* Type: String.

`exoscale_vm__api_secret`

* The Exoscale API secret corresponding to the API key.
* Type: String.

`exoscale_vm__service_offering`

* The Exoscale instance type as `<family>.<size>`, for example `standard.tiny` or `memory.extra-large`. This defines the number of CPU cores and the amount of RAM. The available types are listed on the [Exoscale pricing page](https://www.exoscale.com/pricing/#compute), or with `exo compute instance-type list --verbose`. Changing it on an existing instance scales the instance, see `exoscale_vm__force`.
* Type: String.

`exoscale_vm__template`

* The Exoscale template for the instance, as name or as ID. The available templates can be listed with `exo compute instance-template list`. Use the ID for a custom template whose name is not unique.
* Type: String.

`exoscale_vm__zone`

* The Exoscale zone the instance should be in, for example `ch-gva-2`. The available zones can be listed with `exo zone list`.
* Type: String.

Example:
```yaml
# mandatory
exoscale_vm__api_key: 'EXOtn4Rg5ooosUALc1uNTqVTyTd'
exoscale_vm__api_secret: 'linuxfabrik'
exoscale_vm__service_offering: 'standard.tiny'
exoscale_vm__template: 'Rocky Linux 9 (Blue Onyx) 64-bit'
exoscale_vm__zone: 'ch-dk-2'
```


## Optional Role Variables

`exoscale_vm__disk_size`

* The size of the root disk in GiB, between 10 and 51200. Increasing it on an existing instance grows the disk, see `exoscale_vm__force`.
* Type: Number.
* Default: `10`

`exoscale_vm__force`

* Allows the role to stop a running instance to scale it or to grow its disk. The instance is started again afterwards, unless `exoscale_vm__state` is `stopped`. Without it, the role fails instead.
* Type: Bool.
* Default: `false`

`exoscale_vm__name`

* The name of the instance. By default, the Ansible inventory name prefixed with `e` is used, as it has to start with a letter.
* Type: String.
* Default: `'e{{ inventory_hostname }}'`

`exoscale_vm__private_instance`

* Choose if the instance should be "private" without a public IP, or not. Only takes effect when the instance is created.
* Type: Bool.
* Default: `true`

`exoscale_vm__private_networks`

* A list of dictionaries defining which private networks should be attached to this instance. It also allows the creation of new private networks, or setting a fixed IP for the instance.
* Type: List of dictionaries.
* Default: `[]`

* Subkeys:

    * `name`:

        * Mandatory. The name of an existing network, or the network which should be created.
        * Type: String.

    * `cidr`:

        * Optional. If this is given, a new network with this cidr is created, where Exoscale hands out the addresses by DHCP. Ignored if the network already exists.
        * Type: String.

    * `fixed_ip`:

        * Optional. The fixed IP of this instance in the network. If the instance currently has another address in the network, it is changed.
        * Type: String.

    * `state`:

        * Optional. `present` attaches the instance to the network, `absent` detaches it.
        * Type: String.
        * Default: `'present'`

`exoscale_vm__security_group_rules`

* A list of dictionaries containing rules for the security group (basically Exoscale firewall rules). If set, the role creates a security group named after the instance and attaches the instance to it, in addition to the `default` security group.
* Type: List of dictionaries.
* Default: unset

* Subkeys:

    * `cidr`:

        * Optional. The network the rule applies to.
        * Type: String.
        * Default: `'0.0.0.0/0'`

    * `end_port`:

        * Mandatory for `tcp` and `udp`. The ending port.
        * Type: Number.

    * `icmp_code`:

        * Optional, only for `icmp` and `icmpv6`. The ICMP code, `-1` for any.
        * Type: Number.
        * Default: `-1`

    * `icmp_type`:

        * Optional, only for `icmp` and `icmpv6`. The ICMP type, `-1` for any.
        * Type: Number.
        * Default: `-1`

    * `protocol`:

        * Mandatory. To which IP protocol the rule is applied. Possible options: `ah`, `all`, `esp`, `gre`, `icmp`, `icmpv6`, `ipip`, `tcp`, `udp`.
        * Type: String.

    * `start_port`:

        * Mandatory for `tcp` and `udp`. The starting port.
        * Type: Number.

    * `state`:

        * Optional. State of the rule. Either `absent` or `present`.
        * Type: String.
        * Default: `'present'`

    * `type`:

        * Optional. For which direction the rule should apply. Possible options: `ingress`, `egress`.
        * Type: String.
        * Default: `'ingress'`

`exoscale_vm__ssh_key`

* The name of the SSH-key deposited in Exoscale [here](https://portal.exoscale.com/compute/keypairs). Defaults to using the local username of the Ansible control node. Only takes effect when the instance is created.
* Type: String.
* Default: `'{{ lookup("env", "USER") }}'`

`exoscale_vm__state`

* The state of the instance. Possible options:

    * `absent`: Deletes the instance, and its security group if `exoscale_vm__security_group_rules` is set.
    * `present`: Creates the instance if it is missing, and leaves the power state of an existing instance alone.
    * `restarted`: Reboots a running instance on every run, and starts a stopped one.
    * `started`: Creates the instance if it is missing, and starts it if it is stopped.
    * `stopped`: Creates the instance without booting it if it is missing, and stops it if it is running.

* Type: String.
* Default: `'started'`

`exoscale_vm__template_visibility`

* Visibility of the Exoscale template for the instance. Usually `'private'` for custom templates. Ignored if `exoscale_vm__template` is an ID.
* Type: String. One of `private`, `public`.
* Default: `'public'`

Example:
```yaml
# optional
exoscale_vm__disk_size: 20
exoscale_vm__force: true
exoscale_vm__name: '{{ inventory_hostname }}'
exoscale_vm__private_instance: false
exoscale_vm__private_networks:
  - name: 'net-prod01'
    cidr: '192.0.2.0/24'
    fixed_ip: '192.0.2.10'
  - name: 'net-old'
    state: 'absent'
exoscale_vm__security_group_rules:
  - type: 'ingress'
    protocol: 'tcp'
    start_port: 22
    end_port: 22
  - type: 'ingress'
    protocol: 'icmp'
    icmp_type: 8
    icmp_code: 0
    cidr: '198.51.100.0/24'
exoscale_vm__ssh_key: '{{ lookup("env", "USER") }}'
exoscale_vm__state: 'started'
exoscale_vm__template_visibility: 'private'
```


## Troubleshooting

**The run aborts with `the instance has to be stopped to scale it ...` or `... to grow its disk ...`**

* `exoscale_vm__service_offering` or `exoscale_vm__disk_size` differ from the running instance. Either set `exoscale_vm__force: true` (for example as `--extra-vars`) to let the role stop and start the instance, stop it yourself first, or adjust the inventory to the current instance.

**The run aborts with `the disk cannot shrink ...`**

* `exoscale_vm__disk_size` is smaller than the current disk of the instance. Set it to at least the current size.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
