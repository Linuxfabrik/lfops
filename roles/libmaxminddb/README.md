# Ansible Role linuxfabrik.lfops.libmaxminddb

This role downloads, compiles and installs [libmaxminddb](https://github.com/maxmind/libmaxminddb/).

For Maxmind, depending on your needs, you normally run three playbooks in this particular order:

1. libmaxminddb (this role)
2. mod_maxminddb
3. maxmind_geoip


## How the Role Behaves

* Build dependencies are OS-specific:

    * Red Hat-family: `gcc`, `httpd-devel`, `make`, `tar` (installed from the base / EPEL repos).
    * Debian / Ubuntu: `apache2-dev`, `gcc`, `make`, `tar` (installed from the standard apt repos).

* The Tarball is fetched on the Ansible controller (`delegate_to: 'localhost'`, `run_once: true`), then copied to the target. The controller therefore needs Internet access to GitHub; the target does not.
* `./configure && make && make check && make install` is executed in `~/libmaxminddb-<version>/` on the target.
* `/etc/ld.so.conf.d/local.conf` is set to `/usr/local/lib` and `ldconfig` is run so the freshly installed library is picked up by the dynamic linker.


## Tags

`libmaxminddb`

* Installs the build toolchain, downloads, compiles and installs libmaxminddb.
* Triggers: none.


## Optional Role Variables

`libmaxminddb__version`

* The version to install. Possible options: https://github.com/maxmind/libmaxminddb/releases.
* Type: String.
* Default: `'1.7.1'`

Example:

```yaml
# optional
libmaxminddb__version: '1.7.1'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
