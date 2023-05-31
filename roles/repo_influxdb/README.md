# Ansible Role linuxfabrik.lfops.repo_influxdb

This role deploys the InfluxDB repository.

Runs on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)
* Debian 11


## Tags

| Tag             | What it does                    |
| ---             | ------------                    |
| `repo_influxdb` | Deploys the InfluxDB Repository |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `repo_influxdb__mirror_url` | Set the URL to a custom mirror server providing the repository. Defaults to `lfops__repo_mirror_url` to allow easily setting the same URL for all `repo_*` roles. If `lfops__repo_mirror_url` is not set, the default mirrors of the repo are used. | `'{{ lfops__repo_mirror_url | default("") }}'` |

Example:
```yaml
# optional
repo_influxdb__mirror_url: 'https://mirror.example.com'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
