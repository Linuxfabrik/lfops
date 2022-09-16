# Ansible Role linuxfabrik.lfops.apache_tomcat

This role installs and configures [Apache Tomcat](https://tomcat.apache.org/) - not via the operating system's package manager, but by downloading the specified version directly from [https://tomcat.apache.org](https://tomcat.apache.org).

Tested on

* RHEL 7 (and compatible)
* RHEL 8 (and compatible)


## Mandatory Requirements

* Install `java.` This can be done using the [linuxfabrik.lfops.java](https://github.com/Linuxfabrik/lfops/tree/main/roles/java) role. If you use the  [Apache Tomcat Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/apache_tomcat.yml), this is automatically done for you.


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

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apache_tomcat__catalina_opts`| todo | `'-Xms512M -Xmx1024M -server -XX:+UseParallelGC'` |
| `apache_tomcat__install_dir`| The directory in which the Tomcat instances will be installed as subfolders. | `'/opt'` |
| `apache_tomcat__instances`| A dictionary of todo | `todo` |
| `apache_tomcat__logrotate_rotate`| The number of days the logfiles should be kept by logrotate. | `14` |
| `apache_tomcat__roles__group_var` / `apache_tomcat__roles__host_var`| todo | `[]` |
| `apache_tomcat__server_xml_use_remote_ip_valve`| todo | `false` |
| `apache_tomcat__service_enabled`| Enables or disables all Tomcat services, analogous to `systemctl enable/disable`. | `true` |
| `apache_tomcat__service_state`| Changes the state of all Tomcat services, analogous to `systemctl start/stop/restart/reload`. Possible options:<br> * `started`<br> * `stopped`<br> * `restarted`<br> * `reloaded` | `'started'` |
| `apache_tomcat__users__group_var` / `apache_tomcat__users__host_var| todo | `[]` |

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

apache_tomcat__logrotate_rotate: 14
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
