# Ansible Role icingaweb2

TODO

FQCN: linuxfabrik.lfops.icingaweb2

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* TODO

    Icinga 2 with the IDO database backend (MySQL or PostgreSQL)
    A web server, e.g. Apache or Nginx
    PHP version >= 7.3
    Older versions (5.6+) are only supported up until Icinga Web v2.11



### Optional

    For exports to PDF also the following PHP modules are required: mbstring, GD, Imagick
    LDAP PHP library when using Active Directory or LDAP for authentication



## Tags

| Tag         | What it does                                 |
| ---         | ------------                                 |
| icingaweb2 | TODO |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/icingaweb2/defaults/main.yml) for the variable defaults.


### Mandatory

icingaweb2__api_user_login:


### Optional


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
