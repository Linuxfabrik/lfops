Ansible role lf-apache-httpd
============================

THis README is a big TODO.

This role installs and maintains

* a CIS-compliant Apache
* The global Apache config  (``httpd.conf``)
* Apache Modules  (``mods-available``, ``mods-enabled``)
* Apache configuration snippets (``conf-available``, ``conf-enabled``)
* Apache vHosts (``sites-available``, ``sites-enabled``)

Tested on RHEL 8+ and compatible.

This role configures Apache in the same way as is usual on Debian systems, so quite different to upstream's suggested way to configure the web server. This is because this role attempts to make adding and removing modules, virtual hosts, and extra configuration directives as flexible as possible, in order to make automating the changes and administering the server as easy as possible.

The config is split into several files forming the configuration hierarchy outlined below, all located in the ``/etc/httpd/`` directory:

.. code-block:: text

    /etc/httpd/
    |-- httpd.conf
    |-- conf-enabled
    |   +-- *.conf
    |-- mods-enabled
    |   +-- *.conf
    `-- sites-enabled
        +-- *.conf

We try to avoid using ``<IfModule>`` in the global Apache configuration as well as in the configuration of the vhosts as much as possible in order to facilitate debugging. Otherwise, when using ``<IfModule>``, configuration options are silently dropped, and their absence is very difficult to notice.

For flexibility, use the ``raw`` variable to configure the following topics (have a look at the "Apache vHost Config Snippets" section for some examples):

* SSL/TLS Certificates.
* Quality of Service (``mod_qos`` directives).
* Proxy passing rules.
* Any other configuration instructions not covered in the "Role Variables" chapters.

If you want to check Apache with `our STIG audit script <https://git.linuxfabrik.ch/linuxfabrik-ansible/roles/stig/-/tree/master>`_, run it as follows:

* Application Server: ``./audit.py --lengthy --profile-name='CIS Apache HTTP Server 2.4' --profile-version='v2.0.0' --hostname=web --control-name-exclude='2\.4|2\.6|2\.8|5\.7|6\.6|6\.7``
* Proxy Server: ``./audit.py --lengthy --profile-name='CIS Apache HTTP Server 2.4' --profile-version='v2.0.0' --hostname=web --control-name-exclude='2\.4|2\.6|2\.8|5\.7``

PHP
    This role prefers the use of PHP-FPM over PHP. It does not install either.

SELinux
    Use specialized roles to set specific SELinux Booleans, Policies etc.


Requirements
------------

Mandatory:

* On RHEL-compatible systems, enable the EPEL repository (e.g. use the ``lf-linuxfabrik.lfops.repo_epel`` role) since this role installs ``mod_qos`` from it.
* The ``conf_server_name`` variable for each vHost definition.

Optional:

* Install PHP-FPM, PHP


Tags
----

.. csv-table::
    :header-rows: 1

    Tag,                                What it does
    apache-httpd:vhosts,                "
    | create/remove sites-available configuration
    | enable/disable apache virtual hosts
    | create documentroot for all vhosts"
    apache-httpd:global,                "Create or update global Apache configuration"
    apache-httpd:mods,                  "
    | create/remove mods-available config
    | enable/disable modules"
    apache-httpd:snippets,              "
    | create/remove conf-available snippets
    | enable/disable configuration snippets"
    apache-httpd:crs,                   "Download, verify and install OWASP ModSecurity Core Rule Set (CRS)"
    apache-httpd:modules,               "Ensure base and additional packages are in their desired state"
    apache-httpd:state,                 "Ensure that the httpd service is in the desired state"


Role Variables - Overview
-------------------------

* ``CamelCase`` variables are native Apache directives.
* ``lower_case`` variables are defined by the role itself.
* Variables apply to the global Apache configuration, or to individual areas such as vhosts.
* Have a look at the ``main/defaults.yml`` for the variable defaults.


Role Variables - Global Behaviour
---------------------------------

apache_httpd__deploy_state
~~~~~~~~~~~~~~~~~~~~~~~~~~

What is the desired state which this role should achieve? Possible options:

* ``present``: Ensure that Apache is installed and configured as requested.
* ``absent``: Ensure that Apache is uninstalled and it's configuration is removed.

Default:

.. code-block:: yaml

    apache_httpd__deploy_state: 'present'


apache_httpd__server_type
~~~~~~~~~~~~~~~~~~~~~~~~~

What is the primary use case of this server?

* ``app``: Application Server, for example with PHP.
* ``reverse-proxy``: Reverse Proxy Server.

Default:

.. code-block:: yaml

    apache_httpd__server_type: 'app'


apache_httpd__skip_php
~~~~~~~~~~~~~~~~~~~~~~

Skip PHP configuration globally and in each vHost within Apache.

Default:

.. code-block:: yaml

    apache_httpd__skip_php: True


apache_httpd__skip_php_fpm
~~~~~~~~~~~~~~~~~~~~~~~~~~

Skip PHP-FPM configuration globally and in each vHost within Apache.

Default:

.. code-block:: yaml

    apache_httpd__skip_php_fpm: True


apache_httpd__systemd_enabled
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Whether the Apache webserver service should start on boot (``True``) or not (``False``).

Default:

.. code-block:: yaml

    apache_httpd__systemd_enabled: True


apache_httpd__systemd_state
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure Apache webserver service is in a specific state.

* ``reloaded``
* ``restarted``
* ``started``
* ``stopped``

Default:

.. code-block:: yaml

    apache_httpd__systemd_state: 'started'


Role Variables - Apache Module Installation
-------------------------------------------

Which Apache modules (the role refers to them as "packages" due to package management) need to be installed.

apache_httpd__dependent_packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable allows other Ansible roles to pass configuration to the ``lf-apache-httpd`` role.



apache_httpd__group_packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable is intended to be used in a host inventory group of Ansible (can only be used in one host group at a time).


apache_httpd__host_packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable is intended to be used in the inventory of hosts as needed.


apache_httpd__role_packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable is used in the role internally. It contains the default set of packages that should be installed.




Role Variables - Apache Module Configuration
--------------------------------------------

Which Apache modules need to be configured.


apache_httpd__dependent_modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable allows other Ansible roles to pass configuration to the ``lf-apache-httpd`` role.


apache_httpd__group_modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable is intended to be used in a host inventory group of Ansible (can only be used in one host group at a time).


apache_httpd__host_modules
~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable is intended to be used in the inventory of hosts as needed.


apache_httpd__role_app_modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable is used in the role internally. It contains the default set of modules that should be installed for an application server.


apache_httpd__role_modules
~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable is used in the role internally. It contains the default set of modules that should be installed for any type of server.


apache_httpd__role_proxy_modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Modules for a Reverse Proxy server.

This variable is used in the role internally. It contains the default set of modules that should be installed for a reverse proxy server.


