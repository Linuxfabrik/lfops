# Ansible Role linuxfabrik.lfops.hostname

This role simply sets the hostname of the server.

Tested on

* RHEL 8 (and compatible)


## Tags

| Tag        | What it does                    |
| ---        | ------------                    |
| `hostname` | Sets the hostname of the server |


## Optional Role Variables

| Variable                | Description                                                                                                                                                        | Default Value                                                            |
| --------                | -----------                                                                                                                                                        | -------------                                                            |
| `hostname__domain_name` | This variable allows to set the same domain name for multiple servers. Only sensible if `hostname__hostname` is not modified.                                      | `''`                                                                     |
| `hostname__hostname`    | The hostname to set. This could be a fully qualified domain name (FQDN). Setting this overwrites `hostname__domain_name`. Defaults to using the Ansible inventory name and the `hostname__domain_name` as a suffix. | `'{{ (inventory_hostname ~ "." ~ hostname__domain_name) | trim(".") }}'` |

Example:
```yaml
# optional
hostname__domain_name: 'example.com'
hostname__hostname: '{{ (inventory_hostname ~ "." ~ hostname__domain_name) | trim(".") }}'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
