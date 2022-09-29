# Ansible Role linuxfabrik.lfops.selinux

This role

* sets the state of SELinux using `setenforce`
* toggles SELinux booleans using `setsebool`
* sets SELinux file contexts using `semanage fcontext` and applies them afterwards using `restorecon`

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Install the SELinux python bindings. This can be done using the [linuxfabrik.lfops.policycoreutils](https://github.com/Linuxfabrik/lfops/tree/main/roles/policycoreutils) role.


## Tags

| Tag                  | What it does                                                   |
| ---                  | ------------                                                   |
| `selinux`            | * `setenforce ...`<br> * `setsebool -P ...`<br> * `semanage fcontext --add --type ...`<br> * `restorecon -îvr ...` |
| `selinux:setenforce` | * `setenforce ...` |
| `selinux:setsebool`  | * `setsebool -P ...` |
| `selinux:fcontext`   | * `semanage fcontext --add --type ...`<br> * `restorecon -îvr ...` |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `selinux__booleans__host_var` /<br> `selinux__booleans__group_var` | A list of dictionaries containing SELinux booleans to set persistently. Subkeys:<br> * `key`: Mandatory, string. Key of the SELinux boolean.<br> * `value`: Mandatory, string. Value of the SELinux boolean.<br>For the usage in `host_vars` / `group_vars` (can only be used in one group at a time). | `[]` |
| `selinux__fcontexts__host_var` /<br> `selinux__fcontexts__group_var` | A list of dictionaries containing SELinux file contexts. Subkeys:<br> * `setype`: Mandatory, string. SELinux file type.<br> * `target`: Mandatory, string. The FILE_SPEC which maps file paths using regular expressions to SELinux labels. Either a fully qualified path, or a Perl compatible regular expression (PCRE).<br> * `state`: Optional, string. Whether the SELinux file context must be `absent` or `present`. Defaults to `'present'`.<br> * `path`: Mandatory, string. The pathname (for the file) to be relabeled. | See example below. |
| `selinux__state` | The SELinux state. Possible options:<br> * `disabled`<br> * `enforcing`<br> * `permissive` | `'enforcing'` |

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
    path: '/data'
  - setype: 'httpd_sys_rw_content_t'
    target: '/var/www/html/nextcloud/.htaccess'
    state: 'present'
    path: '/var/www/html/nextcloud/.htaccess'
selinux__state: 'enforcing'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
