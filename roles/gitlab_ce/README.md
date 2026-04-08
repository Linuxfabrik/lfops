# Ansible Role linuxfabrik.lfops.gitlab_ce

This role installs and configures [GitLab CE](https://about.gitlab.com/), including regular backups.

* After installation, the password for the first user "root" can be found in `/etc/gitlab/initial_root_password`.
* One of the first steps after that would be to deactivate the registration form: In the left sidebar, select Admin > Settings > General, and expand "Sign-up restrictions". Clear the "Sign-up enabled" checkbox, then select "Save changes" (you can't disable signups without using the UI).


## Mandatory Requirements

* Enable the official GitLab CE Repository. This can be done using the [linuxfabrik.lfops.repo_gitlab_ce](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_gitlab_ce) role.

If you use the [gitlab_ce Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/gitlab_ce.yml), this is automatically done for you.


## Tags

`gitlab_ce`

* `install tar gitlab-ce`
* `mkdir -p /backup/gitlab`
* Deploy `/etc/systemd/system/gitlab-dump.service`
* Deploy `/etc/systemd/system/gitlab-dump.timer`
* `systemctl enable gitlab-dump.timer --now`
* Deploy `/etc/gitlab/gitlab.rb`
* `gitlab-ctl reconfigure`
* `gitlab-ctl restart`
* Triggers: `gitlab-ctl restart`.

`gitlab_ce:configure`

* Same as above, but without install.
* Triggers: `gitlab-ctl restart`.


## Mandatory Role Variables

`gitlab_ce__rb_external_url`

* The URL of your GitLab instance. Currently, only `http://` is supported by this role. If running behind a reverse proxy or on a trusted network, this is good enough.
* Type: String.
* Default: none

Example:
```yaml
# mandatory
gitlab_ce__rb_external_url: 'http://git.example.com'
```


## Optional Role Variables

`gitlab_ce__on_calendar`

* The `OnCalendar` definition for the GitLab Backup. Have a look at `man systemd.time(7)` for the format.
* Type: String.
* Default: `'*-*-* 23:{{ 59 | random(seed=inventory_hostname) }}'`

`gitlab_ce__rb_git_data_dirs_default_path`

* For setting up different data storing directory. If missing, the directory will be created by GitLab. If you want to use a single non-default directory to store git data use a path that doesn't contain symlinks. [Docs](https://docs.gitlab.com/omnibus/settings/configuration.html#store-git-data-in-an-alternative-directory)
* Type: String.
* Default: unset

`gitlab_ce__rb_gitlab_rails_backup_keep_time`

* The duration in seconds to keep backups before they are allowed to be deleted.
* Type: Number.
* Default: `86400`

`gitlab_ce__rb_gitlab_rails_backup_path`

* Backup Settings. [Docs](https://docs.gitlab.com/omnibus/settings/backups.html)
* Type: String.
* Default: `'/backup/gitlab'`

`gitlab_ce__rb_gitlab_rails_extra_matomo_site_id`

* Extra customization for Matomo.
* Type: String.
* Default: unset

`gitlab_ce__rb_gitlab_rails_extra_matomo_url`

* Extra customization for Matomo.
* Type: String.
* Default: unset

`gitlab_ce__rb_gitlab_rails_gitlab_default_projects_features_builds`

* Whether builds are enabled by default for projects.
* Type: Bool.
* Default: `true`

`gitlab_ce__rb_gitlab_rails_gitlab_default_projects_features_container_registry`

* Whether the container registry is enabled by default for projects.
* Type: Bool.
* Default: `true`

`gitlab_ce__rb_gitlab_rails_gitlab_default_projects_features_issues`

* Whether issues are enabled by default for projects.
* Type: Bool.
* Default: `true`

`gitlab_ce__rb_gitlab_rails_gitlab_default_projects_features_merge_requests`

* Whether merge requests are enabled by default for projects.
* Type: Bool.
* Default: `true`

`gitlab_ce__rb_gitlab_rails_gitlab_default_projects_features_snippets`

* Whether snippets are enabled by default for projects.
* Type: Bool.
* Default: `true`

`gitlab_ce__rb_gitlab_rails_gitlab_default_projects_features_wiki`

* Whether the wiki feature is enabled by default for projects.
* Type: Bool.
* Default: `true`

`gitlab_ce__rb_gitlab_rails_gitlab_email_display_name`

* The display name used in GitLab emails.
* Type: String.
* Default: `'GitLab@{{ inventory_hostname }}'`

`gitlab_ce__rb_gitlab_rails_gitlab_email_from`

* If your SMTP server does not like the default 'From: gitlab@gitlab.example.com', you can change the 'From' with this setting.
* Type: String.
* Default: `'{{ mailto_root__from | d("") }}'`

`gitlab_ce__rb_gitlab_rails_gitlab_email_reply_to`

* The 'Reply To' address for emails if it differs from the 'From' address.
* Type: String.
* Default: unset

`gitlab_ce__rb_gitlab_rails_ldap_enabled`

* Whether the LDAP integration is enabled. [Docs](https://docs.gitlab.com/administration/uploads/#using-local-storage)
* Type: Bool.
* Default: `false`

`gitlab_ce__rb_gitlab_rails_ldap_servers`

* LDAP configuration for one or more servers. [Docs](https://docs.gitlab.com/administration/auth/ldap/?tab=Self-compiled+%28source%29#configure-ldap)
* Type: Dictionary.
* Default: unset

`gitlab_ce__rb_gitlab_rails_omniauth_allow_single_sign_on`

* OmniAuth Settings. [Docs](https://docs.gitlab.com/ee/integration/omniauth.html)
* Type: List.
* Default: unset

`gitlab_ce__rb_gitlab_rails_omniauth_auto_link_ldap_user`

* OmniAuth Settings. [Docs](https://docs.gitlab.com/ee/integration/omniauth.html)
* Type: Bool.
* Default: unset

`gitlab_ce__rb_gitlab_rails_omniauth_block_auto_created_users`

* OmniAuth Settings. [Docs](https://docs.gitlab.com/ee/integration/omniauth.html)
* Type: Bool.
* Default: unset

`gitlab_ce__rb_gitlab_rails_omniauth_enabled`

* OmniAuth Settings. [Docs](https://docs.gitlab.com/ee/integration/omniauth.html)
* Type: Bool.
* Default: unset

`gitlab_ce__rb_gitlab_rails_omniauth_external_providers`

* OmniAuth Settings. [Docs](https://docs.gitlab.com/ee/integration/omniauth.html)
* Type: List.
* Default: unset

`gitlab_ce__rb_gitlab_rails_omniauth_providers`

* OmniAuth Settings. [Docs](https://docs.gitlab.com/ee/integration/omniauth.html)
* Type: List of dictionaries.
* Default: unset

`gitlab_ce__rb_gitlab_rails_rack_attack_git_basic_auth_bantime`

* Ban an IP for x seconds after too many auth attempts.
* Type: Number.
* Default: `3600`

`gitlab_ce__rb_gitlab_rails_rack_attack_git_basic_auth_enabled`

* Whether rack attack for Git basic auth is enabled.
* Type: Bool.
* Default: `true`

`gitlab_ce__rb_gitlab_rails_rack_attack_git_basic_auth_findtime`

* Reset the auth attempt counter per IP after x seconds.
* Type: Number.
* Default: `60`

`gitlab_ce__rb_gitlab_rails_rack_attack_git_basic_auth_ip_whitelist`

* List of IP addresses to whitelist from rack attack.
* Type: List.
* Default: `['127.0.0.1']`

`gitlab_ce__rb_gitlab_rails_rack_attack_git_basic_auth_maxretry`

* Limit the number of Git HTTP authentication attempts per IP.
* Type: Number.
* Default: `10`

`gitlab_ce__rb_gitlab_rails_time_zone`

* The time zone for GitLab. [Docs](https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/doc/settings/gitlab.yml.md)
* Type: String.
* Default: `'Europe/Zurich'`

`gitlab_ce__rb_gitlab_rails_uploads_directory`

* For setting up a different storage directory for uploads. If missing, the directory will be created by GitLab. [Docs](https://docs.gitlab.com/administration/uploads/#using-local-storage)
* Type: String.
* Default: `'/var/opt/gitlab/gitlab-rails/uploads'`

`gitlab_ce__rb_letsencrypt_enable`

* If GitLab should manage Let's Encrypt certificates itself.
* Type: Bool.
* Default: `false`

`gitlab_ce__rb_nginx_listen_https`

* Set this to `false` only if your reverse proxy internally communicates over HTTP. [Docs](https://docs.gitlab.com/omnibus/settings/nginx.html#supporting-proxied-ssl)
* Type: Bool.
* Default: `false`

`gitlab_ce__rb_nginx_listen_port`

* Override only if you use a reverse proxy. [Docs](https://docs.gitlab.com/omnibus/settings/nginx.html#setting-the-nginx-listen-port)
* Type: Number.
* Default: `80`

`gitlab_ce__rb_nginx_ssl_certificate`

* Path to the SSL certificate.
* Type: String.
* Default: unset

`gitlab_ce__rb_nginx_ssl_certificate_key`

* Path to the SSL certificate key.
* Type: String.
* Default: unset

`gitlab_ce__rb_registry_external_url`

* The URL of the GitLab Container registry.
* Type: String.
* Default: unset

`gitlab_ce__rb_registry_nginx_enable`

* Set this to `true` to enable the GitLab Container Registry.
* Type: Bool.
* Default: unset

`gitlab_ce__rb_registry_nginx_listen_https`

* Set this to `false` only if your reverse proxy internally communicates over HTTP. [Docs](https://docs.gitlab.com/omnibus/settings/nginx.html#supporting-proxied-ssl)
* Type: Bool.
* Default: `false`

`gitlab_ce__rb_registry_nginx_listen_port`

* The port on which the Container Registry is listening.
* Type: Number.
* Default: `5050`

`gitlab_ce__rb_registry_nginx_proxy_set_headers`

* Nginx headers for the Container Registry.
* Type: Dictionary.
* Default: `{'X-Forwarded-Proto': 'https', 'X-Forwarded-Ssl': 'on'}`

`gitlab_ce__version`

* The GitLab version to install. This is useful when restoring from a backup. When unset, the latest available version is used.
* Type: String.
* Default: unset

Example (GitLab running on port 80 behind a reverse proxy, offering Google Authentication, with Matomo integration, plus running a registry):
```yaml
# optional
gitlab_ce__on_calendar: '*:0/15'  # every 15 minutes

gitlab_ce__rb_git_data_dirs_default_path: '/data/gitlab/git-data'

gitlab_ce__rb_gitlab_rails_backup_keep_time: 86400
gitlab_ce__rb_gitlab_rails_backup_path: '/backup/gitlab'

gitlab_ce__rb_gitlab_rails_gitlab_email_display_name: 'My GitLab'
gitlab_ce__rb_gitlab_rails_gitlab_email_from: 'vcs@example.com'
gitlab_ce__rb_gitlab_rails_gitlab_email_reply_to: 'no-reply@example.com'

gitlab_ce__rb_gitlab_rails_gitlab_default_projects_features_builds: false
gitlab_ce__rb_gitlab_rails_gitlab_default_projects_features_container_registry: false
gitlab_ce__rb_gitlab_rails_gitlab_default_projects_features_issues: true
gitlab_ce__rb_gitlab_rails_gitlab_default_projects_features_merge_requests: true
gitlab_ce__rb_gitlab_rails_gitlab_default_projects_features_snippets: false
gitlab_ce__rb_gitlab_rails_gitlab_default_projects_features_wiki: false

gitlab_ce__rb_gitlab_rails_extra_matomo_site_id: '4711'
gitlab_ce__rb_gitlab_rails_extra_matomo_url: 'analytics.example.com/'

gitlab_ce__rb_gitlab_rails_ldap_enabled: true
gitlab_ce__rb_gitlab_rails_ldap_servers:
  main:
    label: 'LDAP'
    host: 'ldap.example.com'
    port: 636
    uid: 'sAMAccountName'
    bind_dn: 'CN=Gitlab,OU=Users,DC=example,DC=com'
    password: '<bind_user_password>'
    encryption: 'simple_tls'
    verify_certificates: true
    timeout: 10
    active_directory: false
    user_filter: '(employeeType=developer)'
    base: 'dc=example,dc=com'
    lowercase_usernames: false
    retry_empty_result_with_codes: [80]
    allow_username_or_email_login: false
    block_auto_created_users: false

gitlab_ce__rb_gitlab_rails_omniauth_allow_single_sign_on:
  - 'google_oauth2'
gitlab_ce__rb_gitlab_rails_omniauth_auto_link_ldap_user: false
gitlab_ce__rb_gitlab_rails_omniauth_block_auto_created_users: false
gitlab_ce__rb_gitlab_rails_omniauth_enabled: true
gitlab_ce__rb_gitlab_rails_omniauth_external_providers:
  - 'google_oauth2'
gitlab_ce__rb_gitlab_rails_omniauth_providers:
  - name: 'google_oauth2'
    app_id: '1095d5c3-8428-44df-89fb-cb0a77ec363f.apps.googleusercontent.com'
    app_secret: '45d85464-bc66-4236-9931-c42394f5d08e'

gitlab_ce__rb_gitlab_rails_rack_attack_git_basic_auth_bantime: 3600
gitlab_ce__rb_gitlab_rails_rack_attack_git_basic_auth_enabled: true
gitlab_ce__rb_gitlab_rails_rack_attack_git_basic_auth_findtime: 60
gitlab_ce__rb_gitlab_rails_rack_attack_git_basic_auth_ip_whitelist:
  - '127.0.0.1'
gitlab_ce__rb_gitlab_rails_rack_attack_git_basic_auth_maxretry: 10

gitlab_ce__rb_gitlab_rails_time_zone: 'Europe/Zurich'

gitlab_ce__rb_letsencrypt_enable: false

gitlab_ce__rb_nginx_listen_port: '80'
gitlab_ce__rb_nginx_ssl_certificate: '/etc/pki/tls/certs/git.example.com.crt'
gitlab_ce__rb_nginx_ssl_certificate_key: '/etc/pki/tls/private/git.example.com.key'
gitlab_ce__rb_registry_external_url: 'https://registry.example.com'
gitlab_ce__rb_registry_nginx_enable: true
gitlab_ce__rb_registry_nginx_listen_https: false
gitlab_ce__rb_registry_nginx_listen_port: 5050
gitlab_ce__rb_registry_nginx_proxy_set_headers:
  'X-Forwarded-Proto': 'https'
  'X-Forwarded-Ssl': 'on'

gitlab_ce__version: '14.8.2'
```


## License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