Role Variables - Apache "conf-available"
----------------------------------------

apache_httpd__dependent_snippets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable allows other Ansible roles to pass configuration to the ``lf-apache-httpd`` role.

type:

* ``conf``
* ``raw``

Default:

.. code-block:: yaml

    Have a look at defaults/main.yml


apache_httpd__group_snippets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable is intended to be used in a host inventory group of Ansible (can only be used in one host group at a time).


apache_httpd__host_snippets
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable is intended to be used in the inventory of hosts as needed.


apache_httpd__role_snippets
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable is used in the role internally.



Role Variables - Apache Global Config
-------------------------------------

Configured in the global Apache ``httpd.conf`` or ``apache2.conf``. Most of these variables refer to the "core" module.


apache_httpd__conf_add_default_charset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/core.html#adddefaultcharset

Default:

.. code-block:: yaml

    apache_httpd__conf_add_default_charset: 'UTF-8'


apache_httpd__coreruleset_url
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The OWASP ModSecurity Core Rule Set (CRS) Download URL. Change this if you are running your own mirror servers.

Default:

.. code-block:: yaml

    apache_httpd__coreruleset_url: 'https://github.com/coreruleset/coreruleset/archive'


apache_httpd__coreruleset_version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The OWASP ModSecurity Core Rule Set (CRS) version number without "v".

Default:

.. code-block:: yaml

    apache_httpd__coreruleset_version: '3.3.2'


apache_httpd__coreruleset_checksum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The OWASP ModSecurity Core Rule Set (CRS) SHA1 checksum according to your version.

Default:

.. code-block:: yaml

    apache_httpd__coreruleset_checksum: 'sha1:63aa8ee3f3c9cb23f5639dd235bac1fa1bc64264'


apache_httpd__conf_custom_log
~~~~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/mod_log_config.html#customlog

Default:

.. code-block:: yaml

    apache_httpd__conf_custom_log: 'logs/access log combined'


apache_httpd__conf_directory_index
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/mod_dir.html#directoryindex

Default:

.. code-block:: yaml

    apache_httpd__conf_directory_index: 'index.html index.htm index.txt'


apache_httpd__conf_document_root
~~~~~~~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/core.html#documentroot

Default:

.. code-block:: yaml

    apache_httpd__conf_document_root: '/var/www/html'


apache_httpd__conf_enable_send_file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/core.html#enablesendfile

Default:

.. code-block:: yaml

    apache_httpd__conf_enable_send_file: 'On'


conf_error_log
~~~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/core.html#errorlog

Default:

.. code-block:: yaml

    conf_error_log: 'syslog:local1'


apache_httpd__conf_hostname_lookups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/core.html#hostnamelookups

Default:

.. code-block:: yaml

    apache_httpd__conf_hostname_lookups: 'Off'


apache_httpd__conf_keep_alive
~~~~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/core.html#keepalive

Default:

.. code-block:: yaml

    apache_httpd__conf_keep_alive: 'On'


apache_httpd__conf_limit_request_body
~~~~~~~~~~~~~~~~

vHost types: app, localhost, proxy

https://httpd.apache.org/docs/2.4/mod/core.html#limitrequestbody

Restricts the total size of the HTTP request body sent from the client.

CIS: Do not set it above '102400'.

Default:

.. code-block:: yaml

    apache_httpd__conf_limit_request_body: '102400'


apache_httpd__conf_limit_request_fields
~~~~~~~~~~~~~~~~~~

vHost types: app, localhost, proxy

https://httpd.apache.org/docs/2.4/mod/core.html#limitrequestfields

Limits the number of HTTP request header fields that will be accepted from the client.

CIS: Do not set it above '100'.

Default:

.. code-block:: yaml

    apache_httpd__conf_limit_request_fields: '50'


apache_httpd__conf_limit_request_field_size
~~~~~~~~~~~~~~~~~~~~~

vHost types: app, localhost, proxy

https://httpd.apache.org/docs/2.4/mod/core.html#limitrequestfieldsize

Limits the size of the HTTP request header allowed from the client.

CIS: Do not set it above '1024'.

Default:

.. code-block:: yaml

    apache_httpd__conf_limit_request_field_size: '1024'


apache_httpd__conf_limit_request_line
~~~~~~~~~~~~~~~~

vHost types: app, localhost, proxy

https://httpd.apache.org/docs/2.4/mod/core.html#limitrequestline

Sets the number of *bytes* that will be allowed on the HTTP request-line.

CIS: Do not set it above '512'.

Default:

.. code-block:: yaml

    apache_httpd__conf_limit_request_line: '512'




conf_keep_alive_timeout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/core.html#keepalivetimeout

CIS: Do not set it above '15' seconds.

Default:

.. code-block:: yaml

    conf_keep_alive_timeout: '5'


apache_httpd__conf_listen
~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/mpm_common.html#listen

Default:

.. code-block:: yaml

    apache_httpd__conf_listen: 80


apache_httpd__conf_log_format
~~~~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/mod_log_config.html#logformat

One of

* ``agent``
* ``combined``
* ``common``
* ``debug``
* ``fail2ban``
* ``referer``
* ``vhost_combined``

Default:

.. code-block:: yaml

    apache_httpd__conf_log_format: 'common'


conf_log_level
~~~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/core.html#loglevel

Default:

.. code-block:: yaml

    conf_log_level: 'warn'


apache_httpd__conf_max_keep_alive_requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/core.html#maxkeepaliverequests

Default:

.. code-block:: yaml

    apache_httpd__conf_max_keep_alive_requests: '500'


apache_httpd__conf_server_admin
~~~~~~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/core.html#serveradmin

Default:

.. code-block:: yaml

    apache_httpd__conf_server_admin: 'webmaster@linuxfabrik.ch'


conf_server_name
~~~~~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/core.html#servername

Default:

.. code-block:: yaml

    conf_server_name: 'localhost'


apache_httpd__conf_timeout
~~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/core.html#timeout

CIS: Do not set it above '10' seconds.

Default:

.. code-block:: yaml

    apache_httpd__conf_timeout: '10'


apache_httpd__conf_trace_enable
~~~~~~~~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/core.html#traceenable

CIS: Do not set it to ``On``.

Default:

.. code-block:: yaml

    apache_httpd__conf_trace_enable: 'Off'




Role Variables - Apache Virtual Host Configuration
--------------------------------------------------

Variables used in a vHost definition.

Where to define a vHost?

* If defining a vHost for a host group (``group_vars``): ``apache_httpd__group_vhosts``
* If defining a vHost for a single host (``host_vars``): ``apache_httpd__host_vhosts``
* If writing a role (for example a "Wordpress" role): ``apache_httpd__dependent_vhosts``

The following variables are subkeys of one of the above variables.

allowed_file_extensions
~~~~~~~~~~~~~~~~~~~~~~~

