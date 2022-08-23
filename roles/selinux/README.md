# Ansible Role linuxfabrik.lfops.selinux

This role sets the state of SELinux and optionally toggles SELinux booleans.

Tested on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Install the SELinux python bindings. This can be done using the [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils) role.


## Tags

| Tag                | What it does                                                   |
| ---                | ------------                                                   |
| `selinux`          | Sets the SELinux state and optionally toggles SELinux booleans |
| `selinux:state`    | Sets the SELinux state                                         |
| `selinux:booleans` | Toggles SELinux booleans                                       |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `selinux__host_booleans` / `selinux__group_booleans` | A list of dictionaries containing SELinux booleans. Subkeys:<br> * `key`: Mandatory, string. Key of the SELinux boolean.<br> * `value`: Mandatory, string. Value of the SELinux boolean.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `selinux__state` | The SELinux state. Possible options:<br> * `disabled`<br> * `enforcing`<br> * `permissive` | `'enforcing'` |

Example:
```yaml
# optional
selinux__host_booleans:
  - key: 'httpd_can_network_connect'
    value: 'on'
selinux__group_booleans: []
selinux__state: 'enforcing'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
