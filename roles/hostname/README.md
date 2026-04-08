# Ansible Role linuxfabrik.lfops.hostname

This role simply sets the hostname of the server.


## Tags

`hostname`

* Sets the hostname of the server.
* Triggers: none.


## Optional Role Variables

`hostname__domain_part`

* The domain (name) part of the hostname. Allows easily setting the same domain name for multiple servers.
* Type: String.
* Default: `''`

`hostname__full_hostname`

* The full hostname to set. This could be a fully qualified domain name (FQDN). Setting this overwrites `hostname__host_part` and `hostname__domain_part`.
* Type: String.
* Default: `'{{ (hostname__host_part ~ "." ~ hostname__domain_part) | trim(".") }}'`

`hostname__host_part`

* The host part of the hostname.
* Type: String.
* Default: `'{{ inventory_hostname }}'`

Example:
```yaml
# optional
hostname__domain_part: 'example.com'
hostname__full_hostname: 'server.example.com'
hostname__host_part: 'server'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
