# Ansible Role nfs_server

This role installs and configures [NFS](http://linux-nfs.org/) as a server.

FQCN: linuxfabrik.lfops.nfs_server

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Requirements

This role does not have any requirements.

## Tags

| Tag                | What it does                           |
| ---                | ------------                           |
| nfs_server         | Installs and configures NFS  as server |
| nfs_server:state   | Manages the state of the NFS server    |
| nfs_server:exports | Configures the NFS exports             |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/nfs_server/defaults/main.yml) for the variable defaults.


### Mandatory

#### nfs_server__exports

A list of valid NFS server exports. Have a look at `man 5 exports`.

Example:
```yaml
nfs_server__exports:
  - '/data/appserver1 192.0.2.10(rw,sync,all_squash)'
  - '/data/appserver2 192.0.2.11(ro,sync,all_squash)'
```


### Optional

#### nfs_server__service_enabled

Enables or disables the influxdb service, analogous to `systemctl enable/disable --now`. Possible options:

* true
* false

Default:
```yaml
nfs_server__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
