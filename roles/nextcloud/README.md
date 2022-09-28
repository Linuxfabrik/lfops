# Ansible Role linuxfabrik.lfops.nextcloud

This role installs Nextcloud including the tools needed by the most popular business plugins.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Install a web server (for example Apache httpd), and configure a virtual host for Nextcloud. This can be done using the [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role.
* Install MariaDB 10+. This can be done using the [linuxfabrik.lfops.mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server) role.
* Install PHP 7+. This can be done using the [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role.
* Set the size of your `/tmp` partition to 50 GB+, if you want to allow 5x simultaenous uploads with files each 10 GB in size.

If you use the ["Setup Nextcloud" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_nextcloud.yml), this is automatically done for you.


## Optional Requirements

* Install Redis. This can be done using the [linuxfabrik.lfops.redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis) role.
* Install Collabora. This can be done using the [linuxfabrik.lfops.collabora](https://github.com/Linuxfabrik/lfops/tree/main/roles/collabora) role.
* Install Coturn for Nextcloud Talk. This can be done using the [linuxfabrik.lfops.coturn](https://github.com/Linuxfabrik/lfops/tree/main/roles/coturn) role.

If you use the ["Setup Nextcloud" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_nextcloud.yml), this is automatically done for you.


## Tags

| Tag                       | What it does |
| ---                       | ------------ |
| `nextcloud`               | Installs Nextcloud. |
| `nextcloud:apps`          | TODO |
| `nextcloud:cron`          | * Set background job to "cron"<br>* Deploy /etc/systemd/system/nextcloud-jobs.service<br>* Deploy /etc/systemd/system/nextcloud-jobs.timer<br>* Deploy /etc/systemd/system/nextcloud-app-update.service<br>* Deploy /etc/systemd/system/nextcloud-app-update.timer |
| `nextcloud:selinux`       | * semanage fcontext -a -t ...<br>* setsebool -P ... |
| `nextcloud:state`         | * systemctl enable/disable nextcloud-jobs.timer --now<br>* systemctl enable/disable nextcloud-app-update.timer --now |
| `nextcloud:sysconfig`     | * Set nextcloud system settings<br>* Set nextcloud proxy settings<br>* Convert some database columns to big int<br>* nextcloud: restart php-fpm |
| `nextcloud:update_script` | Deploy /usr/local/bin/nextcloud-update |
| `nextcloud:user`          | * Create Nextcloud user<br>* Update Nextcloud settings for user |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `nextcloud__fqdn` | The FQDN for the Nextcloud instance. |
| `nextcloud__users` | List of user accounts to create. Attention: The first user has to be the primary administrator account. |

Example:
```yaml
# mandatory
nextcloud__fqdn: 'cloud.example.com'
nextcloud__users:
  # first user has to be the admin account
  - username: 'nextcloud-admin'
    password: 'linuxfabrik'
    group: 'admin'
    settings:
      - 'core lang en'
      - 'core locale de_CH'
      - 'core timezone Europe/Zurich'
      - 'files quota "50 MB"'
      - 'firstrunwizard show 0'
      - 'settings email info@example.org'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `nextcloud__apache_httpd__vhosts__group_var` / `nextcloud__apache_httpd__vhosts__host_var` | The Apache vHost definition for the Nextcloud instance. | Have a look at [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/nextcloud/defaults/main.yml) |
| `nextcloud__apps` | List of Nextcloud Apps to install. Possible options:<br> * `name`: Mandatory, string. The app name.<br> * `state`: Mandatory, string. State of the app, one of `present`, `absent`. | `[]` |
| `nextcloud__apps_config` | List of Key/Value pairs for configuring Apps in Nextcloud via OCC. | Have a look at [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/nextcloud/defaults/main.yml) |
| `nextcloud__database_host` | Host where MariaDB is located. | `'localhost'` |
| `nextcloud__database_name` | Name of the Nextcloud database in MariaDB. | `'nextcloud'` |
| `nextcloud__datadir` | Where to store the user files. | `'/data'` |
| `nextcloud__mariadb_login` | The user account for the database administrator. | `'{{ mariadb_server__admin_user }}'` |
| `nextcloud__config_php_objectstore_s3` | S3 Storage Backend. Have a look at the example below on how to configure. | unset |
| `nextcloud__objectstore_swift` | Swift Storage Backend. Have a look at the example below on how to configure. | unset |
| `nextcloud__on_calendar_app_update` | Time to update Nextcloud Apps (Systemd-Timer notation). | `'06,18,23:{{ 59 \| random(seed=inventory_hostname) }}'` |
| `nextcloud__on_calendar_jobs`| Run interval of OCC background jobs. | `'*:0/5'` |
| `nextcloud__php__ini_max_execution_time__group_var` / `nextcloud__php__ini_max_execution_time__host_var` | [php.net](https://www.php.net/manual/en/info.configuration.php) | `'3600` |
| `nextcloud__php__ini_max_file_uploads__group_var` / `nextcloud__php__ini_max_file_uploads__host_var` | [php.net](https://www.php.net/manual/en/ini.core.php) | `'100` |
| `nextcloud__php__ini_memory_limit__group_var` / `nextcloud__php__ini_memory_limit__host_var` | [php.net](https://www.php.net/manual/en/ini.core.php) | `'1024M'` |
| `nextcloud__php__ini_post_max_size__group_var` / `nextcloud__php__ini_post_max_size__host_var` | [php.net](https://www.php.net/manual/en/ini.core.php) | `'16M'` |
| `nextcloud__php__ini_upload_max_filesize__group_var` / `nextcloud__php__ini_upload_max_filesize__host_var` | [php.net](https://www.php.net/manual/en/ini.core.php) | `'10000M'` |
| `nextcloud__php__modules__group_var` / `nextcloud__php__modules__host_var` | List of PHP modules that need to be installed via the standard package manager. | Have a look at [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/nextcloud/defaults/main.yml) |
| `nextcloud__config_php_proxy` | List of Key/Value pairs for configuring Nextcloud behind a reverse proxy via OCC. Have a look at the example below on how to configure. The IP addresses are those of the reverse proxy. | unset |
| `nextcloud__sysconfig` | List of Key/Value pairs for configuring Nextcloud itself via OCC. | Have a look at [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/nextcloud/defaults/main.yml) |
| `nextcloud__timer_app_update_enabled` | Enables/disables Systemd-Timer for updating Apps. | `true` |
| `nextcloud__timer_jobs_enabled` | Enables/disables Systemd-Timer for running OCC background jobs. | `true` |
| nextcloud__users | List of user accounts to create. Attention: The first user has to be the primary administrator account. | 
| `nextcloud__version` | Which version to install. Some of `'latest-XX'` or `'nextcloud-XX.X.XX'`. | `'latest-24'` |

Example:
```yaml
# optional
nextcloud__apps:
  - name: 'bruteforcesettings'
    state: 'present'
  - name: 'weather'
    state: 'absent'
nextcloud__config_php_objectstore_s3_autocreate: true
nextcloud__config_php_objectstore_s3_bucket: 'mybucket'
nextcloud__config_php_objectstore_s3_hostname: 's3.example.com'
nextcloud__config_php_objectstore_s3_key: 'a58387f0-76c3-43f0-bbfc-53428d5b9bfa'
nextcloud__config_php_objectstore_s3_region: 'us-east-1'
nextcloud__config_php_objectstore_s3_secret: 'linuxfabrik'
nextcloud__config_php_objectstore_s3_use_path_style: true
nextcloud__config_php_objectstore_s3_use_ssl: true
nextcloud__config_php_objectstore_swift_autocreate: true
nextcloud__config_php_objectstore_swift_bucket: 'mybucket'
nextcloud__config_php_objectstore_swift_region_name: 'us-east-1'
nextcloud__config_php_objectstore_swift_scope_project_domain_name: 'scope_project_domain_name'
nextcloud__config_php_objectstore_swift_scope_project_name: 'scope_project_name'
nextcloud__config_php_objectstore_swift_service_name: 'service_name'
nextcloud__config_php_objectstore_swift_tenant_name: 'tenant_name'
nextcloud__config_php_objectstore_swift_url: 'https://swift.example.com:5000/v3'
nextcloud__config_php_objectstore_swift_user_domain_name: 'default'
nextcloud__config_php_objectstore_swift_user_name: 'swift'
nextcloud__config_php_objectstore_swift_user_password: 'linuxfabrik'
nextcloud__config_php_proxy_overwrite_cond_addr: '^192\\.0\\.2\\.4$'
nextcloud__config_php_proxy_overwritehost: 'cloud.example.com'
nextcloud__config_php_proxy_overwriteprotocol: 'https'
nextcloud__config_php_proxy_overwritewebroot: '/'
nextcloud__config_php_proxy_trusted_proxies:
  - '192.0.2.4'
nextcloud__config_php_redis_dbindex: 0
nextcloud__config_php_redis_host: '127.0.0.1'
nextcloud__config_php_redis_port: 6379
nextcloud__config_php_redis_timeout: 0.75
nextcloud__database_host: 'localhost'
nextcloud__database_name: 'nextcloud'
nextcloud__datadir: '/data'
nextcloud__mariadb_login: '{{ mariadb_server__admin_user }}'
nextcloud__on_calendar_app_update: '06,18,23:{{ 59 | random(seed=inventory_hostname) }}'
nextcloud__on_calendar_jobs: '*:0/5'
nextcloud__timer_app_update_enabled: true
nextcloud__timer_jobs_enabled: true
nextcloud__version: 'latest-24'
```

## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
