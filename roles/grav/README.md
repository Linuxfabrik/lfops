# Ansible Role linuxfabrik.lfops.grav

This role installs Grav (a simple file-based flat-file CMS platform) using PHP composer. For keeping Grav, Plugins and Themes up to date the role configures the Grav Package Manager (GPM).

It is possible to configure whether the Grav Admin Panel should be installed (it is installed by default). By default, you can access the admin by pointing your browser to http://grav.example.com/admin. You can simply log in with the username and password set in the role variables.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Install a web server (for example Apache httpd), and configure a virtual host for Grav. This can be done using the [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role.
* Install PHP 7.3.6+ (**PHP 8.1 recommended** (20220930)). This can be done using the [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) and [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role.

If you use the ["Grav" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/grav.yml), this is automatically done for you.


## Tags

| Tag         | What it does                 |
| ---         | ------------                 |
| `grav`      | * Install unzip<br> * Test if Grav is already installed<br> * `composer create-project getgrav/grav {{ grav__install_dir }}`<br> * `chown -R apache:apache {{ grav__install_dir }}`<br> * `find {{ grav__install_dir }} -type f -exec chmod --changes 664 {} \;`<br> * `find {{ grav__install_dir }}/bin -type f -exec chmod --changes 775 {} \;`<br> * `find {{ grav__install_dir }} -type d -exec chmod --changes 775 {} \;`<br> * `find {{ grav__install_dir }} -type d -exec chmod --changes +s {} \;`<br> * Deploy `/etc/systemd/system/grav-selfupgrade.service`<br> * Deploy `/etc/systemd/system/grav-selfupgrade.timer`<br> * Deploy `/etc/systemd/system/grav-update.service`<br> * Deploy `/etc/systemd/system/grav-update.timer`<br> * `systemctl enable/disable grav-selfupgrade.timer --now`<br> * `systemctl enable/disable grav-update.timer --now`<br> * Install the Administration Panel plugin for Grav<br> * Create Grav User Accounts |
| `grav:cron` | * Deploy `/etc/systemd/system/grav-selfupgrade.service`<br> * Deploy `/etc/systemd/system/grav-selfupgrade.timer`<br> * Deploy `/etc/systemd/system/grav-update.service`<br> * Deploy `/etc/systemd/system/grav-update.timer`<br> * `systemctl enable/disable grav-selfupgrade.timer --now`<br> * `systemctl enable/disable grav-update.timer --now` |
| `grav:state` | * `systemctl enable/disable grav-selfupgrade.timer --now`<br> * `systemctl enable/disable grav-update.timer --now` |
| `grav:user` | * Install the Administration Panel plugin for Grav<br> * Create Grav User Accounts |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `grav__url` | The Grav URL, without `http://` or `https://`.  |
| `grav__users` | List. Mandatory if using the Grav Admin Panel. Have a look at the example below for defining a user. The `permissions` key can be either `a` for Admin access only, `s` for Site access only and `b` for both Admin and Site access. |

Example:
```yaml
# mandatory
grav__url: 'grav.example.com'
grav__users:
  - user: 'firstname_lastname'
    fullname: 'Firstname Lastname'
    password: 'linuxfabrik'
    email: 'firstname.lastname@example.com'
    permissions: 'b'
```


## Optional Role Variables

| Variable | Description | Default Value |
| -------- | ----------- | ------------- |
| `grav__install_dir` | Grav installation directory. | `'/var/www/html/{{ grav__url }}'` |
| `grav__on_calendar_selfupgrade` | Time to upgrading Grav CMS (Systemd-Timer notation). | `'22:{{ 59 \| random(seed=inventory_hostname) }}'` |
| `grav__on_calendar_update` | Time to update Grav Plugins and Themes (Systemd-Timer notation). | `'23:{{ 59 \| random(seed=inventory_hostname) }}'` |
| `grav__skip_admin` | Bool. If set to `true`, installation of the Admin Panel plugin will be skipped. | `false` |
| `grav__timer_selfupgrade_enabled` | Enables/disables Systemd-Timer for upgrading Grav CMS. | `true` |
| `grav__timer_update_enabled` | Enables/disables Systemd-Timer for updating Grav Plugins and Themes. | `true` |


# Known Limitations

There might be more to implement:

* https://learn.getgrav.org/17/security/configuration


# License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
