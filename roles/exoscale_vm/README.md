# Ansible Role exoscale_vm

This role creates and manages instances (virtual machines) on [Exoscale](https://www.exoscale.com/).

FQCN: linuxfabrik.lfops.exoscale_vm

Tested on

* Fedora 35


## Requirements

### Mandatory

* Install the `python3-cs` library on the Ansible control node.
* Import your public SSH-key into Exoscale ([here](https://portal.exoscale.com/compute/keypairs)). Ideally, set the key name to your local username, then you can use the default value for `exoscale_vm__ssh_key`.


### Optional

* Install the [exo command line tool](https://github.com/exoscale/cli/releases).


## Tags

| Tag         | What it does                   |
| ---         | ------------                   |
| exoscale_vm | Create and manage the instance |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/exoscale_vm/defaults/main.yml) for the variable defaults.


### Mandatory

#### exoscale_vm__api_key

Set the Exoscale API key. API keys can be managed [here](https://portal.exoscale.com/iam/api-keys).
We recommend creating a restricted key with all services except "account" and "iam".

Example:

    exoscale_vm__api_key: 'EXOtn4Rg5ooosUALc1uNTqVTyTd'


#### exoscale_vm__api_secret

Set the Exoscale secret corresponding to the API key.

Example:

```yaml
exoscale_vm__api_secret: '4Is7jmDfzCONfJtEfxqX1VePSK9p7iZLafJy9ItC'
```


#### exoscale_vm__zone

The Exoscale zone the instance should be in.  The possible options can be obtained using `exo zone list`.

Example:

```yaml
exoscale_vm__zone: 'ch-dk-2'
```


#### exoscale_vm__template

The Exoscale template for the instance. The possible options can be obtained using `exo compute instance-template list `.

Example:

```yaml
exoscale_vm__template: 'Rocky Linux 8 (Green Obsidian) 64-bit'
```


##### exoscale_vm__service_offering

The Exoscale template for the instance. The possible options can be obtained using `exo compute instance-type list --verbose`.

Example:

```yaml
exoscale_vm__service_offering: 'b6cd1ff5-3a2f-4e9d-a4d1-8988c1191fe8' # standard.tiny
```


### Optional

#### exoscale_vm__state

The state of the instance. Possible options:

* deployed
* started
* stopped
* restarted
* restored
* destroyed
* expunged
* present
* absent

Default:

```yaml
exoscale_vm__state: 'started'
```


#### exoscale_vm__ssh_key

The name of the SSH-key depoited in Exoscale [here](https://portal.exoscale.com/compute/keypairs). Defaults to using the local username of the Ansible control node.

Default:

```yaml
exoscale_vm__ssh_key: '{{ lookup("env", "USER") }}'
```


#### exoscale_vm__name

The name of the instance. By default, it uses the Ansible inventory name.

Example:

```yaml
exoscale_vm__name: '{{ inventory_hostname }}'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
