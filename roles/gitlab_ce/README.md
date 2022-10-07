# Ansible Role linuxfabrik.lfops.gitlab_ce

This role installs and configures [GitLab CE](https://about.gitlab.com/), including regular backups. After installation, the password for the first user "root" can be found in `/etc/gitlab/initial_root_password`.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Enable the official GitLab CE Repository. This can be done using the [linuxfabrik.lfops.repo_gitlab_ce](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_gitlab_ce) role.

If you use the [gitlab_ce Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/gitlab_ce.yml), this is automatically done for you.


## Tags

| Tag                   | What it does                           |
| ---                   | ------------                           |
| `gitlab_ce`           | * `install tar gitlab-ce`<br> * `mkdir -p /backup/gitlab`<br> * Deploy `/etc/systemd/system/gitlab-dump.service`<br> * Deploy `/etc/systemd/system/gitlab-dump.timer`<br> * `systemctl enable gitlab-dump.timer --now`<br> * Deploy `/etc/gitlab/gitlab.rb`<br> * `gitlab-ctl reconfigure`<br> * `gitlab-ctl restart`
| `gitlab_ce:configure` | Same as above, but without install. |


## Mandatory Role Variables

| Variable              | Description                                                         |
| --------              | -----------                                                         |
| `gitlab_ce__rb_external_url` | The URL of your GitLab instance. Currently, only `http://` is supported by this role. If running behind a reverse proxy or on a trusted network, this is good enough. |

Example:
```yaml
# mandatory
gitlab_ce__rb_external_url: 'http://git.example.com'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `gitlab_ce__on_calendar` | The `OnCalendar` definition for the GitLab Backup. Have a look at `man systemd.time(7)` for the format. | `'*-*-* 23:{{ 59 \| random(seed=inventory_hostname) }}'` |
| `gitlab_ce__rb_git_data_dirs_default_path` | For setting up different data storing directory. If missing, the directory will be created by GitLab. If you want to use a single non-default directory to store git data use a path that doesn't contain symlinks. [Docs](https://docs.gitlab.com/omnibus/settings/configuration.html#store-git-data-in-an-alternative-directory) | unset |
| `gitlab_ce__rb_gitlab_rails_backup_keep_time` | The duration in seconds to keep backups before they are allowed to be deleted | `86400` (24h) |
| `gitlab_ce__rb_gitlab_rails_backup_path` | Backup Settings. [Docs](https://docs.gitlab.com/omnibus/settings/backups.html) | `'/backup/gitlab'` |
| `gitlab_ce__rb_gitlab_rails_extra_matomo_site_id` | Extra customization for Matomo | unset |
| `gitlab_ce__rb_gitlab_rails_extra_matomo_url` | Extra customization for Matomo | unset |
| `gitlab_ce__rb_gitlab_rails_gitlab_email_display_name` | | `'GitLab@{{ inventory_hostname }}'` |
| `gitlab_ce__rb_gitlab_rails_gitlab_email_from` | If your SMTP server does not like the default 'From: gitlab@gitlab.example.com', you can change the 'From' with this setting. | `'{{ mailto_root__from \| d("") }}'` |
| `gitlab_ce__rb_gitlab_rails_omniauth_allow_single_sign_on` | OmniAuth Settings. [Docs](https://docs.gitlab.com/ee/integration/omniauth.html) | unset |
| `gitlab_ce__rb_gitlab_rails_omniauth_auto_link_ldap_user` | OmniAuth Settings. [Docs](https://docs.gitlab.com/ee/integration/omniauth.html) | unset |
| `gitlab_ce__rb_gitlab_rails_omniauth_block_auto_created_users` | OmniAuth Settings. [Docs](https://docs.gitlab.com/ee/integration/omniauth.html) | unset |
| `gitlab_ce__rb_gitlab_rails_omniauth_enabled` | OmniAuth Settings. [Docs](https://docs.gitlab.com/ee/integration/omniauth.html) | unset |
| `gitlab_ce__rb_gitlab_rails_omniauth_external_providers` | OmniAuth Settings. [Docs](https://docs.gitlab.com/ee/integration/omniauth.html) | unset |
| `gitlab_ce__rb_gitlab_rails_omniauth_providers` | OmniAuth Settings. [Docs](https://docs.gitlab.com/ee/integration/omniauth.html) | unset |
| `gitlab_ce__rb_gitlab_rails_rack_attack_git_basic_auth_bantime` | Ban an IP for x seconds after too many auth attempts | `3600` (1h) |
| `gitlab_ce__rb_gitlab_rails_rack_attack_git_basic_auth_enabled` |  | `true` |
| `gitlab_ce__rb_gitlab_rails_rack_attack_git_basic_auth_findtime` | Reset the auth attempt counter per IP after x seconds | `60` |
| `gitlab_ce__rb_gitlab_rails_rack_attack_git_basic_auth_ip_whitelist` |  | `['127.0.0.1']` |
| `gitlab_ce__rb_gitlab_rails_rack_attack_git_basic_auth_maxretry` | Limit the number of Git HTTP authentication attempts per IP | `10` |
| `gitlab_ce__rb_gitlab_rails_time_zone` | [Docs](https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/doc/settings/gitlab.yml.md) | `'Europe/Zurich'` |
| `gitlab_ce__rb_letsencrypt_enable` | If GitLab should manage Let's Encrypt certificates itself | `false` |
| `gitlab_ce__rb_nginx_listen_https` | Set this to `false` only if your reverse proxy internally communicates over HTTP. [Docs](https://docs.gitlab.com/omnibus/settings/nginx.html#supporting-proxied-ssl) | unset |
| `gitlab_ce__rb_nginx_listen_port` | Override only if you use a reverse proxy. [Docs](https://docs.gitlab.com/omnibus/settings/nginx.html#setting-the-nginx-listen-port) | unset |
| `gitlab_ce__rb_registry_external_url` | The URL of the GitLab Container registry. | unset |
| `gitlab_ce__rb_registry_nginx_enable` | Set this to `true` to enable the GitLab Container Registry. | unset |
| `gitlab_ce__rb_registry_nginx_listen_https` | Set this to `false` only if your reverse proxy internally communicates over HTTP. [Docs](https://docs.gitlab.com/omnibus/settings/nginx.html#supporting-proxied-ssl) | unset |
| `gitlab_ce__rb_registry_nginx_listen_port` | The port on which the Container Registry is listening. | unset |
| `gitlab_ce__rb_registry_nginx_proxy_set_headers` | Nginx headers for the Container Registry. | unset |
| `gitlab_ce__version` | The GitLab version to install. This is useful when restoring from a backup. When unset, the latest available version is used. | unset |

Example (GitLab running on port 80 behind a reverse proxy, offering Google Authentication, with Matomo integration, plus running a registry):
```yaml
# optional
gitlab_ce__on_calendar: '*:0/15'  # every 15 minutes

gitlab_ce__rb_git_data_dirs_default_path: '/data/gitlab/git-data'

gitlab_ce__rb_gitlab_rails_backup_keep_time: 86400
gitlab_ce__rb_gitlab_rails_backup_path: '/backup/gitlab'

gitlab_ce__rb_gitlab_rails_gitlab_email_display_name: 'My GitLab'
gitlab_ce__rb_gitlab_rails_gitlab_email_from: 'noreply@example.com'

gitlab_ce__rb_gitlab_rails_extra_matomo_site_id: '4711'
gitlab_ce__rb_gitlab_rails_extra_matomo_url: 'analytics.example.com/'

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
gitlab_ce__rb_nginx_listen_port: false
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
