# Ansible Role collabora_code

This role installs and configures [Collabora Online Development Edition](https://www.collaboraoffice.com/code/).

FQCN: linuxfabrik.lfops.collabora_code

Tested on

* RHEL 8 (and compatible)


## Requirements

### Mandatory

* Enable the official [Collabora CODE Repository](https://docs.fedoraproject.org/en-US/collabora_code/). This can be done using the [linuxfabrik.lfops.repo_collabora_code](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_collabora_code) role.


### Optional

This role does not have any optional requirements.


## Tags

| Tag            | What it does                           |
| ---            | ------------                           |
| collabora_code | Installs and configures Collabora CODE |


## Role Variables

Have a look at the [defaults/main.yml](https://github.com/Linuxfabrik/lfops/blob/main/roles/collabora_code/defaults/main.yml) for the variable defaults.


### Mandatory

This role does not have any mandatory variables.


### Optional

#### collabora_code__coolwsd_ssl_enable

Controls whether SSL encryption between coolwsd and the network is enabled (do not disable for production deployment). Possible options:

* false
* true

Default:
```yaml
collabora_code__coolwsd_ssl_enable: false
```


#### collabora_code__coolwsd_ssl_termination

Enable if coolwsd is behind a SSL-terminating proxy and therefore should act as if its using https but actually receives http. Possible options:

* false
* true

Default:
```yaml
collabora_code__coolwsd_ssl_termination: true
```


#### collabora_code__coolwsd_allowed_languages

List of supported languages of Writing Aids (spell checker, grammar checker, thesaurus, hyphenation) on this instance. Allowing too many has negative effect on startup performance.

Default:
```yaml
collabora_code__coolwsd_allowed_languages:
  - 'de_AT'
  - 'de_CH'
  - 'de_DE'
  - 'el_GR'
  - 'en_AU'
  - 'en_CA'
  - 'en_GB'
  - 'en_US'
  - 'es_ANY'
  - 'fr'
  - 'it_IT'
```


#### collabora_code__coolwsd_logging_file_enable

If coolwsd should write to a logfile or not. Possible options:

* false
* true


Default:
```yaml
collabora_code__coolwsd_logging_file_enable: true
```


#### collabora_code__coolwsd_out_of_focus_timeout_secs

The maximum number of seconds before dimming and stopping updates when the browser tab is no longer in focus.

Default:
```yaml
collabora_code__coolwsd_out_of_focus_timeout_secs: 120
```


#### collabora_code__coolwsd_post_allow

todo
List of client IP addresses to allow for POST(REST).

Default:
```yaml
collabora_code__coolwsd_post_allow: []
```


#### collabora_code__coolwsd_ssl_settings_ca_file_path

Path to the ca file. Set this when coolwsd is SSL-terminating.

Default:
```yaml
collabora_code__coolwsd_ssl_settings_ca_file_path: '/etc/loolwsd/ca-chain.cert.pem'
```


#### collabora_code__coolwsd_ssl_settings_cert_file_path

Path to the cert file. Set this when coolwsd is SSL-terminating.

Default:
```yaml
collabora_code__coolwsd_ssl_settings_cert_file_path: '/etc/loolwsd/cert.pem'
```


#### collabora_code__coolwsd_ssl_settings_key_file_path

Path to the key file. Set this when coolwsd is SSL-terminating.

Default:
```yaml
collabora_code__coolwsd_ssl_settings_key_file_path: '/etc/loolwsd/key.pem'
```


#### collabora_code__host_coolwsd_storage_wopi / collabora_code__group_coolwsd_storage_wopi

These variables are intended to be used in a host / group variable file in the Ansible inventory. Note that the group variable can only be used in one group at a time.

List of regex pattern of hostname to allow access to the backend storage. Ususally the hostname application that uses Collabora CODE, for example Nextcloud.

Default:
```yaml
collabora_code__coolwsd_storage_wopi: []
```

Example:
```yaml
collabora_code__coolwsd_storage_wopi:
  - 'cloud\.example\.com'
```


#### collabora_code__service_enabled

Enables or disables the coolwsd service, analogous to `systemctl enable/disable --now`. Possible options:

* true
* false

Default:
```yaml
collabora_code__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
