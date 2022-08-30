# Ansible Role linuxfabrik.lfops.apache_httpd

This role installs and configures a CIS-compliant [Apache httpd](https://github.com/apache/httpd).

Tested on

* RHEL 8 (and compatible)


## What this Role does

This role configures Apache in the same way as is usual on Debian systems, so quite different to upstream's suggested way to configure the web server. This is because this role attempts to make adding and removing mods, virtual hosts, and extra configuration directives as flexible as possible, in order to make automating the changes and administering the server as easy as possible.

The config is split into several files forming the configuration hierarchy outlined below, all located in the `/etc/httpd/` directory:

```
/etc/httpd/
|-- httpd.conf
|-- conf-available/
|-- conf-enabled/
|-- mods-available/
|-- mods-enabled/
`-- sites-available/
`-- sites-enabled/
```

We try to avoid using `<IfModule>` in the global Apache configuration as well as in the configuration of the vhosts as much as possible in order to facilitate debugging. Otherwise, when using `<IfModule>`, configuration options are silently dropped, and their absence is very difficult to notice.

For flexibility, use the `raw` variable to configure the following topics (have a look at the "Apache vHost Configs" section for some examples):

* SSL/TLS Certificates.
* Quality of Service (`mod_qos` directives).
* Proxy passing rules.
* Any other configuration instructions not covered in the "Role Variables" chapters.

If you want to check Apache with [our STIG audit script](https://github.com/Linuxfabrik/stig>), run it like this:

* Apache Application Server: `./audit.py --lengthy --profile-name='CIS Apache HTTP Server 2.4' --profile-version='v2.0.0' --hostname=web --control-name-exclude='2\.4|2\.6|2\.8|5\.7|6\.6|6\.7`
* Apache Reverse Proxy Server: `./audit.py --lengthy --profile-name='CIS Apache HTTP Server 2.4' --profile-version='v2.0.0' --hostname=proxy --control-name-exclude='2\.4|2\.6|2\.8|5\.7`


## What this Role doesn't do

* PHP: This role prefers the use of PHP-FPM over PHP, but it does not install either.
* SELinux: Use specialized roles to set specific SELinux Booleans, Policies etc.



## Mandatory Requirements

* On RHEL-compatible systems, enable the EPEL repository. This can be done using the [linuxfabrik.lfops.repo_epel](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_epel) role.
* Set the `conf_server_name` variable for each vHost definition. -> just best practise, we would never use a vhost without a ServerName


## Optional Requirements

* Install PHP and configure PHP-FPM. This can be done using the [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role.



## Tags

| Tag      | What it does                   |
| ---      | ------------                   |
| `apache_httpd` | Installs and configures apache_httpd |
| `apache_httpd:config` | Creates or updates global Apache configuration<br>Removes conf-available configs<br>Creates conf-available configs<br>Disables configs<br>Enables configs | 
| `apache_httpd:mod_security_coreruleset` | Downloads, verifies and installs OWASP ModSecurity Core Rule Set (CRS)<br>Installs tar<br>Unarchives the CRS<br>Links the CRS | 
| `apache_httpd:mods` | Removes mods-available configs<br>Create mods-available configs<br>Disable mods<br>Enable mods | 
| `apache_httpd:state` | Ensures that httpd service is in a desired state | 
| `apache_httpd:vhosts` | Removes sites-available vHosts<br>Creates sites-available vHosts<br>Creates DocumentRoot for all vHosts<br>Disables vHosts<br>Enables vHosts | 




apache_httpd__conf__combined_var
apache_httpd__conf_add_default_charset
apache_httpd__conf_custom_log
apache_httpd__conf_directory_index
apache_httpd__conf_document_root
apache_httpd__conf_enable_send_file
apache_httpd__conf_error_log
apache_httpd__conf_hostname_lookups
apache_httpd__conf_keep_alive
apache_httpd__conf_keep_alive_timeout
apache_httpd__conf_limit_request_body
apache_httpd__conf_limit_request_field_size
apache_httpd__conf_limit_request_fields
apache_httpd__conf_limit_request_line
apache_httpd__conf_log_level
apache_httpd__conf_max_keep_alive_requests
apache_httpd__conf_mpm_event_max_connections_per_child
apache_httpd__conf_mpm_event_max_request_workers
apache_httpd__conf_mpm_event_max_spare_threads
apache_httpd__conf_mpm_event_min_spare_threads
apache_httpd__conf_mpm_event_start_servers
apache_httpd__conf_mpm_event_thread_limit
apache_httpd__conf_mpm_event_threads_per_child
apache_httpd__conf_mpm_prefork_max_connections_per_child
apache_httpd__conf_mpm_prefork_max_request_workers
apache_httpd__conf_mpm_prefork_max_spare_servers
apache_httpd__conf_mpm_prefork_min_spare_servers
apache_httpd__conf_mpm_prefork_start_servers
apache_httpd__conf_mpm_worker_max_connections_per_child
apache_httpd__conf_mpm_worker_max_request_workers
apache_httpd__conf_mpm_worker_max_spare_threads
apache_httpd__conf_mpm_worker_min_spare_threads
apache_httpd__conf_mpm_worker_start_servers
apache_httpd__conf_mpm_worker_thread_limit
apache_httpd__conf_mpm_worker_threads_per_child
apache_httpd__conf_server_admin
apache_httpd__conf_server_name
apache_httpd__conf_timeout
apache_httpd__conf_trace_enable
apache_httpd__mod_security_coreruleset_checksum
apache_httpd__mod_security_coreruleset_url
apache_httpd__mod_security_coreruleset_version
apache_httpd__mods__combined_var
apache_httpd__packages__combined_var
apache_httpd__systemd_enabled
apache_httpd__systemd_state
apache_httpd__vhosts__combined_var


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `apache_httpd__denied_peer_ip` | List of IP address ranges which never be used as peer IPs. This should be used to prevent the apache_httpd server from accessing private IPs. Given the turn server is likely behind your firewall, remember to include any privileged public IPs too. |
| `apache_httpd__realm` | The default realm to be used for the users. Hint: Should be the domain of the apache_httpd server for the usage with Nextcloud. |
| `apache_httpd__static_auth_secret` | Static authentication secret value (a string) for TURN REST API only. |


Example:
```yaml
# mandatory
apache_httpd__denied_peer_ip:
  - '192.0.2.0-192.0.255.255'
apache_httpd__realm: 'turn.example.com'
apache_httpd__static_auth_secret: 'egi7eesa9eik4kae9ov9quohpheequ9XighaivobuThoo7ooKuo3aikooNuy9edei4fu3jaikeepai4j'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `apache_httpd__allowed_peer_ip` | List of IP address ranges which are excepted from `apache_httpd__denied_peer_ip`. | `['{{ ansible_facts["default_ipv4"]["address"] }}']` |
| `apache_httpd__listening_port` | TURN listener port for UDP and TCP listeners | `3478` |
| `apache_httpd__max_port` | Upper bound of the UDP port range for relay endpoints allocation. | `65535` |
| `apache_httpd__min_port` | Lower bound of the UDP port range for relay endpoints allocation. | `49152` |
| `apache_httpd__service_enabled` | Enables or disables the apache_httpd service, analogous to `systemctl enable/disable --now`. Possible options: | `true` |
| `apache_httpd__state_nonce` | Use extra security with nonce value having limited lifetime, in seconds. Set it to 0 for unlimited nonce lifetime. | `0` |

Example:
```yaml
# optional
apache_httpd__allowed_peer_ip:
  - '{{ ansible_facts["default_ipv4"]["address"] }}'
apache_httpd__listening_port: 3478
apache_httpd__max_port: 65535
apache_httpd__min_port: 49152
apache_httpd__service_enabled: true
apache_httpd__state_nonce: 0
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
