# Ansible Role linuxfabrik.lfops.wordpress

This role installs and configures the [WordPress CMS](https://wordpress.com/).

Attention: It is intended that when you call `http://{wordpress__url}}` you will get a white page because no theme is installed. `http://{wordpress__url}}/wp-admin` works as expected.


## Mandatory Requirements

* Install a web server (for example Apache httpd), and configure a virtual host for Nextcloud. This can be done using the [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role.
* Install MariaDB 10+. This can be done using the [linuxfabrik.lfops.mariadb_server](https://github.com/Linuxfabrik/lfops/tree/main/roles/mariadb_server) role.
* Install PHP 7+. This can be done using the [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role.

If you use the [WordPress Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/setup_wordpress.yml), this is automatically done for you.


## Tags

| Tag                | What it does                                                                                                            | Reload / Restart |
| ---                | ------------                                                                                                            | ---------------- |
| `wordpress`        | Installs and configures wordpress                                                                                       | - |
| `wordpress:export` | Exports the site content (posts, pages, comments, custom fields, categories and tags) as a wxr file.                    | - |
| `wordpress:file_policy` | * `chown -R --changes apache:apache {{ wordpress__install_dir  }}`<br> * `restorecon -Fvr {{ wordpress__install_dir }}` | - |
| `wordpress:update` | Updates the WordPress core to `wordpress__version`. Also applies all DB migrations, and updates all plugins and themes. | - |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `wordpress__admin_email` | The Email of the WordPress admin user. |
| `wordpress__admin_user` | The WordPress admin user account. Subkeys:<br> * `username`: Mandatory, string. Username<br> * `password`: Mandatory, string. Password |
| `wordpress__database_user` | The database user account with permissions on the `wordpress__database_name` database. Subkeys:<br> * `username`: Mandatory, string. Username<br> * `password`: Mandatory, string. Password |
| `wordpress__site_title` | The WordPress site title. |
| `wordpress__url` | The WordPress URL, without `http://` or `https://`.  |

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
wordpress__url: 'wordpress.example.com'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `wordpress__database_host` | The host on which the database is accessible. | `'localhost'` |
| `wordpress__database_name` | The name of the database. | `'wordpress'` |
| `wordpress__disallow_file_edit` | Prevent editing of plugin / theme files from the admin WebGUI. Strongly recommended to set this to `true` for security reasons. | `true` |
| `wordpress__install_dir` | The installation directory for WordPress. | `'/var/www/html/{{ wordpress__url }}'` |
| `wordpress__plugins` | List of WordPress plugin slugs. To get a list of already installed plugins, use the WordPress CLI `sudo -u apache /usr/local/bin/wp plugin list --status=active`. Subkeys: <br> * name: Mandatory, string. Plugin slug, path to a local zip file, or URL to a remote zip file. <br> * state: Optional, string. Either `'present'` or `'absent`' | `[]` |
| `wordpress__theme` | The WordPress theme to install. Accepts a theme slug, the path to a local zip file, or a URL to a remote zip file. | unset |
| `wordpress__version` | The WordPress version to install. Possible options: <br> * Version number <br> * `'latest'` <br> * `'nightly'` | `'latest'` |
| `wordpress__wxr_export` | Path to a WXR export file which will be imported after installing WordPress. The file includes posts, pages, comments, custom fields, categories and tags, and can be created using the [wp-cli export function](https://developer.wordpress.org/cli/commands/export/) or the `wordpress:export` tag. | unset |

Example:
```yaml
# optional
wordpress__database_host: 'localhost'
wordpress__database_name: 'wordpress'
wordpress__disallow_file_edit: true
wordpress__install_dir: '/var/www/html/{{ wordpress__url }}'
wordpress__plugins:
  - name: 'bbPress'
    state: 'present'
  - name: 'Akismet'
    state: 'absent'
wordpress__theme: 'twentysixteen'
wordpress__version: 'latest'
wordpress__wxr_export: '/tmp/wordpress.xml'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
