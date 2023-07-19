# Ansible Role linuxfabrik.lfops.kvm_vm

This role creates and manages virtual machines (VMs) on a KVM host.

By default, this role uses a base image which will be modified using cloud-init and sysprep (for deploying ssh keys or setting the root password).

Note: cloud-init and sysprep are only run if the boot disk is newly created.

If you want to create a VM with an existing disk, have a look at the `kvm_vm__existing_boot_disk` variable.

The role currently does not support resizing the VM.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Install Python 3, and the python3-libvirt and python3-lxml modules on the KVM host. This can be done using the [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python) role. If you use the [kvm_host Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/kvm_host.yml) to setup the KVM host, this is automatically done for you.
* Place the base image in the `kvm_vm__pool` on the KVM host.


## Tags

| Tag            | What it does                            |
| ---            | ------------                            |
| `kvm_vm`       | Creates and manages the virtual machine |
| `kvm_vm:state` | Sets the state of the VM                |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `kvm_vm__base_image` | The base image file which will be used for the VM. Has to be placed in the `kvm_vm__pool` storage pool. |
| `kvm_vm__boot_disk_size` | The size to which the boot disk will be resized. This is required since we are using a base image. Should either be in bytes, or given using an optional suffix: k or K (kilobyte, 1024), M (megabyte, 1024k) and G (gigabyte, 1024M) and T (terabyte, 1024G) are supported. b is ignored. |
| `kvm_vm__host` | The KVM host. Will be used in `delegate_to` statements, meaning the host should either be in the ansible inventory or reachable via the given value. |
| `kvm_vm__memory` | Memory to allocate for the VM, in MiB. |
| `kvm_vm__vcpus` | Number of virtual cpus to configure for the VM. |

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

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `kvm_vm__additional_disks` | A list of additional disks. They will be created in the `kvm_vm__pool` if they do not exist already. Subkeys:<ul><li>`name`: Mandatory, string. The name of the disk. Will be prepended with the `kvm_vm__name` and suffixed with `.qcow2`.</li><li>* `size`: Mandatory, string. The size of the disk, in the same format as `kvm_vm__boot_disk_size`.</li></ul>| `[]` |
| `kvm_vm__autostart` | Whether the VM should be started on host boot up or not. | `true` |
| `kvm_vm__boot_uefi` | Boot the VM with UEFI. | `false` |
| `kvm_vm__connect_url` | URL for connecting to the hypervisor on the `kvm_vm__host`. | `'qemu:///system'` |
| `kvm_vm__existing_additional_disks` | A list of existing additional disks. They will not be modified, only added to the VM during creation. The disk have to be placed in the `kvm_vm__pool` storage pool. | `[]` |
| `kvm_vm__existing_boot_disk` | This allows to provide an already existing boot image, skipping the usage of a base image, and any modification to the disk. The disk has to be placed in the `kvm_vm__pool` storage pool. | unset |
| `kvm_vm__max_memory` | The run time maximum memory allocation of the VM. This is the maximum amount of memory that can be hot-plugged. | `'{{ kvm_vm__memory }}'` |
| `kvm_vm__name` | The domain name of the VM. | `'{{ inventory_hostname }}'` |
| `kvm_vm__network_connections` | List of dictionaries of network connections to configure. Currently only supports ethernet devices (no bond/bridges/vlans). Subkeys: <br> * `name`: Mandatory, string. Name of the network interface. <br> * `mac`: Optional, string. MAC of the interface. Defaults to a randomly generated MAC starting with `52:54:`. <br> * `addresses`: Optional, list. List of IP addresses to assign. Defaults is unset. <br> * `dhcp4`: Optional, bool. If dhcp for IPv4 should be enabled or not. Defaults to `false`. <br> * `dhcp6`: Optional, bool. If dhcp for IPv6 should be enabled or not. Defaults to `false`. <br> * `gateway4`: Optional, string. IPv4 Gateway. Requires setting `addresses`. Default is unset. <br> * `gateway6`: Optional, string. IPv6 Gateway. Requires setting `addresses`. Default is unset. <br> * `network_type`: Optional, string. Libvirt Network type. Either `'bridge'` or `'network'`. Defaults to `'network'`. <br> * `network_name`: Optional, string. Libvirt Network name. This is either the name of the bridge or of the virtual network. Defaults to `'default'`. | `[]` |
| `kvm_vm__packages` | A list of packages which will be injected into the image using `virt-customize`. | `['cloud-init', 'qemu-guest-agent']` |
| `kvm_vm__pool` | The KVM storage pool for the base image and disks. | `'default'` |
| `kvm_vm__root_password` | The root password of the VM. | unset |
| `kvm_vm__ssh_authorized_keys` | A list of keys which will be authorized to connect to the VM via SSH. | `[]` |
| `kvm_vm__state` | The state of the VM. Possible options: <br> * `'absent'`: Use with caution. Destroys the VM and deletes all storage volumes. <br> * `'destroyed'`: "hard shutdown". Immediately terminates the VM. Does not delete any storage volumes. <br> * `'paused'`: Suspends the VM. It is kept in memory but won't be scheduled anymore. <br> * `'running'` <br> * `'shutdown'`: Gracefully shuts down the VM. | `'running'` |

Example:
```yaml
# optional
kvm_vm__additional_disks:
  - name: 'disk1'
    size: '10G'
kvm_vm__autostart: true
kvm_vm__boot_uefi: true
kvm_vm__existing_additional_disks:
  - 'vm1-existing-disk1.qcow2'
  - 'vm1-existing-disk2.qcow2'
kvm_vm__existing_boot_disk: 'vm1-existing-boot.qcow2'
kvm_vm__connect_url: 'qemu:///system'
kvm_vm__max_memory: '{{ kvm_vm__memory }}'
kvm_vm__name: '{{ inventory_hostname }}'
kvm_vm__network_connections:
  - name: 'eth0'
    addresses:
      - '192.0.2.2'
    gateway4: '192.0.2.1'
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
