# Ansible Role linuxfabrik.lfops.wordpress

This role installs and configures the [WordPress CMS](https://wordpress.com/).

Attention: It is intended that when you call `wordpress__url` you will get a white page because no theme is installed. `wordpress__url` followed by `/wp-admin` works as expected.


*Available since LFOps `2.0.0`.*


## How the Role Behaves

* The WordPress core, `wp-config.php` and `wp-content/mu-plugins` belong to `root`, so code running in the web server cannot modify them. `wp-content` belongs to `apache`, so plugins, themes, translations and uploads can still be installed and updated from the web interface (`FS_METHOD` is `direct`).
* WordPress therefore cannot update its core itself, and its automatic core updates are switched off (`WP_AUTO_UPDATE_CORE`). `wordpress-core-minor-update-<instance>.timer` installs the latest minor release daily instead and reloads a running PHP-FPM afterwards, and `--tags wordpress:update` installs `wordpress__version`. The update button for the core in the web interface fails.
* WP-CLI runs as `root` only for commands that do not load WordPress (core download, config, checksum verification). Everything that loads WordPress runs as `apache`, because loading it executes code from `wp-content`, which `apache` can write.
* WordPress cannot write `.htaccess`, so pretty permalinks need either the `FallbackResource` from "Post-Installation Steps", or the rewrite rules WordPress displays after a change of the permalink structure, added to `.htaccess` by hand.
* Everything that exists once per WordPress instance carries the host and path of `wordpress__url` as the name of the instance, with `/` replaced by `-` (`example.com`, `example.com-blog`): `wordpress-cron-<instance>.timer`, `wordpress-core-minor-update-<instance>.timer` and the export directory. The vHost belongs to the host name and is shared by all instances under it (`<host>.80.conf`). The role removes `wordpress-cron.timer` of older role versions, but not their vHost file `wordpress.conf`.
* The REST API only answers logged-in users. The role installs and activates the [Disable WP REST API](https://wordpress.org/plugins/disable-wp-rest-api/) plugin, and uninstalls the Disable REST API (`disable-json-api`) plugin where it is present. Anonymous requests to any route, including the routes of plugins installed later, get `401 rest_login_required`. The plugin has no settings, so a front-end feature that calls the REST API without a login, such as some contact forms, needs an exception in code.


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* A web server (for example Apache httpd) must be installed, with a virtual host configured for WordPress (role: [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd)).
* MariaDB 10+ must be installed (role: [linuxfabrik.lfops.mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server)).
* PHP 7+ must be installed (role: [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php)).


## Multiple Instances on One Host

Several WordPress instances can share a host as pseudo hosts in the inventory: one inventory host per instance, all with the same `ansible_host`, each with its own `wordpress__url`, `wordpress__database_name` and `wordpress__database_user`. The instances can use different host names (`https://blog.example.com`, `https://shop.example.com`), different paths under one host name (`https://example.com/blog`, `https://example.com/shop`), or both, including an instance at the root of a host name next to instances in its sub-paths. The instances share the web server, PHP-FPM and MariaDB, so:

* Instances under one host name share its vHost. Its document root is the installation directory without the path, for example `/var/www/html/example.com` for `/var/www/html/example.com/blog`, so if you set `wordpress__install_dir`, keep that part the same for all of them. Put settings for this vHost (`apache_httpd__vhosts__*_var`) into a group that contains exactly the pseudo hosts of this host name, or into the `host_vars` of the pseudo host if it is the only one. A pseudo host of another host name must not get them: the role injects only the vHost of its own host name, so there the entry lacks its `template` and the run aborts. `apache_httpd__vhosts__group_var` is a single variable, so a pseudo host must not be in two groups that set it, otherwise Ansible keeps only one of the values.
* Put everything that is not specific to one instance, such as `mariadb_server__admin_user`, `php__*` or `apache_httpd__*` settings other than the vHosts, into a group that contains all pseudo hosts of the machine, not into their `host_vars`. Pseudo hosts that disagree about a shared configuration file overwrite each other on every run. This includes values that are looked up per `inventory_hostname`, such as passwords from Bitwarden, and `mariadb_server__dump_on_calendar`, whose default depends on the `inventory_hostname`.
* Add the pseudo hosts to `lfops_setup_wordpress` only, and the real host to all other playbooks, such as `setup_basic` or the monitoring.
* Do not run the pseudo hosts of a machine in parallel, for example with `--forks 1` or one `--limit` after the other. Otherwise Ansible configures the same machine several times at once, which leads to package manager lock timeouts, overlapping service restarts and a broken initial MariaDB setup.
* All instances run as `apache`, so a vulnerable plugin in one instance can modify the `wp-content` and read the `wp-config.php` of every other instance on the host.


## Post-Installation Steps

* Enable automatic updates for the plugins, since the role leaves them to WordPress: in the web interface under Plugins > Installed Plugins, select all plugins and apply the bulk action "Enable Auto-updates", or run `sudo --user=apache /usr/local/bin/wp plugin auto-updates enable --all --path=/var/www/html/example.com`. Plugins installed later start with auto-updates off, so repeat this for them. WordPress updates the plugins in the background, triggered by `wordpress-cron-<instance>.timer`, and restores the previous version of an active plugin if the site shows a fatal error afterwards. For that check the host requests its own `wordpress__url`, so it has to reach it, behind a reverse proxy through the proxy: a request that cannot connect counts as a fatal error and rolls every update of an active plugin back.

* Let Apache hand requests for pretty permalinks to WordPress, so they work without rewrite rules in `.htaccess`. Add a `FallbackResource` for each instance to the `raw` variable of the vHost of its host name, where "Multiple Instances on One Host" puts the vHost settings. Each instance needs its own `<Directory>` block with the absolute path of its `index.php` in the URL; a relative path does not work for permalinks below the instance. A block for a sub-path takes precedence over the one of an instance at the root above it. The entry is merged into the vHost the role deploys, so `conf_server_name`, `virtualhost_port` and `raw` are enough. For example, with an instance at `https://example.com` and two at `https://other-example.com/instance1` and `https://other-example.com/instance2`:

    ```yaml
    # host_vars/example.com.yml, the only pseudo host of example.com
    apache_httpd__vhosts__host_var:
      - conf_server_name: 'example.com'
        virtualhost_port: 80
        raw: !unsafe |-
          <Directory /var/www/html/example.com>
              FallbackResource /index.php
          </Directory>
    ```

    ```yaml
    # group_vars/wordpress_other_example_com.yml, a group of the pseudo hosts other-example.com-instance1 and other-example.com-instance2
    apache_httpd__vhosts__group_var:
      - conf_server_name: 'other-example.com'
        virtualhost_port: 80
        raw: !unsafe |-
          <Directory /var/www/html/other-example.com/instance1>
              FallbackResource /instance1/index.php
          </Directory>
          <Directory /var/www/html/other-example.com/instance2>
              FallbackResource /instance2/index.php
          </Directory>
    ```


## Tags

`wordpress`

* Installs and configures wordpress.
* Triggers: none.

`wordpress:export`

* Exports the site content (posts, pages, comments, custom fields, categories and tags) as a wxr file to `/backup/wordpress-export/<instance>`, which only `apache` and `root` can read.
* Triggers: none.

`wordpress:file_policy`

* Gives the core, `wp-config.php` and `wp-content/mu-plugins` to `root` and the rest of `wp-content` to `apache`.
* `restorecon -Fvr {{ wordpress__install_dir }}`.
* Triggers: none.

`wordpress:update`

* Updates the WordPress core to `wordpress__version`. Also applies all DB migrations, and updates all plugins and themes.
* Reloads a running PHP-FPM after the core and again after the plugin and theme updates, so that OPcache does not keep serving old files.
* Triggers: none.


## Mandatory Role Variables

`wordpress__admin_email`

* The Email of the WordPress admin user.
* Type: String.

`wordpress__admin_user`

* The WordPress admin user account.
* Type: Dictionary.
* Subkeys:

    * `username`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Mandatory. Password.
        * Type: String.

`wordpress__database_user`

* The database user account with permissions on the `wordpress__database_name` database.
* Type: Dictionary.
* Subkeys:

    * `username`:

        * Mandatory. Username.
        * Type: String.

    * `password`:

        * Mandatory. Password.
        * Type: String.

`wordpress__site_title`

* The WordPress site title.
* Type: String.

`wordpress__url`

* The URL under which WordPress is reachable, including `http://` or `https://` and an optional path such as `/blog`, without a trailing slash. Use the URL your users type in the browser, which with a reverse proxy that terminates TLS in front is an `https://` URL even though Apache httpd on the host serves plain HTTP.
* It is the single source for the site address: WordPress is installed with it, and the role sets `home` and `siteurl` to it on every run, so an address changed in the WordPress settings is set back. With `https://`, WordPress builds its links for HTTPS and marks its login cookies `Secure`, and the role forces HTTPS for the login and the admin area. The host part becomes the `ServerName` of the vHost, and host and path the default installation directory.
* Type: String.

Example:
```yaml
# mandatory
wordpress__admin_email: 'webmaster@example.com'
wordpress__admin_user:
  username: 'wordpress-admin'
  password: 'linuxfabrik'
wordpress__database_user:
  username: 'wordpress'
  password: 'linuxfabrik'
wordpress__site_title: 'WordPress Test Site'
wordpress__url: 'https://wordpress.example.com'
```


## Optional Role Variables

`wordpress__application_passwords_enabled`

* Whether users can create application passwords, with which REST API clients such as the WordPress mobile app or external integrations log in. The role switches them on or off through the must-use plugin `wp-content/mu-plugins/linuxfabrik.php`.
* Type: Bool.
* Default: `false`
* Deviates from the upstream default `true`: an application password logs a client in without a second factor, so it bypasses a two-factor plugin.

`wordpress__database_host`

* The host on which the database is accessible.
* Type: String.
* Default: `'localhost'`

`wordpress__database_name`

* The name of the database. Each instance on a host needs its own.
* Type: String.
* Default: `'wordpress'`

`wordpress__disallow_file_edit`

* Prevent editing of plugin / theme files from the admin WebGUI. Strongly recommended to set this to `true` for security reasons.
* Type: Bool.
* Default: `true`

`wordpress__install_dir`

* The installation directory for WordPress. For a `wordpress__url` with a path, it has to end with that path; the part before it becomes the document root of the vHost.
* Type: String.
* Default: `/var/www/html/` followed by the host and path of `wordpress__url`, for example `'/var/www/html/wordpress.example.com'` or `'/var/www/html/example.com/blog'`

`wordpress__on_calendar_core_minor_update`

* When `wordpress-core-minor-update-<instance>.timer` installs the latest minor release of the WordPress core (systemd timer notation).
* Type: String.
* Default: `'04:{{ 59 | random(seed=inventory_hostname) }}'`

`wordpress__plugins`

* List of WordPress plugin slugs. To get a list of already installed plugins, use the WordPress CLI `sudo -u apache /usr/local/bin/wp plugin list --status=active`.
* Type: List of dictionaries.
* Default: `[]`
* Subkeys:

    * `name`:

        * Mandatory. Plugin slug, path to a local zip file, or URL to a remote zip file.
        * Type: String.

    * `state`:

        * Optional. Either `'present'` or `'absent'`.
        * Type: String.
        * Default: `'present'`

`wordpress__theme`

* The WordPress theme to install. Accepts a theme slug, the path to a local zip file, or a URL to a remote zip file.
* Type: String.
* Default: unset

`wordpress__timer_core_minor_update_enabled`

* Enables or disables `wordpress-core-minor-update-<instance>.timer`, which installs the latest minor release of the WordPress core. With the timer disabled, the core only changes with `--tags wordpress:update`.
* Type: Bool.
* Default: `true`

`wordpress__trusted_proxies`

* IP addresses of the reverse proxies in front of WordPress. Only on requests from one of them does WordPress take the client address from the `X-Forwarded-For` header, because any client can send that header. List every proxy of a chain, individual addresses only, no CIDR ranges.
* Leave it empty for a WordPress that clients reach directly. Behind a proxy that is not listed, WordPress sees the proxy's address for every visitor, for example in comments and in login-limiting plugins.
* Type: List of strings.
* Default: `[]`

`wordpress__version`

* The WordPress version to install. Possible options: version number, `'latest'`, `'nightly'`.
* Type: String.
* Default: `'latest'`

`wordpress__wxr_export`

* Path to a WXR export file on the managed host, readable by `apache`, which will be imported when the role installs WordPress. The file includes posts, pages, comments, custom fields, categories and tags, and can be created using the [wp-cli export function](https://developer.wordpress.org/cli/commands/export/) or the `wordpress:export` tag.
* Type: String.
* Default: unset

Example:
```yaml
# optional
wordpress__application_passwords_enabled: true
wordpress__database_host: 'localhost'
wordpress__database_name: 'wordpress'
wordpress__disallow_file_edit: true
wordpress__install_dir: '/var/www/html/wordpress.example.com'
wordpress__on_calendar_core_minor_update: '04:30'
wordpress__plugins:
  - name: 'bbPress'
    state: 'present'
  - name: 'Akismet'
    state: 'absent'
wordpress__theme: 'twentysixteen'
wordpress__timer_core_minor_update_enabled: true
wordpress__trusted_proxies:
  - '192.0.2.10'
wordpress__version: 'latest'
wordpress__wxr_export: '/tmp/wordpress.xml'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
