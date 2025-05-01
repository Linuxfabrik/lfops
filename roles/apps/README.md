# Ansible Role linuxfabrik.lfops.apps

This role manages a list of applications using the OS's package manager.


## Tags

| Tag           | What it does                                 |
| ---           | ------------                                 |
| `apps` | <ul><li>Remove apps using the package manager</li><li>Deploy apps using the package manager</li></ul> |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apps__apps__host_var` /<br> `apps__apps__group_var` | List of apps to remove or to deploy. Subkeys:<ul><li>`name`: Mandatory, string. Name of the application package.</li><li>`state`: Optional, string. Possible options: `present` (default), `absent`. You can use other states like `latest` ONLY if they are supported by the underlying package module(s) executed.</li></ul> | `[]` |

Example:
```yaml
# optional
apps__apps__host_var:
  - name: 'svn'
    state: 'absent'
  - name: 'git'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
