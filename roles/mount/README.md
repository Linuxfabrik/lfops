# Ansible Role linuxfabrik.lfops.mount

This role installs NFS and CIFS client utilities when necessary and configures mount points in `/etc/fstab`.


*Available since LFOps `3.0.0`.*


## How the Role Behaves

* The role creates a missing mount point as `root:root` with mode `0755` and never changes an existing one, so the owner and mode of the root of a mounted filesystem stay as they are on the share. Only where a mount sets `owner`, `group` or `mode`, the role applies them to the path after mounting, that is to the root of the mounted filesystem. On an NFS export with `root_squash` this fails, since root may not change them there; set them on the NFS server instead.
* A freshly created filesystem carries no SELinux labels, so confined services such as Apache httpd are denied access to it. When SELinux is not disabled and the mount point of a mounted filesystem is still `unlabeled_t`, the role runs `restorecon -R` on it once. A filesystem that already carries labels is not touched, so a context set by hand, for example with `chcon`, survives. NFS and CIFS shares get their context from the mount options and are never relabeled.


## Tags

`mount`

* Installs nfs-utils/cifs on RedHat-Based systems or nfs-common/cifs-utils on Debian-Based systems, creates missing directories for the mount points, alters `/etc/fstab`, mounts the volumes and applies the `owner`, `group` and `mode` set for a mount.
* Relabels a mounted filesystem with `restorecon -R` while its mount point carries no SELinux label (`unlabeled_t`), as on a freshly created volume.
* Triggers: none.


## Optional Role Variables

`mount__mounts__host_var` / `mount__mounts__group_var`

* List of directories containing the mounts to create.
* Subkeys:

    * `path`:

        * Mandatory. Path to the mount point.
        * Type: String.

    * `src`:

        * Mandatory. Device (or NFS volume, or something else) to be mounted on `path`.
        * Type: String.

    * `fstype`:

        * Mandatory. Filesystem type.
        * Type: String.

    * `group`:

        * Optional. Group of the root of the mounted filesystem.
        * Type: String.
        * Default: unset, the group is left as it is

    * `mode`:

        * Optional. Mode of the root of the mounted filesystem, as a quoted octal number, for example `'0750'`.
        * Type: String.
        * Default: unset, the mode is left as it is

    * `opts`:

        * Optional. Mount options, `man fstab`.
        * Type: String.

    * `owner`:

        * Optional. Owner of the root of the mounted filesystem.
        * Type: String.
        * Default: unset, the owner is left as it is

    * `state`:

        * Optional. Possible options: `absent`, `absent_from_fstab`, `ephemeral`, `mounted`, `present`, `remounted` or `unmounted`. For details, have a look at the [ansible.posix.mount module](https://docs.ansible.com/ansible/latest/collections/ansible/posix/mount_module.html).
        * Type: String.
        * Default: `'mounted'`

* Type: List of dictionaries.
* Default: `[]`

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
    owner: 'myuser'
    group: 'mygroup'
    mode: '0750'
    opts: 'defaults'
    state: 'mounted'
```


## Troubleshooting

**`mount.nfs: access denied by server while mounting`**

* Run `exportfs -rv` on the NFS server and try again.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
