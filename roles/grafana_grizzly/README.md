# Ansible Role linuxfabrik.lfops.grafana_grizzly

This role installs [grizzly](https://grafana.github.io/grizzly/), a tool for the management of Grafana dashboards.

Additionally, this role allows you to apply Grafana resources which are saved as `{{ inventory_dir }}/host_vars/{{ inventory_hostname }}/files/grafana_grizzly/*.yml`.


## Mandatory Requirements

* A Grafana Server. This can be done using the [linuxfabrik.lfops.grafana](https://github.com/linuxfabrik/lfops/tree/main/roles/grafana) role.
* A Grafana [service account](https://grafana.com/docs/grafana/latest/administration/service-accounts/) with an Admin token. This can be done using the [linuxfabrik.lfops.grafana](https://github.com/linuxfabrik/lfops/tree/main/roles/grafana) role.

If you use the [Grafana Grizzly Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/grafana_grizzly.yml) this is automatically done for you.


## Tags

| Tag                     | What it does                                     |
| ---                     | ------------                                     |
| `grafana_grizzly`       | Installs grizzly and applies the given resources |
| `grafana_grizzly:apply` | Applies the given resources                      |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `grafana_grizzly__grafana_service_account_login` | The login for a Grafana service account with a "Admin" token. The password will be automatically generated by Grafana and therefore cannot be set here. Set it manually according to the output during the Ansible run. |

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
| `grafana_grizzly__version` | The version of Grizzly to install. Possible options: `'latest'`, or any from https://github.com/grafana/grizzly/releases. | `'v0.2.0'` |

Hints:

* 20240624 we can't use "latest", because then we get annoying errors like:
  `"Providers: Grafana - active, Mimir - inactive (mimir address is not set), Synthetic Monitoring - inactive (stack id is not set)'"`
* `v0.2.0` is the last known good version to use for the way we how we deploy grizzly dashboards and datasources

Example:
```yaml
# optional
grafana_grizzly__grafana_url: 'http://localhost:3000'
grafana_grizzly__version: 'v0.2.0'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
