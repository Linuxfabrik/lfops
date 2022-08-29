# Ansible Role linuxfabrik.lfops.kernel_settings

This role configures kernel settings.

The role does nothing on its own and relies on the [linux_system_roles.kernel_settings role](https://github.com/linux-system-roles/kernel_settings).

Tested on

* RHEL 8 (and compatible)


# Mandatory Requirements

* Install the [Linux System Roles](https://linux-system-roles.github.io/) on the Ansible control node, for example by calling `ansible-galaxy collection install fedora.linux_system_roles`.


## Tags

| Tag               | What it does               |
| ---               | ------------               |
| `kernel_settings` | Configures kernel settings |


## Optional Role Variables

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

* `kernel_settings__sysctl__host_var`, `kernel_settings__sysctl__group_var`
* `kernel_settings__sysfs__host_var`, `kernel_settings__sysfs__group_var`
* `kernel_settings__systemd_cpu_affinity__host_var`, `kernel_settings__systemd_cpu_affinity__group_var`
* `kernel_settings__transparent_hugepages_defrag__host_var`, `kernel_settings__transparent_hugepages_defrag__group_var`
* `kernel_settings__transparent_hugepages__host_var`, `kernel_settings__transparent_hugepages__group_var`

For details have a look at the available role variables from the [linux_system_roles.kernel_settings role](https://github.com/linux-system-roles/kernel_settings/blob/master/README.md).

Example:
```yaml
# optional
kernel_settings__sysctl__group_var:
  - name: 'vm.overcommit_memory'
    value: 1
  - name: 'net.core.somaxconn'
    value: 1024
kernel_settings__sysfs__group_var:
  - name: '/sys/kernel/debug/x86/pti_enabled'
    value: 0
  - name: '/sys/kernel/debug/x86/retp_enabled'
    value: 0
kernel_settings__systemd_cpu_affinity__group_var: '1,3,5,7'
kernel_settings__transparent_hugepages__group_var: 'madvise'
kernel_settings__transparent_hugepages_defrag__group_var: 'defer'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
