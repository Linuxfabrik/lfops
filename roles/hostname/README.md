# Ansible Role linuxfabrik.lfops.hostname

This role sets the system hostname (the name returned by `hostname` / `hostnamectl status` and stored in `/etc/hostname`) via the `ansible.builtin.hostname` module. The new name is applied immediately and persists across reboots. It also maps the hostname to the host's IP address in `/etc/hosts` for proper local name resolution.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

The role adds a marker block to `/etc/hosts` that maps the FQDN (and the short name) to `hostname__etc_hosts_ip` (the host's primary IPv4 address by default). It does not template the whole file, so entries written by others stay.

cloud-init (with `manage_etc_hosts: true`) and the Debian installer also map the hostname to a loopback address (`127.0.0.1`, `127.0.1.1` or `::1`). Since glibc returns the `/etc/hosts` entries in file order, the hostname would resolve to the loopback address, and Lynis reports this as NAME-4406. The role therefore removes loopback lines that carry nothing but the short name, alone or with any domain (`myhost`, `myhost.example`, `myhost.example.com`). A loopback line that lists other names as well, such as `127.0.0.1 localhost myhost`, is left untouched.

Set `hostname__manage_etc_hosts: false` to leave `/etc/hosts` untouched.


## Known Limitations

* As long as cloud-init is installed and `manage_etc_hosts` is `true`, cloud-init may render `/etc/hosts` from its template again at boot (on every boot with the upstream default, once per instance on Hetzner images). This drops the marker block and maps the hostname to the loopback address again, until the next run of the role. `setup_basic` removes cloud-init with the `cloud_init` role. To keep cloud-init, set `manage_etc_hosts: false` in the user-data. A file in `/etc/cloud/cloud.cfg.d/` does not help, since the vendor-data and user-data of the provider take precedence over it.


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
* Default: `'{{ ansible_facts["default_ipv4"]["address"] | d("") }}'` (the host's primary IPv4 address)

`hostname__full_hostname`

* The full hostname to set. This could be a fully qualified domain name (FQDN). Setting this overwrites `hostname__host_part` and `hostname__domain_part`.
* Type: String.
* Default: `'{{ (hostname__host_part ~ "." ~ hostname__domain_part) | trim(".") }}'`

`hostname__host_part`

* The host part of the hostname.
* Type: String.
* Default: `'{{ inventory_hostname }}'`

`hostname__manage_etc_hosts`

* Whether to maintain the `/etc/hosts` entry that maps the hostname to `hostname__etc_hosts_ip`, and to remove the loopback entries that carry nothing but the hostname. Set to `false` to leave `/etc/hosts` untouched.
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
