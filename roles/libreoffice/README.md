# Ansible Role linuxfabrik.lfops.libreoffice

This role installs LibreOffice on a server, intended for headless operation and mainly used for document conversion (e.g. by an Apache HTTPd-based web app calling `soffice --headless --convert-to pdf`).

By default it only installs `libreoffice-core` plus the writer / calc / impress / draw / math packages. With `libreoffice__client_apache: true` it additionally prepares the host for using LibreOffice from an Apache HTTPd context (Red Hat only).


*Available since LFOps `2.0.0`.*


## What `libreoffice__client_apache: true` Does

Setting this to `true` triggers a Red Hat-specific block. On Debian / Ubuntu the block is not skipped automatically; the SELinux compile steps will fail there, so do not enable this on Debian-family hosts.

When enabled, the role:

* Creates `/usr/share/httpd/.config/libreoffice/` and `/usr/share/httpd/.cache/`, owned by `apache:apache`.
* Runs a one-shot dummy conversion as user `apache` to populate `~/.config/libreoffice/4/`.
* Runs `restorecon -Fvr` on the two directories.
* Compiles two custom SELinux policy modules (`selinux-sofficebin`, `selinux-java`) via `checkmodule` / `semodule_package` and installs them with `semodule --install`. These grant `httpd_t` the additional permissions LibreOffice needs (`setattr` on directories under `lib_t`, `read` on `cgroup_t` files, etc.).
* Via the companion playbook: also runs `linuxfabrik.lfops.selinux` to set the SELinux booleans `httpd_can_network_connect` and `httpd_execmem` to `on`, and to register fcontexts mapping `/usr/share/httpd/.cache` and `/usr/share/httpd/.config` to `httpd_sys_rw_content_t`.

The SELinux booleans / fcontexts are injected from `libreoffice__selinux__booleans__dependent_var` and `libreoffice__selinux__fcontexts__dependent_var` in `defaults/main.yml`. They are role-internal and not meant to be overridden from inventory.


## Tags

`libreoffice`

* Installs LibreOffice and, with `client_apache: true`, the Apache HTTPd integration.
* Triggers: none.


## Optional Role Variables

`libreoffice__client_apache`

* If `true`, prepare the host for running LibreOffice from an Apache HTTPd context (directory layout, dummy run, custom SELinux modules; on Red Hat additionally the SELinux booleans / fcontexts via the companion playbook). Red Hat only.
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
