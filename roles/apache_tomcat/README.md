# Ansible Role linuxfabrik.lfops.apache_tomcat

This role installs and configures one [Apache Tomcat](https://tomcat.apache.org/) instance.

It is possible to configure whether the Manager Web GUI should be installed (it is installed by default). When installed, the Manager Web GUI is accessible via http://tomcat:8080/manager/. The GUI is protected against CSRF, but the text and JMX interfaces are not. To maintain CSRF protection, users with the `manager-gui` role should not be given the `manager-script` or `manager-jmx` roles. The role uses the operating system's package manager, so EPEL is a must on RHEL. Logrotation in Tomcat is disabled and is done by logrotated.

Tested on

* RHEL 8 (and compatible)


## Mandatory Requirements

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.


## Tags

| Tag                       | What it does                                   |
| ---                       | ------------                                   |
| `apache_tomcat`           | Installs and configures Apache Tomcat          |
| `apache_tomcat:configure` | Configures Apache Tomcat                       |
| `apache_tomcat:state`     | Manages the state of the Apache Tomcat service |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `apache_tomcat__manager_context_allow` | A regex that regulates which IP addresses are allowed to access the manager and host-manager webapps. Use `'|.*'` to allow any. |
| `apache_tomcat__version` | The version of Apache Tomcat to install. Possible options: <https://tomcat.apache.org/whichversion.html> |

Example:
```yaml
# mandatory
apache_tomcat__manager_context_allow: '|192\.0\.2\.\d+'
apache_tomcat__version: '10.0.23'
```


## Optional Role Variables

https://tomcat.apache.org/tomcat-9.0-doc/config/http.html

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apache_tomcat__catalina_opts`| todo | `'-Xms512M -Xmx1024M -server -XX:+UseParallelGC'` |
| `apache_tomcat__install_dir`| The directory in which the Tomcat instances will be installed as subfolders. | `'/opt'` |
| `apache_tomcat__instances`| A dictionary of todo | `todo` |
| `apache_tomcat__logrotate`| Log files are rotated `count` days before being removed or mailed to the address specified in a `logrotate` mail directive. If count is `0`, old versions are removed rather than rotated. If count is `-1`, old logs are not removed at all (use with caution, may waste performance and disk space). | `{{ logrotate__rotate | d(14) }}` |
| `apache_tomcat__roles__group_var` / `apache_tomcat__roles__host_var`| todo | `[]` |
| `apache_tomcat__server_xml_use_remote_ip_valve`| todo | `false` |
| `apache_tomcat__service_enabled`| Enables or disables all Tomcat services, analogous to `systemctl enable/disable`. | `true` |
| `apache_tomcat__service_state`| Changes the state of all Tomcat services, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |
| `apache_tomcat__users__group_var` / `apache_tomcat__users__host_var| Currently, this role can't delete users. | `[]` |

Example:
```yaml
# optional
apache_tomcat__catalina_opts: '-Xms512M -Xmx1024M -server -XX:+UseParallelGC'
apache_tomcat__install_dir: '/opt'
apache_tomcat__instances:
  tomcat:
    connector_port: 8080 # default
    shutdown_port: 8005 # default
    ajp_port: 8009 # default
    tomcat_context_xml_cache_max_size: 10240 # default unset
    tomcat_server_xml_max_threads: '{{ ansible_facts["processor_vcpus"] * 250 }}' # default
    tomcat_server_xml_auto_deploy: true # default TODO
    tomcat_server_xml_deploy_on_startup: true # default TODO
    tomcat_server_xml_unpack_wars: true # default TODO
    tomcat_server_xml_context: # default unset
      - path: '/jolokia' # A context path must either be an empty string or start with a '/' and not end with a '/'. required
        doc_base: 'jolokia' # required
        additional_properties: '' # default ''
        raw: '' # default ''

      - path: '/manager'
        doc_base: 'manager'
        additional_properties: 'antiResourceLocking="false" privileged="true"'
        raw: |-
          <Valve className="org.apache.catalina.valves.RemoteAddrValve"
                allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1{{ apache_tomcat__manager_context_allow }}"/>
          <Manager sessionAttributeValueClassNameFilter="java\.lang\.(?:Boolean|Integer|Long|Number|String)|org\.apache\.catalina\.filters\.CsrfPreventionFilter\$LruCache(?:\$1)?|java\.util\.(?:Linked)?HashMap"/>
apache_tomcat__logrotate: 7
apache_tomcat__roles__group_var: []
apache_tomcat__roles__host_var:
  - name: 'my-role'
    state: 'present'
apache_tomcat__server_xml_use_remote_ip_valve: false
apache_tomcat__service_enabled: true
apache_tomcat__service_state: 'started'
apache_tomcat__users__group_var: []
apache_tomcat__users__host_var:
  - username: 'admin'
    password: 'linuxfabrik'
    roles:
      - 'admin-gui'
      - 'manager-gui'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
