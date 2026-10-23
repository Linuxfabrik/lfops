# Ansible Role linuxfabrik.lfops.cloud_init

This role removes the `cloud-init` package and cleans up artifacts that the package leaves behind.

Concretely, the role:

* Removes the `cloud-init` package via the OS package manager.
* Removes `/etc/NetworkManager/conf.d/99-cloud-init.conf` and reloads NetworkManager if it is running. cloud-init writes `dns = none` there, so NetworkManager does not manage `/etc/resolv.conf`. After the reload it writes the DNS servers of the active connection into `/etc/resolv.conf`.
* Removes `/etc/cloud/cloud.cfg.rpmsave` left over from the package removal.

Depending on the cloud provider, `cloud-init` changes SSH security settings, which we do not want. Note that removing `cloud-init` may break first-boot integrations of the cloud provider (metadata, SSH key injection, hostname provisioning, ...). Run this role only on hosts that have already been provisioned, or on installations where you do not rely on cloud-init at all.


*Available since LFOps `2.0.0`.*


## Tags

`cloud_init`

* Removes the cloud-init package and its leftover config files.
* Triggers: NetworkManager.service reload.


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
