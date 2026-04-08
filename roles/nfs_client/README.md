# Ansible Role linuxfabrik.lfops.nfs_client

This role installs NFS client utilities and controls active and configured NFS mount points in `/etc/fstab`.


## Tags

`nfs_client`

* Install nfs-utils on RedHat-Based systems or nfs-common on Debian-Based systems.
* `mkdir -p nfs-mount-point`.
* Mount NFS volumes.
* Triggers: systemctl daemon-reload.


## Optional Role Variables

`nfs_client__mounts`

* List of NFS mounts to create. For details, have a look at the [ansible.posix.mount_module](https://docs.ansible.com/ansible/latest/collections/ansible/posix/mount_module.html#parameter-state).
* Type: List of dictionaries.
* Default: unset
* Subkeys:

    * `src`:

        * Mandatory. Source of the NFS mount.
        * Type: String.

    * `path`:

        * Mandatory. Path of the mount point.
        * Type: String.

    * `opts`:

        * Mandatory. Mount options.
        * Type: String.

    * `state`:

        * Mandatory. State of the mount.
        * Type: String.

    * `owner`:

        * Optional. Owner of the mount point directory.
        * Type: String.
        * Default: `'root'`

    * `group`:

        * Optional. Group of the mount point directory.
        * Type: String.
        * Default: `'root'`

    * `mode`:

        * Optional. Mode of the mount point directory.
        * Type: String.
        * Default: `'0o755'`

Example:
```yaml
# optional
nfs_client__mounts:
  - src: 'nfs-server.example.com:/path/to/exported/data'
    path: '/mnt/nfs/data'
    opts: 'defaults'
    state: 'mounted'
    owner: 'root'
    group: 'root'
    mode: '0o755'
```


## Troubleshooting

`mount.nfs: access denied by server while mounting`: Run `exportfs -rv` on the NFS server and try again.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
