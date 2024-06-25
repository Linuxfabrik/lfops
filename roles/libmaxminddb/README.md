# Ansible Role linuxfabrik.lfops.libmaxminddb

This role downloads, compiles and installs [libmaxminddb](https://github.com/maxmind/libmaxminddb/).

For Maxmind, depending on your needs, you normally run three playbooks in this particular order:

1. libmaxminddb (this role)
2. mod_maxminddb
3. maxmind_geoip


## Tags

| Tag                   | What it does                                 |
| ---                   | ------------                                 |
| `libmaxminddb`        | <ul><li>install gcc httpd-devel</li><li>curl https://github.com/maxmind/libmaxminddb/releases/download/{{ libmaxminddb__version }}/libmaxminddb-{{ libmaxminddb__version }}.tar.gz --output /tmp/libmaxminddb-{{ libmaxminddb__version }}.tar.gz</li><li>copy /tmp/libmaxminddb-{{ libmaxminddb__version }}.tar.gz to the server</li><li>mkdir -p /tmp/libmaxminddb-{{ libmaxminddb__version }}</li><li>tar xfz --strip-components 1 -C /tmp/libmaxminddb-{{ libmaxminddb__version }} /tmp/libmaxminddb-{{ libmaxminddb__version }}.tar.gz</li><li>rm -f /tmp/libmaxminddb-{{ libmaxminddb__version }}.tar.gz</li><li>./configure</li><li>make</li><li>make check</li><li>make install</li><li>Configure Dynamic Linker Run Time Bindings</li><li>ldconfig</li></ul> |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `libmaxminddb__version` | String. The version to install. | `1.7.1` |

libmaxminddb:
```yaml
# optional
libmaxminddb__version: '1.7.1'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
