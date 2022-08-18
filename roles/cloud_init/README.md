# Ansible Role linuxfabrik.lfops.cloud_init

This role simply removes the `cloud-init*` package from the system.

Depending on the cloud provider, `cloud-init` changes SSH security settings, which we do not want.
Note that removing `cloud-init` could break some functions of the cloud provider.

Tested on

* RHEL 8 (and compatible)


## Tags

| Tag          | What it does                   |
| ---          | ------------                   |
| `cloud_init` | Removes the cloud-init package |


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