vHost types: app, localhost

The above mentioned vHost types block ALL file extensions by default (including ``.gitignore``, ``.svn``, ``.htaccess``, ``.hg``, ``.bzr`` etc.), unless specifically allowed. Use ``find {{ apache_httpd__conf_document_root }} -type f -name '*.*' | awk -F. '{print $NF }' | sort --unique`` to compile a list of the file extensions that are currently present.

Hint: The config ensures that filenames starting with a dot (".") are never matched.

Default:

.. code-block:: yaml

    allowed_file_extensions:
      - 'css'
      - 'gif'
      - 'html?'
      - 'ico'
      - 'jpe?g'
      - 'js'
      - 'pdf'
      - 'php'
      - 'png'
      - 'ttf'
      - 'txt'
      - 'woff2?'


allowed_http_methods
~~~~~~~~~~~~~~~~~~~~

vHost types: app, localhost, proxy

Should be used to disable unwanted `HTTP methods <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods>`_. Only the explicity listed ones are allowed. Returns a `405 - Method Not Allowed <https://en.wikipedia.org/wiki/List_of_HTTP_status_codes>`_ if a forbidden HTTP method is used.

This does not disable TRACE.

Always enable GET and OPTIONS at least. For an OPTIONS request, Apache always returns ``Allow: GET,POST,OPTIONS,HEAD``, no matter what.

We are NOT using `LimitExcept <https://httpd.apache.org/docs/2.4/mod/core.html#limitexcept>`_ because this directive is not allowed in a VirtualHost context.

Available HTTP methods:

* CONNECT
* DELETE
* GET
* HEAD
* OPTIONS
* PATCH
* POST
* PUT

Available WebDAV methods:

* COPY
* LOCK
* MKCOL
* MOVE
* PROPFIND
* PROPPATCH
* UNLOCK

Default:

.. code-block:: yaml

    allowed_http_methods:
      - 'GET'
      - 'OPTIONS'


AllowOverride
~~~~~~~~~~~~~

vHost types: app, localhost

https://httpd.apache.org/docs/2.4/mod/core.html#allowoverride

Types of directives that are allowed in ``.htaccess`` files. Will be set in the ``<Directory {{ apache_httpd__conf_document_root }}/{{ item.conf_server_name }}>`` directive of the vHost.

Default:

.. code-block:: yaml

    AllowOverride: 'None'


apache_httpd__dependent_vhosts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable allows other Ansible roles to pass configuration to the ``lf-apache-httpd`` role.

Default:

.. code-block:: yaml

    apache_httpd__dependent_vhosts: []


apache_httpd__group_vhosts
~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable is intended to be used in a host inventory group of Ansible (can only be used in one host group at a time).

Default:

.. code-block:: yaml

    apache_httpd__group_vhosts: []


apache_httpd__host_vhosts
~~~~~~~~~~~~~~~~~~~~~~~~~

This variable is intended to be used in the inventory of hosts as needed.

Default:

.. code-block:: yaml

    apache_httpd__host_vhosts: []


apache_httpd__role_vhosts
~~~~~~~~~~~~~~~~~~~~~~~~~

This variable is used in the role internally.


apache_httpd__vhost_type
~~~~~~~~~~~~~~~~~~~~~~~~

The default template type to use for virtual hosts.

Default:

.. code-block:: yaml

    apache_httpd__vhost_type: 'app'


authz_document_root
~~~~~~~~~~~~~~~~~~~

vHost types: app, localhost

Authorization statement for the ``DocumentRoot {{ apache_httpd__conf_document_root }}/{{ item.conf_server_name }}`` directive.

Default:

.. code-block:: yaml

    authz_document_root: |-
        Require local

Example:

.. code-block:: yaml

    authz_document_root: |-
        Require local
        # allow reverse proxys
        Require ip 192.168.109.7
        Require ip 192.168.109.35


authz_file_extensions
~~~~~~~~~~~~~~~~~~~~~

vHost types: app, localhost

Authorization statement for the https://httpd.apache.org/docs/2.4/mod/core.html#filesmatch directive which is based on ``allowed_file_extensions``.

Default:

.. code-block:: yaml

    authz_file_extensions: |-
        Require local

Example:

.. code-block:: yaml

    authz_file_extensions: |-
        Require local
        # allow reverse proxys
        Require ip 192.168.209.7
        Require ip 192.168.209.35


by_role
~~~~~~~

vHost types: app, localhost, proxy, redirect, raw

If defined it results in a comment ``# Generated by Ansible role: {{ item.by_role }}`` at the beginning of a vHost definition.


comment
~~~~~~~

vHost types: app, localhost, proxy, raw

Describes the vHost and results in a comment right above the ``<VirtualHost>`` section.

Default:

.. code-block:: yaml

    comment: 'no description available'

Example:

.. code-block:: yaml

    comment: 'Runs MyApp on Port 443. This vHost is hardened.'


conf_custom_log
~~~~~~~~~

vHost types: app, localhost, proxy

https://httpd.apache.org/docs/2.4/mod/mod_log_config.html#customlog

If undefined, no logs are written. You might want to configure it for debugging reasons or software like fail2ban.

One of

* ``agent``
* ``combined``
* ``common``
* ``debug``
* ``fail2ban``
* ``referer``
* ``vhost_combined``

Default:

    No custom log.

Example:

.. code-block:: yaml

    conf_custom_log: 'logs/myapp.example.com-access.log combined'


DirectoryIndex
~~~~~~~~~~~~~~

vHost types: app

https://httpd.apache.org/docs/2.4/mod/mod_dir.html#directoryindex

Default:

.. code-block:: yaml

    DirectoryIndex: 'index.html index.htm index.txt'


enabled
~~~~~~~

Enable this vHost (True/False).

Default:

.. code-block:: yaml

    enabled: True


conf_error_log
~~~~~~~~

vHost types: app, localhost, proxy

https://httpd.apache.org/docs/2.4/mod/core.html#errorlog

Default:

.. code-block:: yaml

    conf_error_log: 'logs/{{ conf_server_name }}-error.log'

Example:

.. code-block:: yaml

    conf_error_log: 'syslog:local1'


filename
~~~~~~~~

The filename of the vHost definition. If not set it defaults to the ``conf_server_name`` variable. The filename is automatically suffixed by ``.virtualhost_port.conf``.

Default:

.. code-block:: yaml

    filename: "conf_server_name.virtualhost_port.conf"

Example:

.. code-block:: yaml

    filename: 'myapp.example.com'


conf_keep_alive_timeout
~~~~~~~~~~~~~~~~

vHost types: app, localhost, proxy

https://httpd.apache.org/docs/2.4/mod/core.html#keepalivetimeout

CIS: Do not set it above '15' seconds.

Default:

.. code-block:: yaml

    conf_keep_alive_timeout: '5'


