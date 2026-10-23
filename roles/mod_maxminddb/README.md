# Ansible Role linuxfabrik.lfops.mod_maxminddb

This role downloads, compiles and installs the Maxmind module [mod_maxminddb](https://github.com/maxmind/mod_maxminddb/) for Apache httpd. The resulting `mod_maxminddb.so` is placed where Apache expects it on the target distribution:

* Red Hat-family: `/usr/lib64/httpd/modules/mod_maxminddb.so`
* Debian / Ubuntu: `/usr/lib/apache2/modules/mod_maxminddb.so`

For Maxmind, depending on your needs, you normally run three playbooks in this particular order:

1. libmaxminddb
2. mod_maxminddb (this role)
3. maxmind_geoip


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* Build dependencies are OS-specific:

    * Red Hat-family: `gcc`, `httpd-devel`, `make`, `redhat-rpm-config`, `tar`.
    * Debian / Ubuntu: `apache2-dev`, `gcc`, `make`, `tar` (no `redhat-rpm-config`; that package is RH-only).

* The Tarball is fetched on the Ansible controller (`delegate_to: 'localhost'`), then copied to the target. The controller therefore needs Internet access to GitHub; the target does not.
* `./configure && make` is executed in `~/mod_maxminddb-<version>/`, then `src/.libs/mod_maxminddb.so` is copied to the module path listed above. `make install` is deliberately not used: its `apxs -i -a` also edits the Apache config (a second `LoadModule` in `httpd.conf` on Red Hat-family, a rewritten `maxminddb.load` plus a `.bak~` file on Debian / Ubuntu).
* The `LoadModule` directive is written to `mod_maxminddb__apache_conf_modules_d` (default is OS-specific, see variable below) and points to the OS-specific module path listed above.
* On Debian / Ubuntu the role additionally runs the equivalent of `a2enmod maxminddb` (via `community.general.apache2_module`) so the freshly placed `.load` file gets symlinked into `/etc/apache2/mods-enabled/`. On Red Hat-family hosts the module is picked up automatically because it lives in `/etc/httpd/conf.modules.d/`.


## Requirements

* Apache httpd must be installed (role: [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd)), so that the module and `LoadModule` directories exist.


## Tags

`mod_maxminddb`

* Installs the build toolchain, downloads, compiles and installs `mod_maxminddb`, and writes the corresponding `LoadModule` directive.
* Triggers: none.


## Optional Role Variables

`mod_maxminddb__apache_conf_modules_d`

* Path and filename for the `LoadModule` directive.
* Type: String.
* Default (OS-specific):

    * Red Hat-family: `'/etc/httpd/conf.modules.d/20-mod_maxminddb.conf'`
    * Debian / Ubuntu: `'/etc/apache2/mods-available/maxminddb.load'`

`mod_maxminddb__version`

* The version to install. Possible options: https://github.com/maxmind/mod_maxminddb/releases.
* Type: String.
* Default: `'1.2.0'`

Example:

```yaml
# optional
mod_maxminddb__apache_conf_modules_d: '/etc/httpd/conf-available/mod_maxminddb.conf'
mod_maxminddb__version: '1.2.0'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
