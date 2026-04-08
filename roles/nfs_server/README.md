# Ansible Role linuxfabrik.lfops.nfs_server

This role installs and configures [NFS](http://linux-nfs.org/) as a server.


## Tags

`nfs_server`

* Install nfs-utils on RedHat-Based systems or nfs-kernel-server on Debian-Based systems.
* Enable/disable nfs-server.service.
* `mkdir -p nfs-export-directory`.
* Deploy /etc/exports.
* Triggers: nfs-server.service reload.

`nfs_server:state`

* Enable/disable nfs-server.service.
* Triggers: none.

`nfs_server:exports`

* `mkdir -p nfs-export-directory`.
* Deploy /etc/exports.
* Triggers: nfs-server.service reload.


## Mandatory Role Variables

`nfs_server__exports`

* List of NFS exports to create.
* Type: List of dictionaries.
* Subkeys:

    * `path`:

        * Mandatory. Directory to export.
        * Type: String.

    * `clients`:

        * Mandatory. List of client specifications. Have a look at `man 5 exports`.
        * Type: List.

    * `owner`:

        * Optional. Owner of the export directory.
        * Type: String.
        * Default: `'nobody'`

    * `group`:

        * Optional. Group of the export directory.
        * Type: String.
        * Default: `'nogroup'` (`'nobody'` for RHEL, CentOS, Fedora, Rocky)

    * `mode`:

        * Optional. Mode of the export directory.
        * Type: String.
        * Default: `'0o755'`

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

`nfs_server__service_enabled`

* Enables or disables the nfs-server service, analogous to `systemctl enable/disable --now`.
* Type: Bool.
* Default: `true`

Example:
```yaml
# optional
nfs_server__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
