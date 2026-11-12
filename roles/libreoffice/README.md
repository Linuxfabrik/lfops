# Ansible Role linuxfabrik.lfops.libreoffice

This role installs LibreOffice on a server, intended for headless operation and mainly used for document conversion (e.g. by an Apache HTTPd-based web app calling `soffice --headless --convert-to pdf`).

By default it only installs `libreoffice-core` plus the writer / calc / impress / draw / math packages. With `libreoffice__client_apache: true` it additionally prepares the host for using LibreOffice from an Apache HTTPd context.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

When `libreoffice__client_apache: true` is set, the role:

* Creates `~/.config/libreoffice/`, `~/.cache/` and `~/.ansible/tmp/` in the home directory of the web server user (`/usr/share/httpd` for `apache` on Red Hat, `/var/www` for `www-data` on Debian and Ubuntu), owned by that user.
* Starts LibreOffice once as the web server user (`soffice --headless --terminate_after_init`) to populate `~/.config/libreoffice/4/`.
* On Red Hat with SELinux enabled: runs `restorecon -vr` on `~/.cache` and `~/.config` after creating them.

On Red Hat, LibreOffice started from the web server runs in the `httpd_t` SELinux domain and needs permissions this role does not set itself. The `linuxfabrik.lfops.selinux` role, wired in by the playbook, installs two custom policy modules (`selinux-java`, `selinux-sofficebin`), which let `httpd_t` read `cgroup_t` files, change the attributes of `lib_t` directories and write `usr_t` files, and applies the SELinux booleans and file contexts listed in Dependent Roles.


## Known Limitations

* The role does not run on RHEL 10, which ships no LibreOffice. EPEL 10 does not carry it either.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* Optional (Red Hat only, when `libreoffice__client_apache: true`): the custom SELinux policy modules `selinux-java` and `selinux-sofficebin` must be installed, the SELinux booleans `httpd_can_network_connect` and `httpd_execmem` must be `on`, and `/usr/share/httpd/.cache` and `/usr/share/httpd/.config` must map to the `httpd_sys_rw_content_t` fcontext (role: [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux)).


## Tags

`libreoffice`

* Installs LibreOffice and, with `client_apache: true`, the Apache HTTPd integration.
* Triggers: none.


## Optional Role Variables

`libreoffice__client_apache`

* If `true`, prepare the host for running LibreOffice from an Apache HTTPd context (directory layout, user profile; on Red Hat additionally the custom SELinux modules, booleans and file contexts applied by the `selinux` role the playbook wires in).
* Type: Bool.
* Default: `false`

Example:
```yaml
# optional
libreoffice__client_apache: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
