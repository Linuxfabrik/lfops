# Ansible Role linuxfabrik.lfops.mod_maxminddb

This role downloads, compiles and installs the Maxmind module [mod_maxminddb](https://github.com/maxmind/mod_maxminddb/) for Apache httpd (`/usr/lib64/httpd/modules/mod_maxminddb.so`).

For Maxmind, depending on your needs, you normally run three playbooks in this particular order:

1. libmaxminddb
2. mod_maxminddb (this role)
3. maxmind_geoip


## Mandatory Requirements

Apache has to be installed and at least one `LoadModule` directive already has to exist, otherwise compile might fail. If you get `apxs:Error: Activation failed for custom /etc/httpd/conf/httpd.conf file..`, `apxs:Error: At least one 'LoadModule' directive already has to exist..`, check if `/usr/lib64/httpd/modules/mod_maxminddb.so` has been built (this is the reason why errors are ignored - the module is compiled anyway).


## Tags

`mod_maxminddb`

* Install gcc httpd-devel redhat-rpm-config.
* curl https://github.com/maxmind/mod_maxminddb/releases/download/{{ mod_maxminddb__version }}/mod_maxminddb-{{ mod_maxminddb__version }}.tar.gz --output /tmp/mod_maxminddb-{{ mod_maxminddb__version }}.tar.gz.
* Copy /tmp/mod_maxminddb-{{ mod_maxminddb__version }}.tar.gz to the server.
* mkdir -p /tmp/mod_maxminddb-{{ mod_maxminddb__version }}.
* tar xfz --strip-components 1 -C /tmp/mod_maxminddb-{{ mod_maxminddb__version }} /tmp/mod_maxminddb-{{ mod_maxminddb__version }}.tar.gz.
* rm -f /tmp/mod_maxminddb-{{ mod_maxminddb__version }}.tar.gz.
* ./configure.
* Create Apache `LoadModule` directive in {{ mod_maxminddb__apache_conf_modules_d }}.
* make install.
* Triggers: none.


## Optional Role Variables

`mod_maxminddb__apache_conf_modules_d`

* Path and filename to place the new `LoadModule` directive for Apache.
* Type: String.
* Default: `'/etc/httpd/conf.modules.d/20-mod_maxminddb.conf'`

`mod_maxminddb__version`

* The version to install.
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
