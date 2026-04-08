# Ansible Role linuxfabrik.lfops.lvm

This role manages LVM (Logical Volume Manager) including partitions, physical volumes, volume groups, and logical volumes. It can also create filesystems and mount the logical volumes.


## Tags

`lvm`

* Runs all LVM tasks.
* Triggers: none.

`lvm:filesystem`

* Creates filesystems on logical volumes.
* Triggers: none.

`lvm:info`

* Displays current LVM state (lsblk, df, pvs, vgs, lvs).
* Triggers: none.

`lvm:lv`

* Creates/extends/removes logical volumes.
* Triggers: none.

`lvm:mount`

* Creates mount directories, mounts volumes, restorecon.
* Triggers: none.

`lvm:vg`

* Growpart (if enabled), creates/resizes PVs, creates/extends/removes VGs.
* Triggers: none.


## Optional Role Variables

`lvm__lvs__host_var` / `lvm__lvs__group_var`

* List of logical volumes to manage.
* Subkeys:

    * `name`:

        * Mandatory. The logical volume name.
        * Type: String.

    * `vg`:

        * Mandatory. The volume group name.
        * Type: String.

    * `size`:

        * Mandatory (for state=present). Absolute size of the LV (relative sizes with `+` or `-` prefix are not allowed). Supports formats like `10G`, `512M`, `100%FREE`, `50%VG`, `50%PVS`, `50%ORIGIN`.
        * Type: String.

    * `fstype`:

        * Optional. Filesystem type.
        * Type: String.
        * Default: `'xfs'`

    * `resizefs`:

        * Optional. Resize the underlying filesystem when extending the LV.
        * Type: Bool.
        * Default: `true`

    * `shrink`:

        * Optional. Allow shrinking the LV.
        * Type: Bool.
        * Default: `false`

    * `force`:

        * Optional. Force removal of LV. Only used when `state: absent`.
        * Type: Bool.
        * Default: `false`

    * `mount_path`:

        * Optional. Mount point path. If specified, the directory will be created, the LV will be mounted, and `restorecon` will be run automatically on the mount path.
        * Type: String.

    * `mount_opts`:

        * Optional. Mount options.
        * Type: String.
        * Default: `'defaults'`

    * `mount_owner`:

        * Optional. Owner of the mount directory.
        * Type: String.
        * Default: `'root'`

    * `mount_group`:

        * Optional. Group of the mount directory.
        * Type: String.
        * Default: `'root'`

    * `mount_mode`:

        * Optional. Mode of the mount directory.
        * Type: String.
        * Default: `0o0755`

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

* Type: List of dictionaries.
* Default: `[]`

`lvm__vgs__host_var` / `lvm__vgs__group_var`

* List of volume groups to manage. PVs listed in `pvs` are automatically created and resized.
* Subkeys:

    * `name`:

        * Mandatory. The volume group name.
        * Type: String.

    * `pvs`:

        * Mandatory (for state=present). List of physical volume device paths to include in the VG. PVs are automatically created (`pvcreate`) and resized (`pvresize`) before the VG is created/extended.
        * Type: List.

    * `growpart`:

        * Optional. If `true`, automatically runs `growpart` on partition-based PVs (e.g., `/dev/vda3`) before resizing. The partition device and number are auto-detected from the PV path.
        * Type: Bool.
        * Default: `false`

    * `pesize`:

        * Optional. Physical extent size (e.g., `4`, `128K`).
        * Type: String.
        * Default: `4`

    * `force`:

        * Optional. Force removal of VG even if LVs exist. Only used when `state: absent`.
        * Type: Bool.
        * Default: `false`

    * `state`:

        * Optional. `present` or `absent`.
        * Type: String.
        * Default: `'present'`

* Type: List of dictionaries.
* Default: `[]`

Example:
```yaml
# optional
lvm__lvs__host_var:
  - name: 'data'
    vg: 'data'
    size: '100G'
    fstype: 'xfs'
    mount_path: '/data'
    mount_opts: 'nodev,noexec,nosuid'
lvm__vgs__host_var:
  - name: 'data'
    pvs:
      - '/dev/vdb'
```

to extend an existing LV:
```yaml
lvm__lvs__host_var:
  - name: 'root'
    vg: 'rl'
    size: '25G'
```

to create a `/data/` mount on a separate device (`/dev/vdb`):
```yaml
lvm__lvs__host_var:
  - name: 'data'
    vg: 'data'
    size: '100%FREE'
    fstype: 'xfs'
    mount_path: '/data'
    mount_opts: 'nodev,noexec,nosuid'
lvm__vgs__host_var:
  - name: 'data'
    pvs:
      - '/dev/vdb'
```

to create a `/data/` mount on an existing volume group:
```yaml
lvm__lvs__host_var:
  - name: 'data'
    vg: 'rl'
    size: '100%FREE'
    fstype: 'xfs'
    mount_path: '/data'
    mount_opts: 'nodev,noexec,nosuid'
lvm__vgs__host_var:
  # pvresize and growpart
  - name: 'rl'
    pvs:
      - '/dev/vdb3'
    growpart: true
```

grow a partition:
```yaml
lvm__vgs__host_var:
  - name: 'rl'
    pvs:
      - '/dev/vda3'
    growpart: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