conf_log_level
~~~~~~~~

vHost types: app, localhost, proxy

https://httpd.apache.org/docs/2.4/mod/core.html#loglevel

Default:

.. code-block:: yaml

    conf_log_level: 'notice core:info'


Options
~~~~~~~

vHost types: app, localhost

https://httpd.apache.org/docs/2.4/mod/core.html#options

Sets the ``Options`` for the ``<Directory {{ apache_httpd__conf_document_root }}/{{ item.conf_server_name }}>`` directive.

Default:

.. code-block:: yaml

    Options: 'None'


php_set_handler
~~~~~~~~~~~~~~~

vHost types: app, localhost

Set the handler for PHP

* socket-based: ``SetHandler "proxy:unix:/run/php-fpm/www.sock|fcgi://localhost"``
* network-based: ``SetHandler "proxy:fcgi://127.0.0.1:9000/"``

Default:

.. code-block:: yaml

    php_set_handler: 'SetHandler "proxy:unix:/run/php-fpm/www.sock|fcgi://localhost"'


ProxyErrorOverride
~~~~~~~~~~~~~~~~~~

https://httpd.apache.org/docs/2.4/mod/mod_proxy.html#proxyerroroverride

vHost types: proxy

If you want to have a common look and feel on the error pages seen by the end user, set this to "On" and define them on the reverse proxy server.

Default:

.. code-block:: yaml

    ProxyErrorOverride: 'On'


ProxyPreserveHost
~~~~~~~~~~~~~~~~~~

vHost types: proxy

https://httpd.apache.org/docs/2.4/mod/mod_proxy.html#proxypreservehost

When enabled, this option will pass the ``Host:`` line from the incoming request to the proxied host, instead of the hostname specified in the ``ProxyPass`` line.

Default:

.. code-block:: yaml

    ProxyPreserveHost: 'Off'


ProxyTimeout
~~~~~~~~~~~~

vHost types: proxy

https://httpd.apache.org/docs/2.4/mod/mod_proxy.html#proxytimeout

Default:

.. code-block:: yaml

    ProxyTimeout: '5'


raw
~~~

vHost types: app, localhost, proxy, raw

It is sometimes desirable to pass variable content that Jinja would handle as variables or blocks. Jinja's ``{% raw %}`` statement does not work in Ansible. The best and safest solution is to declare ``raw`` variables as ``!unsafe``, to prevent templating errors and information disclosure.

For example to pass ``{%Y-...``, use ``raw`` like this:

.. code-block:: yaml

    raw: !unsafe |-
        LogFormat "%h %u [%{%Y-%m-%d %H:%M:%S}t.%{usec_frac}t] \"%r\" %>s %b" mylog


conf_request_read_timeout
~~~~~~~~~~~~~~~~~~

vHost types: app, localhost, proxy

https://httpd.apache.org/docs/2.4/mod/mod_reqtimeout.html#requestreadtimeout

CIS:

* Do not set the Timeout Limits for Request Headers above 40.
* Do not set the Timeout Limits for the Request Body above 20.

Default:

.. code-block:: yaml

    conf_request_read_timeout: 'header=20-40,MinRate=500 body=20,MinRate=500'


conf_server_admin
~~~~~~~~~~~

vHost types: app, localhost, proxy

https://httpd.apache.org/docs/2.4/mod/core.html#serveradmin

Default:

.. code-block:: yaml

    conf_server_admin: 'webmaster@linuxfabrik.ch'


conf_server_alias
~~~~~~~~~~~

vHost types: app, localhost, proxy

https://httpd.apache.org/docs/2.4/mod/core.html#serveralias

Set this only if you need more than one ``conf_server_name``.


conf_server_name
~~~~~~~~~~

vHost types: app, localhost, proxy

https://httpd.apache.org/docs/2.4/mod/core.html#servername

Mandatory.


Example:

.. code-block:: yaml

    conf_server_name: 'myapp.example.com'


state
~~~~~

Should the vhost definition file be created (``present``) or deleted (``absent``).

Default:

.. code-block:: yaml

    state: 'present'


type
~~~~

Define the vHost type to deploy (have a look at the templates for details). One of:

* | ``app``
  | A hardened vHost running an application like Nextcloud, Wordpress etc. with the most common options. Can be extended by using the ``raw`` variable.
* | ``dont-touch``
  |  Needed if you just want to enable/disable an existing vHost using Ansible, but the vHost definition file should not be touched at all.
* | ``localhost``
  | A hardened, pre-defined VirtualHost just listening on https://localhost, and only accessible from localhost. Due to its naming, it is the first defined vHost. Useful for Apache status info etc. Can be extended by using the ``raw`` variable. The following URLs are pre-configured, accessible just from localhost: ``/fpm-ping``, ``/fpm-status``, ``/monitoring.php``, ``/server-info``, ``/server-status``.
* | ``proxy``
  | A typical hardened reverse proxy vHost. Can be extended by using the ``raw`` variable. This proxy vHost definition prevents Apache from functioning as a forward proxy server (inside > out).
* | ``redirect``
  | A vHost that redirects from one port (default "80") to another (default "443"). Custom redirect rules can be provided using the ``raw`` variable.
* | ``raw``
  | If none of the above vHost types fit, use the ``raw`` one and define everything except ``<VirtualHost>`` and ``</VirtualHost>`` completely from scratch.

"Hardened" means among other things:

* Old HTTP protocol (< HTTP/1.1) versions are disallowed.
* IP address based requests are disallowed.
* Number of bytes that are allowed in a request are limited.
* etc.


virtualhost_ip
~~~~~~~~~~~~~~

vHost types: app, localhost, proxy, raw, redirect

Used within the ``<VirtualHost {{ virtualhost_ip }}:{{ virtualhost_port }}>`` directive.

Default:

.. code-block:: yaml

    virtualhost_ip: '*'


virtualhost_port
~~~~~~~~~~~~~~~~

vHost types: app, localhost, proxy, raw, redirect

Used within the ``<VirtualHost {{ virtualhost_ip }}:{{ virtualhost_port }}>`` directive.

Default:

.. code-block:: yaml

    virtualhost_port: 443


Apache vHost Config Snippets
----------------------------

Config options at your free disposal for the ``raw`` variable (which is inserted just before the closing ``VirtualHost`` directive). Unsorted.

Usage:

.. code-block:: yaml

    raw: !unsafe |-
      # my config here...

A list of best practise Apache Config-Snippets. Use them as a starting point.


Redirect from port 80 to port 443
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Including one exception:

.. code-block:: text

    RewriteCond %{SERVER_PORT} 80
    RewriteCond %{REQUEST_URI} !^/\.well\-known/acme\-challenge/
    RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]


HTTP Basic Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~

CIS: You do not want to use this - it does not meet current security standards for protecting the login credentials and protecting the authenticated session.

