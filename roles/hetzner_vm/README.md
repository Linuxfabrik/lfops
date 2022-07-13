# Ansible Role hetzner_vm

This role creates and manages servers (virtual machines) and volumes on [Hetzner](https://www.hetzner.com/).

FQCN: linuxfabrik.lfops.hetzner_vm

Tested on

* Fedora 35


## Requirements

### Mandatory

* Install the python `hcloud` library on the Ansible control node (`pip install --user hcloud`).
* Import your public SSH-key into Hetzner (your project > Security > SSH Keys).


### Optional

* Install the [hcloud command line tool](https://github.com/hetzner/cli/releases).


## Tags

| Tag        | What it does                   |
| ---        | ------------                   |
| hetzner_vm | Creates and manages the server |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/hetzner_vm/defaults/main.yml) for the variable defaults.


### Mandatory

#### hetzner_vm__api_token

Set the Hetzner API token. API tokens can be managed in your project > Security > API Tokens.
The API token requires read and write permissions.

Example:
```yaml
hetzner_vm__api_token: 'V5bg8DsrWxgbydkiS6RrE2Jcbcw1eWEZxh26Oms2t6ZhTWfg25r60ua9upCZgt79ui'
```


#### hetzner_vm__image

The Hetzner image to use for the server. The possible options can be obtained using `hcloud image list`.

Example:
```yaml
hetzner_vm__image: 'rocky-8'
```


#### hetzner_vm__location

The Hetzner location the instance should run in. The possible options can be obtained using `hcloud location list`.

Example:
```yaml
hetzner_vm__location: 'nbg1'
```


#### hetzner_vm__server_type

The Hetzner server type. This defines the number of CPU cores, the CPU type, the disk space and the memory size. The possible options can be obtained using `hcloud server-type list`. Note that you cannot upgrade a running instance. Either stop the instance using `hetzner_vm__state: 'stopped'` or set `hetzner_vm__force: true`.

Example:
```yaml
hetzner_vm__server_type: 'cx11'
```


### Optional

#### hetzner_vm__state

The state of the server. Possible options:

* absent
* present
* rebuild
* restarted
* started
* stopped

Default:
```yaml
hetzner_vm__state: 'started'
```


#### hetzner_vm__force

Force the update of the server. This may power off the server. The rescaling process will usually take just a few minutes. Also have a look at `hetzner_vm__upgrade_disk`.

Default:
```yaml
hetzner_vm__force: false
```


#### hetzner_vm__upgrade_disk

Resize the disk when resizing the server. This will prevent downgrades to a `hetzner_vm__server_type` with a smaller disk later on, as the disk cannot be shrunk.

Default:
```yaml
hetzner_vm__upgrade_disk: false
```


#### hetzner_vm__volumes

Dictionary of volumes that should be managed and attached to this server.

Subkeys:
* `name`: Mandatory, string. The name of the volume.
* `size`: Mandatory, integer. The size in GBs. Has to be higher than 10. Note that shrinking of volumes is not supported.
* `format`: Optional, string. The format of the volume. Possible options: `xfs`, `ext4`.
* `state`: Optional, string. Defaults to `present`. The state of the volume. Possible options: `present`, `absent`.



#### hetzner_vm__ssh_keys

List of SSH-key names that should be placed on the server. The names have to match the SSH-keys depoisted in Hetzner.

Default:
```yaml
hetzner_vm__ssh_keys: []
```


#### hetzner_vm__name

The name of the server. By default, it uses the Ansible inventory name.

Default:
```yaml
hetzner_vm__name: '{{ inventory_hostname }}'
```


#### hetzner_vm__backups

Choose if Hetzner itself should make backups of the volumes. Note that backups cost an additional 20% of the server price. Volumes are not included in backups. Possible options:

* true
* false

Default:
```yaml
hetzner_vm__backups: false
```


### hetzner_vm__firewalls

List of Hetzner firewalls that should be applied to the server.

Default:
```yaml
hetzner_vm__firewalls: []
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
