# Ansible Role linuxfabrik.lfops.selinux

[SELinux](https://github.com/SELinuxProject) (Security-Enhanced Linux) is a kernel security module that implements Mandatory Access Control: every process and every file gets a security label, and a system-wide policy decides which transitions and accesses are allowed. This role exposes the user-facing knobs of an SELinux installation. It

* sets the state of SELinux using `setenforce`
* toggles SELinux booleans using `setsebool`
* sets SELinux file contexts using `semanage fcontext`. It does NOT automatically apply them using `restorecon` - have a look at `selinux__restorecons__*_var`
* manages SELinux ports using `semanage port`
* applies SELinux contexts to files using `restorecon`
* compiles and installs custom SELinux policy modules from source (.te, .fc, .if files)


*Available since LFOps `2.0.0`.*


## How the Role Behaves

A policy module is compiled on the target host, because a compiled policy package is tied to the policy version of the host it was built for. The compilation happens in a temporary directory that is removed again at the end of the run, and it pulls in a compiler toolchain (`make` and `selinux-policy-devel`) on every host that gets a module.

Compiling the same source twice yields a byte-identical policy package, so the role compares what it compiled against what is installed and only calls `semodule --install` when the two differ. Editing a module's source therefore deploys the new version, while an unchanged module reports no change. Removing a module by hand outside of Ansible reinstalls it on the next run.

Under `--check` the role compiles and compares as usual, since that only writes to the temporary directory. It cannot report the resulting `semodule --install` though: Ansible skips command tasks in check mode.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* The SELinux python bindings must be installed (role: [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils)).


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
* For the usage in `host_vars` / `group_vars` (can only be used in one group at a time).
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Name of the SELinux module. It must match the module name declared in the `.te` source.
        * Type: String.

    * `content_te`:

        * Mandatory, unless `src` is given. The `.te` policy source itself. Use this for a short module that carries no `.fc` or `.if` file, and for a module a role injects, which has no directory on the Ansible controller to point at. A module that also needs a `.fc` or `.if` file uses `src`; for file contexts alone, prefer `selinux__fcontexts__*_var`.
        * Type: String.

    * `src`:

        * Mandatory, unless `content_te` is given. Path to a directory containing module source files. The directory must contain a `.te` file with the same basename as the module name. Optional `.fc` (file context) and `.if` (interface) files will be included if present.
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

        * Mandatory. Protocol for the specified port (range). Part of the entry's unique identity, so it must be set explicitly (commonly `'tcp'`).
        * Type: String.

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
  - name: 'custom_httpd'
    src: '{{ inventory_dir }}/host_files/{{ inventory_hostname }}/selinux/custom_httpd' # directory containing myapp_policy.te, myapp_policy.fc, myapp_policy.if
    state: 'present'
  - name: 'myapp_policy'
    src: '{{ inventory_dir }}/group_files/selinux/myapp_policy'
  - name: 'myapp_socket'
    content_te: |
      module myapp_socket 1.0;

      require {
          type myapp_t;
          class unix_stream_socket connectto;
      }

      allow myapp_t self:unix_stream_socket connectto;
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