.. code-block:: text

    <Location />
        AuthType Basic
        AuthName "Restricted Area"
        AuthBasicProvider file
        AuthUserFile /etc/httpd/.htpasswd
        Require user linuxfabrik-user
    </Location>


Require directive examples
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Require all denied
    Require all granted

    # complete subnet
    Require ip 10.80

    # a single IP
    Require ip 192.168.109.7
    Require local
    Require user linuxfabrik-user


Security related HTTP headers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    # Headers sorted by Category and Header Name
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers

    # Caching
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control

    # Caching: Maybe disable browser's cache validation due to cache poisoning attacks
    #Header unset ETag

    # The Cache-Control header is defined as part of HTTP/1.1 specifications and supersedes previous headers (e.g. Expires).
    # The maximum amount of time a resource is considered fresh, relative to the time of the request.
    # Caching: holds instructions for caching in both requests and responses
    #Header set Cache-Control: "max-age=0, no-cache, no-store, must-revalidate"
    # the .+ at the start of the regex ensures that files named ".png", or ".gif", for example, are not matched
    <FilesMatch ".+\.(css|flv|gif|html?|ico|jpe?g|js|png|svg|swf|ttf|txt|woff2?)$">
       Header always set Cache-Control "max-age=864000, public"
    </FilesMatch>

    # Security related Header: CSP allows to control resources the user agent is allowed to
    # load for a given page (helps guard against cross-site scripting attacks). Always use
    # "default-src 'none'", especially for APIs.
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy

    # Sample Safe Policy - start using this:
    Header always set Content-Security-Policy: "\
        default-src 'none'; \
        base-uri 'none'; \
        block-all-mixed-content; \
        child-src 'none'; \
        connect-src 'none'; \
        font-src 'none'; \
        form-action 'none'; \
        frame-ancestors 'none'; \
        frame-src 'none'; \
        img-src 'none'; \
        manifest-src 'none'; \
        media-src 'none'; \
        object-src 'none'; \
        prefetch-src 'none'; \
        require-trusted-types-for 'script'; \
        sandbox; \
        script-src 'none'; \
        style-src 'none'; \
        worker-src 'none'; \
        "

    # A Report-Only Policy (for Browser Console)
    #Header always set Content-Security-Policy-Report-Only: "\
    #    default-src 'none'; \
    #    base-uri 'none'; \
    #    block-all-mixed-content; \
    #    child-src 'none'; \
    #    connect-src 'none'; \
    #    font-src 'none'; \
    #    form-action 'none'; \
    #    frame-ancestors 'none'; \
    #    frame-src 'none'; \
    #    img-src 'none'; \
    #    manifest-src 'none'; \
    #    media-src 'none'; \
    #    object-src 'none'; \
    #    prefetch-src 'none'; \
    #    require-trusted-types-for 'script'; \
    #    sandbox; \
    #    script-src 'none'; \
    #    style-src 'none'; \
    #    worker-src 'none'; \
    #    "

    # A real-life example for docs.linuxfabrik.ch
    #Header always set Content-Security-Policy: " \
    #    default-src 'self'; \
    #    base-uri 'none'; \
    #    child-src 'none'; \
    #    connect-src 'self' https://analytics.linuxfabrik.ch; \
    #    font-src 'self' https://use.fontawesome.com; \
    #    form-action 'self'; \
    #    frame-ancestors 'none'; \
    #    frame-src 'none'; \
    #    img-src 'self' https://analytics.linuxfabrik.ch https://img.shields.io; \
    #    manifest-src 'none'; \
    #    media-src 'none'; \
    #    object-src 'none'; \
    #    prefetch-src 'none'; \
    #    sandbox allow-same-origin allow-forms allow-scripts; \
    #    script-src 'self' 'unsafe-eval' 'unsafe-inline' https://analytics.linuxfabrik.ch https://use.fontawesome.com; \
    #    style-src 'self' 'unsafe-inline' https://use.fontawesome.com; \
    #    worker-src 'none'; \
    #    "
    # Also set this if CSP directives uses any "unsafe" values.
    #Header always set X-XSS-Protection: "1; mode=block"

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin
    # Security Header: indicates whether the response can be shared with requesting code from the given origin
    Header always set Access-Control-Allow-Origin "https://test.linuxfabrik.ch"
    #  the response should also include a Vary response header with the value Origin — to indicate to browsers that server responses can differ based on the value of the Origin request header.
    Header always set Vary "Origin"

    # Security Header: lets sites opt in to reporting and/or enforcement of Certificate Transparency requirements, to prevent the use of misissued certificates from going unnoticed
    Header always set Expect-CT: "max-age=86400, enforce"
    # Security Header: allows a site to control which features and APIs can be used in the browser
    Header always set Permissions-Policy: "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()"
    # Security Header: controls how much referrer information (sent via the Referer header) should be included with requests
    Header always set Referrer-Policy: "strict-origin-when-cross-origin"
    # Security Header: stops a browser from trying to MIME-sniff the content type and forces it to stick with the declared content-type
    Header always set X-Content-Type-Options: "nosniff"
    # Security Header: tells the browser whether you want to allow your site to be framed or not. "frame-ancestors" in CSP is used instead.
    #Header always set X-Frame-Options: "SAMEORIGIN"
    # Security Header: feature of Internet Explorer, Chrome and Safari that stops pages from loading when they detect reflected cross-site scripting (XSS) attacks
    # Note: Most major browsers have dropped / deprecated support for this header in 2020.

    # User-Agent Detection: Use for websites without Responsive Web Design, or
    # where the addition of a DEFLATE filter depends on the User-Agent.
    #Header append Vary: "User-Agent"

    # Proxy: may also needs changes to the backend web application
    RequestHeader set X-Forwarded-Proto "https"


SSL/TLS settings
~~~~~~~~~~~~~~~~

.. code-block:: text

    SSLEngine on
    SSLCertificateFile      {{ apache_httpd__openssl_certificate_path }}/localhost.pem
    SSLCertificateKeyFile   {{ apache_httpd__openssl_privatekey_path }}/localhost.key
    SSLCertificateChainFile {{ apache_httpd__openssl_chain_path }}/chain.pem


mod_qos / Quality of Service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`mod_qos <http://mod-qos.sourceforge.net/index.html>`_: If you decide to use HTTP/2, you should only use the request level control directives ("QS_Loc\*") as mod_qos works for the hypertext transfer protocol version 1.0 and 1.1 (RFC1945/RFC2616) only. If not using HTTP/2, you can use the full feature set of mod_qos, like this:

