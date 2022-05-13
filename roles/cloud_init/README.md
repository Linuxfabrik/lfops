# Ansible Role cloud_init

This role simply removes the `cloud-init*` package from the system.

Depending on the cloud provider, `cloud-init` changes SSH security settings, which we do not want.
Note that removing `cloud-init` could break some functions of the cloud provider.

FQCN: linuxfabrik.lfops.cloud_init

Tested on

* RHEL 8 (and compatible)


## Requirements

This role does not have any requirements.


## Tags

| Tag        | What it does                   |
| ---        | ------------                   |
| cloud_init | Removes the cloud-init package |


## Role Variables

This role does not have any role variables.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
