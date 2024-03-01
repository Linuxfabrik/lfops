# Ansible Role linuxfabrik.lfops.mount

This role installs NFS and CIFS client utilities when necessary and configures mount points in `/etc/fstab`.


Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Debian 11 (and compatible)


## Tags

| Tag                  | What it does                           |
| ---                  | ------------                           |
| `mount`              | <ul><li>Install nfs-utils/cifs on RedHat-Based systems or nfs-common/cifs-utils on Debian-Based systems</li><li>`mkdir -p mount-point`</li><li>Mount volumes</li></ul> |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `mount__mounts` | List of mounts to create. Subkeys: <ul><li>`path`</li><li>`src`</li><li>`fstype`</li><li>`opts`</li><li>`state`</li></ul>For details, have a look at the [ansible.posix.mount_module](https://docs.ansible.com/ansible/latest/collections/ansible/posix/mount_module.html#parameter-state). | unset |

Example:
```yaml
# optional
mount__mounts:
  - path: '/mnt/nfs/data'
    fstype: 'nfs'
    src: 'nfs-server.example.com:/path/to/exported/data'
    opts: 'defaults'
    state: 'present'
  - path: '/mnt/cifs/data'
    fstype: 'cifs'
    src: '//cifs-server.example.com/CIFS-Share'
    opts: 'username=USERNAME,password=PASSWORD,vers=2.0,rw'
    state: 'present'
  - path: '/data'
    fstype: 'xfs'
    src: '/dev/sdb1'
    opts: 'defaults'
    state: 'present'
```


## Troubleshooting

`mount.nfs: access denied by server while mounting`: Run `exportfs -rv` on the NFS server and try again.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
