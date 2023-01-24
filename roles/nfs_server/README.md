# Ansible Role linuxfabrik.lfops.nfs_server

This role installs and configures [NFS](http://linux-nfs.org/) as a server.

Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Debian 11 (and compatible)


## Tags

| Tag                  | What it does                           |
| ---                  | ------------                           |
| `nfs_server`         | Installs and configures NFS  as server |
| `nfs_server:state`   | Manages the state of the NFS server    |
| `nfs_server:exports` | Configures the NFS exports             |


## Mandatory Role Variables

| Variable              | Description                                                         |
| --------              | -----------                                                         |
| `nfs_server__exports` | A list of valid NFS server exports. Have a look at `man 5 exports`. |

Example:
```yaml
# mandatory
nfs_server__exports:
  - '/data/appserver1 192.0.2.10(rw,sync,all_squash)'
  - '/data/appserver2 192.0.2.11(ro,sync,all_squash)'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `nfs_server__service_enabled` | Enables or disables the nfs-server service, analogous to `systemctl enable/disable --now`. | `true` |

Example:
```yaml
# optional
nfs_server__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
