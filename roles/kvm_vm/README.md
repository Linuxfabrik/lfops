# Ansible Role linuxfabrik.lfops.kvm_vm

This role creates and manages virtual machines (VMs) on a KVM host.

By default, this role requires an OS image that has been modified using cloud-init and sysprep (to provide ssh keys or set the root password). Note: cloud-init and sysprep are only run when the boot disk is re-created.

If you want to create a VM with an existing disk, see the `kvm_vm__existing_boot_disk` variable.


## Mandatory Requirements

* Install Python 3, and the python3-libvirt and python3-lxml modules on the KVM host. This can be done using the [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python) role. If you use the [kvm_host Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/kvm_host.yml) to setup the KVM host, this is automatically done for you.
* Place the base image in the `kvm_vm__pool` on the KVM host. If `kvm_vm__pool` is `default`, you get the storage path by running `virsh pool-dumpxml default | grep -i path` on the KVM host.


## Tags

`kvm_vm`

* Creates and manages the virtual machine.
* Triggers: none.

`kvm_vm:additional_disks`

* Creates additional disks. Note that you need to manually attach them to the VM if the VM already exists.
* Triggers: none.

`kvm_vm:resize_disks`

* Resizes boot and additional disks. If the VM is running, also performs a live `virsh blockresize`.
* Triggers: none.

`kvm_vm:state`

* Sets the state of the VM.
* Triggers: none.


## Mandatory Role Variables

`kvm_vm__base_image`

* The base image file which will be used for the VM. Has to be placed in the `kvm_vm__pool` storage pool.
* Type: String.

`kvm_vm__boot_disk_size`

* The size of the boot disk. On initial creation this is required since we are using a base image. On subsequent runs the boot disk will be grown to this size if it is currently smaller (live resize via `virsh blockresize` is performed when the VM is running). Shrinking is never attempted. Should either be in bytes, or given using an optional suffix: k or K (kilobyte, 1024), M (megabyte, 1024k) and G (gigabyte, 1024M) and T (terabyte, 1024G) are supported. b is ignored.
* Type: String.

`kvm_vm__host`

* The KVM host. Will be used in `delegate_to` statements, meaning the host should either be in the ansible inventory or reachable via the given value.
* Type: String.

`kvm_vm__memory`

* Memory to allocate for the VM, in MiB.
* Type: Number.

`kvm_vm__vcpus`

* Number of virtual cpus to configure for the VM.
* Type: Number.

Example:
```yaml
# mandatory
kvm_vm__base_image: 'rocky8-base-image.qcow2'
kvm_vm__boot_disk_size: '50G'
kvm_vm__host: 'kvm-host.example.com'
kvm_vm__memory: 2048
kvm_vm__vcpus: 2
```


## Optional Role Variables

`kvm_vm__additional_disks`

* A list of additional disks. They will be created in the `kvm_vm__pool` if they do not exist already. Note: the disk will only be attached to the VM during VM creation, not during subsequent runs. On subsequent runs, existing disks will be grown if `size` is larger than the current size (live resize via `virsh blockresize` is performed when the VM is running). Shrinking is never attempted.
* Subkeys:

    * `name`:

        * Mandatory. The name of the disk. Will be prepended with the `kvm_vm__name` and suffixed with `.qcow2`.
        * Type: String.

    * `size`:

        * Mandatory. The size of the disk, in the same format as `kvm_vm__boot_disk_size`.
        * Type: String.

    * `pool`:

        * Optional. Storage pool of the disk.
        * Type: String.

* Type: List of dictionaries.
* Default: `[]`

`kvm_vm__autostart`

* Whether the VM should be started on host boot up or not.
* Type: Bool.
* Default: `true`

`kvm_vm__boot`

* See `man virt-install` for details on `--boot`.
* Type: String.
* Default: `''`

`kvm_vm__connect_url`

* URL for connecting to the hypervisor on the `kvm_vm__host`.
* Type: String.
* Default: `'qemu:///system'`

`kvm_vm__existing_additional_disks`

* A list of existing additional disks. They will not be modified, only added to the VM during creation. The disk have to be placed in the `kvm_vm__pool` storage pool.
* Type: List.
* Default: `[]`

`kvm_vm__existing_boot_disk`

* This allows to provide an already existing boot image, skipping the usage of a base image, and any modification to the disk. The disk has to be placed in the `kvm_vm__pool` storage pool.
* Type: String.
* Default: unset

`kvm_vm__machine`

