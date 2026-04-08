# Ansible Role linuxfabrik.lfops.nextcloud

This role installs Nextcloud including the tools needed by the most popular business plugins and [notify_push](https://github.com/nextcloud/notify_push). By default, the latest available version is installed. You can choose wether to use

* local block storage (default)
* S3 object storage backend (by providing `nextcloud__storage_backend_s3`)
* Swift object storage backend (by providing `nextcloud__storage_backend_swift`)

After installing Nextcloud, head over to your http(s)://nextcloud/index.php/settings/admin to set or verify your email server configuration. Afterwards, use the "Send email" button below the form to verify your settings.


## Mandatory Requirements

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Install a web server (for example Apache httpd), and configure a virtual host for Nextcloud. This can be done using the [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role.
* Install MariaDB 10.6+. This can be done using the [linuxfabrik.lfops.mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server) role.
* Install PHP 8.1+. This can be done using the [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) and [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role.
* Install Redis 7+. This can be done using the [linuxfabrik.lfops.repo_redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_redis) and [linuxfabrik.lfops.redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis) role.
* Set the size of your `/tmp` partition accordingly. For example: If you want to allow 5x simultaneous uploads with files each 10 GB in size, set it to 50 GB+.
* Configure the systemd service for [notify_push](https://github.com/nextcloud/notify_push).

If you use the ["Setup Nextcloud" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_nextcloud.yml), this is automatically done for you (you still have to take care of providing the required versions).


## Optional Requirements

* Install Collabora. This can be done using the [linuxfabrik.lfops.collabora](https://github.com/Linuxfabrik/lfops/tree/main/roles/collabora) role.
* Install Coturn for Nextcloud Talk. This can be done using the [linuxfabrik.lfops.coturn](https://github.com/Linuxfabrik/lfops/tree/main/roles/coturn) role.

If you use the ["Setup Nextcloud" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_nextcloud.yml), this is automatically done for you.


## Tags

`nextcloud`

* Installs and configures the whole Nextcloud server.
* Triggers: none.

`nextcloud:apps`

* Enables, disables apps and sets their settings.
* Triggers: none.

`nextcloud:configure`

* Deploys the `nextcloud__sysconfig__*_var` and configures notify_push.
* Triggers: none.

`nextcloud:cron`

* Sets the Nextcloud background job setting to cron, deploys and manages the state of `nextcloud-app-update.{service,timer}`, `nextcloud-jobs.{service,timer}`, `nextcloud-ldap-show-remnants.{service,timer}`, `nextcloud-ldap-show-remnants` script, `nextcloud-scan-files.{service,timer}`.
* Triggers: none.

`nextcloud:notify_push`

* Configures notify_push.
* Triggers: none.

`nextcloud:scripts`

* Deploys `/usr/local/bin/nextcloud-update`.
* Triggers: none.

`nextcloud:state`

* Manages the state of `nextcloud-jobs.timer`, `nextcloud-app-update.timer`, `nextcloud-scan-files.timer`, `nextcloud-ldap-show-remnants.timer`.
* Triggers: none.


## Mandatory Role Variables

`nextcloud__fqdn`

* The FQDN of the Nextcloud instance.
* Type: String.

`nextcloud__users`

* List of dictionaries containing the user accounts to create. Attention: The first user has to be the primary administrator account.
* Type: List of dictionaries.
* Subkeys:

    * `username`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Mandatory. Password.
        * Type: String.

    * `group`:

        * Optional. Group of the user.
        * Type: String.
        * Default: unset

    * `settings`:

        * Optional. Nextcloud settings for the user. Have a look at the example below.
        * Type: List of strings.
        * Default: `[]`

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

`nextcloud__app_configs__host_var` / `nextcloud__app_configs__group_var`

* List of dictionaries containing key-value pairs for configuring apps in Nextcloud.
* Type: List of dictionaries.
* Default: Have a look at [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/nextcloud/defaults/main.yml)
* Subkeys:

    * `key`:

        * Mandatory. The name of the config option to set.
        * Type: String.

    * `value`:

        * Mandatory. The configuration value.
        * Type: String.

    * `force`:

        * Optional. Set to `true` to install the app regardless of the Nextcloud version requirement.
        * Type: Bool.

    * `state`:

        * Optional. Either `absent`, `disabled`, `enabled` or `present`. Note that `enabled` also installs the app.
        * Type: String.
        * Default: `'enabled'`

`nextcloud__apps__host_var` / `nextcloud__apps__group_var`

* List of dictionaries containing Nextcloud apps to install.
* Type: List of dictionaries.
* Default: Have a look at [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/nextcloud/defaults/main.yml)
* Subkeys:

    * `name`:

        * Mandatory. The app name.
        * Type: String.

    * `state`:

        * Optional. State of the app, either `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`nextcloud__database_host`

* Host where MariaDB is located.
* Type: String.
* Default: `'localhost'`

`nextcloud__database_name`

* Name of the Nextcloud database in MariaDB.
* Type: String.
* Default: `'nextcloud'`

`nextcloud__datadir`

* Where to store the user files.
* Type: String.
* Default: `'/data'`

`nextcloud__icinga2_api_url`

* The URL of the Icinga2 API (usually on the Icinga2 Master). This will be used to set a downtime for the corresponding host and all its services in the `/usr/local/bin/nextcloud-update` script.
* Type: String.
* Default: `'https://{{ icinga2_agent__icinga2_master_host | d("") }}:{{ icinga2_agent__icinga2_master_port | d(5665) }}'`

`nextcloud__icinga2_api_user_login`

* The Icinga2 API User to set the downtime for the corresponding host and all its services in the `/usr/local/bin/nextcloud-update` script.
* Type: Dictionary.
* Default: `'{{ system_update__icinga2_api_user_login }}'`

`nextcloud__icinga2_hostname`

* The hostname of the Icinga2 host on which the downtime should be set.
* Type: String.
* Default: `'{{ ansible_facts["nodename"] }}'`

`nextcloud__mariadb_login`

* The user account for the database administrator. The Nextcloud setup will create its own database account.
* Type: Dictionary.
* Default: `'{{ mariadb_server__admin_user }}'`

`nextcloud__on_calendar_app_update`

* Time to update the Nextcloud apps. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format.
* Type: String.
* Default: `'06,18,23:{{ 59 | random(seed=inventory_hostname) }}'`

`nextcloud__on_calendar_jobs`

* Run interval of OCC background jobs. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format.
* Type: String.
* Default: `'*:0/5'`

`nextcloud__on_calendar_scan_files`

* Run interval of rescanning filesystem. Have a look at [systemd.time(7)](https://www.freedesktop.org/software/systemd/man/systemd.time.html) for the format.
* Type: String.
* Default: `'*:50:15'`

`nextcloud__skip_apps`

* Completely skips the management of Nextcloud apps. Set this to prevent changes via the WebGUI from being overwritten.
* Type: Bool.
* Default: `false`

`nextcloud__skip_notify_push`

* Skips the configuration of notify_push. Use this if the DNS setup is not done yet when running the role.
* Type: Bool.
* Default: `false`

`nextcloud__storage_backend_s3`

* S3 Storage Backend. If ommitted, local storage is used. If both S3 and Swift are provided, S3 is configured. Have a look at the example below on how to configure.
* Type: Dictionary.
* Default: unset

`nextcloud__storage_backend_swift`

* Swift Storage Backend. If ommitted, local storage is used. If both S3 and Swift are provided, S3 is configured. Have a look at the example below on how to configure.
* Type: Dictionary.
* Default: unset

`nextcloud__sysconfig__host_var` / `nextcloud__sysconfig__group_var`

* List of dictionaries containing key-value pairs for Nextcloud system config settings. Also use this setting to configure [Nextcloud behind a reverse proxy](https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/reverse_proxy_configuration.html), have a look at the example below on how to configure.
* Type: List of dictionaries.
* Default: Have a look at [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/nextcloud/defaults/main.yml)
* Subkeys:

    * `key`:

        * Mandatory. The name of the config option to set.
        * Type: String.

    * `value`:

        * Mandatory. The configuration value.
        * Type: String.

    * `type`:

        * Optional. The type of the configuration value.
        * Type: String.
        * Default: `'string'`

    * `state`:

        * Optional. Either `present` or `absent`.
        * Type: String.
        * Default: `'present'`

`nextcloud__timer_app_update_enabled`

* Enables/disables Systemd-Timer for updating apps.
* Type: Bool.
* Default: `false`

`nextcloud__timer_jobs_enabled`

* Enables/disables Systemd-Timer for running OCC background jobs.
* Type: Bool.
* Default: `true`

`nextcloud__timer_ldap_show_remnants_enabled`

* Enables/disables Systemd-Timer for mailing once a month which users are not available on LDAP anymore, but have remnants in Nextcloud. Will only be applied if the app `users_ldap` is present.
* Type: Bool.
* Default: `true`

`nextcloud__timer_scan_files_enabled`

* Enables/disables Systemd-Timer for re-scanning the Nextcloud files.
* Type: Bool.
* Default: `true`

`nextcloud__version`

* Which version to install. One of `'latest'`, `'latest-XX'` or `'nextcloud-XX.X.XX'`. Have a look at https://download.nextcloud.com/server/releases/ for a list of available releases.
* Type: String.
* Default: `'latest'`

`nextcloud__vhost_virtualhost_ip`

* Used within the `<VirtualHost {{ virtualhost_ip }}:{{ virtualhost_port }}>` directive.
* Type: String.
* Default: `*`

`nextcloud__vhost_virtualhost_port`

* Used within the `<VirtualHost {{ virtualhost_ip }}:{{ virtualhost_port }}>` directive.
* Type: Number.
* Default: `80`

Example:
```yaml
# optional
nextcloud__app_configs__host_var:
  - key: 'core shareapi_default_expire_date'
    value: 'yes'
    state: 'present'
  - key: 'theming imprintUrl'
    value: 'https://www.example.com'
    state: 'present'
nextcloud__apps__host_var:
  - name: 'bruteforcesettings'
    state: 'present'
  - name: 'weather'
    state: 'absent'
nextcloud__database_host: 'localhost'
nextcloud__database_name: 'nextcloud'
nextcloud__datadir: '/data'
nextcloud__icinga2_api_url: 'https://icinga.example.com:5665'
nextcloud__icinga2_api_user_login:
  username: 'downtime-user'
  password: 'linuxfabrik'
nextcloud__icinga2_hostname: 'myhost.example.com'
nextcloud__mariadb_login: '{{ mariadb_server__admin_user }}'
nextcloud__on_calendar_app_update: '06,18,23:{{ 59 | random(seed=inventory_hostname) }}'
nextcloud__on_calendar_jobs: '*:0/5'
nextcloud__on_calendar_scan_files: '*:50:15'
nextcloud__skip_apps: true
nextcloud__skip_notify_push: true
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
nextcloud__sysconfig__host_var:
  - key: 'check_for_working_wellknown_setup'
    value: 'true'
    type: 'boolean'
    state: 'present'
  - key: 'updatechecker'
    value: 'false'
    type: 'boolean'
    state: 'present'
  - key: 'redis timeout'
    value: '0.5'
    type: 'double'
    state: 'present'
  # reverse proxy config
  - key: 'overwrite.cli.url '
    value: 'https://cloud.example.com'
    state: 'present'
  - key: 'overwritecondaddr '
    value: '^192\.0\.2\.7$' # IP of the reverse proxy
    state: 'present'
  - key: 'overwritehost '
    value: 'cloud.example.com'
    state: 'present'
  - key: 'overwriteprotocol '
    value: 'https'
    state: 'present'
  - key: 'overwritewebroot '
    value: '/'
    state: 'present'
  - key: 'trusted_proxies 0 '
    value: '192.0.2.7' # IP of the reverse proxy
    state: 'present'

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
