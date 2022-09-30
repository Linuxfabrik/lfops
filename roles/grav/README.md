# Ansible Role linuxfabrik.lfops.grav

This role installs Grav (a simple file-based flat-file CMS platform) using PHP composer. For keeping Grav, Plugins and Themes up to date the role configures the Grav Package Manager (GPM).

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Install a web server (for example Apache httpd), and configure a virtual host for Grav. This can be done using the [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role.
* Install PHP 7.3.6+ (**PHP 8.1 recommended** (20220930)). This can be done using the [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) and [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role.

If you use the ["Grav" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/grav.yml), this is automatically done for you.


## Tags

| Tag         | What it does                 |
| ---         | ------------                 |
| `grav`      | * Clone and install Grav with all dependencies via composer |
| `grav:cron` | * Deploy `/etc/systemd/system/grav-selfupgrade.service`<br> * Deploy `/etc/systemd/system/grav-selfupgrade.timer`<br> * Deploy `/etc/systemd/system/grav-update.service`<br> * Deploy `/etc/systemd/system/grav-update.timer`<br> * `systemctl enable/disable grav-selfupgrade.timer --now`<br> * `systemctl enable/disable grav-update.timer --now` |
| `grav:state` | * `systemctl enable/disable grav-selfupgrade.timer --now`<br> * `systemctl enable/disable grav-update.timer --now` |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `grav__url` | The Grav URL, without `http://` or `https://`.  |

Example:
```yaml
# mandatory
grav__url: 'grav.example.com'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `grav__on_calendar_selfupgrade` | Time to upgrading Grav CMS (Systemd-Timer notation). | `'22:{{ 59 \| random(seed=inventory_hostname) }}'` |
| `grav__on_calendar_update` | Time to update Grav Plugins and Themes (Systemd-Timer notation). | `'23:{{ 59 \| random(seed=inventory_hostname) }}'` |
| `grav__timer_selfupgrade_enabled` | Enables/disables Systemd-Timer for upgrading Grav CMS. | `true` |
| `grav__timer_update_enabled` | Enables/disables Systemd-Timer for updating Grav Plugins and Themes. | `true` |


# License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
