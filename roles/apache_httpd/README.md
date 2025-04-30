# Ansible Role linuxfabrik.lfops.apache_httpd

This role installs and configures a CIS-compliant [Apache httpd](https://httpd.apache.org/).


## What this Role does

This role configures Apache in the same way as is usual on Debian systems, so quite different to upstream's suggested way to configure the web server. This is because this role attempts to make adding and removing mods, virtual hosts, and extra configuration directives as flexible as possible, in order to make automating the changes and administering the server as easy as possible.

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

We try to avoid using `<IfModule>` in the global Apache configuration as well as in the configuration of the vhosts as much as possible in order to facilitate debugging. Otherwise, when using `<IfModule>`, configuration options are silently dropped, and their absence is very difficult to notice.

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


## Config Examples for vHosts

[Have a look here](https://github.com/Linuxfabrik/lfops/blob/main/roles/apache_httpd/EXAMPLES.md).



## Mandatory Requirements

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Install the `python3-passlib` library. This can be done using the [linuxfabrik.lfops.python](https://github.com/Linuxfabrik/lfops/tree/main/roles/python) role.


## Optional Requirements

* Install PHP and configure PHP-FPM. This can be done using the [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role.



## Tags

| Tag      | What it does                   |
| ---      | ------------                   |
| `apache_httpd` | * Installs and configures apache_httpd |
| `apache_httpd:config` | * Creates or updates global Apache configuration<br> * Removes conf-available configs<br> * Creates conf-available configs<br> * Disables configs<br> * Enables configs |
| `apache_httpd:htpasswd` | Manages htpasswd files. |
| `apache_httpd:matomo` | * Deploys Matomo Log Analytics Python Script |
| `apache_httpd:mod_security_coreruleset` | * Downloads, verifies and installs OWASP ModSecurity Core Rule Set (CRS)<br> * Installs tar<br> * Unarchives the CRS<br> * Links the CRS |
| `apache_httpd:mods` | * Removes mods-available configs<br> * Create mods-available configs<br> * Disable mods<br> * Enable mods |
| `apache_httpd:state` | * Ensures that httpd service is in a desired state |
| `apache_httpd:vhosts` | * Removes sites-available vHosts<br> * Creates sites-available vHosts<br> * Creates DocumentRoot for all vHosts<br> * Disables vHosts<br> * Enables vHosts |


## Mandatory Role Variables - Global Apache Config (core)

| Variable | Description |
| -------- | ----------- |
| `apache_httpd__conf_server_admin` | Mandatory, string. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#serveradmin) |


Example:
```yaml
# mandatory
apache_httpd__conf_server_admin: 'webmaster@example.com'
```

## Optional Role Variables - Global Apache Config (core)

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apache_httpd__conf_add_default_charset` | String. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#adddefaultcharset) | `'UTF-8'` |
| `apache_httpd__conf_document_root` | String. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#documentroot) | `'/var/www/html'` |
| `apache_httpd__conf_enable_send_file` | String. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#enablesendfile) | `'On'` |
| `apache_httpd__conf_error_log` | String. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#errorlog) | `'syslog:local1'` |
| `apache_httpd__conf_hostname_lookups` | String. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#hostnamelookups) | `'Off'` |
| `apache_httpd__conf_keep_alive` | String. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#keepalive) | `'On'` |
| `apache_httpd__conf_keep_alive_timeout` | Number. CIS: Do not set it above `15` seconds.<br>[Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#keepalivetimeout) | `5` |
| `apache_httpd__conf_limit_request_body` | Number. CIS: Do not set it above `102400`.<br>[Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#limitrequestbody) | `102400` |
| `apache_httpd__conf_limit_request_field_size` | Number. CIS: Do not set it above `1024` - but this might be too small for any modern application which sets cookies in its Header.<br>[Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#limitrequestfieldsize) | `8190` |
| `apache_httpd__conf_limit_request_fields` | Number. CIS: Do not set it above `100`.<br>[Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#limitrequestfields) | `100` |
| `apache_httpd__conf_limit_request_line` | Number. CIS: Do not set it above `512` - but this might be too small for any modern application which sets cookies in its Header.<br>[Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#limitrequestline) | `8190` |
| `apache_httpd__conf_log_level` | String. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#loglevel) | `'warn'` |
| `apache_httpd__conf_max_keep_alive_requests` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#maxkeepaliverequests) | `500` |
| `apache_httpd__conf_server_name` | String. Mandatory, string. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#servername) | `'localhost'` |
| `apache_httpd__conf_timeout` | Number. CIS: Do not set it above `10` seconds.<br>[Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#timeout) | `10` |
| `apache_httpd__conf_trace_enable` | String. CIS: Do not set it to `'On'`.<br>[Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#traceenable) | `'Off'` |


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

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apache_httpd__conf__group_var` /<br> `apache_httpd__conf__host_var` | List. List of dictionaries of `conf-available`/`conf-enabled` files. <br> Subkeys:<br> * `filename`: Mandatory, string. Destination filename in `conf-available/`, and normally is equal to the name of the source `template` used. Will be suffixed with `.conf`.<br> * `enabled`: boolean. Defaults to `true`. Creates a symlink to `conf-available/<keyname>.conf` in `conf-enabled/` (`true`), otherwise the link is removed (`false`).<br> * `state`: string. `conf-available/<keyname>.conf` is created (`present`), otherwise file is removed (`absent`).<br> * `template`: Mandatory, string. Name of the Jinja template source file to use.<br>See example below. | [Have a look](https://github.com/Linuxfabrik/lfops/blob/main/roles/apache_httpd/defaults/main.yml) |
| `apache_httpd__htpasswd__group_var` /<br> `apache_httpd__htpasswd__host_var` | List of dictionaries containing used to create and update the flat-files used to store usernames and password for basic authentication of HTTP users. Subkeys: <ul><li>`username`: Mandatory, string. Username.</li><li>`password`: Mandatory, string. Password.</li><li>`path`: Optional, string. Path to the htpasswd file. Defaults to `/etc/httpd/.htpasswd`.</li><li>`state`: Optional, string. Either `present` or `absent`. Defaults to `present`.</li></ul> | `[]` |
| `apache_httpd__limit_vhosts` | List. Checks if the `conf_server_name` is in the list and only deploys those. Can be used on the CLI to speed up the deployment on large proxy servers, e.g. `--extra-vars='apache_httpd__limit_vhosts=["test.example.com"]'`.| unset |
| `apache_httpd__mods__group_var` / `apache_httpd__mods__host_var` | List. List of dictionaries of `mods-available`/`mods-enabled` files. <br>Subkeys:<br> * `filename`: Mandatory, string. Destination filename in `mods-available/`, and normally is equal to the name of the source `template` used. Will be suffixed with `.conf`.<br> * `enabled`: boolean. Defaults to `true`. Creates a symlink to `mods-available/<keyname>.mods` in `mods-enabled/` (`true`), otherwise the link is removed (`false`).<br> * `state`: string. `mods-available/<keyname>.conf` is created (`present`), otherwise file is removed (`absent`).<br> * `template`: string. Name of the Ansible Jinja template source file to use. If ommited, `filename` is used.<br>See example below. | [Have a look](https://github.com/Linuxfabrik/lfops/blob/main/roles/apache_httpd/defaults/main.yml) |
| `apache_httpd__packages__group_var` / `apache_httpd__packages__host_var` | List. List of dictionaries of packages to install, related to Apache, using the OS package manager. Possible options:<br> * `name`: Mandatory, string. The package name.<br> * `state`: Mandatory, string. State of the package, one of `present`, `absent`. Packages are removed first and then added. | [Have a look](https://github.com/Linuxfabrik/lfops/blob/main/roles/apache_httpd/defaults/main.yml) |
| `apache_httpd__skip_document_root_chown` | Boolean. Set to true to skip the `chown -R apache:apache` of the document root. | `false` |
| `apache_httpd__skip_php_fpm` | Boolean. Skip PHP configuration globally and in each vHost within Apache. | `false` |
| `apache_httpd__systemd_enabled` | Boolean. Whether the Apache webserver service should start on boot (`true`) or not (`false`). | `true` |
| `apache_httpd__systemd_state` | String. Make sure Apache webserver service is in a specific state. Possible options:<br> * `reloaded`<br> * `restarted`<br> * `started`<br> * `stopped` | `'started'` |

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

| Variable | Description |
| -------- | ----------- |
| `conf_server_name` | Mandatory, string. Set this variable for each vHost definition. Although this is just best practise, we would never use a vHost without a ServerName. |


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

* **app**<br>
  A hardened vHost running an application like Nextcloud, Wordpress etc. with the most common options. Can be extended by using the `raw` variable.<br>
* **localhost**<br>
  A hardened, pre-defined VirtualHost just listening on https://localhost, and only accessible from localhost. Due to its naming, it is the first defined vHost. Useful for <br>Apache status info etc. Can be extended by using the `raw` variable. The following URLs are pre-configured, accessible just from localhost: `/fpm-ping`, `/fpm-status`, `/monitoring.php`, `/server-info`, `/server-status`.
* **proxy**<br>
  A typical hardened reverse proxy vHost. Can be extended by using the `raw` variable. This proxy vHost definition prevents Apache from functioning as a forward proxy <br>server (inside > out).
* **redirect**<br>
  A vHost that redirects from one port (default "80") to another (default "443"). Custom redirect rules can be provided using the `raw` variable.<br>
* **raw**<br>
  If none of the above vHost templates fit, use the `raw` one and define everything except `<VirtualHost>` and `</VirtualHost>` completely from scratch.<br>
* **wordpress**<br>
  A special vHost just for deploying WordPress instances.

"Hardened" means among other things:

* Old HTTP protocol (< HTTP/1.1) versions are disallowed.
* IP address based requests are disallowed.
* Number of bytes that are allowed in a request are limited.
* etc.

This role creates a vHost named `localhost` by default. Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/apache_httpd/defaults/main.yml) |

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `allow_accessing_dotfiles` | Boolean. app-vHosts block access to files that begin with a period. With this setting you can disable this behavior. | `false` |
| `allow_requests_without_hostname` | Boolean. app-vHosts forbid accessing them without a hostname / just by IP. With this setting you can disable this behavior. | `false` |
| `allowed_file_extensions` | List. app- and localhost-vHosts block ALL file extensions by default (including `.gitignore`, `.svn`, `.htaccess`, `.hg`, `.bzr` etc.), unless specifically allowed. Use `find {{ apache_httpd__conf_document_root }} -type f -name '*.*' \| awk -F. '{print $NF }' \| sort --unique \| sed -e 's/^/- \x27/' -e 's/$/\x27/'` to compile a list of the file extensions that are currently present in your application. Note: The vHost templates already ensure that files and folders starting with a dot (".") are forbidden. Use `skip_allowed_file_extensions` to allow all file extensions. | * app: `['css', 'gif', 'html?', 'ico', 'jpe?g', 'js', 'pdf', 'php', 'png', 'svg', 'ttf', 'txt', 'woff2?']`<br> * localhost: `['css', 'gif', 'html?', 'ico', 'jpe?g', 'js', 'pdf', 'php', 'png', 'svg', 'ttf', 'txt', 'woff2?']`<br> |
| `allowed_http_methods` | List. Should be used to disable unwanted [HTTP methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods). Only the explicity listed ones are allowed. Use `skip_allowed_http_methods` to allow all HTTP methods. Returns a [405 - Method Not Allowed](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) if a forbidden HTTP method is used.<br> * This does not disable TRACE.<br> * Always enable GET and OPTIONS at least. For an OPTIONS request, Apache always returns `Allow: GET,POST,OPTIONS,HEAD`, no matter what.<br> * We are NOT using [LimitExcept](https://httpd.apache.org/docs/2.4/mod/core.html#limitexcept), because this directive is not allowed in a VirtualHost context.<br><br>Available HTTP methods:<br> * CONNECT<br> * DELETE<br> * GET<br> * HEAD<br> * OPTIONS<br> * PATCH<br> * POST<br> * PUT<br><br>Available WebDAV methods:<br> * COPY<br> * LOCK<br> * MKCOL<br> * MOVE<br> * PROPFIND<br> * PROPPATCH<br> * UNLOCK | * app: `['GET', 'OPTIONS']`<br> * localhost: `['GET', 'OPTIONS']`<br> * proxy: `['GET', 'OPTIONS']` |
| `authz_document_root` | String. Authorization statement for the `DocumentRoot {{ apache_httpd__conf_document_root }}/{{ conf_server_name }}` directive. | * app: `'Require all granted'`<br> * localhost: `'Require all granted'` |
| `by_role` | String. If defined it results in a comment `# Generated by Ansible role: {{ by_role }}` at the beginning of a vHost definition. | * app: unset<br> * localhost: unset<br> * proxy: unset<br> * raw: unset<br> * redirect: unset |
| `comment` | String. Describes the vHost and results in a comment right above the `<VirtualHost>` section. | * app: `'no description available'`<br> * localhost: `'no description available'`<br> * proxy: `'no description available'`<br> * raw: `'no description available'` |
| `conf_allow_override` | String. Will be set in the `<Directory>` directive of the vHost.<br>[Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#allowoverride) | * app: `'None'`<br> * localhost: `'None'` |
| `conf_custom_log` | String. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mod_log_config.html#customlog). The log format has to be of<br> * `agent`<br> * `combined`<br> * `combinedio`<br> * `common`<br> * `debug`<br> * `fail2ban`<br> * `linuxfabrikio`<br> * `matomo`<br> * `referer`<br> * `vhost_common` | * app: `'logs/{{ conf_server_name }}-access.log linuxfabrikio`<br> * localhost: `'logs/{{ conf_server_name }}-access.log linuxfabrikio<`br> * proxy: `'logs/{{ conf_server_name }}-access.log linuxfabrikio` |
| `conf_directory_index` | String. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mod_dir.html#directoryindex) | * app: `{{ apache_httpd__mod_dir_directory_index }}` |
| `conf_document_root` | String. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#documentroot) | * app: `{{ apache_httpd__conf_document_root}}/{{ conf_server_name }}`<br> * localhost: `{{ apache_httpd__conf_document_root}}/{{ conf_server_name }}` |
| `conf_error_log` | String. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#errorlog) | * app: `logs/{{ conf_server_name }}-error.log`<br> * localhost: `logs/{{ conf_server_name }}-error.log`<br> * proxy: `logs/{{ conf_server_name }}-error.log` |
| `conf_keep_alive_timeout` | Number. CIS: Do not set it above '15' seconds.<br>[Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#keepalivetimeout) | * app: `5`<br> * localhost: `5`<br> * proxy: `5` |
| `conf_log_level` | String. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#loglevel) | * app: `'notice core:info'`<br> * localhost: `'notice core:info'`<br> * proxy: `'notice core:info'` |
| `conf_options` | String. Sets the `Options` for the `<Directory>` directive.<br>[Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#options) | * app: `'None'`<br> * localhost: `'None'` |
| `conf_proxy_error_override` | String. If you want to have a common look and feel on the error pages seen by the end user, set this to "On" and define them on the reverse proxy server.<br>[Apache Directive](https://httpd.apache.org/docs/2.4/mod/mod_proxy.html#proxyerroroverride) | * proxy: `'On'` |
| `conf_proxy_preserve_host` | String. When enabled, this option will pass the `Host:` line from the incoming request to the proxied host, instead of the hostname specified in the `ProxyPass` line.<br>[Apache Directive](https://httpd.apache.org/docs/2.4/mod/mod_proxy.html#proxypreservehost) | `'Off'` |
| `conf_proxy_timeout` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mod_proxy.html#proxytimeout) | `5` |
| `conf_request_read_timeout` | Number. CIS:<br> * Do not set the Timeout Limits for Request Headers above 40.<br> * Do not set the Timeout Limits for the Request Body above 20.<br>[Apache Directive](https://httpd.apache.org/docs/2.4/mod/mod_reqtimeout.html#requestreadtimeout) | * app: `'header=20-40,MinRate=500 body=20,MinRate=500'`<br> * localhost: `'header=20-40,MinRate=500 body=20,MinRate=500'`<br> * proxy: `'header=20-40,MinRate=500 body=20,MinRate=500'` |
| `conf_server_admin` | String. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#serveradmin) | * app: `{{ apache_httpd__conf_server_admin }}`<br> * localhost: `{{ apache_httpd__conf_server_admin }}`<br> * proxy: `{{ apache_httpd__conf_server_admin }}` |
| `conf_server_alias` | List. Set this only if you need more than one `conf_server_name`.<br>[Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#serveralias) | * app: unset<br> * localhost: unset<br> * proxy: unset |
| `conf_server_name` | String. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#servername) | * app: unset<br> * localhost: unset<br> * proxy: unset<br> * redirect: unset |
| `conf_timeout` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/core.html#timeout) | * app: `{{ apache_httpd__conf_timeout }}`<br> * localhost: `{{ apache_httpd__conf_timeout }}`<br> * proxy: `{{ apache_httpd__conf_timeout }}` |
| `enabled` | Boolean. Enable this vHost. | `true` |
| `filename` | String. The filename of the vHost definition. If not set it defaults to the `conf_server_name` variable. If not set, the filename is automatically suffixed by `.virtualhost_port.conf`. | conf_server_name.virtualhost_port.conf |
| `php_set_handler` | String. Set the handler for PHP<br> * socket-based: `SetHandler "proxy:unix:/run/php-fpm/www.sock\|fcgi://localhost"`<br> * network-based: `SetHandler "proxy:fcgi://127.0.0.1:9000/"` | * app: `'SetHandler "proxy:unix:/run/php-fpm/www.sock\|fcgi://localhost"'`<br> * localhost: `'SetHandler "proxy:unix:/run/php-fpm/www.sock\|fcgi://localhost"'` |
| `raw` | String. It is sometimes desirable to pass variable content that Jinja would handle as variables or blocks. Jinja's `{% raw %}` statement does not work in Ansible. The best and safest solution is to declare `raw` variables as `!unsafe`, to prevent templating errors and information disclosure.  | * app: unset<br> * localhost: unset<br> * proxy: unset<br> * raw: unset<br> * redirect: unset |
| `skip_allowed_file_extensions` | Boolean. Skips checking file extensions in app- and localhost-vHosts, allowing essentially all file extensions. | `false` |
| `skip_allowed_http_methods` | Boolean. Skips checking the HTTP methods in app-, localhost-, proxy-, wordpress-vHosts, allowing essentially all HTTP methods. | `false` |
| `state` | String. Should the vhost definition file be created (`present`) or deleted (`absent`). | * app: unset<br> * localhost: `'present'`<br> * proxy: unset<br> * raw: unset<br> * redirect: unset |
| `template` | String. Have a look at the intro of this paragraph. | unset |
| `virtualhost_ip` | String. Used within the `<VirtualHost {{ virtualhost_ip }}:{{ virtualhost_port }}>` directive. | * app: `'*'`<br> * localhost: `'*'`<br> * proxy: `'*'`<br> * raw: `'*'`<br> * redirect: `'*'` |
| `virtualhost_port` | Number. Used within the `<VirtualHost {{ virtualhost_ip }}:{{ virtualhost_port }}>` directive. | * app: `443`<br> * localhost: `443`<br> * proxy: `443`<br> * raw: `443`<br> * redirect: `80` |

Example: [Have a look here](https://github.com/Linuxfabrik/lfops/blob/main/roles/apache_httpd/EXAMPLES.md).



## Optional Role Variables - mod_dir

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apache_httpd__mod_dir_directory_index` | String. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mod_dir.html#directoryindex) | `'index.html index.htm index.txt'` |


Example:
```yaml
# optional - mod_dir
apache_httpd__mod_dir_directory_index: 'index.html'
```


## Optional Role Variables - mod_log_config

This module is for flexible logging of client requests. Logs are written in a customizable format, and may be written directly to a file, or to an external program. Conditional logging is provided so that individual requests may be included or excluded from the logs based on characteristics of the request.

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apache_httpd__mod_log_config_custom_log` | String. One of<br> * `agent`<br> * `combined`<br> * `combinedio`<br> * `common`<br> * `debug`<br> * `fail2ban`<br> * `linuxfabrikio`<br> * `matomo`<br> * `referer`<br> * `vhost_common`<br>[Apache Directive](https://httpd.apache.org/docs/2.4/mod/mod_log_config.html#customlog) | unset |

Example:
```yaml
# optional - mod_log_config
apache_httpd__mod_log_config_custom_log: 'logs/access.log combined'
```


## Optional Role Variables - mod_security (security2)

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apache_httpd__mod_security_coreruleset_url` | String. The OWASP ModSecurity Core Rule Set (CRS) Download URL. Change this if you are running your own mirror servers. | `'https://github.com/coreruleset/coreruleset/archive'` |
| `apache_httpd__mod_security_coreruleset_version` | String. The OWASP ModSecurity Core Rule Set (CRS) version number without "v". | `'4.4.0'` |
| `apache_httpd__skip_mod_security_coreruleset` | Boolean. Skip the installation of the OWASP ModSecurity Core Rule Set (CRS). | `true` |

Example:
```yaml
# optional - mod_security
apache_httpd__mod_security_coreruleset_url: 'https://github.com/coreruleset/coreruleset/archive'
apache_httpd__mod_security_coreruleset_version: '4.14.0'
apache_httpd__skip_mod_security_coreruleset: true
```


## Optional Role Variables - mod_ssl

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apache_httpd__mod_ssl_ssl_use_stapling` | String. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mod_ssl.html#sslusestapling) | `'on'` |

Example:
```yaml
# optional - mod_ssl
apache_httpd__mod_ssl_ssl_use_stapling: 'on'
```


## Optional Role Variables - mpm_common

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apache_httpd__mpm_common_listen` | List of numbers or strings. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#listen) | `[80]` |


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


| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apache_httpd__mpm_event_max_connections_per_child` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxconnectionsperchild) | `0` |
| `apache_httpd__mpm_event_max_request_workers` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxrequestworkers) | `400` |
| `apache_httpd__mpm_event_max_spare_threads` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxsparethreads) | `250` |
| `apache_httpd__mpm_event_min_spare_threads` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#minsparethreads) | `75` |
| `apache_httpd__mpm_event_start_servers` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#startservers) | `3` |
| `apache_httpd__mpm_event_thread_limit` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#threadlimit) | `64` |
| `apache_httpd__mpm_event_threads_per_child` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#threadsperchild) | `25` |


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

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apache_httpd__mpm_prefork_max_connections_per_child` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxconnectionsperchild) | `0` |
| `apache_httpd__mpm_prefork_max_request_workers` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxrequestworkers) | `256` |
| `apache_httpd__mpm_prefork_max_spare_threads` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxsparethreads) | `10` |
| `apache_httpd__mpm_prefork_min_spare_threads` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#minsparethreads) | `5` |
| `apache_httpd__mpm_prefork_start_servers` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#startservers) | `5` |

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

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apache_httpd__mpm_worker_max_connections_per_child` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxconnectionsperchild) | `0` |
| `apache_httpd__mpm_worker_max_request_workers` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxrequestworkers) | `400` |
| `apache_httpd__mpm_worker_max_spare_threads` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxsparethreads) | `250` |
| `apache_httpd__mpm_worker_min_spare_threads` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#minsparethreads) | `75` |
| `apache_httpd__mpm_worker_start_servers` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#startservers) | `3` |
| `apache_httpd__mpm_worker_thread_limit` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#threadlimit) | `64` |
| `apache_httpd__mpm_worker_threads_per_child` | Number. [Apache Directive](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#threadsperchild) | `25` |


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

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apache_httpd__wsgi_python_home` | String. [Apache Directive](https://modwsgi.readthedocs.io/en/develop/configuration-directives/WSGIPythonHome.html) | `/opt/python` |
| `apache_httpd__wsgi_python_path` | String. [Apache Directive](https://modwsgi.readthedocs.io/en/develop/configuration-directives/WSGIPythonPath.html) | `/var/www/html/python/` |
| `apache_httpd__wsgi_script_alias` | String. [Apache Directive](https://modwsgi.readthedocs.io/en/develop/configuration-directives/WSGIScriptAlias.html) | `/ /var/www/html/python/index.py` |



## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
