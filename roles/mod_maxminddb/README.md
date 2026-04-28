# Ansible Role linuxfabrik.lfops.mod_maxminddb

This role downloads, compiles and installs the Maxmind module [mod_maxminddb](https://github.com/maxmind/mod_maxminddb/) for Apache httpd. The resulting `mod_maxminddb.so` is placed where Apache expects it on the target distribution:

* Red Hat-family: `/usr/lib64/httpd/modules/mod_maxminddb.so`
* Debian / Ubuntu: `/usr/lib/apache2/modules/mod_maxminddb.so`

For Maxmind, depending on your needs, you normally run three playbooks in this particular order:

1. libmaxminddb
2. mod_maxminddb (this role)
3. maxmind_geoip


## Mandatory Requirements

Apache has to be installed and at least one `LoadModule` directive already has to exist, otherwise the compile step might fail. If you get `apxs:Error: Activation failed for custom /etc/httpd/conf/httpd.conf file..` or `apxs:Error: At least one 'LoadModule' directive already has to exist..`, check whether `mod_maxminddb.so` has been built (this is the reason why errors of `make install` are ignored — the module is compiled anyway).


## How the Role Behaves

* Build dependencies are OS-specific:

    * Red Hat-family: `gcc`, `httpd-devel`, `make`, `redhat-rpm-config`, `tar`.
    * Debian / Ubuntu: `apache2-dev`, `gcc`, `make`, `tar` (no `redhat-rpm-config`; that package is RH-only).

* The Tarball is fetched on the Ansible controller (`delegate_to: 'localhost'`, `run_once: true`), then copied to the target. The controller therefore needs Internet access to GitHub; the target does not.
* `./configure && make install` is executed in `~/mod_maxminddb-<version>/`. `make install` errors are ignored because `apxs`-based `LoadModule` activation often fails on a default Apache config; the compiled `.so` is what we care about.
* The `LoadModule` directive is written to `mod_maxminddb__apache_conf_modules_d` (default is OS-specific, see variable below) and points to the OS-specific module path listed above.
* On Debian / Ubuntu the role additionally runs the equivalent of `a2enmod maxminddb` (via `community.general.apache2_module`) so the freshly placed `.load` file gets symlinked into `/etc/apache2/mods-enabled/`. On Red Hat-family hosts the module is picked up automatically because it lives in `/etc/httpd/conf.modules.d/`.


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
