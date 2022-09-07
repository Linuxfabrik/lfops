# Ansible Role linuxfabrik.lfops.nextcloud

This role installs Nextcloud.

Tested on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Install Apache and a vHost for Nextcloud. This can be done using the [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role.
* Install MariaDB. This can be done using the [linuxfabrik.lfops.mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server) role.
* Install PHP. This can be done using the [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role.


## Optional Requirements

* Install Redis. This can be done using the [linuxfabrik.lfops.redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis) role.
* Install Collabora. This can be done using the [linuxfabrik.lfops.collabora](https://github.com/Linuxfabrik/lfops/tree/main/roles/collabora) role.
* Install Coturn (for Nextcloud Talk). This can be done using the [linuxfabrik.lfops.coturn](https://github.com/Linuxfabrik/lfops/tree/main/roles/coturn) role.



## Tags

| Tag                       | What it does |
| ---                       | ------------ |
| `nextcloud`               | Installs Nextcloud. |
| `nextcloud:cron`          | todo |
| `nextcloud:occ`           | todo |
| `nextcloud:selinux`       | todo |
| `nextcloud:state`         | todo |
| `nextcloud:update_script` | todo |
| `nextcloud:user`          | todo |



## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `nextcloud__apache_httpd__vhosts__group_var` / `nextcloud__apache_httpd__vhosts__host_var` | descr | `'default` |
| `nextcloud__appconfig` | descr | `''` |
| `nextcloud__database` | descr | `'nextcloud'` |
| `nextcloud__datadir` | descr | `'/data'` |
| `nextcloud__kernel_settings__sysctl__group_var` / `nextcloud__kernel_settings__sysctl__host_var` | descr | `'default` |
| `nextcloud__kernel_settings__transparent_hugepages__group_var` / `nextcloud__kernel_settings__transparent_hugepages__host_var` | descr | `'default` | 'madvise'
| `nextcloud__mariadb_login` | descr | `'{{ mariadb_server__admin_user }}'` |
| `nextcloud__on_calendar_app_update` | descr | `'06,18,23:{{ 59 | random(seed=inventory_hostname) }}'` |
| `nextcloud__on_calendar_jobs`| Run interval of OCC background jobs. | `'*:0/5'` |
| `nextcloud__php__ini_max_execution_time__group_var` / `nextcloud__php__ini_max_execution_time__host_var` | descr | `'3600` |
| `nextcloud__php__ini_max_file_uploads__group_var` / `nextcloud__php__ini_max_file_uploads__host_var` | descr | `'100` |
| `nextcloud__php__ini_memory_limit__group_var` / `nextcloud__php__ini_memory_limit__host_var` | descr | `'1024M'` |
| `nextcloud__php__ini_post_max_size__group_var` / `nextcloud__php__ini_post_max_size__host_var` | descr | `'16M'` |
| `nextcloud__php__ini_upload_max_filesize__group_var` / `nextcloud__php__ini_upload_max_filesize__host_var` | descr | `'10000M'` |
| `nextcloud__php__modules__group_var` / `nextcloud__php__modules__host_var` | descr | `'default` |
| `nextcloud__proxyconfig` | descr | `[]` |
| `nextcloud__sysconfig` | descr | `''` |
| `nextcloud__timer_app_update_enabled` | descr | `true` |
| `nextcloud__timer_jobs_enabled` | descr | `true` |
| `nextcloud__version` | descr | `'latest-24'` |

Creating an Admin and a user:

nextcloud__users:
  - username: 'thefirstadmin'
    password: 'linuxfabrik'
    group: 'admin'
    settings:
      - 'core lang en'
      - 'core locale de_CH'
      - 'core timezone Europe/Zurich'
      - 'files quota "50 MB"'
      - 'firstrunwizard show 0'
      - 'settings email info@example.org'
  - username: 'john.doe'
    password: 'linuxfabrik'


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
