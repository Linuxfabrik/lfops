# Ansible Role linuxfabrik.lfops.grav

This role installs Grav (a simple file-based flat-file CMS platform) using PHP composer, and keeps Grav, its plugins and themes up to date with the Grav Package Manager (GPM).


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* The code of Grav, its configuration (`user/config`), pages, plugins and themes belong to `root` and are read-only for the web server, so a hole in Grav or in one of its plugins cannot plant code in the site. The web server can only write the directories Grav writes to at runtime, which are the ones the problems plugin shipped with Grav checks for: `assets`, `backup`, `cache`, `images`, `logs`, `tmp`, `user/accounts` and `user/data`. Only these get the SELinux type `httpd_sys_rw_content_t`, everything else gets `httpd_sys_content_t`. The role sets the owners on every run and reports a change only if it had to change one.
* Content and configuration below `user/` reach the server by other means than Grav, for example a CI/CD pipeline. Deploy them as `root`; the role hands every file outside the runtime directories to `root` on its next run anyway.
* Grav therefore cannot update itself. `grav-update-<instance>.timer` updates the plugins and themes, `grav-selfupgrade-<instance>.timer` upgrades Grav, both with `/usr/local/sbin/grav-gpm`. It runs `bin/gpm` as `root` with a cache, log and tmp directory of its own below `/var/cache/grav-gpm`, since Grav loads PHP code from its cache, which the web server can write. Afterwards it hands the runtime directories back to the web server, restores the SELinux labels and clears the cache of the web server. Use it for every other `bin/gpm` command as well, for example `grav-gpm /var/www/html/www.example.com uninstall form`. A `bin/gpm` run as `root` without it executes code the web server can write; one as `apache` fails.
* The role does not install the Admin Panel. It could not save any setting, since the configuration belongs to `root`, and installing plugins or upgrading Grav from the web interface fails for the same reason. At the end of the play the role lists the Admin Panel plugins that an earlier version installed (`admin`, `admin2`, `api`, `login`), but leaves their removal to you.
* The vHost allows the HTTP methods `GET` and `OPTIONS` only. A plugin that takes form submissions, such as `form`, needs `POST` in `allowed_http_methods`.
* Grav generates `user/config/security-private.php` (the secret for nonces and sessions) and `user/config/versions.yaml` on the first request, which it cannot do in a read-only `user/config`. The role creates both if they are missing; the web server can read `security-private.php`, but not change it.
* Everything that exists once per Grav instance carries `grav__url` as the name of the instance, with `/` replaced by `-`: `grav-selfupgrade-<instance>.timer` and `grav-update-<instance>.timer`, so several instances can share a host. The role removes `grav-selfupgrade.timer` and `grav-update.timer` of older role versions.


## Known Limitations

There might be more to implement:

* https://learn.getgrav.org/17/security/configuration


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* A web server (for example Apache httpd) with a virtual host configured for Grav must be available (role: [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd)).
* PHP 8.3+ must be installed (roles: [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) and [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php)).
* The SELinux file contexts are set by the role [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux).


## Post-Installation Steps

* Behind a reverse proxy that terminates TLS, set `session.secure` in the site's `user/config/system.yaml`. Grav otherwise sets the `Secure` flag on its session cookies only on requests it sees arriving over HTTPS, and the proxy talks plain HTTP to it. The role does not touch this file, since it belongs to the site content. Leave it unset for a site that browsers reach over plain HTTP.

    ```yaml
    session:
      secure: true
    ```


## Tags

`grav`

* `composer create-project getgrav/grav {{ grav__install_dir }}`, if Grav is not installed yet.
* Hand everything below `{{ grav__install_dir }}` to `root:root` with modes `0644` and `0755`, but the runtime directories, which go to `apache:apache`.
* Deploy `user/config/security-private.php` and `user/config/versions.yaml`, if they are missing.
* `restorecon -Fvr {{ grav__install_dir }}`.
* Report installed Admin Panel plugins.
* Deploy `/usr/local/sbin/grav-gpm`.
* Remove `grav-selfupgrade.{service,timer}` and `grav-update.{service,timer}` of older role versions.
* Deploy `/etc/systemd/system/grav-selfupgrade-<instance>.{service,timer}`.
* Deploy `/etc/systemd/system/grav-update-<instance>.{service,timer}`.
* `systemctl enable/disable grav-selfupgrade-<instance>.timer --now`.
* `systemctl enable/disable grav-update-<instance>.timer --now`.
* Triggers: none.

`grav:state`

* `systemctl enable/disable grav-selfupgrade-<instance>.timer --now`.
* `systemctl enable/disable grav-update-<instance>.timer --now`.
* Triggers: none.


## Mandatory Role Variables

`grav__url`

* The Grav URL, without `http://` or `https://`.
* Type: String.

Example:
```yaml
# mandatory
grav__url: 'grav.example.com'
```


## Optional Role Variables

`grav__install_dir`

* Grav installation directory.
* Type: String.
* Default: `'/var/www/html/{{ grav__url }}'`

`grav__on_calendar_selfupgrade`

* Time to upgrade Grav (systemd timer notation).
* Type: String.
* Default: `'22:{{ 59 | random(seed=inventory_hostname) }}'`

`grav__on_calendar_update`

* Time to update the Grav plugins and themes (systemd timer notation).
* Type: String.
* Default: `'23:{{ 59 | random(seed=inventory_hostname) }}'`

`grav__timer_selfupgrade_enabled`

* Enables/disables the systemd timer that upgrades Grav.
* Type: Bool.
* Default: `true`

`grav__timer_update_enabled`

* Enables/disables the systemd timer that updates the Grav plugins and themes.
* Type: Bool.
* Default: `true`

Example:
```yaml
# optional
grav__install_dir: '/var/www/html/grav'
grav__on_calendar_selfupgrade: '22:30'
grav__on_calendar_update: '23:30'
grav__timer_selfupgrade_enabled: true
grav__timer_update_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
