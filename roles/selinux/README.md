# Ansible Role linuxfabrik.lfops.selinux

This role

* sets the state of SELinux using `setenforce`
* toggles SELinux booleans using `setsebool`
* sets SELinux file contexts using `semanage fcontext`. It does NOT automatically apply them using `restorecon` - have a look at `selinux__restorecons__*_var`
* manages SELinux ports using `semanage port`
* applies SELinux contexts to files using `restorecon`
* compiles and installs custom SELinux policy modules from source (.te, .fc, .if files). Note: Module installation is not idempotent - modules with `state: present` will always be compiled and installed on each run


## Mandatory Requirements

* Install the SELinux python bindings. This can be done using the [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils) role.


## Tags

`selinux`

* `setenforce ...`.
* `setsebool -P ...`.
* `semanage fcontext --add --type ...`.
* `restorecon ...`.
* `semodule -i ...`.
* Triggers: none.

`selinux:fcontext`

* `semanage fcontext --add --type ...`.
* Triggers: none.

`selinux:modules`

* `semodule -i ...`.
* `semodule -r ...`.
* Triggers: none.

`selinux:port`

* `semanage port --add --type ... --proto ...`.
* Triggers: none.

`selinux:restorecon`

* `restorecon ...`.
* Triggers: none.

`selinux:setenforce`

* `setenforce ...`.
* Triggers: none.

`selinux:setsebool`

* `setsebool -P ...`.
* Triggers: none.


## Optional Role Variables

`selinux__booleans__host_var` / `selinux__booleans__group_var`

* A list of dictionaries containing SELinux booleans to set persistently.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `key`:

        * Mandatory. Key of the SELinux boolean.
        * Type: String.

    * `value`:

        * Mandatory. Value of the SELinux boolean.
        * Type: String.

`selinux__fcontexts__host_var` / `selinux__fcontexts__group_var`

* A list of dictionaries containing SELinux file contexts.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `setype`:

        * Mandatory. SELinux file type.
        * Type: String.

    * `target`:

        * Mandatory. The FILE_SPEC which maps file paths using regular expressions to SELinux labels. Either a fully qualified path, or a Perl compatible regular expression (PCRE).
        * Type: String.

    * `state`:

        * Optional. Whether the SELinux file context must be `absent` or `present`.
        * Type: String.
        * Default: `'present'`

`selinux__modules__host_var` / `selinux__modules__group_var`

* A list of dictionaries containing custom SELinux policy modules to compile and install.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). Note: Modules with `state: present` will always be compiled and installed on each run to ensure they stay up-to-date with source changes.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the SELinux module.
        * Type: String.

    * `src`:

        * Mandatory. Path to directory containing module source files. The directory must contain a `.te` file with the same basename as the module name. Optional `.fc` (file context) and `.if` (interface) files will be included if present.
        * Type: String.

    * `state`:

        * Optional. Whether the module must be `absent` or `present`.
        * Type: String.
        * Default: `'present'`

`selinux__policy`

* The name of the SELinux policy to use.
* Type: String.
* Default: `'targeted'`

`selinux__ports__host_var` / `selinux__ports__group_var`

* A list of dictionaries containing SELinux ports.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `setype`:

        * Mandatory. SELinux port type.
        * Type: String.

    * `port`:

        * Mandatory. Port or port range.
        * Type: String.

    * `proto`:

        * Optional. Protocol for the specified port (range).
        * Type: String.
        * Default: `'tcp'`

    * `state`:

        * Optional. Whether the SELinux port must be `absent` or `present`.
        * Type: String.
        * Default: `'present'`

`selinux__restorecons__host_var` / `selinux__restorecons__group_var`

* A list of dictionaries containing paths to run `restorecon` on.
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `path`:

        * Mandatory. Path to restore SELinux context on.
        * Type: String.

    * `force`:

        * Optional. If `true`, forces complete context replacement (`-F` flag).
        * Type: Bool.
        * Default: `true`

    * `recursive`:

        * Optional. If `true`, recursively restores contexts in directories (`-r` flag).
        * Type: Bool.
        * Default: `true`

    * `state`:

        * Optional. Whether restorecon should be run (`present`) or skipped (`absent`).
        * Type: String.
        * Default: `'present'`

`selinux__state`

* The SELinux state. Possible options: `disabled`, `enforcing`, `permissive`.
* Type: String.
* Default: `'enforcing'`

Example:
```yaml
# optional
selinux__booleans__host_var:
  - key: 'httpd_can_network_connect_db'
    value: 'on'
  - key: 'httpd_can_sendmail'
    value: 'on'
  - key: 'httpd_execmem'
    value: 'on'
  - key: 'httpd_use_nfs'
    value: 'on'
selinux__fcontexts__host_var:
  - setype: 'httpd_sys_rw_content_t'
    target: '/data(/.*)?'
    state: 'present'
  - setype: 'httpd_sys_rw_content_t'
    target: '/var/www/html/nextcloud/.htaccess'
    state: 'present'
selinux__modules__host_var:
  - name: 'myapp_policy'
    src: '{{ inventory_dir }}/host_files/selinux/myapp_policy' # directory containing myapp_policy.te, myapp_policy.fc, myapp_policy.if
    state: 'present'
  - name: 'custom_httpd'
    src: '{{ inventory_dir }}/host_files/selinux/custom_httpd'
  - name: 'old_module'
    state: 'absent'
selinux__policy: 'default'
selinux__ports__host_var:
  - setype: 'http_port_t'
    port: '8070-8080'
  - setype: 'ssh_port_t'
    port: 22
selinux__restorecons__host_var:
  - path: '/data'
  - path: '/var/www/html/nextcloud'
  - path: '/opt/app/file.txt'
    recursive: false  # only restore this specific file, not recursively
  - path: '/tmp/test'
    force: false  # only update the type portion of the context
  - path: '/old/legacy/path'
    state: 'absent'  # skip this path
selinux__state: 'enforcing'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
