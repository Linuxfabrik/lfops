# Ansible Role linuxfabrik.lfops.hetzner_vm

This role creates and manages servers (virtual machines) and volumes on [Hetzner](https://www.hetzner.com/)

* Installs the VM with the provided t-shirt-size / flavor / server-type (or removes it)
* Turns Hetzner backups on/off
* Selects the image to install
* Selects the location
* Deploys the SSH keys from the Hetzner portal
* Upgrades disks
* Manages additional volumes

This role does not configure the VM's network interfaces.

Tested on

* Fedora 35
* Fedora 36


## Mandatory Requirements

* Install the python `hcloud` library on the Ansible control node (`dnf -y install hcloud`, `pip install --user hcloud` etc.).
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
| `hetzner_vm__server_type` | The Hetzner server type. This defines the number of CPU cores, the CPU type, the disk space and the memory size. The possible options can be obtained using `hcloud server-type list`. Note that you cannot upgrade a running instance. Either stop the instance using `hetzner_vm__state: 'stopped'` or set `hetzner_vm__force: true`. Also have a look at `hetzner_vm__upgrade_disk`. |

Example:
```yaml
# mandatory
hetzner_vm__api_token: 'V5bg8DsrWxgbydkiS6RrE2Jcbcw1eWEZxh26Oms2t6ZhTWfg25r60ua9upCZgt79ui'
hetzner_vm__image: 'rocky-8'
hetzner_vm__location: 'nbg1'
hetzner_vm__server_type: 'cx11'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `hetzner_vm__backups` | Choose if Hetzner itself should make backups of the volumes. Note that backups cost an additional 20% of the server price. Volumes are not included in backups. Possible options: | `false` |
| `hetzner_vm__firewalls` | List of Hetzner firewalls that should be applied to the server. | `[]` |
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
hetzner_vm__firewalls: []
hetzner_vm__force: false
hetzner_vm__name: '{{ inventory_hostname }}'
hetzner_vm__ssh_keys:
  - 'alice'
  - 'bob'
hetzner_vm__state: 'started'
hetzner_vm__upgrade_disk: false
hetzner_vm__volumes: []
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
