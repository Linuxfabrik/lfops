# Ansible Role linuxfabrik.lfops.collabora

This role installs and configures either [Collabora Online Development Edition](https://www.collaboraoffice.com/code/) or [Collabora Online Enterprise Edition](https://www.collaboraoffice.com/collabora-online-3/). Note: To use Collabora Enterprise, you need an active [Collabora Subscription](https://www.collaboraoffice.com/subscriptions-2/).

If you skip the repo for Collabora (`collabora__skip_repo_collabora: true`), Collabora CODE is used. If you skip the repo for Collabora CODE (`collabora__skip_repo_collabora_code: true`), Collabora Enterprise Edition is used.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Enable either the official [Collabora CODE Repository](https://docs.fedoraproject.org/en-US/collabora_code/) or your Collabora Enterprise Repository. This can be done using the [linuxfabrik.lfops.repo_collabora_code](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_collabora_code) role.

If you use the ["Collabora" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/collabora.yml), this is automatically done for you.

## Tags

| Tag              | What it does                           |
| ---              | ------------                           |
| `collabora` | Installs and configures either Collabora CODE or Collabora Enterprise |
| `collabora:spell_check` | Installs spell checking tools |

## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `collabora__coolwsd_allowed_languages` | List of supported languages of Writing Aids (spell checker, grammar checker, thesaurus, hyphenation) on this instance. Allowing too many has negative effect on startup performance. |
| `collabora__coolwsd_experimental_features` | If experimental features should be enabled or not. | `false` |
| `collabora__coolwsd_logging_file_enable` | If coolwsd should write to a logfile or not. Possible options: | `true` |
| `collabora__coolwsd_out_of_focus_timeout_secs` | The maximum number of seconds before dimming and stopping updates when the browser tab is no longer in focus. | `120` |
| `collabora__coolwsd_post_allow` | List of client IP addresses to allow for POST(REST). | `[]` |
| `collabora__coolwsd_ssl_enable` | Controls whether SSL encryption between coolwsd and the network is enabled (do not disable for production deployment). Possible options: | `false` |
| `collabora__coolwsd_ssl_settings_ca_file_path` | Path to the ca file. Set this when coolwsd is SSL-terminating. | `'/etc/loolwsd/ca-chain.cert.pem'` |
| `collabora__coolwsd_ssl_settings_cert_file_path` | Path to the cert file. Set this when coolwsd is SSL-terminating. | `'/etc/loolwsd/cert.pem'` |
| `collabora__coolwsd_ssl_settings_key_file_path` | Path to the key file. Set this when coolwsd is SSL-terminating. | `'/etc/loolwsd/key.pem'` |
| `collabora__coolwsd_ssl_termination` | Enable if coolwsd is behind a SSL-terminating proxy and therefore should act as if its using https but actually receives http. Possible options: | `true` |
| `collabora__coolwsd_storage_wopi__group_var` | List of regex pattern of hostname to allow access to the backend storage. Ususally the hostname application that uses Collabora CODE, for example Nextcloud. <br>For the usage in `group_vars` (can only be used in one group at a time). | `[]` |
| `collabora__coolwsd_storage_wopi__host_var` | List of regex pattern of hostname to allow access to the backend storage. Ususally the hostname application that uses Collabora CODE, for example Nextcloud. <br>For the usage in `host_vars`. | `[]` |
| `collabora__language_packages__group_var` | A list of additional packages will be installed for language support (spell checking, thesaurus, etc). Defaults to de, en, fr, and it. <br>For the usage in `group_vars` (can only be used in one group at a time). | `[]` |
| `collabora__language_packages__host_var` | A list of additional packages will be installed for language support (spell checking, thesaurus, etc). Defaults to de, en, fr, and it. <br>For the usage in `host_vars`. | `[]` |
| `collabora__logrotate` | Number. Log files are rotated `count` days before being removed or mailed to the address specified in a `logrotate` mail directive. If count is `0`, old versions are removed rather than rotated. If count is `-1`, old logs are not removed at all (use with caution, may waste performance and disk space). | `{{ logrotate__rotate | d(14) }}` |
| `collabora__service_enabled` | Enables or disables the coolwsd service, analogous to `systemctl enable/disable --now`. Possible options: | `true` |

Example:
```yaml
# optional
collabora__coolwsd_allowed_languages:
  - 'de_AT'
  - 'de_CH'
  - 'de_DE'
  - 'en_AU'
  - 'en_CA'
  - 'en_GB'
  - 'en_US'
  - 'fr'
  - 'it_IT'
collabora__coolwsd_experimental_features: false
collabora__coolwsd_logging_file_enable: true
collabora__coolwsd_out_of_focus_timeout_secs: 120
collabora__coolwsd_post_allow: []
collabora__coolwsd_ssl_enable: false
collabora__coolwsd_ssl_settings_ca_file_path: '/etc/loolwsd/ca-chain.cert.pem'
collabora__coolwsd_ssl_settings_cert_file_path: '/etc/loolwsd/cert.pem'
collabora__coolwsd_ssl_settings_key_file_path: '/etc/loolwsd/key.pem'
collabora__coolwsd_ssl_termination: true
collabora__coolwsd_storage_wopi__group_var: []
collabora__coolwsd_storage_wopi__host_var:
  - 'cloud\.example\.com'
collabora__language_packages__group_var: []
collabora__language_packages__host_var: []
collabora__logrotate: 7
collabora__service_enabled: true
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
