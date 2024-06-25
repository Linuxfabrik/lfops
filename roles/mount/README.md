# Ansible Role linuxfabrik.lfops.mount

This role installs NFS and CIFS client utilities when necessary and configures mount points in `/etc/fstab`.


## Tags

| Tag                  | What it does                           |
| ---                  | ------------                           |
| `mount`              | Installs nfs-utils/cifs on RedHat-Based systems or nfs-common/cifs-utils on Debian-Based systems, creates the corresponding directories for the mount points, alters `/etc/fstab` und mounts the volumes |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `mount__mounts__host_var` / <br> `mount__mounts__group_var` | List of directories containing the mounts to create. Subkeys: <ul><li>`path`</li><li>`src`</li><li>`fstype`</li><li>`opts`</li><li>`state`</li></ul>For details, have a look at the [ansible.posix.mount_module](https://docs.ansible.com/ansible/latest/collections/ansible/posix/mount_module.html). | unset |

Example:
```yaml
# optional
mount__mounts__host_var:
  - path: '/mnt/nfs/data'
    fstype: 'nfs'
    src: 'nfs-server.example.com:/path/to/exported/data'
    opts: 'defaults'
    state: 'mounted'
  - path: '/mnt/cifs/data'
    fstype: 'cifs'
    src: '//cifs-server.example.com/CIFS-Share'
    opts: 'username=USERNAME,password=PASSWORD,vers=2.0,rw'
    state: 'mounted'
  - path: '/data'
    fstype: 'xfs'
    src: '/dev/sdb1'
    opts: 'defaults'
    state: 'mounted'
```


## Troubleshooting

`mount.nfs: access denied by server while mounting`: Run `exportfs -rv` on the NFS server and try again.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
