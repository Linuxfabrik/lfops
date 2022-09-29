# Ansible Role linuxfabrik.lfops.grav

This role installs Grav (a simple file-based flat-file CMS platform) using PHP composer.

Runs on

* RHEL 8 (and compatible)


## Mandatory Requirements

* Install a web server (for example Apache httpd), and configure a virtual host for Nextcloud. This can be done using the [linuxfabrik.lfops.apache_httpd](https://github.com/Linuxfabrik/lfops/tree/main/roles/apache_httpd) role.
* Install PHP 7+ (**PHP 8.1 recommended** (20220930)). This can be done using the [linuxfabrik.lfops.repo_remi](https://github.com/Linuxfabrik/lfops/tree/main/roles/repo_remi) and [linuxfabrik.lfops.php](https://github.com/Linuxfabrik/lfops/tree/main/roles/php) role.

If you use the ["Grav" Playbook](https://github.com/Linuxfabrik/lfops/blob/main/playbooks/grav.yml), this is automatically done for you.


## Tags

| Tag       | What it does                 |
| ---       | ------------                 |
| `grav`    | * Clone and install Grav with all dependencies via composer |


## Mandatory Role Variables

| Variable | Description |
| -------- | ----------- |
| `grav__url` | The Grav URL, without `http://` or `https://`.  |

Example:
```yaml
# mandatory
grav__url: 'grav.example.com'
```


# License

[The Unlicense](https://unlicense.org/)


## Author Information

[Linuxfabrik GmbH, Zurich](https://www.linuxfabrik.ch)
