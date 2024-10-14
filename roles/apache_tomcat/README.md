# Ansible Role linuxfabrik.lfops.apache_tomcat

This role installs and configures an instance of [Apache Tomcat](https://tomcat.apache.org/). The role uses the operating system's package manager, so EPEL is a must on RHEL. Log rotation in Tomcat is disabled and is done by logrotated. This role currently supports Tomcat v9.

Optionally this role also installs:

* the Manager Web GUIs (default: install). When installed, the Manager Web GUIs are available at

    * http://tomcat:8080/host-manager/html: Admin Interface (Virtual Host Manager)
    * http://tomcat:8080/manager/html: Web Application Manager
    * http://tomcat:8080/manager/status: Server Status

* the home page ("ROOT" web application; default: install). When installed, it is accessible at http://tomcat:8080/.

Notes:

* On RHEL 8 and compatible, it installs Tomcat 9.0.65+ and Java 1.8.0+
* On RHEL 9 and compatible, it installs Tomcat 9.0.87+ and OpenJDK 11.0.24+ (LTS)
* If activating AJP, this role currently sets `secretRequired` to `false`.


## Multiple Tomcat Instances

How to deploy multiple Tomcat instances on a single server using this and other roles? Imagine you want to run an 'author' and a 'public' instance. Place your config files in `host_files` (for example `host_files/{{ inventory_hostname }}/var/lib/tomcats/{author,public}/conf/{context,server}.xml` and deploy like this:

```yaml

files__directories__host_var:
  - path: '/var/lib/tomcats/author/conf'
    owner: 'tomcat'
    group: 'tomcat'
  - path: '/var/lib/tomcats/author/lib'
    owner: 'tomcat'
    group: 'tomcat'
  - path: '/var/lib/tomcats/author/logs'
    owner: 'tomcat'
    group: 'tomcat'
  - path: '/var/lib/tomcats/author/webapps'
    owner: 'tomcat'
    group: 'tomcat'
  - path: '/var/lib/tomcats/author/work'
    owner: 'tomcat'
    group: 'tomcat'
  - path: '/var/lib/tomcats/public/conf'
    owner: 'tomcat'
    group: 'tomcat'
  - path: '/var/lib/tomcats/public/lib'
    owner: 'tomcat'
    group: 'tomcat'
  - path: '/var/lib/tomcats/public/logs'
    owner: 'tomcat'
    group: 'tomcat'
  - path: '/var/lib/tomcats/public/webapps'
    owner: 'tomcat'
    group: 'tomcat'
  - path: '/var/lib/tomcats/public/work'
    owner: 'tomcat'
    group: 'tomcat'
files__files__host_var:
  - path: '/var/lib/tomcats/author/conf/context.xml'
  - path: '/var/lib/tomcats/author/conf/server.xml'
  - path: '/var/lib/tomcats/public/conf/context.xml'
  - path: '/var/lib/tomcats/public/conf/server.xml'

shell__commands__host_var:
  - name: '100-prepare-tomcat-instances'
    commands: |
      cp --archive --no-clobber /etc/tomcat/* /var/lib/tomcats/author/conf/
      cp --archive --no-clobber /etc/tomcat/* /var/lib/tomcats/public/conf/
      restorecon -Fvr /var/lib/tomcats
      chown -R tomcat:tomcat /var/lib/tomcats
    creates: '/var/lib/tomcats/author/conf/server.xml'
  - name: '110-enable-tomcat-services'
    commands: |
      systemctl enable --now tomcat@author.service
      systemctl enable --now tomcat@public.service
```

If you are running multiple instances, and there is no need for the main `tomcat.service`, you can simply disable it:

```yaml
# we only run sub-tomcat's
apache_tomcat__service_enabled: false
apache_tomcat__service_state: 'stopped'
```

The deployment:

```bash
ansible-playbook --inventory=myinv linuxfabrik.lfops.apache_tomcat
ansible-playbook --inventory=myinv linuxfabrik.lfops.files
ansible-playbook --inventory=myinv linuxfabrik.lfops.shell
```


## Mandatory Requirements

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Set SELinux Booleans and Policies properly. This can be done using the [linuxfabrik.lfops.selinux](https://github.com/Linuxfabrik/lfops/tree/main/roles/selinux) role.

If you use the [Apache Tomcat Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/apache_tomcat.yml), this is automatically done for you.


## Tags

| Tag                       | What it does                                   |
| ---                       | ------------                                   |
| `apache_tomcat`           | Install tomcat and optional default web apps, configure Tomcat (`server.xml` and others), configure logrotating, configure access to optional web apps, create users and roles, and enable or disable the default Tomcat service. |
| `apache_tomcat:configure` | Configure Tomcat (`server.xml` and others), configure logrotating. |
| `apache_tomcat:webapps`   | Configure access to optional web apps. |
| `apache_tomcat:users`     | Create users and roles. |
| `apache_tomcat:state`     | Enable/disable the default Tomcat service. |


## Mandatory Role Variables

Only mandatory if installing the Manager Web GUI and/or the ROOT webapp.

Note that for Tomcat 7 onwards, the roles required to use the manager application were changed from the single `manager` role to the following four roles. You will need to assign the role(s) required for the functionality you wish to access:

* `manager-gui`: Allows access to the HTML GUI and the status pages.
* `manager-script`: Allows access to the text interface and the status pages.
* `manager-jmx`: Allows access to the JMX proxy and the status pages.
* `manager-status`: Allows access to the status pages only.

The GUI is protected against CSRF, but the text and JMX interfaces are not. To maintain CSRF protection, users with the `manager-gui` role should not be given the `manager-script` or `manager-jmx` roles.

| Variable | Description |
| -------- | ----------- |
| `apache_tomcat__webapps_docs_context_xml_allow` | String. A regex that describes which IP addresses are allowed to access the documentation webapp. |
| `apache_tomcat__webapps_manager_context_xml_allow` | String. A regex that describes which IP addresses are allowed to access the [manager and host-manager](https://tomcat.apache.org/tomcat-9.0-doc/manager-howto.html) webapps. |
| `apache_tomcat__users__host_var` / <br> `apache_tomcat__users__group_var`  | List of dictionaries. Users allowed to access the Manager Web GUI. Subkeys: <ul><li>`password`: Mandatory, string.</li><li>`roles`: Mandatory, list. Any of `admin`, `admin-gui`, `admin-script`, `manager`, `manager-gui`, `manager-script`, `manager-jmx`, `manager-status` </li><li>`state`: Optional, string. Either `present` or `absent`.</li><li>`username`: Mandatory, string.</li></ul> |

Example:
```yaml
# only mandatory if installing the Manager Web GUI and/or the ROOT webapp
apache_tomcat__users__host_var:
  - username: 'tomcat-admin'
    password: 'linuxfabrik'
    roles:
      - 'admin-gui'
      - 'manager-gui'
    state: 'present'
apache_tomcat__webapps_docs_context_xml_allow: '|192\.2\.0\.\d+|10\.80\.32\.\d+'
apache_tomcat__webapps_manager_context_xml_allow: '|192\.2\.0\.\d+|10\.80\.32\.\d+'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apache_tomcat__webapps_manager_web_xml_max_file_size` | Number. [Manager App](https://tomcat.apache.org/tomcat-9.0-doc/manager-howto.html). File size limit for WAR file uploads in bytes. Defaults to 50MB. | `52428800`
| `apache_tomcat__webapps_manager_web_xml_max_request_size` | Number. [Manager App](https://tomcat.apache.org/tomcat-9.0-doc/manager-howto.html). Request limit in bytes. Defaults to 50MB. | `52428800`
| `apache_tomcat__context_xml_cache_max_size` | Number. The maximum size of the static resource cache in kilobytes. If not specified, the default value is `10240` (10 megabytes). This value may be changed while the web application is running (e.g. via JMX). If the cache is using more memory than the new limit the cache will attempt to reduce in size over time to meet the new limit. If necessary, cacheObjectMaxSize will be reduced to ensure that it is no larger than `cacheMaxSize/20`. [Doc](https://tomcat.apache.org/tomcat-9.0-doc/config/resources.html) | `102400` |
| `apache_tomcat__env_xms` | Number. `CATALINA_OPTS=-Xms`. Specifies the initial heap size. | `'1024M'` |
| `apache_tomcat__env_xmx` | Number. `CATALINA_OPTS=-Xmx`. Specifies the maximum heap size. | `'1024M'` |
| `apache_tomcat__env_xx` | For specifiying various [JVM Options](http://www.oracle.com/technetwork/articles/java/vmoptions-jsp-140102.html) after `-XX:`:<br>* Boolean options are turned on with `-XX:+` and turned off with `-XX:-`.<br> * Numeric options are set with `-XX:=`. Numbers can include `'m'` or `'M'` for megabytes, `'k'` or `'K'` for kilobytes, and `'g'` or `'G'` for gigabytes (for example, `32k` is the same as `32768`).<br> * String options are set with `-XX:=`, are usually used to specify a file, a path, or a list of commands. | `'+UseParallelGC'` |
| `apache_tomcat__logrotate` | Number. Log files are rotated `count` days before being removed or mailed to the address specified in a `logrotate` mail directive. If count is `0`, old versions are removed rather than rotated. If count is `-1`, old logs are not removed at all (use with caution, may waste performance and disk space). | `{{ logrotate__rotate \| d(14) }}` |
| `apache_tomcat__roles__host_var` / <br> `apache_tomcat__roles__group_var` | List of dictionaries. Tomcat roles to deploy. Subkeys: <ul><li>`name`: Mandatory, string. Name of the role.</li><li>`state`: Optional, string. Either `present` or `absent`.</li></ul><br> Built-in Tomcat manager roles are: <ul><li>`manager-gui`: Allows access to the HTML GUI and the status pages.</li><li>`manager-script`: Allows access to the HTTP API and the status pages.</li><li>`manager-jmx`: Allows access to the JMX proxy and the status pages.</li><li>`manager-status`: Allows access to the status pages only.</li></ul> | `['admin-gui', 'manager-gui']` |
| `apache_tomcat__server_xml_ajp_port` | Number. The TCP port number on which this Connector will create a server socket and await incoming connections. Your operating system will allow only one server application to listen to a particular port number on a particular IP address. If the special value of 0 (zero) is used, then Tomcat will select a free port at random to use for this connector. This is typically only useful in embedded and testing applications. [Doc](https://tomcat.apache.org/tomcat-9.0-doc/config/ajp.html) | unset (not listening on AJP) |
| `apache_tomcat__server_xml_connector_compression` | String. The Connector may use HTTP/1.1 GZIP compression in an attempt to save server bandwidth. The acceptable values for the parameter is "off" (disable compression), "on" (allow compression, which causes text data to be compressed), "force" (forces compression in all cases), or a numerical integer value (which is equivalent to "on", but specifies the minimum amount of data before the output is compressed). If the content-length is not known and compression is set to "on" or more aggressive, the output will also be compressed. If not specified, this attribute is set to "off".<br>Note: There is a tradeoff between using compression (saving your bandwidth) and using the sendfile feature (saving your CPU cycles). If the connector supports the sendfile feature, e.g. the NIO connector, using sendfile will take precedence over compression. The symptoms will be that static files greater that 48 Kb will be sent uncompressed. You can turn off sendfile by setting useSendfile attribute of the connector, as documented below, or change the sendfile usage threshold in the configuration of the DefaultServlet in the default conf/web.xml or in the web.xml of your web application. [Doc](https://tomcat.apache.org/tomcat-9.0-doc/config/http.html) | `'on'` |
| `apache_tomcat__server_xml_connector_connection_timeout` | The number of milliseconds this Connector will wait, after accepting a connection, for the request URI line to be presented. Use a value of `-1` to indicate no (i.e. infinite) timeout. The default value is `60000` (i.e. 60 seconds) but note that the standard `server.xml` that ships with Tomcat sets this to `20000` (i.e. 20 seconds). Unless `disableUploadTimeout` is set to `false`, this timeout will also be used when reading the request body (if any). This parameter is there specifically to fight one type of Denial-Of-Service attack, whereby some malicious client(s) create a TCP connection to the server (which has the effect of reserving some resources on the server for handling this connection), and then just sit there without sending any HTTP request on that connection. By making this delay shorter, you shorten the time during which the server resources are allocated, to serve a request that will never come. [Doc](https://tomcat.apache.org/tomcat-9.0-doc/config/http.html) | `20000` |
| `apache_tomcat__server_xml_connector_max_threads` | Number. The maximum number of request processing threads to be created by this Connector, which therefore determines the maximum number of simultaneous requests that can be handled. If not specified, this attribute is set to `200`. If an executor is associated with this connector, this attribute is ignored as the connector will execute tasks using the executor rather than an internal thread pool. Note that if an executor is configured any value set for this attribute will be recorded correctly but it will be reported (e.g. via JMX) as `-1` to make clear that it is not used. [Doc](https://tomcat.apache.org/tomcat-9.0-doc/config/http.html) | `200` |
| `apache_tomcat__server_xml_connector_min_spare_threads` | Number. The minimum number of threads always kept running. This includes both active and idle threads. If an executor is associated with this connector, this attribute is ignored as the connector will execute tasks using the executor rather than an internal thread pool. Note that if an executor is configured any value set for this attribute will be recorded correctly but it will be reported (e.g. via JMX) as `-1` to make clear that it is not used. [Doc](https://tomcat.apache.org/tomcat-9.0-doc/config/http.html) | `10` |
| `apache_tomcat__server_xml_connector_port` | The TCP port number on which this Connector will create a server socket and await incoming connections. Your operating system will allow only one server application to listen to a particular port number on a particular IP address. If the special value of `0` (zero) is used, then Tomcat will select a free port at random to use for this connector. This is typically only useful in embedded and testing applications. [Doc](https://tomcat.apache.org/tomcat-9.0-doc/config/http.html) | `8080` |
| `apache_tomcat__server_xml_shutdown_port` | | `8005` |
| `apache_tomcat__service_enabled` | Bool. Enables or disables the service, analogous to `systemctl enable/disable --now`. | `true` |
| `apache_tomcat__service_state` | String. Changes the state of the service, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `reloaded`<br> * `restarted`<br> * `started`<br> * `stopped` | `'started'` |
| `apache_tomcat__skip_admin_webapps` | Bool. If set to `true`, installation of the Manager Web GUIs will be skipped. | `false` |
| `apache_tomcat__skip_root_webapp` | Bool. If set to `true`, installation of the ROOT webapp (the tomcat startpage) will be skipped. | `false` |
| `apache_tomcat__webapps_manager_web_xml_max_file_size` | Number. [Manager App](https://tomcat.apache.org/tomcat-9.0-doc/manager-howto.html). File size limit for WAR file uploads in bytes. Defaults to 50MB. | `52428800`
| `apache_tomcat__webapps_manager_web_xml_max_request_size` | Number. [Manager App](https://tomcat.apache.org/tomcat-9.0-doc/manager-howto.html). Request limit in bytes. Defaults to 50MB. | `52428800`

Example:
```yaml
# optional
apache_tomcat__webapps_manager_web_xml_max_file_size: 209715200
apache_tomcat__webapps_manager_web_xml_max_request_size: 209715200
apache_tomcat__context_xml_cache_max_size: 102400
apache_tomcat__env_xms: '1024M'
apache_tomcat__env_xmx: '1024M'
apache_tomcat__env_xx: '+UseParallelGC'
apache_tomcat__logrotate: 7
apache_tomcat__roles__host_var:
  - name: 'admin-gui'
    state: 'present'
  - name: 'manager-gui'
    state: 'absent'
apache_tomcat__server_xml_ajp_port: 8009
apache_tomcat__server_xml_connector_compressable_mime_types: 'text/html,text/xml,text/plain'
apache_tomcat__server_xml_connector_compression: 'on'
apache_tomcat__server_xml_connector_connection_timeout: 60000
apache_tomcat__server_xml_connector_max_threads: 200
apache_tomcat__server_xml_connector_min_spare_threads: 10
apache_tomcat__server_xml_connector_port: 8080
apache_tomcat__server_xml_shutdown_port: 8005
apache_tomcat__service_enabled: true
apache_tomcat__service_state: 'started'
apache_tomcat__skip_admin_webapps: false
apache_tomcat__skip_root_webapp: false
```


## Troubleshooting

```
WARN org.hibernate.engine.jdbc.internal.JdbcServicesImpl:169 - HHH000342: Could not obtain connection to query metadata : Cannot create PoolableConnectionFactory (Communications link failure`
The last packet sent successfully to the server was 0 milliseconds ago. The driver has not received any packets from the server.
Caused by: org.hibernate.HibernateException: Connection cannot be null when 'hibernate.dialect' not set
```
* `chown -R root:tomcat /var/lib/tomcat/webapps/`?
* Database Credentials correct?
* Connection string correct? Example: `jdbc:mysql://localhost/linuxfabrik?createDatabaseIfNotExist=true&useEncoding=true&characterEncoding=UTF-8`
* SELinux Boolean for Tomcat set? `setsebool tomcat_can_network_connect_db on`


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
