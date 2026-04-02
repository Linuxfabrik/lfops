# Ansible Role linuxfabrik.lfops.apache_httpd

This role installs and configures a CIS-compliant [Apache httpd](https://httpd.apache.org/).


## What this Role does

This role configures Apache using a Debian-style layout with `conf-available/conf-enabled`, `mods-available/mods-enabled`, and `sites-available/sites-enabled` directories. On Red Hat-based systems, this means a significant restructuring of the default Apache configuration. The goal is to make adding and removing mods, virtual hosts, and extra configuration directives as flexible as possible, regardless of the underlying platform.

The config is split into several files forming the configuration hierarchy outlined below, all located in the `/etc/httpd/` directory:

```
/etc/httpd/
`-- httpd.conf
`-- conf-available/
`-- conf-enabled/
`-- mods-available/
`-- mods-enabled/
`-- sites-available/
`-- sites-enabled/
```

We avoid using `<IfModule>` in vHost definitions and in the global `httpd.conf` to facilitate debugging. Without `<IfModule>`, a missing module causes a clear startup error instead of silently dropping configuration. `<IfModule>` is only used in `mods-available/` and `conf-available/` where it is necessary to guard module-specific configuration.

For flexibility, use the `raw` variable to configure the following topics (have a look at the "Apache vHost Configs" section for some examples):

* SSL/TLS Certificates.
* Quality of Service (`mod_qos` directives).
* Proxy passing rules.
* Any other configuration instructions not covered in the "Role Variables" chapters.

If you want to check Apache with [our STIG audit script](https://github.com/Linuxfabrik/stig), run it like this:

* Apache Application Server:<br>`./audit.py --lengthy --profile-name='CIS Apache HTTP Server 2.4' --profile-version='v2.0.0' --hostname=web --control-name-exclude='2\.4|2\.6|2\.8|5\.7|6\.6|6\.7`
* Apache Reverse Proxy Server:<br>`./audit.py --lengthy --profile-name='CIS Apache HTTP Server 2.4' --profile-version='v2.0.0' --hostname=proxy --control-name-exclude='2\.4|2\.6|2\.8|5\.7`


## What this Role doesn't do

* PHP: This role prefers the use of PHP-FPM over PHP, but it does not install either.
* SELinux: Use specialized roles to set specific SELinux Booleans, Policies etc.


## Platform-Specific Behavior

This role supports both Red Hat and Debian-based systems. Paths and service names differ between platforms:

* Config path: Red Hat `/etc/httpd`, Debian `/etc/apache2`
* Service name: Red Hat `httpd`, Debian `apache2`
* User/Group: Red Hat `apache`/`apache`, Debian `www-data`/`www-data`
* PHP-FPM socket: Red Hat `/run/php-fpm/www.sock`, Debian `/run/php/www.sock`

These differences are handled automatically. All documentation below uses Red Hat paths.


## Config Examples for vHosts

See [EXAMPLES.md](https://github.com/Linuxfabrik/lfops/blob/main/roles/apache_httpd/EXAMPLES.md).



## Mandatory Requirements

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Install the `python3-passlib` library. This can be done using the [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python) role.


## Optional Requirements

* Install PHP and configure PHP-FPM. This can be done using the [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role.



## Tags

`apache_httpd`

* Installs base packages and Apache packages/modules.
* Creates the `conf-available/conf-enabled`, `mods-available/mods-enabled`, `sites-available/sites-enabled` directory structure.
* Creates symlink for the log directory.
* Sets ownership on the document root (`chown -R apache:apache`).
* Hardens permissions on the config directory (`chmod -R g-w`).
* Ensures httpd service is in the desired state.
* Triggers: httpd.service reload.

`apache_httpd:config`

* Creates or updates the global Apache configuration (`httpd.conf`).
* Removes rpmnew/rpmsave files (and Debian equivalents).
* Removes, creates, disables, and enables conf-available configs.
* Triggers: httpd.service reload.

`apache_httpd:htpasswd`

* Creates or updates htpasswd flat-files for basic authentication.
* Triggers: none.

`apache_httpd:matomo`

* Deploys Matomo Log Analytics Python Script to `/usr/local/sbin/import_logs.py`.
* Triggers: none.

`apache_httpd:mod_security_coreruleset`

* Installs `tar`.
* Downloads and verifies the OWASP ModSecurity Core Rule Set (CRS).
* Extracts the archive and creates a symlink to the CRS directory.
* Copies the default `crs-setup.conf.example` to `crs-setup.conf`.
* Triggers: none.

`apache_httpd:mods`

* Installs base packages and Apache packages/modules.
* Creates the `conf-available/conf-enabled`, `mods-available/mods-enabled`, `sites-available/sites-enabled` directory structure.
* Removes, creates, disables, and enables mods-available configs.
* Triggers: httpd.service reload.

`apache_httpd:state`

* Ensures httpd service is in the desired state.
* Triggers: none.

`apache_httpd:vhosts`

* Disables and removes sites-available vHosts.
* Creates DocumentRoot directories for all vHosts.
* Creates and enables sites-available vHosts.
* Supports `apache_httpd__limit_vhosts` to deploy only specific vHosts.
* Triggers: httpd.service reload.

Tip:

* To deploy a single vHost only, supplement the `apache_httpd:vhosts` tag with the extra variable `--extra-vars='apache_httpd__limit_vhosts=["www.example.com"]'`. See [Optional Role Variables - Specific to this role](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd#optional-role-variables---specific-to-this-role).



## Mandatory Role Variables - Global Apache Config (core)

`apache_httpd__conf_server_admin`

* See [ServerAdmin](https://httpd.apache.org/docs/2.4/mod/core.html#serveradmin).
* Type: String.


Example:
```yaml
# mandatory
apache_httpd__conf_server_admin: 'webmaster@example.com'
```

## Optional Role Variables - Global Apache Config (core)

`apache_httpd__conf_add_default_charset`

* See [AddDefaultCharset](https://httpd.apache.org/docs/2.4/mod/core.html#adddefaultcharset).
* Type: String.
* Default: `'UTF-8'`

`apache_httpd__conf_document_root`

* See [DocumentRoot](https://httpd.apache.org/docs/2.4/mod/core.html#documentroot).
* Type: String.
* Default: `'/var/www/html'`

`apache_httpd__conf_enable_send_file`

* See [EnableSendfile](https://httpd.apache.org/docs/2.4/mod/core.html#enablesendfile).
* Type: String.
* Default: `'On'`

`apache_httpd__conf_error_log`

* See [ErrorLog](https://httpd.apache.org/docs/2.4/mod/core.html#errorlog).
* Type: String.
* Default: `'syslog:local1'`

`apache_httpd__conf_hostname_lookups`

* See [HostnameLookups](https://httpd.apache.org/docs/2.4/mod/core.html#hostnamelookups).
* Type: String.
* Default: `'Off'`

`apache_httpd__conf_keep_alive`

* See [KeepAlive](https://httpd.apache.org/docs/2.4/mod/core.html#keepalive).
* Type: String.
* Default: `'On'`

`apache_httpd__conf_keep_alive_timeout`

* See [KeepAliveTimeout](https://httpd.apache.org/docs/2.4/mod/core.html#keepalivetimeout).
* Type: Number.
* CIS: Do not set it above `15` seconds.
* Default: `5`

`apache_httpd__conf_limit_request_body`

* See [LimitRequestBody](https://httpd.apache.org/docs/2.4/mod/core.html#limitrequestbody).
* Type: Number.
* CIS: Do not set it above `102400`.
* Default: `102400`

`apache_httpd__conf_limit_request_field_size`

* See [LimitRequestFieldSize](https://httpd.apache.org/docs/2.4/mod/core.html#limitrequestfieldsize).
* Type: Number.
* CIS: Do not set it above `1024` - but this might be too small for any modern application which sets cookies in its Header.
* Default: `8190`

`apache_httpd__conf_limit_request_fields`

* See [LimitRequestFields](https://httpd.apache.org/docs/2.4/mod/core.html#limitrequestfields).
* Type: Number.
* CIS: Do not set it above `100`.
* Default: `100`

`apache_httpd__conf_limit_request_line`

* See [LimitRequestLine](https://httpd.apache.org/docs/2.4/mod/core.html#limitrequestline).
* Type: Number.
* CIS: Do not set it above `512` - but this might be too small for any modern application which sets cookies in its Header.
* Default: `8190`

`apache_httpd__conf_log_level`

* See [LogLevel](https://httpd.apache.org/docs/2.4/mod/core.html#loglevel).
* Type: String.
* Default: `'warn'`

`apache_httpd__conf_max_keep_alive_requests`

* See [MaxKeepAliveRequests](https://httpd.apache.org/docs/2.4/mod/core.html#maxkeepaliverequests).
* Type: Number.
* Default: `500`

`apache_httpd__conf_server_name`

* See [ServerName](https://httpd.apache.org/docs/2.4/mod/core.html#servername).
* Type: String.
* Default: `'localhost'`

`apache_httpd__conf_timeout`

* See [Timeout](https://httpd.apache.org/docs/2.4/mod/core.html#timeout).
* Type: Number.
* CIS: Do not set it above `10` seconds.
* Default: `10`

`apache_httpd__conf_trace_enable`

* See [TraceEnable](https://httpd.apache.org/docs/2.4/mod/core.html#traceenable).
* Type: String.
* CIS: Do not set it to `'On'`.
* Default: `'Off'`


Example:
```yaml
# optional - core
apache_httpd__conf_add_default_charset: 'UTF-8'
apache_httpd__conf_document_root: '/var/www/html'
apache_httpd__conf_enable_send_file: 'On'
apache_httpd__conf_error_log: 'syslog:local1'
apache_httpd__conf_hostname_lookups: 'Off'
apache_httpd__conf_keep_alive: 'On'
apache_httpd__conf_keep_alive_timeout: 5
apache_httpd__conf_limit_request_body: 102400
apache_httpd__conf_limit_request_field_size: 8190
apache_httpd__conf_limit_request_fields: 100
apache_httpd__conf_limit_request_line: 8190
apache_httpd__conf_log_level: 'warn'
apache_httpd__conf_max_keep_alive_requests: 500
apache_httpd__conf_server_name: 'localhost'
apache_httpd__conf_timeout: 10
apache_httpd__conf_trace_enable: 'Off'
```


## Optional Role Variables - Specific to this role

`apache_httpd__conf__group_var` / `apache_httpd__conf__host_var`

* conf-available/conf-enabled files. See example below.
* Type: List of dictionaries.
* Default: See [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/apache_httpd/defaults/main.yml)

Subkeys:

> `enabled`
>
> * Creates a symlink to conf-available/filename.conf in conf-enabled (true), otherwise the link is removed (false).
> * Type: Boolean.
> * Default: `true`
>
> `filename`
>
> * Required. Destination filename in conf-available/, normally equal to the name of the source template used. Suffixed with `.conf`.
> * Type: String.
>
> `state`
>
> * conf-available/filename.conf is created (`present`), otherwise file is removed (`absent`).
> * Type: String.
>
> `template`
>
> * Required. Name of the Jinja template source file to use.
> * Type: String.

`apache_httpd__htpasswd__group_var` / `apache_httpd__htpasswd__host_var`

* Create and update flat-files for basic authentication of HTTP users.
* Type: List of dictionaries.
* Default: `[]`

Subkeys:

> `password`
>
> * Required. Password.
> * Type: String.
>
> `path`
>
> * Path to the htpasswd file.
> * Type: String.
> * Default: `'/etc/httpd/.htpasswd'`
>
> `state`
>
> * Either `present` or `absent`.
> * Type: String.
> * Default: `'present'`
>
> `username`
>
> * Required. Username.
> * Type: String.

`apache_httpd__limit_vhosts`

* Checks if the `conf_server_name` is in the list and only deploys those. Can be used on the CLI to speed up the deployment on large proxy servers, e.g. `--extra-vars='apache_httpd__limit_vhosts=["test.example.com"]'`.
* Type: List.
* Default: unset

`apache_httpd__mods__group_var` / `apache_httpd__mods__host_var`

* mods-available/mods-enabled files. See example below.
* Type: List of dictionaries.
* Default: See [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/apache_httpd/defaults/main.yml)

Subkeys:

> `enabled`
>
> * Creates a symlink to mods-available/filename.mods in mods-enabled (true), otherwise the link is removed (false).
> * Type: Boolean.
> * Default: `true`
>
> `filename`
>
> * Required. Destination filename in mods-available/, normally equal to the name of the source template used. Suffixed with `.conf`.
> * Type: String.
>
> `state`
>
> * mods-available/filename.conf is created (`present`), otherwise file is removed (`absent`).
> * Type: String.
>
> `template`
>
> * Name of the Ansible Jinja template source file to use. If omitted, `filename` is used.
> * Type: String.

`apache_httpd__packages__group_var` / `apache_httpd__packages__host_var`

* Packages to install using the OS package manager. Packages are removed first and then added.
* Type: List of dictionaries.
* Default: See [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/apache_httpd/defaults/main.yml)

Subkeys:

> `name`
>
> * Required. The package name.
> * Type: String.
>
> `state`
>
> * State of the package, one of `present`, `absent`.
> * Type: String.

`apache_httpd__skip_document_root_chown`

* Set to true to skip the `chown -R apache:apache` of the document root.
* Type: Boolean.
* Default: `false`

`apache_httpd__skip_php_fpm`

* Skip PHP-FPM configuration globally and in each vHost within Apache. When set to `false` (default), the role automatically injects PHP-FPM `ProxyPass` directives into app, localhost, and wordpress vHosts.
* Type: Boolean.
* Default: `false`

`apache_httpd__systemd_enabled`

* Whether the Apache webserver service should start on boot (true) or not (false).
* Type: Boolean.
* Default: `true`

`apache_httpd__systemd_state`

* Make sure Apache webserver service is in a specific state. Possible options: `reloaded`, `restarted`, `started`, `stopped`.
* Type: String.
* Default: `'started'`

Example:
```yaml
# optional - role-specific
apache_httpd__conf__host_var:
  - filename: 'deflate'
    enabled: true
    state: 'present'
    template: 'deflate'
apache_httpd__htpasswd__host_var:
  - username: 'test-user'
    password: 'linuxfabrik'
    state: 'present'
apache_httpd__limit_vhosts:
    - 'test.example.com'
apache_httpd__mods__host_var:
  - filename: 'alias'
    enabled: true
    state: 'present'
    template: 'alias'
  - filename: 'authn_core'
    enabled: false # overwrite the default
    state: 'absent' # overwrite the default
    template: 'authn_core'
apache_httpd__packages__host_var:
  - name: 'mod_qos'
    state: 'present'
apache_httpd__skip_document_root_chown: true
apache_httpd__skip_php_fpm: false
apache_httpd__systemd_enabled: true
apache_httpd__systemd_state: 'started'
```


## Mandatory Role Variables - vHosts

`apache_httpd__vhosts__group_var` / `apache_httpd__vhosts__host_var`:

`conf_server_name`

* Set this variable for each vHost definition. Although this is just best practice, we would never use a vHost without a ServerName.
* Type: String.


Example:
```yaml
# mandatory
apache_httpd__vhosts__host_var:
  # Application vHosts
  - template: 'app'
    conf_server_name: 'myapp.example.com'
```


## Optional Role Variables - vHosts

Using `apache_httpd__vhosts__group_var` or `apache_httpd__vhosts__host_var` (which are dictionaries), you define vHosts for Apache. The example below shows a complete example, use this as a starting point.

Types of vHosts:

* **app**: A hardened vHost running an application like Nextcloud, Wordpress etc. with the most common options. Can be extended by using the `raw` variable.
* **localhost**: A hardened, pre-defined VirtualHost just listening on https://localhost, and only accessible from localhost. Due to its naming, it is the first defined vHost. Can be extended by using the `raw` variable. The following URLs are pre-configured and only accessible from localhost:
    * `/fpm-ping` - PHP-FPM health check
    * `/fpm-status` - PHP-FPM status page
    * `/monitoring.php` - Linuxfabrik monitoring endpoint
    * `/server-info` - Apache server info (`mod_info` required)
    * `/server-status` - Apache server status (`mod_status` required)
* **proxy**: A typical hardened reverse proxy vHost. Can be extended by using the `raw` variable. This proxy vHost definition prevents Apache from functioning as a forward proxy server (inside > out).
* **raw**: If none of the above vHost templates fit, use the `raw` one and define everything except `<VirtualHost>` and `</VirtualHost>` completely from scratch.
* **redirect**: A vHost that redirects from one port (default "80") to another (default "443"). Custom redirect rules can be provided using the `raw` variable.
* **wordpress**: A special vHost just for deploying WordPress instances.

"Hardened" means among other things:

* Old HTTP protocol (< HTTP/1.1) versions are disallowed.
* IP address based requests are disallowed.
* Number of bytes that are allowed in a request are limited.
* Access to dotfiles (files starting with `.`) is blocked, except `.well-known` (for ACME/Let's Encrypt challenges).
* Forbidden HTTP methods return a `405 Method Not Allowed` via `RewriteRule`.

This role creates a vHost named `localhost` by default. See [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/apache_httpd/defaults/main.yml)

`allow_accessing_dotfiles`

* app-vHosts block access to files that begin with a period. With this setting you can disable this behavior.
* Type: Boolean.
* Default: `false`

`allow_requests_without_hostname`

* app-vHosts forbid accessing them without a hostname / just by IP. With this setting you can disable this behavior.
* Type: Boolean.
* Default: `false`

`allowed_file_extensions`

* app- and localhost-vHosts block ALL file extensions by default, unless specifically allowed. The patterns use Apache regex syntax (e.g. `html?` matches both `html` and `htm`, `jpe?g` matches both `jpeg` and `jpg`). Files and folders starting with a dot are always forbidden. Use `skip_allowed_file_extensions` to allow all file extensions.
* To compile a list of file extensions present in your application, run:
  `find {{ apache_httpd__conf_document_root }} -type f -name '*.*' | awk -F. '{print $NF }' | sort --unique | sed -e 's/^/- \x27/' -e 's/$/\x27/'`
* Type: List.
* Default: app/localhost `['css', 'gif', 'html?', 'ico', 'jpe?g', 'js', 'pdf', 'php', 'png', 'svg', 'ttf', 'txt', 'woff2?']`

`allowed_http_methods`

* Restrict allowed [HTTP methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods). Only the explicitly listed ones are allowed; all others return [405 Method Not Allowed](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes). This does not disable TRACE. Always enable GET and OPTIONS at least. For an OPTIONS request, Apache always returns `Allow: GET,POST,OPTIONS,HEAD`, no matter what. We are NOT using [LimitExcept](https://httpd.apache.org/docs/2.4/mod/core.html#limitexcept), because this directive is not allowed in a VirtualHost context. Use `skip_allowed_http_methods` to allow all HTTP methods.
* Available HTTP methods:
    * CONNECT, DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT
* Available WebDAV methods:
    * COPY, LOCK, MKCOL, MOVE, PROPFIND, PROPPATCH, UNLOCK
* Type: List.
* Default: app/localhost/proxy `['GET', 'OPTIONS']`

`authz_document_root`

* Authorization statement for the `DocumentRoot {{ apache_httpd__conf_document_root }}/{{ conf_server_name }}` directive.
* Type: String.
* Default: app/localhost `'Require all granted'`

`by_role`

* If defined it results in a comment `# Generated by Ansible role: {{ by_role }}` at the beginning of a vHost definition.
* Type: String.
* Default: unset

`comment`

* Describes the vHost and results in a comment right above the `<VirtualHost>` section.
* Type: String.
* Default: `'no description available'`

`conf_allow_override`

* Will be set in the `<Directory>` directive of the vHost. See [AllowOverride](https://httpd.apache.org/docs/2.4/mod/core.html#allowoverride).
* Type: String.
* Default: app/localhost `'None'`

`conf_custom_log`

* The log format has to be one of: `agent`, `combined`, `combinedio`, `common`, `debug`, `fail2ban`, `linuxfabrikio`, `matomo`, `referer`, `vhost_common`. See [CustomLog](https://httpd.apache.org/docs/2.4/mod/mod_log_config.html#customlog).
* Type: String.
* Default: app/localhost/proxy `'logs/{{ conf_server_name }}-access.log linuxfabrikio'`

`conf_directory_index`

* See [DirectoryIndex](https://httpd.apache.org/docs/2.4/mod/mod_dir.html#directoryindex).
* Type: String.
* Default: app `{{ apache_httpd__mod_dir_directory_index }}`

`conf_document_root`

* See [DocumentRoot](https://httpd.apache.org/docs/2.4/mod/core.html#documentroot).
* Type: String.
* Default: app/localhost `'{{ apache_httpd__conf_document_root }}/{{ conf_server_name }}'`

`conf_error_log`

* See [ErrorLog](https://httpd.apache.org/docs/2.4/mod/core.html#errorlog).
* Type: String.
* Default: app/localhost/proxy `'logs/{{ conf_server_name }}-error.log'`

`conf_keep_alive_timeout`

* See [KeepAliveTimeout](https://httpd.apache.org/docs/2.4/mod/core.html#keepalivetimeout).
* Type: Number.
* CIS: Do not set it above `15` seconds.
* Default: `5`

`conf_log_level`

* See [LogLevel](https://httpd.apache.org/docs/2.4/mod/core.html#loglevel).
* Type: String.
* Default: `'notice core:info'`

`conf_options`

* Sets the `Options` for the `<Directory>` directive. See [Options](https://httpd.apache.org/docs/2.4/mod/core.html#options).
* Type: String.
* Default: app/localhost `'None'`

`conf_proxy_error_override`

* If you want to have a common look and feel on the error pages seen by the end user, set this to "On" and define them on the reverse proxy server. See [ProxyErrorOverride](https://httpd.apache.org/docs/2.4/mod/mod_proxy.html#proxyerroroverride).
* Type: String.
* Default: proxy `'On'`

`conf_proxy_preserve_host`

* When enabled, this option will pass the `Host:` line from the incoming request to the proxied host, instead of the hostname specified in the `ProxyPass` line. See [ProxyPreserveHost](https://httpd.apache.org/docs/2.4/mod/mod_proxy.html#proxypreservehost).
* Type: String.
* Default: `'Off'`

`conf_proxy_timeout`

* See [ProxyTimeout](https://httpd.apache.org/docs/2.4/mod/mod_proxy.html#proxytimeout).
* Type: Number.
* Default: `5`

`conf_request_read_timeout`

* See [RequestReadTimeout](https://httpd.apache.org/docs/2.4/mod/mod_reqtimeout.html#requestreadtimeout).
* Type: Number.
* CIS: Do not set the Timeout Limits for Request Headers above 40. Do not set the Timeout Limits for the Request Body above 20.
* Default: `'header=20-40,MinRate=500 body=20,MinRate=500'`

`conf_server_admin`

* See [ServerAdmin](https://httpd.apache.org/docs/2.4/mod/core.html#serveradmin).
* Type: String.
* Default: `{{ apache_httpd__conf_server_admin }}`

`conf_server_alias`

* Set this only if you need more than one `conf_server_name`. See [ServerAlias](https://httpd.apache.org/docs/2.4/mod/core.html#serveralias).
* Type: List.
* Default: unset

`conf_server_name`

* See [ServerName](https://httpd.apache.org/docs/2.4/mod/core.html#servername).
* Type: String.
* Default: unset

`conf_timeout`

* See [Timeout](https://httpd.apache.org/docs/2.4/mod/core.html#timeout).
* Type: Number.
* Default: `{{ apache_httpd__conf_timeout }}`

`enabled`

* Enable this vHost.
* Type: Boolean.
* Default: `true`

`filename`

* The filename of the vHost definition. If not set it defaults to the `conf_server_name` variable. The filename is automatically suffixed by `.virtualhost_port.conf`.
* Type: String.
* Default: `conf_server_name.virtualhost_port.conf`

`php_set_handler`

* Set the handler for PHP. Socket-based: `SetHandler "proxy:unix:/run/php-fpm/www.sock|fcgi://localhost"`. Network-based: `SetHandler "proxy:fcgi://127.0.0.1:9000/"`.
* Type: String.
* Default: app/localhost `'SetHandler "proxy:unix:/run/php-fpm/www.sock|fcgi://localhost"'`

`raw`

* It is sometimes desirable to pass variable content that Jinja would handle as variables or blocks. The best and safest solution is to declare `raw` variables as `!unsafe`, to prevent templating errors and information disclosure.
* Type: String.
* Default: unset

`skip_allowed_file_extensions`

* Skips checking file extensions in app- and localhost-vHosts, allowing essentially all file extensions.
* Type: Boolean.
* Default: `false`

`skip_allowed_http_methods`

* Skips checking the HTTP methods in app-, localhost-, proxy-, wordpress-vHosts, allowing essentially all HTTP methods.
* Type: Boolean.
* Default: `false`

`state`

* Should the vhost definition file be created (`present`) or deleted (`absent`).
* Type: String.
* Default: localhost `'present'`, others unset

`template`

* See the "Types of vHosts" section above.
* Type: String.
* Default: unset

`virtualhost_ip`

* Used within the `<VirtualHost {{ virtualhost_ip }}:{{ virtualhost_port }}>` directive.
* Type: String.
* Default: `'*'`

`virtualhost_port`

* Used within the `<VirtualHost {{ virtualhost_ip }}:{{ virtualhost_port }}>` directive.
* Type: Number.
* Default: `443`, redirect `80`

Example: See [EXAMPLES.md](https://github.com/Linuxfabrik/lfops/blob/main/roles/apache_httpd/EXAMPLES.md).



## Optional Role Variables - mod_dir

`apache_httpd__mod_dir_directory_index`

* See [DirectoryIndex](https://httpd.apache.org/docs/2.4/mod/mod_dir.html#directoryindex).
* Type: String.
* Default: `'index.html index.htm index.txt'`


Example:
```yaml
# optional - mod_dir
apache_httpd__mod_dir_directory_index: 'index.html'
```


## Optional Role Variables - mod_log_config

This module is for flexible logging of client requests. Logs are written in a customizable format, and may be written directly to a file, or to an external program. Conditional logging is provided so that individual requests may be included or excluded from the logs based on characteristics of the request.

`apache_httpd__mod_log_config_custom_log`

* Global log directive that applies to requests not handled by any vHost. Each vHost defines its own log via `conf_custom_log`. One of: `agent`, `combined`, `combinedio`, `common`, `debug`, `fail2ban`, `linuxfabrikio`, `matomo`, `referer`, `vhost_common`. See [CustomLog](https://httpd.apache.org/docs/2.4/mod/mod_log_config.html#customlog).
* Type: String.
* Default: unset

Example:
```yaml
# optional - mod_log_config
apache_httpd__mod_log_config_custom_log: 'logs/access.log combined'
```


## Optional Role Variables - mod_security (security2)

`apache_httpd__mod_security_coreruleset_url`

* The OWASP ModSecurity Core Rule Set (CRS) Download URL. Change this if you are running your own mirror servers.
* Type: String.
* Default: `'https://github.com/coreruleset/coreruleset/archive'`

`apache_httpd__mod_security_coreruleset_version`

* The OWASP ModSecurity Core Rule Set (CRS) version number without "v".
* Type: String.
* Default: `'4.24.1'`

`apache_httpd__skip_mod_security_coreruleset`

* Skip the installation of the OWASP ModSecurity Core Rule Set (CRS).
* Type: Boolean.
* Default: `true`

Example:
```yaml
# optional - mod_security
apache_httpd__mod_security_coreruleset_url: 'https://github.com/coreruleset/coreruleset/archive'
apache_httpd__mod_security_coreruleset_version: '4.24.1'
apache_httpd__skip_mod_security_coreruleset: true
```


## Optional Role Variables - mod_ssl

`apache_httpd__mod_ssl_ssl_use_stapling`

* See [SSLUseStapling](https://httpd.apache.org/docs/2.4/mod/mod_ssl.html#sslusestapling).
* Type: String.
* Default: `'on'`

Example:
```yaml
# optional - mod_ssl
apache_httpd__mod_ssl_ssl_use_stapling: 'on'
```


## Optional Role Variables - mpm_common

`apache_httpd__mpm_common_listen`

* See [Listen](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#listen).
* Type: List of numbers or strings.
* Default: `[80]`


Example:
```yaml
# optional - mpm_common
apache_httpd__mpm_common_listen:
  - 80
  - '192.0.2.10:80'
```


## Optional Role Variables - mpm_event_module

TLDR: event MPM: A variant of the worker MPM with the goal of consuming threads only for connections with active processing. See: http://httpd.apache.org/docs/2.4/mod/event.html

Event: Based on worker, this MPM goes one step further by optimizing how the parent process
schedules tasks to the child processes and the threads associated to those. A connection stays
open for 5 seconds by default and closes if no new event happens; this is the keep-alive
directive default value, which retains the thread associated to it. The Event MPM enables the
process to manage threads so that some threads are free to handle new incoming connections while
others are kept bound to the live connections. Allowing re-distribution of assigned tasks to
threads will make for better resource utilization and performance.

Best for PHP-FPM. Default.

`apache_httpd__mpm_event_max_connections_per_child`

* See [MaxConnectionsPerChild](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxconnectionsperchild).
* Type: Number.
* Default: `0`

`apache_httpd__mpm_event_max_request_workers`

* See [MaxRequestWorkers](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxrequestworkers).
* Type: Number.
* Default: `400`

`apache_httpd__mpm_event_max_spare_threads`

* See [MaxSpareThreads](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxsparethreads).
* Type: Number.
* Default: `250`

`apache_httpd__mpm_event_min_spare_threads`

* See [MinSpareThreads](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#minsparethreads).
* Type: Number.
* Default: `75`

`apache_httpd__mpm_event_start_servers`

* See [StartServers](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#startservers).
* Type: Number.
* Default: `3`

`apache_httpd__mpm_event_thread_limit`

* See [ThreadLimit](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#threadlimit).
* Type: Number.
* Default: `64`

`apache_httpd__mpm_event_threads_per_child`

* See [ThreadsPerChild](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#threadsperchild).
* Type: Number.
* Default: `25`


Example:
```yaml
# optional - mpm_event_module
apache_httpd__mpm_event_max_connections_per_child: 0
apache_httpd__mpm_event_max_request_workers: 400
apache_httpd__mpm_event_max_spare_threads: 250
apache_httpd__mpm_event_min_spare_threads: 75
apache_httpd__mpm_event_start_servers: 3
apache_httpd__mpm_event_thread_limit: 64
apache_httpd__mpm_event_threads_per_child: 25
```


## Optional Role Variables - mpm_prefork_module

TLDR: prefork MPM: Implements a non-threaded, pre-forking web server. See: http://httpd.apache.org/docs/2.4/mod/prefork.html

Pre-fork: A new process is created for each incoming connection reaching the server. Each process
is isolated from the others, so no memory is shared between them, even if they are performing
identical calls at some point in their execution. This is a safe way to run applications linked
to libraries that do not support threading—typically older applications or libraries.

NOTE: If enabling prefork, the httpd_graceful_shutdown SELinux boolean should be enabled, to allow graceful stop/shutdown.

This MPM is very self-regulating, so it is rarely necessary to adjust its configuration directives. Most important is that `apache_httpd__mpm_prefork_max_request_workers` be big enough to handle as many simultaneous requests as you expect to receive, but small enough to assure that there is enough physical RAM for all processes.

Best for Standard PHP running any version of `mod_php`. Does not work with http2.

`apache_httpd__mpm_prefork_max_connections_per_child`

* See [MaxConnectionsPerChild](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxconnectionsperchild).
* Type: Number.
* Default: `0`

`apache_httpd__mpm_prefork_max_request_workers`

* See [MaxRequestWorkers](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxrequestworkers).
* Type: Number.
* Default: `256`

`apache_httpd__mpm_prefork_max_spare_servers`

* See [MaxSpareServers](https://httpd.apache.org/docs/2.4/mod/prefork.html#maxspareservers).
* Type: Number.
* Default: `10`

`apache_httpd__mpm_prefork_min_spare_servers`

* See [MinSpareServers](https://httpd.apache.org/docs/2.4/mod/prefork.html#minspareservers).
* Type: Number.
* Default: `5`

`apache_httpd__mpm_prefork_start_servers`

* See [StartServers](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#startservers).
* Type: Number.
* Default: `5`

Example:
```yaml
# optional - mpm_prefork_module
apache_httpd__mpm_prefork_max_connections_per_child: 0
apache_httpd__mpm_prefork_max_request_workers: 256
apache_httpd__mpm_prefork_max_spare_servers: 10
apache_httpd__mpm_prefork_min_spare_servers: 5
apache_httpd__mpm_prefork_start_servers: 5
```


## Optional Role Variables - mpm_worker_module

TLDR: worker MPM: Multi-Processing Module implementing a hybrid multi-threaded multi-process web server. See: http://httpd.apache.org/docs/2.4/mod/worker.html

Worker: A parent process is responsible for launching a pool of child processes, some of which
are listening for new incoming connections, and others are serving the requested content. Each
process is threaded (a single thread can handle one connection) so one process can handle several
requests concurrently. This method of treating connections encourages better resource
utilization, while still maintaining stability. This is a result of the pool of available
processes, which often has free available threads ready to immediately serve new connections.

The most important directives used to control this MPM are `apache_httpd__mpm_worker_threads_per_child`, which controls the number of threads deployed by each child process and `apache_httpd__mpm_worker_max_request_workers`, which controls the maximum total number of threads that may be launched.

Best for mod_qos if you intend to use any connection level control directive ("QS_Srv\*"), which is normally done on a Reverse Proxy. Works with PHP-FPM, too.

`apache_httpd__mpm_worker_max_connections_per_child`

* See [MaxConnectionsPerChild](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxconnectionsperchild).
* Type: Number.
* Default: `0`

`apache_httpd__mpm_worker_max_request_workers`

* See [MaxRequestWorkers](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxrequestworkers).
* Type: Number.
* Default: `400`

`apache_httpd__mpm_worker_max_spare_threads`

* See [MaxSpareThreads](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxsparethreads).
* Type: Number.
* Default: `250`

`apache_httpd__mpm_worker_min_spare_threads`

* See [MinSpareThreads](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#minsparethreads).
* Type: Number.
* Default: `75`

`apache_httpd__mpm_worker_start_servers`

* See [StartServers](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#startservers).
* Type: Number.
* Default: `3`

`apache_httpd__mpm_worker_thread_limit`

* See [ThreadLimit](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#threadlimit).
* Type: Number.
* Default: `64`

`apache_httpd__mpm_worker_threads_per_child`

* See [ThreadsPerChild](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#threadsperchild).
* Type: Number.
* Default: `25`


Example:
```yaml
# optional - mpm_worker_module
apache_httpd__mpm_worker_max_connections_per_child: 0
apache_httpd__mpm_worker_max_request_workers: 400
apache_httpd__mpm_worker_max_spare_threads: 250
apache_httpd__mpm_worker_min_spare_threads: 75
apache_httpd__mpm_worker_start_servers: 3
apache_httpd__mpm_worker_thread_limit: 64
apache_httpd__mpm_worker_threads_per_child: 25
```


## Optional Role Variables - wsgi_python3_module

`apache_httpd__wsgi_python_home`

* See [WSGIPythonHome](https://modwsgi.readthedocs.io/en/develop/configuration-directives/WSGIPythonHome.html).
* Type: String.
* Default: `'/opt/python'`

`apache_httpd__wsgi_python_path`

* See [WSGIPythonPath](https://modwsgi.readthedocs.io/en/develop/configuration-directives/WSGIPythonPath.html).
* Type: String.
* Default: `'/var/www/html/python/'`

`apache_httpd__wsgi_script_alias`

* See [WSGIScriptAlias](https://modwsgi.readthedocs.io/en/develop/configuration-directives/WSGIScriptAlias.html).
* Type: String.
* Default: `'/ /var/www/html/python/index.py'`

Example:
```yaml
# optional - wsgi_python3_module
apache_httpd__wsgi_python_home: '/opt/python'
apache_httpd__wsgi_python_path: '/var/www/html/python/'
apache_httpd__wsgi_script_alias: '/ /var/www/html/python/index.py'
```



## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
