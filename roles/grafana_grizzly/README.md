# Ansible Role linuxfabrik.lfops.grafana_grizzly

This role installs [grizzly](https://grafana.github.io/grizzly/), a tool for the management of Grafana dashboards.

Additionally, this role allows you to apply Grafana resources which are saved as `{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/grafana_grizzly/*.yml`.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* A Grafana Server. This can be done using the [linuxfabrik.lfops.grafana](https://github.com/linuxfabrik/lfops/tree/main/roles/grafana) role.
* A Grafana [service account](https://grafana.com/docs/grafana/latest/administration/service-accounts/) with an Admin token. This can be done using the [linuxfabrik.lfops.grafana](https://github.com/linuxfabrik/lfops/tree/main/roles/grafana) role.


## Tags

| Tag                     | What it does                                     |
| ---                     | ------------                                     |
| `grafana_grizzly`       | Installs grizzly and applies the given resources |
| `grafana_grizzly:apply` | Applies the given resources                      |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `grafana_grizzly__grafana_service_account_login` | The login for a Grafana service account with a "Admin" token. |

Example:
```yaml
# mandatory
grafana_grizzly__grafana_service_account_login:
  username: 'grizzly'
  password: 'linuxfabrik'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `grafana_grizzly__grafana_url` | The URL under which Grafana is reachable | `'{{ grafana__root_url }}'` |

Example:
```yaml
# optional
grafana_grizzly__grafana_url: 'http://localhost:3000'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
