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

Runs on

* Fedora 35
* Fedora 36


## Mandatory Requirements

* Install the Python library `hcloud` on the Ansible control node (use `pip install --user --upgrade hcloud`).
* Import your public SSH-key into Hetzner (your project > Security > SSH Keys).


## Optional Requirements

* Install the [hcloud command line tool](https://github.com/hetznercloud/cli/releases).


## Tags

| Tag          | What it does                   |
| ---          | ------------                   |
| `hetzner_vm` | Creates and manages the server |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `hetzner_vm__api_token` | Set the Hetzner API token. API tokens can be managed in your project > Security > API Tokens. The API token requires read and write permissions. |
| `hetzner_vm__image` | The Hetzner image to use for the server. The possible options can be obtained using `hcloud image list`. |
| `hetzner_vm__location` | The Hetzner location the instance should run in. The possible options can be obtained using `hcloud location list`. |
| `hetzner_vm__server_type` | The Hetzner server type. This defines the number of CPU cores, the CPU type, the disk space and the memory size. The possible options can be obtained using `hcloud server-type list`. Note that you cannot upgrade a running instance (otherwise you'll get `server must be stopped before changing type`). Either stop the instance using `hetzner_vm__state: 'stopped'` or set `hetzner_vm__force: true`. Also have a look at `hetzner_vm__upgrade_disk`. |

You also need ONE of these:

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `hetzner_vm__enable_public_ipv4` | Choose if the VM should have a public IPv6 address. | `false` |
| `hetzner_vm__enable_public_ipv6` | Choose if the VM should have a public IPv6 address. | `false` |
| `hetzner_vm__networks` | A list of dictionaries defining which networks should be attached to this instance. It also allows the creation of new internal networks, or setting a fixed IP for the instance. Subkeys:<br> * `name`: Mandatory, string. The name of an existing network, or the network which should be created.<br> * `cidr`: Optional, string. If this is given, a new network with this cidr is created.<br> * `fixed_ip`: Optional, string. The fixed IP of this instance. This can be used for attach to an existing network, or when creating a new one.<br> * `state`: Optional, string. State (`absent` / `present`). Defaults to `present`. <br> * `routes`: Optional, list. Routes for this network, with `destination` and `gateway` subkeys. Defaults to `[]`.| `[]` |


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

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `hetzner_vm__backups` | Choose if Hetzner itself should make backups of the volumes. Note that backups cost an additional 20% of the server price. Volumes are not included in backups. Possible options: | `false` |
| `hetzner_vm__firewall_rules` | List of firewall rules that should be applied to the server. Subkeys:<br> * `direction`: Mandatory, string. Either `in` or `out`.<br> * `port`: Mandatory, int. Port.<br> * `protocol`: Mandatory, string. Either `tcp`, `udp`, `icmp`.<br> * `source_ips`: Mandatory, list. List of allowed CIDR source addresses. | `[]` |
| `hetzner_vm__force` | Force the update of the server. This may power off the server. The rescaling process will usually take just a few minutes. Also have a look at `hetzner_vm__upgrade_disk`. | `false` |
| `hetzner_vm__name` | The name of the server. By default, it uses the Ansible inventory name. | `'{{ inventory_hostname }}'` |
| `hetzner_vm__ssh_keys` | List of SSH-key names that should be placed on the server. The names have to match the SSH-keys depoisted in Hetzner. | `[]` |
| `hetzner_vm__state` | The state of the server. Possible options:<br> * absent<br> * present<br> * rebuild<br> * restarted<br> * started<br> * stopped | `'started'` |
| `hetzner_vm__upgrade_disk` | Resize the disk when resizing the server. This will prevent downgrades to a `hetzner_vm__server_type` with a smaller disk later on, as the disk cannot be shrunk. | `false` |
| `hetzner_vm__volumes` | Dictionary of volumes that should be managed and attached to this server. Subkeys:<br> * `name`: Mandatory, string. The name of the volume.<br> * `size`: Mandatory, integer. The size in GBs. Has to be higher than 10. Note that shrinking of volumes is not supported.<br> * `format`: Optional, string. The format of the volume. Possible options: `xfs`, `ext4`.<br> * `state`: Optional, string. Defaults to `present`. The state of the volume. Possible options: `present`, `absent`. | `[]` |

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
  - name: 'data'
    size: '100'
```


## Known Limitations

Creating a server with only an internal network *and* a fixed IP is currently not possible. See https://github.com/ansible-collections/hetzner.hcloud/issues/172. As a workaround, you need to assign a public IP as well, preferabably `hetzner_vm__enable_public_ipv6: true` as these are free. After running ansible, you can shutdown the VM via the WebGUI, go to Networking and Disable public network.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
