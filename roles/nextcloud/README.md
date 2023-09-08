# Ansible Role linuxfabrik.lfops.nextcloud

This role installs Nextcloud including the tools needed by the most popular business plugins. By default, the latest available version is installed. You can choose wether to use
* local block storage (default)
* S3 object storage backend (by providing `nextcloud__storage_backend_s3`)
* Swift object storage backend (by providing `nextcloud__storage_backend_swift`)

After installing Nextcloud, head over to your http(s)://nextcloud/index.php/settings/admin to set or verify your email server configuration. Afterwards, use the "Send email" button below the form to verify your settings.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Install a web server (for example Apache httpd), and configure a virtual host for Nextcloud. This can be done using the [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role.
* Install MariaDB 10.6+. This can be done using the [linuxfabrik.lfops.mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server) role.
* Install PHP 8.1+. This can be done using the [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) and [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role.
* Install Redis 7+. This can be done using the [linuxfabrik.lfops.repo_redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_redis) and [linuxfabrik.lfops.redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis) role.
* Set the size of your `/tmp` partition accordingly. For example: If you want to allow 5x simultaenous uploads with files each 10 GB in size, set it to 50 GB+.

If you use the ["Setup Nextcloud" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_nextcloud.yml), this installation is automatically done for you (you still have to take care of providing the required versions).


## Optional Requirements

* Install Redis. This can be done using the [linuxfabrik.lfops.redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis) role.
* Install Collabora. This can be done using the [linuxfabrik.lfops.collabora](https://github.com/Linuxfabrik/lfops/tree/main/roles/collabora) role.
* Install Coturn for Nextcloud Talk. This can be done using the [linuxfabrik.lfops.coturn](https://github.com/Linuxfabrik/lfops/tree/main/roles/coturn) role.

If you use the ["Setup Nextcloud" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_nextcloud.yml), this is automatically done for you.


## Tags

| Tag                       | What it does |
| ---                       | ------------ |
| `nextcloud`               | * Install bzip2 samba-client<br> * `wget https://download.nextcloud.com/server/releases/{{ nextcloud__version }}.tar.bz2`<br> * `bunzip /tmp/nextcloud-{{ nextcloud__version }}.tar.bz2 /var/www/html/`<br> * Storage Backend: Deploy `/var/www/html/nextcloud/config/objectstore.config.php`<br> * `chown -R apache:apache /var/www/html/nextcloud`<br> * `mkdir path/to/data; chown -R apache:apache path/to/data; chmod 0750 -R path/to/data`<br> * `chmod +x /var/www/html/nextcloud/occ`<br> * `restorecon -Fvr ...`<br> * Run nextcloud installer<br> * Convert some database columns to big int<br> * Set Nextcloud system settings<br> * Set Nextcloud proxy settings<br> * nextcloud: restart php-fpm<br> * Register if role state file exists<br> * Disable every possible Nextcloud App on initial setup, but do this only once<br> * Install and enable Nextcloud Apps on initial setup, but do this only once<br> * Enable a subset of pre-installed Nextcloud Apps on initial setup, but do this only once<br> * Create a role state file<br> * Disable Nextcloud Apps<br> * Install Nextcloud Apps<br> * Enable Nextcloud Apps<br> * Set Nextcloud App Settings<br> * `chown -R apache:apache /var/www/html/nextcloud`<br> * Deploy `/etc/systemd/system/nextcloud-jobs.service`<br> * Deploy `/etc/systemd/system/nextcloud-jobs.timer`<br> * Set background job to "cron"<br> * Deploy `/etc/systemd/system/nextcloud-app-update.service`<br> * Deploy `/etc/systemd/system/nextcloud-app-update.timer`<br> * Deploy /etc/systemd/system/nextcloud-scan-files.service<br> * Deploy /etc/systemd/system/nextcloud-scan-files.timer<br> * Deploy `/etc/systemd/system/nextcloud-ldap-show-remnants.service`<br> * Deploy `/etc/systemd/system/nextcloud-ldap-show-remnants.timer`<br> * Deploy `/usr/local/bin/nextcloud-ldap-show-remnants`<br> * `systemctl enable/disable nextcloud-jobs.timer --now`<br> * `systemctl enable/disable nextcloud-app-update.timer --now`<br> * `systemctl enable/disable nextcloud-scan-files.timer --now`<br> * `systemctl enable/disable nextcloud-ldap-show-remnants.timer --now`<br> * Deploy `/usr/local/bin/nextcloud-update` |
| `nextcloud:apps`          | * Disable Nextcloud Apps<br> * Install Nextcloud Apps<br> * Enable Nextcloud Apps<br> * Set Nextcloud App Settings |
| `nextcloud:cron`          | * Deploy `/etc/systemd/system/nextcloud-jobs.service`<br> * Deploy `/etc/systemd/system/nextcloud-jobs.timer`<br> * Set background job to "cron"<br> * Deploy `/etc/systemd/system/nextcloud-app-update.service`<br> * Deploy `/etc/systemd/system/nextcloud-app-update.timer`<br> * Deploy /etc/systemd/system/nextcloud-scan-files.service<br> * Deploy /etc/systemd/system/nextcloud-scan-files.timer<br> * Deploy `/etc/systemd/system/nextcloud-ldap-show-remnants.service`<br> * Deploy `/etc/systemd/system/nextcloud-ldap-show-remnants.timer`<br> * Deploy `/usr/local/bin/nextcloud-ldap-show-remnants`<br> * `systemctl enable/disable nextcloud-jobs.timer --now`<br> * `systemctl enable/disable nextcloud-app-update.timer --now`<br> * `systemctl enable/disable nextcloud-scan-files.timer --now`<br> * `systemctl enable/disable nextcloud-ldap-show-remnants.timer --now`<br> * Deploy `/usr/local/bin/nextcloud-update` |
| `nextcloud:state`         | * `systemctl enable/disable nextcloud-jobs.timer --now`<br> * `systemctl enable/disable nextcloud-app-update.timer --now` |
| `nextcloud:scripts` | * Deploy `/usr/local/bin/nextcloud-update` |
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
| `nextcloud__apache_httpd__vhosts_virtualhost_ip` | String. Used within the `<VirtualHost {{ virtualhost_ip }}:{{ virtualhost_port }}>` directive. | `*` |
| `nextcloud__apache_httpd__vhosts_virtualhost_port` | Number. Used within the `<VirtualHost {{ virtualhost_ip }}:{{ virtualhost_port }}>` directive. | `80` |
| `nextcloud__apps` | List of Nextcloud Apps to install. Possible options:<br> * `name`: Mandatory, string. The app name.<br> * `state`: Mandatory, string. State of the app, one of `present`, `absent`. | `[]` |
| `nextcloud__apps_config` | List of Key/Value pairs for configuring Apps in Nextcloud via OCC. | Have a look at [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/nextcloud/defaults/main.yml) |
| `nextcloud__database_host` | Host where MariaDB is located. | `'localhost'` |
| `nextcloud__database_name` | Name of the Nextcloud database in MariaDB. | `'nextcloud'` |
| `nextcloud__datadir` | Where to store the user files. | `'/data'` |
| `nextcloud__mariadb_login` | The user account for the database administrator. | `'{{ mariadb_server__admin_user }}'` |
| `nextcloud__on_calendar_app_update` | Time to update Nextcloud Apps (Systemd-Timer notation). | `'06,18,23:{{ 59 \| random(seed=inventory_hostname) }}'` |
| `nextcloud__on_calendar_jobs`| Run interval of OCC background jobs. | `'*:0/5'` |
| `nextcloud__on_calendar_scan_files`| Run interval of rescanning filesystem. | `'*:50:15'` |
| `nextcloud__php__ini_max_execution_time__group_var` / `nextcloud__php__ini_max_execution_time__host_var` | [php.net](https://www.php.net/manual/en/info.configuration.php) | `'3600` |
| `nextcloud__php__ini_max_file_uploads__group_var` / `nextcloud__php__ini_max_file_uploads__host_var` | [php.net](https://www.php.net/manual/en/ini.core.php) | `'100` |
| `nextcloud__php__ini_memory_limit__group_var` / `nextcloud__php__ini_memory_limit__host_var` | [php.net](https://www.php.net/manual/en/ini.core.php) | `'1024M'` |
| `nextcloud__php__ini_post_max_size__group_var` / `nextcloud__php__ini_post_max_size__host_var` | [php.net](https://www.php.net/manual/en/ini.core.php) | `'16M'` |
| `nextcloud__php__ini_upload_max_filesize__group_var` / `nextcloud__php__ini_upload_max_filesize__host_var` | [php.net](https://www.php.net/manual/en/ini.core.php) | `'10000M'` |
| `nextcloud__php__modules__group_var` / `nextcloud__php__modules__host_var` | List of PHP modules that need to be installed via the standard package manager. | Have a look at [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/nextcloud/defaults/main.yml) |
| `nextcloud__proxyconfig` | List of Key/Value pairs for [configuring Nextcloud behind a reverse proxy](https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/reverse_proxy_configuration.html) via OCC. The IP addresses are those of the reverse proxy. | unset. Have a look at the example below on how to configure. |
| `nextcloud__storage_backend_s3` | S3 Storage Backend. If ommitted, local storage is used. If both S3 and Swift are provided, S3 is configured. | unset. Have a look at the example below on how to configure. |
| `nextcloud__storage_backend_swift` | Swift Storage Backend. If ommitted, local storage is used. If both S3 and Swift are provided, S3 is configured. | unset. Have a look at the example below on how to configure. |
| `nextcloud__sysconfig` | List of Key/Value pairs for configuring Nextcloud itself via OCC. | Have a look at [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/nextcloud/defaults/main.yml) |
| `nextcloud__timer_app_update_enabled` | Enables/disables Systemd-Timer for updating Apps. | `false` |
| `nextcloud__timer_jobs_enabled` | Enables/disables Systemd-Timer for running OCC background jobs. | `true` |
| `nextcloud__timer_ldap_show_remnants_enabled` | Enables/disables Systemd-Timer for mailing once a month which users are not available on LDAP anymore, but have remnants in Nextcloud. Will only be applied if the app `users_ldap` is present. | `true` |
| `nextcloud__version` | Which version to install. One of `'latest'`, `'latest-XX'` or `'nextcloud-XX.X.XX'`. Have a look at https://download.nextcloud.com/server/releases/ for a list of available releases. | `'latest'` |

Example:
```yaml
# optional
nextcloud__apps:
  - name: 'bruteforcesettings'
    state: 'present'
  - name: 'weather'
    state: 'absent'

nextcloud__database_host: 'localhost'
nextcloud__database_name: 'nextcloud'

nextcloud__datadir: '/data'

nextcloud__mariadb_login: '{{ mariadb_server__admin_user }}'

nextcloud__on_calendar_app_update: '06,18,23:{{ 59 | random(seed=inventory_hostname) }}'
nextcloud__on_calendar_jobs: '*:0/5'
nextcloud__on_calendar_scan_files: '*:50:15'

nextcloud__proxyconfig:
  - { key: 'overwrite.cli.url', value: '--value=https://cloud.example.com' }
  - { key: 'overwritecondaddr', value: '--value=^192\\.0\\.2\\.7$' }
  - { key: 'overwritehost',     value: '--value=cloud.example.com' }
  - { key: 'overwriteprotocol', value: '--value=https' }
  - { key: 'overwritewebroot',  value: '--value=/' }
  - { key: 'trusted_proxies',   value: '0 --value=192.0.2.7' }

# if not local storage, then either one of s3 ...
nextcloud__storage_backend_s3:
  autocreate: true
  bucket: 'mybucket'
  hostname: 's3.pub1.infomaniak.cloud'
  key: '428fc7e2-b532-4704-9df0-a764c7253a15'
  port: 9000
  region: 'us-east-1'
  secret: 'linuxfabrik'
  use_path_style: true
  use_ssl: true

# ... or swift
nextcloud__storage_backend_swift:
  autocreate: true
  bucket: 'mybucket'
  region: 'dc3-a'
  scope_project_domain_name: 'Default'
  scope_project_name: 'PCP-XXXXXX'
  service_name: 'swift'
  url: 'https://api.pub1.infomaniak.cloud/identity/v3'
  user_domain_name: 'Default'
  user_name: 'PCU-XXXXXX'
  user_password: 'linuxfabrik'

nextcloud__timer_app_update_enabled: true
nextcloud__timer_jobs_enabled: true
nextcloud__timer_ldap_show_remnants_enabled: true

nextcloud__version: 'latest'
```

## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
