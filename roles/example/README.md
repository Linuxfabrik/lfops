# Ansible Role linuxfabrik.lfops.example

This role configures something using [example](https://example.com/). Currently, this role Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Fedora 35
* Fedora 36


## Mandatory Requirements

* Enable the [example repository](https://example.com/). This can be done using the [linuxfabrik.lfops.repo_example](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_example) role.
* Install EXAMPLE. This can be done using the [linuxfabrik.lfops.example](https://github.com/Linuxfabrik/lfops/tree/main/roles/example) role.
* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.

**Attention**

> Make sure that this condition is met.


## Optional Requirements

* Step 1
* Step 2


## Tags

| Tag                   | What it does                                 |
| ---                   | ------------                                 |
| `example`             | * step 1<br> * step 2                        |
| `example:configure`   | * step 1<br> * step 2                        |
| `example:script`      | * step 1<br> * step 2                        |
| `example:state`       | * step 1<br> * step 2                        |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `example__var1` | List/Dict/String/Number/Bool. Description. |

Example:
```yaml
# mandatory
example__var1: 'value'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `example__logrotate` | Number. Log files are rotated `count` days before being removed or mailed to the address specified in a `logrotate` mail directive. If count is `0`, old versions are removed rather than rotated. If count is `-1`, old logs are not removed at all (use with caution, may waste performance and disk space). | `{{ logrotate__rotate \| d(14) }}` |
| `example__service_enabled` | Bool. Enables or disables the service, analogous to `systemctl enable/disable --now`. | `true` |
| `example__service_state`| String. Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `reloaded`<br> * `restarted`<br> * `started`<br> * `stopped` | `'started'` |
| `example__var2` | List/Dict/String/Number/Bool. Description. | `'default'` |
| `example__var3` | Dict. Description. Possible options:<br> * `name`: Mandatory, string. The package name.<br> * `state`: Mandatory, string. State of the package, one of `present`, `absent`. | `{}` |

Example:
```yaml
# optional
example__var2: 'value'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