.. code-block:: text

    <IfModule qos_module>
        BrowserMatch "(curl|rclone|rsync|wget)" QS_Cond=tools

        # Defines the maximum allowed number of concurrent TCP connections for this virtual host.
        QS_SrvMaxConn                          100

        # Defines the maximum number of connections per source IP address for this virtual host.
        QS_SrvMaxConnPerIP                     1

        # Defines the number of concurrent requests for the specified request pattern (path and query).
        QS_LocRequestLimitMatch       "^.*$"   100

        # Only enforced for requests whose QS_Cond variable matches the specified condition:
        BrowserMatch "(curl|rclone|rsync|wget)" QS_Cond=tools
        QS_CondLocRequestLimitMatch   "^.*$"   1    tools

        # limits the download bandwidth when accessing MP4 files to 1 megabyte/sec
        # and does not allow more then 1 client to download such file type in
        # parallel:
        QS_LocKBytesPerSecLimitMatch \.mp4     1
        QS_LocRequestLimitMatch      \.mp4     1

        # Throttles the download bandwidth for the specified request pattern (path and query, in KBytes/sec).
        # If you want to throttle to 10 Mbit/sec (should be the default minimum), you have to provide "1250"
        # (multiply the data transfer rate value by 125).
        QS_LocKBytesPerSecLimitMatch  "^.*$"   1250
    </IfModule>


Proxy Passing Rules
~~~~~~~~~~~~~~~~~~~

BTW, using mod_rewrite is much more flexible than ProxyPass. This is an example of a reverse proxy passing incoming requests to a backend server.

.. code-block:: text

    # proxy_module and other
    <Proxy *>
        Require all granted
    </Proxy>
    SSLProxyEngine On
    SSLProxyCheckPeerCN Off
    SSLProxyCheckPeerExpire On
    RewriteRule ^/(.*) https://backend/$1 [proxy,last]
    ProxyPassReverse / https://backend/


mod_maxminddb, GeoIP-Blocking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As a starting point, have a look at https://docs.linuxfabrik.ch for details.

.. code-block:: text

    # GeoIP-Blocking
    MaxMindDBEnable On
    MaxMindDBFile COUNTRY_DB /usr/share/GeoIP/GeoLite2-Country.mmdb
    MaxMindDBEnv MM_COUNTRY_CODE COUNTRY_DB/country/iso_code

    # Deny all, but allow some specific countries, ordered alphabetically
    SetEnvIf MM_COUNTRY_CODE AT AllowCountry
    SetEnvIf MM_COUNTRY_CODE CH AllowCountry
    SetEnvIf MM_COUNTRY_CODE DE AllowCountry
    <Proxy *>
        <RequireAny>
            Require env AllowCountry
            # list of IP's in an external file, containing lines like
            # Require ip 10.1
            Include /etc/GeoIP-Whitelist.conf
        </RequireAny>
    </Proxy>


mod_security + OWASP CRS Rule Set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Will be installed on reverse proxy servers only.

As a starting point. Replace ``<MYVHOST>`` with your ``conf_server_name`` or FQDN.

