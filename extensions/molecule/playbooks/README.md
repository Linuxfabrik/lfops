# Molecule Provisioning Playbooks

These shared playbooks back the Molecule test scenarios under `extensions/molecule`. They provision the systems under test as either containers or VMs and are wired into Molecule through the `create`, `prepare`, and `destroy` hooks in `extensions/molecule/config.yml`. A scenario can switch backends by overriding those hooks in its own `molecule.yml`.

This directory also serves as a reference for how the LFOps test setup spins instances up and down. The variables consumed here are set per host in the shared inventory (`extensions/molecule/inventory/host_vars`) or in a scenario-specific inventory.

Two backends are provided:

* libvirt/KVM virtual machines, provisioned through the [linuxfabrik.lfops.kvm_vm](https://github.com/Linuxfabrik/lfops/tree/main/roles/kvm_vm) role.
* Podman containers.


## Mandatory Requirements

* The collections listed in `extensions/molecule/requirements.yml` (`community.crypto`, `community.libvirt`, `containers.podman`). Molecule installs them during the `dependency` stage.


## Optional Requirements

Depending on the backend a scenario uses:

* VM backend:

    * A libvirt/KVM hypervisor reachable as the create host (`kvm_vm__host`, `localhost` by default), with a `default` storage pool and a `default` network.
    * `virsh` on the Ansible controller.
    * Passwordless sudo on the Ansible controller.

* Container backend:

    * Podman on the Ansible controller.


## Playbooks

`vm-create.yml`

* Generates an ephemeral SSH keypair, downloads the cloud image into the libvirt storage pool (when `molecule__vm_image_url` is set), creates the VMs through the `kvm_vm` role, waits for each to obtain an IP address, and writes a dynamic inventory so Molecule can reach them over SSH.

`vm-prepare.yml`

* Waits for SSH to become available on each VM and gathers facts.

`vm-destroy.yml`

* Removes the VMs through the `kvm_vm` role and deletes the ephemeral keypair and dynamic inventory.

`container-create.yml`

* Starts one Podman container per host. Fails early and prints the container log when a container does not come up.

`container-prepare.yml`

* Installs Python inside the container when the image does not ship it, then gathers facts.

`container-destroy.yml`

* Removes the containers.


## Mandatory Variables

`molecule__container_image`

* Container backend only. The image to start the container from.
* Type: String.

Example:
```yaml
# mandatory (container backend)
molecule__container_image: 'docker.io/rockylinux/rockylinux:9-ubi-init'
```


## Optional Variables

`molecule__container_capabilities`

* Container backend only. Linux capabilities to add to the container.
* Type: List.
* Default: unset (Podman default).

`molecule__container_command`

* Container backend only. The command the container runs to stay alive.
* Type: String.
* Default: `'sleep 1d'`

`molecule__container_log_driver`

* Container backend only. The Podman log driver.
* Type: String.
* Default: `'json-file'`

`molecule__container_privileged`

* Container backend only. Run the container in privileged mode.
* Type: Bool.
* Default: `false`

`molecule__container_systemd`

* Container backend only. Run the container with systemd enabled.
* Type: Bool.
* Default: `false`

`molecule__container_volumes`

* Container backend only. Volumes to mount into the container.
* Type: List.
* Default: unset (no volumes).

`molecule__vm_image_url`

* VM backend only. URL of the cloud image to download into the libvirt storage pool. When unset, no image is downloaded and the base image is assumed to exist already.
* Type: String.

The VM backend additionally consumes the `kvm_vm__*` variables, which are passed straight to the [linuxfabrik.lfops.kvm_vm](https://github.com/Linuxfabrik/lfops/tree/main/roles/kvm_vm) role; see that role's README for their meaning. The playbooks set `kvm_vm__ssh_authorized_keys` and `kvm_vm__state` themselves.

Example:
```yaml
# optional (container backend)
molecule__container_command: '/usr/sbin/init'
molecule__container_systemd: true

# optional (VM backend)
molecule__vm_image_url: 'https://dl.rockylinux.org/pub/rocky/9/images/x86_64/Rocky-9-GenericCloud-Base.latest.x86_64.qcow2'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
