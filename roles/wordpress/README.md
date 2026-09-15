# Ansible Role linuxfabrik.lfops.wordpress

This role installs and configures the [WordPress CMS](https://wordpress.com/).

Attention: It is intended that when you call `wordpress__url` you will get a white page because no theme is installed. `wordpress__url` followed by `/wp-admin` works as expected.


*Available since LFOps `2.0.0`.*


## Dependent Roles

Any [LFOps playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/README.md) that installs this role runs these for you. Optional ones can be disabled via the playbook's skip variables.

* A web server (for example Apache httpd) must be installed, with a virtual host configured for WordPress (role: [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd)).
* MariaDB 10+ must be installed (role: [linuxfabrik.lfops.mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server)).
* PHP 7+ must be installed (role: [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php)).


## Tags

`wordpress`

* Installs and configures wordpress.
* Triggers: none.

`wordpress:export`

* Exports the site content (posts, pages, comments, custom fields, categories and tags) as a wxr file to `/backup/wordpress-export`, which only `apache` and `root` can read.
* Triggers: none.

`wordpress:file_policy`

* `chown -R --changes apache:apache {{ wordpress__install_dir }}`.
* `restorecon -Fvr {{ wordpress__install_dir }}`.
* Triggers: none.

`wordpress:update`

* Updates the WordPress core to `wordpress__version`. Also applies all DB migrations, and updates all plugins and themes.
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

* The URL under which WordPress is reachable, including `http://` or `https://`. Use the URL your users type in the browser, which with a reverse proxy that terminates TLS in front is an `https://` URL even though Apache httpd on the host serves plain HTTP.
* It is the single source for the site address: WordPress is installed with it, and the role sets `home` and `siteurl` to it on every run, so an address changed in the WordPress settings is set back. With `https://`, WordPress builds its links for HTTPS and marks its login cookies `Secure`, and the role forces HTTPS for the login and the admin area. The host part becomes the `ServerName` of the vHost and the default installation directory.
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

* The name of the database.
* Type: String.
* Default: `'wordpress'`

`wordpress__disallow_file_edit`

* Prevent editing of plugin / theme files from the admin WebGUI. Strongly recommended to set this to `true` for security reasons.
* Type: Bool.
* Default: `true`

`wordpress__install_dir`

* The installation directory for WordPress.
* Type: String.
* Default: `/var/www/html/` followed by the host part of `wordpress__url`, for example `'/var/www/html/wordpress.example.com'`

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

* Path to a WXR export file which will be imported after installing WordPress. The file includes posts, pages, comments, custom fields, categories and tags, and can be created using the [wp-cli export function](https://developer.wordpress.org/cli/commands/export/) or the `wordpress:export` tag.
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
wordpress__plugins:
  - name: 'bbPress'
    state: 'present'
  - name: 'Akismet'
    state: 'absent'
wordpress__theme: 'twentysixteen'
wordpress__trusted_proxies:
  - '192.0.2.10'
wordpress__version: 'latest'
wordpress__wxr_export: '/tmp/wordpress.xml'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
