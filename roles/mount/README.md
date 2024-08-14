# Ansible Role linuxfabrik.lfops.mount

This role installs NFS and CIFS client utilities when necessary and configures mount points in `/etc/fstab`.


## Tags

| Tag                  | What it does                           |
| ---                  | ------------                           |
| `mount`              | Installs nfs-utils/cifs on RedHat-Based systems or nfs-common/cifs-utils on Debian-Based systems, creates the corresponding directories for the mount points, alters `/etc/fstab` und mounts the volumes |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `mount__mounts__host_var` / <br> `mount__mounts__group_var` | List of directories containing the mounts to create. Subkeys: <ul><li>`path`: Mandatory, string. Path to the mount point.</li><li>`src`: Mandatory, string. Device (or NFS volume, or something else) to be mounted on `path`.</li><li>`fstype`: Mandatory, string. Filesystem type.</li><li>`opts`: Optional, string. Mount options, `man fstab`. Defaults to none.</li><li>`state`: Optional, string. Possible options: `absent`, `absent_from_fstab`, `ephemeral`, `mounted`, `present`, `remounted` or `unmounted`. Defaults to `mounted`. For details, have a look at the [ansible.posix.mount module](https://docs.ansible.com/ansible/latest/collections/ansible/posix/mount_module.html).</li></ul> | `[]` |

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
