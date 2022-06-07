# Ansible Role hostname

This role simply sets the hostname of the server.

FQCN: linuxfabrik.lfops.hostname

Tested on

* RHEL 8 (and compatible)


## Requirements

This role does not have any requirements.


## Tags

| Tag      | What it does                    |
| ---      | ------------                    |
| hostname | Sets the hostname of the server |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/hostname/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### hostname__hostname

The hostname to set. This could be a fully qualified domain name (FQDN). Defaults to using the Ansible inventory name and the `hostname__domain_name` as a suffix.

Default:
```yaml
hostname__hostname: '{{ (inventory_hostname ~ "." ~ hostname__domain_name) | trim(".") }}'
```


#### hostname__domain_name

This variable allows to set the same domain name for multiple servers. Only sensible if `hostname__hostname` is not modified.

Default:
```yaml
hostname__domain_name: ''
```

Example:
```yaml
hostname__domain_name: 'example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
