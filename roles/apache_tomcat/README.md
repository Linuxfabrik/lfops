# Ansible Role linuxfabrik.lfops.apache_tomcat

TODO: finish this README

This role installs and configures [Apache Tomcat](https://tomcat.apache.org/).

Tested on

* RHEL 7 (and compatible)


## Mandatory Requirements

* Install `java.` This can be done using the [linuxfabrik.lfops.java](https://github.com/Linuxfabrik/lfops/tree/main/roles/java) role.


## Tags

| Tag                       | What it does                                   |
| ---                       | ------------                                   |
| `apache_tomcat`           | Installs and configures Apache Tomcat          |
| `apache_tomcat:configure` | Configures Apache Tomcat                       |
| `apache_tomcat:state`     | Manages the state of the Apache Tomcat service |


## Mandatory Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |

Example:
```yaml
# mandatory
apache_tomcat__manager_context_allow: '|.*' # regex. this allows any. for host-manager and manager webapp access
apache_tomcat__version: '10.0.23' # https://tomcat.apache.org/whichversion.html
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |

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
apache_tomcat__roles__group_var: {}
apache_tomcat__roles__host_var:
  admin-gui:
    state: 'absent' # overwrite the default
  my-role:
    state: 'present'
apache_tomcat__server_xml_use_remote_ip_valve: false
apache_tomcat__service_enabled: true
apache_tomcat__service_state: 'started'
apache_tomcat__users__group_var: {}
apache_tomcat__users__host_var:
  admin:
    password: 'password'
    roles:
      - 'admin-gui'
      - 'manager-gui'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
