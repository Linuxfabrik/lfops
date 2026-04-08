# Ansible Role linuxfabrik.lfops.hetzner_vm

This role creates and manages servers (virtual machines) and volumes at the [Hetzner console](https://console.hetzner.cloud)

* Installs the VM with the provided t-shirt-size / flavor / server-type (or removes it)
* Rescales the VM (for this the VM must be stopped before changing type)
* Turns Hetzner backups on/off
* Selects the image to install
* Selects the location
* Deploys the SSH keys from the Hetzner portal
* Upgrades disks
* Manages additional volumes (just attaches/removes them to/from the VM, but does not mount/unmount them in any way)
* Manages networks, subnets and routes
* Manages firewall rules

This role does not configure the VM's network interfaces.


## Mandatory Requirements

* Install the Python library `hcloud` on the Ansible control node (use `pip install --user --upgrade hcloud`).
* Import your public SSH-key into Hetzner (your project > Security > SSH Keys).


## Optional Requirements

* Install the [hcloud command line tool](https://github.com/hetznercloud/cli/releases).


## Tags

`hetzner_vm`

* Creates and manages the server.
* Triggers: none.

`hetzner_vm:firewalls`

* Manages the provider firewalls of the host.
* Triggers: none.


## Mandatory Role Variables

`hetzner_vm__api_token`

* Set the Hetzner API token. API tokens can be managed in your project > Security > API Tokens. The API token requires read and write permissions.
* Type: String.

`hetzner_vm__image`

* The Hetzner image to use for the server. The possible options can be obtained using `hcloud image list`.
* Type: String.

`hetzner_vm__location`

* The Hetzner location the instance should run in. The possible options can be obtained using `hcloud location list`.
* Type: String.

`hetzner_vm__server_type`

* The Hetzner server type. This defines the number of CPU cores, the CPU type, the disk space and the memory size. The possible options can be obtained using `hcloud server-type list`. Note that you cannot upgrade a running instance (otherwise you'll get `server must be stopped before changing type`). Either stop the instance using `hetzner_vm__state: 'stopped'` or set `hetzner_vm__force: true`. Also have a look at `hetzner_vm__upgrade_disk`.
* Type: String.

You also need ONE of these:

`hetzner_vm__enable_public_ipv4`

* Choose if the VM should have a public IPv4 address.
* Type: Bool.
* Default: `false`

`hetzner_vm__enable_public_ipv6`

* Choose if the VM should have a public IPv6 address.
* Type: Bool.
* Default: `false`

`hetzner_vm__networks`

* A list of dictionaries defining which networks should be attached to this instance. It also allows the creation of new internal networks, or setting a fixed IP for the instance.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. The name of an existing network, or the network which should be created.
        * Type: String.

    * `cidr`:

        * Optional. If this is given, a new network with this cidr is created.
        * Type: String.

    * `fixed_ip`:

        * Optional. The fixed IP of this instance. This can be used for attach to an existing network, or when creating a new one.
        * Type: String.

    * `state`:

        * Optional. State of the network attachment.
        * Type: String.
        * Default: `'present'`

    * `routes`:

        * Optional. Routes for this network, with `destination` and `gateway` subkeys.
        * Type: List.
        * Default: `[]`

Example:
```yaml
# mandatory
hetzner_vm__api_token: 'V5bg8DsrWxgbydkiS6RrE2Jcbcw1eWEZxh26Oms2t6ZhTWfg25r60ua9upCZgt79ui'
hetzner_vm__image: 'rocky-8'
hetzner_vm__location: 'nbg1'
hetzner_vm__server_type: 'cx11'

# one of these
hetzner_vm__enable_public_ipv4: false
hetzner_vm__enable_public_ipv6: false
hetzner_vm__networks:
  - name: 'net-test01'
    cidr: '10.126.219.0/24'
    fixed_ip: '10.126.219.12'
    state: 'present'
    routes:
      - destination: '0.0.0.0/0'
        gateway: '10.126.219.2'
```


## Optional Role Variables

`hetzner_vm__backups`

* Choose if Hetzner itself should make backups of the volumes. Note that backups cost an additional 20% of the server price. Volumes are not included in backups.
* Type: Bool.
* Default: `false`

`hetzner_vm__firewall_rules`

* List of firewall rules that should be applied to the server.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `direction`:

        * Mandatory. Either `in` or `out`.
        * Type: String.

    * `port`:

        * Mandatory. Single port or range, in the form of `1024-5000`.
        * Type: Number or String.

    * `protocol`:

        * Mandatory. Either `tcp`, `udp`, `icmp`.
        * Type: String.

    * `source_ips`:

        * Mandatory. List of allowed CIDR source addresses.
        * Type: List.

`hetzner_vm__force`

* Force the update of the server. This may power off the server. The rescaling process will usually take just a few minutes. Also have a look at `hetzner_vm__upgrade_disk`.
* Type: Bool.
* Default: `false`

`hetzner_vm__name`

* The name of the server. By default, it uses the Ansible inventory name.
* Type: String.
* Default: `'{{ inventory_hostname }}'`

`hetzner_vm__ssh_keys`

* List of SSH-key names that should be placed on the server. The names have to match the SSH-keys deposited in Hetzner.
* Type: List.
* Default: `[]`

`hetzner_vm__state`

* The state of the server. Possible options: `absent`, `present`, `rebuild`, `restarted`, `started`, `stopped`.
* Type: String.
* Default: `'started'`

`hetzner_vm__upgrade_disk`

* Resize the disk when resizing the server. This will prevent downgrades to a `hetzner_vm__server_type` with a smaller disk later on, as the disk cannot be shrunk.
* Type: Bool.
* Default: `false`

`hetzner_vm__volumes`

* Dictionary of volumes that should be managed and attached to this server.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. The name of the volume.
        * Type: String.

    * `size`:

        * Mandatory. The size in GBs. Has to be higher than 10. Note that shrinking of volumes is not supported.
        * Type: Number.

    * `format`:

        * Optional. The format of the volume. Possible options: `xfs`, `ext4`.
        * Type: String.
        * Default: `'xfs'`

    * `state`:

        * Optional. The state of the volume. Possible options: `present`, `absent`.
        * Type: String.
        * Default: `'present'`

Example:
```yaml
# optional
hetzner_vm__backups: false
hetzner_vm__firewall_rules:
  - direction: 'in'
    port: 22
    protocol: 'tcp'
    source_ips:
      - 0.0.0.0/0
      - ::/0
hetzner_vm__force: false
hetzner_vm__name: '{{ inventory_hostname }}'
hetzner_vm__ssh_keys:
  - 'alice'
  - 'bob'
hetzner_vm__state: 'started'
hetzner_vm__upgrade_disk: false
hetzner_vm__volumes:
  - name: '{{ inventory_hostname }}-data'
    size: '100'
```


## Known Limitations

It is currently not possible to start a server with only an internal network *and* a fixed IP (see https://github.com/ansible-collections/hetzner.hcloud/issues/172). As a workaround, the server can be created with `hetzner_vm__state: 'stopped'` and then started:
```bash
ansible-playbook --inventory=inventory linuxfabrik.lfops.hetzner_vm --extra-vars="hetzner_vm__state='stopped'"
ansible-playbook --inventory=inventory linuxfabrik.lfops.hetzner_vm --extra-vars="hetzner_vm__state='started'"
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
