# Ansible Role linuxfabrik.lfops.nfs_client

This role installs NFS client utilities and controls active and configured NFS mount points in `/etc/fstab`.


Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Debian 11 (and compatible)


## Tags

| Tag                  | What it does                           |
| ---                  | ------------                           |
| `nfs_client`         | <ul><li>Install nfs-utils on RedHat-Based systems or nfs-common on Debian-Based systems</li><li>`mkdir -p nfs-mount-point`</li><li>Mount NFS volumes</li></ul> |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `nfs_client__mounts` | List of NFS mounts to create. Subkeys: <ul><li>`src`</li><li>`path`</li><li>`opts`</li><li>`state`</li></ul>For details, have a look at the [ansible.posix.mount_module](https://docs.ansible.com/ansible/latest/collections/ansible/posix/mount_module.html#parameter-state). | unset |

Example:
```yaml
# optional
nfs_client__mounts:
  - src: 'nfs-server.example.com:/path/to/exported/data'
    path: '/mnt/nfs/data'
    opts: 'defaults'
    state: 'mounted'
```


## Troubleshooting

`mount.nfs: access denied by server while mounting`: Run `exportfs -rv` on the NFS server and try again.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
