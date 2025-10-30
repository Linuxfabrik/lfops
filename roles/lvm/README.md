# Ansible Role linuxfabrik.lfops.lvm

This role manages LVM (Logical Volume Manager) including partitions, physical volumes, volume groups, and logical volumes. It can also create filesystems and mount the logical volumes.


## Tags

| Tag              | What it does                                                            | Reload / Restart |
| ---              | ------------                                                            | ---------------- |
| `lvm`            | Runs all LVM tasks                                                      | -                |
| `lvm:filesystem` | Creates filesystems on logical volumes                                  | -                |
| `lvm:info`       | Displays current LVM state (lsblk, df, pvs, vgs, lvs)                   | -                |
| `lvm:lv`         | Creates/extends/removes logical volumes                                 | -                |
| `lvm:mount`      | Creates mount directories, mounts volumes, restorecon                   | -                |
| `lvm:vg`         | Growpart (if enabled), creates/resizes PVs, creates/extends/removes VGs | -                |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `lvm__lvs__host_var` / <br> `lvm__lvs__group_var` | List of logical volumes to manage. Subkeys: <ul><li>`name`: Mandatory, string. The logical volume name.</li><li>`vg`: Mandatory, string. The volume group name.</li><li>`size`: Mandatory (for state=present), string. Absolute size of the LV (relative sizes with `+` or `-` prefix are not allowed). Supports formats like `10G`, `512M`, `100%FREE`, `50%VG`, `50%PVS`, `50%ORIGIN`.</li><li>`fstype`: Optional, string. Filesystem type. Defaults to `xfs`.</li><li>`resizefs`: Optional, boolean. Resize the underlying filesystem when extending the LV. Defaults to `true`.</li><li>`shrink`: Optional, boolean. Allow shrinking the LV. Defaults to `false`.</li><li>`force`: Optional, boolean. Force removal of LV. Only used when `state: absent`. Defaults to `false`.</li><li>`mount_path`: Optional, string. Mount point path. If specified, the directory will be created, the LV will be mounted, and `restorecon` will be run automatically on the mount path.</li><li>`mount_opts`: Optional, string. Mount options. Defaults to `defaults`.</li><li>`mount_owner`: Optional, string. Owner of the mount directory. Defaults to `root`.</li><li>`mount_group`: Optional, string. Group of the mount directory. Defaults to `root`.</li><li>`mount_mode`: Optional, octal. Mode of the mount directory. Defaults to `0o0755`.</li><li>`state`: Optional, string. `present` or `absent`. Defaults to `present`.</li></ul> | `[]` |
| `lvm__vgs__host_var` / <br> `lvm__vgs__group_var` | List of volume groups to manage. PVs listed in `pvs` are automatically created and resized. Subkeys: <ul><li>`name`: Mandatory, string. The volume group name.</li><li>`pvs`: Mandatory (for state=present), list. List of physical volume device paths to include in the VG. PVs are automatically created (`pvcreate`) and resized (`pvresize`) before the VG is created/extended.</li><li>`growpart`: Optional, boolean. If `true`, automatically runs `growpart` on partition-based PVs (e.g., `/dev/vda3`) before resizing. The partition device and number are auto-detected from the PV path. Defaults to `false`.</li><li>`pesize`: Optional, string. Physical extent size (e.g., `4`, `128K`). Defaults to `4`.</li><li>`force`: Optional, boolean. Force removal of VG even if LVs exist. Only used when `state: absent`. Defaults to `false`.</li><li>`state`: Optional, string. `present` or `absent`. Defaults to `present`.</li></ul> | `[]` |

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
