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
* Set the size of your `/tmp` partition accordingly. For example: If you want to allow 5x simultaneous uploads with files each 10 GB in size, set it to 50 GB+.

If you use the ["Setup Nextcloud" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_nextcloud.yml), this is automatically done for you (you still have to take care of providing the required versions).


## Optional Requirements

* Install Collabora. This can be done using the [linuxfabrik.lfops.collabora](https://github.com/Linuxfabrik/lfops/tree/main/roles/collabora) role.
* Install Coturn for Nextcloud Talk. This can be done using the [linuxfabrik.lfops.coturn](https://github.com/Linuxfabrik/lfops/tree/main/roles/coturn) role.

If you use the ["Setup Nextcloud" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_nextcloud.yml), this is automatically done for you.


## Tags

| Tag                       | What it does |
| ---                       | ------------ |
| `nextcloud`               | Installs and configures the whole Nextcloud server |
| `nextcloud:apps`          | Enables, disables apps and sets their settings |
| `nextcloud:configure`     | Deploys the `nextcloud_sysconfig` and the `nextcloud__proxyconfig` |
| `nextcloud:cron`          | Sets the Nextcloud background job setting to cron, deploys and manages the state of: <ul><li>`nextcloud-app-update.{service,timer}`</li><li>`nextcloud-jobs.{service,timer}`</li><li>`nextcloud-ldap-show-remnants.{service,timer}`</li><li>`nextcloud-ldap-show-remnants` script</li><li>`nextcloud-scan-files.{service,timer}`</li></ul> |
| `nextcloud:scripts`       | Deploys `/usr/local/bin/nextcloud-update` |
| `nextcloud:state`         | Manages the state of: <ul><li>`nextcloud-jobs.timer`</li><li>`nextcloud-app-update.timer`</li><li>`nextcloud-scan-files.timer`</li><li>`nextcloud-ldap-show-remnants.timer`</li></ul> |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `nextcloud__fqdn` | The FQDN of the Nextcloud instance. |
| `nextcloud__users` | List of dictionaries containing the user accounts to create. Attention: The first user has to be the primary administrator account. Subkeys: <ul><li>`username`: Mandatory, string. Username.</li><li>`password`: Mandatory, string. Password.</li><li>`group`: Optional, string. Group of the user. Defaults to none.</li><li>`settings`: Optional, list of strings. Nextcloud settings for the user. Have a look at the example below. Defaults to `[]`.</li></ul> |

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
| `nextcloud__apps_config` | List of Key/Value pairs for configuring Apps in Nextcloud via OCC. | Have a look at [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/nextcloud/defaults/main.yml) |
| `nextcloud__apps` | List of Nextcloud Apps to install. Subkeys:<br> * `name`: Mandatory, string. The app name.<br> * `state`: Optional, string. State of the app, either `present` or `absent`. Defaults to `present`. | `[]` |
| `nextcloud__database_host` | Host where MariaDB is located. | `'localhost'` |
| `nextcloud__database_name` | Name of the Nextcloud database in MariaDB. | `'nextcloud'` |
| `nextcloud__datadir` | Where to store the user files. | `'/data'` |
| `nextcloud__mariadb_login` | The user account for the database administrator. The Nextcloud setup will create its own database account. | `'{{ mariadb_server__admin_user }}'` |
| `nextcloud__on_calendar_app_update` | Time to update the Nextcloud Apps. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format. | `'06,18,23:{{ 59 \| random(seed=inventory_hostname) }}'` |
| `nextcloud__on_calendar_jobs`| Run interval of OCC background jobs. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format. | `'*:0/5'` |
| `nextcloud__on_calendar_scan_files`| Run interval of rescanning filesystem. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format. | `'*:50:15'` |
| `nextcloud__proxyconfig` | List of dictionaries for [configuring Nextcloud behind a reverse proxy](https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/reverse_proxy_configuration.html) via OCC. The IP addresses are those of the reverse proxy. Have a look at the example below on how to configure. | unset |
| `nextcloud__storage_backend_s3` | S3 Storage Backend. If ommitted, local storage is used. If both S3 and Swift are provided, S3 is configured. Have a look at the example below on how to configure. | unset |
| `nextcloud__storage_backend_swift` | Swift Storage Backend. If ommitted, local storage is used. If both S3 and Swift are provided, S3 is configured. Have a look at the example below on how to configure. | unset |
| `nextcloud__sysconfig` | List of Key/Value pairs for configuring Nextcloud itself via OCC. | Have a look at [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/nextcloud/defaults/main.yml) |
| `nextcloud__timer_app_update_enabled` | Enables/disables Systemd-Timer for updating Apps. | `false` |
| `nextcloud__timer_jobs_enabled` | Enables/disables Systemd-Timer for running OCC background jobs. | `true` |
| `nextcloud__timer_ldap_show_remnants_enabled` | Enables/disables Systemd-Timer for mailing once a month which users are not available on LDAP anymore, but have remnants in Nextcloud. Will only be applied if the app `users_ldap` is present. | `true` |
| `nextcloud__timer_scan_files_enabled` | Enables/disables Systemd-Timer for re-scanning the Nextcloud files. | `true` |
| `nextcloud__version` | Which version to install. One of `'latest'`, `'latest-XX'` or `'nextcloud-XX.X.XX'`. Have a look at https://download.nextcloud.com/server/releases/ for a list of available releases. | `'latest'` |
| `nextcloud__vhost_virtualhost_ip` | String. Used within the `<VirtualHost {{ virtualhost_ip }}:{{ virtualhost_port }}>` directive. | `*` |
| `nextcloud__vhost_virtualhost_port` | Number. Used within the `<VirtualHost {{ virtualhost_ip }}:{{ virtualhost_port }}>` directive. | `80` |

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
nextcloud__timer_scan_files_enabled: true
nextcloud__version: 'latest'
nextcloud__vhost_virtualhost_ip: '127.0.0.1'
nextcloud__vhost_virtualhost_port: '81'
```

## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
