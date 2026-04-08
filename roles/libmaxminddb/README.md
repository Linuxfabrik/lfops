# Ansible Role linuxfabrik.lfops.libmaxminddb

This role downloads, compiles and installs [libmaxminddb](https://github.com/maxmind/libmaxminddb/).

For Maxmind, depending on your needs, you normally run three playbooks in this particular order:

1. libmaxminddb (this role)
2. mod_maxminddb
3. maxmind_geoip


## Tags

`libmaxminddb`

* Install gcc httpd-devel.
* curl https://github.com/maxmind/libmaxminddb/releases/download/{{ libmaxminddb__version }}/libmaxminddb-{{ libmaxminddb__version }}.tar.gz --output /tmp/libmaxminddb-{{ libmaxminddb__version }}.tar.gz.
* Copy /tmp/libmaxminddb-{{ libmaxminddb__version }}.tar.gz to the server.
* mkdir -p /tmp/libmaxminddb-{{ libmaxminddb__version }}.
* tar xfz --strip-components 1 -C /tmp/libmaxminddb-{{ libmaxminddb__version }} /tmp/libmaxminddb-{{ libmaxminddb__version }}.tar.gz.
* rm -f /tmp/libmaxminddb-{{ libmaxminddb__version }}.tar.gz.
* ./configure.
* make.
* make check.
* make install.
* Configure Dynamic Linker Run Time Bindings.
* ldconfig.
* Triggers: none.


## Optional Role Variables

`libmaxminddb__version`

* The version to install.
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