.. code-block:: text

    <IfModule security2_module>

        LogFormat "%h %{GEOIP_COUNTRY_CODE}e %u [%{%Y-%m-%d %H:%M:%S}t.%{usec_frac}t] \"%r\" %>s %b \
        \"%{Referer}i\" \"%{User-Agent}i\" \"%{Content-Type}i\" %{remote}p %v %A %p %R \
        %{BALANCER_WORKER_ROUTE}e %X \"%{cookie}n\" %{UNIQUE_ID}e %{SSL_PROTOCOL}x %{SSL_CIPHER}x \
        %I %O %{ratio}n%% %D %{ModSecTimeIn}e %{ApplicationTime}e %{ModSecTimeOut}e \
        %{ModSecAnomalyScoreInPLs}e %{ModSecAnomalyScoreOutPLs}e \
        %{ModSecAnomalyScoreIn}e %{ModSecAnomalyScoreOut}e" extended

        LogFormat "[%{%Y-%m-%d %H:%M:%S}t.%{usec_frac}t] %{UNIQUE_ID}e %D \
        PerfModSecInbound: %{TX.perf_modsecinbound}M \
        PerfAppl: %{TX.perf_application}M \
        PerfModSecOutbound: %{TX.perf_modsecoutbound}M \
        TS-Phase1: %{TX.ModSecTimestamp1start}M-%{TX.ModSecTimestamp1end}M \
        TS-Phase2: %{TX.ModSecTimestamp2start}M-%{TX.ModSecTimestamp2end}M \
        TS-Phase3: %{TX.ModSecTimestamp3start}M-%{TX.ModSecTimestamp3end}M \
        TS-Phase4: %{TX.ModSecTimestamp4start}M-%{TX.ModSecTimestamp4end}M \
        TS-Phase5: %{TX.ModSecTimestamp5start}M-%{TX.ModSecTimestamp5end}M \
        Perf-Phase1: %{PERF_PHASE1}M \
        Perf-Phase2: %{PERF_PHASE2}M \
        Perf-Phase3: %{PERF_PHASE3}M \
        Perf-Phase4: %{PERF_PHASE4}M \
        Perf-Phase5: %{PERF_PHASE5}M \
        Perf-ReadingStorage: %{PERF_SREAD}M \
        Perf-WritingStorage: %{PERF_SWRITE}M \
        Perf-GarbageCollection: %{PERF_GC}M \
        Perf-ModSecLogging: %{PERF_LOGGING}M \
        Perf-ModSecCombined: %{PERF_COMBINED}M" perflog

        conf_error_logFormat "[%{cu}t] [%-m:%-l] %-a %-L %M"
        conf_log_level debug

        conf_error_log logs/modsec-<MYVHOST>-error.log
        conf_custom_log  logs/modsec-<MYVHOST>-access.log extended
        conf_custom_log  logs/modsec-<MYVHOST>-perf.log perflog env=write_perflog


        # == ModSec Base Configuration

        SecRuleEngine                 On

        SecRequestBodyAccess          On
        SecRequestBodyLimit           10000000
        SecRequestBodyNoFilesLimit    64000

        SecResponseBodyAccess         On
        SecResponseBodyLimit          10000000

        SecTmpDir                     /tmp/
        SecUploadDir                  /tmp/

        SecDebugLog                   logs/modsec-<MYVHOST>-debug.log
        SecDebugconf_log_level              0

        SecAuditEngine                RelevantOnly
        SecAuditLogRelevantStatus     "^(?:5|4(?!04))"
        SecAuditLogParts              ABEFHIJKZ

        SecAuditLogType               Concurrent
        SecAuditLog                   logs/modsec-<MYVHOST>-audit.log
        SecAuditLogStorageDir         logs/audit/

        SecDefaultAction              "phase:2,pass,log,tag:'Local Lab Service'"


        # == ModSec Rule ID Namespace Definition
        # Service-specific before Core Rule Set: 10000 -  49999
        # Service-specific after Core Rule Set:  50000 -  79999
        # Locally shared rules:                  80000 -  99999
        #  - Performance:                        90000 -  90199
        # Recommended ModSec Rules (few):       200000 - 200010
        # OWASP Core Rule Set:                  900000 - 999999


        # === ModSec timestamps at the start of each phase (ids: 90000 - 90009)

        SecAction "id:90000,phase:1,nolog,pass,setvar:TX.ModSecTimestamp1start=%{DURATION}"
        SecAction "id:90001,phase:2,nolog,pass,setvar:TX.ModSecTimestamp2start=%{DURATION}"
        SecAction "id:90002,phase:3,nolog,pass,setvar:TX.ModSecTimestamp3start=%{DURATION}"
        SecAction "id:90003,phase:4,nolog,pass,setvar:TX.ModSecTimestamp4start=%{DURATION}"
        SecAction "id:90004,phase:5,nolog,pass,setvar:TX.ModSecTimestamp5start=%{DURATION}"

        # SecRule REQUEST_FILENAME "@beginsWith /" \
        #    "id:90005,phase:5,t:none,nolog,noauditlog,pass,setenv:write_perflog"


        # === ModSec Recommended Rules (in modsec src package) (ids: 200000-200010)

        SecRule REQUEST_HEADERS:Content-Type "(?:application(?:/soap\+|/)|text/)xml" \
          "id:200000,phase:1,t:none,t:lowercase,pass,nolog,ctl:requestBodyProcessor=XML"

        SecRule REQUEST_HEADERS:Content-Type "application/json" \
          "id:200001,phase:1,t:none,t:lowercase,pass,nolog,ctl:requestBodyProcessor=JSON"

        SecRule REQBODY_ERROR "!@eq 0" \
          "id:200002,phase:2,t:none,deny,status:400,log,msg:'Failed to parse request body.',\
        logdata:'%{reqbody_error_msg}',severity:2"

        SecRule MULTIPART_STRICT_ERROR "!@eq 0" \
        "id:200003,phase:2,t:none,log,deny,status:403, \
        msg:'Multipart request body failed strict validation: \
        PE %{REQBODY_PROCESSOR_ERROR}, \
        BQ %{MULTIPART_BOUNDARY_QUOTED}, \
        BW %{MULTIPART_BOUNDARY_WHITESPACE}, \
        DB %{MULTIPART_DATA_BEFORE}, \
        DA %{MULTIPART_DATA_AFTER}, \
        HF %{MULTIPART_HEADER_FOLDING}, \
        LF %{MULTIPART_LF_LINE}, \
        SM %{MULTIPART_MISSING_SEMICOLON}, \
        IQ %{MULTIPART_INVALID_QUOTING}, \
        IP %{MULTIPART_INVALID_PART}, \
        IH %{MULTIPART_INVALID_HEADER_FOLDING}, \
        FL %{MULTIPART_FILE_LIMIT_EXCEEDED}'"

        SecRule TX:/^MSC_/ "!@streq 0" \
          "id:200005,phase:2,t:none,deny,status:500,\
          msg:'ModSecurity internal error flagged: %{MATCHED_VAR_NAME}'"


        # === ModSec Core Rule Set Base Configuration (ids: 900000-900999)

        Include    modsecurity.d/crs/crs-setup.conf

        SecAction "id:900110,phase:1,pass,nolog,\
          setvar:tx.inbound_anomaly_score_threshold=5,\
          setvar:tx.outbound_anomaly_score_threshold=4"

        SecAction "id:900000,phase:1,pass,nolog,\
          setvar:tx.paranoia_level=1"


        # === ModSec Core Rule Set: Runtime Exclusion Rules (ids: 10000-49999)

        # ...


        # === ModSecurity Core Rule Set Inclusion

        Include    modsecurity.d/crs/rules/*.conf


        # === ModSec Core Rule Set: Startup Time Rules Exclusions

        # Disables 403 status code after login into the application
        SecRuleRemoveById 920420


        # === ModSec timestamps at the end of each phase (ids: 90010 - 90019)

        SecAction "id:90010,phase:1,pass,nolog,setvar:TX.ModSecTimestamp1end=%{DURATION}"
        SecAction "id:90011,phase:2,pass,nolog,setvar:TX.ModSecTimestamp2end=%{DURATION}"
        SecAction "id:90012,phase:3,pass,nolog,setvar:TX.ModSecTimestamp3end=%{DURATION}"
        SecAction "id:90013,phase:4,pass,nolog,setvar:TX.ModSecTimestamp4end=%{DURATION}"
        SecAction "id:90014,phase:5,pass,nolog,setvar:TX.ModSecTimestamp5end=%{DURATION}"


        # === ModSec performance calculations and variable export (ids: 90100 - 90199)

        SecAction "id:90100,phase:5,pass,nolog,\
          setvar:TX.perf_modsecinbound=%{PERF_PHASE1},\
          setvar:TX.perf_modsecinbound=+%{PERF_PHASE2},\
          setvar:TX.perf_application=%{TX.ModSecTimestamp3start},\
          setvar:TX.perf_application=-%{TX.ModSecTimestamp2end},\
          setvar:TX.perf_modsecoutbound=%{PERF_PHASE3},\
          setvar:TX.perf_modsecoutbound=+%{PERF_PHASE4},\
          setenv:ModSecTimeIn=%{TX.perf_modsecinbound},\
          setenv:ApplicationTime=%{TX.perf_application},\
          setenv:ModSecTimeOut=%{TX.perf_modsecoutbound},\
          setenv:ModSecAnomalyScoreInPLs=%{tx.anomaly_score_pl1}-%{tx.anomaly_score_pl2}-%{tx.anomaly_score_pl3}-%{tx.anomaly_score_pl4},\
          setenv:ModSecAnomalyScoreOutPLs=%{tx.outbound_anomaly_score_pl1}-%{tx.outbound_anomaly_score_pl2}-%{tx.outbound_anomaly_score_pl3}-%{tx.outbound_anomaly_score_pl4},\
          setenv:ModSecAnomalyScoreIn=%{TX.anomaly_score},\
          setenv:ModSecAnomalyScoreOut=%{TX.outbound_anomaly_score}"
    </IfModule>


Apache Modules
--------------

mod_security
~~~~~~~~~~~~

Requires mod_unique (which is per default loaded).


mpm_event
~~~~~~~~~

Conflicts: mpm_worker, mpm_prefork

TLDR: event MPM: A variant of the worker MPM with the goal of consuming
threads only for connections with active processing
See: http://httpd.apache.org/docs/2.4/mod/event.html

Event: Based on worker, this MPM goes one step further by optimizing how the parent process
schedules tasks to the child processes and the threads associated to those. A connection stays
open for 5 seconds by default and closes if no new event happens; this is the keep-alive
directive default value, which retains the thread associated to it. The Event MPM enables the
process to manage threads so that some threads are free to handle new incoming connections while
others are kept bound to the live connections. Allowing re-distribution of assigned tasks to
threads will make for better resource utilization and performance.

Best for PHP-FPM. Default.


mpm_prefork
~~~~~~~~~~~

Conflicts: mpm_worker, mpm_event

TLDR: prefork MPM: Implements a non-threaded, pre-forking web server
See: http://httpd.apache.org/docs/2.4/mod/prefork.html

Pre-fork: A new process is created for each incoming connection reaching the server. Each process
is isolated from the others, so no memory is shared between them, even if they are performing
identical calls at some point in their execution. This is a safe way to run applications linked
to libraries that do not support threading—typically older applications or libraries.

NOTE: If enabling prefork, the httpd_graceful_shutdown SELinux
boolean should be enabled, to allow graceful stop/shutdown.

Best for Standard PHP running any version of ``mod_php``. Does not work with http2.


mpm_worker
~~~~~~~~~~

Conflicts: mpm_event, mpm_prefork

TLDR: worker MPM: Multi-Processing Module implementing a hybrid
multi-threaded multi-process web server
See: http://httpd.apache.org/docs/2.4/mod/worker.html

Worker: A parent process is responsible for launching a pool of child processes, some of which
are listening for new incoming connections, and others are serving the requested content. Each
process is threaded (a single thread can handle one connection) so one process can handle several
requests concurrently. This method of treating connections encourages better resource
utilization, while still maintaining stability. This is a result of the pool of available
processes, which often has free available threads ready to immediately serve new connections.

Best for mod_qos if you intend to use any connection level control directive ("QS_Srv*"),
which is normally done on a Reverse Proxy.
Works with PHP-FPM, too.


php, php7
~~~~~~~~~

Loading PHP by running ``mod_php`` with httpd in ``mpm_prefork`` mode . Deprecated as FPM is now preferred with httpd in ``mpm_event`` mode.


proxy
~~~~~

Needed for PHP-FPM on App-Servers and on Proxy-Servers.


proxy_http
~~~~~~~~~~

Needed for PHP-FPM on App-Servers and on Proxy-Servers.


Example Playbook
----------------

A minimal playbook for "MyApp" could be:

.. code-block:: yaml

    - name: 'Install and manage MyApp with a webserver'
      hosts:
        - myhost
      become: True

      roles:

        - role: 'lf-apache-httpd'
          apache_httpd__dependent_modules:
            - '{{ myapp__apache_httpd__dependent_modules|d({}) }}'
          apache_httpd__dependent_snippets:
            - '{{ myapp__apache_httpd__dependent_snippets|d({}) }}'
          apache_httpd__dependent_vhosts:
            - '{{ myapp__apache_httpd__dependent_vhosts|d({}) }}'

        - role: 'myapp'

A nearly complete "app" vHost definition which is injected into the Apache role by the ``myapp`` role could look like this:

.. code-block:: yaml

    myapp__apache_httpd__dependent_vhosts:

      - by_role: 'myapp'
        comment: 'Runs MyApp on Port 443. This vHost is hardened.'
        enabled: true
        filename: 'myapp.example.com'
        state: 'present'
        type: 'app'

        allowed_file_extensions:
          - 'css'
          - 'gif'
          - 'html?'
          - 'ico'
          - 'jpe?g'
          - 'js'
          - 'pdf'
          - 'php'
          - 'png'
          - 'ttf'
          - 'txt'
          - 'woff2?'
        authz_file_extensions: |-
            Require local

        allowed_http_methods:
          - 'GET'
          - 'OPTIONS'
          - 'POST'

        authz_document_root: |-
            Require local

        php_set_handler: 'SetHandler "proxy:unix:/run/php-fpm/myapp.sock|fcgi://localhost"'

        AllowOverride: 'None'
        conf_custom_log: 'logs/myapp.example.com-access.log fail2ban'
        DirectoryIndex: 'index.php'
        conf_log_level: 'warn'
        Options: 'None'
        ServerAdmin: '{{ myapp__serveradmin }}'
        conf_server_name: 'myapp.example.com'
        conf_server_alias: 'othername.myapp.com'

        raw: !unsafe |-
          <Directory "{{ myapp__app_home }}/data/">
              # Just in case the .htaccess gets disabled.
              Require all denied
          </Directory>
          {% if myapp__data_path != (myapp__app_home + "/data") %}
          <Directory {{ myapp__data_path|quote }}>
              # Just in case someone changes the global Apache defaults and messed
              # with the "Alias" directive ;)
              Require all denied
          </Directory>
          {% endif %}

          # ssl_module
          SSLEngine on
          SSLCertificateFile      /etc/pki/tls/certs/localhost.pem
          SSLCertificateKeyFile   /etc/pki/tls/private/localhost.key

A simple redirect vHost:

.. code-block:: yaml

    myapp__apache_httpd__dependent_vhosts:

      - comment: |-
          Redirect to https://localhost.
        enabled: True
        filename: '000-localhost'
        state: 'present'
        type: 'redirect'
        virtualhost_ip: '*'
        virtualhost_port: 80
        conf_server_name: 'localhost'

A more sophisticated redirect vHost:

.. code-block:: yaml

    myapp__apache_httpd__dependent_vhosts:

      - comment: |-
          Redirect to https://localhost.
        enabled: True
        filename: '000-localhost'
        state: 'present'
        type: 'redirect'
        virtualhost_ip: '*'
        virtualhost_port: 80
        conf_server_name: 'localhost'
        raw: !unsafe |-
            RewriteCond %{REQUEST_URI} !^/\.well\-known/acme\-challenge/
            RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]


For example, to configure a reverse proxy, set the following in the ``host_vars``:

.. code-block:: yaml

    apache_httpd__server_type: 'reverse-proxy'
    apache_httpd__host_vhosts:

      - enabled: true
        filename: 'hello.example.com'
        state: 'present'
        type: 'proxy'

        DirectoryIndex: 'index.php'
        conf_server_name: 'hello.example.com'
        ProxyPreserveHost: 'On'

        raw: !unsafe |-
          # ssl_module
          SSLEngine on
          SSLCertificateFile      /etc/pki/tls/certs/hello.example.com.pem
          SSLCertificateKeyFile   /etc/pki/tls/private/hello.example.com.key
          SSLCACertificateFile    /etc/pki/tls/certs/rootCA.pem

          # proxy_module and other
          <Proxy *>
              Require all granted
          </Proxy>
          SSLProxyEngine On
          SSLProxyCheckPeerCN Off
          SSLProxyCheckPeerExpire On
          RewriteRule ^/(.*) https://192.0.2.157/$1 [proxy,last]
          ProxyPassReverse / https://192.0.2.157/



License
-------

The Unlicense, see `LICENSE file <https://unlicense.org/>`_.


Author Information
------------------

`Linuxfabrik GmbH, Zurich <https://www.linuxfabrik.ch>`_
