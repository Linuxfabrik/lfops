# Ansible Role linuxfabrik.lfops.collabora_code

This role installs and configures [Collabora Online Development Edition](https://www.collaboraoffice.com/code/).

Tested on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Enable the official [Collabora CODE Repository](https://docs.fedoraproject.org/en-US/collabora_code/). This can be done using the [linuxfabrik.lfops.repo_collabora_code](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_collabora_code) role.


## Tags

| Tag              | What it does                           |
| ---              | ------------                           |
| `collabora_code` | Installs and configures Collabora CODE |


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `collabora_code__coolwsd_allowed_languages` | List of supported languages of Writing Aids (spell checker, grammar checker, thesaurus, hyphenation) on this instance. Allowing too many has negative effect on startup performance. |
| `collabora_code__coolwsd_experimental_features` | If experimental features should be enabled or not. | `false` |
| `collabora_code__coolwsd_logging_file_enable` | If coolwsd should write to a logfile or not. Possible options: | `true` |
| `collabora_code__coolwsd_out_of_focus_timeout_secs` | The maximum number of seconds before dimming and stopping updates when the browser tab is no longer in focus. | `120` |
| `collabora_code__coolwsd_post_allow` | List of client IP addresses to allow for POST(REST). | `[]` |
| `collabora_code__coolwsd_ssl_enable` | Controls whether SSL encryption between coolwsd and the network is enabled (do not disable for production deployment). Possible options: | `false` |
| `collabora_code__coolwsd_ssl_settings_ca_file_path` | Path to the ca file. Set this when coolwsd is SSL-terminating. | `'/etc/loolwsd/ca-chain.cert.pem'` |
| `collabora_code__coolwsd_ssl_settings_cert_file_path` | Path to the cert file. Set this when coolwsd is SSL-terminating. | `'/etc/loolwsd/cert.pem'` |
| `collabora_code__coolwsd_ssl_settings_key_file_path` | Path to the key file. Set this when coolwsd is SSL-terminating. | `'/etc/loolwsd/key.pem'` |
| `collabora_code__coolwsd_ssl_termination` | Enable if coolwsd is behind a SSL-terminating proxy and therefore should act as if its using https but actually receives http. Possible options: | `true` |
| `collabora_code__group_coolwsd_storage_wopi` | List of regex pattern of hostname to allow access to the backend storage. Ususally the hostname application that uses Collabora CODE, for example Nextcloud. <br>For the usage in `group_vars` (can only be used in one group at a time). | `[]` |
| `collabora_code__host_coolwsd_storage_wopi` | List of regex pattern of hostname to allow access to the backend storage. Ususally the hostname application that uses Collabora CODE, for example Nextcloud. <br>For the usage in `host_vars`. | `[]` |
| `collabora_code__group_language_packages` | A list of additional packages will be installed for language support (spell checking, thesaurus, etc). Defaults to de, en, fr, and it. <br>For the usage in `group_vars` (can only be used in one group at a time). | `[]` |
| `collabora_code__host_language_packages` | A list of additional packages will be installed for language support (spell checking, thesaurus, etc). Defaults to de, en, fr, and it. <br>For the usage in `host_vars`. | `[]` |
| `collabora_code__service_enabled` | Enables or disables the coolwsd service, analogous to `systemctl enable/disable --now`. Possible options: | `true` |

Example:
```yaml
# optional
collabora_code__coolwsd_allowed_languages:
  - 'de_AT'
  - 'de_CH'
  - 'de_DE'
  - 'en_AU'
  - 'en_CA'
  - 'en_GB'
  - 'en_US'
  - 'fr'
  - 'it_IT'
collabora_code__coolwsd_experimental_features: false
collabora_code__coolwsd_logging_file_enable: true
collabora_code__coolwsd_out_of_focus_timeout_secs: 120
collabora_code__coolwsd_post_allow: []
collabora_code__coolwsd_ssl_enable: false
collabora_code__coolwsd_ssl_settings_ca_file_path: '/etc/loolwsd/ca-chain.cert.pem'
collabora_code__coolwsd_ssl_settings_cert_file_path: '/etc/loolwsd/cert.pem'
collabora_code__coolwsd_ssl_settings_key_file_path: '/etc/loolwsd/key.pem'
collabora_code__coolwsd_ssl_termination: true
collabora_code__group_coolwsd_storage_wopi: []
collabora_code__host_coolwsd_storage_wopi:
  - 'cloud\.example\.com'
collabora_code__group_language_packages: []
collabora_code__host_language_packages: []
collabora_code__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