* The machine type to emulate.
* Type: String.
* Default: unset

`kvm_vm__max_memory`

* The run time maximum memory allocation of the VM. This is the maximum amount of memory that can be hot-plugged.
* Type: Number.
* Default: `'{{ kvm_vm__memory }}'`

`kvm_vm__name`

* The domain name of the VM.
* Type: String.
* Default: `'{{ inventory_hostname }}'`

`kvm_vm__network_connections`

* List of dictionaries of network connections to configure. Currently only supports ethernet devices (no bond/bridges/vlans).
* Subkeys:

    * `name`:

        * Mandatory. Name of the network interface.
        * Type: String.

    * `mac`:

        * Optional. MAC of the interface. Defaults to a randomly generated MAC starting with `52:54:`.
        * Type: String.

    * `addresses`:

        * Optional. List of IP addresses to assign.
        * Type: List.

    * `dhcp4`:

        * Optional. If dhcp for IPv4 should be enabled or not.
        * Type: Bool.
        * Default: `false`

    * `dhcp6`:

        * Optional. If dhcp for IPv6 should be enabled or not.
        * Type: Bool.
        * Default: `false`

    * `gateway4`:

        * Optional. IPv4 Gateway. Requires setting `addresses`.
        * Type: String.

    * `gateway6`:

        * Optional. IPv6 Gateway. Requires setting `addresses`.
        * Type: String.

    * `network_type`:

        * Optional. Libvirt Network type. Either `'bridge'` or `'network'`.
        * Type: String.
        * Default: `'network'`

    * `network_name`:

        * Optional. Libvirt Network name. This is either the name of the bridge or of the virtual network.
        * Type: String.
        * Default: `'default'`

* Type: List of dictionaries.
* Default: `[]`

`kvm_vm__osinfo`

* Set the operating system of the VM, will be used to optimise the guest configuration. Have a look at `man virt-install`.
* Type: String.
* Default: `'detect=on'`

`kvm_vm__packages`

* A list of packages which will be injected into the image using `virt-customize`.
* Type: List.
* Default:
    ```yaml
    kvm_vm__packages:
      - 'cloud-init'
      - 'qemu-guest-agent'
    ```

`kvm_vm__pool`

* The KVM storage pool for the base image and disks.
* Type: String.
* Default: `'default'`

`kvm_vm__root_password`

* The root password of the VM.
* Type: String.
* Default: unset

`kvm_vm__ssh_authorized_keys`

* A list of keys which will be authorized to connect to the VM via SSH.
* Type: List.
* Default: `[]`

`kvm_vm__state`

* The state of the VM. Possible options:

    * `'absent'`: Use with caution. Destroys the VM and deletes all storage volumes.
    * `'destroyed'`: "hard shutdown". Immediately terminates the VM. Does not delete any storage volumes.
    * `'paused'`: Suspends the VM. It is kept in memory but won't be scheduled anymore.
    * `'running'`
    * `'shutdown'`: Gracefully shuts down the VM.

* Type: String.
* Default: `'running'`

Example:
```yaml
# optional
kvm_vm__additional_disks:
  - name: 'disk1'
    size: '10G'
    pool: 'data1'
kvm_vm__autostart: true
# a more complex `--boot` parameter: boot using UEFI, but without Secure Boot (paths valid for RHEL)
kvm_vm__boot: 'loader=/usr/share/OVMF/OVMF_CODE.secboot.fd,loader.readonly=yes,loader.type=pflash,nvram.template=/usr/share/OVMF/OVMF_VARS.fd,loader_secure=no'
kvm_vm__existing_additional_disks:
  - 'vm1-existing-disk1.qcow2'
  - 'vm1-existing-disk2.qcow2'
kvm_vm__existing_boot_disk: 'vm1-existing-boot.qcow2'
kvm_vm__connect_url: 'qemu:///system'
kvm_vm__machine: 'q35'
kvm_vm__max_memory: '{{ kvm_vm__memory }}'
kvm_vm__name: '{{ inventory_hostname }}'
kvm_vm__network_connections:
  - name: 'eth0'
    addresses:
      - '192.0.2.2'
    gateway4: '192.0.2.1'
kvm_vm__osinfo: 'detect=on'
kvm_vm__packages:
  - 'cloud-init'
  - 'qemu-guest-agent'
kvm_vm__pool: 'default'
kvm_vm__root_password: 'linuxfabrik'
kvm_vm__ssh_authorized_keys: []
kvm_vm__state: 'running'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
