# Ansible Role linuxfabrik.lfops.nfs_server

This role installs and configures [NFS](http://linux-nfs.org/) as a server.


## Tags

| Tag                  | What it does                           | Reload / Restart |
| ---                  | ------------                           | ---------------- |
| `nfs_server`         | <ul><li>Install nfs-utils on RedHat-Based systems or nfs-kernel-server on Debian-Based systems</li><li>Enable/disable nfs-server.service</li><li>`mkdir -p nfs-export-directory`</li><li>Deploy /etc/exports</li></ul> | Reloads nfs-server.service |
| `nfs_server:state`   | <ul><li>Enable/disable nfs-server.service</li></ul> | - |
| `nfs_server:exports` | <ul><li>`mkdir -p nfs-export-directory`</li><li>Deploy /etc/exports</li></ul> | Reloads nfs-server.service |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `nfs_server__exports` | List of NFS exports to create. Subkeys: <ul><li>`path`: Mandatory, string. Directory to export.</li><li>`clients`: Mandatory, list. List of client specifications. Have a look at `man 5 exports`.</li><li>`owner`: Optional, string. Owner of the export directory. Defaults to `'nobody'`.</li><li>`group`: Optional, string. Group of the export directory. Defaults to `'nogroup'` (`'nobody'` for RHEL, CentOS, Fedora, Rocky).</li><li>`mode`: Optional, string. Mode of the export directory. Defaults to `'0o755'`.</li></ul> |

Example:
```yaml
# mandatory
nfs_server__exports:
  - path: '/data/dir1'
    clients:
      - '192.0.2.1(rw,sync,all_squash)'
      - '192.0.2.2(ro,sync,all_squash)'
    owner: 'root'
    group: 'root'
    mode: '0o755'
  - path: '/data/dir2'
    clients:
      - '192.0.2.3(ro,sync,all_squash)'
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
