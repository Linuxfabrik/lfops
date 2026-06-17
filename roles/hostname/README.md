# Ansible Role linuxfabrik.lfops.hostname

This role sets the system hostname (the name returned by `hostname` / `hostnamectl status` and stored in `/etc/hostname`) via the `ansible.builtin.hostname` module. The new name is applied immediately and persists across reboots. It also maps the hostname to the host's IP address in `/etc/hosts` for proper local name resolution.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

The role adds a marker block to `/etc/hosts` that maps the FQDN (and the short name) to `hostname__etc_hosts_ip` (the host's primary IPv4 address by default). It does not template the whole file, because `/etc/hosts` is co-managed by cloud-init, which maintains the localhost entries.

If cloud-init is configured with `manage_etc_hosts: true`, it rewrites `/etc/hosts` on every boot and would drop this block. On the standard cloud images used with LFOps cloud-init only manages the localhost line, so the block persists. Set `hostname__manage_etc_hosts: false` to leave `/etc/hosts` untouched.


## Tags

`hostname`

* Sets the hostname of the server and maintains its `/etc/hosts` entry.
* Triggers: none.


## Optional Role Variables

`hostname__domain_part`

* The domain (name) part of the hostname. Allows easily setting the same domain name for multiple servers.
* Type: String.
* Default: `''`

`hostname__etc_hosts_ip`

* The IP address the hostname is mapped to in `/etc/hosts`. When empty, the `/etc/hosts` entry is skipped.
* Type: String.
* Default: `'{{ ansible_facts["default_ipv4"]["address"] | default("") }}'` (the host's primary IPv4 address)

`hostname__full_hostname`

* The full hostname to set. This could be a fully qualified domain name (FQDN). Setting this overwrites `hostname__host_part` and `hostname__domain_part`.
* Type: String.
* Default: `'{{ (hostname__host_part ~ "." ~ hostname__domain_part) | trim(".") }}'`

`hostname__host_part`

* The host part of the hostname.
* Type: String.
* Default: `'{{ inventory_hostname }}'`

`hostname__manage_etc_hosts`

* Whether to maintain the `/etc/hosts` entry that maps the hostname to `hostname__etc_hosts_ip`. Set to `false` to leave `/etc/hosts` untouched.
* Type: Bool.
* Default: `true`

Example:
```yaml
# optional
hostname__domain_part: 'example.com'
hostname__etc_hosts_ip: '192.0.2.10'
hostname__full_hostname: 'server.example.com'
hostname__host_part: 'server'
hostname__manage_etc_hosts: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
